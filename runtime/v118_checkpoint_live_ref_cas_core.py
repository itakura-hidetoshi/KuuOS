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
    PREFLIGHT_READY,
    RepositoryCheckpointLiveGitPreflightPolicy,
    RepositoryCheckpointLiveGitPreflightReceipt,
    RepositoryCheckpointLiveGitPreflightRequest,
)
from runtime.kuuos_repository_checkpoint_live_git_preflight_v1_17 import (
    execute_repository_checkpoint_live_git_preflight,
    repository_checkpoint_live_git_preflight_policy_issues,
    repository_checkpoint_live_git_preflight_receipt_issues,
    repository_checkpoint_live_git_preflight_request_issues,
)
from runtime.kuuos_repository_checkpoint_live_ref_cas_types_v1_18 import (
    LIVE_REF_CAS_ABORTED,
    LIVE_REF_CAS_COMMITTED,
    LIVE_REF_CAS_ERROR,
    LIVE_REF_CAS_REJECTED,
    SANDBOX_MARKER_FILENAME,
    LiveRefCasCommandReceipt,
    RepositoryCheckpointLiveRefCasPolicy,
    RepositoryCheckpointLiveRefCasRequest,
    RepositoryCheckpointLiveRefCasResult,
    live_ref_cas_command_receipt_digest,
    repository_checkpoint_live_ref_cas_policy_digest,
    repository_checkpoint_live_ref_cas_request_digest,
    repository_checkpoint_live_ref_cas_result_digest,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_CHECKPOINT_REF = re.compile(r"^refs/kuuos/checkpoints/[A-Za-z0-9._/-]+$")


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def _valid_checkpoint_reference(value: str) -> bool:
    return bool(
        _CHECKPOINT_REF.fullmatch(value)
        and ".." not in value
        and "//" not in value
        and not value.endswith("/")
        and "\x00" not in value
    )


def _valid_oid(value: str) -> bool:
    return bool(_HEX40.fullmatch(value) and value != "0" * 40)


def repository_path_digest(path: str | Path) -> str:
    return canonical_digest({"path": str(Path(path).expanduser().resolve())})


def build_repository_checkpoint_live_ref_cas_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    allowed_repository_path_digests: tuple[str, ...],
    max_preflight_age_seconds: int = 60,
    max_execution_duration_seconds: int = 30,
    max_command_timeout_seconds: int = 10,
    max_output_bytes: int = 16384,
) -> RepositoryCheckpointLiveRefCasPolicy:
    policy = RepositoryCheckpointLiveRefCasPolicy(
        policy_id=policy_id,
        authorized_executor_ids=_canonical(authorized_executor_ids),
        allowed_repository_path_digests=_canonical(
            allowed_repository_path_digests
        ),
        allowed_git_executable_names=("git",),
        max_preflight_age_seconds=max_preflight_age_seconds,
        max_execution_duration_seconds=max_execution_duration_seconds,
        max_command_timeout_seconds=max_command_timeout_seconds,
        max_output_bytes=max_output_bytes,
        require_ready_v117_preflight=True,
        require_preflight_recomputation=True,
        require_exact_preflight_receipt_match=True,
        require_sandbox_marker=True,
        require_atomic_update_ref=True,
        require_checkpoint_namespace=True,
        require_no_existing_target_reflog=True,
        live_reference_update_enabled=True,
        allow_force_update=False,
        allow_reference_delete=False,
        allow_head_update=False,
        allow_branch_update=False,
        allow_tag_update=False,
        allow_remote_reference_update=False,
        allow_push=False,
        allow_object_database_write=False,
        allow_index_write=False,
        allow_working_tree_write=False,
        allow_reflog_write=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_live_ref_cas_policy_digest(policy),
    )
    issues = repository_checkpoint_live_ref_cas_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_live_ref_cas_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_live_ref_cas_policy_issues(
    policy: RepositoryCheckpointLiveRefCasPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_live_ref_cas_policy_id_missing")
    if policy.authorized_executor_ids != _canonical(
        policy.authorized_executor_ids
    ) or not policy.authorized_executor_ids:
        issues.append("checkpoint_live_ref_cas_executor_allowlist_invalid")
    if policy.allowed_repository_path_digests != _canonical(
        policy.allowed_repository_path_digests
    ) or not policy.allowed_repository_path_digests:
        issues.append("checkpoint_live_ref_cas_repository_allowlist_invalid")
    if any(
        not _HEX64.fullmatch(value)
        for value in policy.allowed_repository_path_digests
    ):
        issues.append("checkpoint_live_ref_cas_repository_digest_invalid")
    if policy.allowed_git_executable_names != ("git",):
        issues.append("checkpoint_live_ref_cas_git_allowlist_invalid")
    if min(
        policy.max_preflight_age_seconds,
        policy.max_execution_duration_seconds,
        policy.max_command_timeout_seconds,
        policy.max_output_bytes,
    ) <= 0:
        issues.append("checkpoint_live_ref_cas_bound_invalid")
    required = (
        policy.require_ready_v117_preflight,
        policy.require_preflight_recomputation,
        policy.require_exact_preflight_receipt_match,
        policy.require_sandbox_marker,
        policy.require_atomic_update_ref,
        policy.require_checkpoint_namespace,
        policy.require_no_existing_target_reflog,
        policy.live_reference_update_enabled,
    )
    if not all(required):
        issues.append("checkpoint_live_ref_cas_required_guard_disabled")
    forbidden = (
        policy.allow_force_update,
        policy.allow_reference_delete,
        policy.allow_head_update,
        policy.allow_branch_update,
        policy.allow_tag_update,
        policy.allow_remote_reference_update,
        policy.allow_push,
        policy.allow_object_database_write,
        policy.allow_index_write,
        policy.allow_working_tree_write,
        policy.allow_reflog_write,
    )
    if any(forbidden):
        issues.append("checkpoint_live_ref_cas_forbidden_capability_enabled")
    if policy.policy_digest != repository_checkpoint_live_ref_cas_policy_digest(
        policy
    ):
        issues.append("checkpoint_live_ref_cas_policy_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_live_ref_cas_request(
    execution_id: str,
    preflight_request: RepositoryCheckpointLiveGitPreflightRequest,
    preflight_receipt: RepositoryCheckpointLiveGitPreflightReceipt,
    transition: RepositoryCheckpointAtomicCasTransitionResult,
    *,
    executor_id: str,
    sandbox_marker_token: str,
    requested_at_epoch_seconds: int,
) -> RepositoryCheckpointLiveRefCasRequest:
    request = RepositoryCheckpointLiveRefCasRequest(
        execution_id=execution_id,
        repository_path=preflight_request.repository_path,
        repository_path_digest=preflight_receipt.repository_path_digest,
        repository_id=transition.repository_id,
        git_dir_fingerprint=transition.git_dir_fingerprint,
        checkpoint_reference=transition.checkpoint_reference,
        expected_current_oid=transition.expected_current_oid,
        proposed_checkpoint_oid=transition.proposed_checkpoint_oid,
        transition_result_digest=transition.result_digest,
        preflight_policy_digest=preflight_receipt.policy_digest,
        preflight_request_digest=preflight_request.request_digest,
        preflight_receipt_digest=preflight_receipt.receipt_digest,
        executor_id=executor_id,
        sandbox_marker_token=sandbox_marker_token,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=repository_checkpoint_live_ref_cas_request_digest(request),
    )
    issues = repository_checkpoint_live_ref_cas_request_issues(request)
    if issues:
        raise ValueError(f"checkpoint_live_ref_cas_request_invalid:{issues[0]}")
    return request


def repository_checkpoint_live_ref_cas_request_issues(
    request: RepositoryCheckpointLiveRefCasRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        request.execution_id,
        request.repository_path,
        request.repository_path_digest,
        request.repository_id,
        request.git_dir_fingerprint,
        request.checkpoint_reference,
        request.transition_result_digest,
        request.preflight_policy_digest,
        request.preflight_request_digest,
        request.preflight_receipt_digest,
        request.executor_id,
        request.sandbox_marker_token,
    )
    if any(not value for value in required):
        issues.append("checkpoint_live_ref_cas_required_field_missing")
    if not Path(request.repository_path).is_absolute() or "\x00" in request.repository_path:
        issues.append("checkpoint_live_ref_cas_repository_path_invalid")
    for digest in (
        request.repository_path_digest,
        request.git_dir_fingerprint,
        request.transition_result_digest,
        request.preflight_policy_digest,
        request.preflight_request_digest,
        request.preflight_receipt_digest,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("checkpoint_live_ref_cas_digest_invalid")
            break
    if not _valid_checkpoint_reference(request.checkpoint_reference):
        issues.append("checkpoint_live_ref_cas_reference_invalid")
    if not _valid_oid(request.expected_current_oid) or not _valid_oid(
        request.proposed_checkpoint_oid
    ):
        issues.append("checkpoint_live_ref_cas_oid_invalid")
    if request.expected_current_oid == request.proposed_checkpoint_oid:
        issues.append("checkpoint_live_ref_cas_oid_not_distinct")
    if not _HEX64.fullmatch(request.sandbox_marker_token):
        issues.append("checkpoint_live_ref_cas_marker_token_invalid")
    if request.requested_at_epoch_seconds < 0:
        issues.append("checkpoint_live_ref_cas_request_time_invalid")
    if request.request_digest != repository_checkpoint_live_ref_cas_request_digest(
        request
    ):
        issues.append("checkpoint_live_ref_cas_request_digest_mismatch")
    return tuple(issues)


def _run_git_command(
    root: Path,
    arguments: tuple[str, ...],
    policy: RepositoryCheckpointLiveRefCasPolicy,
    *,
    sequence_number: int,
    operation: str,
    mutating: bool,
    git_executable: str,
) -> tuple[LiveRefCasCommandReceipt, str, str]:
    resolved_executable = shutil.which(git_executable)
    executable_name = Path(git_executable).name
    executable_allowed = bool(
        resolved_executable
        and executable_name in policy.allowed_git_executable_names
    )
    fixed_shape = bool(
        executable_allowed
        and (
            (
                operation == "atomic-update-ref"
                and len(arguments) == 5
                and arguments[0:2] == ("update-ref", "--no-deref")
            )
            or (
                operation == "post-verify-ref"
                and len(arguments) == 4
                and arguments[0:3] == ("show-ref", "--verify", "--hash")
            )
        )
    )
    argv = (
        resolved_executable or git_executable,
        "--no-optional-locks",
        "-C",
        str(root),
        "-c",
        "core.logAllRefUpdates=false",
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
    receipt = LiveRefCasCommandReceipt(
        sequence_number=sequence_number,
        operation=operation,
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
        mutating_command=mutating,
        fixed_argument_shape=fixed_shape,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=live_ref_cas_command_receipt_digest(receipt),
    )
    return receipt, stdout, stderr


def execute_repository_checkpoint_live_ref_cas(
    request: RepositoryCheckpointLiveRefCasRequest,
    transition: RepositoryCheckpointAtomicCasTransitionResult,
    preflight_policy: RepositoryCheckpointLiveGitPreflightPolicy,
    preflight_request: RepositoryCheckpointLiveGitPreflightRequest,
    supplied_preflight_receipt: RepositoryCheckpointLiveGitPreflightReceipt,
    policy: RepositoryCheckpointLiveRefCasPolicy,
    *,
    execution_started_at_epoch_seconds: int,
    execution_completed_at_epoch_seconds: int,
    git_executable: str = "git",
) -> RepositoryCheckpointLiveRefCasResult:
    policy_valid = not repository_checkpoint_live_ref_cas_policy_issues(policy)
    request_valid = not repository_checkpoint_live_ref_cas_request_issues(request)
    transition_valid = not repository_checkpoint_atomic_cas_transition_result_issues(
        transition
    )
    preflight_policy_valid = not repository_checkpoint_live_git_preflight_policy_issues(
        preflight_policy
    )
    preflight_request_valid = not repository_checkpoint_live_git_preflight_request_issues(
        preflight_request
    )
    supplied_preflight_valid = not repository_checkpoint_live_git_preflight_receipt_issues(
        supplied_preflight_receipt
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
    request_binding_exact = bool(
        request.transition_result_digest == transition.result_digest
        and request.preflight_policy_digest == preflight_policy.policy_digest
        and request.preflight_request_digest == preflight_request.request_digest
        and request.preflight_receipt_digest == supplied_preflight_receipt.receipt_digest
        and request.repository_path == preflight_request.repository_path
        and request.repository_path_digest
        == supplied_preflight_receipt.repository_path_digest
        and request.repository_id == transition.repository_id
        == preflight_request.repository_id
        == supplied_preflight_receipt.repository_id
        and request.git_dir_fingerprint == transition.git_dir_fingerprint
        == preflight_request.git_dir_fingerprint
        == supplied_preflight_receipt.git_dir_fingerprint
        and request.checkpoint_reference == transition.checkpoint_reference
        == preflight_request.checkpoint_reference
        == supplied_preflight_receipt.checkpoint_reference
        and request.expected_current_oid == transition.expected_current_oid
        == preflight_request.expected_current_oid
        == supplied_preflight_receipt.expected_current_oid
        and request.proposed_checkpoint_oid == transition.proposed_checkpoint_oid
        == preflight_request.proposed_checkpoint_oid
        == supplied_preflight_receipt.proposed_checkpoint_oid
    )
    executor_authorized = request.executor_id in policy.authorized_executor_ids
    resolved_root = Path(request.repository_path).expanduser().resolve()
    actual_path_digest = repository_path_digest(resolved_root)
    repository_path_allowed = bool(
        request.repository_path_digest == actual_path_digest
        and actual_path_digest in policy.allowed_repository_path_digests
        and resolved_root.exists()
        and resolved_root.is_dir()
    )
    preflight_ready = bool(
        supplied_preflight_valid
        and supplied_preflight_receipt.status == PREFLIGHT_READY
        and all(supplied_preflight_receipt.checks.values())
        and supplied_preflight_receipt.live_git_command_invoked
        and not supplied_preflight_receipt.live_repository_mutated
    )
    preflight_age = (
        execution_started_at_epoch_seconds
        - preflight_request.requested_at_epoch_seconds
    )
    preflight_fresh = bool(
        0 <= preflight_age <= policy.max_preflight_age_seconds
    )
    execution_duration = (
        execution_completed_at_epoch_seconds - execution_started_at_epoch_seconds
    )
    execution_duration_within_policy = bool(
        0 <= execution_duration <= policy.max_execution_duration_seconds
    )
    no_future_evidence = bool(
        request.requested_at_epoch_seconds <= execution_started_at_epoch_seconds
        and preflight_request.requested_at_epoch_seconds
        <= execution_started_at_epoch_seconds
        and execution_started_at_epoch_seconds
        <= execution_completed_at_epoch_seconds
    )
    checkpoint_reference_valid = _valid_checkpoint_reference(
        request.checkpoint_reference
    )

    recomputed_preflight = None
    preflight_recomputed = False
    preflight_receipt_exact = False
    recomputation_error = False
    preliminary_ready = all(
        (
            policy_valid,
            request_valid,
            transition_committed,
            preflight_policy_valid,
            preflight_request_valid,
            request_binding_exact,
            executor_authorized,
            repository_path_allowed,
            preflight_ready,
            preflight_fresh,
            execution_duration_within_policy,
            no_future_evidence,
            checkpoint_reference_valid,
        )
    )
    if preliminary_ready:
        try:
            recomputed_preflight = execute_repository_checkpoint_live_git_preflight(
                preflight_request,
                transition,
                preflight_policy,
                git_executable=git_executable,
            )
            preflight_recomputed = True
            preflight_receipt_exact = bool(
                recomputed_preflight.to_dict()
                == supplied_preflight_receipt.to_dict()
                and recomputed_preflight.status == PREFLIGHT_READY
            )
        except (OSError, TypeError, ValueError):
            recomputation_error = True

    git_dir = resolved_root / ".git"
    marker_path = git_dir / SANDBOX_MARKER_FILENAME
    sandbox_marker_present = bool(
        git_dir.is_dir()
        and marker_path.exists()
        and marker_path.is_file()
        and not marker_path.is_symlink()
    )
    marker_content = ""
    if sandbox_marker_present:
        try:
            if marker_path.stat().st_size <= 256:
                marker_content = marker_path.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError):
            marker_content = ""
    sandbox_marker_exact = marker_content == request.sandbox_marker_token
    reflog_path = git_dir / "logs" / Path(request.checkpoint_reference)
    target_reflog_absent_before = not reflog_path.exists()
    checkpoint_reference_direct = bool(
        preflight_receipt_exact
        and recomputed_preflight is not None
        and recomputed_preflight.checkpoint_reference_direct
    )
    observed_before_oid = (
        recomputed_preflight.observed_current_oid
        if recomputed_preflight is not None
        else supplied_preflight_receipt.observed_current_oid
    )
    current_oid_matches_expected = (
        observed_before_oid == request.expected_current_oid
    )
    proposed_object_exists = bool(
        preflight_receipt_exact
        and recomputed_preflight is not None
        and recomputed_preflight.proposed_object_exists
    )

    mutation_ready = all(
        (
            preliminary_ready,
            preflight_recomputed,
            preflight_receipt_exact,
            sandbox_marker_present,
            sandbox_marker_exact,
            checkpoint_reference_direct,
            target_reflog_absent_before,
            current_oid_matches_expected,
            proposed_object_exists,
        )
    )
    command_receipts: list[LiveRefCasCommandReceipt] = []
    update_ref_attempted = False
    update_ref_succeeded = False
    post_update_verified = False
    observed_after_oid = observed_before_oid
    command_error = recomputation_error

    if mutation_ready:
        update_ref_attempted = True
        update_receipt, _, _ = _run_git_command(
            resolved_root,
            (
                "update-ref",
                "--no-deref",
                request.checkpoint_reference,
                request.proposed_checkpoint_oid,
                request.expected_current_oid,
            ),
            policy,
            sequence_number=1,
            operation="atomic-update-ref",
            mutating=True,
            git_executable=git_executable,
        )
        command_receipts.append(update_receipt)
        update_ref_succeeded = bool(
            update_receipt.return_code == 0
            and not update_receipt.timed_out
            and update_receipt.fixed_argument_shape
            and update_receipt.stdout_size_bytes <= policy.max_output_bytes
            and update_receipt.stderr_size_bytes <= policy.max_output_bytes
        )
        if update_receipt.return_code in (-124, -127):
            command_error = True

        verify_receipt, verify_stdout, _ = _run_git_command(
            resolved_root,
            (
                "show-ref",
                "--verify",
                "--hash",
                request.checkpoint_reference,
            ),
            policy,
            sequence_number=2,
            operation="post-verify-ref",
            mutating=False,
            git_executable=git_executable,
        )
        command_receipts.append(verify_receipt)
        observed_after_oid = verify_stdout.strip().lower()
        post_update_verified = bool(
            verify_receipt.return_code == 0
            and not verify_receipt.timed_out
            and verify_receipt.fixed_argument_shape
            and observed_after_oid == request.proposed_checkpoint_oid
        )
        if verify_receipt.return_code in (-124, -127):
            command_error = True

    target_reflog_absent_after = not reflog_path.exists()
    committed = bool(
        mutation_ready
        and update_ref_attempted
        and update_ref_succeeded
        and post_update_verified
        and target_reflog_absent_after
    )
    if committed:
        status = LIVE_REF_CAS_COMMITTED
        reason = "ATOMIC_CHECKPOINT_REFERENCE_UPDATE_COMMITTED"
    elif command_error:
        status = LIVE_REF_CAS_ERROR
        reason = "LIVE_GIT_COMMAND_ERROR"
    elif update_ref_attempted:
        status = LIVE_REF_CAS_ABORTED
        reason = "ATOMIC_CHECKPOINT_REFERENCE_UPDATE_ABORTED"
    else:
        status = LIVE_REF_CAS_REJECTED
        reason = "LIVE_REFERENCE_MUTATION_PRECONDITION_REJECTED"

    reference_write = committed
    checks = {
        "policy_valid": policy_valid,
        "request_valid": request_valid,
        "transition_committed": transition_committed,
        "preflight_policy_valid": preflight_policy_valid,
        "preflight_request_valid": preflight_request_valid,
        "request_binding_exact": request_binding_exact,
        "executor_authorized": executor_authorized,
        "repository_path_allowed": repository_path_allowed,
        "preflight_ready": preflight_ready,
        "preflight_fresh": preflight_fresh,
        "preflight_recomputed": preflight_recomputed,
        "preflight_receipt_exact": preflight_receipt_exact,
        "sandbox_marker_present": sandbox_marker_present,
        "sandbox_marker_exact": sandbox_marker_exact,
        "checkpoint_reference_valid": checkpoint_reference_valid,
        "checkpoint_reference_direct": checkpoint_reference_direct,
        "target_reflog_absent_before": target_reflog_absent_before,
        "current_oid_matches_expected": current_oid_matches_expected,
        "proposed_object_exists": proposed_object_exists,
        "execution_duration_within_policy": execution_duration_within_policy,
        "no_future_evidence": no_future_evidence,
    }
    result = RepositoryCheckpointLiveRefCasResult(
        execution_id=request.execution_id,
        status=status,
        reason=reason,
        policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        transition_result_digest=transition.result_digest,
        supplied_preflight_receipt_digest=supplied_preflight_receipt.receipt_digest,
        recomputed_preflight_receipt_digest=(
            recomputed_preflight.receipt_digest
            if recomputed_preflight is not None
            else ""
        ),
        repository_path_digest=actual_path_digest,
        repository_id=request.repository_id,
        git_dir_fingerprint=request.git_dir_fingerprint,
        checkpoint_reference=request.checkpoint_reference,
        expected_current_oid=request.expected_current_oid,
        observed_before_oid=observed_before_oid,
        proposed_checkpoint_oid=request.proposed_checkpoint_oid,
        observed_after_oid=observed_after_oid,
        executor_id=request.executor_id,
        execution_started_at_epoch_seconds=execution_started_at_epoch_seconds,
        execution_completed_at_epoch_seconds=execution_completed_at_epoch_seconds,
        policy_valid=policy_valid,
        request_valid=request_valid,
        request_binding_exact=request_binding_exact,
        executor_authorized=executor_authorized,
        repository_path_allowed=repository_path_allowed,
        preflight_ready=preflight_ready,
        preflight_fresh=preflight_fresh,
        preflight_recomputed=preflight_recomputed,
        preflight_receipt_exact=preflight_receipt_exact,
        sandbox_marker_present=sandbox_marker_present,
        sandbox_marker_exact=sandbox_marker_exact,
        checkpoint_reference_valid=checkpoint_reference_valid,
        checkpoint_reference_direct=checkpoint_reference_direct,
        target_reflog_absent_before=target_reflog_absent_before,
        target_reflog_absent_after=target_reflog_absent_after,
        current_oid_matches_expected=current_oid_matches_expected,
        proposed_object_exists=proposed_object_exists,
        execution_duration_within_policy=execution_duration_within_policy,
        no_future_evidence=no_future_evidence,
        update_ref_attempted=update_ref_attempted,
        update_ref_succeeded=update_ref_succeeded,
        post_update_verified=post_update_verified,
        reference_cas_committed=committed,
        live_git_command_invoked=bool(
            supplied_preflight_receipt.live_git_command_invoked
            or preflight_recomputed
            or command_receipts
        ),
        live_repository_mutated=reference_write,
        checkpoint_reference_write_performed=reference_write,
        object_database_write_performed=False,
        index_write_performed=False,
        working_tree_write_performed=False,
        reflog_write_performed=False,
        force_update_performed=False,
        reference_delete_performed=False,
        head_updated=False,
        branch_updated=False,
        tag_updated=False,
        remote_reference_updated=False,
        push_performed=False,
        signing_performed=False,
        command_receipts=tuple(command_receipts),
        checks=checks,
        evidence_digests={
            "v116_transition": transition.result_digest,
            "v117_preflight_policy": preflight_policy.policy_digest,
            "v117_preflight_request": preflight_request.request_digest,
            "v117_supplied_preflight_receipt": supplied_preflight_receipt.receipt_digest,
            "v117_recomputed_preflight_receipt": (
                recomputed_preflight.receipt_digest
                if recomputed_preflight is not None
                else ""
            ),
            "v118_policy": policy.policy_digest,
            "v118_request": request.request_digest,
            "repository_path": actual_path_digest,
            "sandbox_marker": canonical_digest(
                {"marker": marker_content if sandbox_marker_exact else ""}
            ),
        },
        result_digest="",
    )
    result = replace(
        result,
        result_digest=repository_checkpoint_live_ref_cas_result_digest(result),
    )
    issues = repository_checkpoint_live_ref_cas_result_issues(result)
    if issues:
        raise ValueError(f"checkpoint_live_ref_cas_result_invalid:{issues[0]}")
    return result


def repository_checkpoint_live_ref_cas_result_issues(
    result: RepositoryCheckpointLiveRefCasResult,
) -> tuple[str, ...]:
    issues: list[str] = []
    if result.status not in (
        LIVE_REF_CAS_COMMITTED,
        LIVE_REF_CAS_ABORTED,
        LIVE_REF_CAS_REJECTED,
        LIVE_REF_CAS_ERROR,
    ):
        issues.append("checkpoint_live_ref_cas_status_invalid")
    committed = result.status == LIVE_REF_CAS_COMMITTED
    if result.reference_cas_committed != committed:
        issues.append("checkpoint_live_ref_cas_commit_flag_mismatch")
    if result.live_repository_mutated != committed:
        issues.append("checkpoint_live_ref_cas_live_mutation_flag_mismatch")
    if result.checkpoint_reference_write_performed != committed:
        issues.append("checkpoint_live_ref_cas_reference_write_flag_mismatch")
    if committed and not all(
        (
            result.update_ref_attempted,
            result.update_ref_succeeded,
            result.post_update_verified,
            result.observed_before_oid == result.expected_current_oid,
            result.observed_after_oid == result.proposed_checkpoint_oid,
            result.target_reflog_absent_before,
            result.target_reflog_absent_after,
        )
    ):
        issues.append("checkpoint_live_ref_cas_committed_semantics_invalid")
    if not committed and result.checkpoint_reference_write_performed:
        issues.append("checkpoint_live_ref_cas_rejected_write_detected")
    if any(
        (
            result.object_database_write_performed,
            result.index_write_performed,
            result.working_tree_write_performed,
            result.reflog_write_performed,
            result.force_update_performed,
            result.reference_delete_performed,
            result.head_updated,
            result.branch_updated,
            result.tag_updated,
            result.remote_reference_updated,
            result.push_performed,
            result.signing_performed,
        )
    ):
        issues.append("checkpoint_live_ref_cas_forbidden_effect")
    for sequence, command in enumerate(result.command_receipts, start=1):
        if command.sequence_number != sequence:
            issues.append("checkpoint_live_ref_cas_command_sequence_invalid")
            break
        if command.shell_used or not command.optional_locks_disabled:
            issues.append("checkpoint_live_ref_cas_command_guard_invalid")
            break
        if command.receipt_digest != live_ref_cas_command_receipt_digest(command):
            issues.append("checkpoint_live_ref_cas_command_digest_mismatch")
            break
    if result.result_digest != repository_checkpoint_live_ref_cas_result_digest(
        result
    ):
        issues.append("checkpoint_live_ref_cas_result_digest_mismatch")
    return tuple(issues)
