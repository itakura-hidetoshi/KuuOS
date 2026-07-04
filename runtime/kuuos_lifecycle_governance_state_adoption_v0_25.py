#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_transition_completion_v0_24 import (
    COMPLETED as SOURCE_COMPLETED,
    artifact_issues as source_artifact_issues,
    all_source_digests as completion_source_digests,
)

VERSION = "kuuos_lifecycle_bounded_state_adoption_v0_25"
ADOPTED = "LIFECYCLE_BOUNDED_STATE_ADOPTION_ADOPTED_FOR_SEPARATE_REPOSITORY_MUTATION_REVIEW"
DENIED = "LIFECYCLE_BOUNDED_STATE_ADOPTION_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_STATE_ADOPTION_REJECTED"
OBJECTIVE = "ADOPT_COMPLETED_LIFECYCLE_STATE_FOR_SEPARATE_REPOSITORY_REVIEW_ONLY"
SOURCE_ORDER_CHECK = "source_transition_completion_precedes_state_adoption_and_deadline_valid"

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

def adoption_digest(value: Rec) -> str:
    return _digest(value, "adoption_digest")

def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")

def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))

def make_policy(policy_id: str, *, allowed_state_adopter_ids: tuple[str, ...], allowed_state_adopter_organization_ids: tuple[str, ...], max_adoption_delay_seconds: int = 900, max_evidence_age_seconds: int = 300, max_repository_review_delay_seconds: int = 900) -> Rec:
    value = Rec(policy_id=policy_id, allowed_state_adopter_ids=_canon(allowed_state_adopter_ids), allowed_state_adopter_organization_ids=_canon(allowed_state_adopter_organization_ids), max_adoption_delay_seconds=max_adoption_delay_seconds, max_evidence_age_seconds=max_evidence_age_seconds, max_repository_review_delay_seconds=max_repository_review_delay_seconds, completed_source_required=True, source_recomputation_required=True, state_adoption_route_required=True, adopter_authority_required=True, adopter_separation_required=True, repository_review_route_required_next=True, repository_read_only=True, external_operation_absent_required=True, policy_digest="", version=VERSION)
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_state_adoption_policy_invalid:" + issues[0])
    return value

def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_state_adopter_ids or not value.allowed_state_adopter_organization_ids:
        issues.append("allowed_state_adopter_missing")
    if min(value.max_adoption_delay_seconds, value.max_evidence_age_seconds, value.max_repository_review_delay_seconds) <= 0:
        issues.append("bound_invalid")
    if not value.repository_read_only or not value.external_operation_absent_required:
        issues.append("repository_or_external_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)

def all_source_digests(source_completion, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = completion_source_digests(source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:]))
    result.update(lifecycle_transition_completion=source_completion.completion_digest, lifecycle_transition_completion_evidence=source_evidence.evidence_digest, lifecycle_transition_completion_policy=source_policy.policy_digest, lifecycle_transition_completion_record=source_record.record_digest)
    return result

def source_recomputed_valid(source_completion, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_completion, source_evidence, source_policy, *source_args)

def expected_repository_review_route_digest(source_completion, source_record, *, state_adoption_id: str, state_adopter_id: str, adopted_lifecycle_state_digest: str, repository_review_deadline_at_epoch_seconds: int) -> str:
    return canonical_digest({"source_transition_completion_id": source_completion.transition_completion_id, "source_transition_completion_record_digest": source_record.record_digest, "source_state_adoption_route_digest": source_completion.lifecycle_state_adoption_route_digest, "state_adoption_id": state_adoption_id, "state_adopter_id": state_adopter_id, "adopted_lifecycle_state_digest": adopted_lifecycle_state_digest, "repository_review_deadline_at_epoch_seconds": repository_review_deadline_at_epoch_seconds})

def make_evidence(source_completion, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **overrides: Any) -> Rec:
    values = dict(source_transition_completion_id=source_completion.transition_completion_id, source_transition_completion_record_digest=source_record.record_digest, source_artifact_digests=all_source_digests(source_completion, source_evidence, source_policy, source_record, source_args), source_completion_operator_id=source_completion.completion_operator_id, source_completion_operator_organization_id=source_completion.completion_operator_organization_id, subject_id=source_completion.subject_id, requester_id=source_completion.requester_id, transition_package_digest=source_completion.transition_package_digest, previous_lifecycle_state_digest=source_completion.expected_current_lifecycle_state_digest, adopted_lifecycle_state_digest=source_completion.proposed_target_lifecycle_state_digest, source_state_adoption_route_digest=source_completion.lifecycle_state_adoption_route_digest, lifecycle_state_adoption_deadline_at_epoch_seconds=source_completion.lifecycle_state_adoption_deadline_at_epoch_seconds, package_expiry_at_epoch_seconds=source_evidence.package_expiry_at_epoch_seconds)
    values.update(overrides)
    if "repository_review_route_digest" not in values:
        values["repository_review_route_digest"] = expected_repository_review_route_digest(source_completion, source_record, state_adoption_id=values["state_adoption_id"], state_adopter_id=values["state_adopter_id"], adopted_lifecycle_state_digest=values["adopted_lifecycle_state_digest"], repository_review_deadline_at_epoch_seconds=values["repository_review_deadline_at_epoch_seconds"])
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_state_adoption_evidence_invalid:" + issues[0])
    return value

