#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_transition_preparation_core_v0_19 import artifact_issues as source_artifact_issues
from runtime.kuuos_lifecycle_transition_preparation_source_v0_19 import all_source_digests as prior_source_digests
from runtime.kuuos_lifecycle_transition_preparation_types_v0_19 import PREPARED as SOURCE_PREPARED

VERSION = "kuuos_lifecycle_bounded_transition_approval_v0_20"
APPROVED = "LIFECYCLE_BOUNDED_TRANSITION_APPROVAL_APPROVED_FOR_SEPARATE_TRANSITION_START_AUTHORIZATION"
DENIED = "LIFECYCLE_BOUNDED_TRANSITION_APPROVAL_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_TRANSITION_APPROVAL_REJECTED"
OBJECTIVE = "APPROVE_PREPARED_LIFECYCLE_TRANSITION_PACKAGE_FOR_SEPARATE_START_AUTHORIZATION_ONLY"
SOURCE_ORDER_CHECK = "source_preparation_precedes_approval_and_deadline_valid"

class Rec(SimpleNamespace):
    def to_dict(self) -> dict[str, Any]:
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, tuple):
                result[key] = list(value)
            elif isinstance(value, dict):
                result[key] = dict(value)
            else:
                result[key] = value
        return result

def _digest(value: Rec, field: str) -> str:
    payload = value.to_dict()
    payload.pop(field, None)
    return canonical_digest(payload)

def policy_digest(value: Rec) -> str:
    return _digest(value, "policy_digest")

def evidence_digest(value: Rec) -> str:
    return _digest(value, "evidence_digest")

def submission_digest(value: Rec) -> str:
    return _digest(value, "approval_digest")

def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")

def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))

def make_policy(policy_id: str, *, allowed_transition_approver_ids: tuple[str, ...], allowed_transition_approver_organization_ids: tuple[str, ...], allowed_future_transition_operator_ids: tuple[str, ...], max_approval_delay_seconds: int = 900, max_evidence_age_seconds: int = 300, max_start_authorization_delay_seconds: int = 900) -> Rec:
    value = Rec(policy_id=policy_id, allowed_transition_approver_ids=_canon(allowed_transition_approver_ids), allowed_transition_approver_organization_ids=_canon(allowed_transition_approver_organization_ids), allowed_future_transition_operator_ids=_canon(allowed_future_transition_operator_ids), max_approval_delay_seconds=max_approval_delay_seconds, max_evidence_age_seconds=max_evidence_age_seconds, max_start_authorization_delay_seconds=max_start_authorization_delay_seconds, source_recomputation_required=True, prepared_source_required=True, package_route_binding_required=True, approver_authority_required=True, approver_separation_required=True, start_authorization_route_required=True, lifecycle_state_read_only=True, repository_read_only=True, policy_digest="", version=VERSION)
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_approval_policy_invalid:" + issues[0])
    return value

def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_transition_approver_ids or not value.allowed_transition_approver_organization_ids or not value.allowed_future_transition_operator_ids:
        issues.append("allowed_actor_missing")
    if min(value.max_approval_delay_seconds, value.max_evidence_age_seconds, value.max_start_authorization_delay_seconds) <= 0:
        issues.append("bound_invalid")
    if not value.lifecycle_state_read_only or not value.repository_read_only:
        issues.append("read_only_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)

def all_source_digests(source_preparation, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = prior_source_digests(source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:]))
    result.update(lifecycle_transition_preparation=source_preparation.preparation_digest, lifecycle_transition_preparation_evidence=source_evidence.evidence_digest, lifecycle_transition_preparation_policy=source_policy.policy_digest, lifecycle_transition_preparation_record=source_record.record_digest)
    return result

def source_recomputed_valid(source_preparation, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_preparation, source_evidence, source_policy, *source_args)

def expected_transition_start_authorization_route_digest(source_preparation, source_record, *, transition_approval_id: str, transition_package_digest: str, transition_approver_id: str, future_transition_operator_id: str, expected_current_lifecycle_state_digest: str, proposed_target_lifecycle_state_digest: str, transition_start_authorization_deadline_at_epoch_seconds: int) -> str:
    return canonical_digest({"source_transition_preparation_id": source_preparation.transition_preparation_id, "source_transition_preparation_record_digest": source_record.record_digest, "transition_approval_route_digest": source_preparation.transition_approval_route_digest, "transition_approval_id": transition_approval_id, "transition_package_digest": transition_package_digest, "transition_approver_id": transition_approver_id, "future_transition_operator_id": future_transition_operator_id, "expected_current_lifecycle_state_digest": expected_current_lifecycle_state_digest, "proposed_target_lifecycle_state_digest": proposed_target_lifecycle_state_digest, "transition_start_authorization_deadline_at_epoch_seconds": transition_start_authorization_deadline_at_epoch_seconds})

