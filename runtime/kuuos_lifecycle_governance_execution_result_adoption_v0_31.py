#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_execution_result_review_v0_30 import (
    ACCEPTED as SOURCE_ACCEPTED,
    artifact_issues as source_artifact_issues,
    all_source_digests as review_source_digests,
)

VERSION = "kuuos_lifecycle_execution_result_adoption_v0_31"
ADOPTED = "LIFECYCLE_EXECUTION_RESULT_ADOPTION_ADOPTED_FOR_SEPARATE_COMPLETION_REVIEW"
DEFERRED = "LIFECYCLE_EXECUTION_RESULT_ADOPTION_DEFERRED"
REJECTED = "LIFECYCLE_EXECUTION_RESULT_ADOPTION_REJECTED"
OBJECTIVE = "ADOPT_REVIEWED_EXECUTION_RESULT_FOR_SEPARATE_COMPLETION_REVIEW_ONLY"
SOURCE_ORDER_CHECK = "source_result_review_precedes_result_adoption_and_deadline_valid"


class Rec(SimpleNamespace):
    def to_dict(self) -> dict[str, Any]:
        out = {}
        for key, value in self.__dict__.items():
            if isinstance(value, tuple):
                out[key] = list(value)
            elif isinstance(value, dict):
                out[key] = dict(value)
            else:
                out[key] = value
        return out


def _digest(value: Rec, field: str) -> str:
    payload = value.to_dict()
    payload.pop(field, None)
    return canonical_digest(payload)


def policy_digest(value: Rec) -> str:
    return _digest(value, "policy_digest")


def evidence_digest(value: Rec) -> str:
    return _digest(value, "evidence_digest")


