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

VERSION = "kuuos_lifecycle_post_apoptosis_long_term_memory_v0_34"
MEMORIZED = "LIFECYCLE_POST_APOPTOSIS_LONG_TERM_MEMORY_BOUND_FOR_PERIODIC_REVIEW"
ALERT = "LIFECYCLE_POST_APOPTOSIS_LONG_TERM_MEMORY_ALERT"
REJECTED = "LIFECYCLE_POST_APOPTOSIS_LONG_TERM_MEMORY_REJECTED"
OBJECTIVE = "BIND_STABLE_POST_APOPTOSIS_OBSERVATION_TO_LONG_TERM_MEMORY_ONLY"
SOURCE_ORDER_CHECK = "source_observation_precedes_long_term_memory_binding"


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
    max_memory_binding_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_memory_steward_ids=_canon(allowed_memory_steward_ids),
        allowed_memory_steward_organization_ids=_canon(allowed_memory_steward_organization_ids),
        max_memory_binding_delay_seconds=max_memory_binding_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        stable_source_required=True,
        source_recomputation_required=True,
        memorial_record_read_only_required=True,
        memory_record_immutable_required=True,
        non_resurrection_required=True,
        access_limited_required=True,
        periodic_review_route_required_next=True,
        repository_read_only=True,
        repository_change_absent_required=True,
        external_operation_absent_required=True,
        policy_digest="",
        version=VERSION,
    )
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("post_apoptosis_long_term_memory_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_memory_steward_ids or not value.allowed_memory_steward_organization_ids:
        issues.append("allowed_memory_steward_missing")
    if min(value.max_memory_binding_delay_seconds, value.max_evidence_age_seconds) <= 0:
        issues.append("bound_invalid")
    if not all((
        value.memorial_record_read_only_required,
        value.memory_record_immutable_required,
        value.non_resurrection_required,
        value.access_limited_required,
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


def expected_periodic_review_route_digest(source_observation, source_record, *, memory_id: str, steward_id: str, memory_record_digest: str, access_policy_digest: str) -> str:
    return canonical_digest({
        "source_observation_id": source_observation.observation_id,
        "source_observation_record_digest": source_record.record_digest,
        "memory_id": memory_id,
        "steward_id": steward_id,
        "apoptosis_target_id": source_observation.apoptosis_target_id,
        "memory_record_digest": memory_record_digest,
        "access_policy_digest": access_policy_digest,
        "non_resurrection_covenant_digest": source_observation.non_resurrection_covenant_digest,
    })


def make_evidence(source_observation, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(
        source_observation_id=source_observation.observation_id,
        source_observation_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(source_observation, source_evidence, source_policy, source_record, source_args),
        apoptosis_target_id=source_observation.apoptosis_target_id,
        quarantine_boundary_digest=source_observation.quarantine_boundary_digest,
        memorial_record_digest=source_observation.memorial_record_digest,
        non_resurrection_covenant_digest=source_observation.non_resurrection_covenant_digest,
    )
    values.update(overrides)
    if "periodic_review_route_digest" not in values:
        values["periodic_review_route_digest"] = expected_periodic_review_route_digest(
            source_observation,
            source_record,
            memory_id=values["memory_id"],
            steward_id=values["memory_steward_id"],
            memory_record_digest=values["memory_record_digest"],
            access_policy_digest=values["access_policy_digest"],
        )
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("post_apoptosis_long_term_memory_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = (
        "evidence_id", "memory_id", "memory_steward_id", "memory_steward_organization_id",
        "memory_steward_mandate_receipt_digest", "memory_steward_authority_receipt_digest",
        "memory_steward_identity_confirmation_digest", "apoptosis_target_id", "memory_record_digest",
        "access_policy_digest", "memorial_record_digest", "non_resurrection_covenant_digest",
        "periodic_review_route_digest",
    )
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.memory_binding_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.bound_at_epoch_seconds) < 0:
        issues.append("negative_memory_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_memory(memory_id: str, memory_steward_id: str, memory_steward_organization_id: str, memory_binding_requested_at_epoch_seconds: int, bound_at_epoch_seconds: int, source_observation, source_record, memory_evidence: Rec, *, memory_record_digest: str, access_policy_digest: str, periodic_review_route_digest: str, memory_bound: bool, alert_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(
        memory_id=memory_id,
        memory_steward_id=memory_steward_id,
        memory_steward_organization_id=memory_steward_organization_id,
        objective=objective,
        memory_binding_requested_at_epoch_seconds=memory_binding_requested_at_epoch_seconds,
        bound_at_epoch_seconds=bound_at_epoch_seconds,
        source_observation_id=source_observation.observation_id,
        source_observation_record_digest=source_record.record_digest,
        apoptosis_target_id=source_observation.apoptosis_target_id,
        quarantine_boundary_digest=source_observation.quarantine_boundary_digest,
        memorial_record_digest=source_observation.memorial_record_digest,
        non_resurrection_covenant_digest=source_observation.non_resurrection_covenant_digest,
        memory_record_digest=memory_record_digest,
        access_policy_digest=access_policy_digest,
        periodic_review_route_digest=periodic_review_route_digest,
        memory_evidence_digest=memory_evidence.evidence_digest,
        memory_bound=memory_bound,
        alert_reason_digest=alert_reason_digest,
        memory_digest="",
        version=VERSION,
    )
    value.memory_digest = memory_digest(value)
    issues = memory_issues(value)
    if issues:
        raise ValueError("post_apoptosis_long_term_memory_invalid:" + issues[0])
    return value


def memory_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("alert_reason_digest", "memory_digest", "version", "memory_bound"):
            continue
        if content == "" or content is None:
            issues.append("required_memory_field_missing")
            break
    if not value.memory_bound and not value.alert_reason_digest:
        issues.append("alert_reason_missing")
    if min(value.memory_binding_requested_at_epoch_seconds, value.bound_at_epoch_seconds) < 0:
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
        record.non_resurrection_covenant_active,
        record.memorial_record_read_only,
        not record.repository_changed,
        not record.external_operation_performed,
    ))


def evaluate(memory: Rec, evidence: Rec, policy: Rec, source_observation, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_observation, source_evidence, source_policy, source_record, source_args)
    expected_route = expected_periodic_review_route_digest(
        source_observation,
        source_record,
        memory_id=memory.memory_id,
        steward_id=memory.memory_steward_id,
        memory_record_digest=memory.memory_record_digest,
        access_policy_digest=memory.access_policy_digest,
    )
    memory_delay = evidence.bound_at_epoch_seconds - source_observation.observed_at_epoch_seconds
    evidence_age = evidence.bound_at_epoch_seconds - evidence.captured_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "memory_valid": not memory_issues(memory),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_observation, source_evidence, source_policy, source_record, source_args),
        "source_observation_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and memory.source_observation_id == evidence.source_observation_id == source_observation.observation_id and memory.source_observation_record_digest == evidence.source_observation_record_digest == source_record.record_digest,
        "identity_binding_valid": memory.memory_id == evidence.memory_id and memory.memory_steward_id == evidence.memory_steward_id and memory.memory_steward_organization_id == evidence.memory_steward_organization_id and memory.memory_evidence_digest == evidence.evidence_digest,
        "target_binding_valid": memory.apoptosis_target_id == evidence.apoptosis_target_id == source_observation.apoptosis_target_id,
        "memory_record_binding_valid": memory.memory_record_digest == evidence.memory_record_digest and evidence.memory_record_immutable,
        "access_policy_binding_valid": memory.access_policy_digest == evidence.access_policy_digest and evidence.access_policy_limited,
        "periodic_review_route_binding_valid": memory.periodic_review_route_digest == evidence.periodic_review_route_digest == expected_route,
        "memorial_read_only": memory.memorial_record_digest == evidence.memorial_record_digest and evidence.memorial_record_read_only,
        "non_resurrection_maintained": memory.non_resurrection_covenant_digest == evidence.non_resurrection_covenant_digest and evidence.non_resurrection_covenant_active,
        "steward_allowed": memory.memory_steward_id in policy.allowed_memory_steward_ids,
        "steward_organization_allowed": memory.memory_steward_organization_id in policy.allowed_memory_steward_organization_ids,
        "objective_allowed": memory.objective == OBJECTIVE,
        "memory_delay_valid": 0 <= memory_delay <= policy.max_memory_binding_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "time_order_valid": source_observation.observed_at_epoch_seconds <= evidence.memory_binding_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.bound_at_epoch_seconds,
        "no_reactivation_route": not evidence.reactivation_route_present,
        "no_boundary_drift": not evidence.quarantine_boundary_drift_detected,
        "repository_change_absent": not evidence.repository_changed,
        "external_operation_absent": not evidence.external_operation_performed,
        "steward_mandate_verified": evidence.memory_steward_mandate_verified,
        "steward_authority_verified": evidence.memory_steward_authority_verified,
        "steward_identity_confirmed": evidence.memory_steward_identity_confirmed,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = (
    "policy_valid", "memory_valid", "evidence_valid", "source_recomputed_valid", "source_observation_ready", "source_binding_valid", "identity_binding_valid", "target_binding_valid", "memory_record_binding_valid", "access_policy_binding_valid", "periodic_review_route_binding_valid", "memorial_read_only", "non_resurrection_maintained", "steward_allowed", "steward_organization_allowed", "objective_allowed", "memory_delay_valid", "evidence_fresh", "time_order_valid", "repository_change_absent", "external_operation_absent",
)
ALERT_CHECKS = (
    "no_reactivation_route", "no_boundary_drift", "steward_mandate_verified", "steward_authority_verified", "steward_identity_confirmed",
)


