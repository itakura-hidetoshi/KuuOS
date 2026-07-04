#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_transition_start_authorization_v0_21 import (
    AUTHORIZED as SOURCE_AUTHORIZED,
    artifact_issues as source_artifact_issues,
    all_source_digests as authorization_source_digests,
)

VERSION = "kuuos_lifecycle_bounded_transition_start_v0_22"
STARTED = "LIFECYCLE_BOUNDED_TRANSITION_START_STARTED_FOR_SEPARATE_TRANSITION_COMPLETION_REVIEW"
DENIED = "LIFECYCLE_BOUNDED_TRANSITION_START_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_TRANSITION_START_REJECTED"
OBJECTIVE = "START_AUTHORIZED_LIFECYCLE_TRANSITION_FOR_SEPARATE_COMPLETION_REVIEW_ONLY"
SOURCE_ORDER_CHECK = "source_start_authorization_precedes_transition_start_and_deadline_valid"

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

def start_digest(value: Rec) -> str:
    return _digest(value, "start_digest")

def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")

def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))

def make_policy(policy_id: str, *, allowed_transition_operator_ids: tuple[str, ...], allowed_transition_operator_organization_ids: tuple[str, ...], max_start_delay_seconds: int = 900, max_evidence_age_seconds: int = 300, max_completion_review_delay_seconds: int = 900) -> Rec:
    value = Rec(policy_id=policy_id, allowed_transition_operator_ids=_canon(allowed_transition_operator_ids), allowed_transition_operator_organization_ids=_canon(allowed_transition_operator_organization_ids), max_start_delay_seconds=max_start_delay_seconds, max_evidence_age_seconds=max_evidence_age_seconds, max_completion_review_delay_seconds=max_completion_review_delay_seconds, authorized_source_required=True, source_recomputation_required=True, transition_start_route_required=True, operator_authority_required=True, operator_separation_required=True, completion_review_route_required_next=True, lifecycle_state_read_only=True, repository_read_only=True, policy_digest="", version=VERSION)
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_start_policy_invalid:" + issues[0])
    return value

def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_transition_operator_ids or not value.allowed_transition_operator_organization_ids:
        issues.append("allowed_actor_missing")
    if min(value.max_start_delay_seconds, value.max_evidence_age_seconds, value.max_completion_review_delay_seconds) <= 0:
        issues.append("bound_invalid")
    if not value.lifecycle_state_read_only or not value.repository_read_only:
        issues.append("read_only_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)

def all_source_digests(source_authorization, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = authorization_source_digests(source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:]))
    result.update(lifecycle_transition_start_authorization=source_authorization.authorization_digest, lifecycle_transition_start_authorization_evidence=source_evidence.evidence_digest, lifecycle_transition_start_authorization_policy=source_policy.policy_digest, lifecycle_transition_start_authorization_record=source_record.record_digest)
    return result

def source_recomputed_valid(source_authorization, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_authorization, source_evidence, source_policy, *source_args)

def expected_completion_review_route_digest(source_authorization, source_record, *, transition_start_id: str, transition_operator_id: str, transition_package_digest: str, expected_current_lifecycle_state_digest: str, proposed_target_lifecycle_state_digest: str, transition_completion_review_deadline_at_epoch_seconds: int) -> str:
    return canonical_digest({"source_transition_start_authorization_id": source_authorization.transition_start_authorization_id, "source_transition_start_authorization_record_digest": source_record.record_digest, "source_transition_start_route_digest": source_authorization.transition_start_route_digest, "transition_start_id": transition_start_id, "transition_operator_id": transition_operator_id, "transition_package_digest": transition_package_digest, "expected_current_lifecycle_state_digest": expected_current_lifecycle_state_digest, "proposed_target_lifecycle_state_digest": proposed_target_lifecycle_state_digest, "transition_completion_review_deadline_at_epoch_seconds": transition_completion_review_deadline_at_epoch_seconds})

