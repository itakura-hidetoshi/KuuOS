#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_lifecycle_bounded_transition_preparation_v0_19"
PREPARED = "LIFECYCLE_BOUNDED_TRANSITION_PREPARATION_READY_FOR_SEPARATE_TRANSITION_APPROVAL"
BLOCKED = "LIFECYCLE_BOUNDED_TRANSITION_PREPARATION_BLOCKED"
REJECTED = "LIFECYCLE_BOUNDED_TRANSITION_PREPARATION_REJECTED"
OBJECTIVE = "PREPARE_APPROVED_LIFECYCLE_TRANSITION_PACKAGE_FOR_SEPARATE_APPROVAL_ONLY"


@dataclass(frozen=True)
class LifecycleTransitionStepV019:
    step_id: str
    sequence_number: int
    action_kind: str
    target_resource_id: str
    expected_pre_state_digest: str
    proposed_post_state_digest: str
    reversible: bool
    rollback_step_id: str
    evidence_capture_digest: str
    stop_condition_digest: str
    step_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleTransitionPackageV019:
    package_id: str
    source_transition_decision_id: str
    transition_kind: str
    expected_current_lifecycle_state_digest: str
    proposed_target_lifecycle_state_digest: str
    transition_rule_digest: str
    steps: tuple[LifecycleTransitionStepV019, ...]
    rollback_plan_digest: str
    recovery_plan_digest: str
    monitoring_plan_digest: str
    evidence_capture_plan_digest: str
    resource_reservation_digest: str
    authority_continuity_plan_digest: str
    irreversible_exception_digest: str
    aggregate_stop_conditions_digest: str
    execution_window_start_epoch_seconds: int
    execution_window_end_epoch_seconds: int
    package_digest: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["steps"] = [step.to_dict() for step in self.steps]
        return payload


