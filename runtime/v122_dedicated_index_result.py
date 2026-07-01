#!/usr/bin/env python3
from runtime.kuuos_repository_dedicated_index_types_v1_22 import (
    INDEX_ERROR,
    INDEX_MATERIALIZED,
    INDEX_REJECTED,
    INDEX_REUSED,
    RepositoryDedicatedIndexResult,
    dedicated_index_git_command_receipt_digest,
    repository_dedicated_index_result_digest,
)


def repository_dedicated_index_result_issues(
    result: RepositoryDedicatedIndexResult,
) -> tuple[str, ...]:
    issues: list[str] = []
    if result.status not in (
        INDEX_MATERIALIZED,
        INDEX_REUSED,
        INDEX_REJECTED,
        INDEX_ERROR,
    ):
        issues.append("dedicated_index_status_invalid")
    materialized = result.status == INDEX_MATERIALIZED
    reused = result.status == INDEX_REUSED
    if result.live_repository_mutated != result.dedicated_index_write_performed:
        issues.append("dedicated_index_mutation_accounting_mismatch")
    if materialized and not all(
        (
            result.dedicated_index_write_performed,
            result.read_tree_command_attempted,
            result.read_tree_command_succeeded,
            result.verify_index_command_attempted,
            result.verify_index_command_succeeded,
            result.dedicated_index_present_after,
            result.index_entries_exact,
            result.canonical_index_unchanged,
            not result.exact_existing_index_reused,
        )
    ):
        issues.append("dedicated_index_materialized_semantics_invalid")
    if reused and not all(
        (
            result.dedicated_index_existed_before,
            result.dedicated_index_present_after,
            result.exact_existing_index_reused,
            result.verify_index_command_attempted,
            result.verify_index_command_succeeded,
            result.index_entries_exact,
            result.canonical_index_unchanged,
            not result.read_tree_command_attempted,
            not result.read_tree_command_succeeded,
            not result.dedicated_index_write_performed,
            not result.live_repository_mutated,
        )
    ):
        issues.append("dedicated_index_reused_semantics_invalid")
    if result.status == INDEX_REJECTED and any(
        (
            result.dedicated_index_write_performed,
            result.live_repository_mutated,
            result.read_tree_command_attempted,
            result.canonical_index_write_performed,
        )
    ):
        issues.append("dedicated_index_rejected_after_write")
    if result.dedicated_index_write_performed and result.status not in (
        INDEX_MATERIALIZED,
        INDEX_ERROR,
    ):
        issues.append("dedicated_index_write_status_invalid")
    if any(
        (
            result.canonical_index_write_performed,
            result.current_object_database_write_performed,
            result.current_reference_write_performed,
            result.working_tree_write_performed,
            result.reflog_write_performed,
            result.push_performed,
            result.signing_performed,
        )
    ):
        issues.append("dedicated_index_forbidden_effect")
    for sequence, receipt in enumerate(result.command_receipts, start=1):
        if receipt.sequence_number != sequence:
            issues.append("dedicated_index_command_sequence_invalid")
            break
        if receipt.shell_used or not receipt.fixed_argument_shape:
            issues.append("dedicated_index_command_guard_invalid")
            break
        if receipt.receipt_digest != dedicated_index_git_command_receipt_digest(receipt):
            issues.append("dedicated_index_command_digest_mismatch")
            break
    if result.result_digest != repository_dedicated_index_result_digest(result):
        issues.append("dedicated_index_result_digest_mismatch")
    return tuple(issues)
