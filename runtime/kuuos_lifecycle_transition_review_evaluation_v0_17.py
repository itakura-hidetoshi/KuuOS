from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import (
    REVIEWED as SOURCE_REVIEWED,
    LifecyclePostOperationReviewArtifactV016,
    LifecyclePostOperationReviewEvidenceV016,
    LifecyclePostOperationReviewPolicyV016,
    LifecyclePostOperationReviewSubmissionV016,
)
from runtime.kuuos_lifecycle_transition_review_binding_v0_17 import (
    evidence_issues,
    scope_matches,
    submission_issues,
)
from runtime.kuuos_lifecycle_transition_review_policy_v0_17 import policy_issues
from runtime.kuuos_lifecycle_transition_review_source_v0_17 import (
    all_source_digests,
    expected_transition_review_route_digest,
    source_recomputed_valid,
)
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import (
    OBJECTIVE,
    LifecycleTransitionReviewEvidenceV017,
    LifecycleTransitionReviewPolicyV017,
    LifecycleTransitionReviewSubmissionV017,
)

STRUCTURAL_CHECKS = (
    "policy_valid",
    "review_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_post_operation_review_completed",
    "source_binding_valid",
    "identity_binding_valid",
    "transition_reviewer_allowed",
    "transition_reviewer_organization_allowed",
    "transition_decision_maker_allowed",
    "transition_reviewer_separated_from_source_reviewer",
    "transition_reviewer_separated_from_completion_reviewer",
    "transition_reviewer_separated_from_operator",
    "transition_reviewer_separated_from_requester",
    "transition_reviewer_separated_from_source_decision_reviewer",
    "transition_reviewer_separated_from_authorization_decision_maker",
    "transition_reviewer_separated_from_operation_approver",
    "transition_reviewer_separated_from_subject",
    "transition_reviewer_separated_from_transition_decision_maker",
    "transition_reviewer_organization_separated",
    "objective_allowed",
    "transition_kind_allowed",
    "review_delay_valid",
    "evidence_fresh",
    "review_expiry_valid",
    "decision_delay_valid",
    "time_order_valid",
    "transition_review_route_binding_valid",
    "scope_binding_valid",
    "scope_bounded",
    "target_resources_allowed",
    "protected_resources_excluded",
    "external_operation_absent",
    "repository_change_absent",
)

BLOCKING_CHECKS = (
    "transition_reviewer_mandate_verified",
    "transition_reviewer_qualification_verified",
    "transition_reviewer_identity_confirmed",
    "conflict_disclosure_complete",
    "material_conflict_absent",
    "jurisdiction_verified",
    "review_ready",
    "transition_basis_sufficient",
    "necessity_verified",
    "proportionality_verified",
    "reversibility_or_exception_justified",
    "dependencies_cleared",
    "authority_continuity_verified",
    "transition_state_compatible",
    "stakeholder_impact_acceptable",
    "legal_policy_compliant",
    "appeal_route_available",
    "dissent_route_available",
    "minority_opinion_recorded",
    "no_unresolved_anomaly",
    "recovery_not_required",
    "institutional_hold_absent",
    "emergency_state_absent",
)


