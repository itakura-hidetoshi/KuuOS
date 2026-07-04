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

VERSION = "kuuos_lifecycle_execution_result_adoption_v0_31"
ADOPTED = "LIFECYCLE_EXECUTION_RESULT_ADOPTION_ADOPTED_FOR_SEPARATE_LIFECYCLE_CLOSURE_REVIEW"
HELD = "LIFECYCLE_EXECUTION_RESULT_ADOPTION_HELD"
REJECTED = "LIFECYCLE_EXECUTION_RESULT_ADOPTION_REJECTED"
OBJECTIVE = "ADOPT_EXECUTION_RESULT_FOR_SEPARATE_LIFECYCLE_CLOSURE_REVIEW_ONLY"
SOURCE_ORDER_CHECK = "source_result_review_precedes_result_adoption_and_deadline_valid"


class Rec(SimpleNamespace):
    def to_dict(self) -> dict[str, Any]:
        out = {}
        for k, v in self.__dict__.items():
            out[k] = list(v) if isinstance(v, tuple) else dict(v) if isinstance(v, dict) else v
        return out


def _digest(value: Rec, field: str) -> str:
    payload = value.to_dict(); payload.pop(field, None); return canonical_digest(payload)

def policy_digest(v: Rec) -> str: return _digest(v, "policy_digest")
def evidence_digest(v: Rec) -> str: return _digest(v, "evidence_digest")
def adoption_digest(v: Rec) -> str: return _digest(v, "adoption_digest")
def record_digest(v: Rec) -> str: return _digest(v, "record_digest")
def _canon(xs: tuple[str, ...]) -> tuple[str, ...]: return tuple(sorted(set(xs)))


def make_policy(policy_id: str, *, allowed_adopter_ids: tuple[str, ...], allowed_adopter_organization_ids: tuple[str, ...], max_adoption_delay_seconds: int = 900, max_evidence_age_seconds: int = 300, max_closure_review_delay_seconds: int = 900) -> Rec:
    v = Rec(policy_id=policy_id, allowed_adopter_ids=_canon(allowed_adopter_ids), allowed_adopter_organization_ids=_canon(allowed_adopter_organization_ids), max_adoption_delay_seconds=max_adoption_delay_seconds, max_evidence_age_seconds=max_evidence_age_seconds, max_closure_review_delay_seconds=max_closure_review_delay_seconds, accepted_source_required=True, source_recomputation_required=True, result_adoption_route_required=True, adopter_authority_required=True, adopter_separation_required=True, closure_review_route_required_next=True, repository_read_only=True, file_write_absent_required=True, ref_update_absent_required=True, branch_move_absent_required=True, external_operation_absent_required=True, terminal_marker_absent_required=True, resource_removal_absent_required=True, policy_digest="", version=VERSION)
    v.policy_digest = policy_digest(v)
    issues = policy_issues(v)
    if issues: raise ValueError("lifecycle_execution_result_adoption_policy_invalid:" + issues[0])
    return v


def policy_issues(v: Rec) -> tuple[str, ...]:
    issues = []
    if not v.policy_id: issues.append("policy_id_missing")
    if not v.allowed_adopter_ids or not v.allowed_adopter_organization_ids: issues.append("allowed_adopter_missing")
    if min(v.max_adoption_delay_seconds, v.max_evidence_age_seconds, v.max_closure_review_delay_seconds) <= 0: issues.append("bound_invalid")
    if not all((v.repository_read_only, v.file_write_absent_required, v.ref_update_absent_required, v.branch_move_absent_required, v.external_operation_absent_required, v.terminal_marker_absent_required, v.resource_removal_absent_required)): issues.append("adoption_guard_disabled")
    if v.policy_digest != policy_digest(v): issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> dict[str, str]:
    if len(source_args) < 4: raise ValueError("source_argument_count_invalid")
    result = review_source_digests(source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:]))
    result.update(lifecycle_execution_result_review=source_review.review_digest, lifecycle_execution_result_review_evidence=source_evidence.evidence_digest, lifecycle_execution_result_review_policy=source_policy.policy_digest, lifecycle_execution_result_review_record=source_record.record_digest)
    return result