def compute_artifact(memory: Rec, evidence: Rec, policy: Rec, source_observation, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(memory, evidence, policy, source_observation, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_observation.observed_at_epoch_seconds <= memory.memory_binding_requested_at_epoch_seconds <= memory.bound_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_observation_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in ALERT_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = ALERT, failed
        elif memory.memory_bound:
            status, reason = MEMORIZED, "post_apoptosis_memory_bound_for_periodic_review"
        else:
            status, reason = ALERT, "post_apoptosis_memory_not_bound"
    issued = status != REJECTED
    memorized = status == MEMORIZED
    alert = status == ALERT
    artifact = Rec(
        memory_id=memory.memory_id,
        status=status,
        reason=reason,
        apoptosis_target_id=memory.apoptosis_target_id,
        memory_record_digest=memory.memory_record_digest,
        access_policy_digest=memory.access_policy_digest,
        periodic_review_route_digest=memory.periodic_review_route_digest,
        memorial_record_digest=memory.memorial_record_digest,
        non_resurrection_covenant_digest=memory.non_resurrection_covenant_digest,
        policy_digest=policy.policy_digest,
        memory_digest=memory.memory_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_observation_ready=checks["source_observation_ready"],
        long_term_memory_record_issued=issued,
        long_term_memory_binding_completed=issued,
        long_term_memory_bound=memorized,
        long_term_memory_alert=alert,
        long_term_memory_rejected=status == REJECTED,
        ready_for_periodic_review=memorized,
        periodic_review_required_next=memorized,
        periodic_review_route_required_next=memorized,
        memory_response_required_next=alert,
        memory_response_route_required_next=alert,
        memory_record_immutable=memorized and evidence.memory_record_immutable,
        access_policy_limited=memorized and evidence.access_policy_limited,
        non_resurrection_covenant_active=memorized and evidence.non_resurrection_covenant_active,
        memorial_record_read_only=memorized and evidence.memorial_record_read_only,
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
        raise ValueError("post_apoptosis_long_term_memory_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("long_term_memory_recomputation_mismatch")
    if artifact.status not in (MEMORIZED, ALERT, REJECTED):
        issues.append("status_invalid")
    if artifact.status == MEMORIZED and not all((artifact.long_term_memory_record_issued, artifact.long_term_memory_binding_completed, artifact.long_term_memory_bound, artifact.ready_for_periodic_review, artifact.periodic_review_required_next, artifact.memory_record_immutable, artifact.access_policy_limited, artifact.non_resurrection_covenant_active, artifact.memorial_record_read_only)):
        issues.append("memorized_gate_invalid")
    if artifact.status == ALERT and not all((artifact.long_term_memory_record_issued, artifact.long_term_memory_binding_completed, artifact.long_term_memory_alert, not artifact.periodic_review_required_next, artifact.memory_response_required_next)):
        issues.append("alert_gate_invalid")
    if artifact.status == REJECTED and any((artifact.long_term_memory_record_issued, artifact.long_term_memory_binding_completed, artifact.periodic_review_required_next, artifact.memory_response_required_next)):
        issues.append("rejected_record_issued")
    if artifact.repository_changed or artifact.external_operation_performed:
        issues.append("memory_layer_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
