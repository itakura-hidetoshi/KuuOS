#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_long_term_memory_v0_34 import (
    SEALED as SOURCE_SEALED,
    artifact_issues as source_artifact_issues,
    all_source_digests as memory_source_digests,
)

VERSION = "kuuos_lifecycle_archive_v0_35"
ARCHIVED = "LIFECYCLE_ARCHIVE_BOUND_FOR_FINAL_CLOSURE"
ALERT = "LIFECYCLE_ARCHIVE_ALERT"
REJECTED = "LIFECYCLE_ARCHIVE_REJECTED"
OBJECTIVE = "BIND_LONG_TERM_MEMORY_TO_ARCHIVE_ONLY"
SOURCE_ORDER_CHECK = "source_memory_precedes_archive_binding"


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


def archive_digest(value: Rec) -> str:
    return _digest(value, "archive_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(
    policy_id: str,
    *,
    allowed_archive_steward_ids: tuple[str, ...],
    allowed_archive_steward_organization_ids: tuple[str, ...],
    max_archive_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_archive_steward_ids=_canon(allowed_archive_steward_ids),
        allowed_archive_steward_organization_ids=_canon(allowed_archive_steward_organization_ids),
        max_archive_delay_seconds=max_archive_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        sealed_source_required=True,
        source_recomputation_required=True,
        archive_binding_required=True,
        archive_boundary_required=True,
        memory_seal_required=True,
        memorial_read_only_required=True,
        covenant_active_required=True,
        retrieval_read_only_required=True,
        final_closure_route_required_next=True,
        repository_read_only=True,
        repository_change_absent_required=True,
        external_operation_absent_required=True,
        policy_digest="",
        version=VERSION,
    )
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_archive_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_archive_steward_ids or not value.allowed_archive_steward_organization_ids:
        issues.append("allowed_archive_steward_missing")
    if min(value.max_archive_delay_seconds, value.max_evidence_age_seconds) <= 0:
        issues.append("bound_invalid")
    if not all((
        value.archive_binding_required,
        value.archive_boundary_required,
        value.memory_seal_required,
        value.memorial_read_only_required,
        value.covenant_active_required,
        value.retrieval_read_only_required,
        value.repository_read_only,
        value.repository_change_absent_required,
        value.external_operation_absent_required,
    )):
        issues.append("archive_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(source_memory, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = memory_source_digests(
        source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:])
    )
    result.update(
        lifecycle_long_term_memory=source_memory.memory_digest,
        lifecycle_long_term_memory_evidence=source_evidence.evidence_digest,
        lifecycle_long_term_memory_policy=source_policy.policy_digest,
        lifecycle_long_term_memory_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(source_memory, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_memory, source_evidence, source_policy, *source_args)


def expected_final_closure_route_digest(source_memory, source_record, *, archive_id: str, archive_steward_id: str, archive_receipt_digest: str) -> str:
    return canonical_digest({
        "source_memory_id": source_memory.memory_id,
        "source_memory_record_digest": source_record.record_digest,
        "archive_id": archive_id,
        "archive_steward_id": archive_steward_id,
        "apoptosis_target_id": source_memory.apoptosis_target_id,
        "archive_boundary_digest": source_memory.archive_boundary_digest,
        "memory_seal_digest": source_memory.memory_seal_digest,
        "archive_receipt_digest": archive_receipt_digest,
        "covenant_digest": source_memory.non_resurrection_covenant_digest,
    })


def make_evidence(source_memory, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(
        source_memory_id=source_memory.memory_id,
        source_memory_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(source_memory, source_evidence, source_policy, source_record, source_args),
        apoptosis_target_id=source_memory.apoptosis_target_id,
        memory_seal_digest=source_memory.memory_seal_digest,
        archive_boundary_digest=source_memory.archive_boundary_digest,
        memorial_record_digest=source_memory.memorial_record_digest,
        covenant_digest=source_memory.non_resurrection_covenant_digest,
    )
    values.update(overrides)
    if "final_closure_route_digest" not in values:
        values["final_closure_route_digest"] = expected_final_closure_route_digest(
            source_memory,
            source_record,
            archive_id=values["archive_id"],
            archive_steward_id=values["archive_steward_id"],
            archive_receipt_digest=values["archive_receipt_digest"],
        )
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_archive_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = (
        "evidence_id",
        "archive_id",
        "archive_steward_id",
        "archive_steward_organization_id",
        "archive_steward_mandate_receipt_digest",
        "archive_steward_authority_receipt_digest",
        "archive_steward_identity_confirmation_digest",
        "apoptosis_target_id",
        "archive_receipt_digest",
        "archive_boundary_digest",
        "memory_seal_digest",
        "memorial_record_digest",
        "covenant_digest",
        "final_closure_route_digest",
    )
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.archive_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.archived_at_epoch_seconds) < 0:
        issues.append("negative_archive_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_archive(archive_id: str, archive_steward_id: str, archive_steward_organization_id: str, archive_requested_at_epoch_seconds: int, archived_at_epoch_seconds: int, source_memory, source_record, archive_evidence: Rec, *, archive_receipt_digest: str, final_closure_route_digest: str, archive_confirmed: bool, alert_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(
        archive_id=archive_id,
        archive_steward_id=archive_steward_id,
        archive_steward_organization_id=archive_steward_organization_id,
        objective=objective,
        archive_requested_at_epoch_seconds=archive_requested_at_epoch_seconds,
        archived_at_epoch_seconds=archived_at_epoch_seconds,
        source_memory_id=source_memory.memory_id,
        source_memory_record_digest=source_record.record_digest,
        apoptosis_target_id=source_memory.apoptosis_target_id,
        memory_seal_digest=source_memory.memory_seal_digest,
        archive_boundary_digest=source_memory.archive_boundary_digest,
        archive_receipt_digest=archive_receipt_digest,
        final_closure_route_digest=final_closure_route_digest,
        memorial_record_digest=source_memory.memorial_record_digest,
        covenant_digest=source_memory.non_resurrection_covenant_digest,
        archive_evidence_digest=archive_evidence.evidence_digest,
        archive_confirmed=archive_confirmed,
        alert_reason_digest=alert_reason_digest,
        archive_digest="",
        version=VERSION,
    )
    value.archive_digest = archive_digest(value)
    issues = archive_issues(value)
    if issues:
        raise ValueError("lifecycle_archive_invalid:" + issues[0])
    return value


def archive_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("alert_reason_digest", "archive_digest", "version", "archive_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_archive_field_missing")
            break
    if not value.archive_confirmed and not value.alert_reason_digest:
        issues.append("alert_reason_missing")
    if min(value.archive_requested_at_epoch_seconds, value.archived_at_epoch_seconds) < 0:
        issues.append("negative_archive_time")
    if value.archive_digest != archive_digest(value):
        issues.append("archive_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all((
        record.status == SOURCE_SEALED,
        record.long_term_memory_record_issued,
        record.long_term_memory_completed,
        record.long_term_memory_sealed,
        record.ready_for_non_resurrection_archive,
        record.non_resurrection_archive_required_next,
        record.non_resurrection_archive_route_required_next,
        record.authority_remains_closed,
        record.dependency_ingress_remains_closed,
        record.activation_route_remains_closed,
        record.non_resurrection_covenant_active,
        record.memorial_record_read_only,
        not record.repository_changed,
        not record.external_operation_performed,
    ))


