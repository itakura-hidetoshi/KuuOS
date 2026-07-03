from __future__ import annotations

from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_transition_review_core_v0_17 import (
    artifact_issues as source_artifact_issues,
)
from runtime.kuuos_lifecycle_transition_review_source_v0_17 import (
    all_source_digests as prior_source_digests,
)
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import (
    LifecycleTransitionReviewArtifactV017,
    LifecycleTransitionReviewEvidenceV017,
    LifecycleTransitionReviewPolicyV017,
    LifecycleTransitionReviewSubmissionV017,
)


def all_source_digests(
    source_review: LifecycleTransitionReviewSubmissionV017,
    source_evidence: LifecycleTransitionReviewEvidenceV017,
    source_policy: LifecycleTransitionReviewPolicyV017,
    source_record: LifecycleTransitionReviewArtifactV017,
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
        lifecycle_transition_review=source_review.review_digest,
        lifecycle_transition_review_evidence=source_evidence.evidence_digest,
        lifecycle_transition_review_policy=source_policy.policy_digest,
        lifecycle_transition_review_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(
    source_review: LifecycleTransitionReviewSubmissionV017,
    source_evidence: LifecycleTransitionReviewEvidenceV017,
    source_policy: LifecycleTransitionReviewPolicyV017,
    source_record: LifecycleTransitionReviewArtifactV017,
    source_args: tuple[Any, ...],
) -> bool:
    return not source_artifact_issues(
        source_record,
        source_review,
        source_evidence,
        source_policy,
        *source_args,
    )


def prior_actor_ids(source_review: LifecycleTransitionReviewSubmissionV017) -> set[str]:
    return {
        source_review.subject_id,
        source_review.requester_id,
        source_review.source_decision_reviewer_id,
        source_review.source_authorization_decision_maker_id,
        source_review.source_operation_approver_id,
        source_review.source_operator_id,
        source_review.source_completion_reviewer_id,
        source_review.source_post_operation_reviewer_id,
        source_review.transition_reviewer_id,
    }


def expected_transition_preparation_route_digest(
    source_review: LifecycleTransitionReviewSubmissionV017,
    source_evidence: LifecycleTransitionReviewEvidenceV017,
    source_record: LifecycleTransitionReviewArtifactV017,
    *,
    transition_preparer_id: str,
    expected_current_lifecycle_state_digest: str,
    proposed_target_lifecycle_state_digest: str,
    transition_rule_digest: str,
    transition_preparation_deadline_at_epoch_seconds: int,
) -> str:
    return canonical_digest(
        {
            "source_transition_review_id": source_review.transition_review_id,
            "source_transition_review_record_digest": source_record.record_digest,
            "source_transition_reviewer_id": source_review.transition_reviewer_id,
            "source_transition_review_route_digest": (
                source_evidence.transition_review_route_digest
            ),
            "proposed_transition_kind": source_review.proposed_transition_kind,
            "expected_current_lifecycle_state_digest": (
                expected_current_lifecycle_state_digest
            ),
            "proposed_target_lifecycle_state_digest": (
                proposed_target_lifecycle_state_digest
            ),
            "transition_rule_digest": transition_rule_digest,
            "transition_preparer_id": transition_preparer_id,
            "transition_preparation_deadline_at_epoch_seconds": (
                transition_preparation_deadline_at_epoch_seconds
            ),
        }
    )
