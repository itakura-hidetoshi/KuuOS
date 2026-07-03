from __future__ import annotations

from dataclasses import fields, replace
from typing import Any

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    LifecycleDecisionReviewArtifactV011,
    LifecycleDecisionReviewEvidenceV011,
    LifecycleDecisionReviewPolicyV011,
    LifecycleDecisionReviewSubmissionV011,
)
from runtime.kuuos_lifecycle_authorization_decision_source_v0_12 import (
    all_source_digests,
)
from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    OBJECTIVE,
    LifecycleAuthorizationDecisionEvidenceV012,
    LifecycleAuthorizationDecisionSubmissionV012,
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
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_evidence: LifecycleDecisionReviewEvidenceV011,
    source_policy: LifecycleDecisionReviewPolicyV011,
    source_record: LifecycleDecisionReviewArtifactV011,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> LifecycleAuthorizationDecisionEvidenceV012:
    values = {
        "source_decision_review_id": source_review.decision_review_id,
        "source_decision_review_record_digest": source_record.record_digest,
        "source_artifact_digests": all_source_digests(
            source_review,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        "source_decision_reviewer_id": source_review.decision_reviewer_id,
        "authorization_decision_maker_id": (
            source_review.authorization_decision_maker_id
        ),
        "subject_id": source_review.subject_id,
        "subject_kind": source_review.subject_kind,
        "subject_version": source_review.subject_version,
        "requester_id": source_review.requester_id,
        "future_operator_id": source_review.future_operator_id,
        "authorized_scope_digest": source_evidence.reviewed_scope_digest,
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
        "evidence_capture_plan_digest": (
            source_evidence.evidence_capture_plan_digest
        ),
        "evidence_capture_plan_complete": (
            source_evidence.evidence_capture_plan_complete
        ),
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
        "minority_opinion_digest": source_evidence.minority_opinion_digest,
        "minority_opinion_recorded": source_evidence.minority_opinion_recorded,
    }
    values.update(overrides)
    for name in SEQUENCE_FIELDS:
        values[name] = canon(tuple(values[name]))
    value = LifecycleAuthorizationDecisionEvidenceV012(
        evidence_digest="",
        **values,
    )
    value = replace(value, evidence_digest=evidence_digest(value))
    issues = evidence_issues(value)
    if issues:
        raise ValueError(
            f"lifecycle_authorization_decision_evidence_invalid:{issues[0]}"
        )
    return value


def evidence_issues(
    value: LifecycleAuthorizationDecisionEvidenceV012,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        value.evidence_id,
        value.authorization_decision_id,
        value.authorization_decision_maker_id,
        value.authorization_decision_maker_organization_id,
        value.decision_maker_mandate_receipt_digest,
        value.decision_maker_qualification_receipt_digest,
        value.decision_maker_independence_declaration_digest,
        value.conflict_disclosure_digest,
        value.jurisdiction_receipt_digest,
        value.quorum_receipt_digest,
        value.decision_rationale_digest,
        value.proportionality_review_digest,
        value.alternatives_review_digest,
        value.irreversibility_review_digest,
        value.human_impact_review_digest,
        value.source_decision_review_id,
        value.source_decision_review_record_digest,
        value.source_decision_reviewer_id,
        value.subject_id,
        value.subject_kind,
        value.subject_version,
        value.requester_id,
        value.future_operator_id,
        value.authorized_scope_digest,
        value.rollback_plan_digest,
        value.recovery_route_digest,
        value.stop_condition_digest,
        value.abort_channel_digest,
        value.human_oversight_digest,
        value.monitoring_plan_digest,
        value.evidence_capture_plan_digest,
        value.simulation_receipt_digest,
        value.operation_approval_route_digest,
        value.appeal_route_digest,
        value.dissent_route_digest,
        value.minority_opinion_digest,
    )
    if not all(required):
        issues.append("required_identity_receipt_or_binding_missing")
    if not value.source_artifact_digests:
        issues.append("source_digests_missing")
    if min(
        value.decision_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.completed_at_epoch_seconds,
        value.authorization_decision_expiry_at_epoch_seconds,
        value.operation_approval_deadline_at_epoch_seconds,
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
    authorization_decision_id: str,
    authorization_decision_maker_id: str,
    authorization_decision_maker_organization_id: str,
    decision_requested_at_epoch_seconds: int,
    completed_at_epoch_seconds: int,
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_record: LifecycleDecisionReviewArtifactV011,
    decision_evidence: LifecycleAuthorizationDecisionEvidenceV012,
    *,
    operation_approval_route_digest: str,
    operation_approval_deadline_at_epoch_seconds: int,
    objective: str = OBJECTIVE,
) -> LifecycleAuthorizationDecisionSubmissionV012:
    value = LifecycleAuthorizationDecisionSubmissionV012(
        authorization_decision_id=authorization_decision_id,
        authorization_decision_maker_id=authorization_decision_maker_id,
        authorization_decision_maker_organization_id=(
            authorization_decision_maker_organization_id
        ),
        objective=objective,
        decision_requested_at_epoch_seconds=decision_requested_at_epoch_seconds,
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        source_decision_review_id=source_review.decision_review_id,
        source_decision_review_record_digest=source_record.record_digest,
        subject_id=source_review.subject_id,
        subject_kind=source_review.subject_kind,
        subject_version=source_review.subject_version,
        decision_evidence_digest=decision_evidence.evidence_digest,
        requester_id=source_review.requester_id,
        source_decision_reviewer_id=source_review.decision_reviewer_id,
        future_operator_id=source_review.future_operator_id,
        operation_approval_route_digest=operation_approval_route_digest,
        operation_approval_deadline_at_epoch_seconds=(
            operation_approval_deadline_at_epoch_seconds
        ),
        decision_digest="",
    )
    value = replace(value, decision_digest=submission_digest(value))
    issues = submission_issues(value)
    if issues:
        raise ValueError(
            f"lifecycle_authorization_decision_invalid:{issues[0]}"
        )
    return value


def submission_issues(
    value: LifecycleAuthorizationDecisionSubmissionV012,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name not in {
            "decision_digest",
            "version",
            "decision_requested_at_epoch_seconds",
            "completed_at_epoch_seconds",
            "operation_approval_deadline_at_epoch_seconds",
        }
    )
    if not all(required):
        issues.append("required_decision_field_missing")
    if min(
        value.decision_requested_at_epoch_seconds,
        value.completed_at_epoch_seconds,
        value.operation_approval_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_decision_time")
    if value.decision_digest != submission_digest(value):
        issues.append("decision_digest_mismatch")
    return tuple(issues)


def scope_matches(
    evidence: LifecycleAuthorizationDecisionEvidenceV012,
    source: LifecycleDecisionReviewEvidenceV011,
) -> bool:
    pairs = (
        ("authorized_scope_digest", "reviewed_scope_digest"),
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
