from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_transition_decision_binding_v0_18 import (
    evidence_issues,
    submission_issues,
)
from runtime.kuuos_lifecycle_transition_decision_policy_v0_18 import policy_issues
from runtime.kuuos_lifecycle_transition_decision_source_v0_18 import (
    all_source_digests,
    expected_transition_preparation_route_digest,
    source_recomputed_valid,
)
from runtime.kuuos_lifecycle_transition_decision_state_v0_18 import allowed_transition
from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import (
    OBJECTIVE,
    LifecycleTransitionDecisionEvidenceV018,
    LifecycleTransitionDecisionPolicyV018,
    LifecycleTransitionDecisionSubmissionV018,
)
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import (
    CLEAR as SOURCE_CLEAR,
    LifecycleTransitionReviewArtifactV017,
    LifecycleTransitionReviewEvidenceV017,
    LifecycleTransitionReviewPolicyV017,
    LifecycleTransitionReviewSubmissionV017,
)

STRUCTURAL_CHECKS = (
    "policy_valid",
    "decision_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_transition_review_clear",
    "source_binding_valid",
    "identity_binding_valid",
    "decision_maker_allowed",
    "decision_maker_organization_allowed",
    "transition_preparer_allowed",
    "transition_kind_allowed",
    "decision_maker_separated_from_transition_reviewer",
    "decision_maker_separated_from_post_operation_reviewer",
    "decision_maker_separated_from_completion_reviewer",
    "decision_maker_separated_from_operator",
    "decision_maker_separated_from_operation_approver",
    "decision_maker_separated_from_authorization_decision_maker",
    "decision_maker_separated_from_source_decision_reviewer",
    "decision_maker_separated_from_requester",
    "decision_maker_separated_from_subject",
    "decision_maker_separated_from_preparer",
    "decision_maker_organization_separated",
    "objective_allowed",
    "decision_delay_valid",
    "evidence_fresh",
    "decision_expiry_valid",
    "preparation_delay_valid",
    "time_order_valid",
    "current_state_matches_reviewed_state",
    "target_state_matches_reviewed_state",
    "allowed_transition_relation_valid",
    "preparation_route_binding_valid",
    "decision_maker_mandate_verified",
    "decision_maker_qualification_verified",
    "decision_maker_identity_confirmed",
    "conflict_disclosure_complete",
    "material_conflict_absent",
    "jurisdiction_verified",
    "decision_ready",
    "decision_rationale_present",
    "denial_route_available",
    "appeal_route_available",
    "dissent_route_available",
    "minority_opinion_recorded",
    "external_operation_absent",
    "repository_change_absent",
)

DENIAL_CHECKS = (
    "decision_approved",
    "no_unresolved_anomaly",
    "recovery_not_required",
    "institutional_hold_absent",
    "emergency_state_absent",
)


def _source_clear(record: LifecycleTransitionReviewArtifactV017) -> bool:
    return all(
        (
            record.status == SOURCE_CLEAR,
            record.transition_review_record_issued,
            record.transition_review_completed,
            record.clear_for_transition_decision,
            not record.transition_review_blocked,
            record.transition_decision_required_next,
            record.transition_decision_route_required_next,
            not record.transition_reassessment_required_next,
            not record.transition_reassessment_route_required_next,
            not record.transition_decision_made,
            not record.lifecycle_transition_performed,
            not record.authority_changed,
            not record.quiescence_state_changed,
            not record.terminal_state_changed,
            not record.terminal_marker_written,
            not record.resource_removed,
            not record.external_operation_performed,
            not record.repository_changed,
            record.lifecycle_state_read_only,
            record.repository_read_only,
        )
    )


