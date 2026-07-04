#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_transition_start_v0_22 import (
    STARTED as SOURCE_STARTED,
    artifact_issues as source_artifact_issues,
    all_source_digests as start_source_digests,
)

VERSION = "kuuos_lifecycle_bounded_transition_completion_review_v0_23"
APPROVED = "LIFECYCLE_BOUNDED_TRANSITION_COMPLETION_REVIEW_APPROVED_FOR_SEPARATE_TRANSITION_COMPLETION"
DENIED = "LIFECYCLE_BOUNDED_TRANSITION_COMPLETION_REVIEW_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_TRANSITION_COMPLETION_REVIEW_REJECTED"
OBJECTIVE = "REVIEW_STARTED_LIFECYCLE_TRANSITION_FOR_SEPARATE_COMPLETION_ONLY"
SOURCE_ORDER_CHECK = "source_transition_start_precedes_completion_review_and_deadline_valid"

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

def review_digest(value: Rec) -> str:
    return _digest(value, "review_digest")

def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")

def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))

def make_policy(policy_id: str, *, allowed_completion_reviewer_ids: tuple[str, ...], allowed_completion_reviewer_organization_ids: tuple[str, ...], max_review_delay_seconds: int = 900, max_evidence_age_seconds: int = 300, max_completion_delay_seconds: int = 900) -> Rec:
    value = Rec(policy_id=policy_id, allowed_completion_reviewer_ids=_canon(allowed_completion_reviewer_ids), allowed_completion_reviewer_organization_ids=_canon(allowed_completion_reviewer_organization_ids), max_review_delay_seconds=max_review_delay_seconds, max_evidence_age_seconds=max_evidence_age_seconds, max_completion_delay_seconds=max_completion_delay_seconds, started_source_required=True, source_recomputation_required=True, completion_review_route_required=True, reviewer_authority_required=True, reviewer_separation_required=True, separate_completion_required_next=True, lifecycle_state_read_only=True, repository_read_only=True, policy_digest="", version=VERSION)
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_completion_review_policy_invalid:" + issues[0])
    return value

def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_completion_reviewer_ids or not value.allowed_completion_reviewer_organization_ids:
        issues.append("allowed_reviewer_missing")
    if min(value.max_review_delay_seconds, value.max_evidence_age_seconds, value.max_completion_delay_seconds) <= 0:
        issues.append("bound_invalid")
    if not value.lifecycle_state_read_only or not value.repository_read_only:
        issues.append("read_only_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)

def all_source_digests(source_start, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = start_source_digests(source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:]))
    result.update(lifecycle_transition_start=source_start.start_digest, lifecycle_transition_start_evidence=source_evidence.evidence_digest, lifecycle_transition_start_policy=source_policy.policy_digest, lifecycle_transition_start_record=source_record.record_digest)
    return result

def source_recomputed_valid(source_start, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_start, source_evidence, source_policy, *source_args)

def expected_transition_completion_route_digest(source_start, source_record, *, completion_review_id: str, completion_reviewer_id: str, transition_package_digest: str, expected_current_lifecycle_state_digest: str, proposed_target_lifecycle_state_digest: str, transition_completion_deadline_at_epoch_seconds: int) -> str:
    return canonical_digest({"source_transition_start_id": source_start.transition_start_id, "source_transition_start_record_digest": source_record.record_digest, "source_completion_review_route_digest": source_start.transition_completion_review_route_digest, "completion_review_id": completion_review_id, "completion_reviewer_id": completion_reviewer_id, "transition_package_digest": transition_package_digest, "expected_current_lifecycle_state_digest": expected_current_lifecycle_state_digest, "proposed_target_lifecycle_state_digest": proposed_target_lifecycle_state_digest, "transition_completion_deadline_at_epoch_seconds": transition_completion_deadline_at_epoch_seconds})

