from __future__ import annotations

from dataclasses import fields, replace
from typing import Any

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import (
    LifecycleOperationApprovalArtifactV013,
    LifecycleOperationApprovalEvidenceV013,
    LifecycleOperationApprovalPolicyV013,
    LifecycleOperationApprovalSubmissionV013,
)
from runtime.kuuos_lifecycle_operation_start_source_v0_14 import (
    all_source_digests,
    expected_operation_start_route_digest,
)
from runtime.kuuos_lifecycle_operation_start_types_v0_14 import (
    OBJECTIVE,
    LifecycleOperationStartEvidenceV014,
    LifecycleOperationStartSubmissionV014,
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
    "approved_scope_digest": "approved_scope_digest",
    "operation_scope_items": "operation_scope_items",
    "target_resource_ids": "target_resource_ids",
    "protected_resource_ids": "protected_resource_ids",
    "reversible_step_ids": "reversible_step_ids",
    "irreversible_step_ids": "irreversible_step_ids",
    "execution_package_digest": "execution_package_digest",
    "resource_reservation_digest": "resource_reservation_digest",
    "rollback_plan_digest": "rollback_plan_digest",
    "recovery_route_digest": "recovery_route_digest",
    "stop_condition_digest": "stop_condition_digest",
    "abort_channel_digest": "abort_channel_digest",
    "human_oversight_digest": "human_oversight_digest",
    "monitoring_plan_digest": "monitoring_plan_digest",
    "evidence_capture_plan_digest": "evidence_capture_plan_digest",
    "operation_window_seconds": "operation_window_seconds",
    "protected_core_excluded": "protected_core_excluded",
    "institutional_hold_active": "institutional_hold_active",
    "emergency_state_active": "emergency_state_active",
}


