#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_execution_result_review_v0_30 import (
    ACCEPTED as SOURCE_ACCEPTED,
    artifact_issues as source_artifact_issues,
    all_source_digests as review_source_digests,
)

VERSION = "kuuos_lifecycle_apoptosis_closure_review_v0_31"
CLOSED = "LIFECYCLE_APOPTOSIS_CLOSURE_REVIEW_CLOSED_FOR_POST_APOPTOSIS_QUARANTINE"
BLOCKED = "LIFECYCLE_APOPTOSIS_CLOSURE_REVIEW_BLOCKED"
REJECTED = "LIFECYCLE_APOPTOSIS_CLOSURE_REVIEW_REJECTED"
OBJECTIVE = "REVIEW_APOPTOSIS_TARGET_CLOSURE_FOR_POST_APOPTOSIS_BOUNDARY_ONLY"
SOURCE_ORDER_CHECK = "source_result_review_precedes_apoptosis_closure_review_and_deadline_valid"


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


def closure_review_digest(value: Rec) -> str:
    return _digest(value, "closure_review_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(
    policy_id: str,
    *,
    allowed_closure_reviewer_ids: tuple[str, ...],
    allowed_closure_reviewer_organization_ids: tuple[str, ...],
    max_closure_review_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_closure_reviewer_ids=_canon(allowed_closure_reviewer_ids),
        allowed_closure_reviewer_organization_ids=_canon(allowed_closure_reviewer_organization_ids),
        max_closure_review_delay_seconds=max_closure_review_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        accepted_source_required=True,
        source_recomputation_required=True,
        apoptosis_target_binding_required=True,
        authority_closure_required=True,
        dependency_ingress_closure_required=True,
        activation_route_closure_required=True,
        quarantine_binding_required=True,
        memory_binding_required=True,
        non_resurrection_required=True,
        closure_reviewer_authority_required=True,
        closure_reviewer_separation_required=True,
        repository_read_only=True,
        repository_change_absent_required=True,
        external_operation_absent_required=True,
        policy_digest="",
        version=VERSION,
    )
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_apoptosis_closure_review_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_closure_reviewer_ids or not value.allowed_closure_reviewer_organization_ids:
        issues.append("allowed_closure_reviewer_missing")
    if min(value.max_closure_review_delay_seconds, value.max_evidence_age_seconds) <= 0:
        issues.append("bound_invalid")
    if not all((
        value.apoptosis_target_binding_required,
        value.authority_closure_required,
        value.dependency_ingress_closure_required,
        value.activation_route_closure_required,
        value.quarantine_binding_required,
        value.memory_binding_required,
        value.non_resurrection_required,
        value.repository_read_only,
        value.repository_change_absent_required,
        value.external_operation_absent_required,
    )):
        issues.append("closure_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = review_source_digests(
        source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:])
    )
    result.update(
        lifecycle_execution_result_review=source_review.review_digest,
        lifecycle_execution_result_review_evidence=source_evidence.evidence_digest,
        lifecycle_execution_result_review_policy=source_policy.policy_digest,
        lifecycle_execution_result_review_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_review, source_evidence, source_policy, *source_args)


def expected_post_apoptosis_route_digest(source_review, source_record, *, closure_review_id: str, closure_reviewer_id: str, quarantine_binding_digest: str, memorial_record_digest: str, non_resurrection_covenant_digest: str) -> str:
    return canonical_digest({
        "source_review_id": source_review.review_id,
        "source_review_record_digest": source_record.record_digest,
        "closure_review_id": closure_review_id,
        "closure_reviewer_id": closure_reviewer_id,
        "adopted_lifecycle_state_digest": source_review.adopted_lifecycle_state_digest,
        "source_result_adoption_route_digest": source_review.result_adoption_route_digest,
        "quarantine_binding_digest": quarantine_binding_digest,
        "memorial_record_digest": memorial_record_digest,
        "non_resurrection_covenant_digest": non_resurrection_covenant_digest,
    })


