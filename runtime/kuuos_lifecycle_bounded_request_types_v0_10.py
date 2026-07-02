#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_lifecycle_bounded_request_v0_10"
ISSUED = "LIFECYCLE_BOUNDED_REQUEST_ISSUED_FOR_DECISION_REVIEW"
BLOCKED = "LIFECYCLE_BOUNDED_REQUEST_BLOCKED"
REJECTED = "LIFECYCLE_BOUNDED_REQUEST_REJECTED"
OBJECTIVE = "ISSUE_BOUNDED_LIFECYCLE_REQUEST_FOR_DECISION_REVIEW_ONLY"


@dataclass(frozen=True)
class LifecycleBoundedRequestPolicyV010:
    policy_id: str
    allowed_requester_ids: tuple[str, ...]
    allowed_requester_organization_ids: tuple[str, ...]
    allowed_decision_authority_ids: tuple[str, ...]
    allowed_target_resource_ids: tuple[str, ...]
    max_request_delay_seconds: int
    max_evidence_age_seconds: int
    max_request_expiry_seconds: int
    max_operation_window_seconds: int
    max_scope_items: int
    require_complete_source_recomputation: bool
    require_clear_source_review: bool
    require_requester_qualification: bool
    require_requester_independence: bool
    require_conflict_disclosure: bool
    require_exact_scope_binding: bool
    require_package_safety: bool
    require_decision_route: bool
    require_appeal_route: bool
    require_dissent_route: bool
    require_authority_operator_separation: bool
    request_artifact_only: bool
    lifecycle_read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "allowed_requester_ids",
            "allowed_requester_organization_ids",
            "allowed_decision_authority_ids",
            "allowed_target_resource_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleBoundedRequestEvidenceV010:
    evidence_id: str
    bounded_request_id: str
    requester_id: str
    requester_organization_id: str
    decision_authority_id: str
    future_operator_id: str
    requester_qualification_receipt_digest: str
    requester_qualification_verified: bool
    requester_independence_declaration_digest: str
    requester_independence_declared: bool
    conflict_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    subject_id: str
    subject_kind: str
    subject_version: str
    source_review_id: str
    source_review_record_digest: str
    source_artifact_digests: dict[str, str]
    operation_scope_digest: str
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
    requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    request_expiry_at_epoch_seconds: int
    decision_deadline_at_epoch_seconds: int
    decision_route_digest: str
    decision_route_available: bool
    protected_core_excluded: bool
    institutional_hold_active: bool
    emergency_state_active: bool
    appeal_route_digest: str
    appeal_route_available: bool
    dissent_route_digest: str
    dissent_route_available: bool
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
class LifecycleBoundedRequestSubmissionV010:
    bounded_request_id: str
    requester_id: str
    requester_organization_id: str
    objective: str
    requested_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    source_review_id: str
    source_review_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    request_evidence_digest: str
    decision_authority_id: str
    future_operator_id: str
    decision_route_digest: str
    decision_deadline_at_epoch_seconds: int
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleBoundedRequestArtifactV010:
    bounded_request_id: str
    status: str
    reason: str
    requester_id: str
    requester_organization_id: str
    subject_id: str
    source_review_id: str
    decision_authority_id: str
    future_operator_id: str
    policy_digest: str
    request_digest: str
    evidence_digest: str
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    request_record_issued: bool
    bounded_request_issued: bool
    ready_for_decision_review: bool
    decision_review_required_next: bool
    decision_made: bool
    operation_started: bool
    operation_completed: bool
    lifecycle_effect_performed: bool
    repository_change_performed: bool
    lifecycle_read_only: bool
    record_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _digest_without(value: Any, field_name: str) -> str:
    payload = value.to_dict()
    payload.pop(field_name, None)
    return canonical_digest(payload)


def policy_digest(value: LifecycleBoundedRequestPolicyV010) -> str:
    return _digest_without(value, "policy_digest")


def evidence_digest(value: LifecycleBoundedRequestEvidenceV010) -> str:
    return _digest_without(value, "evidence_digest")


def submission_digest(value: LifecycleBoundedRequestSubmissionV010) -> str:
    return _digest_without(value, "request_digest")


def record_digest(value: LifecycleBoundedRequestArtifactV010) -> str:
    return _digest_without(value, "record_digest")
