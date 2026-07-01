#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_repository_bounded_tree_commit_types_v1_20 import (
    TREE_COMMIT_ERROR,
    TREE_COMMIT_MATERIALIZED,
    TREE_COMMIT_REJECTED,
    TREE_COMMIT_REUSED,
    RepositoryBoundedTreeCommitResult,
    repository_bounded_tree_commit_result_digest,
    tree_commit_git_command_receipt_digest,
)


def repository_bounded_tree_commit_result_issues(
    result: RepositoryBoundedTreeCommitResult,
) -> tuple[str, ...]:
    issues: list[str] = []
    known = {
        TREE_COMMIT_MATERIALIZED,
        TREE_COMMIT_REUSED,
        TREE_COMMIT_REJECTED,
        TREE_COMMIT_ERROR,
    }
    if result.status not in known:
        issues.append("v120_result_status_invalid")
    if result.result_digest != repository_bounded_tree_commit_result_digest(result):
        issues.append("v120_result_digest_mismatch")
    if result.expected_tree_oids != tuple(sorted(result.expected_tree_oids)):
        issues.append("v120_result_expected_tree_oids_not_canonical")
    if result.observed_tree_oids != tuple(sorted(result.observed_tree_oids)):
        issues.append("v120_result_observed_tree_oids_not_canonical")
    if result.v119_result_digests != tuple(sorted(result.v119_result_digests)):
        issues.append("v120_result_v119_digests_not_canonical")
    if result.tree_write_count < 0 or result.commit_write_count not in (0, 1):
        issues.append("v120_result_write_count_invalid")
    if result.tree_reuse_count < 0:
        issues.append("v120_result_reuse_count_invalid")
    write_performed = result.tree_write_count > 0 or result.commit_write_count > 0
    if result.object_database_write_performed != write_performed:
        issues.append("v120_result_object_write_accounting_mismatch")
    if result.live_repository_mutated != result.object_database_write_performed:
        issues.append("v120_result_mutation_accounting_mismatch")
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
        issues.append("v120_result_forbidden_effect_performed")
    for receipt in result.command_receipts:
        if receipt.receipt_digest != tree_commit_git_command_receipt_digest(receipt):
            issues.append("v120_result_command_receipt_digest_mismatch")
            break
        if receipt.shell_used or not receipt.fixed_argument_shape:
            issues.append("v120_result_command_receipt_boundary_invalid")
            break
    required_checks = (
        "policy_valid",
        "request_valid",
        "candidate_valid",
        "request_binding_exact",
        "v119_results_valid",
        "blob_result_coverage_exact",
        "executor_authorized",
        "repository_path_allowed",
        "sandbox_marker_present",
        "sandbox_marker_exact",
        "object_format_sha1",
        "parent_commit_present",
        "parent_commit_type_exact",
        "tree_payloads_exact",
        "commit_payload_exact",
        "tree_objects_present_after",
        "commit_object_present_after",
        "tree_objects_type_exact",
        "commit_object_type_exact",
        "tree_objects_content_exact",
        "commit_object_content_exact",
    )
    for name in required_checks:
        if name not in result.checks:
            issues.append("v120_result_check_missing")
            break
        if result.checks[name] != getattr(result, name):
            issues.append("v120_result_check_mismatch")
            break
    success_checks = all(getattr(result, name) for name in required_checks)
    if result.status == TREE_COMMIT_MATERIALIZED:
        if not success_checks or not write_performed:
            issues.append("v120_materialized_result_incoherent")
        if result.observed_tree_oids != result.expected_tree_oids:
            issues.append("v120_materialized_tree_oid_mismatch")
        if result.observed_root_tree_oid != result.expected_root_tree_oid:
            issues.append("v120_materialized_root_tree_oid_mismatch")
        if result.observed_commit_oid != result.expected_commit_oid:
            issues.append("v120_materialized_commit_oid_mismatch")
    elif result.status == TREE_COMMIT_REUSED:
        if not success_checks or write_performed:
            issues.append("v120_reused_result_incoherent")
        if result.tree_reuse_count != len(result.expected_tree_oids):
            issues.append("v120_reused_tree_count_mismatch")
        if not result.commit_reused:
            issues.append("v120_reused_commit_missing")
    elif result.status == TREE_COMMIT_REJECTED:
        if result.live_git_command_invoked or write_performed:
            issues.append("v120_rejected_result_has_effect")
    elif result.status == TREE_COMMIT_ERROR:
        if write_performed and not result.live_repository_mutated:
            issues.append("v120_error_result_lost_write_accounting")
    return tuple(issues)
