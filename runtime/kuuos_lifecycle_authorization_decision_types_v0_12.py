#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_lifecycle_bounded_authorization_decision_v0_12"
APPROVED = "LIFECYCLE_BOUNDED_AUTHORIZATION_DECISION_APPROVED"
DENIED = "LIFECYCLE_BOUNDED_AUTHORIZATION_DECISION_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_AUTHORIZATION_DECISION_REJECTED"
OBJECTIVE = "AUTHORIZE_BOUNDED_LIFECYCLE_OPERATION_WITHOUT_STARTING_IT"


@dataclass(frozen=True)
class LifecycleAuthorizationDecisionPolicyV012:
    policy_id: str
    allowed_authorization_decision_maker_ids: tuple[str, ...]
    allowed_authorization_decision_maker_organization_ids: tuple[str, ...]
    allowed_future_operator_ids: tuple[str, ...]
    allowed_target_resource_ids: tuple[str, ...]
    max_decision_delay_seconds: int
    max_evidence_age_seconds: int
    max_approval_expiry_seconds: int
    max_operation_window_seconds: int
    max_scope_items: int
    require_complete_source_recomputation: bool
    require_clear_source_review: bool
    require_authority_mandate: bool
    require_authority_qualification: bool
    require_authority_independence: bool
    require_conflict_disclosure: bool
    require_jurisdiction: bool
    require_quorum: bool
    require_reasoned_decision: bool
    require_proportionality: bool
    require_less_restrictive_alternatives: bool
    require_irreversibility_review: bool
    require_human_impact_review: bool
    require_exact_scope_binding: bool
    require_package_safety: bool
    require_appeal_route: bool
    require_dissent_route: bool
    require_minority_opinion_record: bool
    require_role_separation: bool
    authorization_decision_enabled: bool
    operation_approval_enabled: bool
    operation_start_enabled: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "allowed_authorization_decision_maker_ids",
            "allowed_authorization_decision_maker_organization_ids",
            "allowed_future_operator_ids",
            "allowed_target_resource_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleAuthorizationDecisionEvidenceV012:
    evidence_id: str
    authorization_decision_id: str
    authorization_decision_maker_id: str
    authorization_decision_maker_organization_id: str
    authority_mandate_receipt_digest: str
    authority_mandate_verified: bool
    authority_qualification_receipt_digest: str
    authority_qualification_verified: bool
    authority_independence_declaration_digest: str
    authority_independence_declared: bool
    conflict_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    jurisdiction_receipt_digest: str
    jurisdiction_verified: bool
    quorum_receipt_digest: str
    quorum_verified: bool
    decision_rationale_digest: str
    decision_rationale_complete: bool
    proportionality_review_digest: str
    proportionality_satisfied: bool
    less_restrictive_alternatives_digest: str
    less_restrictive_alternatives_exhausted: bool
    irreversibility_review_digest: str
    irreversibility_review_complete: bool
    human_impact_review_digest: str
    human_impact_review_complete: bool
    subject_id: str
    subject_kind: str
    subject_version: str
    source_decision_review_id: str
    source_decision_review_record_digest: str
    source_artifact_digests: dict[str, str]
    decision_reviewer_id: str
    requester_id: str
    future_operator_id: str
    authorized_scope_digest: str
    operation_scope_items: tuple[str, ...]
    target_resource_ids: tuple[str, ...]
    protected_resource_ids: tuple[str, ...]
    reversible_step_ids: tuple[str, ...]
    irreversible_step_ids: tuple[str, ...]
    rollback_plan_digest: str
    rollback_plan_verified: bool
    recovery_route_digest: str
    recovery_route_verified: bool
    stop_condition_digest: str
    stop_conditions_complete: bool
    abort_channel_digest: str
    abort_channel_available: bool
    human_oversight_digest: str
    human_oversight_available: bool
    monitoring_plan_digest: str
    monitoring_plan_complete: bool
    evidence_capture_plan_digest: str
    evidence_capture_plan_complete: bool
    simulation_receipt_digest: str
    simulation_verified: bool
    operation_window_seconds: int
    decision_requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    approval_expiry_at_epoch_seconds: int
    protected_core_excluded: bool
    institutional_hold_active: bool
    emergency_state_active: bool
    appeal_route_digest: str
    appeal_route_available: bool
    dissent_route_digest: str
    dissent_route_available: bool
    minority_opinion_digest: str
    minority_opinion_recorded: bool
    evidence_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "operation_scope_items",
            "target_resource_ids",
            "protected_resource_ids",
            "reversible_step_ids",
            "irreversible_step_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleAuthorizationDecisionSubmissionV012:
    authorization_decision_id: str
    authorization_decision_maker_id: str
    authorization_decision_maker_organization_id: str
    objective: str
    decision_requested_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    source_decision_review_id: str
    source_decision_review_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    authorization_evidence_digest: str
    decision_reviewer_id: str
    requester_id: str
    future_operator_id: str
    approval_expiry_at_epoch_seconds: int
    decision_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleAuthorizationDecisionArtifactV012:
    authorization_decision_id: str
    status: str
    reason: str
    authorization_decision_maker_id: str
    authorization_decision_maker_organization_id: str
    subject_id: str
    source_decision_review_id: str
    decision_reviewer_id: str
    requester_id: str
    future_operator_id: str
    policy_digest: str
    decision_digest: str
    evidence_digest: str
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    decision_record_issued: bool
    authorization_decision_made: bool
    operation_approved: bool
    operation_start_required_next: bool
    operation_started: bool
    operation_completed: bool
    authority_changed: bool
    quiescence_state_changed: bool
    terminal_state_changed: bool
    terminal_marker_written: bool
    resource_removed: bool
    external_operation_performed: bool
    repository_changed: bool
    governance_decision_only: bool
    record_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _digest_without(value: Any, field_name: str) -> str:
    payload = value.to_dict()
    payload.pop(field_name, None)
    return canonical_digest(payload)


def policy_digest(value: LifecycleAuthorizationDecisionPolicyV012) -> str:
    return _digest_without(value, "policy_digest")


def evidence_digest(value: LifecycleAuthorizationDecisionEvidenceV012) -> str:
    return _digest_without(value, "evidence_digest")


def submission_digest(value: LifecycleAuthorizationDecisionSubmissionV012) -> str:
    return _digest_without(value, "decision_digest")


def record_digest(value: LifecycleAuthorizationDecisionArtifactV012) -> str:
    return _digest_without(value, "record_digest")
