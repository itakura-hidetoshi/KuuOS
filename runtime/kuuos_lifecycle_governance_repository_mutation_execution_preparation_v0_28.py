#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_repository_mutation_authorization_v0_27 import (
    AUTHORIZED as SOURCE_AUTHORIZED,
    artifact_issues as source_artifact_issues,
    all_source_digests as authorization_source_digests,
)

VERSION = "kuuos_lifecycle_bounded_repository_mutation_execution_preparation_v0_28"
PREPARED = "LIFECYCLE_BOUNDED_REPOSITORY_MUTATION_EXECUTION_PREPARATION_PREPARED_FOR_SEPARATE_BOUNDED_REPOSITORY_MUTATION_EXECUTION"
BLOCKED = "LIFECYCLE_BOUNDED_REPOSITORY_MUTATION_EXECUTION_PREPARATION_BLOCKED"
REJECTED = "LIFECYCLE_BOUNDED_REPOSITORY_MUTATION_EXECUTION_PREPARATION_REJECTED"
OBJECTIVE = "PREPARE_REPOSITORY_MUTATION_EXECUTION_FOR_SEPARATE_BOUNDED_EXECUTION_ONLY"
SOURCE_ORDER_CHECK = "source_authorization_precedes_execution_preparation_and_deadline_valid"


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