def evaluate(archive: Rec, evidence: Rec, policy: Rec, source_memory, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_memory, source_evidence, source_policy, source_record, source_args)
    expected_route = expected_final_closure_route_digest(
        source_memory,
        source_record,
        archive_id=archive.archive_id,
        archive_steward_id=archive.archive_steward_id,
        archive_receipt_digest=archive.archive_receipt_digest,
    )
    archive_delay = evidence.archived_at_epoch_seconds - source_memory.sealed_at_epoch_seconds
    evidence_age = evidence.archived_at_epoch_seconds - evidence.captured_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "archive_valid": not archive_issues(archive),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_memory, source_evidence, source_policy, source_record, source_args),
        "source_memory_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and archive.source_memory_id == evidence.source_memory_id == source_memory.memory_id and archive.source_memory_record_digest == evidence.source_memory_record_digest == source_record.record_digest,
        "identity_binding_valid": archive.archive_id == evidence.archive_id and archive.archive_steward_id == evidence.archive_steward_id and archive.archive_steward_organization_id == evidence.archive_steward_organization_id and archive.archive_evidence_digest == evidence.evidence_digest,
        "apoptosis_target_binding_valid": archive.apoptosis_target_id == evidence.apoptosis_target_id == source_memory.apoptosis_target_id,
        "archive_route_binding_valid": archive.final_closure_route_digest == evidence.final_closure_route_digest == expected_route,
        "archive_receipt_valid": archive.archive_receipt_digest == evidence.archive_receipt_digest and evidence.archive_receipt_confirmed,
        "archive_boundary_valid": archive.archive_boundary_digest == evidence.archive_boundary_digest and evidence.archive_boundary_confirmed,
        "memory_seal_valid": archive.memory_seal_digest == evidence.memory_seal_digest and evidence.memory_seal_confirmed,
        "memorial_read_only": archive.memorial_record_digest == evidence.memorial_record_digest and evidence.memorial_record_read_only,
        "covenant_active": archive.covenant_digest == evidence.covenant_digest and evidence.covenant_active,
        "retrieval_read_only": evidence.retrieval_read_only,
        "steward_allowed": archive.archive_steward_id in policy.allowed_archive_steward_ids,
        "steward_organization_allowed": archive.archive_steward_organization_id in policy.allowed_archive_steward_organization_ids,
        "objective_allowed": archive.objective == OBJECTIVE,
        "archive_delay_valid": 0 <= archive_delay <= policy.max_archive_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "time_order_valid": source_memory.sealed_at_epoch_seconds <= evidence.archive_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.archived_at_epoch_seconds,
        "authority_remains_closed": evidence.authority_closed,
        "dependency_ingress_remains_closed": evidence.dependency_ingress_closed,
        "activation_route_remains_closed": evidence.activation_route_closed,
        "no_reactivation_route": not evidence.reactivation_route_present,
        "repository_change_absent": not evidence.repository_changed,
        "external_operation_absent": not evidence.external_operation_performed,
        "steward_mandate_verified": evidence.archive_steward_mandate_verified,
        "steward_authority_verified": evidence.archive_steward_authority_verified,
        "steward_identity_confirmed": evidence.archive_steward_identity_confirmed,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = (
    "policy_valid", "archive_valid", "evidence_valid", "source_recomputed_valid", "source_memory_ready", "source_binding_valid", "identity_binding_valid", "apoptosis_target_binding_valid", "archive_route_binding_valid", "archive_receipt_valid", "archive_boundary_valid", "memory_seal_valid", "memorial_read_only", "covenant_active", "retrieval_read_only", "steward_allowed", "steward_organization_allowed", "objective_allowed", "archive_delay_valid", "evidence_fresh", "time_order_valid", "repository_change_absent", "external_operation_absent",
)
ALERT_CHECKS = (
    "authority_remains_closed", "dependency_ingress_remains_closed", "activation_route_remains_closed", "no_reactivation_route", "steward_mandate_verified", "steward_authority_verified", "steward_identity_confirmed", "institutional_hold_absent", "emergency_state_absent",
)


