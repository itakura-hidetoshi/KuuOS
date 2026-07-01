#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
import shutil
import subprocess

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_sandbox_worktree_types_v1_23 import (
    RepositorySandboxWorktreePolicy,
    SandboxWorktreeGitCommandReceipt,
    sandbox_worktree_git_command_receipt_digest,
)


def _environment(index_path: Path) -> dict[str, str]:
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


def run_sandbox_checkout(
    root: Path,
    index_path: Path,
    sandbox_path: Path,
    sandbox_name: str,
    policy: RepositorySandboxWorktreePolicy,
    *,
    git_executable: str,
):
    if git_executable != "git":
        raise ValueError("v123_git_executable_not_allowed")
    resolved = shutil.which("git")
    arguments = (
        "checkout-index",
        "--all",
        "--force",
        f"--prefix={sandbox_name}/",
    )
    fixed_shape = bool(
        resolved
        and sandbox_name
        and "/" not in sandbox_name
        and "\\" not in sandbox_name
    )
    argv = (resolved or "git", "--no-optional-locks", "-C", str(root), *arguments)
    timed_out = False
    try:
        completed = subprocess.run(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            shell=False,
            timeout=policy.max_command_timeout_seconds,
            env=_environment(index_path),
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
    receipt = SandboxWorktreeGitCommandReceipt(
        sequence_number=1,
        operation="checkout-index",
        argv=argv,
        cwd_digest=canonical_digest({"cwd": str(root)}),
        index_path_digest=canonical_digest({"index_path": str(index_path)}),
        sandbox_path_digest=canonical_digest({"sandbox_path": str(sandbox_path)}),
        return_code=return_code,
        stdout_digest=canonical_digest({"stdout_hex": stdout.hex()}),
        stderr_digest=canonical_digest({"stderr_hex": stderr.hex()}),
        stdout_size_bytes=len(stdout),
        stderr_size_bytes=len(stderr),
        timed_out=timed_out,
        shell_used=False,
        mutating_command=True,
        fixed_argument_shape=fixed_shape,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=sandbox_worktree_git_command_receipt_digest(receipt),
    )
    return receipt
