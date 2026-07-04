#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_completion_v0_36 import (
    COMPLETED as SOURCE_COMPLETED,
    artifact_issues as source_artifact_issues,
    all_source_digests as completion_source_digests,
)

VERSION = "kuuos_lifecycle_completion_integrity_v0_37"
VERIFIED = "LIFECYCLE_COMPLETION_INTEGRITY_VERIFIED"
ALERT = "LIFECYCLE_COMPLETION_INTEGRITY_ALERT"
REJECTED = "LIFECYCLE_COMPLETION_INTEGRITY_REJECTED"
OBJECTIVE = "VERIFY_TERMINAL_COMPLETION_INTEGRITY_ONLY"
SOURCE_ORDER_CHECK = "source_completion_precedes_integrity_verification"


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


def verification_digest(value: Rec) -> str:
    return _digest(value, "verification_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(policy_id: str, *, allowed_verifier_ids: tuple[str, ...], allowed_verifier_organization_ids: tuple[str, ...], max_delay_seconds: int = 900, max_evidence_age_seconds: int = 300) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_verifier_ids=_canon(allowed_verifier_ids),
        allowed_verifier_organization_ids=_canon(allowed_verifier_organization_ids),
        max_delay_seconds=max_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        completed_source_required=True,
        source_recomputation_required=True,
        terminal_integrity_required=True,
        no_following_route_required=True,
        read_only_required=True,
        repository_read_only=True,
        repository_change_absent_required=True,
        external_operation_absent_required=True,
        policy_digest="",
        version=VERSION,
    )
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("completion_integrity_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_verifier_ids or not value.allowed_verifier_organization_ids:
        issues.append("allowed_verifier_missing")
    if min(value.max_delay_seconds, value.max_evidence_age_seconds) <= 0:
        issues.append("bound_invalid")
    if not all((value.completed_source_required, value.source_recomputation_required, value.terminal_integrity_required, value.no_following_route_required, value.read_only_required, value.repository_read_only, value.repository_change_absent_required, value.external_operation_absent_required)):
        issues.append("policy_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(source_completion, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = completion_source_digests(source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:]))
    result.update(
        lifecycle_completion_v0_36=source_completion.completion_digest,
        lifecycle_completion_v0_36_evidence=source_evidence.evidence_digest,
        lifecycle_completion_v0_36_policy=source_policy.policy_digest,
        lifecycle_completion_v0_36_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(source_completion, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_completion, source_evidence, source_policy, *source_args)


def expected_integrity_digest(source_completion, source_record, *, verification_id: str, verifier_id: str) -> str:
    return canonical_digest({
        "verification_id": verification_id,
        "verifier_id": verifier_id,
        "source_completion_id": source_completion.completion_id,
        "source_record_digest": source_record.record_digest,
        "target_id": source_completion.target_id,
        "terminal_digest": source_completion.terminal_digest,
        "completion_receipt_digest": source_completion.completion_receipt_digest,
        "covenant_digest": source_completion.covenant_digest,
    })


def make_evidence(source_completion, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(
        source_completion_id=source_completion.completion_id,
        source_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(source_completion, source_evidence, source_policy, source_record, source_args),
        target_id=source_completion.target_id,
        terminal_digest=source_completion.terminal_digest,
        completion_receipt_digest=source_completion.completion_receipt_digest,
        memorial_record_digest=source_completion.memorial_record_digest,
        covenant_digest=source_completion.covenant_digest,
    )
    values.update(overrides)
    if "integrity_digest" not in values:
        values["integrity_digest"] = expected_integrity_digest(source_completion, source_record, verification_id=values["verification_id"], verifier_id=values["verifier_id"])
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("completion_integrity_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = ("evidence_id", "verification_id", "verifier_id", "verifier_organization_id", "verifier_mandate_receipt_digest", "verifier_authority_receipt_digest", "verifier_identity_confirmation_digest", "source_completion_id", "source_record_digest", "target_id", "terminal_digest", "completion_receipt_digest", "integrity_digest", "memorial_record_digest", "covenant_digest")
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.verified_at_epoch_seconds) < 0:
        issues.append("negative_verification_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_verification(verification_id: str, verifier_id: str, verifier_organization_id: str, requested_at_epoch_seconds: int, verified_at_epoch_seconds: int, source_completion, source_record, verification_evidence: Rec, *, integrity_digest: str, verification_confirmed: bool, alert_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(
        verification_id=verification_id,
        verifier_id=verifier_id,
        verifier_organization_id=verifier_organization_id,
        objective=objective,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        verified_at_epoch_seconds=verified_at_epoch_seconds,
        source_completion_id=source_completion.completion_id,
        source_record_digest=source_record.record_digest,
        target_id=source_completion.target_id,
        terminal_digest=source_completion.terminal_digest,
        completion_receipt_digest=source_completion.completion_receipt_digest,
        integrity_digest=integrity_digest,
        memorial_record_digest=source_completion.memorial_record_digest,
        covenant_digest=source_completion.covenant_digest,
        verification_evidence_digest=verification_evidence.evidence_digest,
        verification_confirmed=verification_confirmed,
        alert_reason_digest=alert_reason_digest,
        verification_digest="",
        version=VERSION,
    )
    value.verification_digest = verification_digest(value)
    issues = verification_issues(value)
    if issues:
        raise ValueError("completion_integrity_verification_invalid:" + issues[0])
    return value


def verification_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("alert_reason_digest", "verification_digest", "version", "verification_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_verification_field_missing")
            break
    if not value.verification_confirmed and not value.alert_reason_digest:
        issues.append("alert_reason_missing")
    if min(value.requested_at_epoch_seconds, value.verified_at_epoch_seconds) < 0:
        issues.append("negative_verification_time")
    if value.verification_digest != verification_digest(value):
        issues.append("verification_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all((
        record.status == SOURCE_COMPLETED,
        record.completion_record_issued,
        record.completion_completed,
        record.lifecycle_terminal,
        not record.following_route_required_next,
        not record.following_route_permitted,
        record.authority_remains_closed,
        record.dependency_ingress_remains_closed,
        record.activation_route_remains_closed,
        record.covenant_active,
        record.memorial_record_read_only,
        not record.repository_changed,
        not record.external_operation_performed,
    ))


def evaluate(verification: Rec, evidence: Rec, policy: Rec, source_completion, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_completion, source_evidence, source_policy, source_record, source_args)
    expected_integrity = expected_integrity_digest(source_completion, source_record, verification_id=verification.verification_id, verifier_id=verification.verifier_id)
    delay = evidence.verified_at_epoch_seconds - source_completion.completed_at_epoch_seconds
    age = evidence.verified_at_epoch_seconds - evidence.captured_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "verification_valid": not verification_issues(verification),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_completion, source_evidence, source_policy, source_record, source_args),
        "source_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and verification.source_completion_id == evidence.source_completion_id == source_completion.completion_id and verification.source_record_digest == evidence.source_record_digest == source_record.record_digest,
        "identity_binding_valid": verification.verification_id == evidence.verification_id and verification.verifier_id == evidence.verifier_id and verification.verifier_organization_id == evidence.verifier_organization_id and verification.verification_evidence_digest == evidence.evidence_digest,
        "target_binding_valid": verification.target_id == evidence.target_id == source_completion.target_id,
        "integrity_binding_valid": verification.integrity_digest == evidence.integrity_digest == expected_integrity,
        "terminal_digest_bound": verification.terminal_digest == evidence.terminal_digest == source_completion.terminal_digest,
        "receipt_bound": verification.completion_receipt_digest == evidence.completion_receipt_digest == source_completion.completion_receipt_digest,
        "memorial_read_only": verification.memorial_record_digest == evidence.memorial_record_digest and evidence.memorial_record_read_only,
        "covenant_active": verification.covenant_digest == evidence.covenant_digest and evidence.covenant_active,
        "no_following_route": evidence.no_following_route,
        "verifier_allowed": verification.verifier_id in policy.allowed_verifier_ids,
        "verifier_organization_allowed": verification.verifier_organization_id in policy.allowed_verifier_organization_ids,
        "objective_allowed": verification.objective == OBJECTIVE,
        "delay_valid": 0 <= delay <= policy.max_delay_seconds,
        "evidence_fresh": 0 <= age <= policy.max_evidence_age_seconds,
        "time_order_valid": source_completion.completed_at_epoch_seconds <= evidence.requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.verified_at_epoch_seconds,
        "authority_remains_closed": evidence.authority_closed,
        "dependency_ingress_remains_closed": evidence.dependency_ingress_closed,
        "activation_route_remains_closed": evidence.activation_route_closed,
        "repository_change_absent": not evidence.repository_changed,
        "external_operation_absent": not evidence.external_operation_performed,
        "verifier_mandate_verified": evidence.verifier_mandate_verified,
        "verifier_authority_verified": evidence.verifier_authority_verified,
        "verifier_identity_confirmed": evidence.verifier_identity_confirmed,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = ("policy_valid", "verification_valid", "evidence_valid", "source_recomputed_valid", "source_ready", "source_binding_valid", "identity_binding_valid", "target_binding_valid", "integrity_binding_valid", "terminal_digest_bound", "receipt_bound", "memorial_read_only", "covenant_active", "no_following_route", "verifier_allowed", "verifier_organization_allowed", "objective_allowed", "delay_valid", "evidence_fresh", "time_order_valid", "repository_change_absent", "external_operation_absent")
ALERT_CHECKS = ("authority_remains_closed", "dependency_ingress_remains_closed", "activation_route_remains_closed", "verifier_mandate_verified", "verifier_authority_verified", "verifier_identity_confirmed")


def compute_artifact(verification: Rec, evidence: Rec, policy: Rec, source_completion, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(verification, evidence, policy, source_completion, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_completion.completed_at_epoch_seconds <= verification.requested_at_epoch_seconds <= verification.verified_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_policy_integrity_or_binding_invalid"
    else:
        failed = next((name for name in ALERT_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = ALERT, failed
        elif verification.verification_confirmed:
            status, reason = VERIFIED, "completion_integrity_verified"
        else:
            status, reason = ALERT, "verification_not_confirmed"
    issued = status != REJECTED
    verified = status == VERIFIED
    alert = status == ALERT
    artifact = Rec(
        verification_id=verification.verification_id,
        status=status,
        reason=reason,
        target_id=verification.target_id,
        terminal_digest=verification.terminal_digest,
        completion_receipt_digest=verification.completion_receipt_digest,
        integrity_digest=verification.integrity_digest,
        memorial_record_digest=verification.memorial_record_digest,
        covenant_digest=verification.covenant_digest,
        policy_digest=policy.policy_digest,
        verification_digest=verification.verification_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_ready=checks["source_ready"],
        integrity_record_issued=issued,
        integrity_verified=verified,
        integrity_alert=alert,
        integrity_rejected=status == REJECTED,
        lifecycle_terminal_preserved=verified,
        following_route_required_next=False,
        following_route_permitted=False,
        integrity_response_required_next=alert,
        integrity_response_route_required_next=alert,
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
        raise ValueError("completion_integrity_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("completion_integrity_recomputation_mismatch")
    if artifact.status not in (VERIFIED, ALERT, REJECTED):
        issues.append("status_invalid")
    if artifact.status == VERIFIED and not all((artifact.integrity_record_issued, artifact.integrity_verified, artifact.lifecycle_terminal_preserved, not artifact.following_route_required_next, not artifact.following_route_permitted)):
        issues.append("verified_gate_invalid")
    if artifact.status == ALERT and not all((artifact.integrity_record_issued, artifact.integrity_alert, artifact.integrity_response_required_next, not artifact.lifecycle_terminal_preserved)):
        issues.append("alert_gate_invalid")
    if artifact.status == REJECTED and any((artifact.integrity_record_issued, artifact.integrity_verified, artifact.integrity_response_required_next)):
        issues.append("rejected_record_issued")
    if artifact.repository_changed or artifact.external_operation_performed:
        issues.append("integrity_layer_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
