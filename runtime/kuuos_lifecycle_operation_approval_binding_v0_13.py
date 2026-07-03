from __future__ import annotations

from dataclasses import fields, replace
from typing import Any

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    LifecycleAuthorizationDecisionArtifactV012,
    LifecycleAuthorizationDecisionEvidenceV012,
    LifecycleAuthorizationDecisionPolicyV012,
    LifecycleAuthorizationDecisionSubmissionV012,
)
from runtime.kuuos_lifecycle_operation_approval_source_v0_13 import all_source_digests
from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import (
    OBJECTIVE,
    LifecycleOperationApprovalEvidenceV013,
    LifecycleOperationApprovalSubmissionV013,
    evidence_digest,
    submission_digest,
)

SEQUENCE_FIELDS = (
    "operation_scope_items",
    "target_resource_ids",
    "protected_resource_ids",
    "reversible_step_ids",
    "irreversible_step_ids",
)
SOURCE_COPY = {
    "approved_scope_digest": "authorized_scope_digest",
    "operation_scope_items": "operation_scope_items",
    "target_resource_ids": "target_resource_ids",
    "protected_resource_ids": "protected_resource_ids",
    "reversible_step_ids": "reversible_step_ids",
    "irreversible_step_ids": "irreversible_step_ids",
    "rollback_plan_digest": "rollback_plan_digest",
    "rollback_plan_verified": "rollback_plan_verified",
    "recovery_route_digest": "recovery_route_digest",
    "recovery_route_verified": "recovery_route_verified",
    "stop_condition_digest": "stop_condition_digest",
    "stop_conditions_complete": "stop_conditions_complete",
    "abort_channel_digest": "abort_channel_digest",
    "abort_channel_available": "abort_channel_available",
    "human_oversight_digest": "human_oversight_digest",
    "human_oversight_available": "human_oversight_available",
    "monitoring_plan_digest": "monitoring_plan_digest",
    "monitoring_plan_complete": "monitoring_plan_complete",
    "evidence_capture_plan_digest": "evidence_capture_plan_digest",
    "evidence_capture_plan_complete": "evidence_capture_plan_complete",
    "simulation_receipt_digest": "simulation_receipt_digest",
    "simulation_verified": "simulation_verified",
    "operation_window_seconds": "operation_window_seconds",
    "protected_core_excluded": "protected_core_excluded",
    "institutional_hold_active": "institutional_hold_active",
    "emergency_state_active": "emergency_state_active",
    "appeal_route_digest": "appeal_route_digest",
    "appeal_route_available": "appeal_route_available",
    "dissent_route_digest": "dissent_route_digest",
    "dissent_route_available": "dissent_route_available",
    "minority_opinion_digest": "minority_opinion_digest",
    "minority_opinion_recorded": "minority_opinion_recorded",
}


