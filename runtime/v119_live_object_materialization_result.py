#!/usr/bin/env python3
from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    OBJECT_ERROR,
    OBJECT_MATERIALIZED,
    OBJECT_REJECTED,
    OBJECT_REUSED,
    RepositoryLiveObjectMaterializationResult,
    live_object_git_command_receipt_digest,
    repository_live_object_materialization_result_digest,
)


def repository_live_object_materialization_result_issues(
    result: RepositoryLiveObjectMaterializationResult,
) -> tuple[str, ...]:
    issues: list[str] = []
    if result.status not in (
        OBJECT_MATERIALIZED,
        OBJECT_REUSED,
        OBJECT_REJECTED,
        OBJECT_ERROR,
    ):
        issues.append("live_object_materialization_status_invalid")
    materialized = result.status == OBJECT_MATERIALIZED
    reused = result.status == OBJECT_REUSED
    if result.object_database_write_performed != materialized:
        issues.append("live_object_materialization_write_flag_mismatch")
    if result.live_repository_mutated != materialized:
        issues.append("live_object_materialization_mutation_flag_mismatch")
    if materialized and not all(
        (
            result.write_command_attempted,
            result.write_command_succeeded,
            not result.object_existed_before,
            result.object_present_after,
            result.object_type_blob,
            result.object_size_exact,
            result.object_content_exact,
        )
    ):
        issues.append("live_object_materialization_success_semantics_invalid")
    if reused and not all(
        (
            result.object_existed_before,
            result.object_present_after,
            result.exact_existing_object_reused,
            not result.write_command_attempted,
            not result.object_database_write_performed,
        )
    ):
        issues.append("live_object_materialization_reuse_semantics_invalid")
    if result.status in (OBJECT_REJECTED, OBJECT_REUSED) and any(
        (
            result.object_database_write_performed,
            result.live_repository_mutated,
        )
    ):
        issues.append("live_object_materialization_nonwrite_status_mutated")
    if result.status == OBJECT_ERROR and result.write_command_succeeded:
        if not result.object_database_write_performed:
            issues.append("live_object_materialization_error_write_not_recorded")
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
        issues.append("live_object_materialization_forbidden_effect")
    for sequence, command in enumerate(result.command_receipts, start=1):
        if command.sequence_number != sequence:
            issues.append("live_object_materialization_command_sequence_invalid")
            break
        if command.shell_used or not command.fixed_argument_shape:
            issues.append("live_object_materialization_command_guard_invalid")
            break
        if command.receipt_digest != live_object_git_command_receipt_digest(command):
            issues.append("live_object_materialization_command_digest_mismatch")
            break
    if result.result_digest != repository_live_object_materialization_result_digest(
        result
    ):
        issues.append("live_object_materialization_result_digest_mismatch")
    return tuple(issues)