def adoption_digest(value: Rec) -> str:
    return _digest(value, "adoption_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(
    policy_id: str,
    *,
    allowed_adopter_ids: tuple[str, ...],
    allowed_adopter_organization_ids: tuple[str, ...],
    max_adoption_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
    max_completion_review_delay_seconds: int = 900,
) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_adopter_ids=_canon(allowed_adopter_ids),
        allowed_adopter_organization_ids=_canon(allowed_adopter_organization_ids),
        max_adoption_delay_seconds=max_adoption_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_completion_review_delay_seconds=max_completion_review_delay_seconds,
        accepted_source_required=True,
        source_recomputation_required=True,
        result_adoption_route_required=True,
        adopter_authority_required=True,
        adopter_separation_required=True,
        completion_review_route_required_next=True,
        repository_read_only=True,
        file_write_absent_required=True,
        ref_update_absent_required=True,
        branch_move_absent_required=True,
        external_operation_absent_required=True,
        terminal_marker_absent_required=True,
        resource_removal_absent_required=True,
        policy_digest="",
        version=VERSION,
    )
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_execution_result_adoption_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_adopter_ids or not value.allowed_adopter_organization_ids:
        issues.append("allowed_adopter_missing")
    if min(value.max_adoption_delay_seconds, value.max_evidence_age_seconds, value.max_completion_review_delay_seconds) <= 0:
        issues.append("bound_invalid")
    if not all((
        value.repository_read_only,
        value.file_write_absent_required,
        value.ref_update_absent_required,
        value.branch_move_absent_required,
        value.external_operation_absent_required,
        value.terminal_marker_absent_required,
        value.resource_removal_absent_required,
    )):
        issues.append("adoption_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = review_source_digests(source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:]))
    result.update(
        lifecycle_execution_result_review=source_review.review_digest,
        lifecycle_execution_result_review_evidence=source_evidence.evidence_digest,
        lifecycle_execution_result_review_policy=source_policy.policy_digest,
        lifecycle_execution_result_review_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_review, source_evidence, source_policy, *source_args)


def expected_completion_review_route_digest(source_review, source_record, *, adoption_id: str, adopter_id: str, adoption_receipt_digest: str, completion_review_deadline_at_epoch_seconds: int) -> str:
    return canonical_digest({
        "source_review_id": source_review.review_id,
        "source_review_record_digest": source_record.record_digest,
        "source_result_adoption_route_digest": source_review.result_adoption_route_digest,
        "adoption_id": adoption_id,
        "adopter_id": adopter_id,
        "adopted_lifecycle_state_digest": source_review.adopted_lifecycle_state_digest,
        "result_review_receipt_digest": source_review.result_review_receipt_digest,
        "adoption_receipt_digest": adoption_receipt_digest,
        "completion_review_deadline_at_epoch_seconds": completion_review_deadline_at_epoch_seconds,
    })


def make_evidence(source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(
        source_review_id=source_review.review_id,
        source_review_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(source_review, source_evidence, source_policy, source_record, source_args),
        source_result_reviewer_id=source_review.result_reviewer_id,
        source_execution_id=source_review.source_execution_id,
        source_preparation_id=source_review.source_preparation_id,
        source_authorization_id=source_review.source_authorization_id,
        source_repository_review_id=source_review.source_repository_review_id,
        subject_id=source_review.subject_id,
        requester_id=source_review.requester_id,
        transition_package_digest=source_review.transition_package_digest,
        adopted_lifecycle_state_digest=source_review.adopted_lifecycle_state_digest,
        proposed_repository_mutation_package_digest=source_review.proposed_repository_mutation_package_digest,
        bounded_execution_receipt_digest=source_review.bounded_execution_receipt_digest,
        result_review_receipt_digest=source_review.result_review_receipt_digest,
        source_result_adoption_route_digest=source_review.result_adoption_route_digest,
        source_result_adoption_deadline_at_epoch_seconds=source_review.result_adoption_deadline_at_epoch_seconds,
    )
    values.update(overrides)
    if "completion_review_route_digest" not in values:
        values["completion_review_route_digest"] = expected_completion_review_route_digest(
            source_review,
            source_record,
            adoption_id=values["adoption_id"],
            adopter_id=values["adopter_id"],
            adoption_receipt_digest=values["adoption_receipt_digest"],
            completion_review_deadline_at_epoch_seconds=values["completion_review_deadline_at_epoch_seconds"],
        )
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_execution_result_adoption_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = (
        "evidence_id", "adoption_id", "adopter_id", "adopter_organization_id",
        "adopter_mandate_receipt_digest", "adopter_authority_receipt_digest",
        "adopter_identity_confirmation_digest", "source_review_id", "source_review_record_digest",
        "source_result_adoption_route_digest", "adoption_receipt_digest",
        "completion_review_route_digest", "result_review_record_freshness_digest",
        "adoption_consistency_receipt_digest", "completion_scope_receipt_digest",
    )
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.adoption_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.adopted_at_epoch_seconds, value.source_result_adoption_deadline_at_epoch_seconds, value.completion_review_deadline_at_epoch_seconds) < 0:
        issues.append("negative_adoption_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_adoption(adoption_id: str, adopter_id: str, adopter_organization_id: str, adoption_requested_at_epoch_seconds: int, adopted_at_epoch_seconds: int, source_review, source_record, adoption_evidence: Rec, *, adoption_receipt_digest: str, completion_review_route_digest: str, completion_review_deadline_at_epoch_seconds: int, adoption_confirmed: bool, deferral_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(
        adoption_id=adoption_id,
        adopter_id=adopter_id,
        adopter_organization_id=adopter_organization_id,
        objective=objective,
        adoption_requested_at_epoch_seconds=adoption_requested_at_epoch_seconds,
        adopted_at_epoch_seconds=adopted_at_epoch_seconds,
        source_review_id=source_review.review_id,
        source_review_record_digest=source_record.record_digest,
        source_execution_id=source_review.source_execution_id,
        source_preparation_id=source_review.source_preparation_id,
        source_authorization_id=source_review.source_authorization_id,
        source_repository_review_id=source_review.source_repository_review_id,
        subject_id=source_review.subject_id,
        requester_id=source_review.requester_id,
        source_result_reviewer_id=source_review.result_reviewer_id,
        transition_package_digest=source_review.transition_package_digest,
        adopted_lifecycle_state_digest=source_review.adopted_lifecycle_state_digest,
        proposed_repository_mutation_package_digest=source_review.proposed_repository_mutation_package_digest,
        bounded_execution_receipt_digest=source_review.bounded_execution_receipt_digest,
        result_review_receipt_digest=source_review.result_review_receipt_digest,
        source_result_adoption_route_digest=source_review.result_adoption_route_digest,
        adoption_receipt_digest=adoption_receipt_digest,
        completion_review_route_digest=completion_review_route_digest,
        completion_review_deadline_at_epoch_seconds=completion_review_deadline_at_epoch_seconds,
        adoption_evidence_digest=adoption_evidence.evidence_digest,
        adoption_confirmed=adoption_confirmed,
        deferral_reason_digest=deferral_reason_digest,
        adoption_digest="",
        version=VERSION,
    )
    value.adoption_digest = adoption_digest(value)
    issues = adoption_issues(value)
    if issues:
        raise ValueError("lifecycle_execution_result_adoption_invalid:" + issues[0])
    return value


def adoption_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("deferral_reason_digest", "adoption_digest", "version", "adoption_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_adoption_field_missing")
            break
    if not value.adoption_confirmed and not value.deferral_reason_digest:
        issues.append("deferral_reason_missing")
    if min(value.adoption_requested_at_epoch_seconds, value.adopted_at_epoch_seconds, value.completion_review_deadline_at_epoch_seconds) < 0:
        issues.append("negative_adoption_time")
    if value.adoption_digest != adoption_digest(value):
        issues.append("adoption_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all((
        record.status == SOURCE_ACCEPTED,
        record.execution_result_review_record_issued,
        record.execution_result_review_completed,
        record.execution_result_review_accepted,
        record.ready_for_separate_execution_result_adoption,
        record.execution_result_adoption_required_next,
        record.execution_result_adoption_route_required_next,
        not record.repository_changed,
        record.repository_read_only,
    ))


