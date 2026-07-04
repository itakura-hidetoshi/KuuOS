#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_post_apoptosis_quarantine_v0_32 import (
    QUARANTINED as SOURCE_QUARANTINED,
    artifact_issues as source_artifact_issues,
    all_source_digests as quarantine_source_digests,
)

VERSION = "kuuos_lifecycle_post_apoptosis_observation_v0_33"
STABLE = "LIFECYCLE_POST_APOPTOSIS_OBSERVATION_STABLE_FOR_LONG_TERM_MEMORY"
ALERT = "LIFECYCLE_POST_APOPTOSIS_OBSERVATION_ALERT"
REJECTED = "LIFECYCLE_POST_APOPTOSIS_OBSERVATION_REJECTED"
OBJECTIVE = "OBSERVE_POST_APOPTOSIS_QUARANTINE_STABILITY_ONLY"
SOURCE_ORDER_CHECK = "source_quarantine_precedes_post_apoptosis_observation"


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


def observation_digest(value: Rec) -> str:
    return _digest(value, "observation_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(
    policy_id: str,
    *,
    allowed_observer_ids: tuple[str, ...],
    allowed_observer_organization_ids: tuple[str, ...],
    max_observation_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_observer_ids=_canon(allowed_observer_ids),
        allowed_observer_organization_ids=_canon(allowed_observer_organization_ids),
        max_observation_delay_seconds=max_observation_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        quarantined_source_required=True,
        source_recomputation_required=True,
        quarantine_boundary_required=True,
        authority_closed_required=True,
        dependency_ingress_closed_required=True,
        activation_route_closed_required=True,
        memorial_read_only_required=True,
        non_resurrection_required=True,
        reactivation_absent_required=True,
        successor_non_capture_required=True,
        long_term_memory_route_required_next=True,
        repository_read_only=True,
        repository_change_absent_required=True,
        external_operation_absent_required=True,
        policy_digest="",
        version=VERSION,
    )
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_post_apoptosis_observation_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_observer_ids or not value.allowed_observer_organization_ids:
        issues.append("allowed_observer_missing")
    if min(value.max_observation_delay_seconds, value.max_evidence_age_seconds) <= 0:
        issues.append("bound_invalid")
    if not all((
        value.quarantine_boundary_required,
        value.authority_closed_required,
        value.dependency_ingress_closed_required,
        value.activation_route_closed_required,
        value.memorial_read_only_required,
        value.non_resurrection_required,
        value.reactivation_absent_required,
        value.successor_non_capture_required,
        value.repository_read_only,
        value.repository_change_absent_required,
        value.external_operation_absent_required,
    )):
        issues.append("observation_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(source_quarantine, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = quarantine_source_digests(
        source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:])
    )
    result.update(
        lifecycle_post_apoptosis_quarantine=source_quarantine.quarantine_digest,
        lifecycle_post_apoptosis_quarantine_evidence=source_evidence.evidence_digest,
        lifecycle_post_apoptosis_quarantine_policy=source_policy.policy_digest,
        lifecycle_post_apoptosis_quarantine_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(source_quarantine, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_quarantine, source_evidence, source_policy, *source_args)


def expected_long_term_memory_route_digest(source_quarantine, source_record, *, observation_id: str, observer_id: str, stability_window_digest: str, observation_receipt_digest: str) -> str:
    return canonical_digest({
        "source_quarantine_id": source_quarantine.quarantine_id,
        "source_quarantine_record_digest": source_record.record_digest,
        "observation_id": observation_id,
        "observer_id": observer_id,
        "apoptosis_target_id": source_quarantine.apoptosis_target_id,
        "quarantine_boundary_digest": source_quarantine.quarantine_boundary_digest,
        "observation_window_digest": source_quarantine.observation_window_digest,
        "stability_window_digest": stability_window_digest,
        "observation_receipt_digest": observation_receipt_digest,
        "non_resurrection_covenant_digest": source_quarantine.non_resurrection_covenant_digest,
    })


def make_evidence(source_quarantine, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(
        source_quarantine_id=source_quarantine.quarantine_id,
        source_quarantine_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(source_quarantine, source_evidence, source_policy, source_record, source_args),
        apoptosis_target_id=source_quarantine.apoptosis_target_id,
        apoptosis_boundary_digest=source_quarantine.apoptosis_boundary_digest,
        quarantine_boundary_digest=source_quarantine.quarantine_boundary_digest,
        observation_window_digest=source_quarantine.observation_window_digest,
        memorial_record_digest=source_quarantine.memorial_record_digest,
        non_resurrection_covenant_digest=source_quarantine.non_resurrection_covenant_digest,
    )
    values.update(overrides)
    if "long_term_memory_route_digest" not in values:
        values["long_term_memory_route_digest"] = expected_long_term_memory_route_digest(
            source_quarantine,
            source_record,
            observation_id=values["observation_id"],
            observer_id=values["observer_id"],
            stability_window_digest=values["stability_window_digest"],
            observation_receipt_digest=values["observation_receipt_digest"],
        )
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_post_apoptosis_observation_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = (
        "evidence_id",
        "observation_id",
        "observer_id",
        "observer_organization_id",
        "observer_mandate_receipt_digest",
        "observer_authority_receipt_digest",
        "observer_identity_confirmation_digest",
        "apoptosis_target_id",
        "quarantine_boundary_digest",
        "stability_window_digest",
        "observation_receipt_digest",
        "long_term_memory_route_digest",
        "memorial_record_digest",
        "non_resurrection_covenant_digest",
    )
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.observation_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.observed_at_epoch_seconds) < 0:
        issues.append("negative_observation_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_observation(observation_id: str, observer_id: str, observer_organization_id: str, observation_requested_at_epoch_seconds: int, observed_at_epoch_seconds: int, source_quarantine, source_record, observation_evidence: Rec, *, stability_window_digest: str, observation_receipt_digest: str, long_term_memory_route_digest: str, stability_confirmed: bool, alert_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(
        observation_id=observation_id,
        observer_id=observer_id,
        observer_organization_id=observer_organization_id,
        objective=objective,
        observation_requested_at_epoch_seconds=observation_requested_at_epoch_seconds,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        source_quarantine_id=source_quarantine.quarantine_id,
        source_quarantine_record_digest=source_record.record_digest,
        apoptosis_target_id=source_quarantine.apoptosis_target_id,
        apoptosis_boundary_digest=source_quarantine.apoptosis_boundary_digest,
        quarantine_boundary_digest=source_quarantine.quarantine_boundary_digest,
        observation_window_digest=source_quarantine.observation_window_digest,
        stability_window_digest=stability_window_digest,
        observation_receipt_digest=observation_receipt_digest,
        long_term_memory_route_digest=long_term_memory_route_digest,
        memorial_record_digest=source_quarantine.memorial_record_digest,
        non_resurrection_covenant_digest=source_quarantine.non_resurrection_covenant_digest,
        observation_evidence_digest=observation_evidence.evidence_digest,
        stability_confirmed=stability_confirmed,
        alert_reason_digest=alert_reason_digest,
        observation_digest="",
        version=VERSION,
    )
    value.observation_digest = observation_digest(value)
    issues = observation_issues(value)
    if issues:
        raise ValueError("lifecycle_post_apoptosis_observation_invalid:" + issues[0])
    return value


def observation_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("alert_reason_digest", "observation_digest", "version", "stability_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_observation_field_missing")
            break
    if not value.stability_confirmed and not value.alert_reason_digest:
        issues.append("alert_reason_missing")
    if min(value.observation_requested_at_epoch_seconds, value.observed_at_epoch_seconds) < 0:
        issues.append("negative_observation_time")
    if value.observation_digest != observation_digest(value):
        issues.append("observation_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all((
        record.status == SOURCE_QUARANTINED,
        record.post_apoptosis_quarantine_record_issued,
        record.post_apoptosis_quarantine_completed,
        record.post_apoptosis_quarantined,
        record.ready_for_post_apoptosis_observation,
        record.post_apoptosis_observation_required_next,
        record.post_apoptosis_observation_route_required_next,
        record.authority_remains_closed,
        record.dependency_ingress_remains_closed,
        record.activation_route_remains_closed,
        record.non_resurrection_covenant_active,
        record.memorial_record_read_only,
        not record.repository_changed,
        not record.external_operation_performed,
    ))