def make_evidence(source_preparation, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(source_transition_preparation_id=source_preparation.transition_preparation_id, source_transition_preparation_record_digest=source_record.record_digest, source_artifact_digests=all_source_digests(source_preparation, source_evidence, source_policy, source_record, source_args), source_transition_preparer_id=source_preparation.transition_preparer_id, source_transition_preparer_organization_id=source_preparation.transition_preparer_organization_id, source_transition_decision_id=source_preparation.source_transition_decision_id, source_transition_decision_maker_id=source_preparation.source_transition_decision_maker_id, source_transition_decision_maker_organization_id=source_evidence.source_transition_decision_maker_organization_id, subject_id=source_preparation.subject_id, subject_kind=source_preparation.subject_kind, subject_version=source_preparation.subject_version, requester_id=source_preparation.requester_id, future_transition_operator_id=source_preparation.future_transition_operator_id, transition_package_digest=source_preparation.transition_package_digest, expected_current_lifecycle_state_digest=source_preparation.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_preparation.proposed_target_lifecycle_state_digest, transition_approval_route_digest=source_preparation.transition_approval_route_digest, package_expiry_at_epoch_seconds=source_preparation.package_expiry_at_epoch_seconds, transition_approval_deadline_at_epoch_seconds=source_preparation.transition_approval_deadline_at_epoch_seconds)
    values.update(overrides)
    if "transition_start_authorization_route_digest" not in values:
        values["transition_start_authorization_route_digest"] = expected_transition_start_authorization_route_digest(source_preparation, source_record, transition_approval_id=values["transition_approval_id"], transition_package_digest=values["transition_package_digest"], transition_approver_id=values["transition_approver_id"], future_transition_operator_id=values["future_transition_operator_id"], expected_current_lifecycle_state_digest=values["expected_current_lifecycle_state_digest"], proposed_target_lifecycle_state_digest=values["proposed_target_lifecycle_state_digest"], transition_start_authorization_deadline_at_epoch_seconds=values["transition_start_authorization_deadline_at_epoch_seconds"])
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_approval_evidence_invalid:" + issues[0])
    return value

def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = ("evidence_id", "transition_approval_id", "transition_approver_id", "transition_approver_organization_id", "approver_mandate_receipt_digest", "approver_authority_receipt_digest", "approver_identity_confirmation_digest", "conflict_disclosure_digest", "jurisdiction_receipt_digest", "package_freshness_receipt_digest", "current_state_freshness_receipt_digest", "target_state_validity_receipt_digest", "source_transition_preparation_id", "source_transition_preparation_record_digest", "transition_package_digest", "transition_approval_route_digest", "transition_start_authorization_route_digest")
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.approval_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.approved_at_epoch_seconds, value.package_expiry_at_epoch_seconds, value.transition_approval_deadline_at_epoch_seconds, value.transition_start_authorization_deadline_at_epoch_seconds) < 0:
        issues.append("negative_approval_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)

def make_submission(transition_approval_id: str, transition_approver_id: str, transition_approver_organization_id: str, approval_requested_at_epoch_seconds: int, approved_at_epoch_seconds: int, source_preparation, source_record, approval_evidence: Rec, *, transition_start_authorization_route_digest: str, transition_start_authorization_deadline_at_epoch_seconds: int, transition_approval_granted: bool, denial_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(transition_approval_id=transition_approval_id, transition_approver_id=transition_approver_id, transition_approver_organization_id=transition_approver_organization_id, objective=objective, approval_requested_at_epoch_seconds=approval_requested_at_epoch_seconds, approved_at_epoch_seconds=approved_at_epoch_seconds, source_transition_preparation_id=source_preparation.transition_preparation_id, source_transition_preparation_record_digest=source_record.record_digest, subject_id=source_preparation.subject_id, subject_kind=source_preparation.subject_kind, subject_version=source_preparation.subject_version, transition_approval_evidence_digest=approval_evidence.evidence_digest, requester_id=source_preparation.requester_id, source_transition_preparer_id=source_preparation.transition_preparer_id, source_transition_decision_id=source_preparation.source_transition_decision_id, source_transition_decision_maker_id=source_preparation.source_transition_decision_maker_id, future_transition_operator_id=source_preparation.future_transition_operator_id, transition_package_digest=source_preparation.transition_package_digest, expected_current_lifecycle_state_digest=source_preparation.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_preparation.proposed_target_lifecycle_state_digest, transition_approval_route_digest=source_preparation.transition_approval_route_digest, transition_start_authorization_route_digest=transition_start_authorization_route_digest, transition_start_authorization_deadline_at_epoch_seconds=transition_start_authorization_deadline_at_epoch_seconds, transition_approval_granted=transition_approval_granted, denial_reason_digest=denial_reason_digest, approval_digest="", version=VERSION)
    value.approval_digest = submission_digest(value)
    issues = submission_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_approval_invalid:" + issues[0])
    return value

def submission_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    required = value.to_dict()
    for name in ("denial_reason_digest", "approval_digest", "version"):
        required.pop(name, None)
    if not all(required.values()):
        issues.append("required_approval_field_missing")
    if not value.transition_approval_granted and not value.denial_reason_digest:
        issues.append("denial_reason_missing")
    if min(value.approval_requested_at_epoch_seconds, value.approved_at_epoch_seconds, value.transition_start_authorization_deadline_at_epoch_seconds) < 0:
        issues.append("negative_approval_time")
    if value.approval_digest != submission_digest(value):
        issues.append("approval_digest_mismatch")
    return tuple(issues)

def _source_ready(record) -> bool:
    return all((record.status == SOURCE_PREPARED, record.transition_preparation_record_issued, record.transition_preparation_completed, record.transition_package_prepared, record.ready_for_separate_transition_approval, record.transition_approval_required_next, record.transition_approval_route_required_next, not record.lifecycle_transition_approved, not record.lifecycle_transition_started, not record.lifecycle_transition_completed, not record.lifecycle_transition_performed, not record.external_operation_performed, not record.repository_changed, record.lifecycle_state_read_only, record.repository_read_only))

def _prior_actor_ids(source_preparation, source_evidence) -> set[str]:
    return {source_preparation.subject_id, source_preparation.requester_id, source_preparation.transition_preparer_id, source_preparation.source_transition_decision_maker_id, source_evidence.source_decision_reviewer_id, source_evidence.source_authorization_decision_maker_id, source_evidence.source_operation_approver_id, source_evidence.source_operator_id, source_evidence.source_completion_reviewer_id, source_evidence.source_post_operation_reviewer_id, source_evidence.source_transition_reviewer_id}

def evaluate(approval: Rec, evidence: Rec, policy: Rec, source_preparation, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_preparation, source_evidence, source_policy, source_record, source_args)
    expected_start_route = expected_transition_start_authorization_route_digest(source_preparation, source_record, transition_approval_id=approval.transition_approval_id, transition_package_digest=source_preparation.transition_package_digest, transition_approver_id=approval.transition_approver_id, future_transition_operator_id=source_preparation.future_transition_operator_id, expected_current_lifecycle_state_digest=source_preparation.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_preparation.proposed_target_lifecycle_state_digest, transition_start_authorization_deadline_at_epoch_seconds=approval.transition_start_authorization_deadline_at_epoch_seconds)
    prior = _prior_actor_ids(source_preparation, source_evidence)
    approval_delay = evidence.approved_at_epoch_seconds - source_preparation.prepared_at_epoch_seconds
    evidence_age = evidence.approved_at_epoch_seconds - evidence.captured_at_epoch_seconds
    start_delay = evidence.transition_start_authorization_deadline_at_epoch_seconds - evidence.approved_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "approval_valid": not submission_issues(approval),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_preparation, source_evidence, source_policy, source_record, source_args),
        "source_transition_preparation_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and approval.source_transition_preparation_id == evidence.source_transition_preparation_id == source_preparation.transition_preparation_id and approval.source_transition_preparation_record_digest == evidence.source_transition_preparation_record_digest == source_record.record_digest,
        "identity_binding_valid": approval.transition_approval_id == evidence.transition_approval_id and approval.transition_approver_id == evidence.transition_approver_id and approval.transition_approver_organization_id == evidence.transition_approver_organization_id and approval.transition_approval_evidence_digest == evidence.evidence_digest,
        "package_route_binding_valid": approval.transition_package_digest == evidence.transition_package_digest == source_preparation.transition_package_digest and approval.transition_approval_route_digest == evidence.transition_approval_route_digest == source_preparation.transition_approval_route_digest,
        "state_binding_valid": approval.expected_current_lifecycle_state_digest == evidence.expected_current_lifecycle_state_digest == source_preparation.expected_current_lifecycle_state_digest and approval.proposed_target_lifecycle_state_digest == evidence.proposed_target_lifecycle_state_digest == source_preparation.proposed_target_lifecycle_state_digest,
        "start_authorization_route_binding_valid": approval.transition_start_authorization_route_digest == evidence.transition_start_authorization_route_digest == expected_start_route,
        "approver_bound_to_source": approval.transition_approver_id == source_preparation.transition_approver_id,
        "approver_allowed": approval.transition_approver_id in policy.allowed_transition_approver_ids,
        "approver_organization_allowed": approval.transition_approver_organization_id in policy.allowed_transition_approver_organization_ids,
        "future_operator_bound": approval.future_transition_operator_id == evidence.future_transition_operator_id == source_preparation.future_transition_operator_id,
        "future_operator_allowed": approval.future_transition_operator_id in policy.allowed_future_transition_operator_ids,
        "approver_separated_from_preparer": approval.transition_approver_id != source_preparation.transition_preparer_id,
        "approver_separated_from_decision_maker": approval.transition_approver_id != source_preparation.source_transition_decision_maker_id,
        "approver_separated_from_prior_actors": approval.transition_approver_id not in prior,
        "approver_separated_from_future_operator": approval.transition_approver_id != approval.future_transition_operator_id,
        "approver_organization_separated": approval.transition_approver_organization_id != source_preparation.transition_preparer_organization_id,
        "objective_allowed": approval.objective == OBJECTIVE,
        "approval_delay_valid": 0 <= approval_delay <= policy.max_approval_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "start_authorization_delay_valid": 0 < start_delay <= policy.max_start_authorization_delay_seconds,
        "time_order_valid": source_preparation.prepared_at_epoch_seconds <= evidence.approval_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.approved_at_epoch_seconds < evidence.transition_start_authorization_deadline_at_epoch_seconds <= evidence.package_expiry_at_epoch_seconds,
        "source_approval_deadline_valid": evidence.approved_at_epoch_seconds <= source_preparation.transition_approval_deadline_at_epoch_seconds,
        "approver_mandate_verified": evidence.approver_mandate_verified,
        "approver_authority_verified": evidence.approver_authority_verified,
        "approver_identity_confirmed": evidence.approver_identity_confirmed,
        "conflict_disclosure_complete": evidence.conflict_disclosure_complete,
        "material_conflict_absent": not evidence.material_conflict_present,
        "jurisdiction_verified": evidence.jurisdiction_verified,
        "package_fresh": evidence.package_fresh,
        "current_state_not_stale": evidence.current_state_not_stale,
        "target_state_still_valid": evidence.target_state_still_valid,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
        "external_operation_absent": not evidence.external_operation_performed,
        "repository_change_absent": not evidence.repository_changed,
    }
    return checks, expected_digests