@dataclass(frozen=True)
class LifecycleTransitionPreparationPolicyV019:
    policy_id: str
    allowed_transition_preparer_ids: tuple[str, ...]
    allowed_transition_preparer_organization_ids: tuple[str, ...]
    allowed_transition_approver_ids: tuple[str, ...]
    allowed_future_transition_operator_ids: tuple[str, ...]
    allowed_transition_kinds: tuple[str, ...]
    allowed_action_kinds: tuple[str, ...]
    allowed_target_resource_ids: tuple[str, ...]
    max_preparation_delay_seconds: int
    max_evidence_age_seconds: int
    max_package_expiry_seconds: int
    max_approval_delay_seconds: int
    max_execution_window_seconds: int
    max_steps: int
    require_complete_source_recomputation: bool
    require_approved_source_transition_decision: bool
    require_exact_source_artifact_binding: bool
    require_exact_state_and_rule_binding: bool
    require_ordered_bounded_steps: bool
    require_step_chain_continuity: bool
    require_rollback_plan: bool
    require_recovery_plan: bool
    require_monitoring_plan: bool
    require_evidence_capture_plan: bool
    require_resource_reservation: bool
    require_authority_continuity_plan: bool
    require_irreversible_exception_justification: bool
    require_stop_conditions: bool
    require_preparer_source_binding: bool
    require_preparer_prior_actor_separation: bool
    require_preparer_organization_separation: bool
    require_approver_role_separation: bool
    require_future_operator_role_separation: bool
    require_preparer_mandate: bool
    require_preparer_qualification: bool
    require_preparer_identity_confirmation: bool
    require_conflict_disclosure: bool
    require_jurisdiction: bool
    require_preparation_readiness: bool
    require_no_unresolved_anomaly: bool
    require_no_recovery_in_progress: bool
    require_no_institutional_hold: bool
    require_no_emergency_state: bool
    transition_preparation_artifact_only: bool
    lifecycle_state_read_only: bool
    repository_read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "allowed_transition_preparer_ids",
            "allowed_transition_preparer_organization_ids",
            "allowed_transition_approver_ids",
            "allowed_future_transition_operator_ids",
            "allowed_transition_kinds",
            "allowed_action_kinds",
            "allowed_target_resource_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleTransitionPreparationEvidenceV019:
    evidence_id: str
    transition_preparation_id: str
    transition_preparer_id: str
    transition_preparer_organization_id: str
    preparer_mandate_receipt_digest: str
    preparer_mandate_verified: bool
    preparer_qualification_receipt_digest: str
    preparer_qualification_verified: bool
    preparer_identity_confirmation_digest: str
    preparer_identity_confirmed: bool
    conflict_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    jurisdiction_receipt_digest: str
    jurisdiction_verified: bool
    preparation_readiness_receipt_digest: str
    preparation_ready: bool
    source_transition_decision_id: str
    source_transition_decision_record_digest: str
    source_artifact_digests: dict[str, str]
    source_transition_decision_maker_id: str
    source_transition_decision_maker_organization_id: str
    source_transition_reviewer_id: str
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
    transition_approver_id: str
    future_transition_operator_id: str
    transition_package: LifecycleTransitionPackageV019
    transition_approval_route_digest: str
    rollback_plan_complete: bool
    recovery_plan_complete: bool
    monitoring_plan_complete: bool
    evidence_capture_plan_complete: bool
    resource_reservations_valid: bool
    authority_continuity_planned: bool
    irreversible_steps_justified: bool
    all_steps_bounded: bool
    stop_conditions_complete: bool
    unresolved_anomaly_present: bool
    recovery_in_progress: bool
    institutional_hold_active: bool
    emergency_state_active: bool
    external_operation_performed: bool
    repository_changed: bool
    preparation_requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    prepared_at_epoch_seconds: int
    package_expiry_at_epoch_seconds: int
    transition_approval_deadline_at_epoch_seconds: int
    evidence_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleTransitionPreparationSubmissionV019:
    transition_preparation_id: str
    transition_preparer_id: str
    transition_preparer_organization_id: str
    objective: str
    preparation_requested_at_epoch_seconds: int
    prepared_at_epoch_seconds: int
    package_expiry_at_epoch_seconds: int
    source_transition_decision_id: str
    source_transition_decision_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    transition_preparation_evidence_digest: str
    requester_id: str
    source_transition_decision_maker_id: str
    transition_approver_id: str
    future_transition_operator_id: str
    transition_package_digest: str
    expected_current_lifecycle_state_digest: str
    proposed_target_lifecycle_state_digest: str
    transition_approval_route_digest: str
    transition_approval_deadline_at_epoch_seconds: int
    preparation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleTransitionPreparationArtifactV019:
    transition_preparation_id: str
    status: str
    reason: str
    transition_preparer_id: str
    transition_preparer_organization_id: str
    source_transition_decision_id: str
    source_transition_decision_maker_id: str
    transition_approver_id: str
    future_transition_operator_id: str
    transition_package_digest: str
    expected_current_lifecycle_state_digest: str
    proposed_target_lifecycle_state_digest: str
    transition_approval_route_digest: str
    subject_id: str
    requester_id: str
    policy_digest: str
    preparation_digest: str
    evidence_digest: str
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    source_transition_decision_approved: bool
    transition_preparation_record_issued: bool
    transition_preparation_completed: bool
    transition_package_prepared: bool
    ready_for_separate_transition_approval: bool
    transition_preparation_blocked: bool
    transition_approval_required_next: bool
    transition_approval_route_required_next: bool
    transition_repreparation_required_next: bool
    transition_repreparation_route_required_next: bool
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


def step_digest(value: LifecycleTransitionStepV019) -> str:
    return _digest_without(value, "step_digest")


def package_digest(value: LifecycleTransitionPackageV019) -> str:
    return _digest_without(value, "package_digest")


def policy_digest(value: LifecycleTransitionPreparationPolicyV019) -> str:
    return _digest_without(value, "policy_digest")


def evidence_digest(value: LifecycleTransitionPreparationEvidenceV019) -> str:
    return _digest_without(value, "evidence_digest")


def submission_digest(value: LifecycleTransitionPreparationSubmissionV019) -> str:
    return _digest_without(value, "preparation_digest")


def record_digest(value: LifecycleTransitionPreparationArtifactV019) -> str:
    return _digest_without(value, "record_digest")
