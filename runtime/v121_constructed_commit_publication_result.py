#!/usr/bin/env python3
from runtime.kuuos_repository_constructed_commit_publication_types_v1_21 import (
    COMMIT_PUBLISHED,
    PUBLICATION_ERROR,
    PUBLICATION_REJECTED,
    RepositoryConstructedCommitPublicationResult,
    repository_constructed_commit_publication_result_digest,
)


def repository_constructed_commit_publication_result_issues(
    result: RepositoryConstructedCommitPublicationResult,
) -> tuple[str, ...]:
    issues: list[str] = []
    if result.status not in (
        COMMIT_PUBLISHED,
        PUBLICATION_REJECTED,
        PUBLICATION_ERROR,
    ):
        issues.append("constructed_commit_publication_status_invalid")
    published = result.status == COMMIT_PUBLISHED
    if result.reference_cas_committed != published:
        issues.append("constructed_commit_publication_commit_flag_mismatch")
    if published and not all(
        (
            result.delegated_live_ref_cas_invoked,
            result.delegated_live_ref_cas_valid,
            result.constructed_commit_binding_exact,
            result.live_ref_cas_request_binding_exact,
            result.observed_before_oid == result.expected_current_oid,
            result.observed_after_oid == result.constructed_commit_oid,
            result.checkpoint_reference_write_performed,
            result.live_repository_mutated,
            not result.current_object_database_write_performed,
        )
    ):
        issues.append("constructed_commit_publication_success_semantics_invalid")
    if result.status == PUBLICATION_REJECTED and any(
        (
            result.reference_cas_committed,
            result.checkpoint_reference_write_performed,
            result.live_repository_mutated,
            result.reflog_write_performed,
        )
    ):
        issues.append("constructed_commit_publication_rejected_after_write")
    if result.checkpoint_reference_write_performed and not (
        published or result.status == PUBLICATION_ERROR
    ):
        issues.append("constructed_commit_publication_write_status_invalid")
    if result.live_repository_mutated != bool(
        result.checkpoint_reference_write_performed or result.reflog_write_performed
    ):
        issues.append("constructed_commit_publication_mutation_flag_mismatch")
    if any(
        (
            result.current_object_database_write_performed,
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
        issues.append("constructed_commit_publication_forbidden_effect")
    if result.result_digest != repository_constructed_commit_publication_result_digest(
        result
    ):
        issues.append("constructed_commit_publication_result_digest_mismatch")
    return tuple(issues)
