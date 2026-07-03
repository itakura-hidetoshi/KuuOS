from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    LifecycleAuthorizationDecisionArtifactV012,
    LifecycleAuthorizationDecisionEvidenceV012,
    LifecycleAuthorizationDecisionPolicyV012,
    LifecycleAuthorizationDecisionSubmissionV012,
)
from runtime.kuuos_lifecycle_operation_approval_evaluation_v0_13 import (
    DENIAL_CHECKS,
    STRUCTURAL_CHECKS,
    evaluate,
)
from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import (
    APPROVED,
    DENIED,
    REJECTED,
    LifecycleOperationApprovalArtifactV013,
    LifecycleOperationApprovalEvidenceV013,
    LifecycleOperationApprovalPolicyV013,
    LifecycleOperationApprovalSubmissionV013,
    record_digest,
)

SOURCE_ORDER_CHECK = "source_authorization_completed_before_approval_request"


def compute_artifact(
    approval: LifecycleOperationApprovalSubmissionV013,
    evidence: LifecycleOperationApprovalEvidenceV013,
    policy: LifecycleOperationApprovalPolicyV013,
    source_decision: LifecycleAuthorizationDecisionSubmissionV012,
    source_evidence: LifecycleAuthorizationDecisionEvidenceV012,
    source_policy: LifecycleAuthorizationDecisionPolicyV012,
    source_record: LifecycleAuthorizationDecisionArtifactV012,
    *source_args: Any,
) -> LifecycleOperationApprovalArtifactV013:
    checks, expected_digests = evaluate(
        approval,
        evidence,
        policy,
        source_decision,
        source_evidence,
        source_policy,
        source_record,
        tuple(source_args),
    )
    checks[SOURCE_ORDER_CHECK] = (
        source_decision.completed_at_epoch_seconds
        <= approval.approval_requested_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(
        checks[name] for name in STRUCTURAL_CHECKS
    ):
        status = REJECTED
        reason = "source_authorization_policy_or_binding_invalid"
    else:
        failed = next((name for name in DENIAL_CHECKS if not checks[name]), None)
        if failed is None:
            status = APPROVED
            reason = "approved_for_separate_operation_start_only"
        else:
            status = DENIED
            reason = failed
    record_issued = status != REJECTED
    approval_made = status != REJECTED
    approved = status == APPROVED
    denied = status == DENIED
    artifact = LifecycleOperationApprovalArtifactV013(
        operation_approval_id=approval.operation_approval_id,
        status=status,
        reason=reason,
        operation_approver_id=approval.operation_approver_id,
        operation_approver_organization_id=(
            approval.operation_approver_organization_id
        ),
        source_authorization_decision_id=(
            approval.source_authorization_decision_id
        ),
        source_authorization_decision_maker_id=(
            approval.source_authorization_decision_maker_id
        ),
        source_decision_reviewer_id=approval.source_decision_reviewer_id,
        subject_id=approval.subject_id,
        requester_id=approval.requester_id,
        future_operator_id=approval.future_operator_id,
        policy_digest=policy.policy_digest,
        approval_digest=approval.approval_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        operation_approval_record_issued=record_issued,
        operation_approval_made=approval_made,
        operation_approved=approved,
        operation_denied=denied,
        operation_start_required_next=approved,
        operation_start_route_required_next=approved,
        operation_started=False,
        operation_completed=False,
        authority_changed=False,
        quiescence_state_changed=False,
        terminal_state_changed=False,
        terminal_marker_written=False,
        resource_removed=False,
        external_operation_performed=False,
        repository_changed=False,
        lifecycle_read_only=True,
        record_digest="",
    )
    return replace(artifact, record_digest=record_digest(artifact))


def verify_artifact(*args: Any, **kwargs: Any) -> LifecycleOperationApprovalArtifactV013:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError(f"lifecycle_operation_approval_record_invalid:{issues[0]}")
    return artifact


def artifact_issues(
    artifact: LifecycleOperationApprovalArtifactV013,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues: list[str] = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("operation_approval_recomputation_mismatch")
    if artifact.status not in (APPROVED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == APPROVED and not (
        artifact.operation_approval_record_issued
        and artifact.operation_approval_made
        and artifact.operation_approved
        and not artifact.operation_denied
        and artifact.operation_start_required_next
        and artifact.operation_start_route_required_next
    ):
        issues.append("approved_gate_invalid")
    if artifact.status == DENIED and (
        not artifact.operation_approval_record_issued
        or not artifact.operation_approval_made
        or artifact.operation_approved
        or not artifact.operation_denied
        or artifact.operation_start_required_next
        or artifact.operation_start_route_required_next
    ):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and (
        artifact.operation_approval_record_issued
        or artifact.operation_approval_made
        or artifact.operation_approved
        or artifact.operation_denied
        or artifact.operation_start_required_next
        or artifact.operation_start_route_required_next
    ):
        issues.append("rejected_record_issued")
    later_effects = (
        artifact.operation_started,
        artifact.operation_completed,
        artifact.authority_changed,
        artifact.quiescence_state_changed,
        artifact.terminal_state_changed,
        artifact.terminal_marker_written,
        artifact.resource_removed,
        artifact.external_operation_performed,
        artifact.repository_changed,
    )
    if any(later_effects) or not artifact.lifecycle_read_only:
        issues.append("operation_execution_or_lifecycle_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
