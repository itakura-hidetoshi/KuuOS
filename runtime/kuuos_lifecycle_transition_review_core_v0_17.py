from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import (
    LifecyclePostOperationReviewArtifactV016,
    LifecyclePostOperationReviewEvidenceV016,
    LifecyclePostOperationReviewPolicyV016,
    LifecyclePostOperationReviewSubmissionV016,
)
from runtime.kuuos_lifecycle_transition_review_evaluation_v0_17 import (
    BLOCKING_CHECKS,
    STRUCTURAL_CHECKS,
    evaluate,
)
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import (
    BLOCKED,
    CLEAR,
    REJECTED,
    LifecycleTransitionReviewArtifactV017,
    LifecycleTransitionReviewEvidenceV017,
    LifecycleTransitionReviewPolicyV017,
    LifecycleTransitionReviewSubmissionV017,
    record_digest,
)

SOURCE_ORDER_CHECK = "source_post_operation_review_precedes_transition_review_request"


def compute_artifact(
    review: LifecycleTransitionReviewSubmissionV017,
    evidence: LifecycleTransitionReviewEvidenceV017,
    policy: LifecycleTransitionReviewPolicyV017,
    source_review: LifecyclePostOperationReviewSubmissionV016,
    source_evidence: LifecyclePostOperationReviewEvidenceV016,
    source_policy: LifecyclePostOperationReviewPolicyV016,
    source_record: LifecyclePostOperationReviewArtifactV016,
    *source_args: Any,
) -> LifecycleTransitionReviewArtifactV017:
    checks, expected_digests = evaluate(
        review,
        evidence,
        policy,
        source_review,
        source_evidence,
        source_policy,
        source_record,
        tuple(source_args),
    )
    checks[SOURCE_ORDER_CHECK] = (
        source_review.reviewed_at_epoch_seconds
        <= review.review_requested_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(
        checks[name] for name in STRUCTURAL_CHECKS
    ):
        status = REJECTED
        reason = "source_post_operation_review_policy_or_binding_invalid"
    else:
        failed = next(
            (name for name in BLOCKING_CHECKS if not checks[name]),
            None,
        )
        if failed is None:
            status = CLEAR
            reason = "clear_for_separate_lifecycle_transition_decision_only"
        else:
            status = BLOCKED
            reason = failed
    issued = status != REJECTED
    completed = status != REJECTED
    clear = status == CLEAR
    blocked = status == BLOCKED
    artifact = LifecycleTransitionReviewArtifactV017(
        transition_review_id=review.transition_review_id,
        status=status,
        reason=reason,
        transition_reviewer_id=review.transition_reviewer_id,
        transition_reviewer_organization_id=review.transition_reviewer_organization_id,
        source_post_operation_review_id=review.source_post_operation_review_id,
        source_post_operation_reviewer_id=review.source_post_operation_reviewer_id,
        transition_decision_maker_id=review.transition_decision_maker_id,
        proposed_transition_kind=review.proposed_transition_kind,
        subject_id=review.subject_id,
        requester_id=review.requester_id,
        policy_digest=policy.policy_digest,
        review_digest=review.review_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_post_operation_review_completed=(
            source_record.post_operation_review_completed
        ),
        transition_review_record_issued=issued,
        transition_review_completed=completed,
        clear_for_transition_decision=clear,
        transition_review_blocked=blocked,
        transition_decision_required_next=clear,
        transition_decision_route_required_next=clear,
        transition_reassessment_required_next=blocked,
        transition_reassessment_route_required_next=blocked,
        transition_decision_made=False,
        lifecycle_transition_performed=False,
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


def verify_artifact(*args: Any, **kwargs: Any) -> LifecycleTransitionReviewArtifactV017:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError(f"lifecycle_transition_review_record_invalid:{issues[0]}")
    return artifact


def artifact_issues(
    artifact: LifecycleTransitionReviewArtifactV017,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues: list[str] = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("transition_review_recomputation_mismatch")
    if artifact.status not in (CLEAR, BLOCKED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == CLEAR and not all(
        (
            artifact.source_post_operation_review_completed,
            artifact.transition_review_record_issued,
            artifact.transition_review_completed,
            artifact.clear_for_transition_decision,
            not artifact.transition_review_blocked,
            artifact.transition_decision_required_next,
            artifact.transition_decision_route_required_next,
            not artifact.transition_reassessment_required_next,
            not artifact.transition_reassessment_route_required_next,
            not artifact.transition_decision_made,
            not artifact.lifecycle_transition_performed,
        )
    ):
        issues.append("clear_gate_invalid")
    if artifact.status == BLOCKED and not all(
        (
            artifact.source_post_operation_review_completed,
            artifact.transition_review_record_issued,
            artifact.transition_review_completed,
            not artifact.clear_for_transition_decision,
            artifact.transition_review_blocked,
            not artifact.transition_decision_required_next,
            not artifact.transition_decision_route_required_next,
            artifact.transition_reassessment_required_next,
            artifact.transition_reassessment_route_required_next,
            not artifact.transition_decision_made,
            not artifact.lifecycle_transition_performed,
        )
    ):
        issues.append("blocked_gate_invalid")
    if artifact.status == REJECTED and any(
        (
            artifact.transition_review_record_issued,
            artifact.transition_review_completed,
            artifact.clear_for_transition_decision,
            artifact.transition_review_blocked,
            artifact.transition_decision_required_next,
            artifact.transition_decision_route_required_next,
            artifact.transition_reassessment_required_next,
            artifact.transition_reassessment_route_required_next,
            artifact.transition_decision_made,
            artifact.lifecycle_transition_performed,
        )
    ):
        issues.append("rejected_record_issued")
    effects = (
        artifact.authority_changed,
        artifact.quiescence_state_changed,
        artifact.terminal_state_changed,
        artifact.terminal_marker_written,
        artifact.resource_removed,
        artifact.external_operation_performed,
        artifact.repository_changed,
    )
    if any(effects):
        issues.append("transition_or_repository_effect_performed")
    if not artifact.lifecycle_state_read_only or not artifact.repository_read_only:
        issues.append("read_only_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
