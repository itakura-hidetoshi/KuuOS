#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_bounded_repository_mutation_execution_v0_29 import (
    EXECUTED as SOURCE_EXECUTED,
    artifact_issues as source_artifact_issues,
    all_source_digests as execution_source_digests,
)

VERSION = "kuuos_lifecycle_execution_result_review_v0_30"
ACCEPTED = "LIFECYCLE_EXECUTION_RESULT_REVIEW_ACCEPTED_FOR_SEPARATE_RESULT_ADOPTION"
FAILED = "LIFECYCLE_EXECUTION_RESULT_REVIEW_FAILED"
REJECTED = "LIFECYCLE_EXECUTION_RESULT_REVIEW_REJECTED"
OBJECTIVE = "REVIEW_BOUNDED_EXECUTION_RESULT_FOR_SEPARATE_RESULT_ADOPTION_ONLY"
SOURCE_ORDER_CHECK = "source_execution_precedes_result_review_and_deadline_valid"


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


def review_digest(value: Rec) -> str:
    return _digest(value, "review_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(
    policy_id: str,
    *,
    allowed_result_reviewer_ids: tuple[str, ...],
    allowed_result_reviewer_organization_ids: tuple[str, ...],
    max_review_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
    max_result_adoption_delay_seconds: int = 900,
) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_result_reviewer_ids=_canon(allowed_result_reviewer_ids),
        allowed_result_reviewer_organization_ids=_canon(allowed_result_reviewer_organization_ids),
        max_review_delay_seconds=max_review_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_result_adoption_delay_seconds=max_result_adoption_delay_seconds,
        executed_source_required=True,
        source_recomputation_required=True,
        result_review_route_required=True,
        result_reviewer_authority_required=True,
        result_reviewer_separation_required=True,
        result_adoption_route_required_next=True,
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
        raise ValueError("lifecycle_execution_result_review_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_result_reviewer_ids or not value.allowed_result_reviewer_organization_ids:
        issues.append("allowed_result_reviewer_missing")
    if min(value.max_review_delay_seconds, value.max_evidence_age_seconds, value.max_result_adoption_delay_seconds) <= 0:
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
        issues.append("review_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(source_execution, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = execution_source_digests(
        source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:])
    )
    result.update(
        lifecycle_bounded_repository_mutation_execution=source_execution.execution_digest,
        lifecycle_bounded_repository_mutation_execution_evidence=source_evidence.evidence_digest,
        lifecycle_bounded_repository_mutation_execution_policy=source_policy.policy_digest,
        lifecycle_bounded_repository_mutation_execution_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(source_execution, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(
        source_record, source_execution, source_evidence, source_policy, *source_args
    )


def expected_result_adoption_route_digest(
    source_execution,
    source_record,
    *,
    review_id: str,
    reviewer_id: str,
    result_review_receipt_digest: str,
    result_adoption_deadline_at_epoch_seconds: int,
) -> str:
    return canonical_digest({
        "source_execution_id": source_execution.execution_id,
        "source_execution_record_digest": source_record.record_digest,
        "source_result_review_route_digest": source_execution.result_review_route_digest,
        "review_id": review_id,
        "reviewer_id": reviewer_id,
        "adopted_lifecycle_state_digest": source_execution.adopted_lifecycle_state_digest,
        "bounded_execution_receipt_digest": source_execution.bounded_execution_receipt_digest,
        "result_review_receipt_digest": result_review_receipt_digest,
        "result_adoption_deadline_at_epoch_seconds": result_adoption_deadline_at_epoch_seconds,
    })


def make_evidence(
    source_execution,
    source_evidence,
    source_policy,
    source_record,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> Rec:
    values = dict(
        source_execution_id=source_execution.execution_id,
        source_execution_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(source_execution, source_evidence, source_policy, source_record, source_args),
        source_executor_id=source_execution.executor_id,
        source_executor_organization_id=source_execution.executor_organization_id,
        source_preparation_id=source_execution.source_preparation_id,
        source_authorization_id=source_execution.source_authorization_id,
        source_repository_review_id=source_execution.source_repository_review_id,
        subject_id=source_execution.subject_id,
        requester_id=source_execution.requester_id,
        transition_package_digest=source_execution.transition_package_digest,
        adopted_lifecycle_state_digest=source_execution.adopted_lifecycle_state_digest,
        proposed_repository_mutation_package_digest=source_execution.proposed_repository_mutation_package_digest,
        bounded_execution_plan_digest=source_execution.bounded_execution_plan_digest,
        bounded_execution_receipt_digest=source_execution.bounded_execution_receipt_digest,
        source_result_review_route_digest=source_execution.result_review_route_digest,
        source_result_review_deadline_at_epoch_seconds=source_execution.result_review_deadline_at_epoch_seconds,
    )
    values.update(overrides)
    if "result_adoption_route_digest" not in values:
        values["result_adoption_route_digest"] = expected_result_adoption_route_digest(
            source_execution,
            source_record,
            review_id=values["review_id"],
            reviewer_id=values["result_reviewer_id"],
            result_review_receipt_digest=values["result_review_receipt_digest"],
            result_adoption_deadline_at_epoch_seconds=values["result_adoption_deadline_at_epoch_seconds"],
        )
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_execution_result_review_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = (
        "evidence_id",
        "review_id",
        "result_reviewer_id",
        "result_reviewer_organization_id",
        "result_reviewer_mandate_receipt_digest",
        "result_reviewer_authority_receipt_digest",
        "result_reviewer_identity_confirmation_digest",
        "source_execution_id",
        "source_execution_record_digest",
        "source_result_review_route_digest",
        "result_review_receipt_digest",
        "result_adoption_route_digest",
        "bounded_execution_receipt_freshness_digest",
        "result_consistency_receipt_digest",
        "source_trace_receipt_digest",
    )
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(
        value.review_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.reviewed_at_epoch_seconds,
        value.source_result_review_deadline_at_epoch_seconds,
        value.result_adoption_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_review_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_review(
    review_id: str,
    result_reviewer_id: str,
    result_reviewer_organization_id: str,
    review_requested_at_epoch_seconds: int,
    reviewed_at_epoch_seconds: int,
    source_execution,
    source_record,
    review_evidence: Rec,
    *,
    result_review_receipt_digest: str,
    result_adoption_route_digest: str,
    result_adoption_deadline_at_epoch_seconds: int,
    result_accepted: bool,
    failure_reason_digest: str = "",
    objective: str = OBJECTIVE,
) -> Rec:
    value = Rec(
        review_id=review_id,
        result_reviewer_id=result_reviewer_id,
        result_reviewer_organization_id=result_reviewer_organization_id,
        objective=objective,
        review_requested_at_epoch_seconds=review_requested_at_epoch_seconds,
        reviewed_at_epoch_seconds=reviewed_at_epoch_seconds,
        source_execution_id=source_execution.execution_id,
        source_execution_record_digest=source_record.record_digest,
        source_preparation_id=source_execution.source_preparation_id,
        source_authorization_id=source_execution.source_authorization_id,
        source_repository_review_id=source_execution.source_repository_review_id,
        subject_id=source_execution.subject_id,
        requester_id=source_execution.requester_id,
        source_executor_id=source_execution.executor_id,
        transition_package_digest=source_execution.transition_package_digest,
        adopted_lifecycle_state_digest=source_execution.adopted_lifecycle_state_digest,
        proposed_repository_mutation_package_digest=source_execution.proposed_repository_mutation_package_digest,
        bounded_execution_plan_digest=source_execution.bounded_execution_plan_digest,
        bounded_execution_receipt_digest=source_execution.bounded_execution_receipt_digest,
        source_result_review_route_digest=source_execution.result_review_route_digest,
        result_review_receipt_digest=result_review_receipt_digest,
        result_adoption_route_digest=result_adoption_route_digest,
        result_adoption_deadline_at_epoch_seconds=result_adoption_deadline_at_epoch_seconds,
        review_evidence_digest=review_evidence.evidence_digest,
        result_accepted=result_accepted,
        failure_reason_digest=failure_reason_digest,
        review_digest="",
        version=VERSION,
    )
    value.review_digest = review_digest(value)
    issues = review_issues(value)
    if issues:
        raise ValueError("lifecycle_execution_result_review_invalid:" + issues[0])
    return value


def review_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("failure_reason_digest", "review_digest", "version", "result_accepted"):
            continue
        if content == "" or content is None:
            issues.append("required_review_field_missing")
            break
    if not value.result_accepted and not value.failure_reason_digest:
        issues.append("failure_reason_missing")
    if min(
        value.review_requested_at_epoch_seconds,
        value.reviewed_at_epoch_seconds,
        value.result_adoption_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_review_time")
    if value.review_digest != review_digest(value):
        issues.append("review_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all((
        record.status == SOURCE_EXECUTED,
        record.bounded_repository_mutation_execution_record_issued,
        record.bounded_repository_mutation_execution_completed,
        record.bounded_repository_mutation_execution_recorded,
        record.ready_for_separate_repository_mutation_execution_result_review,
        record.repository_mutation_execution_result_review_required_next,
        record.repository_mutation_execution_result_review_route_required_next,
        not record.repository_changed,
        record.repository_read_only,
    ))


def _prior_actor_ids(source_execution, source_evidence) -> set[str]:
    return {
        source_execution.subject_id,
        source_execution.requester_id,
        source_execution.source_preparer_id,
        source_execution.executor_id,
        source_evidence.executor_id,
    }


def evaluate(
    review: Rec,
    evidence: Rec,
    policy: Rec,
    source_execution,
    source_evidence,
    source_policy,
    source_record,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_execution, source_evidence, source_policy, source_record, source_args)
    expected_adoption_route = expected_result_adoption_route_digest(
        source_execution,
        source_record,
        review_id=review.review_id,
        reviewer_id=review.result_reviewer_id,
        result_review_receipt_digest=review.result_review_receipt_digest,
        result_adoption_deadline_at_epoch_seconds=review.result_adoption_deadline_at_epoch_seconds,
    )
    prior = _prior_actor_ids(source_execution, source_evidence)
    review_delay = evidence.reviewed_at_epoch_seconds - source_execution.executed_at_epoch_seconds
    evidence_age = evidence.reviewed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    adoption_delay = evidence.result_adoption_deadline_at_epoch_seconds - evidence.reviewed_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "review_valid": not review_issues(review),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_execution, source_evidence, source_policy, source_record, source_args),
        "source_execution_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests
        and review.source_execution_id == evidence.source_execution_id == source_execution.execution_id
        and review.source_execution_record_digest == evidence.source_execution_record_digest == source_record.record_digest,
        "identity_binding_valid": review.review_id == evidence.review_id
        and review.result_reviewer_id == evidence.result_reviewer_id
        and review.result_reviewer_organization_id == evidence.result_reviewer_organization_id
        and review.review_evidence_digest == evidence.evidence_digest,
        "result_review_route_binding_valid": review.source_result_review_route_digest
        == evidence.source_result_review_route_digest
        == source_execution.result_review_route_digest,
        "result_adoption_route_binding_valid": review.result_adoption_route_digest
        == evidence.result_adoption_route_digest
        == expected_adoption_route,
        "bounded_execution_receipt_binding_valid": review.bounded_execution_receipt_digest
        == evidence.bounded_execution_receipt_digest
        == source_execution.bounded_execution_receipt_digest,
        "result_review_receipt_binding_valid": review.result_review_receipt_digest == evidence.result_review_receipt_digest,
        "result_reviewer_allowed": review.result_reviewer_id in policy.allowed_result_reviewer_ids,
        "result_reviewer_organization_allowed": review.result_reviewer_organization_id in policy.allowed_result_reviewer_organization_ids,
        "reviewer_separated_from_executor": review.result_reviewer_id != source_execution.executor_id,
        "reviewer_separated_from_prior_actors": review.result_reviewer_id not in prior,
        "reviewer_organization_separated": review.result_reviewer_organization_id != source_execution.executor_organization_id,
        "objective_allowed": review.objective == OBJECTIVE,
        "review_delay_valid": 0 <= review_delay <= policy.max_review_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "result_adoption_delay_valid": 0 < adoption_delay <= policy.max_result_adoption_delay_seconds,
        "time_order_valid": source_execution.executed_at_epoch_seconds
        <= evidence.review_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.reviewed_at_epoch_seconds
        < evidence.result_adoption_deadline_at_epoch_seconds,
        "source_result_review_deadline_valid": evidence.reviewed_at_epoch_seconds
        <= source_execution.result_review_deadline_at_epoch_seconds,
        "external_operation_absent": not evidence.external_operation_performed,
        "file_write_absent": not evidence.file_written,
        "ref_update_absent": not evidence.ref_updated,
        "branch_move_absent": not evidence.branch_moved,
        "terminal_marker_absent": not evidence.terminal_marker_written,
        "resource_removal_absent": not evidence.resource_removed,
        "result_reviewer_mandate_verified": evidence.result_reviewer_mandate_verified,
        "result_reviewer_authority_verified": evidence.result_reviewer_authority_verified,
        "result_reviewer_identity_confirmed": evidence.result_reviewer_identity_confirmed,
        "execution_record_fresh": evidence.execution_record_fresh,
        "bounded_execution_receipt_fresh": evidence.bounded_execution_receipt_fresh,
        "result_consistency_valid": evidence.result_consistency_valid,
        "source_trace_valid": evidence.source_trace_valid,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = (
    "policy_valid",
    "review_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_execution_ready",
    "source_binding_valid",
    "identity_binding_valid",
    "result_review_route_binding_valid",
    "result_adoption_route_binding_valid",
    "bounded_execution_receipt_binding_valid",
    "result_review_receipt_binding_valid",
    "result_reviewer_allowed",
    "result_reviewer_organization_allowed",
    "reviewer_separated_from_executor",
    "reviewer_separated_from_prior_actors",
    "reviewer_organization_separated",
    "objective_allowed",
    "review_delay_valid",
    "evidence_fresh",
    "result_adoption_delay_valid",
    "time_order_valid",
    "source_result_review_deadline_valid",
    "external_operation_absent",
    "file_write_absent",
    "ref_update_absent",
    "branch_move_absent",
    "terminal_marker_absent",
    "resource_removal_absent",
)

FAILURE_CHECKS = (
    "result_reviewer_mandate_verified",
    "result_reviewer_authority_verified",
    "result_reviewer_identity_confirmed",
    "execution_record_fresh",
    "bounded_execution_receipt_fresh",
    "result_consistency_valid",
    "source_trace_valid",
    "no_unresolved_anomaly",
    "recovery_not_in_progress",
    "institutional_hold_absent",
    "emergency_state_absent",
)


def compute_artifact(
    review: Rec,
    evidence: Rec,
    policy: Rec,
    source_execution,
    source_evidence,
    source_policy,
    source_record,
    *source_args: Any,
) -> Rec:
    checks, expected_digests = evaluate(review, evidence, policy, source_execution, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = (
        source_execution.executed_at_epoch_seconds
        <= review.review_requested_at_epoch_seconds
        <= review.reviewed_at_epoch_seconds
        <= source_execution.result_review_deadline_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_execution_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in FAILURE_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = FAILED, failed
        elif review.result_accepted:
            status, reason = ACCEPTED, "accepted_for_separate_execution_result_adoption_only"
        else:
            status, reason = FAILED, "execution_result_not_accepted"
    issued = status != REJECTED
    accepted = status == ACCEPTED
    failed = status == FAILED
    artifact = Rec(
        review_id=review.review_id,
        status=status,
        reason=reason,
        result_reviewer_id=review.result_reviewer_id,
        result_reviewer_organization_id=review.result_reviewer_organization_id,
        source_execution_id=review.source_execution_id,
        source_execution_record_digest=review.source_execution_record_digest,
        source_executor_id=review.source_executor_id,
        source_preparation_id=review.source_preparation_id,
        source_authorization_id=review.source_authorization_id,
        source_repository_review_id=review.source_repository_review_id,
        transition_package_digest=review.transition_package_digest,
        adopted_lifecycle_state_digest=review.adopted_lifecycle_state_digest,
        proposed_repository_mutation_package_digest=review.proposed_repository_mutation_package_digest,
        bounded_execution_plan_digest=review.bounded_execution_plan_digest,
        bounded_execution_receipt_digest=review.bounded_execution_receipt_digest,
        source_result_review_route_digest=review.source_result_review_route_digest,
        result_review_receipt_digest=review.result_review_receipt_digest,
        result_adoption_route_digest=review.result_adoption_route_digest,
        result_adoption_deadline_at_epoch_seconds=review.result_adoption_deadline_at_epoch_seconds,
        subject_id=review.subject_id,
        requester_id=review.requester_id,
        policy_digest=policy.policy_digest,
        review_digest=review.review_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_execution_ready=checks["source_execution_ready"],
        execution_result_review_record_issued=issued,
        execution_result_review_completed=issued,
        execution_result_review_accepted=accepted,
        execution_result_review_failed=failed,
        execution_result_review_rejected=status == REJECTED,
        ready_for_separate_execution_result_adoption=accepted,
        execution_result_adoption_required_next=accepted,
        execution_result_adoption_route_required_next=accepted,
        execution_result_review_replan_required_next=failed,
        execution_result_review_replan_route_required_next=failed,
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
        raise ValueError("lifecycle_execution_result_review_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("execution_result_review_recomputation_mismatch")
    if artifact.status not in (ACCEPTED, FAILED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == ACCEPTED and not all((
        artifact.execution_result_review_record_issued,
        artifact.execution_result_review_completed,
        artifact.execution_result_review_accepted,
        artifact.ready_for_separate_execution_result_adoption,
        artifact.execution_result_adoption_required_next,
        artifact.execution_result_adoption_route_required_next,
        not artifact.repository_changed,
    )):
        issues.append("accepted_gate_invalid")
    if artifact.status == FAILED and not all((
        artifact.execution_result_review_record_issued,
        artifact.execution_result_review_completed,
        artifact.execution_result_review_failed,
        not artifact.execution_result_adoption_required_next,
        artifact.execution_result_review_replan_required_next,
    )):
        issues.append("failed_gate_invalid")
    if artifact.status == REJECTED and any((
        artifact.execution_result_review_record_issued,
        artifact.execution_result_review_completed,
        artifact.execution_result_adoption_required_next,
        artifact.execution_result_review_replan_required_next,
    )):
        issues.append("rejected_record_issued")
    if any((
        artifact.repository_changed,
        artifact.file_written,
        artifact.ref_updated,
        artifact.branch_moved,
        artifact.authority_changed,
        artifact.terminal_marker_written,
        artifact.resource_removed,
        artifact.external_operation_performed,
    )):
        issues.append("review_layer_effect_performed")
    if not artifact.repository_read_only:
        issues.append("repository_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
