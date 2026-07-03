#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_lifecycle_bounded_operation_completion_v0_15"
COMPLETED = (
    "LIFECYCLE_BOUNDED_OPERATION_COMPLETION_"
    "COMPLETED_FOR_SEPARATE_POST_OPERATION_REVIEW"
)
DENIED = "LIFECYCLE_BOUNDED_OPERATION_COMPLETION_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_OPERATION_COMPLETION_REJECTED"
OBJECTIVE = "COMPLETE_STARTED_BOUNDED_LIFECYCLE_OPERATION_ONLY"


@dataclass(frozen=True)
class LifecycleOperationCompletionPolicyV015:
    policy_id: str
    allowed_completion_reviewer_ids: tuple[str, ...]
    allowed_completion_reviewer_organization_ids: tuple[str, ...]
    allowed_target_resource_ids: tuple[str, ...]
    max_completion_delay_seconds: int
    max_evidence_age_seconds: int
    max_scope_items: int
    require_complete_source_recomputation: bool
    require_started_source_operation: bool
    require_exact_source_artifact_binding: bool
    require_exact_completion_reviewer_binding: bool
    require_exact_route_binding: bool
    require_completion_reviewer_operator_separation: bool
    require_completion_reviewer_prior_actor_separation: bool
    require_completion_reviewer_mandate: bool
    require_completion_reviewer_qualification: bool
    require_completion_reviewer_identity_confirmation: bool
    require_conflict_disclosure: bool
    require_jurisdiction: bool
    require_completion_readiness: bool
    require_operation_execution_finished: bool
    require_execution_result_integrity: bool
    require_all_scope_items_accounted: bool
    require_all_reversible_steps_accounted: bool
    require_no_irreversible_steps: bool
    require_target_post_state_evidence: bool
    require_protected_resource_integrity: bool
    require_protected_core_integrity: bool
    require_resource_reservation_release: bool
    require_monitoring_completion: bool
    require_evidence_capture_completion: bool
    require_no_unresolved_stop_condition: bool
    require_abort_not_triggered: bool
    require_no_pending_rollback: bool
    require_no_pending_recovery: bool
    operation_completion_artifact_only: bool
    lifecycle_state_read_only: bool
    repository_read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "allowed_completion_reviewer_ids",
            "allowed_completion_reviewer_organization_ids",
            "allowed_target_resource_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecycleOperationCompletionEvidenceV015:
    evidence_id: str
    operation_completion_id: str
    completion_reviewer_id: str
    completion_reviewer_organization_id: str
    completion_reviewer_mandate_receipt_digest: str
    completion_reviewer_mandate_verified: bool
    completion_reviewer_qualification_receipt_digest: str
    completion_reviewer_qualification_verified: bool
    completion_reviewer_identity_confirmation_digest: str
    completion_reviewer_identity_confirmed: bool
    conflict_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    jurisdiction_receipt_digest: str
    jurisdiction_verified: bool
    completion_readiness_receipt_digest: str
    completion_ready: bool
    source_operation_start_id: str
    source_operation_start_record_digest: str
    source_artifact_digests: dict[str, str]
    source_operator_id: str
    source_operator_organization_id: str
    source_operation_approver_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    subject_id: str
    subject_kind: str
    subject_version: str
    requester_id: str
    operation_completion_route_digest: str
    approved_scope_digest: str
    operation_scope_items: tuple[str, ...]
    target_resource_ids: tuple[str, ...]
    protected_resource_ids: tuple[str, ...]
    reversible_step_ids: tuple[str, ...]
    irreversible_step_ids: tuple[str, ...]
    operation_execution_result_digest: str
    operation_execution_finished: bool
    step_result_digests: dict[str, str]
    execution_result_integrity_verified: bool
    all_scope_items_accounted: bool
    all_reversible_steps_accounted: bool
    target_resource_post_state_digest: str
    target_post_state_verified: bool
    protected_resource_integrity_digest: str
    protected_resources_intact: bool
    protected_core_integrity_digest: str
    protected_core_intact: bool
    resource_reservation_release_digest: str
    resource_reservations_released: bool
    monitoring_completion_digest: str
    monitoring_completed: bool
    evidence_capture_completion_digest: str
    evidence_capture_completed: bool
    unresolved_stop_condition_present: bool
    abort_triggered: bool
    rollback_pending: bool
    recovery_pending: bool
    external_operation_performed: bool
    repository_changed: bool
    completion_requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    operation_completion_deadline_at_epoch_seconds: int
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
class LifecycleOperationCompletionSubmissionV015:
    operation_completion_id: str
    completion_reviewer_id: str
    completion_reviewer_organization_id: str
    objective: str
    completion_requested_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    source_operation_start_id: str
    source_operation_start_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    completion_evidence_digest: str
    requester_id: str
    source_operator_id: str
    source_operation_approver_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    operation_completion_route_digest: str
    completion_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleOperationCompletionArtifactV015:
    operation_completion_id: str
    status: str
    reason: str
    completion_reviewer_id: str
    completion_reviewer_organization_id: str
    source_operation_start_id: str
    source_operator_id: str
    source_operation_approver_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    subject_id: str
    requester_id: str
    policy_digest: str
    completion_digest: str
    evidence_digest: str
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    operation_started: bool
    operation_completion_record_issued: bool
    operation_completion_decision_made: bool
    operation_completed: bool
    operation_completion_denied: bool
    post_operation_review_required_next: bool
    post_operation_review_route_required_next: bool
    operation_recovery_required_next: bool
    operation_recovery_route_required_next: bool
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


def policy_digest(value: LifecycleOperationCompletionPolicyV015) -> str:
    return _digest_without(value, "policy_digest")


def evidence_digest(value: LifecycleOperationCompletionEvidenceV015) -> str:
    return _digest_without(value, "evidence_digest")


def submission_digest(value: LifecycleOperationCompletionSubmissionV015) -> str:
    return _digest_without(value, "completion_digest")


def record_digest(value: LifecycleOperationCompletionArtifactV015) -> str:
    return _digest_without(value, "record_digest")