def evaluate(observation: Rec, evidence: Rec, policy: Rec, source_quarantine, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_quarantine, source_evidence, source_policy, source_record, source_args)
    expected_route = expected_long_term_memory_route_digest(
        source_quarantine,
        source_record,
        observation_id=observation.observation_id,
        observer_id=observation.observer_id,
        stability_window_digest=observation.stability_window_digest,
        observation_receipt_digest=observation.observation_receipt_digest,
    )
    observation_delay = evidence.observed_at_epoch_seconds - source_quarantine.quarantined_at_epoch_seconds
    evidence_age = evidence.observed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "observation_valid": not observation_issues(observation),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_quarantine, source_evidence, source_policy, source_record, source_args),
        "source_quarantine_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and observation.source_quarantine_id == evidence.source_quarantine_id == source_quarantine.quarantine_id and observation.source_quarantine_record_digest == evidence.source_quarantine_record_digest == source_record.record_digest,
        "identity_binding_valid": observation.observation_id == evidence.observation_id and observation.observer_id == evidence.observer_id and observation.observer_organization_id == evidence.observer_organization_id and observation.observation_evidence_digest == evidence.evidence_digest,
        "apoptosis_target_binding_valid": observation.apoptosis_target_id == evidence.apoptosis_target_id == source_quarantine.apoptosis_target_id,
        "quarantine_boundary_binding_valid": observation.quarantine_boundary_digest == evidence.quarantine_boundary_digest == source_quarantine.quarantine_boundary_digest,
        "long_term_memory_route_binding_valid": observation.long_term_memory_route_digest == evidence.long_term_memory_route_digest == expected_route,
        "memorial_read_only": observation.memorial_record_digest == evidence.memorial_record_digest and evidence.memorial_record_read_only,
        "non_resurrection_maintained": observation.non_resurrection_covenant_digest == evidence.non_resurrection_covenant_digest and evidence.non_resurrection_covenant_active,
        "observer_allowed": observation.observer_id in policy.allowed_observer_ids,
        "observer_organization_allowed": observation.observer_organization_id in policy.allowed_observer_organization_ids,
        "objective_allowed": observation.objective == OBJECTIVE,
        "observation_delay_valid": 0 <= observation_delay <= policy.max_observation_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "time_order_valid": source_quarantine.quarantined_at_epoch_seconds <= evidence.observation_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.observed_at_epoch_seconds,
        "authority_remains_closed": evidence.authority_closed,
        "dependency_ingress_remains_closed": evidence.dependency_ingress_closed,
        "activation_route_remains_closed": evidence.activation_route_closed,
        "successor_non_capture": not evidence.successor_captures_quarantined_target,
        "no_reactivation_route": not evidence.reactivation_route_present,
        "no_boundary_drift": not evidence.quarantine_boundary_drift_detected,
        "repository_change_absent": not evidence.repository_changed,
        "external_operation_absent": not evidence.external_operation_performed,
        "observer_mandate_verified": evidence.observer_mandate_verified,
        "observer_authority_verified": evidence.observer_authority_verified,
        "observer_identity_confirmed": evidence.observer_identity_confirmed,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = (
    "policy_valid", "observation_valid", "evidence_valid", "source_recomputed_valid", "source_quarantine_ready", "source_binding_valid", "identity_binding_valid", "apoptosis_target_binding_valid", "quarantine_boundary_binding_valid", "long_term_memory_route_binding_valid", "memorial_read_only", "non_resurrection_maintained", "observer_allowed", "observer_organization_allowed", "objective_allowed", "observation_delay_valid", "evidence_fresh", "time_order_valid", "repository_change_absent", "external_operation_absent",
)
ALERT_CHECKS = (
    "authority_remains_closed", "dependency_ingress_remains_closed", "activation_route_remains_closed", "successor_non_capture", "no_reactivation_route", "no_boundary_drift", "observer_mandate_verified", "observer_authority_verified", "observer_identity_confirmed", "institutional_hold_absent", "emergency_state_absent",
)


