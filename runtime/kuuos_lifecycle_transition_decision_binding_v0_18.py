from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_transition_decision_source_v0_18 import (
    all_source_digests,
    expected_transition_preparation_route_digest,
)
from runtime.kuuos_lifecycle_transition_decision_state_v0_18 import (
    state_issues,
    transition_rule_issues,
)
from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import (
    OBJECTIVE,
    LifecycleStateV018,
    LifecycleTransitionDecisionEvidenceV018,
    LifecycleTransitionDecisionSubmissionV018,
    LifecycleTransitionRuleV018,
    evidence_digest,
    submission_digest,
)
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import (
    LifecycleTransitionReviewArtifactV017,
    LifecycleTransitionReviewEvidenceV017,
    LifecycleTransitionReviewPolicyV017,
    LifecycleTransitionReviewSubmissionV017,
)

REQUIRED_EVIDENCE_FIELDS = (
    "evidence_id",
    "transition_decision_id",
    "transition_decision_maker_id",
    "transition_decision_maker_organization_id",
    "decision_maker_mandate_receipt_digest",
    "decision_maker_qualification_receipt_digest",
    "decision_maker_identity_confirmation_digest",
    "conflict_disclosure_digest",
    "jurisdiction_receipt_digest",
    "decision_readiness_receipt_digest",
    "source_transition_review_id",
    "source_transition_review_record_digest",
    "source_transition_reviewer_id",
    "source_transition_reviewer_organization_id",
    "source_post_operation_reviewer_id",
    "source_completion_reviewer_id",
    "source_operator_id",
    "source_operation_approver_id",
    "source_authorization_decision_maker_id",
    "source_decision_reviewer_id",
    "subject_id",
    "subject_kind",
    "subject_version",
    "requester_id",
    "transition_preparer_id",
    "proposed_transition_kind",
    "transition_preparation_route_digest",
    "decision_rationale_digest",
    "denial_route_digest",
    "appeal_route_digest",
    "dissent_route_digest",
    "minority_opinion_digest",
)


