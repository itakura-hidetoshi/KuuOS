#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_transition_completion_review_v0_23 import (
    APPROVED as SOURCE_APPROVED,
    artifact_issues as source_artifact_issues,
    all_source_digests as review_source_digests,
)

VERSION = "kuuos_lifecycle_bounded_transition_completion_v0_24"
COMPLETED = "LIFECYCLE_BOUNDED_TRANSITION_COMPLETION_COMPLETED_FOR_SEPARATE_LIFECYCLE_STATE_ADOPTION"
DENIED = "LIFECYCLE_BOUNDED_TRANSITION_COMPLETION_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_TRANSITION_COMPLETION_REJECTED"
OBJECTIVE = "COMPLETE_REVIEWED_LIFECYCLE_TRANSITION_FOR_SEPARATE_STATE_ADOPTION_ONLY"
SOURCE_ORDER_CHECK = "source_completion_review_precedes_transition_completion_and_deadline_valid"

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

def completion_digest(value: Rec) -> str:
    return _digest(value, "completion_digest")

def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")

def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))

def make_policy(policy_id: str, *, allowed_completion_operator_ids: tuple[str, ...], allowed_completion_operator_organization_ids: tuple[str, ...], max_completion_delay_seconds: int = 900, max_evidence_age_seconds: int = 300, max_state_adoption_delay_seconds: int = 900) -> Rec:
    value = Rec(policy_id=policy_id, allowed_completion_operator_ids=_canon(allowed_completion_operator_ids), allowed_completion_operator_organization_ids=_canon(allowed_completion_operator_organization_ids), max_completion_delay_seconds=max_completion_delay_seconds, max_evidence_age_seconds=max_evidence_age_seconds, max_state_adoption_delay_seconds=max_state_adoption_delay_seconds, approved_source_required=True, source_recomputation_required=True, transition_completion_route_required=True, completion_operator_authority_required=True, completion_operator_separation_required=True, state_adoption_route_required_next=True, lifecycle_state_read_only=True, repository_read_only=True, policy_digest="", version=VERSION)
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_completion_policy_invalid:" + issues[0])
    return value

def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_completion_operator_ids or not value.allowed_completion_operator_organization_ids:
        issues.append("allowed_completion_operator_missing")
    if min(value.max_completion_delay_seconds, value.max_evidence_age_seconds, value.max_state_adoption_delay_seconds) <= 0:
        issues.append("bound_invalid")
    if not value.lifecycle_state_read_only or not value.repository_read_only:
        issues.append("read_only_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)

def all_source_digests(source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = review_source_digests(source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:]))
    result.update(lifecycle_transition_completion_review=source_review.review_digest, lifecycle_transition_completion_review_evidence=source_evidence.evidence_digest, lifecycle_transition_completion_review_policy=source_policy.policy_digest, lifecycle_transition_completion_review_record=source_record.record_digest)
    return result

def source_recomputed_valid(source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_review, source_evidence, source_policy, *source_args)

def expected_state_adoption_route_digest(source_review, source_record, *, transition_completion_id: str, completion_operator_id: str, transition_package_digest: str, expected_current_lifecycle_state_digest: str, proposed_target_lifecycle_state_digest: str, lifecycle_state_adoption_deadline_at_epoch_seconds: int) -> str:
    return canonical_digest({"source_completion_review_id": source_review.completion_review_id, "source_completion_review_record_digest": source_record.record_digest, "source_transition_completion_route_digest": source_review.transition_completion_route_digest, "transition_completion_id": transition_completion_id, "completion_operator_id": completion_operator_id, "transition_package_digest": transition_package_digest, "expected_current_lifecycle_state_digest": expected_current_lifecycle_state_digest, "proposed_target_lifecycle_state_digest": proposed_target_lifecycle_state_digest, "lifecycle_state_adoption_deadline_at_epoch_seconds": lifecycle_state_adoption_deadline_at_epoch_seconds})