def source_recomputed_valid(source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> bool:
    return not source_artifact_issues(source_record, source_review, source_evidence, source_policy, *source_args)


def expected_closure_review_route_digest(source_review, source_record, *, adoption_id: str, adopter_id: str, adoption_receipt_digest: str, closure_review_deadline_at_epoch_seconds: int) -> str:
    return canonical_digest({"source_review_id": source_review.review_id, "source_review_record_digest": source_record.record_digest, "source_result_adoption_route_digest": source_review.result_adoption_route_digest, "adoption_id": adoption_id, "adopter_id": adopter_id, "adopted_lifecycle_state_digest": source_review.adopted_lifecycle_state_digest, "result_review_receipt_digest": source_review.result_review_receipt_digest, "adoption_receipt_digest": adoption_receipt_digest, "closure_review_deadline_at_epoch_seconds": closure_review_deadline_at_epoch_seconds})


def make_evidence(source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...], **kw: Any) -> Rec:
    values = dict(source_review_id=source_review.review_id, source_review_record_digest=source_record.record_digest, source_artifact_digests=all_source_digests(source_review, source_evidence, source_policy, source_record, source_args), source_reviewer_id=source_review.result_reviewer_id, source_reviewer_organization_id=source_review.result_reviewer_organization_id, source_execution_id=source_review.source_execution_id, source_repository_review_id=source_review.source_repository_review_id, subject_id=source_review.subject_id, requester_id=source_review.requester_id, transition_package_digest=source_review.transition_package_digest, adopted_lifecycle_state_digest=source_review.adopted_lifecycle_state_digest, result_review_receipt_digest=source_review.result_review_receipt_digest, source_result_adoption_route_digest=source_review.result_adoption_route_digest, source_result_adoption_deadline_at_epoch_seconds=source_review.result_adoption_deadline_at_epoch_seconds)
    values.update(kw)
    if "closure_review_route_digest" not in values:
        values["closure_review_route_digest"] = expected_closure_review_route_digest(source_review, source_record, adoption_id=values["adoption_id"], adopter_id=values["adopter_id"], adoption_receipt_digest=values["adoption_receipt_digest"], closure_review_deadline_at_epoch_seconds=values["closure_review_deadline_at_epoch_seconds"])
    v = Rec(version=VERSION, evidence_digest="", **values); v.evidence_digest = evidence_digest(v)
    issues = evidence_issues(v)
    if issues: raise ValueError("lifecycle_execution_result_adoption_evidence_invalid:" + issues[0])
    return v


def evidence_issues(v: Rec) -> tuple[str, ...]:
    required = ("evidence_id", "adoption_id", "adopter_id", "adopter_organization_id", "adopter_mandate_receipt_digest", "adopter_authority_receipt_digest", "adopter_identity_confirmation_digest", "source_review_id", "source_review_record_digest", "source_result_adoption_route_digest", "adoption_receipt_digest", "closure_review_route_digest", "result_adoption_receipt_digest")
    issues = []
    if not all(getattr(v, name, None) for name in required): issues.append("required_evidence_field_missing")
    if min(v.adoption_requested_at_epoch_seconds, v.captured_at_epoch_seconds, v.adopted_at_epoch_seconds, v.source_result_adoption_deadline_at_epoch_seconds, v.closure_review_deadline_at_epoch_seconds) < 0: issues.append("negative_adoption_time")
    if v.evidence_digest != evidence_digest(v): issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_adoption(adoption_id: str, adopter_id: str, adopter_organization_id: str, adoption_requested_at_epoch_seconds: int, adopted_at_epoch_seconds: int, source_review, source_record, adoption_evidence: Rec, *, adoption_receipt_digest: str, closure_review_route_digest: str, closure_review_deadline_at_epoch_seconds: int, adoption_confirmed: bool, hold_reason_digest: str = "", objective: str = OBJECTIVE) -> Rec:
    v = Rec(adoption_id=adoption_id, adopter_id=adopter_id, adopter_organization_id=adopter_organization_id, objective=objective, adoption_requested_at_epoch_seconds=adoption_requested_at_epoch_seconds, adopted_at_epoch_seconds=adopted_at_epoch_seconds, source_review_id=source_review.review_id, source_review_record_digest=source_record.record_digest, source_execution_id=source_review.source_execution_id, source_repository_review_id=source_review.source_repository_review_id, subject_id=source_review.subject_id, requester_id=source_review.requester_id, source_reviewer_id=source_review.result_reviewer_id, transition_package_digest=source_review.transition_package_digest, adopted_lifecycle_state_digest=source_review.adopted_lifecycle_state_digest, result_review_receipt_digest=source_review.result_review_receipt_digest, source_result_adoption_route_digest=source_review.result_adoption_route_digest, adoption_receipt_digest=adoption_receipt_digest, closure_review_route_digest=closure_review_route_digest, closure_review_deadline_at_epoch_seconds=closure_review_deadline_at_epoch_seconds, adoption_evidence_digest=adoption_evidence.evidence_digest, adoption_confirmed=adoption_confirmed, hold_reason_digest=hold_reason_digest, adoption_digest="", version=VERSION)
    v.adoption_digest = adoption_digest(v)
    issues = adoption_issues(v)
    if issues: raise ValueError("lifecycle_execution_result_adoption_invalid:" + issues[0])
    return v