def _source_reviewed(record: LifecyclePostOperationReviewArtifactV016) -> bool:
    return all(
        (
            record.status == SOURCE_REVIEWED,
            record.operation_completed,
            record.post_operation_review_record_issued,
            record.post_operation_review_decision_made,
            record.post_operation_review_completed,
            not record.post_operation_review_denied,
            record.lifecycle_transition_review_required_next,
            record.lifecycle_transition_review_route_required_next,
            not record.operation_recovery_assessment_required_next,
            not record.operation_recovery_assessment_route_required_next,
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
    review: LifecycleTransitionReviewSubmissionV017,
    evidence: LifecycleTransitionReviewEvidenceV017,
    policy: LifecycleTransitionReviewPolicyV017,
    source_review: LifecyclePostOperationReviewSubmissionV016,
    source_evidence: LifecyclePostOperationReviewEvidenceV016,
    source_policy: LifecyclePostOperationReviewPolicyV016,
    source_record: LifecyclePostOperationReviewArtifactV016,
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
            (review.subject_id, review.subject_kind, review.subject_version)
            == (evidence.subject_id, evidence.subject_kind, evidence.subject_version)
            == (source_review.subject_id, source_review.subject_kind, source_review.subject_version),
            review.source_post_operation_review_id
            == evidence.source_post_operation_review_id
            == source_review.post_operation_review_id,
            review.source_post_operation_review_record_digest
            == evidence.source_post_operation_review_record_digest
            == source_record.record_digest,
            evidence.source_artifact_digests == expected_digests,
            review.requester_id == evidence.requester_id == source_review.requester_id,
            review.source_post_operation_reviewer_id
            == evidence.source_post_operation_reviewer_id
            == source_review.post_operation_reviewer_id,
            evidence.source_post_operation_reviewer_organization_id
            == source_evidence.post_operation_reviewer_organization_id,
            review.source_completion_reviewer_id
            == evidence.source_completion_reviewer_id
            == source_review.source_completion_reviewer_id,
            review.source_operator_id
            == evidence.source_operator_id
            == source_review.source_operator_id,
            review.source_operation_approver_id
            == evidence.source_operation_approver_id
            == source_review.source_operation_approver_id,
            review.source_authorization_decision_maker_id
            == evidence.source_authorization_decision_maker_id
            == source_review.source_authorization_decision_maker_id,
            review.source_decision_reviewer_id
            == evidence.source_decision_reviewer_id
            == source_review.source_decision_reviewer_id,
        )
    )
    identity_binding = all(
        (
            review.transition_review_id == evidence.transition_review_id,
            review.transition_reviewer_id == evidence.transition_reviewer_id,
            review.transition_reviewer_organization_id
            == evidence.transition_reviewer_organization_id,
            review.transition_review_evidence_digest == evidence.evidence_digest,
            review.transition_decision_maker_id == evidence.transition_decision_maker_id,
            review.proposed_transition_kind == evidence.proposed_transition_kind,
            review.proposed_target_state_digest == evidence.proposed_target_state_digest,
            review.review_requested_at_epoch_seconds
            == evidence.review_requested_at_epoch_seconds,
            review.reviewed_at_epoch_seconds == evidence.reviewed_at_epoch_seconds,
            review.review_expiry_at_epoch_seconds
            == evidence.review_expiry_at_epoch_seconds,
            review.transition_decision_deadline_at_epoch_seconds
            == evidence.transition_decision_deadline_at_epoch_seconds,
            review.transition_review_route_digest == evidence.transition_review_route_digest,
        )
    )
    delay = review.reviewed_at_epoch_seconds - source_review.reviewed_at_epoch_seconds
    age = review.reviewed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    expiry_span = evidence.review_expiry_at_epoch_seconds - evidence.reviewed_at_epoch_seconds
    decision_delay = (
        evidence.transition_decision_deadline_at_epoch_seconds
        - evidence.reviewed_at_epoch_seconds
    )
    time_order = (
        source_review.reviewed_at_epoch_seconds
        <= evidence.review_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.reviewed_at_epoch_seconds
        < evidence.review_expiry_at_epoch_seconds
        <= evidence.transition_decision_deadline_at_epoch_seconds
    )
    expected_route = expected_transition_review_route_digest(
        source_review,
        source_evidence,
        source_record,
        transition_decision_maker_id=evidence.transition_decision_maker_id,
        proposed_transition_kind=evidence.proposed_transition_kind,
        proposed_target_state_digest=evidence.proposed_target_state_digest,
        transition_decision_deadline_at_epoch_seconds=(
            evidence.transition_decision_deadline_at_epoch_seconds
        ),
    )
    targets = set(evidence.target_resource_ids)
    protected = set(evidence.protected_resource_ids)
    checks = {
        "policy_valid": not policy_issues(policy),
        "review_valid": not submission_issues(review),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(
            source_review,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        "source_post_operation_review_completed": _source_reviewed(source_record),
        "source_binding_valid": source_binding,
        "identity_binding_valid": identity_binding,
        "transition_reviewer_allowed": (
            review.transition_reviewer_id in policy.allowed_transition_reviewer_ids
        ),
        "transition_reviewer_organization_allowed": (
            review.transition_reviewer_organization_id
            in policy.allowed_transition_reviewer_organization_ids
        ),
        "transition_decision_maker_allowed": (
            review.transition_decision_maker_id
            in policy.allowed_transition_decision_maker_ids
        ),
        "transition_reviewer_separated_from_source_reviewer": (
            review.transition_reviewer_id != review.source_post_operation_reviewer_id
        ),
        "transition_reviewer_separated_from_completion_reviewer": (
            review.transition_reviewer_id != review.source_completion_reviewer_id
        ),
        "transition_reviewer_separated_from_operator": (
            review.transition_reviewer_id != review.source_operator_id
        ),
        "transition_reviewer_separated_from_requester": (
            review.transition_reviewer_id != review.requester_id
        ),
        "transition_reviewer_separated_from_source_decision_reviewer": (
            review.transition_reviewer_id != review.source_decision_reviewer_id
        ),
        "transition_reviewer_separated_from_authorization_decision_maker": (
            review.transition_reviewer_id
            != review.source_authorization_decision_maker_id
        ),
        "transition_reviewer_separated_from_operation_approver": (
            review.transition_reviewer_id != review.source_operation_approver_id
        ),
        "transition_reviewer_separated_from_subject": (
            review.transition_reviewer_id != review.subject_id
        ),
        "transition_reviewer_separated_from_transition_decision_maker": (
            review.transition_reviewer_id != review.transition_decision_maker_id
        ),
        "transition_reviewer_organization_separated": (
            review.transition_reviewer_organization_id
            != evidence.source_post_operation_reviewer_organization_id
        ),
        "objective_allowed": review.objective == OBJECTIVE,
        "transition_kind_allowed": (
            review.proposed_transition_kind in policy.allowed_transition_kinds
        ),
        "review_delay_valid": 0 <= delay <= policy.max_review_delay_seconds,
        "evidence_fresh": 0 <= age <= policy.max_evidence_age_seconds,
        "review_expiry_valid": 0 < expiry_span <= policy.max_review_expiry_seconds,
        "decision_delay_valid": 0 < decision_delay <= policy.max_decision_delay_seconds,
        "time_order_valid": time_order,
        "transition_review_route_binding_valid": (
            review.transition_review_route_digest
            == evidence.transition_review_route_digest
            == expected_route
        ),
        "scope_binding_valid": scope_matches(evidence, source_evidence),
        "scope_bounded": 0 < len(evidence.operation_scope_items) <= policy.max_scope_items,
        "target_resources_allowed": bool(targets)
        and targets.issubset(set(policy.allowed_target_resource_ids)),
        "protected_resources_excluded": not (targets & protected),
        "external_operation_absent": not evidence.external_operation_performed,
        "repository_change_absent": not evidence.repository_changed,
        "transition_reviewer_mandate_verified": (
            evidence.transition_reviewer_mandate_verified
        ),
        "transition_reviewer_qualification_verified": (
            evidence.transition_reviewer_qualification_verified
        ),
        "transition_reviewer_identity_confirmed": (
            evidence.transition_reviewer_identity_confirmed
        ),
        "conflict_disclosure_complete": evidence.conflict_disclosure_complete,
        "material_conflict_absent": not evidence.material_conflict_present,
        "jurisdiction_verified": evidence.jurisdiction_verified,
        "review_ready": evidence.review_ready,
        "transition_basis_sufficient": evidence.transition_basis_sufficient,
        "necessity_verified": evidence.necessity_verified,
        "proportionality_verified": evidence.proportionality_verified,
        "reversibility_or_exception_justified": (
            evidence.reversibility_or_exception_justified
        ),
        "dependencies_cleared": evidence.dependencies_cleared,
        "authority_continuity_verified": evidence.authority_continuity_verified,
        "transition_state_compatible": evidence.transition_state_compatible,
        "stakeholder_impact_acceptable": evidence.stakeholder_impact_acceptable,
        "legal_policy_compliant": evidence.legal_policy_compliant,
        "appeal_route_available": evidence.appeal_route_available,
        "dissent_route_available": evidence.dissent_route_available,
        "minority_opinion_recorded": evidence.minority_opinion_recorded,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_required": not evidence.recovery_required,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests
