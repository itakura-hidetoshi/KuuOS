from __future__ import annotations

from dataclasses import fields, replace
from typing import Any

from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import (
    LifecycleBoundedRequestArtifactV010,
    LifecycleBoundedRequestEvidenceV010,
    LifecycleBoundedRequestPolicyV010,
    LifecycleBoundedRequestSubmissionV010,
)
from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_decision_review_source_v0_11 import all_source_digests
from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    OBJECTIVE,
    LifecycleDecisionReviewEvidenceV011,
    LifecycleDecisionReviewSubmissionV011,
    evidence_digest,
    submission_digest,
)

SEQUENCE_FIELDS = (
    "operation_scope_items",
    "target_resource_ids",
    "protected_resource_ids",
    "reversible_step_ids",
    "irreversible_step_ids",
)


def make_evidence(
    source_request: LifecycleBoundedRequestSubmissionV010,
    source_evidence: LifecycleBoundedRequestEvidenceV010,
    source_policy: LifecycleBoundedRequestPolicyV010,
    source_record: LifecycleBoundedRequestArtifactV010,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> LifecycleDecisionReviewEvidenceV011:
    values = {
        "subject_id": source_request.subject_id,
        "subject_kind": source_request.subject_kind,
        "subject_version": source_request.subject_version,
        "source_bounded_request_id": source_request.bounded_request_id,
        "source_bounded_request_record_digest": source_record.record_digest,
        "source_artifact_digests": all_source_digests(
            source_request, source_evidence, source_policy, source_record, source_args
        ),
        "requester_id": source_request.requester_id,
        "authorization_decision_maker_id": source_request.decision_authority_id,
        "future_operator_id": source_request.future_operator_id,
        "reviewed_scope_digest": source_evidence.operation_scope_digest,
        "operation_scope_items": source_evidence.operation_scope_items,
        "target_resource_ids": source_evidence.target_resource_ids,
        "protected_resource_ids": source_evidence.protected_resource_ids,
        "reversible_step_ids": source_evidence.reversible_step_ids,
        "irreversible_step_ids": source_evidence.irreversible_step_ids,
        "rollback_plan_digest": source_evidence.rollback_plan_digest,
        "rollback_plan_verified": source_evidence.rollback_plan_verified,
        "recovery_route_digest": source_evidence.recovery_route_digest,
        "recovery_route_verified": source_evidence.recovery_route_verified,
        "stop_condition_digest": source_evidence.stop_condition_digest,
        "stop_conditions_complete": source_evidence.stop_conditions_complete,
        "abort_channel_digest": source_evidence.abort_channel_digest,
        "abort_channel_available": source_evidence.abort_channel_available,
        "human_oversight_digest": source_evidence.human_oversight_digest,
        "human_oversight_available": source_evidence.human_oversight_available,
        "monitoring_plan_digest": source_evidence.monitoring_plan_digest,
        "monitoring_plan_complete": source_evidence.monitoring_plan_complete,
        "evidence_capture_plan_digest": source_evidence.evidence_capture_plan_digest,
        "evidence_capture_plan_complete": source_evidence.evidence_capture_plan_complete,
        "simulation_receipt_digest": source_evidence.simulation_receipt_digest,
        "simulation_verified": source_evidence.simulation_verified,
        "operation_window_seconds": source_evidence.operation_window_seconds,
        "protected_core_excluded": source_evidence.protected_core_excluded,
        "institutional_hold_active": source_evidence.institutional_hold_active,
        "emergency_state_active": source_evidence.emergency_state_active,
        "appeal_route_digest": source_evidence.appeal_route_digest,
        "appeal_route_available": source_evidence.appeal_route_available,
        "dissent_route_digest": source_evidence.dissent_route_digest,
        "dissent_route_available": source_evidence.dissent_route_available,
    }
    values.update(overrides)
    for name in SEQUENCE_FIELDS:
        values[name] = canon(tuple(values[name]))
    value = LifecycleDecisionReviewEvidenceV011(evidence_digest="", **values)
    value = replace(value, evidence_digest=evidence_digest(value))
    issues = evidence_issues(value)
    if issues:
        raise ValueError(f"lifecycle_decision_review_evidence_invalid:{issues[0]}")
    return value


def evidence_issues(value: LifecycleDecisionReviewEvidenceV011) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        value.evidence_id,
        value.decision_review_id,
        value.decision_reviewer_id,
        value.decision_reviewer_organization_id,
        value.reviewer_qualification_receipt_digest,
        value.reviewer_independence_declaration_digest,
        value.conflict_disclosure_digest,
        value.subject_id,
        value.subject_kind,
        value.subject_version,
        value.source_bounded_request_id,
        value.source_bounded_request_record_digest,
        value.requester_id,
        value.authorization_decision_maker_id,
        value.future_operator_id,
        value.reviewed_scope_digest,
        value.authorization_route_digest,
        value.appeal_route_digest,
        value.dissent_route_digest,
        value.minority_opinion_digest,
    )
    if not all(required):
        issues.append("required_identity_or_binding_missing")
    if not value.source_artifact_digests:
        issues.append("source_digests_missing")
    if min(
        value.review_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.completed_at_epoch_seconds,
        value.review_expiry_at_epoch_seconds,
        value.authorization_decision_deadline_at_epoch_seconds,
        value.operation_window_seconds,
    ) < 0:
        issues.append("negative_time_or_window")
    for name in SEQUENCE_FIELDS:
        if getattr(value, name) != canon(getattr(value, name)):
            issues.append(f"{name}_not_canonical")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_submission(
    decision_review_id: str,
    decision_reviewer_id: str,
    decision_reviewer_organization_id: str,
    review_requested_at_epoch_seconds: int,
    completed_at_epoch_seconds: int,
    source_request: LifecycleBoundedRequestSubmissionV010,
    source_record: LifecycleBoundedRequestArtifactV010,
    review_evidence: LifecycleDecisionReviewEvidenceV011,
    *,
    authorization_route_digest: str,
    authorization_decision_deadline_at_epoch_seconds: int,
    objective: str = OBJECTIVE,
) -> LifecycleDecisionReviewSubmissionV011:
    value = LifecycleDecisionReviewSubmissionV011(
        decision_review_id=decision_review_id,
        decision_reviewer_id=decision_reviewer_id,
        decision_reviewer_organization_id=decision_reviewer_organization_id,
        objective=objective,
        review_requested_at_epoch_seconds=review_requested_at_epoch_seconds,
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        source_bounded_request_id=source_request.bounded_request_id,
        source_bounded_request_record_digest=source_record.record_digest,
        subject_id=review_evidence.subject_id,
        subject_kind=review_evidence.subject_kind,
        subject_version=review_evidence.subject_version,
        review_evidence_digest=review_evidence.evidence_digest,
        requester_id=source_request.requester_id,
        authorization_decision_maker_id=source_request.decision_authority_id,
        future_operator_id=source_request.future_operator_id,
        authorization_route_digest=authorization_route_digest,
        authorization_decision_deadline_at_epoch_seconds=(
            authorization_decision_deadline_at_epoch_seconds
        ),
        review_digest="",
    )
    value = replace(value, review_digest=submission_digest(value))
    issues = submission_issues(value)
    if issues:
        raise ValueError(f"lifecycle_decision_review_invalid:{issues[0]}")
    return value