def evaluate(adoption: Rec, evidence: Rec, policy: Rec, source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_review, source_evidence, source_policy, source_record, source_args)
    expected_route = expected_completion_review_route_digest(source_review, source_record, adoption_id=adoption.adoption_id, adopter_id=adoption.adopter_id, adoption_receipt_digest=adoption.adoption_receipt_digest, completion_review_deadline_at_epoch_seconds=adoption.completion_review_deadline_at_epoch_seconds)
    prior = {source_review.subject_id, source_review.requester_id, source_review.source_executor_id, source_review.result_reviewer_id, source_evidence.result_reviewer_id}
    adoption_delay = evidence.adopted_at_epoch_seconds - source_review.reviewed_at_epoch_seconds
    evidence_age = evidence.adopted_at_epoch_seconds - evidence.captured_at_epoch_seconds
    completion_delay = evidence.completion_review_deadline_at_epoch_seconds - evidence.adopted_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "adoption_valid": not adoption_issues(adoption),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_review, source_evidence, source_policy, source_record, source_args),
        "source_review_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and adoption.source_review_id == evidence.source_review_id == source_review.review_id and adoption.source_review_record_digest == evidence.source_review_record_digest == source_record.record_digest,
        "identity_binding_valid": adoption.adoption_id == evidence.adoption_id and adoption.adopter_id == evidence.adopter_id and adoption.adopter_organization_id == evidence.adopter_organization_id and adoption.adoption_evidence_digest == evidence.evidence_digest,
        "result_adoption_route_binding_valid": adoption.source_result_adoption_route_digest == evidence.source_result_adoption_route_digest == source_review.result_adoption_route_digest,
        "completion_review_route_binding_valid": adoption.completion_review_route_digest == evidence.completion_review_route_digest == expected_route,
        "adoption_receipt_binding_valid": adoption.adoption_receipt_digest == evidence.adoption_receipt_digest,
        "adopter_allowed": adoption.adopter_id in policy.allowed_adopter_ids,
        "adopter_organization_allowed": adoption.adopter_organization_id in policy.allowed_adopter_organization_ids,
        "adopter_separated_from_reviewer": adoption.adopter_id != source_review.result_reviewer_id,
        "adopter_separated_from_prior_actors": adoption.adopter_id not in prior,
        "adopter_organization_separated": adoption.adopter_organization_id != source_review.result_reviewer_organization_id,
        "objective_allowed": adoption.objective == OBJECTIVE,
        "adoption_delay_valid": 0 <= adoption_delay <= policy.max_adoption_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "completion_review_delay_valid": 0 < completion_delay <= policy.max_completion_review_delay_seconds,
        "time_order_valid": source_review.reviewed_at_epoch_seconds <= evidence.adoption_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.adopted_at_epoch_seconds < evidence.completion_review_deadline_at_epoch_seconds,
        "source_adoption_deadline_valid": evidence.adopted_at_epoch_seconds <= source_review.result_adoption_deadline_at_epoch_seconds,
        "external_operation_absent": not evidence.external_operation_performed,
        "file_write_absent": not evidence.file_written,
        "ref_update_absent": not evidence.ref_updated,
        "branch_move_absent": not evidence.branch_moved,
        "terminal_marker_absent": not evidence.terminal_marker_written,
        "resource_removal_absent": not evidence.resource_removed,
        "adopter_mandate_verified": evidence.adopter_mandate_verified,
        "adopter_authority_verified": evidence.adopter_authority_verified,
        "adopter_identity_confirmed": evidence.adopter_identity_confirmed,
        "result_review_record_fresh": evidence.result_review_record_fresh,
        "adoption_consistency_valid": evidence.adoption_consistency_valid,
        "completion_scope_valid": evidence.completion_scope_valid,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = (
    "policy_valid", "adoption_valid", "evidence_valid", "source_recomputed_valid", "source_review_ready", "source_binding_valid", "identity_binding_valid", "result_adoption_route_binding_valid", "completion_review_route_binding_valid", "adoption_receipt_binding_valid", "adopter_allowed", "adopter_organization_allowed", "adopter_separated_from_reviewer", "adopter_separated_from_prior_actors", "adopter_organization_separated", "objective_allowed", "adoption_delay_valid", "evidence_fresh", "completion_review_delay_valid", "time_order_valid", "source_adoption_deadline_valid", "external_operation_absent", "file_write_absent", "ref_update_absent", "branch_move_absent", "terminal_marker_absent", "resource_removal_absent",
)
DEFER_CHECKS = (
    "adopter_mandate_verified", "adopter_authority_verified", "adopter_identity_confirmed", "result_review_record_fresh", "adoption_consistency_valid", "completion_scope_valid", "no_unresolved_anomaly", "recovery_not_in_progress", "institutional_hold_absent", "emergency_state_absent",
)