def make_evidence(
    source_approval: LifecycleOperationApprovalSubmissionV013,
    source_evidence: LifecycleOperationApprovalEvidenceV013,
    source_policy: LifecycleOperationApprovalPolicyV013,
    source_record: LifecycleOperationApprovalArtifactV013,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> LifecycleOperationStartEvidenceV014:
    values = {
        target: getattr(source_evidence, source)
        for target, source in SOURCE_COPY.items()
    }
    values.update(
        source_operation_approval_id=source_approval.operation_approval_id,
        source_operation_approval_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(
            source_approval, source_evidence, source_policy, source_record, source_args
        ),
        source_operation_approver_id=source_approval.operation_approver_id,
        source_authorization_decision_maker_id=(
            source_approval.source_authorization_decision_maker_id
        ),
        source_decision_reviewer_id=source_approval.source_decision_reviewer_id,
        subject_id=source_approval.subject_id,
        subject_kind=source_approval.subject_kind,
        subject_version=source_approval.subject_version,
        requester_id=source_approval.requester_id,
        approved_future_operator_id=source_approval.future_operator_id,
        operation_start_route_digest=expected_operation_start_route_digest(
            source_approval, source_evidence, source_record
        ),
        operation_start_deadline_at_epoch_seconds=(
            source_evidence.operation_start_deadline_at_epoch_seconds
        ),
    )
    values.update(overrides)
    for name in SEQUENCE_FIELDS:
        values[name] = canon(tuple(values[name]))
    value = LifecycleOperationStartEvidenceV014(evidence_digest="", **values)
    value = replace(value, evidence_digest=evidence_digest(value))
    issues = evidence_issues(value)
    if issues:
        raise ValueError(f"lifecycle_operation_start_evidence_invalid:{issues[0]}")
    return value


def evidence_issues(value: LifecycleOperationStartEvidenceV014) -> tuple[str, ...]:
    issues: list[str] = []
    exempt = {
        "evidence_digest",
        "version",
        "material_conflict_present",
        "institutional_hold_active",
        "emergency_state_active",
        "start_requested_at_epoch_seconds",
        "captured_at_epoch_seconds",
        "started_at_epoch_seconds",
        "operation_start_deadline_at_epoch_seconds",
        "operation_completion_deadline_at_epoch_seconds",
        "operation_window_seconds",
        "protected_core_excluded",
        *SEQUENCE_FIELDS,
    }
    if not all(
        getattr(value, item.name)
        for item in fields(value)
        if item.name not in exempt and not item.name.endswith("_reconfirmed")
        and not item.name.endswith("_verified") and not item.name.endswith("_confirmed")
        and not item.name.endswith("_complete") and item.name != "operator_ready"
        and item.name != "start_authorization_acknowledged"
    ):
        issues.append("required_identity_receipt_or_binding_missing")
    if not value.source_artifact_digests:
        issues.append("source_digests_missing")
    times = (
        value.start_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.started_at_epoch_seconds,
        value.operation_start_deadline_at_epoch_seconds,
        value.operation_completion_deadline_at_epoch_seconds,
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
    operation_start_id: str,
    operator_id: str,
    operator_organization_id: str,
    start_requested_at_epoch_seconds: int,
    started_at_epoch_seconds: int,
    source_approval: LifecycleOperationApprovalSubmissionV013,
    source_record: LifecycleOperationApprovalArtifactV013,
    start_evidence: LifecycleOperationStartEvidenceV014,
    *,
    operation_start_route_digest: str,
    operation_completion_deadline_at_epoch_seconds: int,
    objective: str = OBJECTIVE,
) -> LifecycleOperationStartSubmissionV014:
    value = LifecycleOperationStartSubmissionV014(
        operation_start_id=operation_start_id,
        operator_id=operator_id,
        operator_organization_id=operator_organization_id,
        objective=objective,
        start_requested_at_epoch_seconds=start_requested_at_epoch_seconds,
        started_at_epoch_seconds=started_at_epoch_seconds,
        source_operation_approval_id=source_approval.operation_approval_id,
        source_operation_approval_record_digest=source_record.record_digest,
        subject_id=source_approval.subject_id,
        subject_kind=source_approval.subject_kind,
        subject_version=source_approval.subject_version,
        start_evidence_digest=start_evidence.evidence_digest,
        requester_id=source_approval.requester_id,
        source_operation_approver_id=source_approval.operation_approver_id,
        source_authorization_decision_maker_id=(
            source_approval.source_authorization_decision_maker_id
        ),
        source_decision_reviewer_id=source_approval.source_decision_reviewer_id,
        approved_future_operator_id=source_approval.future_operator_id,
        operation_start_route_digest=operation_start_route_digest,
        operation_completion_deadline_at_epoch_seconds=(
            operation_completion_deadline_at_epoch_seconds
        ),
        start_digest="",
    )
    value = replace(value, start_digest=submission_digest(value))
    issues = submission_issues(value)
    if issues:
        raise ValueError(f"lifecycle_operation_start_invalid:{issues[0]}")
    return value


def submission_issues(value: LifecycleOperationStartSubmissionV014) -> tuple[str, ...]:
    issues: list[str] = []
    exempt = {
        "start_digest", "version", "start_requested_at_epoch_seconds",
        "started_at_epoch_seconds", "operation_completion_deadline_at_epoch_seconds",
    }
    if not all(getattr(value, item.name) for item in fields(value) if item.name not in exempt):
        issues.append("required_start_field_missing")
    if min(
        value.start_requested_at_epoch_seconds,
        value.started_at_epoch_seconds,
        value.operation_completion_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_start_time")
    if value.start_digest != submission_digest(value):
        issues.append("start_digest_mismatch")
    return tuple(issues)


def scope_matches(
    evidence: LifecycleOperationStartEvidenceV014,
    source: LifecycleOperationApprovalEvidenceV013,
) -> bool:
    for target, source_name in SOURCE_COPY.items():
        left, right = getattr(evidence, target), getattr(source, source_name)
        if target in SEQUENCE_FIELDS:
            right = canon(tuple(right))
        if left != right:
            return False
    return True
