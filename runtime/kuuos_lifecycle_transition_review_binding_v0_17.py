from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import (
    LifecyclePostOperationReviewArtifactV016,
    LifecyclePostOperationReviewEvidenceV016,
    LifecyclePostOperationReviewPolicyV016,
    LifecyclePostOperationReviewSubmissionV016,
)
from runtime.kuuos_lifecycle_transition_review_source_v0_17 import (
    all_source_digests,
    expected_transition_review_route_digest,
)
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import (
    OBJECTIVE,
    LifecycleTransitionReviewEvidenceV017,
    LifecycleTransitionReviewSubmissionV017,
    evidence_digest,
    submission_digest,
)

SEQUENCE_FIELDS = (
    "operation_scope_items",
    "target_resource_ids",
    "protected_resource_ids",
    "reversible_step_ids",
)
SOURCE_COPY = {
    "reviewed_scope_digest": "approved_scope_digest",
    "operation_scope_items": "operation_scope_items",
    "target_resource_ids": "target_resource_ids",
    "protected_resource_ids": "protected_resource_ids",
    "reversible_step_ids": "reversible_step_ids",
    "step_result_digests": "step_result_digests",
    "operation_execution_result_digest": "source_operation_execution_result_digest",
    "target_resource_post_state_digest": "source_target_resource_post_state_digest",
}
REQUIRED_EVIDENCE_FIELDS = (
    "evidence_id",
    "transition_review_id",
    "transition_reviewer_id",
    "transition_reviewer_organization_id",
    "transition_reviewer_mandate_receipt_digest",
    "transition_reviewer_qualification_receipt_digest",
    "transition_reviewer_identity_confirmation_digest",
    "conflict_disclosure_digest",
    "jurisdiction_receipt_digest",
    "review_readiness_receipt_digest",
    "source_post_operation_review_id",
    "source_post_operation_review_record_digest",
    "source_post_operation_reviewer_id",
    "source_post_operation_reviewer_organization_id",
    "source_completion_reviewer_id",
    "source_operator_id",
    "source_operation_approver_id",
    "source_authorization_decision_maker_id",
    "source_decision_reviewer_id",
    "subject_id",
    "subject_kind",
    "subject_version",
    "requester_id",
    "transition_decision_maker_id",
    "transition_review_route_digest",
    "reviewed_scope_digest",
    "operation_execution_result_digest",
    "target_resource_post_state_digest",
    "proposed_transition_kind",
    "current_lifecycle_state_digest",
    "proposed_target_state_digest",
    "transition_basis_digest",
    "necessity_assessment_digest",
    "proportionality_assessment_digest",
    "reversibility_assessment_digest",
    "dependency_clearance_digest",
    "authority_continuity_digest",
    "transition_state_compatibility_digest",
    "stakeholder_impact_assessment_digest",
    "legal_policy_compliance_digest",
    "appeal_route_digest",
    "dissent_route_digest",
    "minority_opinion_digest",
)


