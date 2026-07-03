from __future__ import annotations

from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_transition_decision_core_v0_18 import (
    artifact_issues as source_artifact_issues,
)
from runtime.kuuos_lifecycle_transition_decision_source_v0_18 import (
    all_source_digests as prior_source_digests,
)
from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import (
    LifecycleTransitionDecisionArtifactV018,
    LifecycleTransitionDecisionEvidenceV018,
    LifecycleTransitionDecisionPolicyV018,
    LifecycleTransitionDecisionSubmissionV018,
)


def all_source_digests(
    source_decision: LifecycleTransitionDecisionSubmissionV018,
    source_evidence: LifecycleTransitionDecisionEvidenceV018,
    source_policy: LifecycleTransitionDecisionPolicyV018,
    source_record: LifecycleTransitionDecisionArtifactV018,
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
        lifecycle_transition_decision=source_decision.decision_digest,
        lifecycle_transition_decision_evidence=source_evidence.evidence_digest,
        lifecycle_transition_decision_policy=source_policy.policy_digest,
        lifecycle_transition_decision_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(
    source_decision: LifecycleTransitionDecisionSubmissionV018,
    source_evidence: LifecycleTransitionDecisionEvidenceV018,
    source_policy: LifecycleTransitionDecisionPolicyV018,
    source_record: LifecycleTransitionDecisionArtifactV018,
    source_args: tuple[Any, ...],
) -> bool:
    return not source_artifact_issues(
        source_record,
        source_decision,
        source_evidence,
        source_policy,
        *source_args,
    )


def prior_actor_ids(
    source_decision: LifecycleTransitionDecisionSubmissionV018,
    source_evidence: LifecycleTransitionDecisionEvidenceV018,
) -> set[str]:
    return {
        source_decision.subject_id,
        source_decision.requester_id,
        source_evidence.source_decision_reviewer_id,
        source_evidence.source_authorization_decision_maker_id,
        source_evidence.source_operation_approver_id,
        source_evidence.source_operator_id,
        source_evidence.source_completion_reviewer_id,
        source_evidence.source_post_operation_reviewer_id,
        source_evidence.source_transition_reviewer_id,
        source_decision.transition_decision_maker_id,
        source_decision.transition_preparer_id,
    }


def expected_transition_approval_route_digest(
    source_decision: LifecycleTransitionDecisionSubmissionV018,
    source_record: LifecycleTransitionDecisionArtifactV018,
    *,
    transition_package_digest: str,
    transition_approver_id: str,
    future_transition_operator_id: str,
    expected_current_lifecycle_state_digest: str,
    proposed_target_lifecycle_state_digest: str,
    transition_approval_deadline_at_epoch_seconds: int,
) -> str:
    return canonical_digest(
        {
            "source_transition_decision_id": source_decision.transition_decision_id,
            "source_transition_decision_record_digest": source_record.record_digest,
            "source_transition_preparation_route_digest": (
                source_decision.transition_preparation_route_digest
            ),
            "transition_package_digest": transition_package_digest,
            "transition_approver_id": transition_approver_id,
            "future_transition_operator_id": future_transition_operator_id,
            "expected_current_lifecycle_state_digest": (
                expected_current_lifecycle_state_digest
            ),
            "proposed_target_lifecycle_state_digest": (
                proposed_target_lifecycle_state_digest
            ),
            "transition_approval_deadline_at_epoch_seconds": (
                transition_approval_deadline_at_epoch_seconds
            ),
        }
    )
