#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_post_apoptosis_observation_v0_33 import (
    STABLE as SOURCE_STABLE,
    artifact_issues as source_artifact_issues,
    all_source_digests as observation_source_digests,
)

VERSION = "kuuos_lifecycle_long_term_memory_v0_34"
SEALED = "LIFECYCLE_LONG_TERM_MEMORY_SEALED_FOR_NON_RESURRECTION_ARCHIVE"
ALERT = "LIFECYCLE_LONG_TERM_MEMORY_ALERT"
REJECTED = "LIFECYCLE_LONG_TERM_MEMORY_REJECTED"
OBJECTIVE = "SEAL_STABLE_POST_APOPTOSIS_MEMORY_ONLY"
SOURCE_ORDER_CHECK = "source_observation_precedes_long_term_memory_sealing"


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


def memory_digest(value: Rec) -> str:
    return _digest(value, "memory_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(
    policy_id: str,
    *,
    allowed_memory_steward_ids: tuple[str, ...],
    allowed_memory_steward_organization_ids: tuple[str, ...],
    max_memory_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_memory_steward_ids=_canon(allowed_memory_steward_ids),
        allowed_memory_steward_organization_ids=_canon(allowed_memory_steward_organization_ids),
        max_memory_delay_seconds=max_memory_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        stable_source_required=True,
        source_recomputation_required=True,
        memory_seal_required=True,
        archive_boundary_required=True,
        memorial_read_only_required=True,
        non_resurrection_required=True,
        authority_closed_required=True,
        dependency_ingress_closed_required=True,
        activation_route_closed_required=True,
        retrieval_read_only_required=True,
        repository_read_only=True,
        repository_change_absent_required=True,
        external_operation_absent_required=True,
        policy_digest="",
        version=VERSION,
    )
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_long_term_memory_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_memory_steward_ids or not value.allowed_memory_steward_organization_ids:
        issues.append("allowed_memory_steward_missing")
    if min(value.max_memory_delay_seconds, value.max_evidence_age_seconds) <= 0:
        issues.append("bound_invalid")
    if not all((
        value.memory_seal_required,
        value.archive_boundary_required,
        value.memorial_read_only_required,
        value.non_resurrection_required,
        value.retrieval_read_only_required,
        value.repository_read_only,
        value.repository_change_absent_required,
        value.external_operation_absent_required,
    )):
        issues.append("memory_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(source_observation, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = observation_source_digests(
        source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:])
    )
    result.update(
        lifecycle_post_apoptosis_observation=source_observation.observation_digest,
        lifecycle_post_apoptosis_observation_evidence=source_evidence.evidence_digest,
        lifecycle_post_apoptosis_observation_policy=source_policy.policy_digest,
        lifecycle_post_apoptosis_observation_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(source_observation, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_observation, source_evidence, source_policy, *source_args)


def expected_archive_route_digest(source_observation, source_record, *, memory_id: str, memory_steward_id: str, memory_seal_digest: str, archive_boundary_digest: str) -> str:
    return canonical_digest({
        "source_observation_id": source_observation.observation_id,
        "source_observation_record_digest": source_record.record_digest,
        "memory_id": memory_id,
        "memory_steward_id": memory_steward_id,
        "apoptosis_target_id": source_observation.apoptosis_target_id,
        "quarantine_boundary_digest": source_observation.quarantine_boundary_digest,
        "memory_seal_digest": memory_seal_digest,
        "archive_boundary_digest": archive_boundary_digest,
        "non_resurrection_covenant_digest": source_observation.non_resurrection_covenant_digest,
    })


def make_evidence(source_observation, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(
        source_observation_id=source_observation.observation_id,
        source_observation_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(source_observation, source_evidence, source_policy, source_record, source_args),
        apoptosis_target_id=source_observation.apoptosis_target_id,
        quarantine_boundary_digest=source_observation.quarantine_boundary_digest,
        stability_window_digest=source_observation.stability_window_digest,
        memorial_record_digest=source_observation.memorial_record_digest,
        non_resurrection_covenant_digest=source_observation.non_resurrection_covenant_digest,
        long_term_memory_route_digest=source_observation.long_term_memory_route_digest,
    )
    values.update(overrides)
    if "archive_route_digest" not in values:
        values["archive_route_digest"] = expected_archive_route_digest(
            source_observation,
            source_record,
            memory_id=values["memory_id"],
            memory_steward_id=values["memory_steward_id"],
            memory_seal_digest=values["memory_seal_digest"],
            archive_boundary_digest=values["archive_boundary_digest"],
        )
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_long_term_memory_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = (
        "evidence_id",
        "memory_id",
        "memory_steward_id",
        "memory_steward_organization_id",
        "memory_steward_mandate_receipt_digest",
        "memory_steward_authority_receipt_digest",
        "memory_steward_identity_confirmation_digest",
        "apoptosis_target_id",
        "memory_seal_digest",
        "archive_boundary_digest",
        "archive_route_digest",
        "memorial_record_digest",
        "non_resurrection_covenant_digest",
    )
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.memory_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.sealed_at_epoch_seconds) < 0:
        issues.append("negative_memory_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_memory(memory_id: str, memory_steward_id: str, memory_steward_organization_id: str, memory_requested_at_epoch_seconds: int, sealed_at_epoch_seconds: int, source_observation, source_record, memory_evidence: Rec, *, memory_seal_digest: str, archive_boundary_digest: str, archive_route_digest: str, memory_confirmed: bool, alert_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(
        memory_id=memory_id,
        memory_steward_id=memory_steward_id,
        memory_steward_organization_id=memory_steward_organization_id,
        objective=objective,
        memory_requested_at_epoch_seconds=memory_requested_at_epoch_seconds,
        sealed_at_epoch_seconds=sealed_at_epoch_seconds,
        source_observation_id=source_observation.observation_id,
        source_observation_record_digest=source_record.record_digest,
        apoptosis_target_id=source_observation.apoptosis_target_id,
        quarantine_boundary_digest=source_observation.quarantine_boundary_digest,
        stability_window_digest=source_observation.stability_window_digest,
        memory_seal_digest=memory_seal_digest,
        archive_boundary_digest=archive_boundary_digest,
        archive_route_digest=archive_route_digest,
        memorial_record_digest=source_observation.memorial_record_digest,
        non_resurrection_covenant_digest=source_observation.non_resurrection_covenant_digest,
        memory_evidence_digest=memory_evidence.evidence_digest,
        memory_confirmed=memory_confirmed,
        alert_reason_digest=alert_reason_digest,
        memory_digest="",
        version=VERSION,
    )
    value.memory_digest = memory_digest(value)
    issues = memory_issues(value)
    if issues:
        raise ValueError("lifecycle_long_term_memory_invalid:" + issues[0])
    return value


def memory_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("alert_reason_digest", "memory_digest", "version", "memory_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_memory_field_missing")
            break
    if not value.memory_confirmed and not value.alert_reason_digest:
        issues.append("alert_reason_missing")
    if min(value.memory_requested_at_epoch_seconds, value.sealed_at_epoch_seconds) < 0:
        issues.append("negative_memory_time")
    if value.memory_digest != memory_digest(value):
        issues.append("memory_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all((
        record.status == SOURCE_STABLE,
        record.post_apoptosis_observation_record_issued,
        record.post_apoptosis_observation_completed,
        record.post_apoptosis_observation_stable,
        record.ready_for_long_term_memory,
        record.long_term_memory_required_next,
        record.long_term_memory_route_required_next,
        record.authority_remains_closed,
        record.dependency_ingress_remains_closed,
        record.activation_route_remains_closed,
        record.non_resurrection_covenant_active,
        record.memorial_record_read_only,
        not record.repository_changed,
        not record.external_operation_performed,
    ))


