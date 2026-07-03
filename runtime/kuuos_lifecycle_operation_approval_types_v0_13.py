#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_lifecycle_bounded_operation_approval_v0_13"
APPROVED = (
    "LIFECYCLE_BOUNDED_OPERATION_APPROVAL_"
    "APPROVED_FOR_SEPARATE_OPERATION_START"
)
DENIED = "LIFECYCLE_BOUNDED_OPERATION_APPROVAL_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_OPERATION_APPROVAL_REJECTED"
OBJECTIVE = "APPROVE_BOUNDED_LIFECYCLE_OPERATION_ONLY"


@dataclass(frozen=True)
class LifecycleOperationApprovalPolicyV013:
    policy_id: str
    allowed_operation_approver_ids: tuple[str, ...]
    allowed_operation_approver_organization_ids: tuple[str, ...]
    allowed_future_operator_ids: tuple[str, ...]
    allowed_target_resource_ids: tuple[str, ...]
    max_approval_delay_seconds: int
    max_evidence_age_seconds: int
    max_approval_expiry_seconds: int
    max_operation_start_delay_seconds: int
    max_operation_window_seconds: int
    max_scope_items: int
    require_complete_source_recomputation: bool
    require_approved_source_authorization: bool
    require_exact_route_binding: bool
    require_operation_approver_mandate: bool
    require_operation_approver_qualification: bool
    require_operation_approver_independence: bool
    require_conflict_disclosure: bool
    require_jurisdiction: bool
    require_quorum: bool
    require_reasoned_approval: bool
    require_proportionality_review: bool
    require_operator_acknowledgement: bool
    require_execution_package_integrity: bool
    require_resource_reservation: bool
    require_exact_scope_binding: bool
    require_rollback_readiness: bool
    require_recovery_readiness: bool
    require_stop_conditions: bool
    require_abort_channel: bool
    require_human_oversight: bool
    require_monitoring: bool
    require_evidence_capture: bool
    require_simulation: bool
    require_no_irreversible_steps: bool
    require_protected_core_exclusion: bool
    require_role_separation: bool
    operation_approval_artifact_only: bool
    lifecycle_read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "allowed_operation_approver_ids",
            "allowed_operation_approver_organization_ids",
            "allowed_future_operator_ids",
            "allowed_target_resource_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleOperationApprovalEvidenceV013:
    evidence_id: str
    operation_approval_id: str
    operation_approver_id: str
    operation_approver_organization_id: str
    approver_mandate_receipt_digest: str
    approver_mandate_verified: bool
    approver_qualification_receipt_digest: str
    approver_qualification_verified: bool
    approver_independence_declaration_digest: str
    approver_independence_declared: bool
    conflict_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    jurisdiction_receipt_digest: str
    jurisdiction_verified: bool
    quorum_receipt_digest: str
    quorum_satisfied: bool
    approval_rationale_digest: str
    reasoned_approval_complete: bool
    proportionality_review_digest: str
    proportionality_satisfied: bool
    source_authorization_decision_id: str
    source_authorization_record_digest: str
    source_artifact_digests: dict[str, str]
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    subject_id: str
    subject_kind: str
    subject_version: str
    requester_id: str
    future_operator_id: str
    operation_approval_route_digest: str
    approved_scope_digest: str
    operation_scope_items: tuple[str, ...]
    target_resource_ids: tuple[str, ...]
    protected_resource_ids: tuple[str, ...]
    reversible_step_ids: tuple[str, ...]
    irreversible_step_ids: tuple[str, ...]
    execution_package_digest: str
    execution_package_integrity_verified: bool
    operator_acknowledgement_digest: str
    operator_acknowledged: bool
    resource_reservation_digest: str
    resources_reserved: bool
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
    approval_requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    operation_approval_expiry_at_epoch_seconds: int
    operation_start_window_open_at_epoch_seconds: int
    operation_start_deadline_at_epoch_seconds: int
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
class LifecycleOperationApprovalSubmissionV013:
    operation_approval_id: str
    operation_approver_id: str
    operation_approver_organization_id: str
    objective: str
    approval_requested_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    source_authorization_decision_id: str
    source_authorization_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    approval_evidence_digest: str
    requester_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    future_operator_id: str
    operation_approval_route_digest: str
    operation_start_deadline_at_epoch_seconds: int
    approval_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleOperationApprovalArtifactV013:
    operation_approval_id: str
    status: str
    reason: str
    operation_approver_id: str
    operation_approver_organization_id: str
    source_authorization_decision_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    subject_id: str
    requester_id: str
    future_operator_id: str
    policy_digest: str
    approval_digest: str
    evidence_digest: str
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    operation_approval_record_issued: bool
    operation_approval_made: bool
    operation_approved: bool
    operation_denied: bool
    operation_start_required_next: bool
    operation_start_route_required_next: bool
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


def policy_digest(value: LifecycleOperationApprovalPolicyV013) -> str:
    return _digest_without(value, "policy_digest")


def evidence_digest(value: LifecycleOperationApprovalEvidenceV013) -> str:
    return _digest_without(value, "evidence_digest")


def submission_digest(value: LifecycleOperationApprovalSubmissionV013) -> str:
    return _digest_without(value, "approval_digest")


def record_digest(value: LifecycleOperationApprovalArtifactV013) -> str:
    return _digest_without(value, "record_digest")
