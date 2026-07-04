#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_apoptosis_closure_review_v0_31 import (
    CLOSED as SOURCE_CLOSED,
    artifact_issues as source_artifact_issues,
    all_source_digests as closure_source_digests,
)

VERSION = "kuuos_lifecycle_post_apoptosis_quarantine_v0_32"
QUARANTINED = "LIFECYCLE_POST_APOPTOSIS_QUARANTINE_BOUND_FOR_OBSERVATION"
BLOCKED = "LIFECYCLE_POST_APOPTOSIS_QUARANTINE_BLOCKED"
REJECTED = "LIFECYCLE_POST_APOPTOSIS_QUARANTINE_REJECTED"
OBJECTIVE = "BOUND_CLOSED_APOPTOSIS_TARGET_IN_POST_APOPTOSIS_QUARANTINE_ONLY"
SOURCE_ORDER_CHECK = "source_apoptosis_closure_precedes_post_apoptosis_quarantine_and_deadline_valid"


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


def quarantine_digest(value: Rec) -> str:
    return _digest(value, "quarantine_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(
    policy_id: str,
    *,
    allowed_quarantine_guardian_ids: tuple[str, ...],
    allowed_quarantine_guardian_organization_ids: tuple[str, ...],
    max_quarantine_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_quarantine_guardian_ids=_canon(allowed_quarantine_guardian_ids),
        allowed_quarantine_guardian_organization_ids=_canon(allowed_quarantine_guardian_organization_ids),
        max_quarantine_delay_seconds=max_quarantine_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        closed_source_required=True,
        source_recomputation_required=True,
        apoptosis_target_binding_required=True,
        quarantine_boundary_required=True,
        authority_remains_closed_required=True,
        dependency_ingress_remains_closed_required=True,
        activation_route_remains_closed_required=True,
        memorial_read_only_required=True,
        non_resurrection_required=True,
        successor_non_capture_required=True,
        observation_route_required_next=True,
        repository_read_only=True,
        repository_change_absent_required=True,
        external_operation_absent_required=True,
        policy_digest="",
        version=VERSION,
    )
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_post_apoptosis_quarantine_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_quarantine_guardian_ids or not value.allowed_quarantine_guardian_organization_ids:
        issues.append("allowed_quarantine_guardian_missing")
    if min(value.max_quarantine_delay_seconds, value.max_evidence_age_seconds) <= 0:
        issues.append("bound_invalid")
    if not all((
        value.quarantine_boundary_required,
        value.authority_remains_closed_required,
        value.dependency_ingress_remains_closed_required,
        value.activation_route_remains_closed_required,
        value.memorial_read_only_required,
        value.non_resurrection_required,
        value.successor_non_capture_required,
        value.repository_read_only,
        value.repository_change_absent_required,
        value.external_operation_absent_required,
    )):
        issues.append("quarantine_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(source_closure, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = closure_source_digests(source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:]))
    result.update(
        lifecycle_apoptosis_closure_review=source_closure.closure_review_digest,
        lifecycle_apoptosis_closure_review_evidence=source_evidence.evidence_digest,
        lifecycle_apoptosis_closure_review_policy=source_policy.policy_digest,
        lifecycle_apoptosis_closure_review_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(source_closure, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_closure, source_evidence, source_policy, *source_args)


def expected_observation_route_digest(source_closure, source_record, *, quarantine_id: str, guardian_id: str, quarantine_boundary_digest: str, observation_window_digest: str) -> str:
    return canonical_digest({
        "source_closure_review_id": source_closure.closure_review_id,
        "source_closure_record_digest": source_record.record_digest,
        "quarantine_id": quarantine_id,
        "guardian_id": guardian_id,
        "apoptosis_target_id": source_closure.apoptosis_target_id,
        "apoptosis_boundary_digest": source_closure.apoptosis_boundary_digest,
        "quarantine_boundary_digest": quarantine_boundary_digest,
        "observation_window_digest": observation_window_digest,
        "non_resurrection_covenant_digest": source_closure.non_resurrection_covenant_digest,
    })


def make_evidence(source_closure, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(
        source_closure_review_id=source_closure.closure_review_id,
        source_closure_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(source_closure, source_evidence, source_policy, source_record, source_args),
        apoptosis_target_id=source_closure.apoptosis_target_id,
        apoptosis_boundary_digest=source_closure.apoptosis_boundary_digest,
        source_quarantine_binding_digest=source_closure.quarantine_binding_digest,
        memorial_record_digest=source_closure.memorial_record_digest,
        non_resurrection_covenant_digest=source_closure.non_resurrection_covenant_digest,
        post_apoptosis_route_digest=source_closure.post_apoptosis_route_digest,
    )
    values.update(overrides)
    if "observation_route_digest" not in values:
        values["observation_route_digest"] = expected_observation_route_digest(
            source_closure,
            source_record,
            quarantine_id=values["quarantine_id"],
            guardian_id=values["quarantine_guardian_id"],
            quarantine_boundary_digest=values["quarantine_boundary_digest"],
            observation_window_digest=values["observation_window_digest"],
        )
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_post_apoptosis_quarantine_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = (
        "evidence_id",
        "quarantine_id",
        "quarantine_guardian_id",
        "quarantine_guardian_organization_id",
        "quarantine_guardian_mandate_receipt_digest",
        "quarantine_guardian_authority_receipt_digest",
        "quarantine_guardian_identity_confirmation_digest",
        "apoptosis_target_id",
        "apoptosis_boundary_digest",
        "quarantine_boundary_digest",
        "observation_window_digest",
        "memorial_record_digest",
        "non_resurrection_covenant_digest",
        "observation_route_digest",
    )
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.quarantine_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.quarantined_at_epoch_seconds) < 0:
        issues.append("negative_quarantine_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_quarantine(quarantine_id: str, quarantine_guardian_id: str, quarantine_guardian_organization_id: str, quarantine_requested_at_epoch_seconds: int, quarantined_at_epoch_seconds: int, source_closure, source_record, quarantine_evidence: Rec, *, quarantine_boundary_digest: str, observation_window_digest: str, observation_route_digest: str, quarantine_confirmed: bool, blocking_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(
        quarantine_id=quarantine_id,
        quarantine_guardian_id=quarantine_guardian_id,
        quarantine_guardian_organization_id=quarantine_guardian_organization_id,
        objective=objective,
        quarantine_requested_at_epoch_seconds=quarantine_requested_at_epoch_seconds,
        quarantined_at_epoch_seconds=quarantined_at_epoch_seconds,
        source_closure_review_id=source_closure.closure_review_id,
        source_closure_record_digest=source_record.record_digest,
        apoptosis_target_id=source_closure.apoptosis_target_id,
        apoptosis_boundary_digest=source_closure.apoptosis_boundary_digest,
        quarantine_boundary_digest=quarantine_boundary_digest,
        observation_window_digest=observation_window_digest,
        observation_route_digest=observation_route_digest,
        memorial_record_digest=source_closure.memorial_record_digest,
        non_resurrection_covenant_digest=source_closure.non_resurrection_covenant_digest,
        quarantine_evidence_digest=quarantine_evidence.evidence_digest,
        quarantine_confirmed=quarantine_confirmed,
        blocking_reason_digest=blocking_reason_digest,
        quarantine_digest="",
        version=VERSION,
    )
    value.quarantine_digest = quarantine_digest(value)
    issues = quarantine_issues(value)
    if issues:
        raise ValueError("lifecycle_post_apoptosis_quarantine_invalid:" + issues[0])
    return value


def quarantine_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("blocking_reason_digest", "quarantine_digest", "version", "quarantine_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_quarantine_field_missing")
            break
    if not value.quarantine_confirmed and not value.blocking_reason_digest:
        issues.append("blocking_reason_missing")
    if min(value.quarantine_requested_at_epoch_seconds, value.quarantined_at_epoch_seconds) < 0:
        issues.append("negative_quarantine_time")
    if value.quarantine_digest != quarantine_digest(value):
        issues.append("quarantine_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all((
        record.status == SOURCE_CLOSED,
        record.apoptosis_closure_review_record_issued,
        record.apoptosis_closure_review_completed,
        record.apoptosis_target_closed,
        record.ready_for_post_apoptosis_quarantine,
        record.post_apoptosis_quarantine_required_next,
        record.post_apoptosis_quarantine_route_required_next,
        record.authority_closed,
        record.dependency_ingress_closed,
        record.activation_route_closed,
        record.non_resurrection_covenant_confirmed,
        not record.repository_changed,
        not record.external_operation_performed,
    ))


def evaluate(quarantine: Rec, evidence: Rec, policy: Rec, source_closure, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_closure, source_evidence, source_policy, source_record, source_args)
    expected_route = expected_observation_route_digest(
        source_closure,
        source_record,
        quarantine_id=quarantine.quarantine_id,
        guardian_id=quarantine.quarantine_guardian_id,
        quarantine_boundary_digest=quarantine.quarantine_boundary_digest,
        observation_window_digest=quarantine.observation_window_digest,
    )
    quarantine_delay = evidence.quarantined_at_epoch_seconds - source_closure.reviewed_at_epoch_seconds
    evidence_age = evidence.quarantined_at_epoch_seconds - evidence.captured_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "quarantine_valid": not quarantine_issues(quarantine),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_closure, source_evidence, source_policy, source_record, source_args),
        "source_closure_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and quarantine.source_closure_review_id == evidence.source_closure_review_id == source_closure.closure_review_id and quarantine.source_closure_record_digest == evidence.source_closure_record_digest == source_record.record_digest,
        "identity_binding_valid": quarantine.quarantine_id == evidence.quarantine_id and quarantine.quarantine_guardian_id == evidence.quarantine_guardian_id and quarantine.quarantine_guardian_organization_id == evidence.quarantine_guardian_organization_id and quarantine.quarantine_evidence_digest == evidence.evidence_digest,
        "apoptosis_target_binding_valid": quarantine.apoptosis_target_id == evidence.apoptosis_target_id == source_closure.apoptosis_target_id and quarantine.apoptosis_boundary_digest == evidence.apoptosis_boundary_digest == source_closure.apoptosis_boundary_digest,
        "quarantine_boundary_binding_valid": quarantine.quarantine_boundary_digest == evidence.quarantine_boundary_digest and evidence.quarantine_boundary_confirmed,
        "observation_route_binding_valid": quarantine.observation_route_digest == evidence.observation_route_digest == expected_route,
        "memorial_read_only": quarantine.memorial_record_digest == evidence.memorial_record_digest and evidence.memorial_record_read_only,
        "non_resurrection_maintained": quarantine.non_resurrection_covenant_digest == evidence.non_resurrection_covenant_digest and evidence.non_resurrection_covenant_active,
        "guardian_allowed": quarantine.quarantine_guardian_id in policy.allowed_quarantine_guardian_ids,
        "guardian_organization_allowed": quarantine.quarantine_guardian_organization_id in policy.allowed_quarantine_guardian_organization_ids,
        "objective_allowed": quarantine.objective == OBJECTIVE,
        "quarantine_delay_valid": 0 <= quarantine_delay <= policy.max_quarantine_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "time_order_valid": source_closure.reviewed_at_epoch_seconds <= evidence.quarantine_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.quarantined_at_epoch_seconds,
        "authority_remains_closed": evidence.authority_closed,
        "dependency_ingress_remains_closed": evidence.dependency_ingress_closed,
        "activation_route_remains_closed": evidence.activation_route_closed,
        "successor_non_capture": not evidence.successor_captures_quarantined_target,
        "no_reactivation_route": not evidence.reactivation_route_present,
        "repository_change_absent": not evidence.repository_changed,
        "external_operation_absent": not evidence.external_operation_performed,
        "guardian_mandate_verified": evidence.quarantine_guardian_mandate_verified,
        "guardian_authority_verified": evidence.quarantine_guardian_authority_verified,
        "guardian_identity_confirmed": evidence.quarantine_guardian_identity_confirmed,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = (
    "policy_valid", "quarantine_valid", "evidence_valid", "source_recomputed_valid", "source_closure_ready", "source_binding_valid", "identity_binding_valid", "apoptosis_target_binding_valid", "quarantine_boundary_binding_valid", "observation_route_binding_valid", "memorial_read_only", "non_resurrection_maintained", "guardian_allowed", "guardian_organization_allowed", "objective_allowed", "quarantine_delay_valid", "evidence_fresh", "time_order_valid", "repository_change_absent", "external_operation_absent",
)
BLOCKING_CHECKS = (
    "authority_remains_closed", "dependency_ingress_remains_closed", "activation_route_remains_closed", "successor_non_capture", "no_reactivation_route", "guardian_mandate_verified", "guardian_authority_verified", "guardian_identity_confirmed", "institutional_hold_absent", "emergency_state_absent",
)