def make_evidence(
    source_review: LifecycleTransitionReviewSubmissionV017,
    source_evidence: LifecycleTransitionReviewEvidenceV017,
    source_policy: LifecycleTransitionReviewPolicyV017,
    source_record: LifecycleTransitionReviewArtifactV017,
    source_args: tuple[Any, ...],
    *,
    current_state: LifecycleStateV018,
    target_state: LifecycleStateV018,
    transition_rule: LifecycleTransitionRuleV018,
    **overrides: Any,
) -> LifecycleTransitionDecisionEvidenceV018:
    values: dict[str, Any] = {
        "source_transition_review_id": source_review.transition_review_id,
        "source_transition_review_record_digest": source_record.record_digest,
        "source_artifact_digests": all_source_digests(
            source_review,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        "source_transition_reviewer_id": source_review.transition_reviewer_id,
        "source_transition_reviewer_organization_id": (
            source_evidence.transition_reviewer_organization_id
        ),
        "source_post_operation_reviewer_id": (
            source_review.source_post_operation_reviewer_id
        ),
        "source_completion_reviewer_id": source_review.source_completion_reviewer_id,
        "source_operator_id": source_review.source_operator_id,
        "source_operation_approver_id": source_review.source_operation_approver_id,
        "source_authorization_decision_maker_id": (
            source_review.source_authorization_decision_maker_id
        ),
        "source_decision_reviewer_id": source_review.source_decision_reviewer_id,
        "subject_id": source_review.subject_id,
        "subject_kind": source_review.subject_kind,
        "subject_version": source_review.subject_version,
        "requester_id": source_review.requester_id,
        "proposed_transition_kind": source_review.proposed_transition_kind,
        "current_state": current_state,
        "target_state": target_state,
        "transition_rule": transition_rule,
    }
    values.update(overrides)
    if "transition_preparation_route_digest" not in values:
        values["transition_preparation_route_digest"] = (
            expected_transition_preparation_route_digest(
                source_review,
                source_evidence,
                source_record,
                transition_preparer_id=values["transition_preparer_id"],
                expected_current_lifecycle_state_digest=current_state.state_digest,
                proposed_target_lifecycle_state_digest=target_state.state_digest,
                transition_rule_digest=transition_rule.rule_digest,
                transition_preparation_deadline_at_epoch_seconds=(
                    values["transition_preparation_deadline_at_epoch_seconds"]
                ),
            )
        )
    value = LifecycleTransitionDecisionEvidenceV018(
        evidence_digest="", **values
    )
    value = replace(value, evidence_digest=evidence_digest(value))
    issues = evidence_issues(value)
    if issues:
        raise ValueError(f"lifecycle_transition_decision_evidence_invalid:{issues[0]}")
    return value


def evidence_issues(
    value: LifecycleTransitionDecisionEvidenceV018,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not all(getattr(value, name) for name in REQUIRED_EVIDENCE_FIELDS):
        issues.append("required_identity_receipt_or_binding_missing")
    if not value.source_artifact_digests:
        issues.append("source_digests_missing")
    if state_issues(value.current_state):
        issues.append("current_state_invalid")
    if state_issues(value.target_state):
        issues.append("target_state_invalid")
    if transition_rule_issues(value.transition_rule):
        issues.append("transition_rule_invalid")
    times = (
        value.decision_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.decided_at_epoch_seconds,
        value.decision_expiry_at_epoch_seconds,
        value.transition_preparation_deadline_at_epoch_seconds,
    )
    if min(times) < 0:
        issues.append("negative_decision_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_submission(
    transition_decision_id: str,
    transition_decision_maker_id: str,
    transition_decision_maker_organization_id: str,
    decision_requested_at_epoch_seconds: int,
    decided_at_epoch_seconds: int,
    decision_expiry_at_epoch_seconds: int,
    source_review: LifecycleTransitionReviewSubmissionV017,
    source_record: LifecycleTransitionReviewArtifactV017,
    decision_evidence: LifecycleTransitionDecisionEvidenceV018,
    *,
    transition_preparer_id: str,
    transition_preparation_route_digest: str,
    transition_preparation_deadline_at_epoch_seconds: int,
    objective: str = OBJECTIVE,
) -> LifecycleTransitionDecisionSubmissionV018:
    value = LifecycleTransitionDecisionSubmissionV018(
        transition_decision_id=transition_decision_id,
        transition_decision_maker_id=transition_decision_maker_id,
        transition_decision_maker_organization_id=(
            transition_decision_maker_organization_id
        ),
        objective=objective,
        decision_requested_at_epoch_seconds=decision_requested_at_epoch_seconds,
        decided_at_epoch_seconds=decided_at_epoch_seconds,
        decision_expiry_at_epoch_seconds=decision_expiry_at_epoch_seconds,
        source_transition_review_id=source_review.transition_review_id,
        source_transition_review_record_digest=source_record.record_digest,
        subject_id=source_review.subject_id,
        subject_kind=source_review.subject_kind,
        subject_version=source_review.subject_version,
        transition_decision_evidence_digest=decision_evidence.evidence_digest,
        requester_id=source_review.requester_id,
        source_transition_reviewer_id=source_review.transition_reviewer_id,
        transition_preparer_id=transition_preparer_id,
        proposed_transition_kind=source_review.proposed_transition_kind,
        expected_current_lifecycle_state_digest=(
            decision_evidence.current_state.state_digest
        ),
        proposed_target_lifecycle_state_digest=(
            decision_evidence.target_state.state_digest
        ),
        transition_preparation_route_digest=transition_preparation_route_digest,
        transition_preparation_deadline_at_epoch_seconds=(
            transition_preparation_deadline_at_epoch_seconds
        ),
        decision_digest="",
    )
    value = replace(value, decision_digest=submission_digest(value))
    issues = submission_issues(value)
    if issues:
        raise ValueError(f"lifecycle_transition_decision_invalid:{issues[0]}")
    return value


def submission_issues(
    value: LifecycleTransitionDecisionSubmissionV018,
) -> tuple[str, ...]:
    issues: list[str] = []
    payload = value.to_dict()
    for name in (
        "decision_requested_at_epoch_seconds",
        "decided_at_epoch_seconds",
        "decision_expiry_at_epoch_seconds",
        "transition_preparation_deadline_at_epoch_seconds",
        "decision_digest",
        "version",
    ):
        payload.pop(name, None)
    if not all(payload.values()):
        issues.append("required_decision_field_missing")
    if min(
        value.decision_requested_at_epoch_seconds,
        value.decided_at_epoch_seconds,
        value.decision_expiry_at_epoch_seconds,
        value.transition_preparation_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_decision_time")
    if value.decision_digest != submission_digest(value):
        issues.append("decision_digest_mismatch")
    return tuple(issues)
