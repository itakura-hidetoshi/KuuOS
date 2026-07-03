from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_decision_review_core_v0_11 import (
    artifact_issues as source_artifact_issues,
)
from runtime.kuuos_lifecycle_decision_review_source_v0_11 import (
    all_source_digests as prior_source_digests,
    prior_actor_ids as prior_review_actor_ids,
)
from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    LifecycleDecisionReviewArtifactV011,
    LifecycleDecisionReviewEvidenceV011,
    LifecycleDecisionReviewPolicyV011,
    LifecycleDecisionReviewSubmissionV011,
)


def all_source_digests(
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_evidence: LifecycleDecisionReviewEvidenceV011,
    source_policy: LifecycleDecisionReviewPolicyV011,
    source_record: LifecycleDecisionReviewArtifactV011,
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
        lifecycle_decision_review=source_review.review_digest,
        lifecycle_decision_review_evidence=source_evidence.evidence_digest,
        lifecycle_decision_review_policy=source_policy.policy_digest,
        lifecycle_decision_review_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_evidence: LifecycleDecisionReviewEvidenceV011,
    source_policy: LifecycleDecisionReviewPolicyV011,
    source_record: LifecycleDecisionReviewArtifactV011,
    source_args: tuple[Any, ...],
) -> bool:
    return not source_artifact_issues(
        source_record,
        source_review,
        source_evidence,
        source_policy,
        *source_args,
    )


def prior_actor_ids(
    subject_id: str,
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_args: tuple[Any, ...],
) -> set[str]:
    if len(source_args) < 8:
        raise ValueError("source_argument_count_invalid")
    source_request = source_args[0]
    result = prior_review_actor_ids(
        subject_id,
        source_request,
        tuple(source_args[4:]),
    )
    result.update(
        {
            source_review.requester_id,
            source_review.decision_reviewer_id,
        }
    )
    return result
