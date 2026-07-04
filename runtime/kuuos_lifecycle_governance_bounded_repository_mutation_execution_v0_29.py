#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_repository_mutation_execution_preparation_v0_28 import (
    PREPARED as SOURCE_PREPARED,
    artifact_issues as source_artifact_issues,
    all_source_digests as preparation_source_digests,
)

VERSION = "kuuos_lifecycle_bounded_repository_mutation_execution_v0_29"
EXECUTED = "LIFECYCLE_BOUNDED_REPOSITORY_MUTATION_EXECUTION_RECORDED_FOR_SEPARATE_EXECUTION_RESULT_REVIEW"
ABORTED = "LIFECYCLE_BOUNDED_REPOSITORY_MUTATION_EXECUTION_ABORTED"
REJECTED = "LIFECYCLE_BOUNDED_REPOSITORY_MUTATION_EXECUTION_REJECTED"
OBJECTIVE = "RECORD_BOUNDED_REPOSITORY_MUTATION_EXECUTION_FOR_SEPARATE_RESULT_REVIEW_ONLY"
SOURCE_ORDER_CHECK = "source_execution_preparation_precedes_bounded_execution_and_deadline_valid"


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


def execution_digest(value: Rec) -> str:
    return _digest(value, "execution_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(
    policy_id: str,
    *,
    allowed_executor_ids: tuple[str, ...],
    allowed_executor_organization_ids: tuple[str, ...],
    max_execution_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
    max_result_review_delay_seconds: int = 900,
) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_executor_ids=_canon(allowed_executor_ids),
        allowed_executor_organization_ids=_canon(allowed_executor_organization_ids),
        max_execution_delay_seconds=max_execution_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_result_review_delay_seconds=max_result_review_delay_seconds,
        prepared_source_required=True,
        source_recomputation_required=True,
        mutation_execution_route_required=True,
        executor_authority_required=True,
        executor_separation_required=True,
        bounded_execution_receipt_required=True,
        result_review_route_required_next=True,
        repository_read_only=True,
        external_operation_absent_required=True,
        uncontrolled_file_write_absent_required=True,
        uncontrolled_ref_update_absent_required=True,
        uncontrolled_branch_move_absent_required=True,
        terminal_marker_absent_required=True,
        resource_removal_absent_required=True,
        policy_digest="",
        version=VERSION,
    )
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_bounded_repository_mutation_execution_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_executor_ids or not value.allowed_executor_organization_ids:
        issues.append("allowed_executor_missing")
    if min(value.max_execution_delay_seconds, value.max_evidence_age_seconds, value.max_result_review_delay_seconds) <= 0:
        issues.append("bound_invalid")
    if not all((
        value.repository_read_only,
        value.external_operation_absent_required,
        value.uncontrolled_file_write_absent_required,
        value.uncontrolled_ref_update_absent_required,
        value.uncontrolled_branch_move_absent_required,
        value.terminal_marker_absent_required,
        value.resource_removal_absent_required,
    )):
        issues.append("execution_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(source_preparation, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = preparation_source_digests(
        source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:])
    )
    result.update(
        lifecycle_repository_mutation_execution_preparation=source_preparation.preparation_digest,
        lifecycle_repository_mutation_execution_preparation_evidence=source_evidence.evidence_digest,
        lifecycle_repository_mutation_execution_preparation_policy=source_policy.policy_digest,
        lifecycle_repository_mutation_execution_preparation_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(source_preparation, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(
        source_record, source_preparation, source_evidence, source_policy, *source_args
    )


def expected_result_review_route_digest(
    source_preparation,
    source_record,
    *,
    execution_id: str,
    executor_id: str,
    bounded_execution_receipt_digest: str,
    result_review_deadline_at_epoch_seconds: int,
) -> str:
    return canonical_digest({
        "source_preparation_id": source_preparation.preparation_id,
        "source_preparation_record_digest": source_record.record_digest,
        "source_mutation_execution_route_digest": source_preparation.mutation_execution_route_digest,
        "execution_id": execution_id,
        "executor_id": executor_id,
        "adopted_lifecycle_state_digest": source_preparation.adopted_lifecycle_state_digest,
        "proposed_repository_mutation_package_digest": source_preparation.proposed_repository_mutation_package_digest,
        "bounded_execution_plan_digest": source_preparation.bounded_execution_plan_digest,
        "bounded_execution_receipt_digest": bounded_execution_receipt_digest,
        "result_review_deadline_at_epoch_seconds": result_review_deadline_at_epoch_seconds,
    })


def make_evidence(
    source_preparation,
    source_evidence,
    source_policy,
    source_record,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> Rec:
    values = dict(
        source_preparation_id=source_preparation.preparation_id,
        source_preparation_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(source_preparation, source_evidence, source_policy, source_record, source_args),
        source_preparer_id=source_preparation.preparer_id,
        source_preparer_organization_id=source_preparation.preparer_organization_id,
        source_authorization_id=source_preparation.source_authorization_id,
        source_repository_review_id=source_preparation.source_repository_review_id,
        subject_id=source_preparation.subject_id,
        requester_id=source_preparation.requester_id,
        transition_package_digest=source_preparation.transition_package_digest,
        adopted_lifecycle_state_digest=source_preparation.adopted_lifecycle_state_digest,
        proposed_repository_mutation_package_digest=source_preparation.proposed_repository_mutation_package_digest,
        bounded_execution_plan_digest=source_preparation.bounded_execution_plan_digest,
        source_mutation_execution_route_digest=source_preparation.mutation_execution_route_digest,
        source_mutation_execution_deadline_at_epoch_seconds=source_preparation.mutation_execution_deadline_at_epoch_seconds,
    )
    values.update(overrides)
    if "result_review_route_digest" not in values:
        values["result_review_route_digest"] = expected_result_review_route_digest(
            source_preparation,
            source_record,
            execution_id=values["execution_id"],
            executor_id=values["executor_id"],
            bounded_execution_receipt_digest=values["bounded_execution_receipt_digest"],
            result_review_deadline_at_epoch_seconds=values["result_review_deadline_at_epoch_seconds"],
        )
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_bounded_repository_mutation_execution_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = (
        "evidence_id",
        "execution_id",
        "executor_id",
        "executor_organization_id",
        "executor_mandate_receipt_digest",
        "executor_authority_receipt_digest",
        "executor_identity_confirmation_digest",
        "source_preparation_id",
        "source_preparation_record_digest",
        "source_mutation_execution_route_digest",
        "bounded_execution_receipt_digest",
        "bounded_execution_plan_digest",
        "mutation_package_integrity_receipt_digest",
        "sandbox_receipt_digest",
        "rollback_guard_receipt_digest",
        "result_review_route_digest",
    )
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(
        value.execution_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.executed_at_epoch_seconds,
        value.source_mutation_execution_deadline_at_epoch_seconds,
        value.result_review_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_execution_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_execution(
    execution_id: str,
    executor_id: str,
    executor_organization_id: str,
    execution_requested_at_epoch_seconds: int,
    executed_at_epoch_seconds: int,
    source_preparation,
    source_record,
    execution_evidence: Rec,
    *,
    bounded_execution_receipt_digest: str,
    result_review_route_digest: str,
    result_review_deadline_at_epoch_seconds: int,
    execution_confirmed: bool,
    abort_reason_digest: str = "",
    objective: str = OBJECTIVE,
) -> Rec:
    value = Rec(
        execution_id=execution_id,
        executor_id=executor_id,
        executor_organization_id=executor_organization_id,
        objective=objective,
        execution_requested_at_epoch_seconds=execution_requested_at_epoch_seconds,
        executed_at_epoch_seconds=executed_at_epoch_seconds,
        source_preparation_id=source_preparation.preparation_id,
        source_preparation_record_digest=source_record.record_digest,
        source_authorization_id=source_preparation.source_authorization_id,
        source_repository_review_id=source_preparation.source_repository_review_id,
        subject_id=source_preparation.subject_id,
        requester_id=source_preparation.requester_id,
        source_preparer_id=source_preparation.preparer_id,
        transition_package_digest=source_preparation.transition_package_digest,
        adopted_lifecycle_state_digest=source_preparation.adopted_lifecycle_state_digest,
        source_mutation_execution_route_digest=source_preparation.mutation_execution_route_digest,
        proposed_repository_mutation_package_digest=source_preparation.proposed_repository_mutation_package_digest,
        bounded_execution_plan_digest=source_preparation.bounded_execution_plan_digest,
        bounded_execution_receipt_digest=bounded_execution_receipt_digest,
        result_review_route_digest=result_review_route_digest,
        result_review_deadline_at_epoch_seconds=result_review_deadline_at_epoch_seconds,
        execution_evidence_digest=execution_evidence.evidence_digest,
        execution_confirmed=execution_confirmed,
        abort_reason_digest=abort_reason_digest,
        execution_digest="",
        version=VERSION,
    )
    value.execution_digest = execution_digest(value)
    issues = execution_issues(value)
    if issues:
        raise ValueError("lifecycle_bounded_repository_mutation_execution_invalid:" + issues[0])
    return value


def execution_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("abort_reason_digest", "execution_digest", "version", "execution_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_execution_field_missing")
            break
    if not value.execution_confirmed and not value.abort_reason_digest:
        issues.append("abort_reason_missing")
    if min(
        value.execution_requested_at_epoch_seconds,
        value.executed_at_epoch_seconds,
        value.result_review_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_execution_time")
    if value.execution_digest != execution_digest(value):
        issues.append("execution_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all((
        record.status == SOURCE_PREPARED,
        record.repository_mutation_execution_preparation_record_issued,
        record.repository_mutation_execution_preparation_completed,
        record.repository_mutation_execution_prepared,
        record.ready_for_separate_bounded_repository_mutation_execution,
        record.bounded_repository_mutation_execution_required_next,
        record.bounded_repository_mutation_execution_route_required_next,
        not record.repository_mutation_performed,
        not record.file_written,
        not record.ref_updated,
        not record.branch_moved,
        not record.external_operation_performed,
        not record.repository_changed,
        record.repository_read_only,
    ))


def _prior_actor_ids(source_preparation, source_evidence) -> set[str]:
    return {
        source_preparation.subject_id,
        source_preparation.requester_id,
        source_preparation.source_authorizer_id,
        source_preparation.preparer_id,
        source_evidence.preparer_id,
    }


def evaluate(
    execution: Rec,
    evidence: Rec,
    policy: Rec,
    source_preparation,
    source_evidence,
    source_policy,
    source_record,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_preparation, source_evidence, source_policy, source_record, source_args)
    expected_result_route = expected_result_review_route_digest(
        source_preparation,
        source_record,
        execution_id=execution.execution_id,
        executor_id=execution.executor_id,
        bounded_execution_receipt_digest=execution.bounded_execution_receipt_digest,
        result_review_deadline_at_epoch_seconds=execution.result_review_deadline_at_epoch_seconds,
    )
    prior = _prior_actor_ids(source_preparation, source_evidence)
    execution_delay = evidence.executed_at_epoch_seconds - source_preparation.prepared_at_epoch_seconds
    evidence_age = evidence.executed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    result_review_delay = evidence.result_review_deadline_at_epoch_seconds - evidence.executed_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "execution_valid": not execution_issues(execution),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_preparation, source_evidence, source_policy, source_record, source_args),
        "source_preparation_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests
        and execution.source_preparation_id == evidence.source_preparation_id == source_preparation.preparation_id
        and execution.source_preparation_record_digest == evidence.source_preparation_record_digest == source_record.record_digest,
        "identity_binding_valid": execution.execution_id == evidence.execution_id
        and execution.executor_id == evidence.executor_id
        and execution.executor_organization_id == evidence.executor_organization_id
        and execution.execution_evidence_digest == evidence.evidence_digest,
        "mutation_execution_route_binding_valid": execution.source_mutation_execution_route_digest
        == evidence.source_mutation_execution_route_digest
        == source_preparation.mutation_execution_route_digest,
        "result_review_route_binding_valid": execution.result_review_route_digest
        == evidence.result_review_route_digest
        == expected_result_route,
        "transition_package_binding_valid": execution.transition_package_digest
        == evidence.transition_package_digest
        == source_preparation.transition_package_digest,
        "adopted_state_binding_valid": execution.adopted_lifecycle_state_digest
        == evidence.adopted_lifecycle_state_digest
        == source_preparation.adopted_lifecycle_state_digest,
        "proposed_repository_mutation_package_binding_valid": execution.proposed_repository_mutation_package_digest
        == evidence.proposed_repository_mutation_package_digest
        == source_preparation.proposed_repository_mutation_package_digest,
        "bounded_execution_plan_binding_valid": execution.bounded_execution_plan_digest
        == evidence.bounded_execution_plan_digest
        == source_preparation.bounded_execution_plan_digest,
        "bounded_execution_receipt_binding_valid": execution.bounded_execution_receipt_digest == evidence.bounded_execution_receipt_digest,
        "executor_allowed": execution.executor_id in policy.allowed_executor_ids,
        "executor_organization_allowed": execution.executor_organization_id in policy.allowed_executor_organization_ids,
        "executor_separated_from_preparer": execution.executor_id != source_preparation.preparer_id,
        "executor_separated_from_prior_actors": execution.executor_id not in prior,
        "executor_organization_separated": execution.executor_organization_id != source_preparation.preparer_organization_id,
        "objective_allowed": execution.objective == OBJECTIVE,
        "execution_delay_valid": 0 <= execution_delay <= policy.max_execution_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "result_review_delay_valid": 0 < result_review_delay <= policy.max_result_review_delay_seconds,
        "time_order_valid": source_preparation.prepared_at_epoch_seconds
        <= evidence.execution_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.executed_at_epoch_seconds
        < evidence.result_review_deadline_at_epoch_seconds,
        "source_execution_deadline_valid": evidence.executed_at_epoch_seconds
        <= source_preparation.mutation_execution_deadline_at_epoch_seconds,
        "external_operation_absent": not evidence.external_operation_performed,
        "uncontrolled_file_write_absent": not evidence.uncontrolled_file_written,
        "uncontrolled_ref_update_absent": not evidence.uncontrolled_ref_updated,
        "uncontrolled_branch_move_absent": not evidence.uncontrolled_branch_moved,
        "terminal_marker_absent": not evidence.terminal_marker_written,
        "resource_removal_absent": not evidence.resource_removed,
        "executor_mandate_verified": evidence.executor_mandate_verified,
        "executor_authority_verified": evidence.executor_authority_verified,
        "executor_identity_confirmed": evidence.executor_identity_confirmed,
        "preparation_record_fresh": evidence.preparation_record_fresh,
        "bounded_execution_receipt_valid": evidence.bounded_execution_receipt_valid,
        "mutation_package_integrity_valid": evidence.mutation_package_integrity_valid,
        "sandbox_receipt_valid": evidence.sandbox_receipt_valid,
        "rollback_guard_valid": evidence.rollback_guard_valid,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = (
    "policy_valid",
    "execution_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_preparation_ready",
    "source_binding_valid",
    "identity_binding_valid",
    "mutation_execution_route_binding_valid",
    "result_review_route_binding_valid",
    "transition_package_binding_valid",
    "adopted_state_binding_valid",
    "proposed_repository_mutation_package_binding_valid",
    "bounded_execution_plan_binding_valid",
    "bounded_execution_receipt_binding_valid",
    "executor_allowed",
    "executor_organization_allowed",
    "executor_separated_from_preparer",
    "executor_separated_from_prior_actors",
    "executor_organization_separated",
    "objective_allowed",
    "execution_delay_valid",
    "evidence_fresh",
    "result_review_delay_valid",
    "time_order_valid",
    "source_execution_deadline_valid",
    "external_operation_absent",
    "uncontrolled_file_write_absent",
    "uncontrolled_ref_update_absent",
    "uncontrolled_branch_move_absent",
    "terminal_marker_absent",
    "resource_removal_absent",
)

ABORT_CHECKS = (
    "executor_mandate_verified",
    "executor_authority_verified",
    "executor_identity_confirmed",
    "preparation_record_fresh",
    "bounded_execution_receipt_valid",
    "mutation_package_integrity_valid",
    "sandbox_receipt_valid",
    "rollback_guard_valid",
    "no_unresolved_anomaly",
    "recovery_not_in_progress",
    "institutional_hold_absent",
    "emergency_state_absent",
)


def compute_artifact(
    execution: Rec,
    evidence: Rec,
    policy: Rec,
    source_preparation,
    source_evidence,
    source_policy,
    source_record,
    *source_args: Any,
) -> Rec:
    checks, expected_digests = evaluate(
        execution, evidence, policy, source_preparation, source_evidence, source_policy, source_record, tuple(source_args)
    )
    checks[SOURCE_ORDER_CHECK] = (
        source_preparation.prepared_at_epoch_seconds
        <= execution.execution_requested_at_epoch_seconds
        <= execution.executed_at_epoch_seconds
        <= source_preparation.mutation_execution_deadline_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_preparation_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in ABORT_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = ABORTED, failed
        elif execution.execution_confirmed:
            status, reason = EXECUTED, "bounded_repository_mutation_execution_recorded_for_separate_result_review_only"
        else:
            status, reason = ABORTED, "bounded_repository_mutation_execution_not_confirmed"
    issued = status != REJECTED
    executed = status == EXECUTED
    aborted = status == ABORTED
    artifact = Rec(
        execution_id=execution.execution_id,
        status=status,
        reason=reason,
        executor_id=execution.executor_id,
        executor_organization_id=execution.executor_organization_id,
        source_preparation_id=execution.source_preparation_id,
        source_preparation_record_digest=execution.source_preparation_record_digest,
        source_preparer_id=execution.source_preparer_id,
        source_authorization_id=execution.source_authorization_id,
        source_repository_review_id=execution.source_repository_review_id,
        transition_package_digest=execution.transition_package_digest,
        adopted_lifecycle_state_digest=execution.adopted_lifecycle_state_digest,
        source_mutation_execution_route_digest=execution.source_mutation_execution_route_digest,
        proposed_repository_mutation_package_digest=execution.proposed_repository_mutation_package_digest,
        bounded_execution_plan_digest=execution.bounded_execution_plan_digest,
        bounded_execution_receipt_digest=execution.bounded_execution_receipt_digest,
        result_review_route_digest=execution.result_review_route_digest,
        result_review_deadline_at_epoch_seconds=execution.result_review_deadline_at_epoch_seconds,
        subject_id=execution.subject_id,
        requester_id=execution.requester_id,
        policy_digest=policy.policy_digest,
        execution_digest=execution.execution_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_preparation_ready=checks["source_preparation_ready"],
        bounded_repository_mutation_execution_record_issued=issued,
        bounded_repository_mutation_execution_completed=issued,
        bounded_repository_mutation_execution_recorded=executed,
        bounded_repository_mutation_execution_aborted=aborted,
        bounded_repository_mutation_execution_rejected=status == REJECTED,
        ready_for_separate_repository_mutation_execution_result_review=executed,
        repository_mutation_execution_result_review_required_next=executed,
        repository_mutation_execution_result_review_route_required_next=executed,
        bounded_repository_mutation_execution_replan_required_next=aborted,
        bounded_repository_mutation_execution_replan_route_required_next=aborted,
        repository_mutation_applied=False,
        uncontrolled_file_written=False,
        uncontrolled_ref_updated=False,
        uncontrolled_branch_moved=False,
        authority_changed=False,
        quiescence_state_changed=False,
        terminal_state_changed=False,
        terminal_marker_written=False,
        resource_removed=False,
        external_operation_performed=False,
        repository_changed=False,
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
        raise ValueError("lifecycle_bounded_repository_mutation_execution_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("bounded_repository_mutation_execution_recomputation_mismatch")
    if artifact.status not in (EXECUTED, ABORTED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == EXECUTED and not all((
        artifact.bounded_repository_mutation_execution_record_issued,
        artifact.bounded_repository_mutation_execution_completed,
        artifact.bounded_repository_mutation_execution_recorded,
        artifact.ready_for_separate_repository_mutation_execution_result_review,
        artifact.repository_mutation_execution_result_review_required_next,
        artifact.repository_mutation_execution_result_review_route_required_next,
        not artifact.repository_changed,
    )):
        issues.append("executed_gate_invalid")
    if artifact.status == ABORTED and not all((
        artifact.bounded_repository_mutation_execution_record_issued,
        artifact.bounded_repository_mutation_execution_completed,
        artifact.bounded_repository_mutation_execution_aborted,
        not artifact.repository_mutation_execution_result_review_required_next,
        artifact.bounded_repository_mutation_execution_replan_required_next,
    )):
        issues.append("aborted_gate_invalid")
    if artifact.status == REJECTED and any((
        artifact.bounded_repository_mutation_execution_record_issued,
        artifact.bounded_repository_mutation_execution_completed,
        artifact.repository_mutation_execution_result_review_required_next,
        artifact.bounded_repository_mutation_execution_replan_required_next,
    )):
        issues.append("rejected_record_issued")
    if any((
        artifact.repository_mutation_applied,
        artifact.uncontrolled_file_written,
        artifact.uncontrolled_ref_updated,
        artifact.uncontrolled_branch_moved,
        artifact.authority_changed,
        artifact.quiescence_state_changed,
        artifact.terminal_state_changed,
        artifact.terminal_marker_written,
        artifact.resource_removed,
        artifact.external_operation_performed,
        artifact.repository_changed,
    )):
        issues.append("uncontrolled_repository_or_external_effect_performed")
    if not artifact.repository_read_only:
        issues.append("repository_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
