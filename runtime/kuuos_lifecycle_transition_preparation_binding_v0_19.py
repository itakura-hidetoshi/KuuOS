from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_lifecycle_transition_preparation_package_v0_19 import (
    package_issues,
)
from runtime.kuuos_lifecycle_transition_preparation_source_v0_19 import (
    all_source_digests,
    expected_transition_approval_route_digest,
)
from runtime.kuuos_lifecycle_transition_preparation_types_v0_19 import (
    OBJECTIVE,
    LifecycleTransitionPackageV019,
    LifecycleTransitionPreparationEvidenceV019,
    LifecycleTransitionPreparationSubmissionV019,
    evidence_digest,
    submission_digest,
)
from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import (
    LifecycleTransitionDecisionArtifactV018,
    LifecycleTransitionDecisionEvidenceV018,
    LifecycleTransitionDecisionPolicyV018,
    LifecycleTransitionDecisionSubmissionV018,
)

REQUIRED_EVIDENCE_FIELDS = (
    "evidence_id",
    "transition_preparation_id",
    "transition_preparer_id",
    "transition_preparer_organization_id",
    "preparer_mandate_receipt_digest",
    "preparer_qualification_receipt_digest",
    "preparer_identity_confirmation_digest",
    "conflict_disclosure_digest",
    "jurisdiction_receipt_digest",
    "preparation_readiness_receipt_digest",
    "source_transition_decision_id",
    "source_transition_decision_record_digest",
    "source_transition_decision_maker_id",
    "source_transition_decision_maker_organization_id",
    "source_transition_reviewer_id",
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
    "transition_approver_id",
    "future_transition_operator_id",
    "transition_approval_route_digest",
)