def make_evidence(source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(
        source_review_id=source_review.review_id,
        source_review_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(source_review, source_evidence, source_policy, source_record, source_args),
        source_result_reviewer_id=source_review.result_reviewer_id,
        source_execution_id=source_review.source_execution_id,
        source_repository_review_id=source_review.source_repository_review_id,
        subject_id=source_review.subject_id,
        requester_id=source_review.requester_id,
        transition_package_digest=source_review.transition_package_digest,
        adopted_lifecycle_state_digest=source_review.adopted_lifecycle_state_digest,
        source_result_adoption_route_digest=source_review.result_adoption_route_digest,
        source_result_adoption_deadline_at_epoch_seconds=source_review.result_adoption_deadline_at_epoch_seconds,
    )
    values.update(overrides)
    if "post_apoptosis_route_digest" not in values:
        values["post_apoptosis_route_digest"] = expected_post_apoptosis_route_digest(
            source_review,
            source_record,
            closure_review_id=values["closure_review_id"],
            closure_reviewer_id=values["closure_reviewer_id"],
            quarantine_binding_digest=values["quarantine_binding_digest"],
            memorial_record_digest=values["memorial_record_digest"],
            non_resurrection_covenant_digest=values["non_resurrection_covenant_digest"],
        )
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_apoptosis_closure_review_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = (
        "evidence_id",
        "closure_review_id",
        "closure_reviewer_id",
        "closure_reviewer_organization_id",
        "closure_reviewer_mandate_receipt_digest",
        "closure_reviewer_authority_receipt_digest",
        "closure_reviewer_identity_confirmation_digest",
        "apoptosis_target_id",
        "apoptosis_boundary_digest",
        "authority_closure_receipt_digest",
        "dependency_ingress_closure_receipt_digest",
        "activation_route_closure_receipt_digest",
        "quarantine_binding_digest",
        "memorial_record_digest",
        "non_resurrection_covenant_digest",
        "post_apoptosis_route_digest",
    )
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.closure_review_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.reviewed_at_epoch_seconds, value.source_result_adoption_deadline_at_epoch_seconds) < 0:
        issues.append("negative_closure_review_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_closure_review(closure_review_id: str, closure_reviewer_id: str, closure_reviewer_organization_id: str, closure_review_requested_at_epoch_seconds: int, reviewed_at_epoch_seconds: int, source_review, source_record, closure_evidence: Rec, *, apoptosis_target_id: str, apoptosis_boundary_digest: str, quarantine_binding_digest: str, memorial_record_digest: str, non_resurrection_covenant_digest: str, post_apoptosis_route_digest: str, closure_confirmed: bool, blocking_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(
        closure_review_id=closure_review_id,
        closure_reviewer_id=closure_reviewer_id,
        closure_reviewer_organization_id=closure_reviewer_organization_id,
        objective=objective,
        closure_review_requested_at_epoch_seconds=closure_review_requested_at_epoch_seconds,
        reviewed_at_epoch_seconds=reviewed_at_epoch_seconds,
        source_review_id=source_review.review_id,
        source_review_record_digest=source_record.record_digest,
        source_execution_id=source_review.source_execution_id,
        source_repository_review_id=source_review.source_repository_review_id,
        subject_id=source_review.subject_id,
        requester_id=source_review.requester_id,
        source_result_reviewer_id=source_review.result_reviewer_id,
        transition_package_digest=source_review.transition_package_digest,
        adopted_lifecycle_state_digest=source_review.adopted_lifecycle_state_digest,
        source_result_adoption_route_digest=source_review.result_adoption_route_digest,
        apoptosis_target_id=apoptosis_target_id,
        apoptosis_boundary_digest=apoptosis_boundary_digest,
        quarantine_binding_digest=quarantine_binding_digest,
        memorial_record_digest=memorial_record_digest,
        non_resurrection_covenant_digest=non_resurrection_covenant_digest,
        post_apoptosis_route_digest=post_apoptosis_route_digest,
        closure_evidence_digest=closure_evidence.evidence_digest,
        closure_confirmed=closure_confirmed,
        blocking_reason_digest=blocking_reason_digest,
        closure_review_digest="",
        version=VERSION,
    )
    value.closure_review_digest = closure_review_digest(value)
    issues = closure_review_issues(value)
    if issues:
        raise ValueError("lifecycle_apoptosis_closure_review_invalid:" + issues[0])
    return value


def closure_review_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("blocking_reason_digest", "closure_review_digest", "version", "closure_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_closure_review_field_missing")
            break
    if not value.closure_confirmed and not value.blocking_reason_digest:
        issues.append("blocking_reason_missing")
    if min(value.closure_review_requested_at_epoch_seconds, value.reviewed_at_epoch_seconds) < 0:
        issues.append("negative_closure_review_time")
    if value.closure_review_digest != closure_review_digest(value):
        issues.append("closure_review_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all((
        record.status == SOURCE_ACCEPTED,
        record.execution_result_review_record_issued,
        record.execution_result_review_completed,
        record.execution_result_review_accepted,
        record.ready_for_separate_execution_result_adoption,
        record.execution_result_adoption_required_next,
        record.execution_result_adoption_route_required_next,
        not record.repository_changed,
        record.repository_read_only,
    ))


