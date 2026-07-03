from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_transition_preparation_evaluation_v0_19 import (
    BLOCKING_CHECKS,
    STRUCTURAL_CHECKS,
    evaluate,
)
from runtime.kuuos_lifecycle_transition_preparation_types_v0_19 import (
    BLOCKED,
    PREPARED,
    REJECTED,
    LifecycleTransitionPreparationArtifactV019,
    LifecycleTransitionPreparationEvidenceV019,
    LifecycleTransitionPreparationPolicyV019,
    LifecycleTransitionPreparationSubmissionV019,
    record_digest,
)
from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import (
    LifecycleTransitionDecisionArtifactV018,
    LifecycleTransitionDecisionEvidenceV018,
    LifecycleTransitionDecisionPolicyV018,
    LifecycleTransitionDecisionSubmissionV018,
)

SOURCE_ORDER_CHECK = "source_decision_precedes_preparation_and_deadline_valid"


def compute_artifact(
    preparation: LifecycleTransitionPreparationSubmissionV019,
    evidence: LifecycleTransitionPreparationEvidenceV019,
    policy: LifecycleTransitionPreparationPolicyV019,
    source_decision: LifecycleTransitionDecisionSubmissionV018,
    source_evidence: LifecycleTransitionDecisionEvidenceV018,
    source_policy: LifecycleTransitionDecisionPolicyV018,
    source_record: LifecycleTransitionDecisionArtifactV018,
    *source_args: Any,
) -> LifecycleTransitionPreparationArtifactV019:
    checks, expected_digests = evaluate(
        preparation,
        evidence,
        policy,
        source_decision,
        source_evidence,
        source_policy,
        source_record,
        tuple(source_args),
    )
    checks[SOURCE_ORDER_CHECK] = (
        source_decision.decided_at_epoch_seconds
        <= preparation.preparation_requested_at_epoch_seconds
        <= preparation.prepared_at_epoch_seconds
        <= source_decision.transition_preparation_deadline_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(
        checks[name] for name in STRUCTURAL_CHECKS
    ):
        status = REJECTED
        reason = "source_decision_package_policy_or_binding_invalid"
    else:
        failed = next(
            (name for name in BLOCKING_CHECKS if not checks[name]),
            None,
        )
        if failed is None:
            status = PREPARED
            reason = "ready_for_separate_transition_approval_only"
        else:
            status = BLOCKED
            reason = failed
    issued = status != REJECTED
    completed = status != REJECTED
    prepared = status == PREPARED
    blocked = status == BLOCKED
    artifact = LifecycleTransitionPreparationArtifactV019(
        transition_preparation_id=preparation.transition_preparation_id,
        status=status,
        reason=reason,
        transition_preparer_id=preparation.transition_preparer_id,
        transition_preparer_organization_id=(
            preparation.transition_preparer_organization_id
        ),
        source_transition_decision_id=preparation.source_transition_decision_id,
        source_transition_decision_maker_id=(
            preparation.source_transition_decision_maker_id
        ),
        transition_approver_id=preparation.transition_approver_id,
        future_transition_operator_id=preparation.future_transition_operator_id,
        transition_package_digest=preparation.transition_package_digest,
        expected_current_lifecycle_state_digest=(
            preparation.expected_current_lifecycle_state_digest
        ),
        proposed_target_lifecycle_state_digest=(
            preparation.proposed_target_lifecycle_state_digest
        ),
        transition_approval_route_digest=(
            preparation.transition_approval_route_digest
        ),
        subject_id=preparation.subject_id,
        requester_id=preparation.requester_id,
        policy_digest=policy.policy_digest,
        preparation_digest=preparation.preparation_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_transition_decision_approved=(
            source_record.transition_approved_for_preparation
        ),
        transition_preparation_record_issued=issued,
        transition_preparation_completed=completed,
        transition_package_prepared=prepared,
        ready_for_separate_transition_approval=prepared,
        transition_preparation_blocked=blocked,
        transition_approval_required_next=prepared,
        transition_approval_route_required_next=prepared,
        transition_repreparation_required_next=blocked,
        transition_repreparation_route_required_next=blocked,
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


def verify_artifact(*args: Any, **kwargs: Any) -> LifecycleTransitionPreparationArtifactV019:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError(
            f"lifecycle_transition_preparation_record_invalid:{issues[0]}"
        )
    return artifact


def artifact_issues(
    artifact: LifecycleTransitionPreparationArtifactV019,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues: list[str] = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("transition_preparation_recomputation_mismatch")
    if artifact.status not in (PREPARED, BLOCKED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == PREPARED and not all(
        (
            artifact.source_transition_decision_approved,
            artifact.transition_preparation_record_issued,
            artifact.transition_preparation_completed,
            artifact.transition_package_prepared,
            artifact.ready_for_separate_transition_approval,
            not artifact.transition_preparation_blocked,
            artifact.transition_approval_required_next,
            artifact.transition_approval_route_required_next,
            not artifact.transition_repreparation_required_next,
            not artifact.transition_repreparation_route_required_next,
        )
    ):
        issues.append("prepared_gate_invalid")
    if artifact.status == BLOCKED and not all(
        (
            artifact.source_transition_decision_approved,
            artifact.transition_preparation_record_issued,
            artifact.transition_preparation_completed,
            not artifact.transition_package_prepared,
            not artifact.ready_for_separate_transition_approval,
            artifact.transition_preparation_blocked,
            not artifact.transition_approval_required_next,
            not artifact.transition_approval_route_required_next,
            artifact.transition_repreparation_required_next,
            artifact.transition_repreparation_route_required_next,
        )
    ):
        issues.append("blocked_gate_invalid")
    if artifact.status == REJECTED and any(
        (
            artifact.transition_preparation_record_issued,
            artifact.transition_preparation_completed,
            artifact.transition_package_prepared,
            artifact.ready_for_separate_transition_approval,
            artifact.transition_preparation_blocked,
            artifact.transition_approval_required_next,
            artifact.transition_approval_route_required_next,
            artifact.transition_repreparation_required_next,
            artifact.transition_repreparation_route_required_next,
        )
    ):
        issues.append("rejected_record_issued")
    later_effects = (
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