def evaluate(memory: Rec, evidence: Rec, policy: Rec, source_observation, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_observation, source_evidence, source_policy, source_record, source_args)
    expected_route = expected_archive_route_digest(
        source_observation,
        source_record,
        memory_id=memory.memory_id,
        memory_steward_id=memory.memory_steward_id,
        memory_seal_digest=memory.memory_seal_digest,
        archive_boundary_digest=memory.archive_boundary_digest,
    )
    memory_delay = evidence.sealed_at_epoch_seconds - source_observation.observed_at_epoch_seconds
    evidence_age = evidence.sealed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "memory_valid": not memory_issues(memory),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_observation, source_evidence, source_policy, source_record, source_args),
        "source_observation_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and memory.source_observation_id == evidence.source_observation_id == source_observation.observation_id and memory.source_observation_record_digest == evidence.source_observation_record_digest == source_record.record_digest,
        "identity_binding_valid": memory.memory_id == evidence.memory_id and memory.memory_steward_id == evidence.memory_steward_id and memory.memory_steward_organization_id == evidence.memory_steward_organization_id and memory.memory_evidence_digest == evidence.evidence_digest,
        "apoptosis_target_binding_valid": memory.apoptosis_target_id == evidence.apoptosis_target_id == source_observation.apoptosis_target_id,
        "archive_route_binding_valid": memory.archive_route_digest == evidence.archive_route_digest == expected_route,
        "memory_seal_valid": memory.memory_seal_digest == evidence.memory_seal_digest and evidence.memory_seal_confirmed,
        "archive_boundary_valid": memory.archive_boundary_digest == evidence.archive_boundary_digest and evidence.archive_boundary_confirmed,
        "memorial_read_only": memory.memorial_record_digest == evidence.memorial_record_digest and evidence.memorial_record_read_only,
        "non_resurrection_maintained": memory.non_resurrection_covenant_digest == evidence.non_resurrection_covenant_digest and evidence.non_resurrection_covenant_active,
        "retrieval_read_only": evidence.retrieval_read_only,
        "steward_allowed": memory.memory_steward_id in policy.allowed_memory_steward_ids,
        "steward_organization_allowed": memory.memory_steward_organization_id in policy.allowed_memory_steward_organization_ids,
        "objective_allowed": memory.objective == OBJECTIVE,
        "memory_delay_valid": 0 <= memory_delay <= policy.max_memory_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "time_order_valid": source_observation.observed_at_epoch_seconds <= evidence.memory_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.sealed_at_epoch_seconds,
        "authority_remains_closed": evidence.authority_closed,
        "dependency_ingress_remains_closed": evidence.dependency_ingress_closed,
        "activation_route_remains_closed": evidence.activation_route_closed,
        "no_reactivation_route": not evidence.reactivation_route_present,
        "repository_change_absent": not evidence.repository_changed,
        "external_operation_absent": not evidence.external_operation_performed,
        "steward_mandate_verified": evidence.memory_steward_mandate_verified,
        "steward_authority_verified": evidence.memory_steward_authority_verified,
        "steward_identity_confirmed": evidence.memory_steward_identity_confirmed,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = (
    "policy_valid", "memory_valid", "evidence_valid", "source_recomputed_valid", "source_observation_ready", "source_binding_valid", "identity_binding_valid", "apoptosis_target_binding_valid", "archive_route_binding_valid", "memory_seal_valid", "archive_boundary_valid", "memorial_read_only", "non_resurrection_maintained", "retrieval_read_only", "steward_allowed", "steward_organization_allowed", "objective_allowed", "memory_delay_valid", "evidence_fresh", "time_order_valid", "repository_change_absent", "external_operation_absent",
)
ALERT_CHECKS = (
    "authority_remains_closed", "dependency_ingress_remains_closed", "activation_route_remains_closed", "no_reactivation_route", "steward_mandate_verified", "steward_authority_verified", "steward_identity_confirmed", "institutional_hold_absent", "emergency_state_absent",
)


