from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_transition_decision_evaluation_v0_18 import (
    DENIAL_CHECKS,
    STRUCTURAL_CHECKS,
    evaluate,
)
from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import (
    APPROVED,
    DENIED,
    REJECTED,
    LifecycleTransitionDecisionArtifactV018,
    LifecycleTransitionDecisionEvidenceV018,
    LifecycleTransitionDecisionPolicyV018,
    LifecycleTransitionDecisionSubmissionV018,
    record_digest,
)
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import (
    LifecycleTransitionReviewArtifactV017,
    LifecycleTransitionReviewEvidenceV017,
    LifecycleTransitionReviewPolicyV017,
    LifecycleTransitionReviewSubmissionV017,
)

SOURCE_ORDER_CHECK = "source_transition_review_and_decision_deadline_valid"


def compute_artifact(
    decision: LifecycleTransitionDecisionSubmissionV018,
    evidence: LifecycleTransitionDecisionEvidenceV018,
    policy: LifecycleTransitionDecisionPolicyV018,
    source_review: LifecycleTransitionReviewSubmissionV017,
    source_evidence: LifecycleTransitionReviewEvidenceV017,
    source_policy: LifecycleTransitionReviewPolicyV017,
    source_record: LifecycleTransitionReviewArtifactV017,
    *source_args: Any,
) -> LifecycleTransitionDecisionArtifactV018:
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
        source_review.reviewed_at_epoch_seconds
        <= decision.decision_requested_at_epoch_seconds
        <= decision.decided_at_epoch_seconds
        <= source_review.transition_decision_deadline_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(
        checks[name] for name in STRUCTURAL_CHECKS
    ):
        status = REJECTED
        reason = "source_transition_review_state_policy_or_binding_invalid"
    else:
        failed = next((name for name in DENIAL_CHECKS if not checks[name]), None)
        if failed is None:
            status = APPROVED
            reason = "approved_for_separate_transition_preparation_only"
        else:
            status = DENIED
            reason = failed
    record_issued = status != REJECTED
    decision_made = status != REJECTED
    approved = status == APPROVED
    denied = status == DENIED
    artifact = LifecycleTransitionDecisionArtifactV018(
        transition_decision_id=decision.transition_decision_id,
        status=status,
        reason=reason,
        transition_decision_maker_id=decision.transition_decision_maker_id,
        transition_decision_maker_organization_id=(
            decision.transition_decision_maker_organization_id
        ),
        source_transition_review_id=decision.source_transition_review_id,
        source_transition_reviewer_id=decision.source_transition_reviewer_id,
        transition_preparer_id=decision.transition_preparer_id,
        proposed_transition_kind=decision.proposed_transition_kind,
        subject_id=decision.subject_id,
        requester_id=decision.requester_id,
        expected_current_lifecycle_state_digest=(
            decision.expected_current_lifecycle_state_digest
        ),
        proposed_target_lifecycle_state_digest=(
            decision.proposed_target_lifecycle_state_digest
        ),
        transition_rule_digest=evidence.transition_rule.rule_digest,
        transition_preparation_route_digest=(
            decision.transition_preparation_route_digest
        ),
        policy_digest=policy.policy_digest,
        decision_digest=decision.decision_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_transition_review_completed=source_record.transition_review_completed,
        transition_decision_record_issued=record_issued,
        transition_decision_made=decision_made,
        transition_approved_for_preparation=approved,
        transition_denied=denied,
        transition_preparation_required_next=approved,
        transition_preparation_route_required_next=approved,
        transition_appeal_or_reconsideration_available=denied,
        lifecycle_transition_prepared=False,
        lifecycle_transition_approved=False,
        lifecycle_transition_started=False,
        lifecycle_transition_completed=False,
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


def verify_artifact(*args: Any, **kwargs: Any) -> LifecycleTransitionDecisionArtifactV018:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError(f"lifecycle_transition_decision_record_invalid:{issues[0]}")
    return artifact


def artifact_issues(
    artifact: LifecycleTransitionDecisionArtifactV018,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues: list[str] = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("transition_decision_recomputation_mismatch")
    if artifact.status not in (APPROVED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == APPROVED and not all(
        (
            artifact.source_transition_review_completed,
            artifact.transition_decision_record_issued,
            artifact.transition_decision_made,
            artifact.transition_approved_for_preparation,
            not artifact.transition_denied,
            artifact.transition_preparation_required_next,
            artifact.transition_preparation_route_required_next,
            not artifact.transition_appeal_or_reconsideration_available,
        )
    ):
        issues.append("approved_gate_invalid")
    if artifact.status == DENIED and not all(
        (
            artifact.source_transition_review_completed,
            artifact.transition_decision_record_issued,
            artifact.transition_decision_made,
            not artifact.transition_approved_for_preparation,
            artifact.transition_denied,
            not artifact.transition_preparation_required_next,
            not artifact.transition_preparation_route_required_next,
            artifact.transition_appeal_or_reconsideration_available,
        )
    ):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and any(
        (
            artifact.transition_decision_record_issued,
            artifact.transition_decision_made,
            artifact.transition_approved_for_preparation,
            artifact.transition_denied,
            artifact.transition_preparation_required_next,
            artifact.transition_preparation_route_required_next,
            artifact.transition_appeal_or_reconsideration_available,
        )
    ):
        issues.append("rejected_record_issued")
    later_effects = (
        artifact.lifecycle_transition_prepared,
        artifact.lifecycle_transition_approved,
        artifact.lifecycle_transition_started,
        artifact.lifecycle_transition_completed,
        artifact.lifecycle_transition_performed,
        artifact.authority_changed,
        artifact.quiescence_state_changed,
        artifact.terminal_state_changed,
        artifact.terminal_marker_written,
        artifact.resource_removed,
        artifact.external_operation_performed,
        artifact.repository_changed,
    )
    if any(later_effects):
        issues.append("transition_or_repository_effect_performed")
    if not artifact.lifecycle_state_read_only or not artifact.repository_read_only:
        issues.append("read_only_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
