from __future__ import annotations

from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_post_operation_review_core_v0_16 import (
    artifact_issues as source_artifact_issues,
)
from runtime.kuuos_lifecycle_post_operation_review_source_v0_16 import (
    all_source_digests as prior_source_digests,
)
from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import (
    LifecyclePostOperationReviewArtifactV016,
    LifecyclePostOperationReviewEvidenceV016,
    LifecyclePostOperationReviewPolicyV016,
    LifecyclePostOperationReviewSubmissionV016,
)


def all_source_digests(
    source_review: LifecyclePostOperationReviewSubmissionV016,
    source_evidence: LifecyclePostOperationReviewEvidenceV016,
    source_policy: LifecyclePostOperationReviewPolicyV016,
    source_record: LifecyclePostOperationReviewArtifactV016,
    source_args: tuple[Any, ...],
) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = prior_source_digests(
        source_args[0],
        source_args[1],
        source_args[2],
        source_args[3],
        tuple(source_args[4:]),
    )
    result.update(
        lifecycle_post_operation_review=source_review.review_digest,
        lifecycle_post_operation_review_evidence=source_evidence.evidence_digest,
        lifecycle_post_operation_review_policy=source_policy.policy_digest,
        lifecycle_post_operation_review_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(
    source_review: LifecyclePostOperationReviewSubmissionV016,
    source_evidence: LifecyclePostOperationReviewEvidenceV016,
    source_policy: LifecyclePostOperationReviewPolicyV016,
    source_record: LifecyclePostOperationReviewArtifactV016,
    source_args: tuple[Any, ...],
) -> bool:
    return not source_artifact_issues(
        source_record,
        source_review,
        source_evidence,
        source_policy,
        *source_args,
    )


def prior_actor_ids(source_review: LifecyclePostOperationReviewSubmissionV016) -> set[str]:
    return {
        source_review.subject_id,
        source_review.requester_id,
        source_review.source_decision_reviewer_id,
        source_review.source_authorization_decision_maker_id,
        source_review.source_operation_approver_id,
        source_review.source_operator_id,
        source_review.source_completion_reviewer_id,
        source_review.post_operation_reviewer_id,
    }


def expected_transition_review_route_digest(
    source_review: LifecyclePostOperationReviewSubmissionV016,
    source_evidence: LifecyclePostOperationReviewEvidenceV016,
    source_record: LifecyclePostOperationReviewArtifactV016,
    *,
    transition_decision_maker_id: str,
    proposed_transition_kind: str,
    proposed_target_state_digest: str,
    transition_decision_deadline_at_epoch_seconds: int,
) -> str:
    return canonical_digest(
        {
            "source_post_operation_review_id": source_review.post_operation_review_id,
            "source_post_operation_review_record_digest": source_record.record_digest,
            "source_post_operation_reviewer_id": source_review.post_operation_reviewer_id,
            "source_post_operation_review_route_digest": (
                source_evidence.post_operation_review_route_digest
            ),
            "source_operation_execution_result_digest": (
                source_evidence.source_operation_execution_result_digest
            ),
            "source_target_resource_post_state_digest": (
                source_evidence.source_target_resource_post_state_digest
            ),
            "transition_decision_maker_id": transition_decision_maker_id,
            "proposed_transition_kind": proposed_transition_kind,
            "proposed_target_state_digest": proposed_target_state_digest,
            "transition_decision_deadline_at_epoch_seconds": (
                transition_decision_deadline_at_epoch_seconds
            ),
        }
    )
