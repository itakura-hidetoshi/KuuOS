#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_lifecycle_bounded_operation_start_v0_14"
STARTED = (
    "LIFECYCLE_BOUNDED_OPERATION_START_"
    "STARTED_FOR_SEPARATE_OPERATION_COMPLETION"
)
DENIED = "LIFECYCLE_BOUNDED_OPERATION_START_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_OPERATION_START_REJECTED"
OBJECTIVE = "START_APPROVED_BOUNDED_LIFECYCLE_OPERATION_ONLY"


@dataclass(frozen=True)
class LifecycleOperationStartPolicyV014:
    policy_id: str
    allowed_operator_ids: tuple[str, ...]
    allowed_operator_organization_ids: tuple[str, ...]
    allowed_target_resource_ids: tuple[str, ...]
    max_start_delay_seconds: int
    max_evidence_age_seconds: int
    max_operation_window_seconds: int
    max_scope_items: int
    require_complete_source_recomputation: bool
    require_approved_source_operation_approval: bool
    require_exact_source_artifact_binding: bool
    require_exact_operator_binding: bool
    require_exact_route_binding: bool
    require_operator_approver_separation: bool
    require_operator_mandate: bool
    require_operator_qualification: bool
    require_operator_identity_confirmation: bool
    require_conflict_disclosure: bool
    require_jurisdiction: bool
    require_operator_readiness: bool
    require_start_authorization_acknowledgement: bool
    require_execution_package_reconfirmation: bool
    require_resource_reservation_reconfirmation: bool
    require_exact_scope_binding: bool
    require_rollback_reconfirmation: bool
    require_recovery_reconfirmation: bool
    require_stop_condition_reconfirmation: bool
    require_abort_channel_reconfirmation: bool
    require_human_oversight_reconfirmation: bool
    require_monitoring_reconfirmation: bool
    require_evidence_capture_reconfirmation: bool
    require_no_irreversible_steps: bool
    require_protected_core_exclusion: bool
    operation_start_artifact_only: bool
    lifecycle_state_read_only: bool
    repository_read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "allowed_operator_ids",
            "allowed_operator_organization_ids",
            "allowed_target_resource_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleOperationStartEvidenceV014:
    evidence_id: str
    operation_start_id: str
    operator_id: str
    operator_organization_id: str
    operator_mandate_receipt_digest: str
    operator_mandate_verified: bool
    operator_qualification_receipt_digest: str
    operator_qualification_verified: bool
    operator_identity_confirmation_digest: str
    operator_identity_confirmed: bool
    conflict_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    jurisdiction_receipt_digest: str
    jurisdiction_verified: bool
    operator_readiness_receipt_digest: str
    operator_ready: bool
    start_authorization_acknowledgement_digest: str
    start_authorization_acknowledged: bool
    source_operation_approval_id: str
    source_operation_approval_record_digest: str
    source_artifact_digests: dict[str, str]
    source_operation_approver_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    subject_id: str
    subject_kind: str
    subject_version: str
    requester_id: str
    approved_future_operator_id: str
    operation_start_route_digest: str
    approved_scope_digest: str
    operation_scope_items: tuple[str, ...]
    target_resource_ids: tuple[str, ...]
    protected_resource_ids: tuple[str, ...]
    reversible_step_ids: tuple[str, ...]
    irreversible_step_ids: tuple[str, ...]
    execution_package_digest: str
    execution_package_recheck_digest: str
    execution_package_integrity_reconfirmed: bool
    resource_reservation_digest: str
    resource_reservation_recheck_digest: str
    resources_reserved_reconfirmed: bool
    rollback_plan_digest: str
    rollback_recheck_digest: str
    rollback_readiness_reconfirmed: bool
    recovery_route_digest: str
    recovery_recheck_digest: str
    recovery_readiness_reconfirmed: bool
    stop_condition_digest: str
    stop_condition_recheck_digest: str
    stop_conditions_reconfirmed: bool
    abort_channel_digest: str
    abort_channel_recheck_digest: str
    abort_channel_reconfirmed: bool
    human_oversight_digest: str
    human_oversight_recheck_digest: str
    human_oversight_reconfirmed: bool
    monitoring_plan_digest: str
    monitoring_recheck_digest: str
    monitoring_reconfirmed: bool
    evidence_capture_plan_digest: str
    evidence_capture_recheck_digest: str
    evidence_capture_reconfirmed: bool
    operation_window_seconds: int
    start_requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    started_at_epoch_seconds: int
    operation_start_deadline_at_epoch_seconds: int
    operation_completion_deadline_at_epoch_seconds: int
    protected_core_excluded: bool
    protected_core_exclusion_reconfirmed: bool
    institutional_hold_active: bool
    institutional_hold_absence_reconfirmed: bool
    emergency_state_active: bool
    emergency_state_absence_reconfirmed: bool
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
class LifecycleOperationStartSubmissionV014:
    operation_start_id: str
    operator_id: str
    operator_organization_id: str
    objective: str
    start_requested_at_epoch_seconds: int
    started_at_epoch_seconds: int
    source_operation_approval_id: str
    source_operation_approval_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    start_evidence_digest: str
    requester_id: str
    source_operation_approver_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    approved_future_operator_id: str
    operation_start_route_digest: str
    operation_completion_deadline_at_epoch_seconds: int
    start_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleOperationStartArtifactV014:
    operation_start_id: str
    status: str
    reason: str
    operator_id: str
    operator_organization_id: str
    source_operation_approval_id: str
    source_operation_approver_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    subject_id: str
    requester_id: str
    approved_future_operator_id: str
    policy_digest: str
    start_digest: str
    evidence_digest: str
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    operation_start_record_issued: bool
    operation_start_decision_made: bool
    operation_started: bool
    operation_start_denied: bool
    operation_completion_required_next: bool
    operation_completion_route_required_next: bool
    operation_completed: bool
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


def policy_digest(value: LifecycleOperationStartPolicyV014) -> str:
    return _digest_without(value, "policy_digest")


def evidence_digest(value: LifecycleOperationStartEvidenceV014) -> str:
    return _digest_without(value, "evidence_digest")


def submission_digest(value: LifecycleOperationStartSubmissionV014) -> str:
    return _digest_without(value, "start_digest")


def record_digest(value: LifecycleOperationStartArtifactV014) -> str:
    return _digest_without(value, "record_digest")