def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = ("evidence_id", "state_adoption_id", "state_adopter_id", "state_adopter_organization_id", "state_adopter_mandate_receipt_digest", "state_adopter_authority_receipt_digest", "state_adopter_identity_confirmation_digest", "source_transition_completion_id", "source_transition_completion_record_digest", "source_state_adoption_route_digest", "repository_review_route_digest", "transition_package_digest", "previous_lifecycle_state_digest", "adopted_lifecycle_state_digest", "completion_record_freshness_receipt_digest", "state_adoption_receipt_digest", "package_freshness_receipt_digest", "previous_state_freshness_receipt_digest", "target_state_validity_receipt_digest")
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if min(value.adoption_requested_at_epoch_seconds, value.captured_at_epoch_seconds, value.adopted_at_epoch_seconds, value.lifecycle_state_adoption_deadline_at_epoch_seconds, value.repository_review_deadline_at_epoch_seconds, value.package_expiry_at_epoch_seconds) < 0:
        issues.append("negative_adoption_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)

def make_submission(state_adoption_id: str, state_adopter_id: str, state_adopter_organization_id: str, adoption_requested_at_epoch_seconds: int, adopted_at_epoch_seconds: int, source_completion, source_record, adoption_evidence: Rec, *, repository_review_route_digest: str, repository_review_deadline_at_epoch_seconds: int, state_adoption_confirmed: bool, denial_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    value = Rec(state_adoption_id=state_adoption_id, state_adopter_id=state_adopter_id, state_adopter_organization_id=state_adopter_organization_id, objective=objective, adoption_requested_at_epoch_seconds=adoption_requested_at_epoch_seconds, adopted_at_epoch_seconds=adopted_at_epoch_seconds, source_transition_completion_id=source_completion.transition_completion_id, source_transition_completion_record_digest=source_record.record_digest, subject_id=source_completion.subject_id, requester_id=source_completion.requester_id, source_completion_operator_id=source_completion.completion_operator_id, transition_package_digest=source_completion.transition_package_digest, previous_lifecycle_state_digest=source_completion.expected_current_lifecycle_state_digest, adopted_lifecycle_state_digest=source_completion.proposed_target_lifecycle_state_digest, source_state_adoption_route_digest=source_completion.lifecycle_state_adoption_route_digest, repository_review_route_digest=repository_review_route_digest, repository_review_deadline_at_epoch_seconds=repository_review_deadline_at_epoch_seconds, adoption_evidence_digest=adoption_evidence.evidence_digest, state_adoption_confirmed=state_adoption_confirmed, denial_reason_digest=denial_reason_digest, adoption_digest="", version=VERSION)
    value.adoption_digest = adoption_digest(value)
    issues = submission_issues(value)
    if issues:
        raise ValueError("lifecycle_state_adoption_invalid:" + issues[0])
    return value

def submission_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("denial_reason_digest", "adoption_digest", "version", "state_adoption_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_adoption_field_missing")
            break
    if value.previous_lifecycle_state_digest == value.adopted_lifecycle_state_digest:
        issues.append("state_digest_unchanged")
    if not value.state_adoption_confirmed and not value.denial_reason_digest:
        issues.append("denial_reason_missing")
    if min(value.adoption_requested_at_epoch_seconds, value.adopted_at_epoch_seconds, value.repository_review_deadline_at_epoch_seconds) < 0:
        issues.append("negative_adoption_time")
    if value.adoption_digest != adoption_digest(value):
        issues.append("adoption_digest_mismatch")
    return tuple(issues)

def _source_ready(record) -> bool:
    return all((record.status == SOURCE_COMPLETED, record.transition_completion_record_issued, record.transition_completion_completed, record.lifecycle_transition_completed, record.ready_for_separate_lifecycle_state_adoption, record.lifecycle_state_adoption_required_next, record.lifecycle_state_adoption_route_required_next, not record.lifecycle_transition_performed, not record.lifecycle_state_changed, not record.external_operation_performed, not record.repository_changed, record.lifecycle_state_read_only, record.repository_read_only))

def _prior_actor_ids(source_completion, source_evidence) -> set[str]:
    return {source_completion.subject_id, source_completion.requester_id, source_completion.completion_operator_id, source_evidence.source_completion_review_id}

def evaluate(adoption: Rec, evidence: Rec, policy: Rec, source_completion, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_completion, source_evidence, source_policy, source_record, source_args)
    expected_repository_route = expected_repository_review_route_digest(source_completion, source_record, state_adoption_id=adoption.state_adoption_id, state_adopter_id=adoption.state_adopter_id, adopted_lifecycle_state_digest=source_completion.proposed_target_lifecycle_state_digest, repository_review_deadline_at_epoch_seconds=adoption.repository_review_deadline_at_epoch_seconds)
    prior = _prior_actor_ids(source_completion, source_evidence)
    adoption_delay = evidence.adopted_at_epoch_seconds - source_completion.completed_at_epoch_seconds
    evidence_age = evidence.adopted_at_epoch_seconds - evidence.captured_at_epoch_seconds
    repository_delay = evidence.repository_review_deadline_at_epoch_seconds - evidence.adopted_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy),
        "adoption_valid": not submission_issues(adoption),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(source_completion, source_evidence, source_policy, source_record, source_args),
        "source_transition_completion_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and adoption.source_transition_completion_id == evidence.source_transition_completion_id == source_completion.transition_completion_id and adoption.source_transition_completion_record_digest == evidence.source_transition_completion_record_digest == source_record.record_digest,
        "identity_binding_valid": adoption.state_adoption_id == evidence.state_adoption_id and adoption.state_adopter_id == evidence.state_adopter_id and adoption.state_adopter_organization_id == evidence.state_adopter_organization_id and adoption.adoption_evidence_digest == evidence.evidence_digest,
        "source_state_adoption_route_binding_valid": adoption.source_state_adoption_route_digest == evidence.source_state_adoption_route_digest == source_completion.lifecycle_state_adoption_route_digest,
        "repository_review_route_binding_valid": adoption.repository_review_route_digest == evidence.repository_review_route_digest == expected_repository_route,
        "package_binding_valid": adoption.transition_package_digest == evidence.transition_package_digest == source_completion.transition_package_digest,
        "state_binding_valid": adoption.previous_lifecycle_state_digest == evidence.previous_lifecycle_state_digest == source_completion.expected_current_lifecycle_state_digest and adoption.adopted_lifecycle_state_digest == evidence.adopted_lifecycle_state_digest == source_completion.proposed_target_lifecycle_state_digest,
        "state_changed": adoption.previous_lifecycle_state_digest != adoption.adopted_lifecycle_state_digest,
        "state_adopter_allowed": adoption.state_adopter_id in policy.allowed_state_adopter_ids,
        "state_adopter_organization_allowed": adoption.state_adopter_organization_id in policy.allowed_state_adopter_organization_ids,
        "state_adopter_separated_from_completion_operator": adoption.state_adopter_id != source_completion.completion_operator_id,
        "state_adopter_separated_from_prior_actors": adoption.state_adopter_id not in prior,
        "state_adopter_organization_separated": adoption.state_adopter_organization_id != source_completion.completion_operator_organization_id,
        "objective_allowed": adoption.objective == OBJECTIVE,
        "adoption_delay_valid": 0 <= adoption_delay <= policy.max_adoption_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "repository_review_delay_valid": 0 < repository_delay <= policy.max_repository_review_delay_seconds,
        "time_order_valid": source_completion.completed_at_epoch_seconds <= evidence.adoption_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.adopted_at_epoch_seconds < evidence.repository_review_deadline_at_epoch_seconds <= evidence.package_expiry_at_epoch_seconds,
        "source_adoption_deadline_valid": evidence.adopted_at_epoch_seconds <= source_completion.lifecycle_state_adoption_deadline_at_epoch_seconds,
        "external_operation_absent": not evidence.external_operation_performed,
        "repository_change_absent": not evidence.repository_changed,
        "state_adopter_mandate_verified": evidence.state_adopter_mandate_verified,
        "state_adopter_authority_verified": evidence.state_adopter_authority_verified,
        "state_adopter_identity_confirmed": evidence.state_adopter_identity_confirmed,
        "completion_record_fresh": evidence.completion_record_fresh,
        "state_adoption_receipt_valid": evidence.state_adoption_receipt_valid,
        "package_fresh": evidence.package_fresh,
        "previous_state_not_stale": evidence.previous_state_not_stale,
        "target_state_still_valid": evidence.target_state_still_valid,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests

STRUCTURAL_CHECKS = ("policy_valid", "adoption_valid", "evidence_valid", "source_recomputed_valid", "source_transition_completion_ready", "source_binding_valid", "identity_binding_valid", "source_state_adoption_route_binding_valid", "repository_review_route_binding_valid", "package_binding_valid", "state_binding_valid", "state_changed", "state_adopter_allowed", "state_adopter_organization_allowed", "state_adopter_separated_from_completion_operator", "state_adopter_separated_from_prior_actors", "state_adopter_organization_separated", "objective_allowed", "adoption_delay_valid", "evidence_fresh", "repository_review_delay_valid", "time_order_valid", "source_adoption_deadline_valid", "external_operation_absent", "repository_change_absent")
DENIAL_CHECKS = ("state_adopter_mandate_verified", "state_adopter_authority_verified", "state_adopter_identity_confirmed", "completion_record_fresh", "state_adoption_receipt_valid", "package_fresh", "previous_state_not_stale", "target_state_still_valid", "no_unresolved_anomaly", "recovery_not_in_progress", "institutional_hold_absent", "emergency_state_absent")

def compute_artifact(adoption: Rec, evidence: Rec, policy: Rec, source_completion, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(adoption, evidence, policy, source_completion, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_completion.completed_at_epoch_seconds <= adoption.adoption_requested_at_epoch_seconds <= adoption.adopted_at_epoch_seconds <= source_completion.lifecycle_state_adoption_deadline_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_completion_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in DENIAL_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = DENIED, failed
        elif adoption.state_adoption_confirmed:
            status, reason = ADOPTED, "adopted_for_separate_repository_mutation_review_only"
        else:
            status, reason = DENIED, "state_adoption_not_confirmed"
    issued = status != REJECTED
    adopted = status == ADOPTED
    denied = status == DENIED
    artifact = Rec(state_adoption_id=adoption.state_adoption_id, status=status, reason=reason, state_adopter_id=adoption.state_adopter_id, state_adopter_organization_id=adoption.state_adopter_organization_id, source_transition_completion_id=adoption.source_transition_completion_id, source_transition_completion_record_digest=adoption.source_transition_completion_record_digest, source_completion_operator_id=adoption.source_completion_operator_id, transition_package_digest=adoption.transition_package_digest, previous_lifecycle_state_digest=adoption.previous_lifecycle_state_digest, adopted_lifecycle_state_digest=adoption.adopted_lifecycle_state_digest, source_state_adoption_route_digest=adoption.source_state_adoption_route_digest, repository_review_route_digest=adoption.repository_review_route_digest, repository_review_deadline_at_epoch_seconds=adoption.repository_review_deadline_at_epoch_seconds, subject_id=adoption.subject_id, requester_id=adoption.requester_id, policy_digest=policy.policy_digest, adoption_digest=adoption.adoption_digest, evidence_digest=evidence.evidence_digest, checks=checks, evidence_digests=expected_digests, source_transition_completion_ready=checks["source_transition_completion_ready"], state_adoption_record_issued=issued, state_adoption_completed=issued, lifecycle_state_adopted=adopted, lifecycle_transition_performed=adopted, lifecycle_state_changed=adopted, state_adoption_denied=denied, state_adoption_rejected=status == REJECTED, ready_for_separate_repository_mutation_review=adopted, repository_mutation_review_required_next=adopted, repository_mutation_review_route_required_next=adopted, state_adoption_replan_required_next=denied, state_adoption_replan_route_required_next=denied, authority_changed=False, quiescence_state_changed=False, terminal_state_changed=False, terminal_marker_written=False, resource_removed=False, external_operation_performed=False, repository_changed=False, repository_read_only=True, record_digest="", version=VERSION)
    artifact.record_digest = record_digest(artifact)
    return artifact

def verify_artifact(*args: Any, **kwargs: Any) -> Rec:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError("lifecycle_state_adoption_record_invalid:" + issues[0])
    return artifact

def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("state_adoption_recomputation_mismatch")
    if artifact.status not in (ADOPTED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == ADOPTED and not all((artifact.state_adoption_record_issued, artifact.state_adoption_completed, artifact.lifecycle_state_adopted, artifact.lifecycle_transition_performed, artifact.lifecycle_state_changed, artifact.ready_for_separate_repository_mutation_review, artifact.repository_mutation_review_required_next, not artifact.repository_changed)):
        issues.append("adopted_gate_invalid")
    if artifact.status == DENIED and not all((artifact.state_adoption_record_issued, artifact.state_adoption_completed, artifact.state_adoption_denied, not artifact.lifecycle_state_adopted, not artifact.lifecycle_state_changed, artifact.state_adoption_replan_required_next)):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and any((artifact.state_adoption_record_issued, artifact.state_adoption_completed, artifact.lifecycle_state_adopted, artifact.lifecycle_state_changed, artifact.repository_mutation_review_required_next, artifact.state_adoption_replan_required_next)):
        issues.append("rejected_record_issued")
    if any((artifact.authority_changed, artifact.quiescence_state_changed, artifact.terminal_state_changed, artifact.terminal_marker_written, artifact.resource_removed, artifact.external_operation_performed, artifact.repository_changed)):
        issues.append("repository_or_external_effect_performed")
    if not artifact.repository_read_only:
        issues.append("repository_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
