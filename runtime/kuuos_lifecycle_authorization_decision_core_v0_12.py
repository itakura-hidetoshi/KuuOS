from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    LifecycleDecisionReviewArtifactV011,
    LifecycleDecisionReviewEvidenceV011,
    LifecycleDecisionReviewPolicyV011,
    LifecycleDecisionReviewSubmissionV011,
)
from runtime.kuuos_lifecycle_authorization_decision_evaluation_v0_12 import (
    DENIAL_CHECKS,
    STRUCTURAL_CHECKS,
    evaluate,
)
from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    APPROVED,
    DENIED,
    REJECTED,
    LifecycleAuthorizationDecisionArtifactV012,
    LifecycleAuthorizationDecisionEvidenceV012,
    LifecycleAuthorizationDecisionPolicyV012,
    LifecycleAuthorizationDecisionSubmissionV012,
    record_digest,
)

SOURCE_ORDER_CHECK = "source_review_completed_before_decision_request"


def compute_artifact(
    decision: LifecycleAuthorizationDecisionSubmissionV012,
    evidence: LifecycleAuthorizationDecisionEvidenceV012,
    policy: LifecycleAuthorizationDecisionPolicyV012,
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_evidence: LifecycleDecisionReviewEvidenceV011,
    source_policy: LifecycleDecisionReviewPolicyV011,
    source_record: LifecycleDecisionReviewArtifactV011,
    *source_args: Any,
) -> LifecycleAuthorizationDecisionArtifactV012:
    checks, expected_digests = evaluate(
        decision,
        evidence,
        policy,
        source_review,
        source_evidence,
        source_policy,
        source_record,
        tuple(source_args),
    )
    checks[SOURCE_ORDER_CHECK] = (
        source_review.completed_at_epoch_seconds
        <= decision.decision_requested_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(
        checks[name] for name in STRUCTURAL_CHECKS
    ):
        status = REJECTED
        reason = "source_decision_policy_or_binding_invalid"
    else:
        failed = next(
            (name for name in DENIAL_CHECKS if not checks[name]),
            None,
        )
        if failed is None:
            status = APPROVED
            reason = "approved_for_separate_operation_approval_only"
        else:
            status = DENIED
            reason = failed
    record_issued = status != REJECTED
    decision_made = status != REJECTED
    approved = status == APPROVED
    denied = status == DENIED
    artifact = LifecycleAuthorizationDecisionArtifactV012(
        authorization_decision_id=decision.authorization_decision_id,
        status=status,
        reason=reason,
        authorization_decision_maker_id=(
            decision.authorization_decision_maker_id
        ),
        authorization_decision_maker_organization_id=(
            decision.authorization_decision_maker_organization_id
        ),
        source_decision_review_id=decision.source_decision_review_id,
        source_decision_reviewer_id=decision.source_decision_reviewer_id,
        subject_id=decision.subject_id,
        requester_id=decision.requester_id,
        future_operator_id=decision.future_operator_id,
        policy_digest=policy.policy_digest,
        decision_digest=decision.decision_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        authorization_decision_record_issued=record_issued,
        authorization_decision_made=decision_made,
        authorization_approved=approved,
        authorization_denied=denied,
        operation_approval_required_next=approved,
        operation_approval_route_required_next=approved,
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


def verify_artifact(*args: Any, **kwargs: Any) -> LifecycleAuthorizationDecisionArtifactV012:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError(
            f"lifecycle_authorization_decision_record_invalid:{issues[0]}"
        )
    return artifact


def artifact_issues(
    artifact: LifecycleAuthorizationDecisionArtifactV012,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues: list[str] = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("authorization_decision_recomputation_mismatch")
    if artifact.status not in (APPROVED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == APPROVED and not (
        artifact.authorization_decision_record_issued
        and artifact.authorization_decision_made
        and artifact.authorization_approved
        and not artifact.authorization_denied
        and artifact.operation_approval_required_next
        and artifact.operation_approval_route_required_next
    ):
        issues.append("approved_gate_invalid")
    if artifact.status == DENIED and (
        not artifact.authorization_decision_record_issued
        or not artifact.authorization_decision_made
        or artifact.authorization_approved
        or not artifact.authorization_denied
        or artifact.operation_approval_required_next
        or artifact.operation_approval_route_required_next
    ):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and (
        artifact.authorization_decision_record_issued
        or artifact.authorization_decision_made
        or artifact.authorization_approved
        or artifact.authorization_denied
        or artifact.operation_approval_required_next
        or artifact.operation_approval_route_required_next
    ):
        issues.append("rejected_record_issued")
    later_effects = (
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
        issues.append("operation_or_lifecycle_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
