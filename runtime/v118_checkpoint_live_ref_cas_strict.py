#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_live_ref_cas_types_v1_18 import (
    LIVE_REF_CAS_ABORTED,
    LIVE_REF_CAS_COMMITTED,
    LIVE_REF_CAS_ERROR,
    LIVE_REF_CAS_REJECTED,
    RepositoryCheckpointLiveRefCasResult,
    live_ref_cas_command_receipt_digest,
    repository_checkpoint_live_ref_cas_result_digest,
)
from runtime.v118_checkpoint_live_ref_cas_core import (
    build_repository_checkpoint_live_ref_cas_policy,
    build_repository_checkpoint_live_ref_cas_request,
    execute_repository_checkpoint_live_ref_cas as _execute_core,
    repository_checkpoint_live_ref_cas_policy_issues,
    repository_checkpoint_live_ref_cas_request_issues,
    repository_path_digest,
)


def normalize_repository_checkpoint_live_ref_cas_result(
    result: RepositoryCheckpointLiveRefCasResult,
) -> RepositoryCheckpointLiveRefCasResult:
    reference_write_observed = bool(result.update_ref_succeeded)
    unexpected_reflog = not result.target_reflog_absent_after
    unexpected_postcondition = bool(
        reference_write_observed
        and (
            not result.post_update_verified
            or unexpected_reflog
            or result.observed_after_oid != result.proposed_checkpoint_oid
        )
    )
    if unexpected_postcondition:
        result = replace(
            result,
            status=LIVE_REF_CAS_ERROR,
            reason="LIVE_REFERENCE_WRITE_POSTCONDITION_ERROR",
            reference_cas_committed=False,
            live_repository_mutated=True,
            checkpoint_reference_write_performed=True,
            reflog_write_performed=unexpected_reflog,
            result_digest="",
        )
    elif reference_write_observed and not result.checkpoint_reference_write_performed:
        result = replace(
            result,
            status=LIVE_REF_CAS_ERROR,
            reason="LIVE_REFERENCE_WRITE_ACCOUNTING_ERROR",
            reference_cas_committed=False,
            live_repository_mutated=True,
            checkpoint_reference_write_performed=True,
            result_digest="",
        )
    if not result.result_digest:
        result = replace(
            result,
            result_digest=repository_checkpoint_live_ref_cas_result_digest(result),
        )
    return result


def execute_repository_checkpoint_live_ref_cas(*args, **kwargs):
    result = normalize_repository_checkpoint_live_ref_cas_result(
        _execute_core(*args, **kwargs)
    )
    issues = repository_checkpoint_live_ref_cas_result_issues(result)
    if issues:
        raise ValueError(f"checkpoint_live_ref_cas_strict_result_invalid:{issues[0]}")
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
    wrote_reference = bool(result.update_ref_succeeded)
    if result.reference_cas_committed != committed:
        issues.append("checkpoint_live_ref_cas_commit_flag_mismatch")
    if result.checkpoint_reference_write_performed != wrote_reference:
        issues.append("checkpoint_live_ref_cas_reference_write_accounting_mismatch")
    if result.live_repository_mutated != bool(
        wrote_reference or result.reflog_write_performed
    ):
        issues.append("checkpoint_live_ref_cas_live_mutation_accounting_mismatch")
    if result.reflog_write_performed != (not result.target_reflog_absent_after):
        issues.append("checkpoint_live_ref_cas_reflog_accounting_mismatch")
    if committed and not all(
        (
            result.update_ref_attempted,
            result.update_ref_succeeded,
            result.post_update_verified,
            result.observed_before_oid == result.expected_current_oid,
            result.observed_after_oid == result.proposed_checkpoint_oid,
            result.target_reflog_absent_before,
            result.target_reflog_absent_after,
            not result.reflog_write_performed,
        )
    ):
        issues.append("checkpoint_live_ref_cas_committed_semantics_invalid")
    if result.status in (LIVE_REF_CAS_REJECTED, LIVE_REF_CAS_ABORTED) and any(
        (
            result.checkpoint_reference_write_performed,
            result.live_repository_mutated,
            result.reflog_write_performed,
        )
    ):
        issues.append("checkpoint_live_ref_cas_nonerror_write_detected")
    if wrote_reference and not committed and result.status != LIVE_REF_CAS_ERROR:
        issues.append("checkpoint_live_ref_cas_uncommitted_write_not_error")
    if any(
        (
            result.object_database_write_performed,
            result.index_write_performed,
            result.working_tree_write_performed,
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


__all__ = [
    "repository_path_digest",
    "build_repository_checkpoint_live_ref_cas_policy",
    "repository_checkpoint_live_ref_cas_policy_issues",
    "build_repository_checkpoint_live_ref_cas_request",
    "repository_checkpoint_live_ref_cas_request_issues",
    "normalize_repository_checkpoint_live_ref_cas_result",
    "execute_repository_checkpoint_live_ref_cas",
    "repository_checkpoint_live_ref_cas_result_issues",
]