def compute_artifact(quarantine: Rec, evidence: Rec, policy: Rec, source_closure, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(quarantine, evidence, policy, source_closure, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_closure.reviewed_at_epoch_seconds <= quarantine.quarantine_requested_at_epoch_seconds <= quarantine.quarantined_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_closure_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in BLOCKING_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = BLOCKED, failed
        elif quarantine.quarantine_confirmed:
            status, reason = QUARANTINED, "post_apoptosis_quarantine_bound_for_observation"
        else:
            status, reason = BLOCKED, "post_apoptosis_quarantine_not_confirmed"
    issued = status != REJECTED
    quarantined = status == QUARANTINED
    blocked = status == BLOCKED
    artifact = Rec(
        quarantine_id=quarantine.quarantine_id,
        status=status,
        reason=reason,
        apoptosis_target_id=quarantine.apoptosis_target_id,
        apoptosis_boundary_digest=quarantine.apoptosis_boundary_digest,
        quarantine_boundary_digest=quarantine.quarantine_boundary_digest,
        observation_window_digest=quarantine.observation_window_digest,
        observation_route_digest=quarantine.observation_route_digest,
        memorial_record_digest=quarantine.memorial_record_digest,
        non_resurrection_covenant_digest=quarantine.non_resurrection_covenant_digest,
        policy_digest=policy.policy_digest,
        quarantine_digest=quarantine.quarantine_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_closure_ready=checks["source_closure_ready"],
        post_apoptosis_quarantine_record_issued=issued,
        post_apoptosis_quarantine_completed=issued,
        post_apoptosis_quarantined=quarantined,
        post_apoptosis_quarantine_blocked=blocked,
        post_apoptosis_quarantine_rejected=status == REJECTED,
        ready_for_post_apoptosis_observation=quarantined,
        post_apoptosis_observation_required_next=quarantined,
        post_apoptosis_observation_route_required_next=quarantined,
        post_apoptosis_quarantine_replan_required_next=blocked,
        post_apoptosis_quarantine_replan_route_required_next=blocked,
        authority_remains_closed=quarantined and evidence.authority_closed,
        dependency_ingress_remains_closed=quarantined and evidence.dependency_ingress_closed,
        activation_route_remains_closed=quarantined and evidence.activation_route_closed,
        non_resurrection_covenant_active=quarantined and evidence.non_resurrection_covenant_active,
        memorial_record_read_only=quarantined and evidence.memorial_record_read_only,
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
        raise ValueError("lifecycle_post_apoptosis_quarantine_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("post_apoptosis_quarantine_recomputation_mismatch")
    if artifact.status not in (QUARANTINED, BLOCKED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == QUARANTINED and not all((artifact.post_apoptosis_quarantine_record_issued, artifact.post_apoptosis_quarantine_completed, artifact.post_apoptosis_quarantined, artifact.ready_for_post_apoptosis_observation, artifact.post_apoptosis_observation_required_next, artifact.authority_remains_closed, artifact.dependency_ingress_remains_closed, artifact.activation_route_remains_closed, artifact.non_resurrection_covenant_active, artifact.memorial_record_read_only)):
        issues.append("quarantined_gate_invalid")
    if artifact.status == BLOCKED and not all((artifact.post_apoptosis_quarantine_record_issued, artifact.post_apoptosis_quarantine_completed, artifact.post_apoptosis_quarantine_blocked, not artifact.post_apoptosis_observation_required_next, artifact.post_apoptosis_quarantine_replan_required_next)):
        issues.append("blocked_gate_invalid")
    if artifact.status == REJECTED and any((artifact.post_apoptosis_quarantine_record_issued, artifact.post_apoptosis_quarantine_completed, artifact.post_apoptosis_observation_required_next, artifact.post_apoptosis_quarantine_replan_required_next)):
        issues.append("rejected_record_issued")
    if artifact.repository_changed or artifact.external_operation_performed:
        issues.append("quarantine_layer_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
