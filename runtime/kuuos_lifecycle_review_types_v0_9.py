#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_apoptosis_execution_review_v0_9"
CLEAR = "APOPTOSIS_EXECUTION_REVIEW_CLEAR_FOR_EXECUTION_REQUEST"
BLOCKED = "APOPTOSIS_EXECUTION_REVIEW_BLOCKED"
REJECTED = "APOPTOSIS_EXECUTION_REVIEW_REJECTED"
OBJECTIVE = "REVIEW_BOUNDED_EXECUTION_PACKAGE_ONLY"


@dataclass(frozen=True)
class LifecycleReviewPolicyV09:
    policy_id: str
    allowed_reviewer_ids: tuple[str, ...]
    allowed_reviewer_organization_ids: tuple[str, ...]
    allowed_target_resource_ids: tuple[str, ...]
    max_review_delay_seconds: int
    max_evidence_age_seconds: int
    max_review_expiry_seconds: int
    max_execution_window_seconds: int
    max_scope_items: int
    require_complete_source_recomputation: bool
    require_ready_source: bool
    require_qualification: bool
    require_independence: bool
    require_conflict_disclosure: bool
    require_package_safety: bool
    require_appeal_route: bool
    require_dissent_route: bool
    require_operator_separation: bool
    read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "allowed_reviewer_ids",
            "allowed_reviewer_organization_ids",
            "allowed_target_resource_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleReviewEvidenceV09:
    evidence_id: str
    review_id: str
    reviewer_id: str
    reviewer_organization_id: str
    future_execution_authority_id: str
    future_execution_operator_id: str
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
    source_preparation_id: str
    source_preparation_record_digest: str
    source_artifact_digests: dict[str, str]
    execution_scope_digest: str
    execution_scope_items: tuple[str, ...]
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
    execution_window_seconds: int
    review_requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    review_expiry_at_epoch_seconds: int
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
            "execution_scope_items",
            "target_resource_ids",
            "protected_resource_ids",
            "reversible_step_ids",
            "irreversible_step_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleReviewRequestV09:
    review_id: str
    reviewer_id: str
    reviewer_organization_id: str
    objective: str
    review_requested_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    source_preparation_id: str
    source_preparation_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    review_evidence_digest: str
    future_execution_authority_id: str
    future_execution_operator_id: str
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleReviewArtifactV09:
    review_id: str
    status: str
    reason: str
    reviewer_id: str
    reviewer_organization_id: str
    subject_id: str
    source_preparation_id: str
    future_execution_authority_id: str
    future_execution_operator_id: str
    policy_digest: str
    request_digest: str
    evidence_digest: str
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    review_record_issued: bool
    review_completed: bool
    clear_for_next_request_layer: bool
    next_request_layer_required: bool
    effect_free: bool
    read_only: bool
    record_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _digest_without(value: Any, field_name: str) -> str:
    payload = value.to_dict()
    payload.pop(field_name, None)
    return canonical_digest(payload)


def lifecycle_review_policy_digest(value: LifecycleReviewPolicyV09) -> str:
    return _digest_without(value, "policy_digest")


def lifecycle_review_evidence_digest(value: LifecycleReviewEvidenceV09) -> str:
    return _digest_without(value, "evidence_digest")


def lifecycle_review_request_digest(value: LifecycleReviewRequestV09) -> str:
    return _digest_without(value, "request_digest")


def lifecycle_review_record_digest(value: LifecycleReviewArtifactV09) -> str:
    return _digest_without(value, "record_digest")


ApoptosisExecutionReviewPolicy = LifecycleReviewPolicyV09
ApoptosisExecutionReviewEvidence = LifecycleReviewEvidenceV09
ApoptosisExecutionReviewRequest = LifecycleReviewRequestV09
ApoptosisExecutionReviewRecord = LifecycleReviewArtifactV09
EXECUTION_REVIEW_CLEAR = CLEAR
EXECUTION_REVIEW_BLOCKED = BLOCKED
EXECUTION_REVIEW_REJECTED = REJECTED
OBJECTIVE_REVIEW_BOUNDED_EXECUTION_PACKAGE_ONLY = OBJECTIVE
apoptosis_execution_review_policy_digest = lifecycle_review_policy_digest
apoptosis_execution_review_evidence_digest = lifecycle_review_evidence_digest
apoptosis_execution_review_request_digest = lifecycle_review_request_digest
apoptosis_execution_review_record_digest = lifecycle_review_record_digest