def evaluate(closure_review: Rec, evidence: Rec, policy: Rec, source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_review, source_evidence, source_policy, source_record, source_args)
    expected_post_route = expected_post_apoptosis_route_digest(
        source_review,
        source_record,
        closure_review_id=closure_review.closure_review_id,
        closure_reviewer_id=closure_review.closure_reviewer_id,
        quarantine_binding_digest=closure_review.quarantine_binding_digest,
        memorial_record_digest=closure_review.memorial_record_digest,
        non_resurrection_covenant_digest=closure_review.non_resurrection_covenant_digest,
    )
    prior = {source_review.subject_id, source_review.requester_id, source_review.source_executor_id, source_review.result_reviewer_id, source_evidence.result_reviewer_id}
    review_delay = evidence.reviewed_at_epoch_seconds - source_review.reviewed_at_epoch_seconds
    evidence_age = evidence.reviewed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "closure_review_valid": not closure_review_issues(closure_review),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_review, source_evidence, source_policy, source_record, source_args),
        "source_review_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and closure_review.source_review_id == evidence.source_review_id == source_review.review_id and closure_review.source_review_record_digest == evidence.source_review_record_digest == source_record.record_digest,
        "identity_binding_valid": closure_review.closure_review_id == evidence.closure_review_id and closure_review.closure_reviewer_id == evidence.closure_reviewer_id and closure_review.closure_reviewer_organization_id == evidence.closure_reviewer_organization_id and closure_review.closure_evidence_digest == evidence.evidence_digest,
        "apoptosis_target_binding_valid": closure_review.apoptosis_target_id == evidence.apoptosis_target_id and closure_review.apoptosis_boundary_digest == evidence.apoptosis_boundary_digest,
        "post_apoptosis_route_binding_valid": closure_review.post_apoptosis_route_digest == evidence.post_apoptosis_route_digest == expected_post_route,
        "quarantine_binding_valid": closure_review.quarantine_binding_digest == evidence.quarantine_binding_digest and evidence.quarantine_binding_confirmed,
        "memory_binding_valid": closure_review.memorial_record_digest == evidence.memorial_record_digest and evidence.memorial_record_confirmed,
        "non_resurrection_valid": closure_review.non_resurrection_covenant_digest == evidence.non_resurrection_covenant_digest and evidence.non_resurrection_covenant_confirmed,
        "closure_reviewer_allowed": closure_review.closure_reviewer_id in policy.allowed_closure_reviewer_ids,
        "closure_reviewer_organization_allowed": closure_review.closure_reviewer_organization_id in policy.allowed_closure_reviewer_organization_ids,
        "closure_reviewer_separated_from_prior_actors": closure_review.closure_reviewer_id not in prior,
        "objective_allowed": closure_review.objective == OBJECTIVE,
        "closure_review_delay_valid": 0 <= review_delay <= policy.max_closure_review_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "time_order_valid": source_review.reviewed_at_epoch_seconds <= evidence.closure_review_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.reviewed_at_epoch_seconds <= source_review.result_adoption_deadline_at_epoch_seconds,
        "authority_closed": evidence.authority_closed,
        "dependency_ingress_closed": evidence.dependency_ingress_closed,
        "activation_route_closed": evidence.activation_route_closed,
        "successor_or_memorial_bound": evidence.successor_binding_confirmed or evidence.memorial_record_confirmed,
        "repository_change_absent": not evidence.repository_changed,
        "external_operation_absent": not evidence.external_operation_performed,
        "closure_reviewer_mandate_verified": evidence.closure_reviewer_mandate_verified,
        "closure_reviewer_authority_verified": evidence.closure_reviewer_authority_verified,
        "closure_reviewer_identity_confirmed": evidence.closure_reviewer_identity_confirmed,
        "no_unresolved_dependency": not evidence.unresolved_dependency_present,
        "no_reactivation_route": not evidence.reactivation_route_present,
        "no_institutional_hold": not evidence.institutional_hold_active,
        "no_emergency_state": not evidence.emergency_state_active,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = (
    "policy_valid", "closure_review_valid", "evidence_valid", "source_recomputed_valid", "source_review_ready", "source_binding_valid", "identity_binding_valid", "apoptosis_target_binding_valid", "post_apoptosis_route_binding_valid", "quarantine_binding_valid", "memory_binding_valid", "non_resurrection_valid", "closure_reviewer_allowed", "closure_reviewer_organization_allowed", "closure_reviewer_separated_from_prior_actors", "objective_allowed", "closure_review_delay_valid", "evidence_fresh", "time_order_valid", "repository_change_absent", "external_operation_absent",
)
BLOCKING_CHECKS = (
    "authority_closed", "dependency_ingress_closed", "activation_route_closed", "successor_or_memorial_bound", "closure_reviewer_mandate_verified", "closure_reviewer_authority_verified", "closure_reviewer_identity_confirmed", "no_unresolved_dependency", "no_reactivation_route", "no_institutional_hold", "no_emergency_state",
)