def evaluate(
    decision: LifecycleTransitionDecisionSubmissionV018,
    evidence: LifecycleTransitionDecisionEvidenceV018,
    policy: LifecycleTransitionDecisionPolicyV018,
    source_review: LifecycleTransitionReviewSubmissionV017,
    source_evidence: LifecycleTransitionReviewEvidenceV017,
    source_policy: LifecycleTransitionReviewPolicyV017,
    source_record: LifecycleTransitionReviewArtifactV017,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(
        source_review,
        source_evidence,
        source_policy,
        source_record,
        source_args,
    )
    source_binding = all(
        (
            decision.source_transition_review_id
            == evidence.source_transition_review_id
            == source_review.transition_review_id,
            decision.source_transition_review_record_digest
            == evidence.source_transition_review_record_digest
            == source_record.record_digest,
            evidence.source_artifact_digests == expected_digests,
            (decision.subject_id, decision.subject_kind, decision.subject_version)
            == (evidence.subject_id, evidence.subject_kind, evidence.subject_version)
            == (source_review.subject_id, source_review.subject_kind, source_review.subject_version),
            decision.requester_id == evidence.requester_id == source_review.requester_id,
            decision.source_transition_reviewer_id
            == evidence.source_transition_reviewer_id
            == source_review.transition_reviewer_id,
            evidence.source_transition_reviewer_organization_id
            == source_evidence.transition_reviewer_organization_id,
            evidence.source_post_operation_reviewer_id
            == source_review.source_post_operation_reviewer_id,
            evidence.source_completion_reviewer_id
            == source_review.source_completion_reviewer_id,
            evidence.source_operator_id == source_review.source_operator_id,
            evidence.source_operation_approver_id
            == source_review.source_operation_approver_id,
            evidence.source_authorization_decision_maker_id
            == source_review.source_authorization_decision_maker_id,
            evidence.source_decision_reviewer_id
            == source_review.source_decision_reviewer_id,
        )
    )
    identity_binding = all(
        (
            decision.transition_decision_id == evidence.transition_decision_id,
            decision.transition_decision_maker_id
            == evidence.transition_decision_maker_id
            == source_review.transition_decision_maker_id,
            decision.transition_decision_maker_organization_id
            == evidence.transition_decision_maker_organization_id,
            decision.transition_decision_evidence_digest == evidence.evidence_digest,
            decision.transition_preparer_id == evidence.transition_preparer_id,
            decision.proposed_transition_kind
            == evidence.proposed_transition_kind
            == source_review.proposed_transition_kind,
            decision.expected_current_lifecycle_state_digest
            == evidence.current_state.state_digest,
            decision.proposed_target_lifecycle_state_digest
            == evidence.target_state.state_digest,
            decision.transition_preparation_route_digest
            == evidence.transition_preparation_route_digest,
            decision.decision_requested_at_epoch_seconds
            == evidence.decision_requested_at_epoch_seconds,
            decision.decided_at_epoch_seconds == evidence.decided_at_epoch_seconds,
            decision.decision_expiry_at_epoch_seconds
            == evidence.decision_expiry_at_epoch_seconds,
            decision.transition_preparation_deadline_at_epoch_seconds
            == evidence.transition_preparation_deadline_at_epoch_seconds,
        )
    )
    delay = decision.decided_at_epoch_seconds - source_review.reviewed_at_epoch_seconds
    age = decision.decided_at_epoch_seconds - evidence.captured_at_epoch_seconds
    expiry_span = evidence.decision_expiry_at_epoch_seconds - evidence.decided_at_epoch_seconds
    preparation_delay = (
        evidence.transition_preparation_deadline_at_epoch_seconds
        - evidence.decided_at_epoch_seconds
    )
    time_order = (
        source_review.reviewed_at_epoch_seconds
        <= evidence.decision_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.decided_at_epoch_seconds
        < evidence.decision_expiry_at_epoch_seconds
        <= evidence.transition_preparation_deadline_at_epoch_seconds
    )
    expected_route = expected_transition_preparation_route_digest(
        source_review,
        source_evidence,
        source_record,
        transition_preparer_id=evidence.transition_preparer_id,
        expected_current_lifecycle_state_digest=evidence.current_state.state_digest,
        proposed_target_lifecycle_state_digest=evidence.target_state.state_digest,
        transition_rule_digest=evidence.transition_rule.rule_digest,
        transition_preparation_deadline_at_epoch_seconds=(
            evidence.transition_preparation_deadline_at_epoch_seconds
        ),
    )
    prior_ids = {
        evidence.source_transition_reviewer_id,
        evidence.source_post_operation_reviewer_id,
        evidence.source_completion_reviewer_id,
        evidence.source_operator_id,
        evidence.source_operation_approver_id,
        evidence.source_authorization_decision_maker_id,
        evidence.source_decision_reviewer_id,
        evidence.requester_id,
        evidence.subject_id,
    }
    checks = {
        "policy_valid": not policy_issues(policy),
        "decision_valid": not submission_issues(decision),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(
            source_review,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        "source_transition_review_clear": _source_clear(source_record),
        "source_binding_valid": source_binding,
        "identity_binding_valid": identity_binding,
        "decision_maker_allowed": (
            decision.transition_decision_maker_id
            in policy.allowed_transition_decision_maker_ids
        ),
        "decision_maker_organization_allowed": (
            decision.transition_decision_maker_organization_id
            in policy.allowed_transition_decision_maker_organization_ids
        ),
        "transition_preparer_allowed": (
            decision.transition_preparer_id in policy.allowed_transition_preparer_ids
        ),
        "transition_kind_allowed": (
            decision.proposed_transition_kind in policy.allowed_transition_kinds
        ),
        "decision_maker_separated_from_transition_reviewer": (
            decision.transition_decision_maker_id
            != evidence.source_transition_reviewer_id
        ),
        "decision_maker_separated_from_post_operation_reviewer": (
            decision.transition_decision_maker_id
            != evidence.source_post_operation_reviewer_id
        ),
        "decision_maker_separated_from_completion_reviewer": (
            decision.transition_decision_maker_id
            != evidence.source_completion_reviewer_id
        ),
        "decision_maker_separated_from_operator": (
            decision.transition_decision_maker_id != evidence.source_operator_id
        ),
        "decision_maker_separated_from_operation_approver": (
            decision.transition_decision_maker_id
            != evidence.source_operation_approver_id
        ),
        "decision_maker_separated_from_authorization_decision_maker": (
            decision.transition_decision_maker_id
            != evidence.source_authorization_decision_maker_id
        ),
        "decision_maker_separated_from_source_decision_reviewer": (
            decision.transition_decision_maker_id
            != evidence.source_decision_reviewer_id
        ),
        "decision_maker_separated_from_requester": (
            decision.transition_decision_maker_id != evidence.requester_id
        ),
        "decision_maker_separated_from_subject": (
            decision.transition_decision_maker_id != evidence.subject_id
        ),
        "decision_maker_separated_from_preparer": (
            decision.transition_decision_maker_id != evidence.transition_preparer_id
        ),
        "decision_maker_prior_actor_separation": (
            decision.transition_decision_maker_id not in prior_ids
        ),
        "decision_maker_organization_separated": (
            decision.transition_decision_maker_organization_id
            != evidence.source_transition_reviewer_organization_id
        ),
        "objective_allowed": decision.objective == OBJECTIVE,
        "decision_delay_valid": 0 <= delay <= policy.max_decision_delay_seconds,
        "evidence_fresh": 0 <= age <= policy.max_evidence_age_seconds,
        "decision_expiry_valid": (
            0 < expiry_span <= policy.max_decision_expiry_seconds
        ),
        "preparation_delay_valid": (
            0 < preparation_delay <= policy.max_preparation_delay_seconds
        ),
        "time_order_valid": time_order,
        "current_state_matches_reviewed_state": (
            evidence.current_state.state_digest
            == source_evidence.current_lifecycle_state_digest
        ),
        "target_state_matches_reviewed_state": (
            evidence.target_state.state_digest
            == source_evidence.proposed_target_state_digest
            == source_review.proposed_target_state_digest
        ),
        "allowed_transition_relation_valid": allowed_transition(
            evidence.current_state,
            evidence.proposed_transition_kind,
            evidence.target_state,
            evidence.transition_rule,
        ),
        "preparation_route_binding_valid": (
            decision.transition_preparation_route_digest
            == evidence.transition_preparation_route_digest
            == expected_route
        ),
        "decision_maker_mandate_verified": evidence.decision_maker_mandate_verified,
        "decision_maker_qualification_verified": (
            evidence.decision_maker_qualification_verified
        ),
        "decision_maker_identity_confirmed": (
            evidence.decision_maker_identity_confirmed
        ),
        "conflict_disclosure_complete": evidence.conflict_disclosure_complete,
        "material_conflict_absent": not evidence.material_conflict_present,
        "jurisdiction_verified": evidence.jurisdiction_verified,
        "decision_ready": evidence.decision_ready,
        "decision_rationale_present": bool(evidence.decision_rationale_digest),
        "denial_route_available": evidence.denial_route_available,
        "appeal_route_available": evidence.appeal_route_available,
        "dissent_route_available": evidence.dissent_route_available,
        "minority_opinion_recorded": evidence.minority_opinion_recorded,
        "external_operation_absent": not evidence.external_operation_performed,
        "repository_change_absent": not evidence.repository_changed,
        "decision_approved": evidence.decision_approved,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_required": not evidence.recovery_required,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests
