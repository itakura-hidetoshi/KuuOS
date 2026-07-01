#!/usr/bin/env python3
from runtime.kuuos_repository_sandbox_worktree_types_v1_23 import (
    WORKTREE_ERROR,
    WORKTREE_MATERIALIZED,
    WORKTREE_REJECTED,
    WORKTREE_REUSED,
    RepositorySandboxWorktreeResult,
    repository_sandbox_worktree_result_digest,
    sandbox_worktree_git_command_receipt_digest,
)


def repository_sandbox_worktree_result_issues(
    result: RepositorySandboxWorktreeResult,
) -> tuple[str, ...]:
    issues: list[str] = []
    if result.status not in (
        WORKTREE_MATERIALIZED,
        WORKTREE_REUSED,
        WORKTREE_REJECTED,
        WORKTREE_ERROR,
    ):
        issues.append("sandbox_worktree_status_invalid")
    materialized = result.status == WORKTREE_MATERIALIZED
    reused = result.status == WORKTREE_REUSED
    if result.live_repository_mutated != result.sandbox_working_tree_write_performed:
        issues.append("sandbox_worktree_mutation_accounting_mismatch")
    if materialized and not all(
        (
            result.checkout_command_attempted,
            result.checkout_command_succeeded,
            result.sandbox_present_after,
            result.sandbox_files_exact,
            result.sandbox_modes_exact,
            result.sandbox_has_no_extra_entries,
            result.dedicated_index_unchanged,
            result.canonical_index_unchanged,
            result.repository_root_unchanged,
            result.sandbox_working_tree_write_performed,
            not result.exact_existing_sandbox_reused,
        )
    ):
        issues.append("sandbox_worktree_materialized_semantics_invalid")
    if reused and not all(
        (
            result.sandbox_existed_before,
            result.sandbox_present_after,
            result.sandbox_files_exact,
            result.sandbox_modes_exact,
            result.sandbox_has_no_extra_entries,
            result.dedicated_index_unchanged,
            result.canonical_index_unchanged,
            result.repository_root_unchanged,
            result.exact_existing_sandbox_reused,
            not result.checkout_command_attempted,
            not result.checkout_command_succeeded,
            not result.sandbox_working_tree_write_performed,
            not result.live_repository_mutated,
        )
    ):
        issues.append("sandbox_worktree_reused_semantics_invalid")
    if result.status == WORKTREE_REJECTED and any(
        (
            result.checkout_command_attempted,
            result.sandbox_working_tree_write_performed,
            result.live_repository_mutated,
        )
    ):
        issues.append("sandbox_worktree_rejected_after_write")
    if result.sandbox_working_tree_write_performed and result.status not in (
        WORKTREE_MATERIALIZED,
        WORKTREE_ERROR,
    ):
        issues.append("sandbox_worktree_write_status_invalid")
    if any(
        (
            result.repository_root_working_tree_write_performed,
            result.dedicated_index_write_performed,
            result.canonical_index_write_performed,
            result.current_object_database_write_performed,
            result.current_reference_write_performed,
            result.reflog_write_performed,
            result.push_performed,
            result.signing_performed,
        )
    ):
        issues.append("sandbox_worktree_forbidden_effect")
    for sequence, receipt in enumerate(result.command_receipts, start=1):
        if receipt.sequence_number != sequence:
            issues.append("sandbox_worktree_command_sequence_invalid")
            break
        if receipt.shell_used or not receipt.fixed_argument_shape:
            issues.append("sandbox_worktree_command_guard_invalid")
            break
        if receipt.receipt_digest != sandbox_worktree_git_command_receipt_digest(receipt):
            issues.append("sandbox_worktree_command_digest_mismatch")
            break
    if result.result_digest != repository_sandbox_worktree_result_digest(result):
        issues.append("sandbox_worktree_result_digest_mismatch")
    return tuple(issues)
