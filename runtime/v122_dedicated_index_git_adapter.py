#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
import shutil
import subprocess

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_dedicated_index_types_v1_22 import (
    DedicatedIndexGitCommandReceipt,
    RepositoryDedicatedIndexPolicy,
    dedicated_index_git_command_receipt_digest,
)


def dedicated_index_path(root: Path, filename: str) -> Path:
    return root / ".git" / filename


def _sanitized_environment(index_path: Path) -> dict[str, str]:
    env = {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("GIT_")
    }
    env["GIT_INDEX_FILE"] = str(index_path)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["LC_ALL"] = "C"
    env["LANG"] = "C"
    return env


def run_dedicated_index_git_command(
    root: Path,
    index_path: Path,
    arguments: tuple[str, ...],
    policy: RepositoryDedicatedIndexPolicy,
    *,
    sequence_number: int,
    operation: str,
    mutating: bool,
    git_executable: str,
) -> tuple[DedicatedIndexGitCommandReceipt, bytes, bytes]:
    if git_executable != "git":
        raise ValueError("v122_git_executable_not_allowed")
    resolved = shutil.which("git")
    fixed_shape = bool(
        resolved
        and (
            (
                operation == "read-tree"
                and len(arguments) == 2
                and arguments[0] == "read-tree"
            )
            or (
                operation == "verify-index"
                and arguments == ("ls-files", "--stage", "-z")
            )
        )
    )
    argv = (
        resolved or "git",
        "--no-optional-locks",
        "-C",
        str(root),
        *arguments,
    )
    timed_out = False
    try:
        completed = subprocess.run(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            shell=False,
            timeout=policy.max_command_timeout_seconds,
            env=_sanitized_environment(index_path),
        )
        return_code = completed.returncode
        stdout = completed.stdout or b""
        stderr = completed.stderr or b""
    except subprocess.TimeoutExpired as error:
        timed_out = True
        return_code = -124
        stdout = error.stdout or b""
        stderr = error.stderr or b""
    except OSError as error:
        return_code = -127
        stdout = b""
        stderr = str(error).encode("utf-8", errors="replace")
    receipt = DedicatedIndexGitCommandReceipt(
        sequence_number=sequence_number,
        operation=operation,
        argv=argv,
        cwd_digest=canonical_digest({"cwd": str(root)}),
        index_path_digest=canonical_digest({"index_path": str(index_path)}),
        return_code=return_code,
        stdout_digest=canonical_digest({"stdout_hex": stdout.hex()}),
        stderr_digest=canonical_digest({"stderr_hex": stderr.hex()}),
        stdout_size_bytes=len(stdout),
        stderr_size_bytes=len(stderr),
        timed_out=timed_out,
        shell_used=False,
        mutating_command=mutating,
        fixed_argument_shape=fixed_shape,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=dedicated_index_git_command_receipt_digest(receipt),
    )
    return receipt, stdout, stderr
