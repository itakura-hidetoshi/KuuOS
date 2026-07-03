#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_lifecycle_bounded_transition_review_v0_17"
CLEAR = "LIFECYCLE_BOUNDED_TRANSITION_REVIEW_CLEAR_FOR_SEPARATE_TRANSITION_DECISION"
BLOCKED = "LIFECYCLE_BOUNDED_TRANSITION_REVIEW_BLOCKED"
REJECTED = "LIFECYCLE_BOUNDED_TRANSITION_REVIEW_REJECTED"
OBJECTIVE = "REVIEW_POST_OPERATION_OUTCOME_FOR_SEPARATE_LIFECYCLE_TRANSITION_DECISION_ONLY"


@dataclass(frozen=True)
class LifecycleTransitionReviewPolicyV017:
    policy_id: str
    allowed_transition_reviewer_ids: tuple[str, ...]
    allowed_transition_reviewer_organization_ids: tuple[str, ...]
    allowed_transition_decision_maker_ids: tuple[str, ...]
    allowed_target_resource_ids: tuple[str, ...]
    allowed_transition_kinds: tuple[str, ...]
    max_review_delay_seconds: int
    max_evidence_age_seconds: int
    max_review_expiry_seconds: int
    max_decision_delay_seconds: int
    max_scope_items: int
    require_complete_source_recomputation: bool
    require_reviewed_source_post_operation_review: bool
    require_exact_source_artifact_binding: bool
    require_exact_transition_reviewer_binding: bool
    require_exact_route_binding: bool
    require_transition_reviewer_source_reviewer_separation: bool
    require_transition_reviewer_prior_actor_separation: bool
    require_transition_reviewer_decision_maker_separation: bool
    require_transition_reviewer_organization_separation: bool
    require_transition_reviewer_mandate: bool
    require_transition_reviewer_qualification: bool
    require_transition_reviewer_identity_confirmation: bool
    require_conflict_disclosure: bool
    require_jurisdiction: bool
    require_review_readiness: bool
    require_transition_basis: bool
    require_necessity_assessment: bool
    require_proportionality_assessment: bool
    require_reversibility_assessment: bool
    require_dependency_clearance: bool
    require_authority_continuity: bool
    require_transition_state_compatibility: bool
    require_stakeholder_impact_assessment: bool
    require_legal_policy_compliance: bool
    require_appeal_route: bool
    require_dissent_route: bool
    require_minority_opinion_record: bool
    require_no_unresolved_anomaly: bool
    require_no_recovery: bool
    require_no_institutional_hold: bool
    require_no_emergency_state: bool
    transition_review_artifact_only: bool
    lifecycle_state_read_only: bool
    repository_read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "allowed_transition_reviewer_ids",
            "allowed_transition_reviewer_organization_ids",
            "allowed_transition_decision_maker_ids",
            "allowed_target_resource_ids",
            "allowed_transition_kinds",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleTransitionReviewEvidenceV017:
    evidence_id: str
    transition_review_id: str
    transition_reviewer_id: str
    transition_reviewer_organization_id: str
    transition_reviewer_mandate_receipt_digest: str
    transition_reviewer_mandate_verified: bool
    transition_reviewer_qualification_receipt_digest: str
    transition_reviewer_qualification_verified: bool
    transition_reviewer_identity_confirmation_digest: str
    transition_reviewer_identity_confirmed: bool
    conflict_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    jurisdiction_receipt_digest: str
    jurisdiction_verified: bool
    review_readiness_receipt_digest: str
    review_ready: bool
    source_post_operation_review_id: str
    source_post_operation_review_record_digest: str
    source_artifact_digests: dict[str, str]
    source_post_operation_reviewer_id: str
    source_post_operation_reviewer_organization_id: str
    source_completion_reviewer_id: str
    source_operator_id: str
    source_operation_approver_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    subject_id: str
    subject_kind: str
    subject_version: str
    requester_id: str
    transition_decision_maker_id: str
    transition_review_route_digest: str
    reviewed_scope_digest: str
    operation_scope_items: tuple[str, ...]
    target_resource_ids: tuple[str, ...]
    protected_resource_ids: tuple[str, ...]
    reversible_step_ids: tuple[str, ...]
    step_result_digests: dict[str, str]
    operation_execution_result_digest: str
    target_resource_post_state_digest: str
    proposed_transition_kind: str
    current_lifecycle_state_digest: str
    proposed_target_state_digest: str
    transition_basis_digest: str
    transition_basis_sufficient: bool
    necessity_assessment_digest: str
    necessity_verified: bool
    proportionality_assessment_digest: str
    proportionality_verified: bool
    reversibility_assessment_digest: str
    reversibility_or_exception_justified: bool
    dependency_clearance_digest: str
    dependencies_cleared: bool
    authority_continuity_digest: str
    authority_continuity_verified: bool
    transition_state_compatibility_digest: str
    transition_state_compatible: bool
    stakeholder_impact_assessment_digest: str
    stakeholder_impact_acceptable: bool
    legal_policy_compliance_digest: str
    legal_policy_compliant: bool
    appeal_route_digest: str
    appeal_route_available: bool
    dissent_route_digest: str
    dissent_route_available: bool
    minority_opinion_digest: str
    minority_opinion_recorded: bool
    unresolved_anomaly_present: bool
    recovery_required: bool
    institutional_hold_active: bool
    emergency_state_active: bool
    external_operation_performed: bool
    repository_changed: bool
    review_requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    reviewed_at_epoch_seconds: int
    review_expiry_at_epoch_seconds: int
    transition_decision_deadline_at_epoch_seconds: int
    evidence_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "operation_scope_items",
            "target_resource_ids",
            "protected_resource_ids",
            "reversible_step_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleTransitionReviewSubmissionV017:
    transition_review_id: str
    transition_reviewer_id: str
    transition_reviewer_organization_id: str
    objective: str
    review_requested_at_epoch_seconds: int
    reviewed_at_epoch_seconds: int
    review_expiry_at_epoch_seconds: int
    source_post_operation_review_id: str
    source_post_operation_review_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    transition_review_evidence_digest: str
    requester_id: str
    source_post_operation_reviewer_id: str
    source_completion_reviewer_id: str
    source_operator_id: str
    source_operation_approver_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    transition_decision_maker_id: str
    proposed_transition_kind: str
    proposed_target_state_digest: str
    transition_review_route_digest: str
    transition_decision_deadline_at_epoch_seconds: int
    review_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleTransitionReviewArtifactV017:
    transition_review_id: str
    status: str
    reason: str
    transition_reviewer_id: str
    transition_reviewer_organization_id: str
    source_post_operation_review_id: str
    source_post_operation_reviewer_id: str
    transition_decision_maker_id: str
    proposed_transition_kind: str
    subject_id: str
    requester_id: str
    policy_digest: str
    review_digest: str
    evidence_digest: str
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    source_post_operation_review_completed: bool
    transition_review_record_issued: bool
    transition_review_completed: bool
    clear_for_transition_decision: bool
    transition_review_blocked: bool
    transition_decision_required_next: bool
    transition_decision_route_required_next: bool
    transition_reassessment_required_next: bool
    transition_reassessment_route_required_next: bool
    transition_decision_made: bool
    lifecycle_transition_performed: bool
    authority_changed: bool
    quiescence_state_changed: bool
    terminal_state_changed: bool
    terminal_marker_written: bool
    resource_removed: bool
    external_operation_performed: bool
    repository_changed: bool
    lifecycle_state_read_only: bool
    repository_read_only: bool
    record_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _digest_without(value: Any, field_name: str) -> str:
    payload = value.to_dict()
    payload.pop(field_name, None)
    return canonical_digest(payload)


def policy_digest(value: LifecycleTransitionReviewPolicyV017) -> str:
    return _digest_without(value, "policy_digest")


def evidence_digest(value: LifecycleTransitionReviewEvidenceV017) -> str:
    return _digest_without(value, "evidence_digest")


def submission_digest(value: LifecycleTransitionReviewSubmissionV017) -> str:
    return _digest_without(value, "review_digest")


def record_digest(value: LifecycleTransitionReviewArtifactV017) -> str:
    return _digest_without(value, "record_digest")
