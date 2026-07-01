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
from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    LiveObjectGitCommandReceipt,
    RepositoryLiveObjectMaterializationPolicy,
    live_object_git_command_receipt_digest,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")


def run_bounded_object_git_command(
    root: Path,
    arguments: tuple[str, ...],
    stdin: bytes,
    policy: RepositoryLiveObjectMaterializationPolicy,
    *,
    sequence_number: int,
    operation: str,
    mutating: bool,
    git_executable: str,
) -> tuple[LiveObjectGitCommandReceipt, bytes, bytes]:
    resolved = shutil.which(git_executable)
    executable_allowed = bool(
        resolved
        and Path(git_executable).name in policy.allowed_git_executable_names
    )
    allowed_shapes = {
        ("rev-parse", "--show-object-format"),
        ("hash-object", "--stdin"),
        ("hash-object", "-w", "--stdin"),
    }
    fixed_shape = bool(
        executable_allowed
        and (
            arguments in allowed_shapes
            or (
                len(arguments) == 3
                and arguments[0] == "cat-file"
                and arguments[1] in ("-e", "-t", "-s", "blob")
                and _HEX40.fullmatch(arguments[2])
            )
        )
    )
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
    except subprocess.TimeoutExpired as error:
        timed_out = True
        return_code = -124
        stdout = error.stdout or b""
        stderr = error.stderr or b""
    except OSError as error:
        return_code = -127
        stdout = b""
        stderr = str(error).encode("utf-8", errors="replace")
    receipt = LiveObjectGitCommandReceipt(
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
        receipt_digest=live_object_git_command_receipt_digest(receipt),
    )
    return receipt, stdout, stderr
