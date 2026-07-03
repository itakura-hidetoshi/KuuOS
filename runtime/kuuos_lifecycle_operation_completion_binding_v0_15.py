from __future__ import annotations

from dataclasses import fields, replace
from typing import Any

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_operation_start_types_v0_14 import (
    LifecycleOperationStartArtifactV014,
    LifecycleOperationStartEvidenceV014,
    LifecycleOperationStartPolicyV014,
    LifecycleOperationStartSubmissionV014,
)
from runtime.kuuos_lifecycle_operation_completion_source_v0_15 import (
    all_source_digests,
    expected_operation_completion_route_digest,
)
from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    OBJECTIVE,
    LifecycleOperationCompletionEvidenceV015,
    LifecycleOperationCompletionSubmissionV015,
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
}


def make_evidence(
    source_start: LifecycleOperationStartSubmissionV014,
    source_evidence: LifecycleOperationStartEvidenceV014,
    source_policy: LifecycleOperationStartPolicyV014,
    source_record: LifecycleOperationStartArtifactV014,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> LifecycleOperationCompletionEvidenceV015:
    values = {
        target: getattr(source_evidence, source)
        for target, source in SOURCE_COPY.items()
    }
    values.update(
        source_operation_start_id=source_start.operation_start_id,
        source_operation_start_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(
            source_start,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        source_operator_id=source_start.operator_id,
        source_operator_organization_id=source_start.operator_organization_id,
        source_operation_approver_id=source_start.source_operation_approver_id,
        source_authorization_decision_maker_id=(
            source_start.source_authorization_decision_maker_id
        ),
        source_decision_reviewer_id=source_start.source_decision_reviewer_id,
        subject_id=source_start.subject_id,
        subject_kind=source_start.subject_kind,
        subject_version=source_start.subject_version,
        requester_id=source_start.requester_id,
        operation_completion_route_digest=(
            expected_operation_completion_route_digest(
                source_start, source_evidence, source_record
            )
        ),
        operation_completion_deadline_at_epoch_seconds=(
            source_start.operation_completion_deadline_at_epoch_seconds
        ),
    )
    values.update(overrides)
    for name in SEQUENCE_FIELDS:
        values[name] = canon(tuple(values[name]))
    values["step_result_digests"] = dict(
        sorted(dict(values["step_result_digests"]).items())
    )
    value = LifecycleOperationCompletionEvidenceV015(
        evidence_digest="", **values
    )
    value = replace(value, evidence_digest=evidence_digest(value))
    issues = evidence_issues(value)
    if issues:
        raise ValueError(
            f"lifecycle_operation_completion_evidence_invalid:{issues[0]}"
        )
    return value


def evidence_issues(
    value: LifecycleOperationCompletionEvidenceV015,
) -> tuple[str, ...]:
    issues: list[str] = []
    exempt = {
        "evidence_digest",
        "version",
        "material_conflict_present",
        "unresolved_stop_condition_present",
        "abort_triggered",
        "rollback_pending",
        "recovery_pending",
        "external_operation_performed",
        "repository_changed",
        "completion_requested_at_epoch_seconds",
        "captured_at_epoch_seconds",
        "completed_at_epoch_seconds",
        "operation_completion_deadline_at_epoch_seconds",
        "step_result_digests",
        *SEQUENCE_FIELDS,
    }
    boolean_suffixes = (
        "_verified",
        "_confirmed",
        "_complete",
        "_completed",
        "_accounted",
        "_intact",
        "_released",
        "_ready",
        "_finished",
    )
    for item in fields(value):
        if item.name in exempt or item.name.endswith(boolean_suffixes):
            continue
        if not getattr(value, item.name):
            issues.append("required_identity_receipt_or_binding_missing")
            break
    if not value.source_artifact_digests:
        issues.append("source_digests_missing")
    if not value.step_result_digests:
        issues.append("step_result_digests_missing")
    if value.step_result_digests != dict(
        sorted(value.step_result_digests.items())
    ):
        issues.append("step_result_digests_not_canonical")
    times = (
        value.completion_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.completed_at_epoch_seconds,
        value.operation_completion_deadline_at_epoch_seconds,
    )
    if min(times) < 0:
        issues.append("negative_completion_time")
    for name in SEQUENCE_FIELDS:
        if getattr(value, name) != canon(getattr(value, name)):
            issues.append(f"{name}_not_canonical")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_submission(
    operation_completion_id: str,
    completion_reviewer_id: str,
    completion_reviewer_organization_id: str,
    completion_requested_at_epoch_seconds: int,
    completed_at_epoch_seconds: int,
    source_start: LifecycleOperationStartSubmissionV014,
    source_record: LifecycleOperationStartArtifactV014,
    completion_evidence: LifecycleOperationCompletionEvidenceV015,
    *,
    operation_completion_route_digest: str,
    objective: str = OBJECTIVE,
) -> LifecycleOperationCompletionSubmissionV015:
    value = LifecycleOperationCompletionSubmissionV015(
        operation_completion_id=operation_completion_id,
        completion_reviewer_id=completion_reviewer_id,
        completion_reviewer_organization_id=(
            completion_reviewer_organization_id
        ),
        objective=objective,
        completion_requested_at_epoch_seconds=(
            completion_requested_at_epoch_seconds
        ),
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        source_operation_start_id=source_start.operation_start_id,
        source_operation_start_record_digest=source_record.record_digest,
        subject_id=source_start.subject_id,
        subject_kind=source_start.subject_kind,
        subject_version=source_start.subject_version,
        completion_evidence_digest=completion_evidence.evidence_digest,
        requester_id=source_start.requester_id,
        source_operator_id=source_start.operator_id,
        source_operation_approver_id=source_start.source_operation_approver_id,
        source_authorization_decision_maker_id=(
            source_start.source_authorization_decision_maker_id
        ),
        source_decision_reviewer_id=(
            source_start.source_decision_reviewer_id
        ),
        operation_completion_route_digest=operation_completion_route_digest,
        completion_digest="",
    )
    value = replace(value, completion_digest=submission_digest(value))
    issues = submission_issues(value)
    if issues:
        raise ValueError(
            f"lifecycle_operation_completion_invalid:{issues[0]}"
        )
    return value


def submission_issues(
    value: LifecycleOperationCompletionSubmissionV015,
) -> tuple[str, ...]:
    issues: list[str] = []
    exempt = {
        "completion_digest",
        "version",
        "completion_requested_at_epoch_seconds",
        "completed_at_epoch_seconds",
    }
    if not all(
        getattr(value, item.name)
        for item in fields(value)
        if item.name not in exempt
    ):
        issues.append("required_completion_field_missing")
    if min(
        value.completion_requested_at_epoch_seconds,
        value.completed_at_epoch_seconds,
    ) < 0:
        issues.append("negative_completion_time")
    if value.completion_digest != submission_digest(value):
        issues.append("completion_digest_mismatch")
    return tuple(issues)


def scope_matches(
    evidence: LifecycleOperationCompletionEvidenceV015,
    source: LifecycleOperationStartEvidenceV014,
) -> bool:
    for target, source_name in SOURCE_COPY.items():
        left = getattr(evidence, target)
        right = getattr(source, source_name)
        if target in SEQUENCE_FIELDS:
            right = canon(tuple(right))
        if left != right:
            return False
    return True
