from __future__ import annotations

from dataclasses import fields, replace
from typing import Any

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    LifecycleOperationCompletionArtifactV015,
    LifecycleOperationCompletionEvidenceV015,
    LifecycleOperationCompletionPolicyV015,
    LifecycleOperationCompletionSubmissionV015,
)
from runtime.kuuos_lifecycle_post_operation_review_source_v0_16 import (
    all_source_digests,
    expected_post_operation_review_route_digest,
)
from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import (
    OBJECTIVE,
    LifecyclePostOperationReviewEvidenceV016,
    LifecyclePostOperationReviewSubmissionV016,
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
    "approved_scope_digest": "approved_scope_digest",
    "operation_scope_items": "operation_scope_items",
    "target_resource_ids": "target_resource_ids",
    "protected_resource_ids": "protected_resource_ids",
    "reversible_step_ids": "reversible_step_ids",
    "step_result_digests": "step_result_digests",
    "source_operation_execution_result_digest": (
        "operation_execution_result_digest"
    ),
    "source_target_resource_post_state_digest": (
        "target_resource_post_state_digest"
    ),
}


def make_evidence(
    source_completion: LifecycleOperationCompletionSubmissionV015,
    source_evidence: LifecycleOperationCompletionEvidenceV015,
    source_policy: LifecycleOperationCompletionPolicyV015,
    source_record: LifecycleOperationCompletionArtifactV015,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> LifecyclePostOperationReviewEvidenceV016:
    values = {
        target: getattr(source_evidence, source)
        for target, source in SOURCE_COPY.items()
    }
    values.update(
        source_operation_completion_id=(
            source_completion.operation_completion_id
        ),
        source_operation_completion_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(
            source_completion,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        source_completion_reviewer_id=(
            source_completion.completion_reviewer_id
        ),
        source_completion_reviewer_organization_id=(
            source_completion.completion_reviewer_organization_id
        ),
        source_operator_id=source_completion.source_operator_id,
        source_operation_approver_id=(
            source_completion.source_operation_approver_id
        ),
        source_authorization_decision_maker_id=(
            source_completion.source_authorization_decision_maker_id
        ),
        source_decision_reviewer_id=(
            source_completion.source_decision_reviewer_id
        ),
        subject_id=source_completion.subject_id,
        subject_kind=source_completion.subject_kind,
        subject_version=source_completion.subject_version,
        requester_id=source_completion.requester_id,
        post_operation_review_route_digest=(
            expected_post_operation_review_route_digest(
                source_completion, source_evidence, source_record
            )
        ),
    )
    values.update(overrides)
    for name in SEQUENCE_FIELDS:
        values[name] = canon(tuple(values[name]))
    values["step_result_digests"] = dict(
        sorted(dict(values["step_result_digests"]).items())
    )
    value = LifecyclePostOperationReviewEvidenceV016(
        evidence_digest="", **values
    )
    value = replace(value, evidence_digest=evidence_digest(value))
    issues = evidence_issues(value)
    if issues:
        raise ValueError(
            f"lifecycle_post_operation_review_evidence_invalid:{issues[0]}"
        )
    return value


def evidence_issues(
    value: LifecyclePostOperationReviewEvidenceV016,
) -> tuple[str, ...]:
    issues: list[str] = []
    exempt = {
        "evidence_digest",
        "version",
        "material_conflict_present",
        "unresolved_anomaly_present",
        "rollback_required",
        "recovery_required",
        "external_operation_performed",
        "repository_changed",
        "review_requested_at_epoch_seconds",
        "captured_at_epoch_seconds",
        "reviewed_at_epoch_seconds",
        "step_result_digests",
        *SEQUENCE_FIELDS,
    }
    boolean_suffixes = (
        "_verified",
        "_confirmed",
        "_complete",
        "_ready",
        "_sufficient",
        "_absent",
        "_intact",
        "_observed",
    )
    for item in fields(value):
        if item.name in exempt or item.name.endswith(boolean_suffixes):
            continue
        if item.type is bool:
            continue
        if not getattr(value, item.name):
            issues.append("required_identity_receipt_or_binding_missing")
            break
    if not value.source_artifact_digests:
        issues.append("source_digests_missing")
    if not value.step_result_digests:
        issues.append("step_result_digests_missing")
    if value.step_result_digests != dict(
        sorted(value.step_result_digests.items())
    ):
        issues.append("step_result_digests_not_canonical")
    times = (
        value.review_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.reviewed_at_epoch_seconds,
    )
    if min(times) < 0:
        issues.append("negative_review_time")
    for name in SEQUENCE_FIELDS:
        if getattr(value, name) != canon(getattr(value, name)):
            issues.append(f"{name}_not_canonical")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_submission(
    post_operation_review_id: str,
    post_operation_reviewer_id: str,
    post_operation_reviewer_organization_id: str,
    review_requested_at_epoch_seconds: int,
    reviewed_at_epoch_seconds: int,
    source_completion: LifecycleOperationCompletionSubmissionV015,
    source_record: LifecycleOperationCompletionArtifactV015,
    review_evidence: LifecyclePostOperationReviewEvidenceV016,
    *,
    post_operation_review_route_digest: str,
    objective: str = OBJECTIVE,
) -> LifecyclePostOperationReviewSubmissionV016:
    value = LifecyclePostOperationReviewSubmissionV016(
        post_operation_review_id=post_operation_review_id,
        post_operation_reviewer_id=post_operation_reviewer_id,
        post_operation_reviewer_organization_id=(
            post_operation_reviewer_organization_id
        ),
        objective=objective,
        review_requested_at_epoch_seconds=review_requested_at_epoch_seconds,
        reviewed_at_epoch_seconds=reviewed_at_epoch_seconds,
        source_operation_completion_id=(
            source_completion.operation_completion_id
        ),
        source_operation_completion_record_digest=source_record.record_digest,
        subject_id=source_completion.subject_id,
        subject_kind=source_completion.subject_kind,
        subject_version=source_completion.subject_version,
        post_operation_review_evidence_digest=review_evidence.evidence_digest,
        requester_id=source_completion.requester_id,
        source_completion_reviewer_id=(
            source_completion.completion_reviewer_id
        ),
        source_operator_id=source_completion.source_operator_id,
        source_operation_approver_id=(
            source_completion.source_operation_approver_id
        ),
        source_authorization_decision_maker_id=(
            source_completion.source_authorization_decision_maker_id
        ),
        source_decision_reviewer_id=(
            source_completion.source_decision_reviewer_id
        ),
        post_operation_review_route_digest=post_operation_review_route_digest,
        review_digest="",
    )
    value = replace(value, review_digest=submission_digest(value))
    issues = submission_issues(value)
    if issues:
        raise ValueError(
            f"lifecycle_post_operation_review_invalid:{issues[0]}"
        )
    return value


def submission_issues(
    value: LifecyclePostOperationReviewSubmissionV016,
) -> tuple[str, ...]:
    issues: list[str] = []
    exempt = {
        "review_digest",
        "version",
        "review_requested_at_epoch_seconds",
        "reviewed_at_epoch_seconds",
    }
    if not all(
        getattr(value, item.name)
        for item in fields(value)
        if item.name not in exempt
    ):
        issues.append("required_review_field_missing")
    if min(
        value.review_requested_at_epoch_seconds,
        value.reviewed_at_epoch_seconds,
    ) < 0:
        issues.append("negative_review_time")
    if value.review_digest != submission_digest(value):
        issues.append("review_digest_mismatch")
    return tuple(issues)


def scope_matches(
    evidence: LifecyclePostOperationReviewEvidenceV016,
    source: LifecycleOperationCompletionEvidenceV015,
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