def compute_artifact(memory: Rec, evidence: Rec, policy: Rec, source_observation, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(memory, evidence, policy, source_observation, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_observation.observed_at_epoch_seconds <= memory.memory_requested_at_epoch_seconds <= memory.sealed_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_observation_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in ALERT_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = ALERT, failed
        elif memory.memory_confirmed:
            status, reason = SEALED, "long_term_memory_sealed_for_non_resurrection_archive"
        else:
            status, reason = ALERT, "long_term_memory_not_confirmed"
    issued = status != REJECTED
    sealed = status == SEALED
    alert = status == ALERT
    artifact = Rec(
        memory_id=memory.memory_id,
        status=status,
        reason=reason,
        apoptosis_target_id=memory.apoptosis_target_id,
        quarantine_boundary_digest=memory.quarantine_boundary_digest,
        stability_window_digest=memory.stability_window_digest,
        memory_seal_digest=memory.memory_seal_digest,
        archive_boundary_digest=memory.archive_boundary_digest,
        archive_route_digest=memory.archive_route_digest,
        memorial_record_digest=memory.memorial_record_digest,
        non_resurrection_covenant_digest=memory.non_resurrection_covenant_digest,
        policy_digest=policy.policy_digest,
        memory_digest=memory.memory_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_observation_ready=checks["source_observation_ready"],
        long_term_memory_record_issued=issued,
        long_term_memory_completed=issued,
        long_term_memory_sealed=sealed,
        long_term_memory_alert=alert,
        long_term_memory_rejected=status == REJECTED,
        ready_for_non_resurrection_archive=sealed,
        non_resurrection_archive_required_next=sealed,
        non_resurrection_archive_route_required_next=sealed,
        long_term_memory_response_required_next=alert,
        long_term_memory_response_route_required_next=alert,
        authority_remains_closed=sealed and evidence.authority_closed,
        dependency_ingress_remains_closed=sealed and evidence.dependency_ingress_closed,
        activation_route_remains_closed=sealed and evidence.activation_route_closed,
        non_resurrection_covenant_active=sealed and evidence.non_resurrection_covenant_active,
        memorial_record_read_only=sealed and evidence.memorial_record_read_only,
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
        raise ValueError("lifecycle_long_term_memory_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("long_term_memory_recomputation_mismatch")
    if artifact.status not in (SEALED, ALERT, REJECTED):
        issues.append("status_invalid")
    if artifact.status == SEALED and not all((artifact.long_term_memory_record_issued, artifact.long_term_memory_completed, artifact.long_term_memory_sealed, artifact.ready_for_non_resurrection_archive, artifact.non_resurrection_archive_required_next, artifact.authority_remains_closed, artifact.dependency_ingress_remains_closed, artifact.activation_route_remains_closed, artifact.non_resurrection_covenant_active, artifact.memorial_record_read_only)):
        issues.append("sealed_gate_invalid")
    if artifact.status == ALERT and not all((artifact.long_term_memory_record_issued, artifact.long_term_memory_completed, artifact.long_term_memory_alert, not artifact.non_resurrection_archive_required_next, artifact.long_term_memory_response_required_next)):
        issues.append("alert_gate_invalid")
    if artifact.status == REJECTED and any((artifact.long_term_memory_record_issued, artifact.long_term_memory_completed, artifact.non_resurrection_archive_required_next, artifact.long_term_memory_response_required_next)):
        issues.append("rejected_record_issued")
    if artifact.repository_changed or artifact.external_operation_performed:
        issues.append("memory_layer_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