def compute_artifact(observation: Rec, evidence: Rec, policy: Rec, source_quarantine, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(observation, evidence, policy, source_quarantine, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_quarantine.quarantined_at_epoch_seconds <= observation.observation_requested_at_epoch_seconds <= observation.observed_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_quarantine_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in ALERT_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = ALERT, failed
        elif observation.stability_confirmed:
            status, reason = STABLE, "post_apoptosis_quarantine_stable_for_long_term_memory"
        else:
            status, reason = ALERT, "post_apoptosis_stability_not_confirmed"
    issued = status != REJECTED
    stable = status == STABLE
    alert = status == ALERT
    artifact = Rec(
        observation_id=observation.observation_id,
        status=status,
        reason=reason,
        apoptosis_target_id=observation.apoptosis_target_id,
        quarantine_boundary_digest=observation.quarantine_boundary_digest,
        observation_window_digest=observation.observation_window_digest,
        stability_window_digest=observation.stability_window_digest,
        long_term_memory_route_digest=observation.long_term_memory_route_digest,
        memorial_record_digest=observation.memorial_record_digest,
        non_resurrection_covenant_digest=observation.non_resurrection_covenant_digest,
        policy_digest=policy.policy_digest,
        observation_digest=observation.observation_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_quarantine_ready=checks["source_quarantine_ready"],
        post_apoptosis_observation_record_issued=issued,
        post_apoptosis_observation_completed=issued,
        post_apoptosis_observation_stable=stable,
        post_apoptosis_observation_alert=alert,
        post_apoptosis_observation_rejected=status == REJECTED,
        ready_for_long_term_memory=stable,
        long_term_memory_required_next=stable,
        long_term_memory_route_required_next=stable,
        post_apoptosis_observation_response_required_next=alert,
        post_apoptosis_observation_response_route_required_next=alert,
        authority_remains_closed=stable and evidence.authority_closed,
        dependency_ingress_remains_closed=stable and evidence.dependency_ingress_closed,
        activation_route_remains_closed=stable and evidence.activation_route_closed,
        non_resurrection_covenant_active=stable and evidence.non_resurrection_covenant_active,
        memorial_record_read_only=stable and evidence.memorial_record_read_only,
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
        raise ValueError("lifecycle_post_apoptosis_observation_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("post_apoptosis_observation_recomputation_mismatch")
    if artifact.status not in (STABLE, ALERT, REJECTED):
        issues.append("status_invalid")
    if artifact.status == STABLE and not all((artifact.post_apoptosis_observation_record_issued, artifact.post_apoptosis_observation_completed, artifact.post_apoptosis_observation_stable, artifact.ready_for_long_term_memory, artifact.long_term_memory_required_next, artifact.authority_remains_closed, artifact.dependency_ingress_remains_closed, artifact.activation_route_remains_closed, artifact.non_resurrection_covenant_active, artifact.memorial_record_read_only)):
        issues.append("stable_gate_invalid")
    if artifact.status == ALERT and not all((artifact.post_apoptosis_observation_record_issued, artifact.post_apoptosis_observation_completed, artifact.post_apoptosis_observation_alert, not artifact.long_term_memory_required_next, artifact.post_apoptosis_observation_response_required_next)):
        issues.append("alert_gate_invalid")
    if artifact.status == REJECTED and any((artifact.post_apoptosis_observation_record_issued, artifact.post_apoptosis_observation_completed, artifact.long_term_memory_required_next, artifact.post_apoptosis_observation_response_required_next)):
        issues.append("rejected_record_issued")
    if artifact.repository_changed or artifact.external_operation_performed:
        issues.append("observation_layer_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
