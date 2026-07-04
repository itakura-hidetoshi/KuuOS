#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_archive_v0_35 import (
    ARCHIVED as SOURCE_READY,
    artifact_issues as source_artifact_issues,
    all_source_digests as prior_source_digests,
)

VERSION = "kuuos_lifecycle_completion_v0_36"
COMPLETED = "LIFECYCLE_COMPLETION_COMPLETE"
ALERT = "LIFECYCLE_COMPLETION_ALERT"
REJECTED = "LIFECYCLE_COMPLETION_REJECTED"
OBJECTIVE = "COMPLETE_LIFECYCLE_STAGE_V0_36_ONLY"
SOURCE_ORDER_CHECK = "source_stage_precedes_completion"


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


def completion_digest(value: Rec) -> str:
    return _digest(value, "completion_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(policy_id: str, *, allowed_authority_ids: tuple[str, ...], allowed_authority_organization_ids: tuple[str, ...], max_delay_seconds: int = 900, max_evidence_age_seconds: int = 300) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_authority_ids=_canon(allowed_authority_ids),
        allowed_authority_organization_ids=_canon(allowed_authority_organization_ids),
        max_delay_seconds=max_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        source_ready_required=True,
        source_recomputation_required=True,
        completion_receipt_required=True,
        no_following_route_required=True,
        memorial_read_only_required=True,
        covenant_active_required=True,
        repository_read_only=True,
        repository_change_absent_required=True,
        external_operation_absent_required=True,
        policy_digest="",
        version=VERSION,
    )
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_completion_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_authority_ids or not value.allowed_authority_organization_ids:
        issues.append("allowed_authority_missing")
    if min(value.max_delay_seconds, value.max_evidence_age_seconds) <= 0:
        issues.append("bound_invalid")
    if not all((value.source_ready_required, value.source_recomputation_required, value.completion_receipt_required, value.no_following_route_required, value.memorial_read_only_required, value.covenant_active_required, value.repository_read_only, value.repository_change_absent_required, value.external_operation_absent_required)):
        issues.append("policy_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(source_stage, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = prior_source_digests(source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:]))
    result.update(
        lifecycle_stage_v0_35=source_stage.archive_digest,
        lifecycle_stage_v0_35_evidence=source_evidence.evidence_digest,
        lifecycle_stage_v0_35_policy=source_policy.policy_digest,
        lifecycle_stage_v0_35_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(source_stage, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_stage, source_evidence, source_policy, *source_args)


def expected_terminal_digest(source_stage, source_record, *, completion_id: str, authority_id: str, completion_receipt_digest: str) -> str:
    return canonical_digest({
        "source_id": source_stage.archive_id,
        "source_record_digest": source_record.record_digest,
        "completion_id": completion_id,
        "authority_id": authority_id,
        "target_id": source_stage.apoptosis_target_id,
        "source_route_digest": source_stage.final_closure_route_digest,
        "completion_receipt_digest": completion_receipt_digest,
        "covenant_digest": source_stage.covenant_digest,
    })


def make_evidence(source_stage, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(
        source_id=source_stage.archive_id,
        source_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(source_stage, source_evidence, source_policy, source_record, source_args),
        target_id=source_stage.apoptosis_target_id,
        memory_seal_digest=source_stage.memory_seal_digest,
        boundary_digest=source_stage.archive_boundary_digest,
        memorial_record_digest=source_stage.memorial_record_digest,
        covenant_digest=source_stage.covenant_digest,
        source_route_digest=source_stage.final_closure_route_digest,
    )
    values.update(overrides)
    if "terminal_digest" not in values:
        values["terminal_digest"] = expected_terminal_digest(source_stage, source_record, completion_id=values["completion_id"], authority_id=values["authority_id"], completion_receipt_digest=values["completion_receipt_digest"])
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_completion_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = ("evidence_id", "completion_id", "authority_id", "authority_organization_id", "mandate_receipt_digest", "authority_receipt_digest", "identity_confirmation_digest", "target_id", "completion_receipt_digest", "terminal_digest", "memorial_record_digest", "covenant_digest")
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.completed_at_epoch_seconds) < 0:
        issues.append("negative_completion_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_completion(completion_id: str, authority_id: str, authority_organization_id: str, requested_at_epoch_seconds: int, completed_at_epoch_seconds: int, source_stage, source_record, completion_evidence: Rec, *, completion_receipt_digest: str, terminal_digest: str, completion_confirmed: bool, alert_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(
        completion_id=completion_id,
        authority_id=authority_id,
        authority_organization_id=authority_organization_id,
        objective=objective,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        source_id=source_stage.archive_id,
        source_record_digest=source_record.record_digest,
        target_id=source_stage.apoptosis_target_id,
        memory_seal_digest=source_stage.memory_seal_digest,
        boundary_digest=source_stage.archive_boundary_digest,
        completion_receipt_digest=completion_receipt_digest,
        terminal_digest=terminal_digest,
        memorial_record_digest=source_stage.memorial_record_digest,
        covenant_digest=source_stage.covenant_digest,
        completion_evidence_digest=completion_evidence.evidence_digest,
        completion_confirmed=completion_confirmed,
        alert_reason_digest=alert_reason_digest,
        completion_digest="",
        version=VERSION,
    )
    value.completion_digest = completion_digest(value)
    issues = completion_issues(value)
    if issues:
        raise ValueError("lifecycle_completion_invalid:" + issues[0])
    return value


def completion_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("alert_reason_digest", "completion_digest", "version", "completion_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_completion_field_missing")
            break
    if not value.completion_confirmed and not value.alert_reason_digest:
        issues.append("alert_reason_missing")
    if min(value.requested_at_epoch_seconds, value.completed_at_epoch_seconds) < 0:
        issues.append("negative_completion_time")
    if value.completion_digest != completion_digest(value):
        issues.append("completion_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all((
        record.status == SOURCE_READY,
        record.archive_record_issued,
        record.archive_completed,
        record.archive_bound,
        record.ready_for_final_closure,
        record.final_closure_required_next,
        record.final_closure_route_required_next,
        record.authority_remains_closed,
        record.dependency_ingress_remains_closed,
        record.activation_route_remains_closed,
        record.covenant_active,
        record.memorial_record_read_only,
        not record.repository_changed,
        not record.external_operation_performed,
    ))


def evaluate(completion: Rec, evidence: Rec, policy: Rec, source_stage, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_stage, source_evidence, source_policy, source_record, source_args)
    expected_terminal = expected_terminal_digest(source_stage, source_record, completion_id=completion.completion_id, authority_id=completion.authority_id, completion_receipt_digest=completion.completion_receipt_digest)
    delay = evidence.completed_at_epoch_seconds - source_stage.archived_at_epoch_seconds
    age = evidence.completed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "completion_valid": not completion_issues(completion),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_stage, source_evidence, source_policy, source_record, source_args),
        "source_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and completion.source_id == evidence.source_id == source_stage.archive_id and completion.source_record_digest == evidence.source_record_digest == source_record.record_digest,
        "identity_binding_valid": completion.completion_id == evidence.completion_id and completion.authority_id == evidence.authority_id and completion.authority_organization_id == evidence.authority_organization_id and completion.completion_evidence_digest == evidence.evidence_digest,
        "target_binding_valid": completion.target_id == evidence.target_id == source_stage.apoptosis_target_id,
        "terminal_binding_valid": completion.terminal_digest == evidence.terminal_digest == expected_terminal,
        "receipt_valid": completion.completion_receipt_digest == evidence.completion_receipt_digest and evidence.completion_receipt_confirmed,
        "memory_seal_valid": completion.memory_seal_digest == evidence.memory_seal_digest and evidence.memory_seal_confirmed,
        "boundary_valid": completion.boundary_digest == evidence.boundary_digest and evidence.boundary_confirmed,
        "memorial_read_only": completion.memorial_record_digest == evidence.memorial_record_digest and evidence.memorial_record_read_only,
        "covenant_active": completion.covenant_digest == evidence.covenant_digest and evidence.covenant_active,
        "no_following_route": evidence.no_following_route,
        "authority_allowed": completion.authority_id in policy.allowed_authority_ids,
        "authority_organization_allowed": completion.authority_organization_id in policy.allowed_authority_organization_ids,
        "objective_allowed": completion.objective == OBJECTIVE,
        "delay_valid": 0 <= delay <= policy.max_delay_seconds,
        "evidence_fresh": 0 <= age <= policy.max_evidence_age_seconds,
        "time_order_valid": source_stage.archived_at_epoch_seconds <= evidence.requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.completed_at_epoch_seconds,
        "authority_remains_closed": evidence.authority_closed,
        "dependency_ingress_remains_closed": evidence.dependency_ingress_closed,
        "activation_route_remains_closed": evidence.activation_route_closed,
        "no_reactivation_route": not evidence.reactivation_route_present,
        "repository_change_absent": not evidence.repository_changed,
        "external_operation_absent": not evidence.external_operation_performed,
        "mandate_verified": evidence.mandate_verified,
        "authority_verified": evidence.authority_verified,
        "identity_confirmed": evidence.identity_confirmed,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = ("policy_valid", "completion_valid", "evidence_valid", "source_recomputed_valid", "source_ready", "source_binding_valid", "identity_binding_valid", "target_binding_valid", "terminal_binding_valid", "receipt_valid", "memory_seal_valid", "boundary_valid", "memorial_read_only", "covenant_active", "no_following_route", "authority_allowed", "authority_organization_allowed", "objective_allowed", "delay_valid", "evidence_fresh", "time_order_valid", "repository_change_absent", "external_operation_absent")
