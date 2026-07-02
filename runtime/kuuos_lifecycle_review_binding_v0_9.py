from __future__ import annotations

from dataclasses import asdict, fields, replace
from typing import Any

from runtime.kuuos_apoptosis_bounded_execution_preparation_types_v0_8 import (
    ApoptosisBoundedExecutionPreparationEvidence,
    ApoptosisBoundedExecutionPreparationPolicy,
    ApoptosisBoundedExecutionPreparationRecord,
    ApoptosisBoundedExecutionPreparationRequest,
)
from runtime.kuuos_lifecycle_review_chain_v0_9 import source_digests
from runtime.kuuos_lifecycle_review_policy_v0_9 import canon
from runtime.kuuos_lifecycle_review_types_v0_9 import (
    OBJECTIVE,
    LifecycleReviewEvidenceV09,
    LifecycleReviewRequestV09,
    lifecycle_review_evidence_digest,
    lifecycle_review_request_digest,
)


_SEQUENCE_FIELDS = (
    "execution_scope_items",
    "target_resource_ids",
    "protected_resource_ids",
    "reversible_step_ids",
    "irreversible_step_ids",
)


def make_evidence(
    preparation_request: ApoptosisBoundedExecutionPreparationRequest,
    preparation_evidence: ApoptosisBoundedExecutionPreparationEvidence,
    preparation_policy: ApoptosisBoundedExecutionPreparationPolicy,
    preparation_record: ApoptosisBoundedExecutionPreparationRecord,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> LifecycleReviewEvidenceV09:
    source = asdict(preparation_evidence)
    field_names = {item.name for item in fields(LifecycleReviewEvidenceV09)}
    values = {
        name: value
        for name, value in source.items()
        if name in field_names and name not in {"evidence_digest", "version"}
    }
    values.update(
        subject_id=preparation_record.subject_id,
        subject_kind=preparation_record.subject_kind,
        subject_version=preparation_record.subject_version,
        source_preparation_id=preparation_record.preparation_id,
        source_preparation_record_digest=preparation_record.record_digest,
        source_artifact_digests=source_digests(
            preparation_request,
            preparation_evidence,
            preparation_policy,
            preparation_record,
            source_args,
        ),
        future_execution_authority_id=preparation_record.future_execution_authority_id,
    )
    values.update(overrides)
    for name in _SEQUENCE_FIELDS:
        values[name] = canon(tuple(values[name]))
    value = LifecycleReviewEvidenceV09(evidence_digest="", **values)
    value = replace(value, evidence_digest=lifecycle_review_evidence_digest(value))
    issues = evidence_issues(value)
    if issues:
        raise ValueError(f"execution_review_evidence_invalid:{issues[0]}")
    return value


def evidence_issues(value: LifecycleReviewEvidenceV09) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        value.evidence_id,
        value.review_id,
        value.reviewer_id,
        value.reviewer_organization_id,
        value.future_execution_authority_id,
        value.future_execution_operator_id,
        value.subject_id,
        value.subject_kind,
        value.subject_version,
        value.source_preparation_id,
        value.source_preparation_record_digest,
    )
    if not all(required):
        issues.append("required_identity_missing")
    if not value.source_artifact_digests:
        issues.append("source_digests_missing")
    if min(
        value.review_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.completed_at_epoch_seconds,
        value.review_expiry_at_epoch_seconds,
        value.execution_window_seconds,
    ) < 0:
        issues.append("negative_time_or_window")
    for name in _SEQUENCE_FIELDS:
        if getattr(value, name) != canon(getattr(value, name)):
            issues.append(f"{name}_not_canonical")
    if value.evidence_digest != lifecycle_review_evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_request(
    review_id: str,
    reviewer_id: str,
    reviewer_organization_id: str,
    review_requested_at_epoch_seconds: int,
    completed_at_epoch_seconds: int,
    preparation_record: ApoptosisBoundedExecutionPreparationRecord,
    review_evidence: LifecycleReviewEvidenceV09,
    *,
    future_execution_operator_id: str,
    objective: str = OBJECTIVE,
) -> LifecycleReviewRequestV09:
    value = LifecycleReviewRequestV09(
        review_id=review_id,
        reviewer_id=reviewer_id,
        reviewer_organization_id=reviewer_organization_id,
        objective=objective,
        review_requested_at_epoch_seconds=review_requested_at_epoch_seconds,
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        source_preparation_id=preparation_record.preparation_id,
        source_preparation_record_digest=preparation_record.record_digest,
        subject_id=preparation_record.subject_id,
        subject_kind=preparation_record.subject_kind,
        subject_version=preparation_record.subject_version,
        review_evidence_digest=review_evidence.evidence_digest,
        future_execution_authority_id=preparation_record.future_execution_authority_id,
        future_execution_operator_id=future_execution_operator_id,
        request_digest="",
    )
    value = replace(value, request_digest=lifecycle_review_request_digest(value))
    issues = request_issues(value)
    if issues:
        raise ValueError(f"execution_review_request_invalid:{issues[0]}")
    return value


def request_issues(value: LifecycleReviewRequestV09) -> tuple[str, ...]:
    issues: list[str] = []
    required = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name not in {
            "request_digest",
            "version",
            "review_requested_at_epoch_seconds",
            "completed_at_epoch_seconds",
        }
    )
    if not all(required):
        issues.append("required_request_field_missing")
    if min(
        value.review_requested_at_epoch_seconds,
        value.completed_at_epoch_seconds,
    ) < 0:
        issues.append("negative_request_time")
    if value.request_digest != lifecycle_review_request_digest(value):
        issues.append("request_digest_mismatch")
    return tuple(issues)


def scope_matches(
    evidence: LifecycleReviewEvidenceV09,
    preparation_evidence: ApoptosisBoundedExecutionPreparationEvidence,
) -> bool:
    source = asdict(preparation_evidence)
    names = (
        "execution_scope_digest",
        "execution_scope_items",
        "target_resource_ids",
        "protected_resource_ids",
        "reversible_step_ids",
        "irreversible_step_ids",
        "rollback_plan_digest",
        "recovery_route_digest",
        "stop_condition_digest",
        "abort_channel_digest",
        "human_oversight_digest",
        "monitoring_plan_digest",
        "evidence_capture_plan_digest",
        "simulation_receipt_digest",
        "execution_window_seconds",
    )
    return all(getattr(evidence, name) == source[name] for name in names)