def compute_artifact(adoption: Rec, evidence: Rec, policy: Rec, source_review, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(adoption, evidence, policy, source_review, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_review.reviewed_at_epoch_seconds <= adoption.adoption_requested_at_epoch_seconds <= adoption.adopted_at_epoch_seconds <= source_review.result_adoption_deadline_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_result_review_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in DEFER_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = DEFERRED, failed
        elif adoption.adoption_confirmed:
            status, reason = ADOPTED, "adopted_for_separate_completion_review_only"
        else:
            status, reason = DEFERRED, "execution_result_adoption_not_confirmed"
    issued = status != REJECTED
    adopted = status == ADOPTED
    deferred = status == DEFERRED
    artifact = Rec(
        adoption_id=adoption.adoption_id,
        status=status,
        reason=reason,
        adopter_id=adoption.adopter_id,
        adopter_organization_id=adoption.adopter_organization_id,
        source_review_id=adoption.source_review_id,
        source_review_record_digest=adoption.source_review_record_digest,
        source_result_reviewer_id=adoption.source_result_reviewer_id,
        source_execution_id=adoption.source_execution_id,
        transition_package_digest=adoption.transition_package_digest,
        adopted_lifecycle_state_digest=adoption.adopted_lifecycle_state_digest,
        result_review_receipt_digest=adoption.result_review_receipt_digest,
        adoption_receipt_digest=adoption.adoption_receipt_digest,
        completion_review_route_digest=adoption.completion_review_route_digest,
        completion_review_deadline_at_epoch_seconds=adoption.completion_review_deadline_at_epoch_seconds,
        subject_id=adoption.subject_id,
        requester_id=adoption.requester_id,
        policy_digest=policy.policy_digest,
        adoption_digest=adoption.adoption_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_review_ready=checks["source_review_ready"],
        execution_result_adoption_record_issued=issued,
        execution_result_adoption_completed=issued,
        execution_result_adopted=adopted,
        execution_result_adoption_deferred=deferred,
        execution_result_adoption_rejected=status == REJECTED,
        ready_for_separate_completion_review=adopted,
        completion_review_required_next=adopted,
        completion_review_route_required_next=adopted,
        execution_result_adoption_replan_required_next=deferred,
        execution_result_adoption_replan_route_required_next=deferred,
        repository_changed=False,
        file_written=False,
        ref_updated=False,
        branch_moved=False,
        authority_changed=False,
        terminal_marker_written=False,
        resource_removed=False,
        external_operation_performed=False,
        repository_read_only=True,
        record_digest="",
        version=VERSION,
    )
    artifact.record_digest = record_digest(artifact)
    return artifact


def verify_artifact(*args: Any, **kwargs: Any) -> Rec:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError("lifecycle_execution_result_adoption_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("execution_result_adoption_recomputation_mismatch")
    if artifact.status not in (ADOPTED, DEFERRED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == ADOPTED and not all((artifact.execution_result_adoption_record_issued, artifact.execution_result_adoption_completed, artifact.execution_result_adopted, artifact.ready_for_separate_completion_review, artifact.completion_review_required_next, artifact.completion_review_route_required_next, not artifact.repository_changed)):
        issues.append("adopted_gate_invalid")
    if artifact.status == DEFERRED and not all((artifact.execution_result_adoption_record_issued, artifact.execution_result_adoption_completed, artifact.execution_result_adoption_deferred, not artifact.completion_review_required_next, artifact.execution_result_adoption_replan_required_next)):
        issues.append("deferred_gate_invalid")
    if artifact.status == REJECTED and any((artifact.execution_result_adoption_record_issued, artifact.execution_result_adoption_completed, artifact.completion_review_required_next, artifact.execution_result_adoption_replan_required_next)):
        issues.append("rejected_record_issued")
    if any((artifact.repository_changed, artifact.file_written, artifact.ref_updated, artifact.branch_moved, artifact.authority_changed, artifact.terminal_marker_written, artifact.resource_removed, artifact.external_operation_performed)):
        issues.append("adoption_layer_effect_performed")
    if not artifact.repository_read_only:
        issues.append("repository_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