def make_evidence(source_authorization, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(source_transition_start_authorization_id=source_authorization.transition_start_authorization_id, source_transition_start_authorization_record_digest=source_record.record_digest, source_artifact_digests=all_source_digests(source_authorization, source_evidence, source_policy, source_record, source_args), source_transition_approval_id=source_authorization.source_transition_approval_id, source_transition_approver_id=source_authorization.source_transition_approver_id, source_transition_start_authorizer_id=source_authorization.transition_start_authorizer_id, source_transition_start_authorizer_organization_id=source_authorization.transition_start_authorizer_organization_id, subject_id=source_authorization.subject_id, requester_id=source_authorization.requester_id, transition_operator_id=source_authorization.future_transition_operator_id, transition_package_digest=source_authorization.transition_package_digest, expected_current_lifecycle_state_digest=source_authorization.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_authorization.proposed_target_lifecycle_state_digest, source_transition_start_route_digest=source_authorization.transition_start_route_digest, transition_start_deadline_at_epoch_seconds=source_authorization.transition_start_deadline_at_epoch_seconds, package_expiry_at_epoch_seconds=source_evidence.package_expiry_at_epoch_seconds)
    values.update(overrides)
    if "transition_completion_review_route_digest" not in values:
        values["transition_completion_review_route_digest"] = expected_completion_review_route_digest(source_authorization, source_record, transition_start_id=values["transition_start_id"], transition_operator_id=values["transition_operator_id"], transition_package_digest=values["transition_package_digest"], expected_current_lifecycle_state_digest=values["expected_current_lifecycle_state_digest"], proposed_target_lifecycle_state_digest=values["proposed_target_lifecycle_state_digest"], transition_completion_review_deadline_at_epoch_seconds=values["transition_completion_review_deadline_at_epoch_seconds"])
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_start_evidence_invalid:" + issues[0])
    return value

def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = ("evidence_id", "transition_start_id", "transition_operator_id", "transition_operator_organization_id", "operator_mandate_receipt_digest", "operator_authority_receipt_digest", "operator_identity_confirmation_digest", "source_transition_start_authorization_id", "source_transition_start_authorization_record_digest", "source_transition_start_route_digest", "transition_completion_review_route_digest", "transition_package_digest", "expected_current_lifecycle_state_digest", "proposed_target_lifecycle_state_digest", "start_authorization_freshness_receipt_digest", "package_freshness_receipt_digest", "current_state_freshness_receipt_digest", "target_state_validity_receipt_digest")
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.start_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.started_at_epoch_seconds, value.transition_start_deadline_at_epoch_seconds, value.transition_completion_review_deadline_at_epoch_seconds, value.package_expiry_at_epoch_seconds) < 0:
        issues.append("negative_start_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)

def make_submission(transition_start_id: str, transition_operator_id: str, transition_operator_organization_id: str, start_requested_at_epoch_seconds: int, started_at_epoch_seconds: int, source_authorization, source_record, start_evidence: Rec, *, transition_completion_review_route_digest: str, transition_completion_review_deadline_at_epoch_seconds: int, transition_start_confirmed: bool, denial_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(transition_start_id=transition_start_id, transition_operator_id=transition_operator_id, transition_operator_organization_id=transition_operator_organization_id, objective=objective, start_requested_at_epoch_seconds=start_requested_at_epoch_seconds, started_at_epoch_seconds=started_at_epoch_seconds, source_transition_start_authorization_id=source_authorization.transition_start_authorization_id, source_transition_start_authorization_record_digest=source_record.record_digest, subject_id=source_authorization.subject_id, requester_id=source_authorization.requester_id, source_transition_approval_id=source_authorization.source_transition_approval_id, source_transition_start_authorizer_id=source_authorization.transition_start_authorizer_id, transition_package_digest=source_authorization.transition_package_digest, expected_current_lifecycle_state_digest=source_authorization.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_authorization.proposed_target_lifecycle_state_digest, source_transition_start_route_digest=source_authorization.transition_start_route_digest, transition_completion_review_route_digest=transition_completion_review_route_digest, transition_completion_review_deadline_at_epoch_seconds=transition_completion_review_deadline_at_epoch_seconds, start_evidence_digest=start_evidence.evidence_digest, transition_start_confirmed=transition_start_confirmed, denial_reason_digest=denial_reason_digest, start_digest="", version=VERSION)
    value.start_digest = start_digest(value)
    issues = submission_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_start_invalid:" + issues[0])
    return value

def submission_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("denial_reason_digest", "start_digest", "version", "transition_start_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_start_field_missing")
            break
    if not value.transition_start_confirmed and not value.denial_reason_digest:
        issues.append("denial_reason_missing")
    if min(value.start_requested_at_epoch_seconds, value.started_at_epoch_seconds, value.transition_completion_review_deadline_at_epoch_seconds) < 0:
        issues.append("negative_start_time")
    if value.start_digest != start_digest(value):
        issues.append("start_digest_mismatch")
    return tuple(issues)

def _source_ready(record) -> bool:
    return all((record.status == SOURCE_AUTHORIZED, record.transition_start_authorization_record_issued, record.transition_start_authorization_completed, record.lifecycle_transition_start_authorized, record.ready_for_separate_transition_start, record.transition_start_required_next, record.transition_start_route_required_next, not record.lifecycle_transition_started, not record.lifecycle_transition_completed, not record.lifecycle_transition_performed, not record.external_operation_performed, not record.repository_changed, record.lifecycle_state_read_only, record.repository_read_only))

def _prior_actor_ids(source_authorization, source_evidence) -> set[str]:
    return {source_authorization.subject_id, source_authorization.requester_id, source_authorization.source_transition_approver_id, source_authorization.transition_start_authorizer_id, source_evidence.source_transition_approval_id}

def evaluate(start: Rec, evidence: Rec, policy: Rec, source_authorization, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_authorization, source_evidence, source_policy, source_record, source_args)
    expected_completion_route = expected_completion_review_route_digest(source_authorization, source_record, transition_start_id=start.transition_start_id, transition_operator_id=start.transition_operator_id, transition_package_digest=source_authorization.transition_package_digest, expected_current_lifecycle_state_digest=source_authorization.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_authorization.proposed_target_lifecycle_state_digest, transition_completion_review_deadline_at_epoch_seconds=start.transition_completion_review_deadline_at_epoch_seconds)
    prior = _prior_actor_ids(source_authorization, source_evidence)
    start_delay = evidence.started_at_epoch_seconds - source_authorization.authorized_at_epoch_seconds
    evidence_age = evidence.started_at_epoch_seconds - evidence.captured_at_epoch_seconds
    review_delay = evidence.transition_completion_review_deadline_at_epoch_seconds - evidence.started_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "start_valid": not submission_issues(start),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_authorization, source_evidence, source_policy, source_record, source_args),
        "source_start_authorization_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and start.source_transition_start_authorization_id == evidence.source_transition_start_authorization_id == source_authorization.transition_start_authorization_id and start.source_transition_start_authorization_record_digest == evidence.source_transition_start_authorization_record_digest == source_record.record_digest,
        "identity_binding_valid": start.transition_start_id == evidence.transition_start_id and start.transition_operator_id == evidence.transition_operator_id and start.transition_operator_organization_id == evidence.transition_operator_organization_id and start.start_evidence_digest == evidence.evidence_digest,
        "source_start_route_binding_valid": start.source_transition_start_route_digest == evidence.source_transition_start_route_digest == source_authorization.transition_start_route_digest,
        "completion_review_route_binding_valid": start.transition_completion_review_route_digest == evidence.transition_completion_review_route_digest == expected_completion_route,
        "package_binding_valid": start.transition_package_digest == evidence.transition_package_digest == source_authorization.transition_package_digest,
        "state_binding_valid": start.expected_current_lifecycle_state_digest == evidence.expected_current_lifecycle_state_digest == source_authorization.expected_current_lifecycle_state_digest and start.proposed_target_lifecycle_state_digest == evidence.proposed_target_lifecycle_state_digest == source_authorization.proposed_target_lifecycle_state_digest,
        "operator_bound_to_authorization": start.transition_operator_id == evidence.transition_operator_id == source_authorization.future_transition_operator_id,
        "operator_allowed": start.transition_operator_id in policy.allowed_transition_operator_ids,
        "operator_organization_allowed": start.transition_operator_organization_id in policy.allowed_transition_operator_organization_ids,
        "operator_separated_from_authorizer": start.transition_operator_id != source_authorization.transition_start_authorizer_id,
        "operator_separated_from_prior_actors": start.transition_operator_id not in prior,
        "operator_organization_separated": start.transition_operator_organization_id != source_authorization.transition_start_authorizer_organization_id,
        "objective_allowed": start.objective == OBJECTIVE,
        "start_delay_valid": 0 <= start_delay <= policy.max_start_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "completion_review_delay_valid": 0 < review_delay <= policy.max_completion_review_delay_seconds,
        "time_order_valid": source_authorization.authorized_at_epoch_seconds <= evidence.start_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.started_at_epoch_seconds < evidence.transition_completion_review_deadline_at_epoch_seconds <= evidence.package_expiry_at_epoch_seconds,
        "source_start_deadline_valid": evidence.started_at_epoch_seconds <= source_authorization.transition_start_deadline_at_epoch_seconds,
        "external_operation_absent": not evidence.external_operation_performed,
        "repository_change_absent": not evidence.repository_changed,
        "operator_mandate_verified": evidence.operator_mandate_verified,
        "operator_authority_verified": evidence.operator_authority_verified,
        "operator_identity_confirmed": evidence.operator_identity_confirmed,
        "start_authorization_fresh": evidence.start_authorization_fresh,
        "package_fresh": evidence.package_fresh,
        "current_state_not_stale": evidence.current_state_not_stale,
        "target_state_still_valid": evidence.target_state_still_valid,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests

STRUCTURAL_CHECKS = ("policy_valid", "start_valid", "evidence_valid", "source_recomputed_valid", "source_start_authorization_ready", "source_binding_valid", "identity_binding_valid", "source_start_route_binding_valid", "completion_review_route_binding_valid", "package_binding_valid", "state_binding_valid", "operator_bound_to_authorization", "operator_allowed", "operator_organization_allowed", "operator_separated_from_authorizer", "operator_separated_from_prior_actors", "operator_organization_separated", "objective_allowed", "start_delay_valid", "evidence_fresh", "completion_review_delay_valid", "time_order_valid", "source_start_deadline_valid", "external_operation_absent", "repository_change_absent")
DENIAL_CHECKS = ("operator_mandate_verified", "operator_authority_verified", "operator_identity_confirmed", "start_authorization_fresh", "package_fresh", "current_state_not_stale", "target_state_still_valid", "no_unresolved_anomaly", "recovery_not_in_progress", "institutional_hold_absent", "emergency_state_absent")

def compute_artifact(start: Rec, evidence: Rec, policy: Rec, source_authorization, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(start, evidence, policy, source_authorization, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_authorization.authorized_at_epoch_seconds <= start.start_requested_at_epoch_seconds <= start.started_at_epoch_seconds <= source_authorization.transition_start_deadline_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_authorization_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in DENIAL_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = DENIED, failed
        elif start.transition_start_confirmed:
            status, reason = STARTED, "started_for_separate_transition_completion_review_only"
        else:
            status, reason = DENIED, "transition_start_not_confirmed"
    issued = status != REJECTED
    started = status == STARTED
    denied = status == DENIED
    artifact = Rec(transition_start_id=start.transition_start_id, status=status, reason=reason, transition_operator_id=start.transition_operator_id, transition_operator_organization_id=start.transition_operator_organization_id, source_transition_start_authorization_id=start.source_transition_start_authorization_id, source_transition_start_authorization_record_digest=start.source_transition_start_authorization_record_digest, source_transition_start_authorizer_id=start.source_transition_start_authorizer_id, source_transition_approval_id=start.source_transition_approval_id, transition_package_digest=start.transition_package_digest, expected_current_lifecycle_state_digest=start.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=start.proposed_target_lifecycle_state_digest, source_transition_start_route_digest=start.source_transition_start_route_digest, transition_completion_review_route_digest=start.transition_completion_review_route_digest, transition_completion_review_deadline_at_epoch_seconds=start.transition_completion_review_deadline_at_epoch_seconds, subject_id=start.subject_id, requester_id=start.requester_id, policy_digest=policy.policy_digest, start_digest=start.start_digest, evidence_digest=evidence.evidence_digest, checks=checks, evidence_digests=expected_digests, source_start_authorization_ready=checks["source_start_authorization_ready"], transition_start_record_issued=issued, transition_start_completed=issued, lifecycle_transition_started=started, transition_start_denied=denied, transition_start_rejected=status == REJECTED, ready_for_separate_transition_completion_review=started, transition_completion_review_required_next=started, transition_completion_review_route_required_next=started, transition_restart_or_reauthorization_required_next=denied, transition_restart_or_reauthorization_route_required_next=denied, lifecycle_transition_completed=False, lifecycle_transition_performed=False, lifecycle_state_changed=False, authority_changed=False, quiescence_state_changed=False, terminal_state_changed=False, terminal_marker_written=False, resource_removed=False, external_operation_performed=False, repository_changed=False, lifecycle_state_read_only=True, repository_read_only=True, record_digest="", version=VERSION)
    artifact.record_digest = record_digest(artifact)
    return artifact

def verify_artifact(*args: Any, **kwargs: Any) -> Rec:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError("lifecycle_transition_start_record_invalid:" + issues[0])
    return artifact

def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("transition_start_recomputation_mismatch")
    if artifact.status not in (STARTED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == STARTED and not all((artifact.transition_start_record_issued, artifact.transition_start_completed, artifact.lifecycle_transition_started, artifact.ready_for_separate_transition_completion_review, artifact.transition_completion_review_required_next, artifact.transition_completion_review_route_required_next, not artifact.lifecycle_transition_completed, not artifact.lifecycle_transition_performed)):
        issues.append("started_gate_invalid")
    if artifact.status == DENIED and not all((artifact.transition_start_record_issued, artifact.transition_start_completed, artifact.transition_start_denied, not artifact.lifecycle_transition_started, not artifact.transition_completion_review_required_next, artifact.transition_restart_or_reauthorization_required_next)):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and any((artifact.transition_start_record_issued, artifact.transition_start_completed, artifact.lifecycle_transition_started, artifact.transition_completion_review_required_next, artifact.transition_restart_or_reauthorization_required_next)):
        issues.append("rejected_record_issued")
    if any((artifact.lifecycle_transition_completed, artifact.lifecycle_transition_performed, artifact.lifecycle_state_changed, artifact.authority_changed, artifact.quiescence_state_changed, artifact.terminal_state_changed, artifact.terminal_marker_written, artifact.resource_removed, artifact.external_operation_performed, artifact.repository_changed)):
        issues.append("completion_or_repository_effect_performed")
    if not artifact.lifecycle_state_read_only or not artifact.repository_read_only:
        issues.append("read_only_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
