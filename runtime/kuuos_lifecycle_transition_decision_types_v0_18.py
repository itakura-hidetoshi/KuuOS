#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_lifecycle_bounded_transition_decision_v0_18"
APPROVED = "LIFECYCLE_BOUNDED_TRANSITION_DECISION_APPROVED_FOR_SEPARATE_TRANSITION_PREPARATION"
DENIED = "LIFECYCLE_BOUNDED_TRANSITION_DECISION_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_TRANSITION_DECISION_REJECTED"
OBJECTIVE = "DECIDE_REVIEWED_LIFECYCLE_TRANSITION_FOR_SEPARATE_PREPARATION_ONLY"


@dataclass(frozen=True)
class LifecycleStateV018:
    authority_state: str
    quiescence_state: str
    terminal_state: str
    resource_state: str
    state_revision: int
    state_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleTransitionRuleV018:
    rule_id: str
    current_state_digest: str
    transition_kind: str
    target_state_digest: str
    policy_basis_digest: str
    reversible_or_exception_required: bool
    authority_continuity_required: bool
    active: bool
    rule_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleTransitionDecisionPolicyV018:
    policy_id: str
    allowed_transition_decision_maker_ids: tuple[str, ...]
    allowed_transition_decision_maker_organization_ids: tuple[str, ...]
    allowed_transition_preparer_ids: tuple[str, ...]
    allowed_transition_kinds: tuple[str, ...]
    max_decision_delay_seconds: int
    max_evidence_age_seconds: int
    max_decision_expiry_seconds: int
    max_preparation_delay_seconds: int
    require_complete_source_recomputation: bool
    require_clear_source_transition_review: bool
    require_exact_source_artifact_binding: bool
    require_exact_state_snapshot_binding: bool
    require_allowed_transition_relation: bool
    require_current_state_not_stale: bool
    require_decision_maker_source_reviewer_separation: bool
    require_decision_maker_prior_actor_separation: bool
    require_decision_maker_preparer_separation: bool
    require_decision_maker_organization_separation: bool
    require_decision_maker_mandate: bool
    require_decision_maker_qualification: bool
    require_decision_maker_identity_confirmation: bool
    require_conflict_disclosure: bool
    require_jurisdiction: bool
    require_decision_readiness: bool
    require_decision_rationale: bool
    require_denial_route: bool
    require_appeal_route: bool
    require_dissent_route: bool
    require_minority_opinion_record: bool
    require_no_unresolved_anomaly: bool
    require_no_recovery: bool
    require_no_institutional_hold: bool
    require_no_emergency_state: bool
    transition_decision_artifact_only: bool
    lifecycle_state_read_only: bool
    repository_read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "allowed_transition_decision_maker_ids",
            "allowed_transition_decision_maker_organization_ids",
            "allowed_transition_preparer_ids",
            "allowed_transition_kinds",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleTransitionDecisionEvidenceV018:
    evidence_id: str
    transition_decision_id: str
    transition_decision_maker_id: str
    transition_decision_maker_organization_id: str
    decision_maker_mandate_receipt_digest: str
    decision_maker_mandate_verified: bool
    decision_maker_qualification_receipt_digest: str
    decision_maker_qualification_verified: bool
    decision_maker_identity_confirmation_digest: str
    decision_maker_identity_confirmed: bool
    conflict_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    jurisdiction_receipt_digest: str
    jurisdiction_verified: bool
    decision_readiness_receipt_digest: str
    decision_ready: bool
    source_transition_review_id: str
    source_transition_review_record_digest: str
    source_artifact_digests: dict[str, str]
    source_transition_reviewer_id: str
    source_transition_reviewer_organization_id: str
    source_post_operation_reviewer_id: str
    source_completion_reviewer_id: str
    source_operator_id: str
    source_operation_approver_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    subject_id: str
    subject_kind: str
    subject_version: str
    requester_id: str
    transition_preparer_id: str
    proposed_transition_kind: str
    current_state: LifecycleStateV018
    target_state: LifecycleStateV018
    transition_rule: LifecycleTransitionRuleV018
    decision_rationale_digest: str
    decision_approved: bool
    denial_route_digest: str
    denial_route_available: bool
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
    decision_requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    decided_at_epoch_seconds: int
    decision_expiry_at_epoch_seconds: int
    transition_preparation_deadline_at_epoch_seconds: int
    evidence_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleTransitionDecisionSubmissionV018:
    transition_decision_id: str
    transition_decision_maker_id: str
    transition_decision_maker_organization_id: str
    objective: str
    decision_requested_at_epoch_seconds: int
    decided_at_epoch_seconds: int
    decision_expiry_at_epoch_seconds: int
    source_transition_review_id: str
    source_transition_review_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    transition_decision_evidence_digest: str
    requester_id: str
    source_transition_reviewer_id: str
    transition_preparer_id: str
    proposed_transition_kind: str
    expected_current_lifecycle_state_digest: str
    proposed_target_lifecycle_state_digest: str
    transition_preparation_deadline_at_epoch_seconds: int
    decision_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleTransitionDecisionArtifactV018:
    transition_decision_id: str
    status: str
    reason: str
    transition_decision_maker_id: str
    transition_decision_maker_organization_id: str
    source_transition_review_id: str
    source_transition_reviewer_id: str
    transition_preparer_id: str
    proposed_transition_kind: str
    subject_id: str
    requester_id: str
    expected_current_lifecycle_state_digest: str
    proposed_target_lifecycle_state_digest: str
    transition_rule_digest: str
    policy_digest: str
    decision_digest: str
    evidence_digest: str
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    source_transition_review_completed: bool
    transition_decision_record_issued: bool
    transition_decision_made: bool
    transition_approved_for_preparation: bool
    transition_denied: bool
    transition_preparation_required_next: bool
    transition_preparation_route_required_next: bool
    transition_appeal_or_reconsideration_available: bool
    lifecycle_transition_prepared: bool
    lifecycle_transition_approved: bool
    lifecycle_transition_started: bool
    lifecycle_transition_completed: bool
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


def lifecycle_state_digest(value: LifecycleStateV018) -> str:
    return _digest_without(value, "state_digest")


def transition_rule_digest(value: LifecycleTransitionRuleV018) -> str:
    return _digest_without(value, "rule_digest")


def policy_digest(value: LifecycleTransitionDecisionPolicyV018) -> str:
    return _digest_without(value, "policy_digest")


def evidence_digest(value: LifecycleTransitionDecisionEvidenceV018) -> str:
    return _digest_without(value, "evidence_digest")


def submission_digest(value: LifecycleTransitionDecisionSubmissionV018) -> str:
    return _digest_without(value, "decision_digest")


def record_digest(value: LifecycleTransitionDecisionArtifactV018) -> str:
    return _digest_without(value, "record_digest")