def compute_artifact(archive: Rec, evidence: Rec, policy: Rec, source_memory, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(archive, evidence, policy, source_memory, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_memory.sealed_at_epoch_seconds <= archive.archive_requested_at_epoch_seconds <= archive.archived_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_memory_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in ALERT_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = ALERT, failed
        elif archive.archive_confirmed:
            status, reason = ARCHIVED, "archive_bound_for_final_closure"
        else:
            status, reason = ALERT, "archive_not_confirmed"
    issued = status != REJECTED
    archived = status == ARCHIVED
    alert = status == ALERT
    artifact = Rec(
        archive_id=archive.archive_id,
        status=status,
        reason=reason,
        apoptosis_target_id=archive.apoptosis_target_id,
        memory_seal_digest=archive.memory_seal_digest,
        archive_boundary_digest=archive.archive_boundary_digest,
        archive_receipt_digest=archive.archive_receipt_digest,
        final_closure_route_digest=archive.final_closure_route_digest,
        memorial_record_digest=archive.memorial_record_digest,
        covenant_digest=archive.covenant_digest,
        policy_digest=policy.policy_digest,
        archive_digest=archive.archive_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_memory_ready=checks["source_memory_ready"],
        archive_record_issued=issued,
        archive_completed=issued,
        archive_bound=archived,
        archive_alert=alert,
        archive_rejected=status == REJECTED,
        ready_for_final_closure=archived,
        final_closure_required_next=archived,
        final_closure_route_required_next=archived,
        archive_response_required_next=alert,
        archive_response_route_required_next=alert,
        authority_remains_closed=archived and evidence.authority_closed,
        dependency_ingress_remains_closed=archived and evidence.dependency_ingress_closed,
        activation_route_remains_closed=archived and evidence.activation_route_closed,
        covenant_active=archived and evidence.covenant_active,
        memorial_record_read_only=archived and evidence.memorial_record_read_only,
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
        raise ValueError("lifecycle_archive_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("archive_recomputation_mismatch")
    if artifact.status not in (ARCHIVED, ALERT, REJECTED):
        issues.append("status_invalid")
    if artifact.status == ARCHIVED and not all((artifact.archive_record_issued, artifact.archive_completed, artifact.archive_bound, artifact.ready_for_final_closure, artifact.final_closure_required_next, artifact.authority_remains_closed, artifact.dependency_ingress_remains_closed, artifact.activation_route_remains_closed, artifact.covenant_active, artifact.memorial_record_read_only)):
        issues.append("archive_gate_invalid")
    if artifact.status == ALERT and not all((artifact.archive_record_issued, artifact.archive_completed, artifact.archive_alert, not artifact.final_closure_required_next, artifact.archive_response_required_next)):
        issues.append("alert_gate_invalid")
    if artifact.status == REJECTED and any((artifact.archive_record_issued, artifact.archive_completed, artifact.final_closure_required_next, artifact.archive_response_required_next)):
        issues.append("rejected_record_issued")
    if artifact.repository_changed or artifact.external_operation_performed:
        issues.append("archive_layer_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
