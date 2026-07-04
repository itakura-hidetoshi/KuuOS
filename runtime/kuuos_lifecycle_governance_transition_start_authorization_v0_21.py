#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_transition_approval_v0_20 import (
    APPROVED as SOURCE_APPROVED,
    artifact_issues as source_artifact_issues,
    all_source_digests as approval_source_digests,
)

VERSION = "kuuos_lifecycle_bounded_transition_start_authorization_v0_21"
AUTHORIZED = "LIFECYCLE_BOUNDED_TRANSITION_START_AUTHORIZATION_AUTHORIZED_FOR_SEPARATE_TRANSITION_START"
DENIED = "LIFECYCLE_BOUNDED_TRANSITION_START_AUTHORIZATION_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_TRANSITION_START_AUTHORIZATION_REJECTED"
OBJECTIVE = "AUTHORIZE_APPROVED_LIFECYCLE_TRANSITION_PACKAGE_FOR_SEPARATE_START_ONLY"
SOURCE_ORDER_CHECK = "source_approval_precedes_start_authorization_and_deadline_valid"

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

def authorization_digest(value: Rec) -> str:
    return _digest(value, "authorization_digest")

def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")

def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))

def make_policy(policy_id: str, *, allowed_transition_start_authorizer_ids: tuple[str, ...], allowed_transition_start_authorizer_organization_ids: tuple[str, ...], allowed_future_transition_operator_ids: tuple[str, ...], max_authorization_delay_seconds: int = 900, max_evidence_age_seconds: int = 300, max_transition_start_delay_seconds: int = 900) -> Rec:
    value = Rec(policy_id=policy_id, allowed_transition_start_authorizer_ids=_canon(allowed_transition_start_authorizer_ids), allowed_transition_start_authorizer_organization_ids=_canon(allowed_transition_start_authorizer_organization_ids), allowed_future_transition_operator_ids=_canon(allowed_future_transition_operator_ids), max_authorization_delay_seconds=max_authorization_delay_seconds, max_evidence_age_seconds=max_evidence_age_seconds, max_transition_start_delay_seconds=max_transition_start_delay_seconds, approved_source_required=True, source_recomputation_required=True, transition_start_route_required=True, authorizer_authority_required=True, authorizer_separation_required=True, lifecycle_state_read_only=True, repository_read_only=True, policy_digest="", version=VERSION)
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_start_authorization_policy_invalid:" + issues[0])
    return value

def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_transition_start_authorizer_ids or not value.allowed_transition_start_authorizer_organization_ids or not value.allowed_future_transition_operator_ids:
        issues.append("allowed_actor_missing")
    if min(value.max_authorization_delay_seconds, value.max_evidence_age_seconds, value.max_transition_start_delay_seconds) <= 0:
        issues.append("bound_invalid")
    if not value.lifecycle_state_read_only or not value.repository_read_only:
        issues.append("read_only_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)

def all_source_digests(source_approval, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = approval_source_digests(source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:]))
    result.update(lifecycle_transition_approval=source_approval.approval_digest, lifecycle_transition_approval_evidence=source_evidence.evidence_digest, lifecycle_transition_approval_policy=source_policy.policy_digest, lifecycle_transition_approval_record=source_record.record_digest)
    return result

def source_recomputed_valid(source_approval, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_approval, source_evidence, source_policy, *source_args)

def expected_transition_start_route_digest(source_approval, source_record, *, transition_start_authorization_id: str, transition_start_authorizer_id: str, future_transition_operator_id: str, transition_package_digest: str, expected_current_lifecycle_state_digest: str, proposed_target_lifecycle_state_digest: str, transition_start_deadline_at_epoch_seconds: int) -> str:
    return canonical_digest({"source_transition_approval_id": source_approval.transition_approval_id, "source_transition_approval_record_digest": source_record.record_digest, "source_transition_start_authorization_route_digest": source_approval.transition_start_authorization_route_digest, "transition_start_authorization_id": transition_start_authorization_id, "transition_start_authorizer_id": transition_start_authorizer_id, "future_transition_operator_id": future_transition_operator_id, "transition_package_digest": transition_package_digest, "expected_current_lifecycle_state_digest": expected_current_lifecycle_state_digest, "proposed_target_lifecycle_state_digest": proposed_target_lifecycle_state_digest, "transition_start_deadline_at_epoch_seconds": transition_start_deadline_at_epoch_seconds})

