#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import (
    RepositoryTreeCommitMaterializationPolicy,
    TreeCommitGitCommandReceipt,
    tree_commit_git_command_receipt_digest,
)
from runtime.v119_missing_object_diagnostic import is_missing_object_diagnostic

_HEX40 = re.compile(r"^[0-9a-f]{40}$")


def _allowed_shape(arguments: tuple[str, ...]) -> bool:
    if arguments in (
        ("rev-parse", "--show-object-format"),
        ("mktree",),
        ("hash-object", "-t", "commit", "--stdin"),
        ("hash-object", "-t", "commit", "-w", "--stdin"),
    ):
        return True
    return bool(
        len(arguments) == 3
        and arguments[0] == "cat-file"
        and arguments[1] in ("-e", "-t", "-s", "blob", "tree", "commit")
        and _HEX40.fullmatch(arguments[2])
    )


def run_bounded_tree_commit_git_command(
    root: Path,
    arguments: tuple[str, ...],
    stdin: bytes,
    policy: RepositoryTreeCommitMaterializationPolicy,
    *,
    sequence_number: int,
    operation: str,
    mutating: bool,
    git_executable: str,
) -> tuple[TreeCommitGitCommandReceipt, bytes, bytes]:
    resolved = shutil.which(git_executable)
    executable_allowed = bool(
        git_executable == "git"
        and resolved
        and Path(git_executable).name in policy.allowed_git_executable_names
    )
    fixed_shape = bool(executable_allowed and _allowed_shape(arguments))
    argv = (
        resolved or git_executable,
        "--no-optional-locks",
        "-C",
        str(root),
        *arguments,
    )
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["LC_ALL"] = "C"
    env["LANG"] = "C"
    timed_out = False
    if not fixed_shape:
        return_code = -126
        stdout = b""
        stderr = b"v120 command shape rejected"
    else:
        try:
            completed = subprocess.run(
                argv,
                input=stdin,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                shell=False,
                timeout=policy.max_command_timeout_seconds,
                env=env,
            )
            return_code = completed.returncode
            stdout = completed.stdout or b""
            stderr = completed.stderr or b""
            if (
                arguments[0:2] == ("cat-file", "-e")
                and return_code != 0
                and is_missing_object_diagnostic(stderr)
            ):
                return_code = 1
        except subprocess.TimeoutExpired as error:
            timed_out = True
            return_code = -124
            stdout = error.stdout or b""
            stderr = error.stderr or b""
        except OSError as error:
            return_code = -127
            stdout = b""
            stderr = str(error).encode("utf-8", errors="replace")
    receipt = TreeCommitGitCommandReceipt(
        sequence_number=sequence_number,
        operation=operation,
        argv=argv,
        cwd_digest=canonical_digest({"cwd": str(root)}),
        stdin_digest=hashlib.sha256(stdin).hexdigest(),
        stdin_size_bytes=len(stdin),
        return_code=return_code,
        stdout_digest=hashlib.sha256(stdout).hexdigest(),
        stderr_digest=hashlib.sha256(stderr).hexdigest(),
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
        receipt_digest=tree_commit_git_command_receipt_digest(receipt),
    )
    return receipt, stdout, stderr
