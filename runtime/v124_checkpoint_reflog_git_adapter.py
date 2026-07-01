#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
import shutil
import subprocess

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_checkpoint_reflog_types_v1_24 import (
    CheckpointReflogGitCommandReceipt,
    RepositoryCheckpointReflogPolicy,
    RepositoryCheckpointReflogRequest,
    checkpoint_reflog_git_command_receipt_digest,
)


def _controlled_environment(
    request: RepositoryCheckpointReflogRequest,
) -> dict[str, str]:
    env = {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("GIT_")
    }
    identity_date = (
        f"{request.recorded_at_epoch_seconds} {request.timezone_offset}"
    )
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_AUTHOR_NAME"] = request.committer_name
    env["GIT_AUTHOR_EMAIL"] = request.committer_email
    env["GIT_AUTHOR_DATE"] = identity_date
    env["GIT_COMMITTER_NAME"] = request.committer_name
    env["GIT_COMMITTER_EMAIL"] = request.committer_email
    env["GIT_COMMITTER_DATE"] = identity_date
    env["LC_ALL"] = "C"
    env["LANG"] = "C"
    return env


def _fixed_shape(operation: str, arguments: tuple[str, ...], request) -> bool:
    if operation in ("pre-read-ref", "post-read-ref"):
        return bool(
            len(arguments) == 4
            and arguments[0:3] == ("show-ref", "--verify", "--hash")
            and arguments[3] == request.checkpoint_reference
        )
    if operation == "verify-old-object":
        return arguments == (
            "cat-file",
            "-e",
            f"{request.transition_old_oid}^{{object}}",
        )
    if operation == "verify-new-object":
        return arguments == (
            "cat-file",
            "-e",
            f"{request.transition_new_oid}^{{object}}",
        )
    if operation == "write-checkpoint-reflog":
        return arguments == (
            "reflog",
            "write",
            request.checkpoint_reference,
            request.transition_old_oid,
            request.transition_new_oid,
            request.message,
        )
    return False


def run_checkpoint_reflog_git_command(
    root: Path,
    target_reflog_path: Path,
    request: RepositoryCheckpointReflogRequest,
    policy: RepositoryCheckpointReflogPolicy,
    *,
    sequence_number: int,
    operation: str,
    arguments: tuple[str, ...],
    mutating: bool,
    git_executable: str,
):
    if git_executable != "git":
        raise ValueError("v124_git_executable_not_allowed")
    resolved = shutil.which("git")
    executable_allowed = bool(
        resolved
        and Path(git_executable).name in policy.allowed_git_executable_names
    )
    fixed_shape = bool(
        executable_allowed and _fixed_shape(operation, arguments, request)
    )
    argv = (
        resolved or git_executable,
        "--no-optional-locks",
        "-C",
        str(root),
        *arguments,
    )
    env = _controlled_environment(request)
    timed_out = False
    try:
        completed = subprocess.run(
            argv,
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
    receipt = CheckpointReflogGitCommandReceipt(
        sequence_number=sequence_number,
        operation=operation,
        argv=argv,
        cwd_digest=canonical_digest({"cwd": str(root)}),
        environment_digest=canonical_digest(
            {
                "GIT_OPTIONAL_LOCKS": env["GIT_OPTIONAL_LOCKS"],
                "GIT_AUTHOR_NAME": env["GIT_AUTHOR_NAME"],
                "GIT_AUTHOR_EMAIL": env["GIT_AUTHOR_EMAIL"],
                "GIT_AUTHOR_DATE": env["GIT_AUTHOR_DATE"],
                "GIT_COMMITTER_NAME": env["GIT_COMMITTER_NAME"],
                "GIT_COMMITTER_EMAIL": env["GIT_COMMITTER_EMAIL"],
                "GIT_COMMITTER_DATE": env["GIT_COMMITTER_DATE"],
                "LC_ALL": env["LC_ALL"],
                "LANG": env["LANG"],
            }
        ),
        target_ref_digest=canonical_digest(
            {"checkpoint_reference": request.checkpoint_reference}
        ),
        target_reflog_path_digest=canonical_digest(
            {"target_reflog_path": str(target_reflog_path)}
        ),
        return_code=return_code,
        stdout_digest=canonical_digest({"stdout_hex": stdout.hex()}),
        stderr_digest=canonical_digest({"stderr_hex": stderr.hex()}),
        stdout_size_bytes=len(stdout),
        stderr_size_bytes=len(stderr),
        timed_out=timed_out,
        shell_used=False,
        optional_locks_disabled=True,
        mutating_command=mutating,
        fixed_argument_shape=fixed_shape,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=checkpoint_reflog_git_command_receipt_digest(receipt),
    )
    return receipt, stdout.decode("utf-8", errors="replace"), stderr.decode(
        "utf-8", errors="replace"
    )
