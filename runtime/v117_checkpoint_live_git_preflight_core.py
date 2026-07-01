#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
import re
import shutil
import subprocess

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_checkpoint_atomic_cas_transition_types_v1_16 import (
    TRANSITION_COMMITTED,
    RepositoryCheckpointAtomicCasTransitionResult,
)
from runtime.kuuos_repository_checkpoint_atomic_cas_transition_v1_16 import (
    repository_checkpoint_atomic_cas_transition_result_issues,
)
from runtime.kuuos_repository_checkpoint_live_git_preflight_types_v1_17 import (
    PREFLIGHT_ERROR,
    PREFLIGHT_READY,
    PREFLIGHT_REJECTED,
    LiveGitCommandReceipt,
    RepositoryCheckpointLiveGitPreflightPolicy,
    RepositoryCheckpointLiveGitPreflightReceipt,
    RepositoryCheckpointLiveGitPreflightRequest,
    live_git_command_receipt_digest,
    repository_checkpoint_live_git_preflight_policy_digest,
    repository_checkpoint_live_git_preflight_receipt_digest,
    repository_checkpoint_live_git_preflight_request_digest,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_CHECKPOINT_REF = re.compile(r"^refs/kuuos/checkpoints/[A-Za-z0-9._/-]+$")
_ALLOWED_SUBCOMMANDS = ("cat-file", "rev-parse", "show-ref", "symbolic-ref")


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def _valid_oid(value: str) -> bool:
    return bool(_HEX40.fullmatch(value) and value != "0" * 40)


def _valid_checkpoint_reference(value: str) -> bool:
    return bool(
        _CHECKPOINT_REF.fullmatch(value)
        and ".." not in value
        and "//" not in value
        and not value.endswith("/")
        and "\x00" not in value
    )


def build_repository_checkpoint_live_git_preflight_policy(
    policy_id: str,
    *,
    max_command_timeout_seconds: int = 10,
    max_command_count: int = 8,
    max_output_bytes: int = 16384,
) -> RepositoryCheckpointLiveGitPreflightPolicy:
    policy = RepositoryCheckpointLiveGitPreflightPolicy(
        policy_id=policy_id,
        allowed_git_executable_names=("git",),
        allowed_read_only_subcommands=_ALLOWED_SUBCOMMANDS,
        max_command_timeout_seconds=max_command_timeout_seconds,
        max_command_count=max_command_count,
        max_output_bytes=max_output_bytes,
        require_optional_locks_disabled=True,
        require_no_shell=True,
        require_checkpoint_namespace=True,
        require_committed_v116_transition=True,
        live_git_read_only_enabled=True,
        allow_live_git_mutation=False,
        allow_object_write=False,
        allow_index_write=False,
        allow_working_tree_write=False,
        allow_reflog_write=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_live_git_preflight_policy_digest(policy),
    )
    issues = repository_checkpoint_live_git_preflight_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_live_git_preflight_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_live_git_preflight_policy_issues(
    policy: RepositoryCheckpointLiveGitPreflightPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_live_git_preflight_policy_id_missing")
    if policy.allowed_git_executable_names != _canonical(
        policy.allowed_git_executable_names
    ) or policy.allowed_git_executable_names != ("git",):
        issues.append("checkpoint_live_git_preflight_executable_allowlist_invalid")
    if policy.allowed_read_only_subcommands != _ALLOWED_SUBCOMMANDS:
        issues.append("checkpoint_live_git_preflight_subcommand_allowlist_invalid")
    if min(
        policy.max_command_timeout_seconds,
        policy.max_command_count,
        policy.max_output_bytes,
    ) <= 0:
        issues.append("checkpoint_live_git_preflight_bound_invalid")
    if policy.max_command_count < 7:
        issues.append("checkpoint_live_git_preflight_command_count_too_small")
    if not all(
        (
            policy.require_optional_locks_disabled,
            policy.require_no_shell,
            policy.require_checkpoint_namespace,
            policy.require_committed_v116_transition,
            policy.live_git_read_only_enabled,
        )
    ):
        issues.append("checkpoint_live_git_preflight_required_guard_disabled")
    if any(
        (
            policy.allow_live_git_mutation,
            policy.allow_object_write,
            policy.allow_index_write,
            policy.allow_working_tree_write,
            policy.allow_reflog_write,
        )
    ):
        issues.append("checkpoint_live_git_preflight_write_capability_enabled")
    if policy.policy_digest != repository_checkpoint_live_git_preflight_policy_digest(
        policy
    ):
        issues.append("checkpoint_live_git_preflight_policy_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_live_git_preflight_request(
    preflight_id: str,
    repository_path: str,
    transition: RepositoryCheckpointAtomicCasTransitionResult,
    *,
    requested_at_epoch_seconds: int,
) -> RepositoryCheckpointLiveGitPreflightRequest:
    request = RepositoryCheckpointLiveGitPreflightRequest(
        preflight_id=preflight_id,
        repository_path=repository_path,
        repository_id=transition.repository_id,
        git_dir_fingerprint=transition.git_dir_fingerprint,
        checkpoint_reference=transition.checkpoint_reference,
        expected_current_oid=transition.expected_current_oid,
        proposed_checkpoint_oid=transition.proposed_checkpoint_oid,
        transition_result_digest=transition.result_digest,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=repository_checkpoint_live_git_preflight_request_digest(request),
    )
    issues = repository_checkpoint_live_git_preflight_request_issues(request)
    if issues:
        raise ValueError(f"checkpoint_live_git_preflight_request_invalid:{issues[0]}")
    return request


def repository_checkpoint_live_git_preflight_request_issues(
    request: RepositoryCheckpointLiveGitPreflightRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    if any(
        not value
        for value in (
            request.preflight_id,
            request.repository_path,
            request.repository_id,
            request.git_dir_fingerprint,
            request.checkpoint_reference,
            request.transition_result_digest,
        )
    ):
        issues.append("checkpoint_live_git_preflight_required_field_missing")
    if "\x00" in request.repository_path:
        issues.append("checkpoint_live_git_preflight_repository_path_invalid")
    if not _HEX64.fullmatch(request.git_dir_fingerprint):
        issues.append("checkpoint_live_git_preflight_git_dir_fingerprint_invalid")
    if not _HEX64.fullmatch(request.transition_result_digest):
        issues.append("checkpoint_live_git_preflight_transition_digest_invalid")
    if not _valid_checkpoint_reference(request.checkpoint_reference):
        issues.append("checkpoint_live_git_preflight_reference_invalid")
    if not _valid_oid(request.expected_current_oid) or not _valid_oid(
        request.proposed_checkpoint_oid
    ):
        issues.append("checkpoint_live_git_preflight_oid_invalid")
    if request.expected_current_oid == request.proposed_checkpoint_oid:
        issues.append("checkpoint_live_git_preflight_oid_not_distinct")
    if request.requested_at_epoch_seconds < 0:
        issues.append("checkpoint_live_git_preflight_request_time_invalid")
    if request.request_digest != repository_checkpoint_live_git_preflight_request_digest(
        request
    ):
        issues.append("checkpoint_live_git_preflight_request_digest_mismatch")
    return tuple(issues)


def _command_shape_is_read_only(
    arguments: tuple[str, ...], request: RepositoryCheckpointLiveGitPreflightRequest
) -> bool:
    allowed = {
        ("rev-parse", "--show-toplevel"),
        ("rev-parse", "--git-dir"),
        ("rev-parse", "--is-bare-repository"),
        ("symbolic-ref", "-q", request.checkpoint_reference),
        ("show-ref", "--verify", "--hash", request.checkpoint_reference),
        ("cat-file", "-e", f"{request.expected_current_oid}^{{commit}}"),
        ("cat-file", "-e", f"{request.proposed_checkpoint_oid}^{{commit}}"),
    }
    return arguments in allowed


def _run_read_only_git(
    root: Path,
    arguments: tuple[str, ...],
    request: RepositoryCheckpointLiveGitPreflightRequest,
    policy: RepositoryCheckpointLiveGitPreflightPolicy,
    *,
    sequence_number: int,
    git_executable: str,
) -> tuple[LiveGitCommandReceipt, str, str]:
    resolved_executable = shutil.which(git_executable)
    executable_name = Path(git_executable).name
    read_only = bool(
        resolved_executable
        and executable_name in policy.allowed_git_executable_names
        and arguments
        and arguments[0] in policy.allowed_read_only_subcommands
        and _command_shape_is_read_only(arguments, request)
    )
    argv = (
        resolved_executable or git_executable,
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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            shell=False,
            timeout=policy.max_command_timeout_seconds,
            env=env,
        )
        return_code = completed.returncode
        stdout_bytes = completed.stdout or b""
        stderr_bytes = completed.stderr or b""
    except subprocess.TimeoutExpired as error:
        timed_out = True
        return_code = -124
        stdout_bytes = error.stdout or b""
        stderr_bytes = error.stderr or b""
    except OSError as error:
        return_code = -127
        stdout_bytes = b""
        stderr_bytes = str(error).encode("utf-8", errors="replace")
    stdout = stdout_bytes.decode("utf-8", errors="replace")
    stderr = stderr_bytes.decode("utf-8", errors="replace")
    receipt = LiveGitCommandReceipt(
        sequence_number=sequence_number,
        argv=argv,
        cwd_digest=canonical_digest({"cwd": str(root)}),
        return_code=return_code,
        stdout_digest=canonical_digest({"stdout": stdout}),
        stderr_digest=canonical_digest({"stderr": stderr}),
        stdout_size_bytes=len(stdout_bytes),
        stderr_size_bytes=len(stderr_bytes),
        timed_out=timed_out,
        optional_locks_disabled=True,
        shell_used=False,
        read_only_command=read_only,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=live_git_command_receipt_digest(receipt),
    )
    return receipt, stdout, stderr


def execute_repository_checkpoint_live_git_preflight(
    request: RepositoryCheckpointLiveGitPreflightRequest,
    transition: RepositoryCheckpointAtomicCasTransitionResult,
    policy: RepositoryCheckpointLiveGitPreflightPolicy,
    *,
    git_executable: str = "git",
) -> RepositoryCheckpointLiveGitPreflightReceipt:
    policy_valid = not repository_checkpoint_live_git_preflight_policy_issues(policy)
    request_valid = not repository_checkpoint_live_git_preflight_request_issues(request)
    transition_valid = not repository_checkpoint_atomic_cas_transition_result_issues(
        transition
    )
    transition_committed = bool(
        transition_valid
        and transition.status == TRANSITION_COMMITTED
        and transition.transition_committed
        and transition.compare_and_swap_succeeded
        and transition.atomic_reference_nonce_transition
        and transition.nonce_consumed
        and not transition.live_git_command_invoked
        and not transition.live_repository_mutated
    )
    transition_binding_exact = bool(
        request.transition_result_digest == transition.result_digest
        and request.repository_id == transition.repository_id
        and request.git_dir_fingerprint == transition.git_dir_fingerprint
        and request.checkpoint_reference == transition.checkpoint_reference
        and request.expected_current_oid == transition.expected_current_oid
        and request.proposed_checkpoint_oid == transition.proposed_checkpoint_oid
    )
    repository_path = Path(request.repository_path).expanduser()
    repository_path_valid = bool(
        request_valid
        and repository_path.is_absolute()
        and repository_path.exists()
        and repository_path.is_dir()
    )
    resolved_root = repository_path.resolve() if repository_path_valid else repository_path
    commands: list[LiveGitCommandReceipt] = []
    outputs: list[tuple[str, str]] = []
    command_arguments = (
        ("rev-parse", "--show-toplevel"),
        ("rev-parse", "--git-dir"),
        ("rev-parse", "--is-bare-repository"),
        ("symbolic-ref", "-q", request.checkpoint_reference),
        ("show-ref", "--verify", "--hash", request.checkpoint_reference),
        ("cat-file", "-e", f"{request.expected_current_oid}^{{commit}}"),
        ("cat-file", "-e", f"{request.proposed_checkpoint_oid}^{{commit}}"),
    )
    if repository_path_valid and policy_valid and request_valid:
        for sequence, arguments in enumerate(command_arguments, start=1):
            receipt, stdout, stderr = _run_read_only_git(
                resolved_root,
                arguments,
                request,
                policy,
                sequence_number=sequence,
                git_executable=git_executable,
            )
            commands.append(receipt)
            outputs.append((stdout, stderr))

    command_count_valid = bool(
        commands and len(commands) <= policy.max_command_count
    )
    all_commands_bounded = bool(
        command_count_valid
        and all(
            not receipt.timed_out
            and receipt.stdout_size_bytes <= policy.max_output_bytes
            and receipt.stderr_size_bytes <= policy.max_output_bytes
            for receipt in commands
        )
    )
    all_commands_read_only = bool(
        commands and all(receipt.read_only_command for receipt in commands)
    )
    optional_locks_disabled = bool(
        commands and all(receipt.optional_locks_disabled for receipt in commands)
    )
    shell_used = any(receipt.shell_used for receipt in commands)

    root_stdout = outputs[0][0].strip() if len(outputs) > 0 else ""
    git_dir_stdout = outputs[1][0].strip() if len(outputs) > 1 else ""
    bare_stdout = outputs[2][0].strip() if len(outputs) > 2 else ""
    observed_oid = outputs[4][0].strip().lower() if len(outputs) > 4 else ""
    root_rc = commands[0].return_code if len(commands) > 0 else -1
    git_dir_rc = commands[1].return_code if len(commands) > 1 else -1
    bare_rc = commands[2].return_code if len(commands) > 2 else -1
    symbolic_rc = commands[3].return_code if len(commands) > 3 else -1
    show_ref_rc = commands[4].return_code if len(commands) > 4 else -1
    expected_object_rc = commands[5].return_code if len(commands) > 5 else -1
    proposed_object_rc = commands[6].return_code if len(commands) > 6 else -1

    resolved_repository_root = (
        Path(root_stdout).resolve() if root_rc == 0 and root_stdout else None
    )
    repository_root_resolved = bool(
        resolved_repository_root is not None
        and resolved_repository_root == resolved_root
    )
    if git_dir_rc == 0 and git_dir_stdout:
        raw_git_dir = Path(git_dir_stdout)
        resolved_git_dir = (
            raw_git_dir.resolve()
            if raw_git_dir.is_absolute()
            else (resolved_root / raw_git_dir).resolve()
        )
    else:
        resolved_git_dir = None
    git_directory_resolved = bool(
        resolved_git_dir is not None
        and resolved_git_dir.exists()
        and resolved_git_dir.is_dir()
    )
    repository_non_bare = bool(bare_rc == 0 and bare_stdout == "false")
    checkpoint_reference_exists = bool(
        show_ref_rc == 0 and _valid_oid(observed_oid)
    )
    checkpoint_reference_direct = bool(symbolic_rc == 1)
    observed_oid_matches_expected = bool(
        checkpoint_reference_exists and observed_oid == request.expected_current_oid
    )
    expected_object_exists = expected_object_rc == 0
    proposed_object_exists = proposed_object_rc == 0
    checkpoint_reference_valid = _valid_checkpoint_reference(
        request.checkpoint_reference
    )
    command_policy_valid = bool(policy_valid and all_commands_read_only)

    checks = {
        "policy_valid": policy_valid,
        "request_valid": request_valid,
        "transition_valid": transition_valid,
        "transition_committed": transition_committed,
        "transition_binding_exact": transition_binding_exact,
        "repository_path_valid": repository_path_valid,
        "repository_root_resolved": repository_root_resolved,
        "git_directory_resolved": git_directory_resolved,
        "repository_non_bare": repository_non_bare,
        "checkpoint_reference_valid": checkpoint_reference_valid,
        "checkpoint_reference_exists": checkpoint_reference_exists,
        "checkpoint_reference_direct": checkpoint_reference_direct,
        "observed_oid_matches_expected": observed_oid_matches_expected,
        "expected_object_exists": expected_object_exists,
        "proposed_object_exists": proposed_object_exists,
        "command_policy_valid": command_policy_valid,
        "all_commands_bounded": all_commands_bounded,
        "all_commands_read_only": all_commands_read_only,
        "optional_locks_disabled": optional_locks_disabled,
        "no_shell": not shell_used,
        "no_live_repository_mutation": True,
        "no_object_database_write": True,
        "no_index_write": True,
        "no_working_tree_write": True,
        "no_reflog_write": True,
    }
    ready = all(checks.values())
    command_error = any(
        receipt.timed_out or receipt.return_code in (-124, -127)
        for receipt in commands
    )
    status = PREFLIGHT_READY if ready else PREFLIGHT_ERROR if command_error else PREFLIGHT_REJECTED
    reason = (
        "LIVE_GIT_READ_ONLY_PREFLIGHT_READY"
        if ready
        else "LIVE_GIT_COMMAND_ERROR"
        if command_error
        else "LIVE_GIT_PREFLIGHT_CONDITION_REJECTED"
    )
    repository_path_digest = canonical_digest({"path": str(resolved_root)})
    resolved_root_digest = canonical_digest(
        {"root": str(resolved_repository_root) if resolved_repository_root else ""}
    )
    resolved_git_dir_digest = canonical_digest(
        {"git_dir": str(resolved_git_dir) if resolved_git_dir else ""}
    )
    receipt = RepositoryCheckpointLiveGitPreflightReceipt(
        preflight_id=request.preflight_id,
        status=status,
        reason=reason,
        policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        transition_result_digest=transition.result_digest,
        repository_path_digest=repository_path_digest,
        resolved_repository_root_digest=resolved_root_digest,
        resolved_git_dir_digest=resolved_git_dir_digest,
        repository_id=request.repository_id,
        git_dir_fingerprint=request.git_dir_fingerprint,
        checkpoint_reference=request.checkpoint_reference,
        expected_current_oid=request.expected_current_oid,
        observed_current_oid=observed_oid,
        proposed_checkpoint_oid=request.proposed_checkpoint_oid,
        transition_valid=transition_valid,
        transition_committed=transition_committed,
        transition_binding_exact=transition_binding_exact,
        repository_path_valid=repository_path_valid,
        repository_root_resolved=repository_root_resolved,
        git_directory_resolved=git_directory_resolved,
        repository_non_bare=repository_non_bare,
        checkpoint_reference_valid=checkpoint_reference_valid,
        checkpoint_reference_exists=checkpoint_reference_exists,
        checkpoint_reference_direct=checkpoint_reference_direct,
        observed_oid_matches_expected=observed_oid_matches_expected,
        expected_object_exists=expected_object_exists,
        proposed_object_exists=proposed_object_exists,
        command_policy_valid=command_policy_valid,
        all_commands_bounded=all_commands_bounded,
        all_commands_read_only=all_commands_read_only,
        optional_locks_disabled=optional_locks_disabled,
        shell_used=shell_used,
        live_git_command_invoked=bool(commands),
        live_repository_mutated=False,
        object_database_write_performed=False,
        index_write_performed=False,
        working_tree_write_performed=False,
        reflog_write_performed=False,
        command_receipts=tuple(commands),
        checks=checks,
        evidence_digests={
            "v116_transition": transition.result_digest,
            "preflight_policy": policy.policy_digest,
            "preflight_request": request.request_digest,
            "repository_path": repository_path_digest,
            "resolved_repository_root": resolved_root_digest,
            "resolved_git_directory": resolved_git_dir_digest,
        },
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=repository_checkpoint_live_git_preflight_receipt_digest(
            receipt
        ),
    )
    issues = repository_checkpoint_live_git_preflight_receipt_issues(receipt)
    if issues:
        raise ValueError(f"checkpoint_live_git_preflight_receipt_invalid:{issues[0]}")
    return receipt


def repository_checkpoint_live_git_preflight_receipt_issues(
    receipt: RepositoryCheckpointLiveGitPreflightReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    if receipt.status not in (PREFLIGHT_READY, PREFLIGHT_REJECTED, PREFLIGHT_ERROR):
        issues.append("checkpoint_live_git_preflight_status_invalid")
    ready = all(receipt.checks.values())
    if (receipt.status == PREFLIGHT_READY) != ready:
        issues.append("checkpoint_live_git_preflight_status_check_mismatch")
    if receipt.live_git_command_invoked != bool(receipt.command_receipts):
        issues.append("checkpoint_live_git_preflight_command_invocation_mismatch")
    if receipt.shell_used or any(
        (
            receipt.live_repository_mutated,
            receipt.object_database_write_performed,
            receipt.index_write_performed,
            receipt.working_tree_write_performed,
            receipt.reflog_write_performed,
        )
    ):
        issues.append("checkpoint_live_git_preflight_forbidden_effect")
    for sequence, command in enumerate(receipt.command_receipts, start=1):
        if command.sequence_number != sequence:
            issues.append("checkpoint_live_git_preflight_command_sequence_invalid")
            break
        if command.receipt_digest != live_git_command_receipt_digest(command):
            issues.append("checkpoint_live_git_preflight_command_digest_mismatch")
            break
    if receipt.receipt_digest != repository_checkpoint_live_git_preflight_receipt_digest(
        receipt
    ):
        issues.append("checkpoint_live_git_preflight_receipt_digest_mismatch")
    return tuple(issues)