def submission_issues(value: LifecycleDecisionReviewSubmissionV011) -> tuple[str, ...]:
    issues: list[str] = []
    required = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name not in {
            "review_digest",
            "version",
            "review_requested_at_epoch_seconds",
            "completed_at_epoch_seconds",
            "authorization_decision_deadline_at_epoch_seconds",
        }
    )
    if not all(required):
        issues.append("required_review_field_missing")
    if min(
        value.review_requested_at_epoch_seconds,
        value.completed_at_epoch_seconds,
        value.authorization_decision_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_review_time")
    if value.review_digest != submission_digest(value):
        issues.append("review_digest_mismatch")
    return tuple(issues)


def scope_matches(
    evidence: LifecycleDecisionReviewEvidenceV011,
    source: LifecycleBoundedRequestEvidenceV010,
) -> bool:
    pairs = (
        ("reviewed_scope_digest", "operation_scope_digest"),
        ("operation_scope_items", "operation_scope_items"),
        ("target_resource_ids", "target_resource_ids"),
        ("protected_resource_ids", "protected_resource_ids"),
        ("reversible_step_ids", "reversible_step_ids"),
        ("irreversible_step_ids", "irreversible_step_ids"),
        ("rollback_plan_digest", "rollback_plan_digest"),
        ("recovery_route_digest", "recovery_route_digest"),
        ("stop_condition_digest", "stop_condition_digest"),
        ("abort_channel_digest", "abort_channel_digest"),
        ("human_oversight_digest", "human_oversight_digest"),
        ("monitoring_plan_digest", "monitoring_plan_digest"),
        ("evidence_capture_plan_digest", "evidence_capture_plan_digest"),
        ("simulation_receipt_digest", "simulation_receipt_digest"),
        ("operation_window_seconds", "operation_window_seconds"),
    )
    for target, source_name in pairs:
        left = getattr(evidence, target)
        right = getattr(source, source_name)
        if target in SEQUENCE_FIELDS:
            right = canon(tuple(right))
        if left != right:
            return False
    return True