def make_evidence(
    source_review: LifecyclePostOperationReviewSubmissionV016,
    source_evidence: LifecyclePostOperationReviewEvidenceV016,
    source_policy: LifecyclePostOperationReviewPolicyV016,
    source_record: LifecyclePostOperationReviewArtifactV016,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> LifecycleTransitionReviewEvidenceV017:
    values = {
        target: getattr(source_evidence, source)
        for target, source in SOURCE_COPY.items()
    }
    values.update(
        source_post_operation_review_id=source_review.post_operation_review_id,
        source_post_operation_review_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(
            source_review,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        source_post_operation_reviewer_id=source_review.post_operation_reviewer_id,
        source_post_operation_reviewer_organization_id=(
            source_evidence.post_operation_reviewer_organization_id
        ),
        source_completion_reviewer_id=source_review.source_completion_reviewer_id,
        source_operator_id=source_review.source_operator_id,
        source_operation_approver_id=source_review.source_operation_approver_id,
        source_authorization_decision_maker_id=(
            source_review.source_authorization_decision_maker_id
        ),
        source_decision_reviewer_id=source_review.source_decision_reviewer_id,
        subject_id=source_review.subject_id,
        subject_kind=source_review.subject_kind,
        subject_version=source_review.subject_version,
        requester_id=source_review.requester_id,
    )
    values.update(overrides)
    if "transition_review_route_digest" not in values:
        values["transition_review_route_digest"] = (
            expected_transition_review_route_digest(
                source_review,
                source_evidence,
                source_record,
                transition_decision_maker_id=values["transition_decision_maker_id"],
                proposed_transition_kind=values["proposed_transition_kind"],
                proposed_target_state_digest=values["proposed_target_state_digest"],
                transition_decision_deadline_at_epoch_seconds=(
                    values["transition_decision_deadline_at_epoch_seconds"]
                ),
            )
        )
    for name in SEQUENCE_FIELDS:
        values[name] = canon(tuple(values[name]))
    values["step_result_digests"] = dict(
        sorted(dict(values["step_result_digests"]).items())
    )
    value = LifecycleTransitionReviewEvidenceV017(
        evidence_digest="", **values
    )
    value = replace(value, evidence_digest=evidence_digest(value))
    issues = evidence_issues(value)
    if issues:
        raise ValueError(f"lifecycle_transition_review_evidence_invalid:{issues[0]}")
    return value


def evidence_issues(
    value: LifecycleTransitionReviewEvidenceV017,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not all(getattr(value, name) for name in REQUIRED_EVIDENCE_FIELDS):
        issues.append("required_identity_receipt_or_binding_missing")
    if not value.source_artifact_digests:
        issues.append("source_digests_missing")
    if not value.step_result_digests:
        issues.append("step_result_digests_missing")
    if value.step_result_digests != dict(sorted(value.step_result_digests.items())):
        issues.append("step_result_digests_not_canonical")
    for name in SEQUENCE_FIELDS:
        if not getattr(value, name) or getattr(value, name) != canon(getattr(value, name)):
            issues.append(f"{name}_invalid")
    times = (
        value.review_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.reviewed_at_epoch_seconds,
        value.review_expiry_at_epoch_seconds,
        value.transition_decision_deadline_at_epoch_seconds,
    )
    if min(times) < 0:
        issues.append("negative_review_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_submission(
    transition_review_id: str,
    transition_reviewer_id: str,
    transition_reviewer_organization_id: str,
    review_requested_at_epoch_seconds: int,
    reviewed_at_epoch_seconds: int,
    review_expiry_at_epoch_seconds: int,
    source_review: LifecyclePostOperationReviewSubmissionV016,
    source_record: LifecyclePostOperationReviewArtifactV016,
    review_evidence: LifecycleTransitionReviewEvidenceV017,
    *,
    transition_decision_maker_id: str,
    proposed_transition_kind: str,
    proposed_target_state_digest: str,
    transition_review_route_digest: str,
    transition_decision_deadline_at_epoch_seconds: int,
    objective: str = OBJECTIVE,
) -> LifecycleTransitionReviewSubmissionV017:
    value = LifecycleTransitionReviewSubmissionV017(
        transition_review_id=transition_review_id,
        transition_reviewer_id=transition_reviewer_id,
        transition_reviewer_organization_id=transition_reviewer_organization_id,
        objective=objective,
        review_requested_at_epoch_seconds=review_requested_at_epoch_seconds,
        reviewed_at_epoch_seconds=reviewed_at_epoch_seconds,
        review_expiry_at_epoch_seconds=review_expiry_at_epoch_seconds,
        source_post_operation_review_id=source_review.post_operation_review_id,
        source_post_operation_review_record_digest=source_record.record_digest,
        subject_id=source_review.subject_id,
        subject_kind=source_review.subject_kind,
        subject_version=source_review.subject_version,
        transition_review_evidence_digest=review_evidence.evidence_digest,
        requester_id=source_review.requester_id,
        source_post_operation_reviewer_id=source_review.post_operation_reviewer_id,
        source_completion_reviewer_id=source_review.source_completion_reviewer_id,
        source_operator_id=source_review.source_operator_id,
        source_operation_approver_id=source_review.source_operation_approver_id,
        source_authorization_decision_maker_id=(
            source_review.source_authorization_decision_maker_id
        ),
        source_decision_reviewer_id=source_review.source_decision_reviewer_id,
        transition_decision_maker_id=transition_decision_maker_id,
        proposed_transition_kind=proposed_transition_kind,
        proposed_target_state_digest=proposed_target_state_digest,
        transition_review_route_digest=transition_review_route_digest,
        transition_decision_deadline_at_epoch_seconds=(
            transition_decision_deadline_at_epoch_seconds
        ),
        review_digest="",
    )
    value = replace(value, review_digest=submission_digest(value))
    issues = submission_issues(value)
    if issues:
        raise ValueError(f"lifecycle_transition_review_invalid:{issues[0]}")
    return value


def submission_issues(
    value: LifecycleTransitionReviewSubmissionV017,
) -> tuple[str, ...]:
    issues: list[str] = []
    payload = value.to_dict()
    for name in (
        "review_requested_at_epoch_seconds",
        "reviewed_at_epoch_seconds",
        "review_expiry_at_epoch_seconds",
        "transition_decision_deadline_at_epoch_seconds",
        "review_digest",
        "version",
    ):
        payload.pop(name, None)
    if not all(payload.values()):
        issues.append("required_review_field_missing")
    if min(
        value.review_requested_at_epoch_seconds,
        value.reviewed_at_epoch_seconds,
        value.review_expiry_at_epoch_seconds,
        value.transition_decision_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_review_time")
    if value.review_digest != submission_digest(value):
        issues.append("review_digest_mismatch")
    return tuple(issues)


def scope_matches(
    evidence: LifecycleTransitionReviewEvidenceV017,
    source: LifecyclePostOperationReviewEvidenceV016,
) -> bool:
    for target, source_name in SOURCE_COPY.items():
        left = getattr(evidence, target)
        right = getattr(source, source_name)
        if target in SEQUENCE_FIELDS:
            right = canon(tuple(right))
        elif target == "step_result_digests":
            right = dict(sorted(dict(right).items()))
        if left != right:
            return False
    return True