def preparation_digest(value: Rec) -> str:
    return _digest(value, "preparation_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(
    policy_id: str,
    *,
    allowed_preparer_ids: tuple[str, ...],
    allowed_preparer_organization_ids: tuple[str, ...],
    max_preparation_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
    max_execution_delay_seconds: int = 900,
) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_preparer_ids=_canon(allowed_preparer_ids),
        allowed_preparer_organization_ids=_canon(allowed_preparer_organization_ids),
        max_preparation_delay_seconds=max_preparation_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_execution_delay_seconds=max_execution_delay_seconds,
        authorized_source_required=True,
        source_recomputation_required=True,
        execution_preparation_route_required=True,
        preparer_authority_required=True,
        preparer_separation_required=True,
        bounded_execution_plan_required=True,
        mutation_execution_route_required_next=True,
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
        raise ValueError("lifecycle_repository_mutation_execution_preparation_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_preparer_ids or not value.allowed_preparer_organization_ids:
        issues.append("allowed_preparer_missing")
    if min(value.max_preparation_delay_seconds, value.max_evidence_age_seconds, value.max_execution_delay_seconds) <= 0:
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
        issues.append("repository_or_external_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(source_authorization, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = authorization_source_digests(
        source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:])
    )
    result.update(
        lifecycle_repository_mutation_authorization=source_authorization.authorization_digest,
        lifecycle_repository_mutation_authorization_evidence=source_evidence.evidence_digest,
        lifecycle_repository_mutation_authorization_policy=source_policy.policy_digest,
        lifecycle_repository_mutation_authorization_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(source_authorization, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(
        source_record, source_authorization, source_evidence, source_policy, *source_args
    )


def expected_mutation_execution_route_digest(
    source_authorization,
    source_record,
    *,
    preparation_id: str,
    preparer_id: str,
    bounded_execution_plan_digest: str,
    proposed_repository_mutation_package_digest: str,
    mutation_execution_deadline_at_epoch_seconds: int,
) -> str:
    return canonical_digest({
        "source_repository_mutation_authorization_id": source_authorization.authorization_id,
        "source_repository_mutation_authorization_record_digest": source_record.record_digest,
        "source_execution_preparation_route_digest": source_authorization.execution_preparation_route_digest,
        "preparation_id": preparation_id,
        "preparer_id": preparer_id,
        "adopted_lifecycle_state_digest": source_authorization.adopted_lifecycle_state_digest,
        "proposed_repository_mutation_package_digest": proposed_repository_mutation_package_digest,
        "bounded_execution_plan_digest": bounded_execution_plan_digest,
        "mutation_execution_deadline_at_epoch_seconds": mutation_execution_deadline_at_epoch_seconds,
    })


def make_evidence(
    source_authorization,
    source_evidence,
    source_policy,
    source_record,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> Rec:
    values = dict(
        source_authorization_id=source_authorization.authorization_id,
        source_authorization_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(source_authorization, source_evidence, source_policy, source_record, source_args),
        source_authorizer_id=source_authorization.authorizer_id,
        source_authorizer_organization_id=source_authorization.authorizer_organization_id,
        source_repository_review_id=source_authorization.source_repository_review_id,
        subject_id=source_authorization.subject_id,
        requester_id=source_authorization.requester_id,
        transition_package_digest=source_authorization.transition_package_digest,
        adopted_lifecycle_state_digest=source_authorization.adopted_lifecycle_state_digest,
        proposed_repository_mutation_package_digest=source_authorization.proposed_repository_mutation_package_digest,
        source_execution_preparation_route_digest=source_authorization.execution_preparation_route_digest,
        source_execution_preparation_deadline_at_epoch_seconds=source_authorization.execution_preparation_deadline_at_epoch_seconds,
    )
    values.update(overrides)
    if "mutation_execution_route_digest" not in values:
        values["mutation_execution_route_digest"] = expected_mutation_execution_route_digest(
            source_authorization,
            source_record,
            preparation_id=values["preparation_id"],
            preparer_id=values["preparer_id"],
            bounded_execution_plan_digest=values["bounded_execution_plan_digest"],
            proposed_repository_mutation_package_digest=values["proposed_repository_mutation_package_digest"],
            mutation_execution_deadline_at_epoch_seconds=values["mutation_execution_deadline_at_epoch_seconds"],
        )
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_repository_mutation_execution_preparation_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = (
        "evidence_id",
        "preparation_id",
        "preparer_id",
        "preparer_organization_id",
        "preparer_mandate_receipt_digest",
        "preparer_authority_receipt_digest",
        "preparer_identity_confirmation_digest",
        "source_authorization_id",
        "source_authorization_record_digest",
        "source_execution_preparation_route_digest",
        "mutation_execution_route_digest",
        "bounded_execution_plan_digest",
        "bounded_execution_plan_receipt_digest",
        "sandbox_allocation_receipt_digest",
        "checkpoint_intent_receipt_digest",
        "mutation_package_integrity_receipt_digest",
        "execution_constraints_receipt_digest",
        "rollback_plan_receipt_digest",
    )
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(
        value.preparation_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.prepared_at_epoch_seconds,
        value.source_execution_preparation_deadline_at_epoch_seconds,
        value.mutation_execution_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_preparation_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_preparation(
    preparation_id: str,
    preparer_id: str,
    preparer_organization_id: str,
    preparation_requested_at_epoch_seconds: int,
    prepared_at_epoch_seconds: int,
    source_authorization,
    source_record,
    preparation_evidence: Rec,
    *,
    bounded_execution_plan_digest: str,
    mutation_execution_route_digest: str,
    mutation_execution_deadline_at_epoch_seconds: int,
    preparation_confirmed: bool,
    blocking_reason_digest: str = "",
    objective: str = OBJECTIVE,
) -> Rec:
    value = Rec(
        preparation_id=preparation_id,
        preparer_id=preparer_id,
        preparer_organization_id=preparer_organization_id,
        objective=objective,
        preparation_requested_at_epoch_seconds=preparation_requested_at_epoch_seconds,
        prepared_at_epoch_seconds=prepared_at_epoch_seconds,
        source_authorization_id=source_authorization.authorization_id,
        source_authorization_record_digest=source_record.record_digest,
        source_repository_review_id=source_authorization.source_repository_review_id,
        subject_id=source_authorization.subject_id,
        requester_id=source_authorization.requester_id,
        source_authorizer_id=source_authorization.authorizer_id,
        transition_package_digest=source_authorization.transition_package_digest,
        adopted_lifecycle_state_digest=source_authorization.adopted_lifecycle_state_digest,
        source_execution_preparation_route_digest=source_authorization.execution_preparation_route_digest,
        proposed_repository_mutation_package_digest=source_authorization.proposed_repository_mutation_package_digest,
        bounded_execution_plan_digest=bounded_execution_plan_digest,
        mutation_execution_route_digest=mutation_execution_route_digest,
        mutation_execution_deadline_at_epoch_seconds=mutation_execution_deadline_at_epoch_seconds,
        preparation_evidence_digest=preparation_evidence.evidence_digest,
        preparation_confirmed=preparation_confirmed,
        blocking_reason_digest=blocking_reason_digest,
        preparation_digest="",
        version=VERSION,
    )
    value.preparation_digest = preparation_digest(value)
    issues = preparation_issues(value)
    if issues:
        raise ValueError("lifecycle_repository_mutation_execution_preparation_invalid:" + issues[0])
    return value


def preparation_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("blocking_reason_digest", "preparation_digest", "version", "preparation_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_preparation_field_missing")
            break
    if not value.preparation_confirmed and not value.blocking_reason_digest:
        issues.append("blocking_reason_missing")
    if min(
        value.preparation_requested_at_epoch_seconds,
        value.prepared_at_epoch_seconds,
        value.mutation_execution_deadline_at_epoch_seconds,
    ) < 0:
        issues.append("negative_preparation_time")
    if value.preparation_digest != preparation_digest(value):
        issues.append("preparation_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all((
        record.status == SOURCE_AUTHORIZED,
        record.repository_mutation_authorization_record_issued,
        record.repository_mutation_authorization_completed,
        record.repository_mutation_authorized,
        record.ready_for_separate_repository_mutation_execution_preparation,
        record.repository_mutation_execution_preparation_required_next,
        record.repository_mutation_execution_preparation_route_required_next,
        not record.repository_mutation_execution_prepared,
        not record.repository_mutation_performed,
        not record.file_written,
        not record.ref_updated,
        not record.branch_moved,
        not record.external_operation_performed,
        not record.repository_changed,
        record.repository_read_only,
    ))


def _prior_actor_ids(source_authorization, source_evidence) -> set[str]:
    return {
        source_authorization.subject_id,
        source_authorization.requester_id,
        source_authorization.source_mutation_reviewer_id,
        source_authorization.authorizer_id,
        source_evidence.authorizer_id,
    }


def evaluate(
    preparation: Rec,
    evidence: Rec,
    policy: Rec,
    source_authorization,
    source_evidence,
    source_policy,
    source_record,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_authorization, source_evidence, source_policy, source_record, source_args)
    expected_execution_route = expected_mutation_execution_route_digest(
        source_authorization,
        source_record,
        preparation_id=preparation.preparation_id,
        preparer_id=preparation.preparer_id,
        bounded_execution_plan_digest=preparation.bounded_execution_plan_digest,
        proposed_repository_mutation_package_digest=preparation.proposed_repository_mutation_package_digest,
        mutation_execution_deadline_at_epoch_seconds=preparation.mutation_execution_deadline_at_epoch_seconds,
    )
    prior = _prior_actor_ids(source_authorization, source_evidence)
    preparation_delay = evidence.prepared_at_epoch_seconds - source_authorization.authorized_at_epoch_seconds
    evidence_age = evidence.prepared_at_epoch_seconds - evidence.captured_at_epoch_seconds
    execution_delay = evidence.mutation_execution_deadline_at_epoch_seconds - evidence.prepared_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "preparation_valid": not preparation_issues(preparation),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_authorization, source_evidence, source_policy, source_record, source_args),
        "source_authorization_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests
        and preparation.source_authorization_id == evidence.source_authorization_id == source_authorization.authorization_id
        and preparation.source_authorization_record_digest == evidence.source_authorization_record_digest == source_record.record_digest,
        "identity_binding_valid": preparation.preparation_id == evidence.preparation_id
        and preparation.preparer_id == evidence.preparer_id
        and preparation.preparer_organization_id == evidence.preparer_organization_id
        and preparation.preparation_evidence_digest == evidence.evidence_digest,
        "execution_preparation_route_binding_valid": preparation.source_execution_preparation_route_digest
        == evidence.source_execution_preparation_route_digest
        == source_authorization.execution_preparation_route_digest,
        "mutation_execution_route_binding_valid": preparation.mutation_execution_route_digest
        == evidence.mutation_execution_route_digest
        == expected_execution_route,
        "transition_package_binding_valid": preparation.transition_package_digest
        == evidence.transition_package_digest
        == source_authorization.transition_package_digest,
        "adopted_state_binding_valid": preparation.adopted_lifecycle_state_digest
        == evidence.adopted_lifecycle_state_digest
        == source_authorization.adopted_lifecycle_state_digest,
        "proposed_repository_mutation_package_binding_valid": preparation.proposed_repository_mutation_package_digest
        == evidence.proposed_repository_mutation_package_digest
        == source_authorization.proposed_repository_mutation_package_digest,
        "bounded_execution_plan_binding_valid": preparation.bounded_execution_plan_digest == evidence.bounded_execution_plan_digest,
        "preparer_allowed": preparation.preparer_id in policy.allowed_preparer_ids,
        "preparer_organization_allowed": preparation.preparer_organization_id in policy.allowed_preparer_organization_ids,
        "preparer_separated_from_authorizer": preparation.preparer_id != source_authorization.authorizer_id,
        "preparer_separated_from_prior_actors": preparation.preparer_id not in prior,
        "preparer_organization_separated": preparation.preparer_organization_id != source_authorization.authorizer_organization_id,
        "objective_allowed": preparation.objective == OBJECTIVE,
        "preparation_delay_valid": 0 <= preparation_delay <= policy.max_preparation_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "execution_delay_valid": 0 < execution_delay <= policy.max_execution_delay_seconds,
        "time_order_valid": source_authorization.authorized_at_epoch_seconds
        <= evidence.preparation_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.prepared_at_epoch_seconds
        < evidence.mutation_execution_deadline_at_epoch_seconds,
        "source_preparation_deadline_valid": evidence.prepared_at_epoch_seconds
        <= source_authorization.execution_preparation_deadline_at_epoch_seconds,
        "external_operation_absent": not evidence.external_operation_performed,
        "repository_change_absent": not evidence.repository_changed,
        "file_write_absent": not evidence.file_written,
        "ref_update_absent": not evidence.ref_updated,
        "branch_move_absent": not evidence.branch_moved,
        "terminal_marker_absent": not evidence.terminal_marker_written,
        "resource_removal_absent": not evidence.resource_removed,
        "preparer_mandate_verified": evidence.preparer_mandate_verified,
        "preparer_authority_verified": evidence.preparer_authority_verified,
        "preparer_identity_confirmed": evidence.preparer_identity_confirmed,
        "authorization_record_fresh": evidence.authorization_record_fresh,
        "bounded_execution_plan_valid": evidence.bounded_execution_plan_valid,
        "sandbox_allocation_valid": evidence.sandbox_allocation_valid,
        "checkpoint_intent_valid": evidence.checkpoint_intent_valid,
        "mutation_package_integrity_valid": evidence.mutation_package_integrity_valid,
        "execution_constraints_valid": evidence.execution_constraints_valid,
        "rollback_plan_valid": evidence.rollback_plan_valid,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = (
    "policy_valid",
    "preparation_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_authorization_ready",
    "source_binding_valid",
    "identity_binding_valid",
    "execution_preparation_route_binding_valid",
    "mutation_execution_route_binding_valid",
    "transition_package_binding_valid",
    "adopted_state_binding_valid",
    "proposed_repository_mutation_package_binding_valid",
    "bounded_execution_plan_binding_valid",
    "preparer_allowed",
    "preparer_organization_allowed",
    "preparer_separated_from_authorizer",
    "preparer_separated_from_prior_actors",
    "preparer_organization_separated",
    "objective_allowed",
    "preparation_delay_valid",
    "evidence_fresh",
    "execution_delay_valid",
    "time_order_valid",
    "source_preparation_deadline_valid",
    "external_operation_absent",
    "repository_change_absent",
    "file_write_absent",
    "ref_update_absent",
    "branch_move_absent",
    "terminal_marker_absent",
    "resource_removal_absent",
)

BLOCKING_CHECKS = (
    "preparer_mandate_verified",
    "preparer_authority_verified",
    "preparer_identity_confirmed",
    "authorization_record_fresh",
    "bounded_execution_plan_valid",
    "sandbox_allocation_valid",
    "checkpoint_intent_valid",
    "mutation_package_integrity_valid",
    "execution_constraints_valid",
    "rollback_plan_valid",
    "no_unresolved_anomaly",
    "recovery_not_in_progress",
    "institutional_hold_absent",
    "emergency_state_absent",
)


def compute_artifact(
    preparation: Rec,
    evidence: Rec,
    policy: Rec,
    source_authorization,
    source_evidence,
    source_policy,
    source_record,
    *source_args: Any,
) -> Rec:
    checks, expected_digests = evaluate(
        preparation, evidence, policy, source_authorization, source_evidence, source_policy, source_record, tuple(source_args)
    )
    checks[SOURCE_ORDER_CHECK] = (
        source_authorization.authorized_at_epoch_seconds
        <= preparation.preparation_requested_at_epoch_seconds
        <= preparation.prepared_at_epoch_seconds
        <= source_authorization.execution_preparation_deadline_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_authorization_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in BLOCKING_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = BLOCKED, failed
        elif preparation.preparation_confirmed:
            status, reason = PREPARED, "prepared_for_separate_bounded_repository_mutation_execution_only"
        else:
            status, reason = BLOCKED, "repository_mutation_execution_preparation_not_confirmed"
    issued = status != REJECTED
    prepared = status == PREPARED
    blocked = status == BLOCKED
    artifact = Rec(
        preparation_id=preparation.preparation_id,
        status=status,
        reason=reason,
        preparer_id=preparation.preparer_id,
        preparer_organization_id=preparation.preparer_organization_id,
        source_authorization_id=preparation.source_authorization_id,
        source_authorization_record_digest=preparation.source_authorization_record_digest,
        source_authorizer_id=preparation.source_authorizer_id,
        source_repository_review_id=preparation.source_repository_review_id,
        transition_package_digest=preparation.transition_package_digest,
        adopted_lifecycle_state_digest=preparation.adopted_lifecycle_state_digest,
        source_execution_preparation_route_digest=preparation.source_execution_preparation_route_digest,
        proposed_repository_mutation_package_digest=preparation.proposed_repository_mutation_package_digest,
        bounded_execution_plan_digest=preparation.bounded_execution_plan_digest,
        mutation_execution_route_digest=preparation.mutation_execution_route_digest,
        mutation_execution_deadline_at_epoch_seconds=preparation.mutation_execution_deadline_at_epoch_seconds,
        subject_id=preparation.subject_id,
        requester_id=preparation.requester_id,
        policy_digest=policy.policy_digest,
        preparation_digest=preparation.preparation_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_authorization_ready=checks["source_authorization_ready"],
        repository_mutation_execution_preparation_record_issued=issued,
        repository_mutation_execution_preparation_completed=issued,
        repository_mutation_execution_prepared=prepared,
        repository_mutation_execution_preparation_blocked=blocked,
        repository_mutation_execution_preparation_rejected=status == REJECTED,
        ready_for_separate_bounded_repository_mutation_execution=prepared,
        bounded_repository_mutation_execution_required_next=prepared,
        bounded_repository_mutation_execution_route_required_next=prepared,
        repository_mutation_execution_preparation_replan_required_next=blocked,
        repository_mutation_execution_preparation_replan_route_required_next=blocked,
        repository_mutation_performed=False,
        file_written=False,
        ref_updated=False,
        branch_moved=False,
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
        raise ValueError("lifecycle_repository_mutation_execution_preparation_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("repository_mutation_execution_preparation_recomputation_mismatch")
    if artifact.status not in (PREPARED, BLOCKED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == PREPARED and not all((
        artifact.repository_mutation_execution_preparation_record_issued,
        artifact.repository_mutation_execution_preparation_completed,
        artifact.repository_mutation_execution_prepared,
        artifact.ready_for_separate_bounded_repository_mutation_execution,
        artifact.bounded_repository_mutation_execution_required_next,
        artifact.bounded_repository_mutation_execution_route_required_next,
        not artifact.repository_mutation_performed,
        not artifact.repository_changed,
    )):
        issues.append("prepared_gate_invalid")
    if artifact.status == BLOCKED and not all((
        artifact.repository_mutation_execution_preparation_record_issued,
        artifact.repository_mutation_execution_preparation_completed,
        artifact.repository_mutation_execution_preparation_blocked,
        not artifact.bounded_repository_mutation_execution_required_next,
        artifact.repository_mutation_execution_preparation_replan_required_next,
    )):
        issues.append("blocked_gate_invalid")
    if artifact.status == REJECTED and any((
        artifact.repository_mutation_execution_preparation_record_issued,
        artifact.repository_mutation_execution_preparation_completed,
        artifact.bounded_repository_mutation_execution_required_next,
        artifact.repository_mutation_execution_preparation_replan_required_next,
    )):
        issues.append("rejected_record_issued")
    if any((
        artifact.repository_mutation_performed,
        artifact.file_written,
        artifact.ref_updated,
        artifact.branch_moved,
        artifact.authority_changed,
        artifact.quiescence_state_changed,
        artifact.terminal_state_changed,
        artifact.terminal_marker_written,
        artifact.resource_removed,
        artifact.external_operation_performed,
        artifact.repository_changed,
    )):
        issues.append("repository_or_external_effect_performed")
    if not artifact.repository_read_only:
        issues.append("repository_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
