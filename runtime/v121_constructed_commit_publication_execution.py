#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_live_ref_cas_types_v1_18 import (
    LIVE_REF_CAS_COMMITTED,
    LIVE_REF_CAS_ERROR,
    RepositoryCheckpointLiveRefCasPolicy,
    RepositoryCheckpointLiveRefCasRequest,
)
from runtime.kuuos_repository_checkpoint_live_ref_cas_v1_18 import (
    execute_repository_checkpoint_live_ref_cas,
    repository_checkpoint_live_ref_cas_request_issues,
    repository_checkpoint_live_ref_cas_result_issues,
)
from runtime.kuuos_repository_constructed_commit_publication_types_v1_21 import (
    COMMIT_PUBLISHED,
    PUBLICATION_ERROR,
    PUBLICATION_REJECTED,
    RepositoryConstructedCommitPublicationPolicy,
    RepositoryConstructedCommitPublicationRequest,
    RepositoryConstructedCommitPublicationResult,
    repository_constructed_commit_publication_result_digest,
)
from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import (
    TREE_COMMIT_MATERIALIZED,
    TREE_COMMIT_REUSED,
    RepositoryTreeCommitMaterializationResult,
)
from runtime.v120_tree_commit_materialization_result import (
    repository_tree_commit_materialization_result_issues,
)
from runtime.v121_constructed_commit_publication_policy import (
    repository_constructed_commit_publication_policy_issues,
    repository_constructed_commit_publication_request_issues,
)
from runtime.v121_constructed_commit_publication_result import (
    repository_constructed_commit_publication_result_issues,
)


