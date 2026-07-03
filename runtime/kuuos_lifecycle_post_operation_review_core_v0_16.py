from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    LifecycleOperationCompletionArtifactV015,
    LifecycleOperationCompletionEvidenceV015,
    LifecycleOperationCompletionPolicyV015,
    LifecycleOperationCompletionSubmissionV015,
)
from runtime.kuuos_lifecycle_post_operation_review_evaluation_v0_16 import (
    DENIAL_CHECKS,
    STRUCTURAL_CHECKS,
    evaluate,
)
from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import (
    DENIED,
    REJECTED,
    REVIEWED,
    LifecyclePostOperationReviewArtifactV016,
    LifecyclePostOperationReviewEvidenceV016,
    LifecyclePostOperationReviewPolicyV016,
    LifecyclePostOperationReviewSubmissionV016,
    record_digest,
)

SOURCE_ORDER_CHECK = "source_completion_precedes_post_operation_review_request"


def compute_artifact(
    review: LifecyclePostOperationReviewSubmissionV016,
    evidence: LifecyclePostOperationReviewEvidenceV016,
    policy: LifecyclePostOperationReviewPolicyV016,
    source_completion: LifecycleOperationCompletionSubmissionV015,
    source_evidence: LifecycleOperationCompletionEvidenceV015,
    source_policy: LifecycleOperationCompletionPolicyV015,
    source_record: LifecycleOperationCompletionArtifactV015,
    *source_args: Any,
) -> LifecyclePostOperationReviewArtifactV016:
    checks, expected_digests = evaluate(
        review,
        evidence,
        policy,
        source_completion,
        source_evidence,
        source_policy,
        source_record,
        tuple(source_args),
    )
    checks[SOURCE_ORDER_CHECK] = (
        source_completion.completed_at_epoch_seconds
        <= review.review_requested_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(
        checks[name] for name in STRUCTURAL_CHECKS
    ):
        status = REJECTED
        reason = "source_operation_completion_policy_or_binding_invalid"
    else:
        failed = next(
            (name for name in DENIAL_CHECKS if not checks[name]),
            None,
        )
        if failed is None:
            status = REVIEWED
            reason = "reviewed_for_separate_lifecycle_transition_review_only"
        else:
            status = DENIED
            reason = failed
    record_issued = status != REJECTED
    decision_made = status != REJECTED
    reviewed = status == REVIEWED
    denied = status == DENIED
    artifact = LifecyclePostOperationReviewArtifactV016(
        post_operation_review_id=review.post_operation_review_id,
        status=status,
        reason=reason,
        post_operation_reviewer_id=review.post_operation_reviewer_id,
        post_operation_reviewer_organization_id=(
            review.post_operation_reviewer_organization_id
        ),
        source_operation_completion_id=(
            review.source_operation_completion_id
        ),
        source_completion_reviewer_id=(
            review.source_completion_reviewer_id
        ),
        source_operator_id=review.source_operator_id,
        source_operation_approver_id=(
            review.source_operation_approver_id
        ),
        source_authorization_decision_maker_id=(
            review.source_authorization_decision_maker_id
        ),
        source_decision_reviewer_id=(
            review.source_decision_reviewer_id
        ),
        subject_id=review.subject_id,
        requester_id=review.requester_id,
        policy_digest=policy.policy_digest,
        review_digest=review.review_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        operation_completed=source_record.operation_completed,
        post_operation_review_record_issued=record_issued,
        post_operation_review_decision_made=decision_made,
        post_operation_review_completed=reviewed,
        post_operation_review_denied=denied,
        lifecycle_transition_review_required_next=reviewed,
        lifecycle_transition_review_route_required_next=reviewed,
        operation_recovery_assessment_required_next=denied,
        operation_recovery_assessment_route_required_next=denied,
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
) -> LifecyclePostOperationReviewArtifactV016:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError(
            f"lifecycle_post_operation_review_record_invalid:{issues[0]}"
        )
    return artifact


def artifact_issues(
    artifact: LifecyclePostOperationReviewArtifactV016,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues: list[str] = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("post_operation_review_recomputation_mismatch")
    if artifact.status not in (REVIEWED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == REVIEWED and not (
        artifact.operation_completed
        and artifact.post_operation_review_record_issued
        and artifact.post_operation_review_decision_made
        and artifact.post_operation_review_completed
        and not artifact.post_operation_review_denied
        and artifact.lifecycle_transition_review_required_next
        and artifact.lifecycle_transition_review_route_required_next
        and not artifact.operation_recovery_assessment_required_next
        and not artifact.operation_recovery_assessment_route_required_next
    ):
        issues.append("reviewed_gate_invalid")
    if artifact.status == DENIED and not (
        artifact.operation_completed
        and artifact.post_operation_review_record_issued
        and artifact.post_operation_review_decision_made
        and not artifact.post_operation_review_completed
        and artifact.post_operation_review_denied
        and not artifact.lifecycle_transition_review_required_next
        and not artifact.lifecycle_transition_review_route_required_next
        and artifact.operation_recovery_assessment_required_next
        and artifact.operation_recovery_assessment_route_required_next
    ):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and (
        artifact.post_operation_review_record_issued
        or artifact.post_operation_review_decision_made
        or artifact.post_operation_review_completed
        or artifact.post_operation_review_denied
        or artifact.lifecycle_transition_review_required_next
        or artifact.lifecycle_transition_review_route_required_next
        or artifact.operation_recovery_assessment_required_next
        or artifact.operation_recovery_assessment_route_required_next
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
        issues.append("post_review_lifecycle_or_repository_effect_performed")
    if (
        not artifact.lifecycle_state_read_only
        or not artifact.repository_read_only
    ):
        issues.append("lifecycle_or_repository_read_only_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
