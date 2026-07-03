from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_operation_start_types_v0_14 import (
    LifecycleOperationStartArtifactV014,
    LifecycleOperationStartEvidenceV014,
    LifecycleOperationStartPolicyV014,
    LifecycleOperationStartSubmissionV014,
)
from runtime.kuuos_lifecycle_operation_completion_evaluation_v0_15 import (
    DENIAL_CHECKS,
    STRUCTURAL_CHECKS,
    evaluate,
)
from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    COMPLETED,
    DENIED,
    REJECTED,
    LifecycleOperationCompletionArtifactV015,
    LifecycleOperationCompletionEvidenceV015,
    LifecycleOperationCompletionPolicyV015,
    LifecycleOperationCompletionSubmissionV015,
    record_digest,
)

SOURCE_ORDER_CHECK = "source_start_completed_before_completion_request"


def compute_artifact(
    completion: LifecycleOperationCompletionSubmissionV015,
    evidence: LifecycleOperationCompletionEvidenceV015,
    policy: LifecycleOperationCompletionPolicyV015,
    source_start: LifecycleOperationStartSubmissionV014,
    source_evidence: LifecycleOperationStartEvidenceV014,
    source_policy: LifecycleOperationStartPolicyV014,
    source_record: LifecycleOperationStartArtifactV014,
    *source_args: Any,
) -> LifecycleOperationCompletionArtifactV015:
    checks, expected_digests = evaluate(
        completion,
        evidence,
        policy,
        source_start,
        source_evidence,
        source_policy,
        source_record,
        tuple(source_args),
    )
    checks[SOURCE_ORDER_CHECK] = (
        source_start.started_at_epoch_seconds
        <= completion.completion_requested_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(
        checks[name] for name in STRUCTURAL_CHECKS
    ):
        status = REJECTED
        reason = "source_operation_start_policy_or_binding_invalid"
    else:
        failed = next(
            (name for name in DENIAL_CHECKS if not checks[name]),
            None,
        )
        if failed is None:
            status = COMPLETED
            reason = "completed_for_separate_post_operation_review_only"
        else:
            status = DENIED
            reason = failed
    record_issued = status != REJECTED
    decision_made = status != REJECTED
    completed = status == COMPLETED
    denied = status == DENIED
    artifact = LifecycleOperationCompletionArtifactV015(
        operation_completion_id=completion.operation_completion_id,
        status=status,
        reason=reason,
        completion_reviewer_id=completion.completion_reviewer_id,
        completion_reviewer_organization_id=(
            completion.completion_reviewer_organization_id
        ),
        source_operation_start_id=completion.source_operation_start_id,
        source_operator_id=completion.source_operator_id,
        source_operation_approver_id=(
            completion.source_operation_approver_id
        ),
        source_authorization_decision_maker_id=(
            completion.source_authorization_decision_maker_id
        ),
        source_decision_reviewer_id=(
            completion.source_decision_reviewer_id
        ),
        subject_id=completion.subject_id,
        requester_id=completion.requester_id,
        policy_digest=policy.policy_digest,
        completion_digest=completion.completion_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        operation_started=source_record.operation_started,
        operation_completion_record_issued=record_issued,
        operation_completion_decision_made=decision_made,
        operation_completed=completed,
        operation_completion_denied=denied,
        post_operation_review_required_next=completed,
        post_operation_review_route_required_next=completed,
        operation_recovery_required_next=denied,
        operation_recovery_route_required_next=denied,
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


def verify_artifact(
    *args: Any, **kwargs: Any
) -> LifecycleOperationCompletionArtifactV015:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError(
            f"lifecycle_operation_completion_record_invalid:{issues[0]}"
        )
    return artifact


def artifact_issues(
    artifact: LifecycleOperationCompletionArtifactV015,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues: list[str] = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("operation_completion_recomputation_mismatch")
    if artifact.status not in (COMPLETED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == COMPLETED and not (
        artifact.operation_started
        and artifact.operation_completion_record_issued
        and artifact.operation_completion_decision_made
        and artifact.operation_completed
        and not artifact.operation_completion_denied
        and artifact.post_operation_review_required_next
        and artifact.post_operation_review_route_required_next
        and not artifact.operation_recovery_required_next
        and not artifact.operation_recovery_route_required_next
    ):
        issues.append("completed_gate_invalid")
    if artifact.status == DENIED and not (
        artifact.operation_started
        and artifact.operation_completion_record_issued
        and artifact.operation_completion_decision_made
        and not artifact.operation_completed
        and artifact.operation_completion_denied
        and not artifact.post_operation_review_required_next
        and not artifact.post_operation_review_route_required_next
        and artifact.operation_recovery_required_next
        and artifact.operation_recovery_route_required_next
    ):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and (
        artifact.operation_completion_record_issued
        or artifact.operation_completion_decision_made
        or artifact.operation_completed
        or artifact.operation_completion_denied
        or artifact.post_operation_review_required_next
        or artifact.post_operation_review_route_required_next
        or artifact.operation_recovery_required_next
        or artifact.operation_recovery_route_required_next
    ):
        issues.append("rejected_record_issued")
    later_effects = (
        artifact.authority_changed,
        artifact.quiescence_state_changed,
        artifact.terminal_state_changed,
        artifact.terminal_marker_written,
        artifact.resource_removed,
        artifact.external_operation_performed,
        artifact.repository_changed,
    )
    if any(later_effects):
        issues.append("post_operation_lifecycle_or_repository_effect_performed")
    if (
        not artifact.lifecycle_state_read_only
        or not artifact.repository_read_only
    ):
        issues.append("lifecycle_or_repository_read_only_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
