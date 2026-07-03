from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import (
    LifecycleOperationApprovalArtifactV013,
    LifecycleOperationApprovalEvidenceV013,
    LifecycleOperationApprovalPolicyV013,
    LifecycleOperationApprovalSubmissionV013,
)
from runtime.kuuos_lifecycle_operation_start_evaluation_v0_14 import (
    DENIAL_CHECKS,
    STRUCTURAL_CHECKS,
    evaluate,
)
from runtime.kuuos_lifecycle_operation_start_types_v0_14 import (
    DENIED,
    REJECTED,
    STARTED,
    LifecycleOperationStartArtifactV014,
    LifecycleOperationStartEvidenceV014,
    LifecycleOperationStartPolicyV014,
    LifecycleOperationStartSubmissionV014,
    record_digest,
)

SOURCE_ORDER_CHECK = "source_approval_completed_before_start_request"


def compute_artifact(
    start: LifecycleOperationStartSubmissionV014,
    evidence: LifecycleOperationStartEvidenceV014,
    policy: LifecycleOperationStartPolicyV014,
    source_approval: LifecycleOperationApprovalSubmissionV013,
    source_evidence: LifecycleOperationApprovalEvidenceV013,
    source_policy: LifecycleOperationApprovalPolicyV013,
    source_record: LifecycleOperationApprovalArtifactV013,
    *source_args: Any,
) -> LifecycleOperationStartArtifactV014:
    checks, expected_digests = evaluate(
        start,
        evidence,
        policy,
        source_approval,
        source_evidence,
        source_policy,
        source_record,
        tuple(source_args),
    )
    checks[SOURCE_ORDER_CHECK] = (
        source_approval.completed_at_epoch_seconds
        <= start.start_requested_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(
        checks[name] for name in STRUCTURAL_CHECKS
    ):
        status = REJECTED
        reason = "source_operation_approval_policy_or_binding_invalid"
    else:
        failed = next((name for name in DENIAL_CHECKS if not checks[name]), None)
        if failed is None:
            status = STARTED
            reason = "started_for_separate_operation_completion_only"
        else:
            status = DENIED
            reason = failed
    record_issued = status != REJECTED
    decision_made = status != REJECTED
    started = status == STARTED
    denied = status == DENIED
    artifact = LifecycleOperationStartArtifactV014(
        operation_start_id=start.operation_start_id,
        status=status,
        reason=reason,
        operator_id=start.operator_id,
        operator_organization_id=start.operator_organization_id,
        source_operation_approval_id=start.source_operation_approval_id,
        source_operation_approver_id=start.source_operation_approver_id,
        source_authorization_decision_maker_id=(
            start.source_authorization_decision_maker_id
        ),
        source_decision_reviewer_id=start.source_decision_reviewer_id,
        subject_id=start.subject_id,
        requester_id=start.requester_id,
        approved_future_operator_id=start.approved_future_operator_id,
        policy_digest=policy.policy_digest,
        start_digest=start.start_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        operation_start_record_issued=record_issued,
        operation_start_decision_made=decision_made,
        operation_started=started,
        operation_start_denied=denied,
        operation_completion_required_next=started,
        operation_completion_route_required_next=started,
        operation_completed=False,
        authority_changed=False,
        quiescence_state_changed=False,
        terminal_state_changed=False,
        terminal_marker_written=False,
        resource_removed=False,
        external_operation_performed=False,
        repository_changed=False,
        lifecycle_state_read_only=True,
        repository_read_only=True,
        record_digest="",
    )
    return replace(artifact, record_digest=record_digest(artifact))


def verify_artifact(*args: Any, **kwargs: Any) -> LifecycleOperationStartArtifactV014:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError(f"lifecycle_operation_start_record_invalid:{issues[0]}")
    return artifact


def artifact_issues(
    artifact: LifecycleOperationStartArtifactV014,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues: list[str] = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("operation_start_recomputation_mismatch")
    if artifact.status not in (STARTED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == STARTED and not (
        artifact.operation_start_record_issued
        and artifact.operation_start_decision_made
        and artifact.operation_started
        and not artifact.operation_start_denied
        and artifact.operation_completion_required_next
        and artifact.operation_completion_route_required_next
    ):
        issues.append("started_gate_invalid")
    if artifact.status == DENIED and (
        not artifact.operation_start_record_issued
        or not artifact.operation_start_decision_made
        or artifact.operation_started
        or not artifact.operation_start_denied
        or artifact.operation_completion_required_next
        or artifact.operation_completion_route_required_next
    ):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and (
        artifact.operation_start_record_issued
        or artifact.operation_start_decision_made
        or artifact.operation_started
        or artifact.operation_start_denied
        or artifact.operation_completion_required_next
        or artifact.operation_completion_route_required_next
    ):
        issues.append("rejected_record_issued")
    later_effects = (
        artifact.operation_completed,
        artifact.authority_changed,
        artifact.quiescence_state_changed,
        artifact.terminal_state_changed,
        artifact.terminal_marker_written,
        artifact.resource_removed,
        artifact.external_operation_performed,
        artifact.repository_changed,
    )
    if any(later_effects):
        issues.append("operation_completion_or_lifecycle_effect_performed")
    if not artifact.lifecycle_state_read_only or not artifact.repository_read_only:
        issues.append("lifecycle_or_repository_read_only_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