STRUCTURAL_CHECKS = ("policy_valid", "approval_valid", "evidence_valid", "source_recomputed_valid", "source_transition_preparation_ready", "source_binding_valid", "identity_binding_valid", "package_route_binding_valid", "state_binding_valid", "start_authorization_route_binding_valid", "approver_bound_to_source", "approver_allowed", "approver_organization_allowed", "future_operator_bound", "future_operator_allowed", "approver_separated_from_preparer", "approver_separated_from_decision_maker", "approver_separated_from_prior_actors", "approver_separated_from_future_operator", "approver_organization_separated", "objective_allowed", "approval_delay_valid", "evidence_fresh", "start_authorization_delay_valid", "time_order_valid", "source_approval_deadline_valid", "external_operation_absent", "repository_change_absent")
DENIAL_CHECKS = ("approver_mandate_verified", "approver_authority_verified", "approver_identity_confirmed", "conflict_disclosure_complete", "material_conflict_absent", "jurisdiction_verified", "package_fresh", "current_state_not_stale", "target_state_still_valid", "no_unresolved_anomaly", "recovery_not_in_progress", "institutional_hold_absent", "emergency_state_absent")

def compute_artifact(approval: Rec, evidence: Rec, policy: Rec, source_preparation, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(approval, evidence, policy, source_preparation, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_preparation.prepared_at_epoch_seconds <= approval.approval_requested_at_epoch_seconds <= approval.approved_at_epoch_seconds <= source_preparation.transition_approval_deadline_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_preparation_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in DENIAL_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = DENIED, failed
        elif approval.transition_approval_granted:
            status, reason = APPROVED, "approved_for_separate_transition_start_authorization_only"
        else:
            status, reason = DENIED, "approval_not_granted"
    issued = status != REJECTED
    approved = status == APPROVED
    denied = status == DENIED
    artifact = Rec(transition_approval_id=approval.transition_approval_id, status=status, reason=reason, transition_approver_id=approval.transition_approver_id, transition_approver_organization_id=approval.transition_approver_organization_id, source_transition_preparation_id=approval.source_transition_preparation_id, source_transition_preparer_id=approval.source_transition_preparer_id, source_transition_decision_id=approval.source_transition_decision_id, source_transition_decision_maker_id=approval.source_transition_decision_maker_id, future_transition_operator_id=approval.future_transition_operator_id, transition_package_digest=approval.transition_package_digest, expected_current_lifecycle_state_digest=approval.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=approval.proposed_target_lifecycle_state_digest, transition_approval_route_digest=approval.transition_approval_route_digest, transition_start_authorization_route_digest=approval.transition_start_authorization_route_digest, subject_id=approval.subject_id, requester_id=approval.requester_id, policy_digest=policy.policy_digest, approval_digest=approval.approval_digest, evidence_digest=evidence.evidence_digest, checks=checks, evidence_digests=expected_digests, source_transition_preparation_ready=checks["source_transition_preparation_ready"], transition_approval_record_issued=issued, transition_approval_completed=issued, transition_package_approved=approved, transition_approval_denied=denied, transition_approval_rejected=status == REJECTED, ready_for_separate_transition_start_authorization=approved, transition_start_authorization_required_next=approved, transition_start_authorization_route_required_next=approved, transition_reapproval_or_repreparation_required_next=denied, transition_reapproval_or_repreparation_route_required_next=denied, lifecycle_transition_start_authorized=False, lifecycle_transition_started=False, lifecycle_transition_completed=False, lifecycle_transition_performed=False, lifecycle_state_changed=False, authority_changed=False, quiescence_state_changed=False, terminal_state_changed=False, terminal_marker_written=False, resource_removed=False, external_operation_performed=False, repository_changed=False, lifecycle_state_read_only=True, repository_read_only=True, record_digest="", version=VERSION)
    artifact.record_digest = record_digest(artifact)
    return artifact

def verify_artifact(*args: Any, **kwargs: Any) -> Rec:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError("lifecycle_transition_approval_record_invalid:" + issues[0])
    return artifact

def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("transition_approval_recomputation_mismatch")
    if artifact.status not in (APPROVED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == APPROVED and not all((artifact.transition_approval_record_issued, artifact.transition_approval_completed, artifact.transition_package_approved, artifact.ready_for_separate_transition_start_authorization, artifact.transition_start_authorization_required_next, artifact.transition_start_authorization_route_required_next, not artifact.lifecycle_transition_start_authorized, not artifact.lifecycle_transition_started, not artifact.lifecycle_transition_performed)):
        issues.append("approved_gate_invalid")
    if artifact.status == DENIED and not all((artifact.transition_approval_record_issued, artifact.transition_approval_completed, artifact.transition_approval_denied, not artifact.transition_package_approved, not artifact.transition_start_authorization_required_next, artifact.transition_reapproval_or_repreparation_required_next)):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and any((artifact.transition_approval_record_issued, artifact.transition_approval_completed, artifact.transition_package_approved, artifact.transition_start_authorization_required_next, artifact.transition_reapproval_or_repreparation_required_next)):
        issues.append("rejected_record_issued")
    if any((artifact.lifecycle_transition_start_authorized, artifact.lifecycle_transition_started, artifact.lifecycle_transition_completed, artifact.lifecycle_transition_performed, artifact.lifecycle_state_changed, artifact.authority_changed, artifact.quiescence_state_changed, artifact.terminal_state_changed, artifact.terminal_marker_written, artifact.resource_removed, artifact.external_operation_performed, artifact.repository_changed)):
        issues.append("transition_or_repository_effect_performed")
    if not artifact.lifecycle_state_read_only or not artifact.repository_read_only:
        issues.append("read_only_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