def compute_artifact(closure_review: Rec, evidence: Rec, policy: Rec, source_review, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(closure_review, evidence, policy, source_review, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_review.reviewed_at_epoch_seconds <= closure_review.closure_review_requested_at_epoch_seconds <= closure_review.reviewed_at_epoch_seconds <= source_review.result_adoption_deadline_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_result_review_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in BLOCKING_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = BLOCKED, failed
        elif closure_review.closure_confirmed:
            status, reason = CLOSED, "apoptosis_target_closed_for_post_apoptosis_quarantine"
        else:
            status, reason = BLOCKED, "apoptosis_closure_not_confirmed"
    issued = status != REJECTED
    closed = status == CLOSED
    blocked = status == BLOCKED
    artifact = Rec(
        closure_review_id=closure_review.closure_review_id,
        status=status,
        reason=reason,
        apoptosis_target_id=closure_review.apoptosis_target_id,
        apoptosis_boundary_digest=closure_review.apoptosis_boundary_digest,
        closure_reviewer_id=closure_review.closure_reviewer_id,
        closure_reviewer_organization_id=closure_review.closure_reviewer_organization_id,
        source_review_id=closure_review.source_review_id,
        source_review_record_digest=closure_review.source_review_record_digest,
        transition_package_digest=closure_review.transition_package_digest,
        adopted_lifecycle_state_digest=closure_review.adopted_lifecycle_state_digest,
        quarantine_binding_digest=closure_review.quarantine_binding_digest,
        memorial_record_digest=closure_review.memorial_record_digest,
        non_resurrection_covenant_digest=closure_review.non_resurrection_covenant_digest,
        post_apoptosis_route_digest=closure_review.post_apoptosis_route_digest,
        policy_digest=policy.policy_digest,
        closure_review_digest=closure_review.closure_review_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_review_ready=checks["source_review_ready"],
        apoptosis_closure_review_record_issued=issued,
        apoptosis_closure_review_completed=issued,
        apoptosis_target_closed=closed,
        apoptosis_closure_blocked=blocked,
        apoptosis_closure_rejected=status == REJECTED,
        ready_for_post_apoptosis_quarantine=closed,
        post_apoptosis_quarantine_required_next=closed,
        post_apoptosis_quarantine_route_required_next=closed,
        apoptosis_closure_replan_required_next=blocked,
        apoptosis_closure_replan_route_required_next=blocked,
        authority_closed=closed and evidence.authority_closed,
        dependency_ingress_closed=closed and evidence.dependency_ingress_closed,
        activation_route_closed=closed and evidence.activation_route_closed,
        non_resurrection_covenant_confirmed=closed and evidence.non_resurrection_covenant_confirmed,
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
        raise ValueError("lifecycle_apoptosis_closure_review_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("apoptosis_closure_review_recomputation_mismatch")
    if artifact.status not in (CLOSED, BLOCKED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == CLOSED and not all((artifact.apoptosis_closure_review_record_issued, artifact.apoptosis_closure_review_completed, artifact.apoptosis_target_closed, artifact.ready_for_post_apoptosis_quarantine, artifact.post_apoptosis_quarantine_required_next, artifact.authority_closed, artifact.dependency_ingress_closed, artifact.activation_route_closed, artifact.non_resurrection_covenant_confirmed)):
        issues.append("closed_gate_invalid")
    if artifact.status == BLOCKED and not all((artifact.apoptosis_closure_review_record_issued, artifact.apoptosis_closure_review_completed, artifact.apoptosis_closure_blocked, not artifact.post_apoptosis_quarantine_required_next, artifact.apoptosis_closure_replan_required_next)):
        issues.append("blocked_gate_invalid")
    if artifact.status == REJECTED and any((artifact.apoptosis_closure_review_record_issued, artifact.apoptosis_closure_review_completed, artifact.post_apoptosis_quarantine_required_next, artifact.apoptosis_closure_replan_required_next)):
        issues.append("rejected_record_issued")
    if artifact.repository_changed or artifact.external_operation_performed:
        issues.append("closure_layer_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