ALERT_CHECKS = ("authority_remains_closed", "dependency_ingress_remains_closed", "activation_route_remains_closed", "no_reactivation_route", "mandate_verified", "authority_verified", "identity_confirmed", "institutional_hold_absent", "emergency_state_absent")


def compute_artifact(completion: Rec, evidence: Rec, policy: Rec, source_stage, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(completion, evidence, policy, source_stage, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_stage.archived_at_epoch_seconds <= completion.requested_at_epoch_seconds <= completion.completed_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_policy_terminal_or_binding_invalid"
    else:
        failed = next((name for name in ALERT_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = ALERT, failed
        elif completion.completion_confirmed:
            status, reason = COMPLETED, "lifecycle_completion_complete"
        else:
            status, reason = ALERT, "completion_not_confirmed"
    issued = status != REJECTED
    done = status == COMPLETED
    alert = status == ALERT
    artifact = Rec(
        completion_id=completion.completion_id,
        status=status,
        reason=reason,
        target_id=completion.target_id,
        memory_seal_digest=completion.memory_seal_digest,
        boundary_digest=completion.boundary_digest,
        completion_receipt_digest=completion.completion_receipt_digest,
        terminal_digest=completion.terminal_digest,
        memorial_record_digest=completion.memorial_record_digest,
        covenant_digest=completion.covenant_digest,
        policy_digest=policy.policy_digest,
        completion_digest=completion.completion_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_ready=checks["source_ready"],
        completion_record_issued=issued,
        completion_completed=done,
        completion_alert=alert,
        completion_rejected=status == REJECTED,
        lifecycle_terminal=done,
        following_route_required_next=False,
        following_route_permitted=False,
        completion_response_required_next=alert,
        completion_response_route_required_next=alert,
        authority_remains_closed=done and evidence.authority_closed,
        dependency_ingress_remains_closed=done and evidence.dependency_ingress_closed,
        activation_route_remains_closed=done and evidence.activation_route_closed,
        covenant_active=done and evidence.covenant_active,
        memorial_record_read_only=done and evidence.memorial_record_read_only,
        repository_changed=False,
        external_operation_performed=False,
        record_digest="",
        version=VERSION,
    )
    artifact.record_digest = record_digest(artifact)
    return artifact


def verify_artifact(*args: Any, **kwargs: Any) -> Rec:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError("lifecycle_completion_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("completion_recomputation_mismatch")
    if artifact.status not in (COMPLETED, ALERT, REJECTED):
        issues.append("status_invalid")
    if artifact.status == COMPLETED and not all((artifact.completion_record_issued, artifact.completion_completed, artifact.lifecycle_terminal, not artifact.following_route_required_next, not artifact.following_route_permitted, artifact.authority_remains_closed, artifact.dependency_ingress_remains_closed, artifact.activation_route_remains_closed, artifact.covenant_active, artifact.memorial_record_read_only)):
        issues.append("complete_gate_invalid")
    if artifact.status == ALERT and not all((artifact.completion_record_issued, artifact.completion_alert, not artifact.lifecycle_terminal, artifact.completion_response_required_next)):
        issues.append("alert_gate_invalid")
    if artifact.status == REJECTED and any((artifact.completion_record_issued, artifact.completion_completed, artifact.completion_response_required_next)):
        issues.append("rejected_record_issued")
    if artifact.repository_changed or artifact.external_operation_performed:
        issues.append("completion_layer_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