def make_evidence(
    source_decision: LifecycleAuthorizationDecisionSubmissionV012,
    source_evidence: LifecycleAuthorizationDecisionEvidenceV012,
    source_policy: LifecycleAuthorizationDecisionPolicyV012,
    source_record: LifecycleAuthorizationDecisionArtifactV012,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> LifecycleOperationApprovalEvidenceV013:
    values = {
        target: getattr(source_evidence, source)
        for target, source in SOURCE_COPY.items()
    }
    values.update(
        source_authorization_decision_id=source_decision.authorization_decision_id,
        source_authorization_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(
            source_decision, source_evidence, source_policy, source_record, source_args
        ),
        source_authorization_decision_maker_id=(
            source_decision.authorization_decision_maker_id
        ),
        source_decision_reviewer_id=source_decision.source_decision_reviewer_id,
        subject_id=source_decision.subject_id,
        subject_kind=source_decision.subject_kind,
        subject_version=source_decision.subject_version,
        requester_id=source_decision.requester_id,
        future_operator_id=source_decision.future_operator_id,
        operation_approval_route_digest=source_decision.operation_approval_route_digest,
    )
    values.update(overrides)
    for name in SEQUENCE_FIELDS:
        values[name] = canon(tuple(values[name]))
    value = LifecycleOperationApprovalEvidenceV013(evidence_digest="", **values)
    value = replace(value, evidence_digest=evidence_digest(value))
    issues = evidence_issues(value)
    if issues:
        raise ValueError(f"lifecycle_operation_approval_evidence_invalid:{issues[0]}")
    return value


def evidence_issues(value: LifecycleOperationApprovalEvidenceV013) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        value.evidence_id,
        value.operation_approval_id,
        value.operation_approver_id,
        value.operation_approver_organization_id,
        value.approver_mandate_receipt_digest,
        value.approver_qualification_receipt_digest,
        value.approver_independence_declaration_digest,
        value.conflict_disclosure_digest,
        value.jurisdiction_receipt_digest,
        value.quorum_receipt_digest,
        value.approval_rationale_digest,
        value.proportionality_review_digest,
        value.source_authorization_decision_id,
        value.source_authorization_record_digest,
        value.source_authorization_decision_maker_id,
        value.source_decision_reviewer_id,
        value.subject_id,
        value.subject_kind,
        value.subject_version,
        value.requester_id,
        value.future_operator_id,
        value.operation_approval_route_digest,
        value.approved_scope_digest,
        value.execution_package_digest,
        value.operator_acknowledgement_digest,
        value.resource_reservation_digest,
        value.rollback_plan_digest,
        value.recovery_route_digest,
        value.stop_condition_digest,
        value.abort_channel_digest,
        value.human_oversight_digest,
        value.monitoring_plan_digest,
        value.evidence_capture_plan_digest,
        value.simulation_receipt_digest,
        value.appeal_route_digest,
        value.dissent_route_digest,
        value.minority_opinion_digest,
    )
    if not all(required):
        issues.append("required_identity_receipt_or_binding_missing")
    if not value.source_artifact_digests:
        issues.append("source_digests_missing")
    times = (
        value.approval_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.completed_at_epoch_seconds,
        value.operation_approval_expiry_at_epoch_seconds,
        value.operation_start_window_open_at_epoch_seconds,
        value.operation_start_deadline_at_epoch_seconds,
        value.operation_window_seconds,
    )
    if min(times) < 0:
        issues.append("negative_time_or_window")
    for name in SEQUENCE_FIELDS:
        if getattr(value, name) != canon(getattr(value, name)):
            issues.append(f"{name}_not_canonical")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_submission(
    operation_approval_id: str,
    operation_approver_id: str,
    operation_approver_organization_id: str,
    approval_requested_at_epoch_seconds: int,
    completed_at_epoch_seconds: int,
    source_decision: LifecycleAuthorizationDecisionSubmissionV012,
    source_record: LifecycleAuthorizationDecisionArtifactV012,
    approval_evidence: LifecycleOperationApprovalEvidenceV013,
    *,
    operation_approval_route_digest: str,
    operation_start_deadline_at_epoch_seconds: int,
    objective: str = OBJECTIVE,
) -> LifecycleOperationApprovalSubmissionV013:
    value = LifecycleOperationApprovalSubmissionV013(
        operation_approval_id=operation_approval_id,
        operation_approver_id=operation_approver_id,
        operation_approver_organization_id=operation_approver_organization_id,
        objective=objective,
        approval_requested_at_epoch_seconds=approval_requested_at_epoch_seconds,
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        source_authorization_decision_id=source_decision.authorization_decision_id,
        source_authorization_record_digest=source_record.record_digest,
        subject_id=source_decision.subject_id,
        subject_kind=source_decision.subject_kind,
        subject_version=source_decision.subject_version,
        approval_evidence_digest=approval_evidence.evidence_digest,
        requester_id=source_decision.requester_id,
        source_authorization_decision_maker_id=source_decision.authorization_decision_maker_id,
        source_decision_reviewer_id=source_decision.source_decision_reviewer_id,
        future_operator_id=source_decision.future_operator_id,
        operation_approval_route_digest=operation_approval_route_digest,
        operation_start_deadline_at_epoch_seconds=operation_start_deadline_at_epoch_seconds,
        approval_digest="",
    )
    value = replace(value, approval_digest=submission_digest(value))
    issues = submission_issues(value)
    if issues:
        raise ValueError(f"lifecycle_operation_approval_invalid:{issues[0]}")
    return value


def submission_issues(value: LifecycleOperationApprovalSubmissionV013) -> tuple[str, ...]:
    issues: list[str] = []
    exempt = {
        "approval_digest", "version", "approval_requested_at_epoch_seconds",
        "completed_at_epoch_seconds", "operation_start_deadline_at_epoch_seconds",
    }
    if not all(getattr(value, item.name) for item in fields(value) if item.name not in exempt):
        issues.append("required_approval_field_missing")
    if min(
        value.approval_requested_at_epoch_seconds,
        value.completed_at_epoch_seconds,
        value.operation_start_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_approval_time")
    if value.approval_digest != submission_digest(value):
        issues.append("approval_digest_mismatch")
    return tuple(issues)


def scope_matches(
    evidence: LifecycleOperationApprovalEvidenceV013,
    source: LifecycleAuthorizationDecisionEvidenceV012,
) -> bool:
    for target, source_name in SOURCE_COPY.items():
        if target.endswith("_verified") or target.endswith("_complete") or target.endswith("_available") or target in {
            "protected_core_excluded", "institutional_hold_active",
            "emergency_state_active", "appeal_route_available",
            "dissent_route_available", "minority_opinion_recorded",
        }:
            continue
        left, right = getattr(evidence, target), getattr(source, source_name)
        if target in SEQUENCE_FIELDS:
            right = canon(tuple(right))
        if left != right:
            return False
    return True
