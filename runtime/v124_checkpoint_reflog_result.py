#!/usr/bin/env python3
from runtime.kuuos_repository_checkpoint_reflog_types_v1_24 import (
    REFLOG_ERROR,
    REFLOG_RECORDED,
    REFLOG_REJECTED,
    REFLOG_REUSED,
    RepositoryCheckpointReflogResult,
    checkpoint_reflog_git_command_receipt_digest,
    repository_checkpoint_reflog_result_digest,
)


def repository_checkpoint_reflog_result_issues(
    result: RepositoryCheckpointReflogResult,
) -> tuple[str, ...]:
    issues: list[str] = []
    if result.status not in (
        REFLOG_RECORDED,
        REFLOG_REUSED,
        REFLOG_REJECTED,
        REFLOG_ERROR,
    ):
        issues.append("checkpoint_reflog_status_invalid")
    recorded = result.status == REFLOG_RECORDED
    reused = result.status == REFLOG_REUSED
    actual_mutation = any(
        (
            result.checkpoint_reflog_write_performed,
            result.other_reflog_write_performed,
            result.current_object_database_write_performed,
            result.current_reference_write_performed,
            result.index_write_performed,
            result.working_tree_write_performed,
        )
    )
    if result.live_repository_mutated != actual_mutation:
        issues.append("checkpoint_reflog_mutation_accounting_mismatch")
    if recorded and not all(
        (
            result.reflog_write_command_attempted,
            result.reflog_write_command_succeeded,
            result.current_ref_exact_before,
            result.current_ref_exact_after,
            result.old_object_present,
            result.new_object_present,
            not result.target_reflog_existed_before,
            result.target_reflog_present_after,
            result.target_reflog_entry_exact,
            result.target_reflog_single_entry,
            result.checkpoint_reflog_write_performed,
            result.live_repository_mutated,
            not result.exact_existing_reflog_reused,
        )
    ):
        issues.append("checkpoint_reflog_recorded_semantics_invalid")
    if reused and not all(
        (
            result.target_reflog_existed_before,
            result.target_reflog_present_after,
            result.target_reflog_entry_exact,
            result.target_reflog_single_entry,
            result.current_ref_exact_before,
            result.current_ref_exact_after,
            result.exact_existing_reflog_reused,
            not result.reflog_write_command_attempted,
            not result.reflog_write_command_succeeded,
            not result.checkpoint_reflog_write_performed,
            not result.live_repository_mutated,
        )
    ):
        issues.append("checkpoint_reflog_reused_semantics_invalid")
    if result.status == REFLOG_REJECTED and any(
        (
            result.reflog_write_command_attempted,
            result.checkpoint_reflog_write_performed,
            result.live_repository_mutated,
        )
    ):
        issues.append("checkpoint_reflog_rejected_after_write")
    if result.checkpoint_reflog_write_performed and result.status not in (
        REFLOG_RECORDED,
        REFLOG_ERROR,
    ):
        issues.append("checkpoint_reflog_write_status_invalid")
    if any(
        (
            result.other_reflog_write_performed,
            result.current_object_database_write_performed,
            result.current_reference_write_performed,
            result.index_write_performed,
            result.working_tree_write_performed,
            result.push_performed,
            result.signing_performed,
        )
    ):
        issues.append("checkpoint_reflog_forbidden_effect")
    write_receipts = 0
    for sequence, receipt in enumerate(result.command_receipts, start=1):
        if receipt.sequence_number != sequence:
            issues.append("checkpoint_reflog_command_sequence_invalid")
            break
        if (
            receipt.shell_used
            or not receipt.optional_locks_disabled
            or not receipt.fixed_argument_shape
        ):
            issues.append("checkpoint_reflog_command_guard_invalid")
            break
        if receipt.operation == "write-checkpoint-reflog":
            write_receipts += 1
            if not receipt.mutating_command:
                issues.append("checkpoint_reflog_write_receipt_not_mutating")
                break
        elif receipt.mutating_command:
            issues.append("checkpoint_reflog_read_receipt_marked_mutating")
            break
        if (
            receipt.receipt_digest
            != checkpoint_reflog_git_command_receipt_digest(receipt)
        ):
            issues.append("checkpoint_reflog_command_digest_mismatch")
            break
    if write_receipts > 1:
        issues.append("checkpoint_reflog_multiple_write_commands")
    if result.reflog_write_command_attempted != (write_receipts == 1):
        issues.append("checkpoint_reflog_write_attempt_accounting_mismatch")
    if result.result_digest != repository_checkpoint_reflog_result_digest(result):
        issues.append("checkpoint_reflog_result_digest_mismatch")
    return tuple(issues)