def make_evidence(source_start, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(source_transition_start_id=source_start.transition_start_id, source_transition_start_record_digest=source_record.record_digest, source_artifact_digests=all_source_digests(source_start, source_evidence, source_policy, source_record, source_args), source_transition_start_authorization_id=source_start.source_transition_start_authorization_id, source_transition_start_authorizer_id=source_start.source_transition_start_authorizer_id, source_transition_operator_id=source_start.transition_operator_id, source_transition_operator_organization_id=source_start.transition_operator_organization_id, subject_id=source_start.subject_id, requester_id=source_start.requester_id, transition_package_digest=source_start.transition_package_digest, expected_current_lifecycle_state_digest=source_start.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_start.proposed_target_lifecycle_state_digest, source_completion_review_route_digest=source_start.transition_completion_review_route_digest, transition_completion_review_deadline_at_epoch_seconds=source_start.transition_completion_review_deadline_at_epoch_seconds, package_expiry_at_epoch_seconds=source_evidence.package_expiry_at_epoch_seconds)
    values.update(overrides)
    if "transition_completion_route_digest" not in values:
        values["transition_completion_route_digest"] = expected_transition_completion_route_digest(source_start, source_record, completion_review_id=values["completion_review_id"], completion_reviewer_id=values["completion_reviewer_id"], transition_package_digest=values["transition_package_digest"], expected_current_lifecycle_state_digest=values["expected_current_lifecycle_state_digest"], proposed_target_lifecycle_state_digest=values["proposed_target_lifecycle_state_digest"], transition_completion_deadline_at_epoch_seconds=values["transition_completion_deadline_at_epoch_seconds"])
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_completion_review_evidence_invalid:" + issues[0])
    return value

def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = ("evidence_id", "completion_review_id", "completion_reviewer_id", "completion_reviewer_organization_id", "reviewer_mandate_receipt_digest", "reviewer_authority_receipt_digest", "reviewer_identity_confirmation_digest", "source_transition_start_id", "source_transition_start_record_digest", "source_completion_review_route_digest", "transition_completion_route_digest", "transition_package_digest", "expected_current_lifecycle_state_digest", "proposed_target_lifecycle_state_digest", "start_record_freshness_receipt_digest", "completion_evidence_receipt_digest", "package_freshness_receipt_digest", "current_state_freshness_receipt_digest", "target_state_validity_receipt_digest")
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.review_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.reviewed_at_epoch_seconds, value.transition_completion_review_deadline_at_epoch_seconds, value.transition_completion_deadline_at_epoch_seconds, value.package_expiry_at_epoch_seconds) < 0:
        issues.append("negative_review_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)

def make_submission(completion_review_id: str, completion_reviewer_id: str, completion_reviewer_organization_id: str, review_requested_at_epoch_seconds: int, reviewed_at_epoch_seconds: int, source_start, source_record, review_evidence: Rec, *, transition_completion_route_digest: str, transition_completion_deadline_at_epoch_seconds: int, completion_review_approved: bool, denial_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(completion_review_id=completion_review_id, completion_reviewer_id=completion_reviewer_id, completion_reviewer_organization_id=completion_reviewer_organization_id, objective=objective, review_requested_at_epoch_seconds=review_requested_at_epoch_seconds, reviewed_at_epoch_seconds=reviewed_at_epoch_seconds, source_transition_start_id=source_start.transition_start_id, source_transition_start_record_digest=source_record.record_digest, subject_id=source_start.subject_id, requester_id=source_start.requester_id, source_transition_start_authorization_id=source_start.source_transition_start_authorization_id, source_transition_operator_id=source_start.transition_operator_id, transition_package_digest=source_start.transition_package_digest, expected_current_lifecycle_state_digest=source_start.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_start.proposed_target_lifecycle_state_digest, source_completion_review_route_digest=source_start.transition_completion_review_route_digest, transition_completion_route_digest=transition_completion_route_digest, transition_completion_deadline_at_epoch_seconds=transition_completion_deadline_at_epoch_seconds, review_evidence_digest=review_evidence.evidence_digest, completion_review_approved=completion_review_approved, denial_reason_digest=denial_reason_digest, review_digest="", version=VERSION)
    value.review_digest = review_digest(value)
    issues = submission_issues(value)
    if issues:
        raise ValueError("lifecycle_transition_completion_review_invalid:" + issues[0])
    return value

def submission_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("denial_reason_digest", "review_digest", "version", "completion_review_approved"):
            continue
        if content == "" or content is None:
            issues.append("required_review_field_missing")
            break
    if not value.completion_review_approved and not value.denial_reason_digest:
        issues.append("denial_reason_missing")
    if min(value.review_requested_at_epoch_seconds, value.reviewed_at_epoch_seconds, value.transition_completion_deadline_at_epoch_seconds) < 0:
        issues.append("negative_review_time")
    if value.review_digest != review_digest(value):
        issues.append("review_digest_mismatch")
    return tuple(issues)

def _source_ready(record) -> bool:
    return all((record.status == SOURCE_STARTED, record.transition_start_record_issued, record.transition_start_completed, record.lifecycle_transition_started, record.ready_for_separate_transition_completion_review, record.transition_completion_review_required_next, record.transition_completion_review_route_required_next, not record.lifecycle_transition_completed, not record.lifecycle_transition_performed, not record.external_operation_performed, not record.repository_changed, record.lifecycle_state_read_only, record.repository_read_only))

def _prior_actor_ids(source_start, source_evidence) -> set[str]:
    return {source_start.subject_id, source_start.requester_id, source_start.source_transition_start_authorizer_id, source_start.transition_operator_id, source_evidence.source_transition_start_authorization_id}

def evaluate(review: Rec, evidence: Rec, policy: Rec, source_start, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_start, source_evidence, source_policy, source_record, source_args)
    expected_completion_route = expected_transition_completion_route_digest(source_start, source_record, completion_review_id=review.completion_review_id, completion_reviewer_id=review.completion_reviewer_id, transition_package_digest=source_start.transition_package_digest, expected_current_lifecycle_state_digest=source_start.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=source_start.proposed_target_lifecycle_state_digest, transition_completion_deadline_at_epoch_seconds=review.transition_completion_deadline_at_epoch_seconds)
    prior = _prior_actor_ids(source_start, source_evidence)
    review_delay = evidence.reviewed_at_epoch_seconds - source_start.started_at_epoch_seconds
    evidence_age = evidence.reviewed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    completion_delay = evidence.transition_completion_deadline_at_epoch_seconds - evidence.reviewed_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "review_valid": not submission_issues(review),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_start, source_evidence, source_policy, source_record, source_args),
        "source_transition_start_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and review.source_transition_start_id == evidence.source_transition_start_id == source_start.transition_start_id and review.source_transition_start_record_digest == evidence.source_transition_start_record_digest == source_record.record_digest,
        "identity_binding_valid": review.completion_review_id == evidence.completion_review_id and review.completion_reviewer_id == evidence.completion_reviewer_id and review.completion_reviewer_organization_id == evidence.completion_reviewer_organization_id and review.review_evidence_digest == evidence.evidence_digest,
        "source_completion_review_route_binding_valid": review.source_completion_review_route_digest == evidence.source_completion_review_route_digest == source_start.transition_completion_review_route_digest,
        "transition_completion_route_binding_valid": review.transition_completion_route_digest == evidence.transition_completion_route_digest == expected_completion_route,
        "package_binding_valid": review.transition_package_digest == evidence.transition_package_digest == source_start.transition_package_digest,
        "state_binding_valid": review.expected_current_lifecycle_state_digest == evidence.expected_current_lifecycle_state_digest == source_start.expected_current_lifecycle_state_digest and review.proposed_target_lifecycle_state_digest == evidence.proposed_target_lifecycle_state_digest == source_start.proposed_target_lifecycle_state_digest,
        "reviewer_allowed": review.completion_reviewer_id in policy.allowed_completion_reviewer_ids,
        "reviewer_organization_allowed": review.completion_reviewer_organization_id in policy.allowed_completion_reviewer_organization_ids,
        "reviewer_separated_from_operator": review.completion_reviewer_id != source_start.transition_operator_id,
        "reviewer_separated_from_prior_actors": review.completion_reviewer_id not in prior,
        "reviewer_organization_separated": review.completion_reviewer_organization_id != source_start.transition_operator_organization_id,
        "objective_allowed": review.objective == OBJECTIVE,
        "review_delay_valid": 0 <= review_delay <= policy.max_review_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "completion_delay_valid": 0 < completion_delay <= policy.max_completion_delay_seconds,
        "time_order_valid": source_start.started_at_epoch_seconds <= evidence.review_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.reviewed_at_epoch_seconds < evidence.transition_completion_deadline_at_epoch_seconds <= evidence.package_expiry_at_epoch_seconds,
        "source_review_deadline_valid": evidence.reviewed_at_epoch_seconds <= source_start.transition_completion_review_deadline_at_epoch_seconds,
        "external_operation_absent": not evidence.external_operation_performed,
        "repository_change_absent": not evidence.repository_changed,
        "reviewer_mandate_verified": evidence.reviewer_mandate_verified,
        "reviewer_authority_verified": evidence.reviewer_authority_verified,
        "reviewer_identity_confirmed": evidence.reviewer_identity_confirmed,
        "start_record_fresh": evidence.start_record_fresh,
        "completion_evidence_valid": evidence.completion_evidence_valid,
        "package_fresh": evidence.package_fresh,
        "current_state_not_stale": evidence.current_state_not_stale,
        "target_state_still_valid": evidence.target_state_still_valid,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests

STRUCTURAL_CHECKS = ("policy_valid", "review_valid", "evidence_valid", "source_recomputed_valid", "source_transition_start_ready", "source_binding_valid", "identity_binding_valid", "source_completion_review_route_binding_valid", "transition_completion_route_binding_valid", "package_binding_valid", "state_binding_valid", "reviewer_allowed", "reviewer_organization_allowed", "reviewer_separated_from_operator", "reviewer_separated_from_prior_actors", "reviewer_organization_separated", "objective_allowed", "review_delay_valid", "evidence_fresh", "completion_delay_valid", "time_order_valid", "source_review_deadline_valid", "external_operation_absent", "repository_change_absent")
DENIAL_CHECKS = ("reviewer_mandate_verified", "reviewer_authority_verified", "reviewer_identity_confirmed", "start_record_fresh", "completion_evidence_valid", "package_fresh", "current_state_not_stale", "target_state_still_valid", "no_unresolved_anomaly", "recovery_not_in_progress", "institutional_hold_absent", "emergency_state_absent")

def compute_artifact(review: Rec, evidence: Rec, policy: Rec, source_start, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(review, evidence, policy, source_start, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_start.started_at_epoch_seconds <= review.review_requested_at_epoch_seconds <= review.reviewed_at_epoch_seconds <= source_start.transition_completion_review_deadline_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_start_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in DENIAL_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = DENIED, failed
        elif review.completion_review_approved:
            status, reason = APPROVED, "approved_for_separate_transition_completion_only"
        else:
            status, reason = DENIED, "completion_review_not_approved"
    issued = status != REJECTED
    approved = status == APPROVED
    denied = status == DENIED
    artifact = Rec(completion_review_id=review.completion_review_id, status=status, reason=reason, completion_reviewer_id=review.completion_reviewer_id, completion_reviewer_organization_id=review.completion_reviewer_organization_id, source_transition_start_id=review.source_transition_start_id, source_transition_start_record_digest=review.source_transition_start_record_digest, source_transition_operator_id=review.source_transition_operator_id, source_transition_start_authorization_id=review.source_transition_start_authorization_id, transition_package_digest=review.transition_package_digest, expected_current_lifecycle_state_digest=review.expected_current_lifecycle_state_digest, proposed_target_lifecycle_state_digest=review.proposed_target_lifecycle_state_digest, source_completion_review_route_digest=review.source_completion_review_route_digest, transition_completion_route_digest=review.transition_completion_route_digest, transition_completion_deadline_at_epoch_seconds=review.transition_completion_deadline_at_epoch_seconds, subject_id=review.subject_id, requester_id=review.requester_id, policy_digest=policy.policy_digest, review_digest=review.review_digest, evidence_digest=evidence.evidence_digest, checks=checks, evidence_digests=expected_digests, source_transition_start_ready=checks["source_transition_start_ready"], completion_review_record_issued=issued, completion_review_completed=issued, completion_review_approved=approved, completion_review_denied=denied, completion_review_rejected=status == REJECTED, ready_for_separate_transition_completion=approved, transition_completion_required_next=approved, transition_completion_route_required_next=approved, transition_completion_replan_required_next=denied, transition_completion_replan_route_required_next=denied, lifecycle_transition_completed=False, lifecycle_transition_performed=False, lifecycle_state_changed=False, authority_changed=False, quiescence_state_changed=False, terminal_state_changed=False, terminal_marker_written=False, resource_removed=False, external_operation_performed=False, repository_changed=False, lifecycle_state_read_only=True, repository_read_only=True, record_digest="", version=VERSION)
    artifact.record_digest = record_digest(artifact)
    return artifact

def verify_artifact(*args: Any, **kwargs: Any) -> Rec:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError("lifecycle_transition_completion_review_record_invalid:" + issues[0])
    return artifact

def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("completion_review_recomputation_mismatch")
    if artifact.status not in (APPROVED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == APPROVED and not all((artifact.completion_review_record_issued, artifact.completion_review_completed, artifact.completion_review_approved, artifact.ready_for_separate_transition_completion, artifact.transition_completion_required_next, artifact.transition_completion_route_required_next, not artifact.lifecycle_transition_completed, not artifact.lifecycle_transition_performed)):
        issues.append("approved_gate_invalid")
    if artifact.status == DENIED and not all((artifact.completion_review_record_issued, artifact.completion_review_completed, artifact.completion_review_denied, not artifact.ready_for_separate_transition_completion, not artifact.transition_completion_required_next, artifact.transition_completion_replan_required_next)):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and any((artifact.completion_review_record_issued, artifact.completion_review_completed, artifact.completion_review_approved, artifact.transition_completion_required_next, artifact.transition_completion_replan_required_next)):
        issues.append("rejected_record_issued")
    if any((artifact.lifecycle_transition_completed, artifact.lifecycle_transition_performed, artifact.lifecycle_state_changed, artifact.authority_changed, artifact.quiescence_state_changed, artifact.terminal_state_changed, artifact.terminal_marker_written, artifact.resource_removed, artifact.external_operation_performed, artifact.repository_changed)):
        issues.append("completion_or_repository_effect_performed")
    if not artifact.lifecycle_state_read_only or not artifact.repository_read_only:
        issues.append("read_only_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
