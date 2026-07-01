#!/usr/bin/env python3
from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import (
    TREE_COMMIT_ERROR,
    TREE_COMMIT_MATERIALIZED,
    TREE_COMMIT_REJECTED,
    TREE_COMMIT_REUSED,
    RepositoryTreeCommitMaterializationResult,
    repository_tree_commit_materialization_result_digest,
    tree_commit_git_command_receipt_digest,
)


def repository_tree_commit_materialization_result_issues(
    result: RepositoryTreeCommitMaterializationResult,
) -> tuple[str, ...]:
    issues: list[str] = []
    if result.status not in (
        TREE_COMMIT_MATERIALIZED,
        TREE_COMMIT_REUSED,
        TREE_COMMIT_REJECTED,
        TREE_COMMIT_ERROR,
    ):
        issues.append("tree_commit_materialization_status_invalid")
    tree_write = bool(
        result.tree_write_command_attempted
        and result.tree_write_command_succeeded
        and not result.tree_existed_before
    )
    commit_write = bool(
        result.commit_write_command_attempted
        and result.commit_write_command_succeeded
        and not result.commit_existed_before
    )
    if result.tree_object_database_write_performed != tree_write:
        issues.append("tree_commit_materialization_tree_write_flag_mismatch")
    if result.commit_object_database_write_performed != commit_write:
        issues.append("tree_commit_materialization_commit_write_flag_mismatch")
    expected_any_write = tree_write or commit_write
    if result.object_database_write_performed != expected_any_write:
        issues.append("tree_commit_materialization_write_flag_mismatch")
    if result.live_repository_mutated != expected_any_write:
        issues.append("tree_commit_materialization_mutation_flag_mismatch")
    exact_postconditions = all(
        (
            result.tree_present_after,
            result.commit_present_after,
            result.tree_type_exact,
            result.commit_type_exact,
            result.tree_content_exact,
            result.commit_content_exact,
        )
    )
    if result.status == TREE_COMMIT_MATERIALIZED and not (
        expected_any_write and exact_postconditions
    ):
        issues.append("tree_commit_materialization_success_semantics_invalid")
    if result.status == TREE_COMMIT_REUSED and not all(
        (
            result.tree_existed_before,
            result.commit_existed_before,
            result.exact_existing_tree_reused,
            result.exact_existing_commit_reused,
            not result.tree_write_command_attempted,
            not result.commit_write_command_attempted,
            not expected_any_write,
            exact_postconditions,
        )
    ):
        issues.append("tree_commit_materialization_reuse_semantics_invalid")
    if result.status == TREE_COMMIT_REJECTED and expected_any_write:
        issues.append("tree_commit_materialization_rejected_after_write")
    if any(
        (
            result.reference_write_performed,
            result.index_write_performed,
            result.working_tree_write_performed,
            result.reflog_write_performed,
            result.push_performed,
            result.signing_performed,
        )
    ):
        issues.append("tree_commit_materialization_forbidden_effect")
    for sequence, command in enumerate(result.command_receipts, start=1):
        if command.sequence_number != sequence:
            issues.append("tree_commit_materialization_command_sequence_invalid")
            break
        if command.shell_used or not command.fixed_argument_shape:
            issues.append("tree_commit_materialization_command_guard_invalid")
            break
        if command.receipt_digest != tree_commit_git_command_receipt_digest(command):
            issues.append("tree_commit_materialization_command_digest_mismatch")
            break
    if result.result_digest != repository_tree_commit_materialization_result_digest(result):
        issues.append("tree_commit_materialization_result_digest_mismatch")
    return tuple(issues)
