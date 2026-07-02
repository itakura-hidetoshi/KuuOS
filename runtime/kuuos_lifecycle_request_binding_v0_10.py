from __future__ import annotations

from dataclasses import fields, replace
from typing import Any

from runtime.kuuos_lifecycle_review_types_v0_9 import (
    LifecycleReviewArtifactV09,
    LifecycleReviewEvidenceV09,
    LifecycleReviewPolicyV09,
    LifecycleReviewRequestV09,
)
from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import (
    OBJECTIVE,
    LifecycleBoundedRequestEvidenceV010,
    LifecycleBoundedRequestSubmissionV010,
    evidence_digest,
    submission_digest,
)
from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_source_chain_v0_10 import (
    all_source_digests,
    source_authority,
    source_operator,
    source_scope,
)


_SEQUENCE_FIELDS = (
    "operation_scope_items",
    "target_resource_ids",
    "protected_resource_ids",
    "reversible_step_ids",
    "irreversible_step_ids",
)

_SCOPE_PAIRS = (
    ("operation_scope_digest", "scope_digest"),
    ("operation_scope_items", "scope_items"),
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
    ("operation_window_seconds", "window_seconds"),
)


def make_evidence(
    review_request: LifecycleReviewRequestV09,
    review_evidence: LifecycleReviewEvidenceV09,
    review_policy: LifecycleReviewPolicyV09,
    review_record: LifecycleReviewArtifactV09,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> LifecycleBoundedRequestEvidenceV010:
    values = {
        "subject_id": review_request.subject_id,
        "subject_kind": review_request.subject_kind,
        "subject_version": review_request.subject_version,
        "source_review_id": review_record.review_id,
        "source_review_record_digest": review_record.record_digest,
        "source_artifact_digests": all_source_digests(
            review_request,
            review_evidence,
            review_policy,
            review_record,
            source_args,
        ),
        "decision_authority_id": source_authority(review_record),
        "future_operator_id": source_operator(review_record),
        "operation_scope_digest": source_scope(review_evidence, "scope_digest"),
        "operation_scope_items": source_scope(review_evidence, "scope_items"),
        "target_resource_ids": review_evidence.target_resource_ids,
        "protected_resource_ids": review_evidence.protected_resource_ids,
        "reversible_step_ids": review_evidence.reversible_step_ids,
        "irreversible_step_ids": review_evidence.irreversible_step_ids,
        "rollback_plan_digest": review_evidence.rollback_plan_digest,
        "rollback_plan_verified": review_evidence.rollback_plan_verified,
        "recovery_route_digest": review_evidence.recovery_route_digest,
        "recovery_route_verified": review_evidence.recovery_route_verified,
        "stop_condition_digest": review_evidence.stop_condition_digest,
        "stop_conditions_complete": review_evidence.stop_conditions_complete,
        "abort_channel_digest": review_evidence.abort_channel_digest,
        "abort_channel_available": review_evidence.abort_channel_available,
        "human_oversight_digest": review_evidence.human_oversight_digest,
        "human_oversight_available": review_evidence.human_oversight_available,
        "monitoring_plan_digest": review_evidence.monitoring_plan_digest,
        "monitoring_plan_complete": review_evidence.monitoring_plan_complete,
        "evidence_capture_plan_digest": review_evidence.evidence_capture_plan_digest,
        "evidence_capture_plan_complete": (
            review_evidence.evidence_capture_plan_complete
        ),
        "simulation_receipt_digest": review_evidence.simulation_receipt_digest,
        "simulation_verified": review_evidence.simulation_verified,
        "operation_window_seconds": source_scope(
            review_evidence,
            "window_seconds",
        ),
        "protected_core_excluded": review_evidence.protected_core_excluded,
        "institutional_hold_active": review_evidence.institutional_hold_active,
        "emergency_state_active": review_evidence.emergency_state_active,
        "appeal_route_digest": review_evidence.appeal_route_digest,
        "appeal_route_available": review_evidence.appeal_route_available,
        "dissent_route_digest": review_evidence.dissent_route_digest,
        "dissent_route_available": review_evidence.dissent_route_available,
    }
    values.update(overrides)
    for name in _SEQUENCE_FIELDS:
        values[name] = canon(tuple(values[name]))
    value = LifecycleBoundedRequestEvidenceV010(evidence_digest="", **values)
    value = replace(value, evidence_digest=evidence_digest(value))
    issues = evidence_issues(value)
    if issues:
        raise ValueError(f"lifecycle_request_evidence_invalid:{issues[0]}")
    return value


def evidence_issues(
    value: LifecycleBoundedRequestEvidenceV010,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        value.evidence_id,
        value.bounded_request_id,
        value.requester_id,
        value.requester_organization_id,
        value.decision_authority_id,
        value.future_operator_id,
        value.subject_id,
        value.subject_kind,
        value.subject_version,
        value.source_review_id,
        value.source_review_record_digest,
        value.decision_route_digest,
    )
    if not all(required):
        issues.append("required_identity_missing")
    if not value.source_artifact_digests:
        issues.append("source_digests_missing")
    if min(
        value.requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.completed_at_epoch_seconds,
        value.request_expiry_at_epoch_seconds,
        value.decision_deadline_at_epoch_seconds,
        value.operation_window_seconds,
    ) < 0:
        issues.append("negative_time_or_window")
    for name in _SEQUENCE_FIELDS:
        if getattr(value, name) != canon(getattr(value, name)):
            issues.append(f"{name}_not_canonical")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_submission(
    bounded_request_id: str,
    requester_id: str,
    requester_organization_id: str,
    requested_at_epoch_seconds: int,
    completed_at_epoch_seconds: int,
    review_record: LifecycleReviewArtifactV09,
    request_evidence: LifecycleBoundedRequestEvidenceV010,
    *,
    decision_route_digest: str,
    decision_deadline_at_epoch_seconds: int,
    objective: str = OBJECTIVE,
) -> LifecycleBoundedRequestSubmissionV010:
    value = LifecycleBoundedRequestSubmissionV010(
        bounded_request_id=bounded_request_id,
        requester_id=requester_id,
        requester_organization_id=requester_organization_id,
        objective=objective,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        source_review_id=review_record.review_id,
        source_review_record_digest=review_record.record_digest,
        subject_id=request_evidence.subject_id,
        subject_kind=request_evidence.subject_kind,
        subject_version=request_evidence.subject_version,
        request_evidence_digest=request_evidence.evidence_digest,
        decision_authority_id=source_authority(review_record),
        future_operator_id=source_operator(review_record),
        decision_route_digest=decision_route_digest,
        decision_deadline_at_epoch_seconds=decision_deadline_at_epoch_seconds,
        request_digest="",
    )
    value = replace(value, request_digest=submission_digest(value))
    issues = submission_issues(value)
    if issues:
        raise ValueError(f"lifecycle_request_invalid:{issues[0]}")
    return value


def submission_issues(
    value: LifecycleBoundedRequestSubmissionV010,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name not in {
            "request_digest",
            "version",
            "requested_at_epoch_seconds",
            "completed_at_epoch_seconds",
            "decision_deadline_at_epoch_seconds",
        }
    )
    if not all(required):
        issues.append("required_request_field_missing")
    if min(
        value.requested_at_epoch_seconds,
        value.completed_at_epoch_seconds,
        value.decision_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_request_time")
    if value.request_digest != submission_digest(value):
        issues.append("request_digest_mismatch")
    return tuple(issues)


def scope_matches(
    evidence: LifecycleBoundedRequestEvidenceV010,
    review_evidence: LifecycleReviewEvidenceV09,
) -> bool:
    return all(
        getattr(evidence, target) == (
            source_scope(review_evidence, source)
            if source in {"scope_digest", "scope_items", "window_seconds"}
            else getattr(review_evidence, source)
        )
        for target, source in _SCOPE_PAIRS
    )
