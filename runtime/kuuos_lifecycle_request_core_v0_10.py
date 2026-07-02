from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_review_types_v0_9 import (
    LifecycleReviewArtifactV09,
    LifecycleReviewEvidenceV09,
    LifecycleReviewPolicyV09,
    LifecycleReviewRequestV09,
)
from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import (
    BLOCKED,
    ISSUED,
    REJECTED,
    LifecycleBoundedRequestArtifactV010,
    LifecycleBoundedRequestEvidenceV010,
    LifecycleBoundedRequestPolicyV010,
    LifecycleBoundedRequestSubmissionV010,
    record_digest,
)
from runtime.kuuos_lifecycle_request_evaluation_v0_10 import (
    BLOCKING_CHECKS,
    STRUCTURAL_CHECKS,
    evaluate,
)


def compute_artifact(
    request: LifecycleBoundedRequestSubmissionV010,
    evidence: LifecycleBoundedRequestEvidenceV010,
    policy: LifecycleBoundedRequestPolicyV010,
    review_request: LifecycleReviewRequestV09,
    review_evidence: LifecycleReviewEvidenceV09,
    review_policy: LifecycleReviewPolicyV09,
    review_record: LifecycleReviewArtifactV09,
    *source_args: Any,
) -> LifecycleBoundedRequestArtifactV010:
    checks, expected_digests = evaluate(
        request,
        evidence,
        policy,
        review_request,
        review_evidence,
        review_policy,
        review_record,
        tuple(source_args),
    )
    if not all(checks[name] for name in STRUCTURAL_CHECKS):
        status = REJECTED
        reason = "source_request_policy_or_binding_invalid"
    else:
        failed = next((name for name in BLOCKING_CHECKS if not checks[name]), None)
        if failed is None:
            status = ISSUED
            reason = "request_issued_for_separate_decision_review_only"
        else:
            status = BLOCKED
            reason = failed

    record_issued = status != REJECTED
    request_issued = status == ISSUED
    artifact = LifecycleBoundedRequestArtifactV010(
        bounded_request_id=request.bounded_request_id,
        status=status,
        reason=reason,
        requester_id=request.requester_id,
        requester_organization_id=request.requester_organization_id,
        subject_id=request.subject_id,
        source_review_id=request.source_review_id,
        decision_authority_id=request.decision_authority_id,
        future_operator_id=request.future_operator_id,
        policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        request_record_issued=record_issued,
        bounded_request_issued=request_issued,
        ready_for_decision_review=request_issued,
        decision_review_required_next=request_issued,
        decision_made=False,
        operation_started=False,
        operation_completed=False,
        lifecycle_effect_performed=False,
        repository_change_performed=False,
        lifecycle_read_only=True,
        record_digest="",
    )
    return replace(artifact, record_digest=record_digest(artifact))


def verify_artifact(*args: Any, **kwargs: Any) -> LifecycleBoundedRequestArtifactV010:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError(f"lifecycle_request_record_invalid:{issues[0]}")
    return artifact


def artifact_issues(
    artifact: LifecycleBoundedRequestArtifactV010,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues: list[str] = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("request_recomputation_mismatch")
    if artifact.status not in (ISSUED, BLOCKED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == ISSUED and not (
        artifact.request_record_issued
        and artifact.bounded_request_issued
        and artifact.ready_for_decision_review
        and artifact.decision_review_required_next
    ):
        issues.append("issued_gate_invalid")
    if artifact.status == BLOCKED and (
        not artifact.request_record_issued
        or artifact.bounded_request_issued
        or artifact.ready_for_decision_review
        or artifact.decision_review_required_next
    ):
        issues.append("blocked_advanced")
    if artifact.status == REJECTED and (
        artifact.request_record_issued
        or artifact.bounded_request_issued
        or artifact.ready_for_decision_review
        or artifact.decision_review_required_next
    ):
        issues.append("rejected_record_issued")
    if (
        artifact.decision_made
        or artifact.operation_started
        or artifact.operation_completed
        or artifact.lifecycle_effect_performed
        or artifact.repository_change_performed
        or not artifact.lifecycle_read_only
    ):
        issues.append("later_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
