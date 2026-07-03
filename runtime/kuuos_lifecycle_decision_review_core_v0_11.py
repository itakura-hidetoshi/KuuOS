from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import (
    LifecycleBoundedRequestArtifactV010,
    LifecycleBoundedRequestEvidenceV010,
    LifecycleBoundedRequestPolicyV010,
    LifecycleBoundedRequestSubmissionV010,
)
from runtime.kuuos_lifecycle_decision_review_evaluation_v0_11 import (
    BLOCKING_CHECKS,
    STRUCTURAL_CHECKS,
    evaluate,
)
from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    BLOCKED,
    CLEAR,
    REJECTED,
    LifecycleDecisionReviewArtifactV011,
    LifecycleDecisionReviewEvidenceV011,
    LifecycleDecisionReviewPolicyV011,
    LifecycleDecisionReviewSubmissionV011,
    record_digest,
)


def compute_artifact(
    review: LifecycleDecisionReviewSubmissionV011,
    evidence: LifecycleDecisionReviewEvidenceV011,
    policy: LifecycleDecisionReviewPolicyV011,
    source_request: LifecycleBoundedRequestSubmissionV010,
    source_evidence: LifecycleBoundedRequestEvidenceV010,
    source_policy: LifecycleBoundedRequestPolicyV010,
    source_record: LifecycleBoundedRequestArtifactV010,
    *source_args: Any,
) -> LifecycleDecisionReviewArtifactV011:
    checks, expected_digests = evaluate(
        review,
        evidence,
        policy,
        source_request,
        source_evidence,
        source_policy,
        source_record,
        tuple(source_args),
    )
    if not all(checks[name] for name in STRUCTURAL_CHECKS):
        status = REJECTED
        reason = "source_review_policy_or_binding_invalid"
    else:
        failed = next((name for name in BLOCKING_CHECKS if not checks[name]), None)
        if failed is None:
            status = CLEAR
            reason = "clear_for_separate_authorization_decision_only"
        else:
            status = BLOCKED
            reason = failed
    record_issued = status != REJECTED
    clear = status == CLEAR
    artifact = LifecycleDecisionReviewArtifactV011(
        decision_review_id=review.decision_review_id,
        status=status,
        reason=reason,
        decision_reviewer_id=review.decision_reviewer_id,
        decision_reviewer_organization_id=review.decision_reviewer_organization_id,
        subject_id=review.subject_id,
        source_bounded_request_id=review.source_bounded_request_id,
        requester_id=review.requester_id,
        authorization_decision_maker_id=review.authorization_decision_maker_id,
        future_operator_id=review.future_operator_id,
        policy_digest=policy.policy_digest,
        review_digest=review.review_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        review_record_issued=record_issued,
        review_completed=record_issued,
        clear_for_authorization_decision=clear,
        authorization_decision_required_next=clear,
        authorization_decision_made=False,
        operation_approved=False,
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


def verify_artifact(*args: Any, **kwargs: Any) -> LifecycleDecisionReviewArtifactV011:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError(f"lifecycle_decision_review_record_invalid:{issues[0]}")
    return artifact


def artifact_issues(
    artifact: LifecycleDecisionReviewArtifactV011,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues: list[str] = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("decision_review_recomputation_mismatch")
    if artifact.status not in (CLEAR, BLOCKED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == CLEAR and not (
        artifact.review_record_issued
        and artifact.review_completed
        and artifact.clear_for_authorization_decision
        and artifact.authorization_decision_required_next
    ):
        issues.append("clear_gate_invalid")
    if artifact.status == BLOCKED and (
        not artifact.review_record_issued
        or not artifact.review_completed
        or artifact.clear_for_authorization_decision
        or artifact.authorization_decision_required_next
    ):
        issues.append("blocked_advanced")
    if artifact.status == REJECTED and (
        artifact.review_record_issued
        or artifact.review_completed
        or artifact.clear_for_authorization_decision
        or artifact.authorization_decision_required_next
    ):
        issues.append("rejected_record_issued")
    later_effects = (
        artifact.authorization_decision_made,
        artifact.operation_approved,
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
        issues.append("later_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
