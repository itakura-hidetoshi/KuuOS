#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_lifecycle_bounded_post_operation_review_v0_16"
REVIEWED = (
    "LIFECYCLE_BOUNDED_POST_OPERATION_REVIEW_"
    "REVIEWED_FOR_SEPARATE_LIFECYCLE_TRANSITION_REVIEW"
)
DENIED = "LIFECYCLE_BOUNDED_POST_OPERATION_REVIEW_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_POST_OPERATION_REVIEW_REJECTED"
OBJECTIVE = "REVIEW_COMPLETED_BOUNDED_LIFECYCLE_OPERATION_OUTCOME_ONLY"


@dataclass(frozen=True)
class LifecyclePostOperationReviewPolicyV016:
    policy_id: str
    allowed_post_operation_reviewer_ids: tuple[str, ...]
    allowed_post_operation_reviewer_organization_ids: tuple[str, ...]
    allowed_target_resource_ids: tuple[str, ...]
    max_review_delay_seconds: int
    max_evidence_age_seconds: int
    max_scope_items: int
    require_complete_source_recomputation: bool
    require_completed_source_operation: bool
    require_exact_source_artifact_binding: bool
    require_exact_post_operation_reviewer_binding: bool
    require_exact_route_binding: bool
    require_post_operation_reviewer_completion_reviewer_separation: bool
    require_post_operation_reviewer_prior_actor_separation: bool
    require_post_operation_reviewer_organization_separation: bool
    require_post_operation_reviewer_mandate: bool
    require_post_operation_reviewer_qualification: bool
    require_post_operation_reviewer_identity_confirmation: bool
    require_conflict_disclosure: bool
    require_jurisdiction: bool
    require_review_readiness: bool
    require_intended_observed_result_comparison: bool
    require_target_post_state_review: bool
    require_collateral_effect_review: bool
    require_protected_resource_continuity: bool
    require_protected_core_continuity: bool
    require_monitoring_evidence_review: bool
    require_completion_evidence_review: bool
    require_no_unresolved_anomaly: bool
    require_no_rollback: bool
    require_no_recovery: bool
    post_operation_review_artifact_only: bool
    lifecycle_state_read_only: bool
    repository_read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for name in (
            "allowed_post_operation_reviewer_ids",
            "allowed_post_operation_reviewer_organization_ids",
            "allowed_target_resource_ids",
        ):
            payload[name] = list(getattr(self, name))
        return payload


@dataclass(frozen=True)
class LifecyclePostOperationReviewEvidenceV016:
    evidence_id: str
    post_operation_review_id: str
    post_operation_reviewer_id: str
    post_operation_reviewer_organization_id: str
    post_operation_reviewer_mandate_receipt_digest: str
    post_operation_reviewer_mandate_verified: bool
    post_operation_reviewer_qualification_receipt_digest: str
    post_operation_reviewer_qualification_verified: bool
    post_operation_reviewer_identity_confirmation_digest: str
    post_operation_reviewer_identity_confirmed: bool
    conflict_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    jurisdiction_receipt_digest: str
    jurisdiction_verified: bool
    review_readiness_receipt_digest: str
    review_ready: bool
    source_operation_completion_id: str
    source_operation_completion_record_digest: str
    source_artifact_digests: dict[str, str]
    source_completion_reviewer_id: str
    source_completion_reviewer_organization_id: str
    source_operator_id: str
    source_operation_approver_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    subject_id: str
    subject_kind: str
    subject_version: str
    requester_id: str
    post_operation_review_route_digest: str
    approved_scope_digest: str
    operation_scope_items: tuple[str, ...]
    target_resource_ids: tuple[str, ...]
    protected_resource_ids: tuple[str, ...]
    reversible_step_ids: tuple[str, ...]
    step_result_digests: dict[str, str]
    source_operation_execution_result_digest: str
    source_target_resource_post_state_digest: str
    intended_result_digest: str
    observed_result_digest: str
    intended_result_matches_observed: bool
    target_post_state_review_digest: str
    target_post_state_verified: bool
    collateral_effects_assessment_digest: str
    collateral_effects_absent: bool
    protected_resource_continuity_digest: str
    protected_resources_intact: bool
    protected_core_continuity_digest: str
    protected_core_intact: bool
    monitoring_evidence_review_digest: str
    monitoring_evidence_sufficient: bool
    completion_evidence_review_digest: str
    completion_evidence_sufficient: bool
    unresolved_anomaly_present: bool
    rollback_required: bool
    recovery_required: bool
    external_operation_performed: bool
    repository_changed: bool
    review_requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    reviewed_at_epoch_seconds: int
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
class LifecyclePostOperationReviewSubmissionV016:
    post_operation_review_id: str
    post_operation_reviewer_id: str
    post_operation_reviewer_organization_id: str
    objective: str
    review_requested_at_epoch_seconds: int
    reviewed_at_epoch_seconds: int
    source_operation_completion_id: str
    source_operation_completion_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    post_operation_review_evidence_digest: str
    requester_id: str
    source_completion_reviewer_id: str
    source_operator_id: str
    source_operation_approver_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    post_operation_review_route_digest: str
    review_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecyclePostOperationReviewArtifactV016:
    post_operation_review_id: str
    status: str
    reason: str
    post_operation_reviewer_id: str
    post_operation_reviewer_organization_id: str
    source_operation_completion_id: str
    source_completion_reviewer_id: str
    source_operator_id: str
    source_operation_approver_id: str
    source_authorization_decision_maker_id: str
    source_decision_reviewer_id: str
    subject_id: str
    requester_id: str
    policy_digest: str
    review_digest: str
    evidence_digest: str
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    operation_completed: bool
    post_operation_review_record_issued: bool
    post_operation_review_decision_made: bool
    post_operation_review_completed: bool
    post_operation_review_denied: bool
    lifecycle_transition_review_required_next: bool
    lifecycle_transition_review_route_required_next: bool
    operation_recovery_assessment_required_next: bool
    operation_recovery_assessment_route_required_next: bool
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


def policy_digest(value: LifecyclePostOperationReviewPolicyV016) -> str:
    return _digest_without(value, "policy_digest")


def evidence_digest(value: LifecyclePostOperationReviewEvidenceV016) -> str:
    return _digest_without(value, "evidence_digest")


def submission_digest(value: LifecyclePostOperationReviewSubmissionV016) -> str:
    return _digest_without(value, "review_digest")


def record_digest(value: LifecyclePostOperationReviewArtifactV016) -> str:
    return _digest_without(value, "record_digest")