def make_evidence(source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(source_completion_review_id=source_review.completion_review_id, source_completion_review_record_digest=source_record.record_digest, source_artifact_digests=all_source_digests(source_review, source_evidence, source_policy, source_record, source_args), source_transition_start_id=source_review.source_transition_start_id, source_transition_start_authorization_id=source_review.source_transition_start_authorization_id, source_transition_operator_id=source_review.source_transition_operator_id, source_completion_reviewer_id=source_review.completion_reviewer_id, source_completion_reviewer_organization_id=source_review.completion_reviewer_organization_id, subject_id=source_review.subject_id, requester_id=source_review.requester_id, completion_operator_id=source_review.source_transition_operator_id, transition_package_digest=source_review.transition_package_digest, expected_current_lifecycle_state_digest=source_review.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_review.proposed_target_lifecycle_state_digest, source_transition_completion_route_digest=source_review.transition_completion_route_digest, transition_completion_deadline_at_epoch_seconds=source_review.transition_completion_deadline_at_epoch_seconds, package_expiry_at_epoch_seconds=source_evidence.package_expiry_at_epoch_seconds)
    values.update(overrides)
    if "lifecycle_state_adoption_route_digest" not in values:
        values["lifecycle_state_adoption_route_digest"] = expected_state_adoption_route_digest(source_review, source_record, transition_completion_id=values["transition_completion_id"], completion_operator_id=values["completion_operator_id"], transition_package_digest=values["transition_package_digest"], expected_current_lifecycle_state_digest=values["expected_current_lifecycle_state_digest"], proposed_target_lifecycle_state_digest=values["proposed_target_lifecycle_state_digest"], lifecycle_state_adoption_deadline_at_epoch_seconds=values["lifecycle_state_adoption_deadline_at_epoch_seconds"])
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_completion_evidence_invalid:" + issues[0])
    return value

def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = ("evidence_id", "transition_completion_id", "completion_operator_id", "completion_operator_organization_id", "completion_operator_mandate_receipt_digest", "completion_operator_authority_receipt_digest", "completion_operator_identity_confirmation_digest", "source_completion_review_id", "source_completion_review_record_digest", "source_transition_completion_route_digest", "lifecycle_state_adoption_route_digest", "transition_package_digest", "expected_current_lifecycle_state_digest", "proposed_target_lifecycle_state_digest", "completion_review_freshness_receipt_digest", "completion_receipt_digest", "package_freshness_receipt_digest", "current_state_freshness_receipt_digest", "target_state_validity_receipt_digest")
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.completion_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.completed_at_epoch_seconds, value.transition_completion_deadline_at_epoch_seconds, value.lifecycle_state_adoption_deadline_at_epoch_seconds, value.package_expiry_at_epoch_seconds) < 0:
        issues.append("negative_completion_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)

def make_submission(transition_completion_id: str, completion_operator_id: str, completion_operator_organization_id: str, completion_requested_at_epoch_seconds: int, completed_at_epoch_seconds: int, source_review, source_record, completion_evidence: Rec, *, lifecycle_state_adoption_route_digest: str, lifecycle_state_adoption_deadline_at_epoch_seconds: int, transition_completion_confirmed: bool, denial_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(transition_completion_id=transition_completion_id, completion_operator_id=completion_operator_id, completion_operator_organization_id=completion_operator_organization_id, objective=objective, completion_requested_at_epoch_seconds=completion_requested_at_epoch_seconds, completed_at_epoch_seconds=completed_at_epoch_seconds, source_completion_review_id=source_review.completion_review_id, source_completion_review_record_digest=source_record.record_digest, subject_id=source_review.subject_id, requester_id=source_review.requester_id, source_transition_start_id=source_review.source_transition_start_id, source_transition_start_authorization_id=source_review.source_transition_start_authorization_id, source_completion_reviewer_id=source_review.completion_reviewer_id, transition_package_digest=source_review.transition_package_digest, expected_current_lifecycle_state_digest=source_review.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_review.proposed_target_lifecycle_state_digest, source_transition_completion_route_digest=source_review.transition_completion_route_digest, lifecycle_state_adoption_route_digest=lifecycle_state_adoption_route_digest, lifecycle_state_adoption_deadline_at_epoch_seconds=lifecycle_state_adoption_deadline_at_epoch_seconds, completion_evidence_digest=completion_evidence.evidence_digest, transition_completion_confirmed=transition_completion_confirmed, denial_reason_digest=denial_reason_digest, completion_digest="", version=VERSION)
    value.completion_digest = completion_digest(value)
    issues = submission_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_completion_invalid:" + issues[0])
    return value

def submission_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("denial_reason_digest", "completion_digest", "version", "transition_completion_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_completion_field_missing")
            break
    if not value.transition_completion_confirmed and not value.denial_reason_digest:
        issues.append("denial_reason_missing")
    if min(value.completion_requested_at_epoch_seconds, value.completed_at_epoch_seconds, value.lifecycle_state_adoption_deadline_at_epoch_seconds) < 0:
        issues.append("negative_completion_time")
    if value.completion_digest != completion_digest(value):
        issues.append("completion_digest_mismatch")
    return tuple(issues)

def _source_ready(record) -> bool:
    return all((record.status == SOURCE_APPROVED, record.completion_review_record_issued, record.completion_review_completed, record.completion_review_approved, record.ready_for_separate_transition_completion, record.transition_completion_required_next, record.transition_completion_route_required_next, not record.lifecycle_transition_completed, not record.lifecycle_transition_performed, not record.external_operation_performed, not record.repository_changed, record.lifecycle_state_read_only, record.repository_read_only))

def _prior_actor_ids(source_review, source_evidence) -> set[str]:
    return {source_review.subject_id, source_review.requester_id, source_review.source_transition_operator_id, source_review.completion_reviewer_id, source_evidence.source_transition_start_id}

def evaluate(completion: Rec, evidence: Rec, policy: Rec, source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_review, source_evidence, source_policy, source_record, source_args)
    expected_adoption_route = expected_state_adoption_route_digest(source_review, source_record, transition_completion_id=completion.transition_completion_id, completion_operator_id=completion.completion_operator_id, transition_package_digest=source_review.transition_package_digest, expected_current_lifecycle_state_digest=source_review.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_review.proposed_target_lifecycle_state_digest, lifecycle_state_adoption_deadline_at_epoch_seconds=completion.lifecycle_state_adoption_deadline_at_epoch_seconds)
    prior = _prior_actor_ids(source_review, source_evidence)
    completion_delay = evidence.completed_at_epoch_seconds - source_review.reviewed_at_epoch_seconds
    evidence_age = evidence.completed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    adoption_delay = evidence.lifecycle_state_adoption_deadline_at_epoch_seconds - evidence.completed_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "completion_valid": not submission_issues(completion),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_review, source_evidence, source_policy, source_record, source_args),
        "source_completion_review_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and completion.source_completion_review_id == evidence.source_completion_review_id == source_review.completion_review_id and completion.source_completion_review_record_digest == evidence.source_completion_review_record_digest == source_record.record_digest,
        "identity_binding_valid": completion.transition_completion_id == evidence.transition_completion_id and completion.completion_operator_id == evidence.completion_operator_id and completion.completion_operator_organization_id == evidence.completion_operator_organization_id and completion.completion_evidence_digest == evidence.evidence_digest,
        "source_completion_route_binding_valid": completion.source_transition_completion_route_digest == evidence.source_transition_completion_route_digest == source_review.transition_completion_route_digest,
        "state_adoption_route_binding_valid": completion.lifecycle_state_adoption_route_digest == evidence.lifecycle_state_adoption_route_digest == expected_adoption_route,
        "package_binding_valid": completion.transition_package_digest == evidence.transition_package_digest == source_review.transition_package_digest,
        "state_binding_valid": completion.expected_current_lifecycle_state_digest == evidence.expected_current_lifecycle_state_digest == source_review.expected_current_lifecycle_state_digest and completion.proposed_target_lifecycle_state_digest == evidence.proposed_target_lifecycle_state_digest == source_review.proposed_target_lifecycle_state_digest,
        "completion_operator_bound": completion.completion_operator_id == evidence.completion_operator_id == source_review.source_transition_operator_id,
        "completion_operator_allowed": completion.completion_operator_id in policy.allowed_completion_operator_ids,
        "completion_operator_organization_allowed": completion.completion_operator_organization_id in policy.allowed_completion_operator_organization_ids,
        "completion_operator_separated_from_reviewer": completion.completion_operator_id != source_review.completion_reviewer_id,
        "completion_operator_separated_from_prior_actors": completion.completion_operator_id not in prior,
        "completion_operator_organization_separated": completion.completion_operator_organization_id != source_review.completion_reviewer_organization_id,
        "objective_allowed": completion.objective == OBJECTIVE,
        "completion_delay_valid": 0 <= completion_delay <= policy.max_completion_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "state_adoption_delay_valid": 0 < adoption_delay <= policy.max_state_adoption_delay_seconds,
        "time_order_valid": source_review.reviewed_at_epoch_seconds <= evidence.completion_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.completed_at_epoch_seconds < evidence.lifecycle_state_adoption_deadline_at_epoch_seconds <= evidence.package_expiry_at_epoch_seconds,
        "source_completion_deadline_valid": evidence.completed_at_epoch_seconds <= source_review.transition_completion_deadline_at_epoch_seconds,
        "external_operation_absent": not evidence.external_operation_performed,
        "repository_change_absent": not evidence.repository_changed,
        "completion_operator_mandate_verified": evidence.completion_operator_mandate_verified,
        "completion_operator_authority_verified": evidence.completion_operator_authority_verified,
        "completion_operator_identity_confirmed": evidence.completion_operator_identity_confirmed,
        "completion_review_fresh": evidence.completion_review_fresh,
        "completion_receipt_valid": evidence.completion_receipt_valid,
        "package_fresh": evidence.package_fresh,
        "current_state_not_stale": evidence.current_state_not_stale,
        "target_state_still_valid": evidence.target_state_still_valid,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests

STRUCTURAL_CHECKS = ("policy_valid", "completion_valid", "evidence_valid", "source_recomputed_valid", "source_completion_review_ready", "source_binding_valid", "identity_binding_valid", "source_completion_route_binding_valid", "state_adoption_route_binding_valid", "package_binding_valid", "state_binding_valid", "completion_operator_bound", "completion_operator_allowed", "completion_operator_organization_allowed", "completion_operator_separated_from_reviewer", "completion_operator_separated_from_prior_actors", "completion_operator_organization_separated", "objective_allowed", "completion_delay_valid", "evidence_fresh", "state_adoption_delay_valid", "time_order_valid", "source_completion_deadline_valid", "external_operation_absent", "repository_change_absent")
DENIAL_CHECKS = ("completion_operator_mandate_verified", "completion_operator_authority_verified", "completion_operator_identity_confirmed", "completion_review_fresh", "completion_receipt_valid", "package_fresh", "current_state_not_stale", "target_state_still_valid", "no_unresolved_anomaly", "recovery_not_in_progress", "institutional_hold_absent", "emergency_state_absent")

def compute_artifact(completion: Rec, evidence: Rec, policy: Rec, source_review, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(completion, evidence, policy, source_review, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_review.reviewed_at_epoch_seconds <= completion.completion_requested_at_epoch_seconds <= completion.completed_at_epoch_seconds <= source_review.transition_completion_deadline_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_review_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in DENIAL_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = DENIED, failed
        elif completion.transition_completion_confirmed:
            status, reason = COMPLETED, "completed_for_separate_lifecycle_state_adoption_only"
        else:
            status, reason = DENIED, "transition_completion_not_confirmed"
    issued = status != REJECTED
    completed = status == COMPLETED
    denied = status == DENIED
    artifact = Rec(transition_completion_id=completion.transition_completion_id, status=status, reason=reason, completion_operator_id=completion.completion_operator_id, completion_operator_organization_id=completion.completion_operator_organization_id, source_completion_review_id=completion.source_completion_review_id, source_completion_review_record_digest=completion.source_completion_review_record_digest, source_completion_reviewer_id=completion.source_completion_reviewer_id, source_transition_start_id=completion.source_transition_start_id, source_transition_start_authorization_id=completion.source_transition_start_authorization_id, transition_package_digest=completion.transition_package_digest, expected_current_lifecycle_state_digest=completion.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=completion.proposed_target_lifecycle_state_digest, source_transition_completion_route_digest=completion.source_transition_completion_route_digest, lifecycle_state_adoption_route_digest=completion.lifecycle_state_adoption_route_digest, lifecycle_state_adoption_deadline_at_epoch_seconds=completion.lifecycle_state_adoption_deadline_at_epoch_seconds, subject_id=completion.subject_id, requester_id=completion.requester_id, policy_digest=policy.policy_digest, completion_digest=completion.completion_digest, evidence_digest=evidence.evidence_digest, checks=checks, evidence_digests=expected_digests, source_completion_review_ready=checks["source_completion_review_ready"], transition_completion_record_issued=issued, transition_completion_completed=issued, lifecycle_transition_completed=completed, transition_completion_denied=denied, transition_completion_rejected=status == REJECTED, ready_for_separate_lifecycle_state_adoption=completed, lifecycle_state_adoption_required_next=completed, lifecycle_state_adoption_route_required_next=completed, transition_recompletion_or_replan_required_next=denied, transition_recompletion_or_replan_route_required_next=denied, lifecycle_transition_performed=False, lifecycle_state_changed=False, authority_changed=False, quiescence_state_changed=False, terminal_state_changed=False, terminal_marker_written=False, resource_removed=False, external_operation_performed=False, repository_changed=False, lifecycle_state_read_only=True, repository_read_only=True, record_digest="", version=VERSION)
    artifact.record_digest = record_digest(artifact)
    return artifact

def verify_artifact(*args: Any, **kwargs: Any) -> Rec:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError("lifecycle_transition_completion_record_invalid:" + issues[0])
    return artifact

def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("transition_completion_recomputation_mismatch")
    if artifact.status not in (COMPLETED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == COMPLETED and not all((artifact.transition_completion_record_issued, artifact.transition_completion_completed, artifact.lifecycle_transition_completed, artifact.ready_for_separate_lifecycle_state_adoption, artifact.lifecycle_state_adoption_required_next, artifact.lifecycle_state_adoption_route_required_next, not artifact.lifecycle_transition_performed, not artifact.lifecycle_state_changed)):
        issues.append("completed_gate_invalid")
    if artifact.status == DENIED and not all((artifact.transition_completion_record_issued, artifact.transition_completion_completed, artifact.transition_completion_denied, not artifact.lifecycle_transition_completed, not artifact.lifecycle_state_adoption_required_next, artifact.transition_recompletion_or_replan_required_next)):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and any((artifact.transition_completion_record_issued, artifact.transition_completion_completed, artifact.lifecycle_transition_completed, artifact.lifecycle_state_adoption_required_next, artifact.transition_recompletion_or_replan_required_next)):
        issues.append("rejected_record_issued")
    if any((artifact.lifecycle_transition_performed, artifact.lifecycle_state_changed, artifact.authority_changed, artifact.quiescence_state_changed, artifact.terminal_state_changed, artifact.terminal_marker_written, artifact.resource_removed, artifact.external_operation_performed, artifact.repository_changed)):
        issues.append("state_or_repository_effect_performed")
    if not artifact.lifecycle_state_read_only or not artifact.repository_read_only:
        issues.append("read_only_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
