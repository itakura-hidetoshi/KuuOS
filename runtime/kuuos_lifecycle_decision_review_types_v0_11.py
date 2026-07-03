#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_lifecycle_bounded_decision_review_v0_11"
CLEAR = "LIFECYCLE_BOUNDED_DECISION_REVIEW_CLEAR_FOR_AUTHORIZATION_DECISION"
BLOCKED = "LIFECYCLE_BOUNDED_DECISION_REVIEW_BLOCKED"
REJECTED = "LIFECYCLE_BOUNDED_DECISION_REVIEW_REJECTED"
OBJECTIVE = "REVIEW_BOUNDED_LIFECYCLE_REQUEST_FOR_SEPARATE_AUTHORIZATION_DECISION_ONLY"


@dataclass(frozen=True)
class LifecycleDecisionReviewPolicyV011:
    policy_id: str
    allowed_decision_reviewer_ids: tuple[str, ...]
    allowed_decision_reviewer_organization_ids: tuple[str, ...]
    allowed_authorization_decision_maker_ids: tuple[str, ...]
    allowed_target_resource_ids: tuple[str, ...]
    max_review_delay_seconds: int
    max_evidence_age_seconds: int
    max_review_expiry_seconds: int
    max_operation_window_seconds: int
    max_scope_items: int
    require_complete_source_recomputation: bool
    require_issued_source_request: bool
    require_reviewer_qualification: bool
    require_reviewer_independence: bool
    require_conflict_disclosure: bool
    require_exact_scope_binding: bool
    require_package_safety: bool
    require_authorization_route: bool
    require_appeal_route: bool
    require_dissent_route: bool
    require_minority_opinion_record: bool
    require_role_separation: bool
    review_artifact_only: bool
    lifecycle_read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "allowed_decision_reviewer_ids",
            "allowed_decision_reviewer_organization_ids",
            "allowed_authorization_decision_maker_ids",
            "allowed_target_resource_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleDecisionReviewEvidenceV011:
    evidence_id: str
    decision_review_id: str
    decision_reviewer_id: str
    decision_reviewer_organization_id: str
    reviewer_qualification_receipt_digest: str
    reviewer_qualification_verified: bool
    reviewer_independence_declaration_digest: str
    reviewer_independence_declared: bool
    conflict_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    subject_id: str
    subject_kind: str
    subject_version: str
    source_bounded_request_id: str
    source_bounded_request_record_digest: str
    source_artifact_digests: dict[str, str]
    requester_id: str
    authorization_decision_maker_id: str
    future_operator_id: str
    reviewed_scope_digest: str
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
    review_requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    review_expiry_at_epoch_seconds: int
    authorization_decision_deadline_at_epoch_seconds: int
    authorization_route_digest: str
    authorization_route_available: bool
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
class LifecycleDecisionReviewSubmissionV011:
    decision_review_id: str
    decision_reviewer_id: str
    decision_reviewer_organization_id: str
    objective: str
    review_requested_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    source_bounded_request_id: str
    source_bounded_request_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    review_evidence_digest: str
    requester_id: str
    authorization_decision_maker_id: str
    future_operator_id: str
    authorization_route_digest: str
    authorization_decision_deadline_at_epoch_seconds: int
    review_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleDecisionReviewArtifactV011:
    decision_review_id: str
    status: str
    reason: str
    decision_reviewer_id: str
    decision_reviewer_organization_id: str
    subject_id: str
    source_bounded_request_id: str
    requester_id: str
    authorization_decision_maker_id: str
    future_operator_id: str
    policy_digest: str
    review_digest: str
    evidence_digest: str
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    review_record_issued: bool
    review_completed: bool
    clear_for_authorization_decision: bool
    authorization_decision_required_next: bool
    authorization_decision_made: bool
    operation_approved: bool
    operation_started: bool
    operation_completed: bool
    authority_changed: bool
    quiescence_state_changed: bool
    terminal_state_changed: bool
    terminal_marker_written: bool
    resource_removed: bool
    external_operation_performed: bool
    repository_changed: bool
    lifecycle_read_only: bool
    record_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _digest_without(value: Any, field_name: str) -> str:
    payload = value.to_dict()
    payload.pop(field_name, None)
    return canonical_digest(payload)


def policy_digest(value: LifecycleDecisionReviewPolicyV011) -> str:
    return _digest_without(value, "policy_digest")


def evidence_digest(value: LifecycleDecisionReviewEvidenceV011) -> str:
    return _digest_without(value, "evidence_digest")


def submission_digest(value: LifecycleDecisionReviewSubmissionV011) -> str:
    return _digest_without(value, "review_digest")


def record_digest(value: LifecycleDecisionReviewArtifactV011) -> str:
    return _digest_without(value, "record_digest")