def make_evidence(source_approval, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(source_transition_approval_id=source_approval.transition_approval_id, source_transition_approval_record_digest=source_record.record_digest, source_artifact_digests=all_source_digests(source_approval, source_evidence, source_policy, source_record, source_args), source_transition_preparation_id=source_approval.source_transition_preparation_id, source_transition_preparer_id=source_approval.source_transition_preparer_id, source_transition_decision_id=source_approval.source_transition_decision_id, source_transition_decision_maker_id=source_approval.source_transition_decision_maker_id, source_transition_approver_id=source_approval.transition_approver_id, source_transition_approver_organization_id=source_approval.transition_approver_organization_id, subject_id=source_approval.subject_id, requester_id=source_approval.requester_id, future_transition_operator_id=source_approval.future_transition_operator_id, transition_package_digest=source_approval.transition_package_digest, expected_current_lifecycle_state_digest=source_approval.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_approval.proposed_target_lifecycle_state_digest, source_transition_start_authorization_route_digest=source_approval.transition_start_authorization_route_digest, package_expiry_at_epoch_seconds=source_evidence.package_expiry_at_epoch_seconds, transition_start_authorization_deadline_at_epoch_seconds=source_approval.transition_start_authorization_deadline_at_epoch_seconds)
    values.update(overrides)
    if "transition_start_route_digest" not in values:
        values["transition_start_route_digest"] = expected_transition_start_route_digest(source_approval, source_record, transition_start_authorization_id=values["transition_start_authorization_id"], transition_start_authorizer_id=values["transition_start_authorizer_id"], future_transition_operator_id=values["future_transition_operator_id"], transition_package_digest=values["transition_package_digest"], expected_current_lifecycle_state_digest=values["expected_current_lifecycle_state_digest"], proposed_target_lifecycle_state_digest=values["proposed_target_lifecycle_state_digest"], transition_start_deadline_at_epoch_seconds=values["transition_start_deadline_at_epoch_seconds"])
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_start_authorization_evidence_invalid:" + issues[0])
    return value

def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = ("evidence_id", "transition_start_authorization_id", "transition_start_authorizer_id", "transition_start_authorizer_organization_id", "authorizer_mandate_receipt_digest", "authorizer_authority_receipt_digest", "authorizer_identity_confirmation_digest", "conflict_disclosure_digest", "jurisdiction_receipt_digest", "source_transition_approval_id", "source_transition_approval_record_digest", "source_transition_start_authorization_route_digest", "transition_start_route_digest", "transition_package_digest", "expected_current_lifecycle_state_digest", "proposed_target_lifecycle_state_digest", "approval_record_freshness_receipt_digest", "package_freshness_receipt_digest", "current_state_freshness_receipt_digest", "target_state_validity_receipt_digest")
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.authorization_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.authorized_at_epoch_seconds, value.transition_start_authorization_deadline_at_epoch_seconds, value.transition_start_deadline_at_epoch_seconds, value.package_expiry_at_epoch_seconds) < 0:
        issues.append("negative_authorization_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)

def make_submission(transition_start_authorization_id: str, transition_start_authorizer_id: str, transition_start_authorizer_organization_id: str, authorization_requested_at_epoch_seconds: int, authorized_at_epoch_seconds: int, source_approval, source_record, authorization_evidence: Rec, *, transition_start_route_digest: str, transition_start_deadline_at_epoch_seconds: int, transition_start_authorized: bool, denial_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(transition_start_authorization_id=transition_start_authorization_id, transition_start_authorizer_id=transition_start_authorizer_id, transition_start_authorizer_organization_id=transition_start_authorizer_organization_id, objective=objective, authorization_requested_at_epoch_seconds=authorization_requested_at_epoch_seconds, authorized_at_epoch_seconds=authorized_at_epoch_seconds, source_transition_approval_id=source_approval.transition_approval_id, source_transition_approval_record_digest=source_record.record_digest, subject_id=source_approval.subject_id, requester_id=source_approval.requester_id, source_transition_preparation_id=source_approval.source_transition_preparation_id, source_transition_decision_id=source_approval.source_transition_decision_id, source_transition_approver_id=source_approval.transition_approver_id, future_transition_operator_id=source_approval.future_transition_operator_id, transition_package_digest=source_approval.transition_package_digest, expected_current_lifecycle_state_digest=source_approval.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_approval.proposed_target_lifecycle_state_digest, source_transition_start_authorization_route_digest=source_approval.transition_start_authorization_route_digest, transition_start_route_digest=transition_start_route_digest, transition_start_deadline_at_epoch_seconds=transition_start_deadline_at_epoch_seconds, transition_start_authorization_evidence_digest=authorization_evidence.evidence_digest, transition_start_authorized=transition_start_authorized, denial_reason_digest=denial_reason_digest, authorization_digest="", version=VERSION)
    value.authorization_digest = authorization_digest(value)
    issues = submission_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_start_authorization_invalid:" + issues[0])
    return value

def submission_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("denial_reason_digest", "authorization_digest", "version", "transition_start_authorized"):
            continue
        if content == "" or content is None:
            issues.append("required_authorization_field_missing")
            break
    if not value.transition_start_authorized and not value.denial_reason_digest:
        issues.append("denial_reason_missing")
    if min(value.authorization_requested_at_epoch_seconds, value.authorized_at_epoch_seconds, value.transition_start_deadline_at_epoch_seconds) < 0:
        issues.append("negative_authorization_time")
    if value.authorization_digest != authorization_digest(value):
        issues.append("authorization_digest_mismatch")
    return tuple(issues)

def _source_ready(record) -> bool:
    return all((record.status == SOURCE_APPROVED, record.transition_approval_record_issued, record.transition_approval_completed, record.transition_package_approved, record.ready_for_separate_transition_start_authorization, record.transition_start_authorization_required_next, record.transition_start_authorization_route_required_next, not record.lifecycle_transition_start_authorized, not record.lifecycle_transition_started, not record.lifecycle_transition_completed, not record.lifecycle_transition_performed, not record.external_operation_performed, not record.repository_changed, record.lifecycle_state_read_only, record.repository_read_only))

def _prior_actor_ids(source_approval, source_evidence) -> set[str]:
    return {source_approval.subject_id, source_approval.requester_id, source_approval.source_transition_preparer_id, source_approval.source_transition_decision_maker_id, source_approval.transition_approver_id, source_evidence.source_transition_preparer_id, source_evidence.source_transition_decision_maker_id}

def evaluate(authorization: Rec, evidence: Rec, policy: Rec, source_approval, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_approval, source_evidence, source_policy, source_record, source_args)
    expected_start_route = expected_transition_start_route_digest(source_approval, source_record, transition_start_authorization_id=authorization.transition_start_authorization_id, transition_start_authorizer_id=authorization.transition_start_authorizer_id, future_transition_operator_id=source_approval.future_transition_operator_id, transition_package_digest=source_approval.transition_package_digest, expected_current_lifecycle_state_digest=source_approval.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_approval.proposed_target_lifecycle_state_digest, transition_start_deadline_at_epoch_seconds=authorization.transition_start_deadline_at_epoch_seconds)
    prior = _prior_actor_ids(source_approval, source_evidence)
    authorization_delay = evidence.authorized_at_epoch_seconds - source_approval.approved_at_epoch_seconds
    evidence_age = evidence.authorized_at_epoch_seconds - evidence.captured_at_epoch_seconds
    start_delay = evidence.transition_start_deadline_at_epoch_seconds - evidence.authorized_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "authorization_valid": not submission_issues(authorization),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_approval, source_evidence, source_policy, source_record, source_args),
        "source_transition_approval_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and authorization.source_transition_approval_id == evidence.source_transition_approval_id == source_approval.transition_approval_id and authorization.source_transition_approval_record_digest == evidence.source_transition_approval_record_digest == source_record.record_digest,
        "identity_binding_valid": authorization.transition_start_authorization_id == evidence.transition_start_authorization_id and authorization.transition_start_authorizer_id == evidence.transition_start_authorizer_id and authorization.transition_start_authorizer_organization_id == evidence.transition_start_authorizer_organization_id and authorization.transition_start_authorization_evidence_digest == evidence.evidence_digest,
        "source_start_authorization_route_binding_valid": authorization.source_transition_start_authorization_route_digest == evidence.source_transition_start_authorization_route_digest == source_approval.transition_start_authorization_route_digest,
        "transition_start_route_binding_valid": authorization.transition_start_route_digest == evidence.transition_start_route_digest == expected_start_route,
        "package_binding_valid": authorization.transition_package_digest == evidence.transition_package_digest == source_approval.transition_package_digest,
        "state_binding_valid": authorization.expected_current_lifecycle_state_digest == evidence.expected_current_lifecycle_state_digest == source_approval.expected_current_lifecycle_state_digest and authorization.proposed_target_lifecycle_state_digest == evidence.proposed_target_lifecycle_state_digest == source_approval.proposed_target_lifecycle_state_digest,
        "future_operator_bound": authorization.future_transition_operator_id == evidence.future_transition_operator_id == source_approval.future_transition_operator_id,
        "future_operator_allowed": authorization.future_transition_operator_id in policy.allowed_future_transition_operator_ids,
        "authorizer_allowed": authorization.transition_start_authorizer_id in policy.allowed_transition_start_authorizer_ids,
        "authorizer_organization_allowed": authorization.transition_start_authorizer_organization_id in policy.allowed_transition_start_authorizer_organization_ids,
        "authorizer_separated_from_approver": authorization.transition_start_authorizer_id != source_approval.transition_approver_id,
        "authorizer_separated_from_prior_actors": authorization.transition_start_authorizer_id not in prior,
        "authorizer_separated_from_future_operator": authorization.transition_start_authorizer_id != authorization.future_transition_operator_id,
        "authorizer_organization_separated": authorization.transition_start_authorizer_organization_id != source_approval.transition_approver_organization_id,
        "objective_allowed": authorization.objective == OBJECTIVE,
        "authorization_delay_valid": 0 <= authorization_delay <= policy.max_authorization_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "transition_start_delay_valid": 0 < start_delay <= policy.max_transition_start_delay_seconds,
        "time_order_valid": source_approval.approved_at_epoch_seconds <= evidence.authorization_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.authorized_at_epoch_seconds < evidence.transition_start_deadline_at_epoch_seconds <= evidence.package_expiry_at_epoch_seconds,
        "source_authorization_deadline_valid": evidence.authorized_at_epoch_seconds <= source_approval.transition_start_authorization_deadline_at_epoch_seconds,
        "external_operation_absent": not evidence.external_operation_performed,
        "repository_change_absent": not evidence.repository_changed,
        "authorizer_mandate_verified": evidence.authorizer_mandate_verified,
        "authorizer_authority_verified": evidence.authorizer_authority_verified,
        "authorizer_identity_confirmed": evidence.authorizer_identity_confirmed,
        "conflict_disclosure_complete": evidence.conflict_disclosure_complete,
        "material_conflict_absent": not evidence.material_conflict_present,
        "jurisdiction_verified": evidence.jurisdiction_verified,
        "approval_record_fresh": evidence.approval_record_fresh,
        "package_fresh": evidence.package_fresh,
        "current_state_not_stale": evidence.current_state_not_stale,
        "target_state_still_valid": evidence.target_state_still_valid,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests

STRUCTURAL_CHECKS = ("policy_valid", "authorization_valid", "evidence_valid", "source_recomputed_valid", "source_transition_approval_ready", "source_binding_valid", "identity_binding_valid", "source_start_authorization_route_binding_valid", "transition_start_route_binding_valid", "package_binding_valid", "state_binding_valid", "future_operator_bound", "future_operator_allowed", "authorizer_allowed", "authorizer_organization_allowed", "authorizer_separated_from_approver", "authorizer_separated_from_prior_actors", "authorizer_separated_from_future_operator", "authorizer_organization_separated", "objective_allowed", "authorization_delay_valid", "evidence_fresh", "transition_start_delay_valid", "time_order_valid", "source_authorization_deadline_valid", "external_operation_absent", "repository_change_absent")
DENIAL_CHECKS = ("authorizer_mandate_verified", "authorizer_authority_verified", "authorizer_identity_confirmed", "conflict_disclosure_complete", "material_conflict_absent", "jurisdiction_verified", "approval_record_fresh", "package_fresh", "current_state_not_stale", "target_state_still_valid", "no_unresolved_anomaly", "recovery_not_in_progress", "institutional_hold_absent", "emergency_state_absent")

def compute_artifact(authorization: Rec, evidence: Rec, policy: Rec, source_approval, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(authorization, evidence, policy, source_approval, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_approval.approved_at_epoch_seconds <= authorization.authorization_requested_at_epoch_seconds <= authorization.authorized_at_epoch_seconds <= source_approval.transition_start_authorization_deadline_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_approval_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in DENIAL_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = DENIED, failed
        elif authorization.transition_start_authorized:
            status, reason = AUTHORIZED, "authorized_for_separate_transition_start_only"
        else:
            status, reason = DENIED, "start_authorization_not_granted"
    issued = status != REJECTED
    authorized = status == AUTHORIZED
    denied = status == DENIED
    artifact = Rec(transition_start_authorization_id=authorization.transition_start_authorization_id, status=status, reason=reason, transition_start_authorizer_id=authorization.transition_start_authorizer_id, transition_start_authorizer_organization_id=authorization.transition_start_authorizer_organization_id, source_transition_approval_id=authorization.source_transition_approval_id, source_transition_approval_record_digest=authorization.source_transition_approval_record_digest, source_transition_approver_id=authorization.source_transition_approver_id, future_transition_operator_id=authorization.future_transition_operator_id, transition_package_digest=authorization.transition_package_digest, expected_current_lifecycle_state_digest=authorization.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=authorization.proposed_target_lifecycle_state_digest, source_transition_start_authorization_route_digest=authorization.source_transition_start_authorization_route_digest, transition_start_route_digest=authorization.transition_start_route_digest, transition_start_deadline_at_epoch_seconds=authorization.transition_start_deadline_at_epoch_seconds, subject_id=authorization.subject_id, requester_id=authorization.requester_id, policy_digest=policy.policy_digest, authorization_digest=authorization.authorization_digest, evidence_digest=evidence.evidence_digest, checks=checks, evidence_digests=expected_digests, source_transition_approval_ready=checks["source_transition_approval_ready"], transition_start_authorization_record_issued=issued, transition_start_authorization_completed=issued, lifecycle_transition_start_authorized=authorized, transition_start_authorization_denied=denied, transition_start_authorization_rejected=status == REJECTED, ready_for_separate_transition_start=authorized, transition_start_required_next=authorized, transition_start_route_required_next=authorized, transition_reauthorization_or_reapproval_required_next=denied, transition_reauthorization_or_reapproval_route_required_next=denied, lifecycle_transition_started=False, lifecycle_transition_completed=False, lifecycle_transition_performed=False, lifecycle_state_changed=False, authority_changed=False, quiescence_state_changed=False, terminal_state_changed=False, terminal_marker_written=False, resource_removed=False, external_operation_performed=False, repository_changed=False, lifecycle_state_read_only=True, repository_read_only=True, record_digest="", version=VERSION)
    artifact.record_digest = record_digest(artifact)
    return artifact

def verify_artifact(*args: Any, **kwargs: Any) -> Rec:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError("lifecycle_transition_start_authorization_record_invalid:" + issues[0])
    return artifact

def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("transition_start_authorization_recomputation_mismatch")
    if artifact.status not in (AUTHORIZED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == AUTHORIZED and not all((artifact.transition_start_authorization_record_issued, artifact.transition_start_authorization_completed, artifact.lifecycle_transition_start_authorized, artifact.ready_for_separate_transition_start, artifact.transition_start_required_next, artifact.transition_start_route_required_next, not artifact.lifecycle_transition_started, not artifact.lifecycle_transition_performed)):
        issues.append("authorized_gate_invalid")
    if artifact.status == DENIED and not all((artifact.transition_start_authorization_record_issued, artifact.transition_start_authorization_completed, artifact.transition_start_authorization_denied, not artifact.lifecycle_transition_start_authorized, not artifact.transition_start_required_next, artifact.transition_reauthorization_or_reapproval_required_next)):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and any((artifact.transition_start_authorization_record_issued, artifact.transition_start_authorization_completed, artifact.lifecycle_transition_start_authorized, artifact.transition_start_required_next, artifact.transition_reauthorization_or_reapproval_required_next)):
        issues.append("rejected_record_issued")
    if any((artifact.lifecycle_transition_started, artifact.lifecycle_transition_completed, artifact.lifecycle_transition_performed, artifact.lifecycle_state_changed, artifact.authority_changed, artifact.quiescence_state_changed, artifact.terminal_state_changed, artifact.terminal_marker_written, artifact.resource_removed, artifact.external_operation_performed, artifact.repository_changed)):
        issues.append("transition_or_repository_effect_performed")
    if not artifact.lifecycle_state_read_only or not artifact.repository_read_only:
        issues.append("read_only_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