def execute_repository_constructed_commit_publication(
    request: RepositoryConstructedCommitPublicationRequest,
    v120_result: RepositoryTreeCommitMaterializationResult,
    live_ref_cas_request: RepositoryCheckpointLiveRefCasRequest,
    transition,
    preflight_policy,
    preflight_request,
    preflight_receipt,
    live_ref_cas_policy: RepositoryCheckpointLiveRefCasPolicy,
    policy: RepositoryConstructedCommitPublicationPolicy,
    *,
    execution_started_at_epoch_seconds: int,
    execution_completed_at_epoch_seconds: int,
    git_executable: str = "git",
) -> RepositoryConstructedCommitPublicationResult:
    policy_valid = not repository_constructed_commit_publication_policy_issues(policy)
    request_valid = not repository_constructed_commit_publication_request_issues(request)
    v120_valid = not repository_tree_commit_materialization_result_issues(v120_result)
    v120_accepted = bool(
        v120_valid
        and v120_result.status in (TREE_COMMIT_MATERIALIZED, TREE_COMMIT_REUSED)
        and v120_result.commit_present_after
        and v120_result.commit_type_exact
        and v120_result.commit_content_exact
        and not v120_result.reference_write_performed
        and not v120_result.index_write_performed
        and not v120_result.working_tree_write_performed
        and not v120_result.reflog_write_performed
        and not v120_result.push_performed
        and not v120_result.signing_performed
    )
    constructed_commit_binding_exact = bool(
        request.v120_result_digest == v120_result.result_digest
        and request.repository_path_digest == v120_result.repository_path_digest
        and request.repository_id == v120_result.repository_id
        and request.git_dir_fingerprint == v120_result.git_dir_fingerprint
        and request.constructed_commit_oid == v120_result.expected_commit_oid
        and v120_result.candidate_commit_oid == v120_result.expected_commit_oid
    )
    live_request_valid = not repository_checkpoint_live_ref_cas_request_issues(
        live_ref_cas_request
    )
    live_request_binding_exact = bool(
        request.live_ref_cas_request_digest == live_ref_cas_request.request_digest
        and request.repository_path_digest
        == live_ref_cas_request.repository_path_digest
        and request.repository_id == live_ref_cas_request.repository_id
        and request.git_dir_fingerprint == live_ref_cas_request.git_dir_fingerprint
        and request.checkpoint_reference
        == live_ref_cas_request.checkpoint_reference
        and request.expected_current_oid == live_ref_cas_request.expected_current_oid
        and request.constructed_commit_oid
        == live_ref_cas_request.proposed_checkpoint_oid
        and request.executor_id == live_ref_cas_request.executor_id
        and request.requested_at_epoch_seconds
        >= live_ref_cas_request.requested_at_epoch_seconds
    )
    executor_authorized = request.executor_id in policy.authorized_executor_ids
    repository_path_allowed = (
        request.repository_path_digest in policy.allowed_repository_path_digests
    )
    preconditions = all(
        (
            policy_valid,
            request_valid,
            v120_accepted,
            constructed_commit_binding_exact,
            live_request_valid,
            live_request_binding_exact,
            executor_authorized,
            repository_path_allowed,
        )
    )

    live_result = None
    delegated_valid = False
    if preconditions:
        live_result = execute_repository_checkpoint_live_ref_cas(
            live_ref_cas_request,
            transition,
            preflight_policy,
            preflight_request,
            preflight_receipt,
            live_ref_cas_policy,
            execution_started_at_epoch_seconds=execution_started_at_epoch_seconds,
            execution_completed_at_epoch_seconds=execution_completed_at_epoch_seconds,
            git_executable=git_executable,
        )
        delegated_valid = not repository_checkpoint_live_ref_cas_result_issues(
            live_result
        )

    published = bool(
        live_result is not None
        and delegated_valid
        and live_result.status == LIVE_REF_CAS_COMMITTED
        and live_result.reference_cas_committed
        and live_result.checkpoint_reference
        == request.checkpoint_reference
        and live_result.expected_current_oid == request.expected_current_oid
        and live_result.proposed_checkpoint_oid == request.constructed_commit_oid
        and live_result.observed_after_oid == request.constructed_commit_oid
        and not live_result.object_database_write_performed
    )
    if published:
        status = COMMIT_PUBLISHED
        reason = "CONSTRUCTED_COMMIT_PUBLISHED_BY_ATOMIC_CHECKPOINT_CAS"
    elif live_result is not None and live_result.status == LIVE_REF_CAS_ERROR:
        status = PUBLICATION_ERROR
        reason = "CONSTRUCTED_COMMIT_PUBLICATION_DELEGATED_ERROR"
    elif live_result is not None and live_result.checkpoint_reference_write_performed:
        status = PUBLICATION_ERROR
        reason = "CONSTRUCTED_COMMIT_PUBLICATION_WRITE_NOT_COMMITTED"
    else:
        status = PUBLICATION_REJECTED
        reason = "CONSTRUCTED_COMMIT_PUBLICATION_PRECONDITION_OR_CAS_REJECTED"

    result = RepositoryConstructedCommitPublicationResult(
        publication_id=request.publication_id,
        status=status,
        reason=reason,
        policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        v120_result_digest=v120_result.result_digest,
        live_ref_cas_request_digest=live_ref_cas_request.request_digest,
        live_ref_cas_result_digest=(
            live_result.result_digest if live_result is not None else ""
        ),
        repository_path_digest=request.repository_path_digest,
        repository_id=request.repository_id,
        git_dir_fingerprint=request.git_dir_fingerprint,
        checkpoint_reference=request.checkpoint_reference,
        expected_current_oid=request.expected_current_oid,
        constructed_commit_oid=request.constructed_commit_oid,
        observed_before_oid=(
            live_result.observed_before_oid if live_result is not None else ""
        ),
        observed_after_oid=(
            live_result.observed_after_oid if live_result is not None else ""
        ),
        executor_id=request.executor_id,
        policy_valid=policy_valid,
        request_valid=request_valid,
        v120_result_valid=v120_valid,
        v120_result_accepted=v120_accepted,
        constructed_commit_binding_exact=constructed_commit_binding_exact,
        live_ref_cas_request_valid=live_request_valid,
        live_ref_cas_request_binding_exact=live_request_binding_exact,
        executor_authorized=executor_authorized,
        repository_path_allowed=repository_path_allowed,
        delegated_live_ref_cas_invoked=live_result is not None,
        delegated_live_ref_cas_valid=delegated_valid,
        reference_cas_committed=published,
        prior_object_database_write_performed=v120_result.object_database_write_performed,
        current_object_database_write_performed=(
            live_result.object_database_write_performed
            if live_result is not None
            else False
        ),
        live_repository_mutated=(
            live_result.live_repository_mutated if live_result is not None else False
        ),
        checkpoint_reference_write_performed=(
            live_result.checkpoint_reference_write_performed
            if live_result is not None
            else False
        ),
        index_write_performed=(
            live_result.index_write_performed if live_result is not None else False
        ),
        working_tree_write_performed=(
            live_result.working_tree_write_performed
            if live_result is not None
            else False
        ),
        reflog_write_performed=(
            live_result.reflog_write_performed if live_result is not None else False
        ),
        force_update_performed=(
            live_result.force_update_performed if live_result is not None else False
        ),
        reference_delete_performed=(
            live_result.reference_delete_performed
            if live_result is not None
            else False
        ),
        head_updated=live_result.head_updated if live_result is not None else False,
        branch_updated=(
            live_result.branch_updated if live_result is not None else False
        ),
        tag_updated=live_result.tag_updated if live_result is not None else False,
        remote_reference_updated=(
            live_result.remote_reference_updated if live_result is not None else False
        ),
        push_performed=live_result.push_performed if live_result is not None else False,
        signing_performed=(
            live_result.signing_performed if live_result is not None else False
        ),
        checks={
            "policy_valid": policy_valid,
            "request_valid": request_valid,
            "v120_result_valid": v120_valid,
            "v120_result_accepted": v120_accepted,
            "constructed_commit_binding_exact": constructed_commit_binding_exact,
            "live_ref_cas_request_valid": live_request_valid,
            "live_ref_cas_request_binding_exact": live_request_binding_exact,
            "executor_authorized": executor_authorized,
            "repository_path_allowed": repository_path_allowed,
            "delegated_live_ref_cas_valid": delegated_valid,
            "reference_cas_committed": published,
        },
        evidence_digests={
            "v120_result": v120_result.result_digest,
            "v121_policy": policy.policy_digest,
            "v121_request": request.request_digest,
            "v118_request": live_ref_cas_request.request_digest,
            "v118_result": live_result.result_digest if live_result is not None else "",
        },
        result_digest="",
    )
    result = replace(
        result,
        result_digest=repository_constructed_commit_publication_result_digest(result),
    )
    issues = repository_constructed_commit_publication_result_issues(result)
    if issues:
        raise ValueError(f"constructed_commit_publication_result_invalid:{issues[0]}")
    return result