def adoption_issues(v: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in v.to_dict().items():
        if name in ("hold_reason_digest", "adoption_digest", "version", "adoption_confirmed"): continue
        if content == "" or content is None: issues.append("required_adoption_field_missing"); break
    if not v.adoption_confirmed and not v.hold_reason_digest: issues.append("hold_reason_missing")
    if min(v.adoption_requested_at_epoch_seconds, v.adopted_at_epoch_seconds, v.closure_review_deadline_at_epoch_seconds) < 0: issues.append("negative_adoption_time")
    if v.adoption_digest != adoption_digest(v): issues.append("adoption_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all((record.status == SOURCE_ACCEPTED, record.execution_result_review_record_issued, record.execution_result_review_completed, record.execution_result_review_accepted, record.ready_for_separate_execution_result_adoption, record.execution_result_adoption_required_next, record.execution_result_adoption_route_required_next, not record.repository_changed, record.repository_read_only))


def _prior_actor_ids(source_review, source_evidence) -> set[str]:
    return {source_review.subject_id, source_review.requester_id, source_review.source_executor_id, source_review.result_reviewer_id, source_evidence.result_reviewer_id}


def evaluate(adoption: Rec, evidence: Rec, policy: Rec, source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(source_review, source_evidence, source_policy, source_record, source_args)
    expected_route = expected_closure_review_route_digest(source_review, source_record, adoption_id=adoption.adoption_id, adopter_id=adoption.adopter_id, adoption_receipt_digest=adoption.adoption_receipt_digest, closure_review_deadline_at_epoch_seconds=adoption.closure_review_deadline_at_epoch_seconds)
    prior = _prior_actor_ids(source_review, source_evidence)
    adoption_delay = evidence.adopted_at_epoch_seconds - source_review.reviewed_at_epoch_seconds
    evidence_age = evidence.adopted_at_epoch_seconds - evidence.captured_at_epoch_seconds
    closure_delay = evidence.closure_review_deadline_at_epoch_seconds - evidence.adopted_at_epoch_seconds
    checks = {
        "policy_valid": not policy_issues(policy), "adoption_valid": not adoption_issues(adoption), "evidence_valid": not evidence_issues(evidence), "source_recomputed_valid": source_recomputed_valid(source_review, source_evidence, source_policy, source_record, source_args), "source_review_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests and adoption.source_review_id == evidence.source_review_id == source_review.review_id and adoption.source_review_record_digest == evidence.source_review_record_digest == source_record.record_digest,
        "identity_binding_valid": adoption.adoption_id == evidence.adoption_id and adoption.adopter_id == evidence.adopter_id and adoption.adopter_organization_id == evidence.adopter_organization_id and adoption.adoption_evidence_digest == evidence.evidence_digest,
        "result_adoption_route_binding_valid": adoption.source_result_adoption_route_digest == evidence.source_result_adoption_route_digest == source_review.result_adoption_route_digest,
        "closure_review_route_binding_valid": adoption.closure_review_route_digest == evidence.closure_review_route_digest == expected_route,
        "result_review_receipt_binding_valid": adoption.result_review_receipt_digest == evidence.result_review_receipt_digest == source_review.result_review_receipt_digest,
        "adoption_receipt_binding_valid": adoption.adoption_receipt_digest == evidence.adoption_receipt_digest,
        "adopter_allowed": adoption.adopter_id in policy.allowed_adopter_ids, "adopter_organization_allowed": adoption.adopter_organization_id in policy.allowed_adopter_organization_ids,
        "adopter_separated_from_reviewer": adoption.adopter_id != source_review.result_reviewer_id, "adopter_separated_from_prior_actors": adoption.adopter_id not in prior, "adopter_organization_separated": adoption.adopter_organization_id != source_review.result_reviewer_organization_id,
        "objective_allowed": adoption.objective == OBJECTIVE, "adoption_delay_valid": 0 <= adoption_delay <= policy.max_adoption_delay_seconds, "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds, "closure_review_delay_valid": 0 < closure_delay <= policy.max_closure_review_delay_seconds,
        "time_order_valid": source_review.reviewed_at_epoch_seconds <= evidence.adoption_requested_at_epoch_seconds <= evidence.captured_at_epoch_seconds <= evidence.adopted_at_epoch_seconds < evidence.closure_review_deadline_at_epoch_seconds,
        "source_adoption_deadline_valid": evidence.adopted_at_epoch_seconds <= source_review.result_adoption_deadline_at_epoch_seconds,
        "external_operation_absent": not evidence.external_operation_performed, "file_write_absent": not evidence.file_written, "ref_update_absent": not evidence.ref_updated, "branch_move_absent": not evidence.branch_moved, "terminal_marker_absent": not evidence.terminal_marker_written, "resource_removal_absent": not evidence.resource_removed,
        "adopter_mandate_verified": evidence.adopter_mandate_verified, "adopter_authority_verified": evidence.adopter_authority_verified, "adopter_identity_confirmed": evidence.adopter_identity_confirmed, "review_record_fresh": evidence.review_record_fresh, "result_adoption_receipt_valid": evidence.result_adoption_receipt_valid, "no_unresolved_anomaly": not evidence.unresolved_anomaly_present, "recovery_not_in_progress": not evidence.recovery_in_progress, "institutional_hold_absent": not evidence.institutional_hold_active, "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests

STRUCTURAL_CHECKS = ("policy_valid", "adoption_valid", "evidence_valid", "source_recomputed_valid", "source_review_ready", "source_binding_valid", "identity_binding_valid", "result_adoption_route_binding_valid", "closure_review_route_binding_valid", "result_review_receipt_binding_valid", "adoption_receipt_binding_valid", "adopter_allowed", "adopter_organization_allowed", "adopter_separated_from_reviewer", "adopter_separated_from_prior_actors", "adopter_organization_separated", "objective_allowed", "adoption_delay_valid", "evidence_fresh", "closure_review_delay_valid", "time_order_valid", "source_adoption_deadline_valid", "external_operation_absent", "file_write_absent", "ref_update_absent", "branch_move_absent", "terminal_marker_absent", "resource_removal_absent")
HOLD_CHECKS = ("adopter_mandate_verified", "adopter_authority_verified", "adopter_identity_confirmed", "review_record_fresh", "result_adoption_receipt_valid", "no_unresolved_anomaly", "recovery_not_in_progress", "institutional_hold_absent", "emergency_state_absent")


def compute_artifact(adoption: Rec, evidence: Rec, policy: Rec, source_review, source_evidence, source_policy, source_record, *source_args: Any) -> Rec:
    checks, expected_digests = evaluate(adoption, evidence, policy, source_review, source_evidence, source_policy, source_record, tuple(source_args))
    checks[SOURCE_ORDER_CHECK] = source_review.reviewed_at_epoch_seconds <= adoption.adoption_requested_at_epoch_seconds <= adoption.adopted_at_epoch_seconds <= source_review.result_adoption_deadline_at_epoch_seconds
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS): status, reason = REJECTED, "source_review_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in HOLD_CHECKS if not checks[name]), None)
        if failed is not None: status, reason = HELD, failed
        elif adoption.adoption_confirmed: status, reason = ADOPTED, "adopted_for_separate_lifecycle_closure_review_only"
        else: status, reason = HELD, "execution_result_adoption_not_confirmed"
    issued, adopted, held = status != REJECTED, status == ADOPTED, status == HELD
    artifact = Rec(adoption_id=adoption.adoption_id, status=status, reason=reason, adopter_id=adoption.adopter_id, adopter_organization_id=adoption.adopter_organization_id, source_review_id=adoption.source_review_id, source_review_record_digest=adoption.source_review_record_digest, source_reviewer_id=adoption.source_reviewer_id, source_execution_id=adoption.source_execution_id, source_repository_review_id=adoption.source_repository_review_id, transition_package_digest=adoption.transition_package_digest, adopted_lifecycle_state_digest=adoption.adopted_lifecycle_state_digest, result_review_receipt_digest=adoption.result_review_receipt_digest, source_result_adoption_route_digest=adoption.source_result_adoption_route_digest, adoption_receipt_digest=adoption.adoption_receipt_digest, closure_review_route_digest=adoption.closure_review_route_digest, closure_review_deadline_at_epoch_seconds=adoption.closure_review_deadline_at_epoch_seconds, subject_id=adoption.subject_id, requester_id=adoption.requester_id, policy_digest=policy.policy_digest, adoption_digest=adoption.adoption_digest, evidence_digest=evidence.evidence_digest, checks=checks, evidence_digests=expected_digests, source_review_ready=checks["source_review_ready"], execution_result_adoption_record_issued=issued, execution_result_adoption_completed=issued, execution_result_adopted=adopted, execution_result_adoption_held=held, execution_result_adoption_rejected=status == REJECTED, ready_for_separate_lifecycle_closure_review=adopted, lifecycle_closure_review_required_next=adopted, lifecycle_closure_review_route_required_next=adopted, execution_result_adoption_replan_required_next=held, execution_result_adoption_replan_route_required_next=held, repository_changed=False, file_written=False, ref_updated=False, branch_moved=False, authority_changed=False, terminal_marker_written=False, resource_removed=False, external_operation_performed=False, repository_read_only=True, record_digest="", version=VERSION)
    artifact.record_digest = record_digest(artifact)
    return artifact


def verify_artifact(*args: Any, **kwargs: Any) -> Rec:
    artifact = compute_artifact(*args, **kwargs); issues = artifact_issues(artifact, *args, **kwargs)
    if issues: raise ValueError("lifecycle_execution_result_adoption_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs); issues = []
    if artifact.to_dict() != expected.to_dict(): issues.append("execution_result_adoption_recomputation_mismatch")
    if artifact.status not in (ADOPTED, HELD, REJECTED): issues.append("status_invalid")
    if artifact.status == ADOPTED and not all((artifact.execution_result_adoption_record_issued, artifact.execution_result_adoption_completed, artifact.execution_result_adopted, artifact.ready_for_separate_lifecycle_closure_review, artifact.lifecycle_closure_review_required_next, artifact.lifecycle_closure_review_route_required_next, not artifact.repository_changed)): issues.append("adopted_gate_invalid")
    if artifact.status == HELD and not all((artifact.execution_result_adoption_record_issued, artifact.execution_result_adoption_completed, artifact.execution_result_adoption_held, not artifact.lifecycle_closure_review_required_next, artifact.execution_result_adoption_replan_required_next)): issues.append("held_gate_invalid")
    if artifact.status == REJECTED and any((artifact.execution_result_adoption_record_issued, artifact.execution_result_adoption_completed, artifact.lifecycle_closure_review_required_next, artifact.execution_result_adoption_replan_required_next)): issues.append("rejected_record_issued")
    if any((artifact.repository_changed, artifact.file_written, artifact.ref_updated, artifact.branch_moved, artifact.authority_changed, artifact.terminal_marker_written, artifact.resource_removed, artifact.external_operation_performed)): issues.append("adoption_layer_effect_performed")
    if not artifact.repository_read_only: issues.append("repository_guard_disabled")
    if artifact.record_digest != record_digest(artifact): issues.append("record_digest_mismatch")
    return tuple(issues)