def make_evidence(
    source_decision: LifecycleTransitionDecisionSubmissionV018,
    source_evidence: LifecycleTransitionDecisionEvidenceV018,
    source_policy: LifecycleTransitionDecisionPolicyV018,
    source_record: LifecycleTransitionDecisionArtifactV018,
    source_args: tuple[Any, ...],
    *,
    transition_package: LifecycleTransitionPackageV019,
    **overrides: Any,
) -> LifecycleTransitionPreparationEvidenceV019:
    values: dict[str, Any] = {
        "source_transition_decision_id": source_decision.transition_decision_id,
        "source_transition_decision_record_digest": source_record.record_digest,
        "source_artifact_digests": all_source_digests(
            source_decision,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        "source_transition_decision_maker_id": (
            source_decision.transition_decision_maker_id
        ),
        "source_transition_decision_maker_organization_id": (
            source_decision.transition_decision_maker_organization_id
        ),
        "source_transition_reviewer_id": source_evidence.source_transition_reviewer_id,
        "source_post_operation_reviewer_id": (
            source_evidence.source_post_operation_reviewer_id
        ),
        "source_completion_reviewer_id": source_evidence.source_completion_reviewer_id,
        "source_operator_id": source_evidence.source_operator_id,
        "source_operation_approver_id": source_evidence.source_operation_approver_id,
        "source_authorization_decision_maker_id": (
            source_evidence.source_authorization_decision_maker_id
        ),
        "source_decision_reviewer_id": source_evidence.source_decision_reviewer_id,
        "subject_id": source_decision.subject_id,
        "subject_kind": source_decision.subject_kind,
        "subject_version": source_decision.subject_version,
        "requester_id": source_decision.requester_id,
        "transition_package": transition_package,
    }
    values.update(overrides)
    if "transition_approval_route_digest" not in values:
        values["transition_approval_route_digest"] = (
            expected_transition_approval_route_digest(
                source_decision,
                source_record,
                transition_package_digest=transition_package.package_digest,
                transition_approver_id=values["transition_approver_id"],
                future_transition_operator_id=values["future_transition_operator_id"],
                expected_current_lifecycle_state_digest=(
                    transition_package.expected_current_lifecycle_state_digest
                ),
                proposed_target_lifecycle_state_digest=(
                    transition_package.proposed_target_lifecycle_state_digest
                ),
                transition_approval_deadline_at_epoch_seconds=(
                    values["transition_approval_deadline_at_epoch_seconds"]
                ),
            )
        )
    value = LifecycleTransitionPreparationEvidenceV019(
        evidence_digest="", **values
    )
    value = replace(value, evidence_digest=evidence_digest(value))
    issues = evidence_issues(value)
    if issues:
        raise ValueError(
            f"lifecycle_transition_preparation_evidence_invalid:{issues[0]}"
        )
    return value


def evidence_issues(
    value: LifecycleTransitionPreparationEvidenceV019,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not all(getattr(value, name) for name in REQUIRED_EVIDENCE_FIELDS):
        issues.append("required_identity_receipt_or_binding_missing")
    if not value.source_artifact_digests:
        issues.append("source_digests_missing")
    if package_issues(value.transition_package):
        issues.append("transition_package_invalid")
    times = (
        value.preparation_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.prepared_at_epoch_seconds,
        value.package_expiry_at_epoch_seconds,
        value.transition_approval_deadline_at_epoch_seconds,
    )
    if min(times) < 0:
        issues.append("negative_preparation_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_submission(
    transition_preparation_id: str,
    transition_preparer_id: str,
    transition_preparer_organization_id: str,
    preparation_requested_at_epoch_seconds: int,
    prepared_at_epoch_seconds: int,
    package_expiry_at_epoch_seconds: int,
    source_decision: LifecycleTransitionDecisionSubmissionV018,
    source_record: LifecycleTransitionDecisionArtifactV018,
    preparation_evidence: LifecycleTransitionPreparationEvidenceV019,
    *,
    transition_approver_id: str,
    future_transition_operator_id: str,
    transition_approval_route_digest: str,
    transition_approval_deadline_at_epoch_seconds: int,
    objective: str = OBJECTIVE,
) -> LifecycleTransitionPreparationSubmissionV019:
    package = preparation_evidence.transition_package
    value = LifecycleTransitionPreparationSubmissionV019(
        transition_preparation_id=transition_preparation_id,
        transition_preparer_id=transition_preparer_id,
        transition_preparer_organization_id=transition_preparer_organization_id,
        objective=objective,
        preparation_requested_at_epoch_seconds=(
            preparation_requested_at_epoch_seconds
        ),
        prepared_at_epoch_seconds=prepared_at_epoch_seconds,
        package_expiry_at_epoch_seconds=package_expiry_at_epoch_seconds,
        source_transition_decision_id=source_decision.transition_decision_id,
        source_transition_decision_record_digest=source_record.record_digest,
        subject_id=source_decision.subject_id,
        subject_kind=source_decision.subject_kind,
        subject_version=source_decision.subject_version,
        transition_preparation_evidence_digest=(
            preparation_evidence.evidence_digest
        ),
        requester_id=source_decision.requester_id,
        source_transition_decision_maker_id=(
            source_decision.transition_decision_maker_id
        ),
        transition_approver_id=transition_approver_id,
        future_transition_operator_id=future_transition_operator_id,
        transition_package_digest=package.package_digest,
        expected_current_lifecycle_state_digest=(
            package.expected_current_lifecycle_state_digest
        ),
        proposed_target_lifecycle_state_digest=(
            package.proposed_target_lifecycle_state_digest
        ),
        transition_approval_route_digest=transition_approval_route_digest,
        transition_approval_deadline_at_epoch_seconds=(
            transition_approval_deadline_at_epoch_seconds
        ),
        preparation_digest="",
    )
    value = replace(value, preparation_digest=submission_digest(value))
    issues = submission_issues(value)
    if issues:
        raise ValueError(f"lifecycle_transition_preparation_invalid:{issues[0]}")
    return value


def submission_issues(
    value: LifecycleTransitionPreparationSubmissionV019,
) -> tuple[str, ...]:
    issues: list[str] = []
    payload = value.to_dict()
    for name in (
        "preparation_requested_at_epoch_seconds",
        "prepared_at_epoch_seconds",
        "package_expiry_at_epoch_seconds",
        "transition_approval_deadline_at_epoch_seconds",
        "preparation_digest",
        "version",
    ):
        payload.pop(name, None)
    if not all(payload.values()):
        issues.append("required_preparation_field_missing")
    if min(
        value.preparation_requested_at_epoch_seconds,
        value.prepared_at_epoch_seconds,
        value.package_expiry_at_epoch_seconds,
        value.transition_approval_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_preparation_time")
    if value.preparation_digest != submission_digest(value):
        issues.append("preparation_digest_mismatch")
    return tuple(issues)
