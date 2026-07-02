#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import fields, replace

from runtime.kuuos_apoptosis_authority_review_types_v0_4 import (
    ApoptosisAuthorityEvidence, ApoptosisAuthorityReviewPolicy,
    ApoptosisAuthorityReviewRecord, ApoptosisAuthorityReviewRequest,
)
from runtime.kuuos_apoptosis_candidate_types_v0_2 import (
    ApoptosisCandidatePolicy, ApoptosisCandidateRecord, ApoptosisCandidateRequest,
)
from runtime.kuuos_apoptosis_dependency_review_types_v0_3 import (
    ApoptosisDependencyEvidence, ApoptosisDependencyReviewPolicy,
    ApoptosisDependencyReviewRecord, ApoptosisDependencyReviewRequest,
)
from runtime.kuuos_apoptosis_observation_types_v0_1 import (
    ApoptosisObservationInput, ApoptosisObservationPolicy, ApoptosisObservationRecord,
)
from runtime.kuuos_apoptosis_quiescence_review_types_v0_5 import (
    QUIESCENCE_REVIEW_CLEAR, ApoptosisQuiescenceEvidence,
    ApoptosisQuiescenceReviewPolicy, ApoptosisQuiescenceReviewRecord,
    ApoptosisQuiescenceReviewRequest,
)
from runtime.kuuos_apoptosis_quiescence_review_v0_5 import (
    apoptosis_quiescence_evidence_issues,
    apoptosis_quiescence_review_policy_issues,
    apoptosis_quiescence_review_record_issues,
    apoptosis_quiescence_review_request_issues,
)
from runtime.kuuos_apoptosis_external_review_types_v0_6 import (
    EXTERNAL_REVIEW_BLOCKED, EXTERNAL_REVIEW_CLEAR, EXTERNAL_REVIEW_REJECTED,
    OBJECTIVE_EXTERNAL_REVIEW_ONLY, ApoptosisExternalReviewEvidence,
    ApoptosisExternalReviewPolicy, ApoptosisExternalReviewRecord,
    ApoptosisExternalReviewRequest, apoptosis_external_review_evidence_digest,
    apoptosis_external_review_policy_digest, apoptosis_external_review_record_digest,
    apoptosis_external_review_request_digest,
)


def _canon(xs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(xs)))


_REQUIRED_POLICY = (
    "require_source_quiescence_review_recomputation", "require_clear_quiescence_source",
    "require_source_subject_binding", "require_source_artifact_binding",
    "require_qualified_reviewer", "require_independent_reviewer",
    "require_conflict_disclosure", "require_no_material_conflict",
    "require_complete_review_scope", "require_review_methodology",
    "require_complete_evidence_receipt", "require_appeal_route", "require_dissent_route",
    "require_protected_core_exclusion", "require_no_institutional_hold",
    "require_no_emergency_state", "require_review_not_expired",
    "require_future_authority_separation", "require_independent_authorization_next",
    "allow_external_review_record_issuance",
)
_EFFECT_POLICY = (
    "allow_authorization_request", "allow_authorization_decision",
    "allow_authority_revocation", "allow_quiescence_transition",
    "allow_terminal_transition", "allow_tombstone_write", "allow_physical_deletion",
    "allow_live_git_execution", "allow_repository_mutation",
)
_EFFECT_RECORD = (
    "authorization_request_issued", "authorization_decision_made",
    "authority_revocation_performed", "quiescence_transition_performed",
    "terminal_transition_performed", "tombstone_write_performed",
    "physical_deletion_performed", "live_git_execution_performed",
    "repository_mutation_performed",
)


def build_apoptosis_external_review_policy(
    policy_id: str, *, allowed_reviewer_ids: tuple[str, ...],
    allowed_reviewer_organization_ids: tuple[str, ...],
    allowed_objectives: tuple[str, ...] = (OBJECTIVE_EXTERNAL_REVIEW_ONLY,),
    max_review_delay_seconds: int = 86_400, max_evidence_age_seconds: int = 3_600,
) -> ApoptosisExternalReviewPolicy:
    values = dict(
        policy_id=policy_id, allowed_reviewer_ids=_canon(allowed_reviewer_ids),
        allowed_reviewer_organization_ids=_canon(allowed_reviewer_organization_ids),
        allowed_objectives=_canon(allowed_objectives),
        max_review_delay_seconds=max_review_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        policy_digest="",
    )
    values.update({name: True for name in _REQUIRED_POLICY})
    values.update({name: False for name in _EFFECT_POLICY})
    policy = ApoptosisExternalReviewPolicy(**values)
    policy = replace(policy, policy_digest=apoptosis_external_review_policy_digest(policy))
    issues = apoptosis_external_review_policy_issues(policy)
    if issues:
        raise ValueError(f"apoptosis_external_review_policy_invalid:{issues[0]}")
    return policy


def apoptosis_external_review_policy_issues(policy: ApoptosisExternalReviewPolicy) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("apoptosis_external_review_policy_id_missing")
    for name in ("allowed_reviewer_ids", "allowed_reviewer_organization_ids"):
        values = getattr(policy, name)
        if not values or values != _canon(values):
            issues.append(f"apoptosis_external_review_{name}_invalid")
    if policy.allowed_objectives != (OBJECTIVE_EXTERNAL_REVIEW_ONLY,):
        issues.append("apoptosis_external_review_objective_scope_invalid")
    if policy.max_review_delay_seconds <= 0 or policy.max_evidence_age_seconds <= 0:
        issues.append("apoptosis_external_review_time_bound_invalid")
    if not all(getattr(policy, name) for name in _REQUIRED_POLICY):
        issues.append("apoptosis_external_review_required_guard_disabled")
    if any(getattr(policy, name) for name in _EFFECT_POLICY):
        issues.append("apoptosis_external_review_execution_effect_enabled")
    if policy.policy_digest != apoptosis_external_review_policy_digest(policy):
        issues.append("apoptosis_external_review_policy_digest_mismatch")
    return tuple(issues)


def build_apoptosis_external_review_evidence(**values) -> ApoptosisExternalReviewEvidence:
    if "quiescence_request" in values:
        qreq = values.pop("quiescence_request"); qev = values.pop("quiescence_evidence")
        qpol = values.pop("quiescence_policy"); qrec = values.pop("quiescence_record")
        areq = values.pop("authority_request"); aev = values.pop("authority_evidence")
        apol = values.pop("authority_policy"); arec = values.pop("authority_record")
        dreq = values.pop("dependency_request"); dev = values.pop("dependency_evidence")
        dpol = values.pop("dependency_policy"); drec = values.pop("dependency_record")
        oin = values.pop("observation_input"); opol = values.pop("observation_policy")
        orec = values.pop("observation_record"); creq = values.pop("candidate_request")
        cpol = values.pop("candidate_policy"); crec = values.pop("candidate_record")
        values.update(
            subject_id=qrec.subject_id, subject_kind=qrec.subject_kind,
            subject_version=qrec.subject_version, source_quiescence_review_id=qrec.review_id,
            source_observation_input_digest=oin.input_digest,
            source_observation_policy_digest=opol.policy_digest,
            source_observation_record_digest=orec.record_digest,
            source_candidate_request_digest=creq.request_digest,
            source_candidate_policy_digest=cpol.policy_digest,
            source_candidate_record_digest=crec.candidate_digest,
            source_dependency_evidence_digest=dev.evidence_digest,
            source_dependency_review_request_digest=dreq.request_digest,
            source_dependency_review_policy_digest=dpol.policy_digest,
            source_dependency_review_record_digest=drec.record_digest,
            source_authority_evidence_digest=aev.evidence_digest,
            source_authority_review_request_digest=areq.request_digest,
            source_authority_review_policy_digest=apol.policy_digest,
            source_authority_review_record_digest=arec.record_digest,
            source_quiescence_evidence_digest=qev.evidence_digest,
            source_quiescence_review_request_digest=qreq.request_digest,
            source_quiescence_review_policy_digest=qpol.policy_digest,
            source_quiescence_review_record_digest=qrec.record_digest,
        )
    evidence = ApoptosisExternalReviewEvidence(evidence_digest="", **values)
    evidence = replace(evidence, evidence_digest=apoptosis_external_review_evidence_digest(evidence))
    issues = apoptosis_external_review_evidence_issues(evidence)
    if issues:
        raise ValueError(f"apoptosis_external_review_evidence_invalid:{issues[0]}")
    return evidence


def apoptosis_external_review_evidence_issues(evidence: ApoptosisExternalReviewEvidence) -> tuple[str, ...]:
    issues: list[str] = []
    optional = {"evidence_digest", "version"}
    for item in fields(evidence):
        value = getattr(evidence, item.name)
        if item.name.endswith("_epoch_seconds") and value < 0:
            issues.append(f"apoptosis_external_review_{item.name}_invalid")
        elif item.type == "str" and item.name not in optional and not value:
            issues.append(f"apoptosis_external_review_{item.name}_missing")
    if evidence.evidence_digest != apoptosis_external_review_evidence_digest(evidence):
        issues.append("apoptosis_external_review_evidence_digest_mismatch")
    return tuple(issues)


def build_apoptosis_external_review_request(
    review_id: str, reviewer_id: str, reviewer_organization_id: str,
    requested_at_epoch_seconds: int, completed_at_epoch_seconds: int,
    quiescence_record: ApoptosisQuiescenceReviewRecord,
    external_evidence: ApoptosisExternalReviewEvidence, *,
    objective: str = OBJECTIVE_EXTERNAL_REVIEW_ONLY,
    future_authorization_authority_id: str,
    future_execution_authority_id: str,
) -> ApoptosisExternalReviewRequest:
    request = ApoptosisExternalReviewRequest(
        review_id=review_id, reviewer_id=reviewer_id,
        reviewer_organization_id=reviewer_organization_id, objective=objective,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        source_quiescence_review_id=quiescence_record.review_id,
        source_quiescence_review_record_digest=quiescence_record.record_digest,
        subject_id=quiescence_record.subject_id, subject_kind=quiescence_record.subject_kind,
        subject_version=quiescence_record.subject_version,
        external_review_evidence_digest=external_evidence.evidence_digest,
        future_authorization_authority_id=future_authorization_authority_id,
        future_execution_authority_id=future_execution_authority_id,
        request_digest="",
    )
    request = replace(request, request_digest=apoptosis_external_review_request_digest(request))
    issues = apoptosis_external_review_request_issues(request)
    if issues:
        raise ValueError(f"apoptosis_external_review_request_invalid:{issues[0]}")
    return request


def apoptosis_external_review_request_issues(request: ApoptosisExternalReviewRequest) -> tuple[str, ...]:
    issues: list[str] = []
    for item in fields(request):
        value = getattr(request, item.name)
        if item.name.endswith("_epoch_seconds") and value < 0:
            issues.append(f"apoptosis_external_review_{item.name}_invalid")
        elif item.type == "str" and item.name not in {"request_digest", "version"} and not value:
            issues.append(f"apoptosis_external_review_{item.name}_missing")
    if request.request_digest != apoptosis_external_review_request_digest(request):
        issues.append("apoptosis_external_review_request_digest_mismatch")
    return tuple(issues)


def _source_valid(qreq, qev, qpol, qrec, areq, aev, apol, arec,
                  dreq, dev, dpol, drec, oin, opol, orec, creq, cpol, crec) -> bool:
    return not (
        apoptosis_quiescence_review_request_issues(qreq)
        or apoptosis_quiescence_evidence_issues(qev)
        or apoptosis_quiescence_review_policy_issues(qpol)
        or apoptosis_quiescence_review_record_issues(
            qrec, qreq, qev, qpol, areq, aev, apol, arec,
            dreq, dev, dpol, drec, oin, opol, orec, creq, cpol, crec,
        )
    )


def _artifact_binding(e, qreq, qev, qpol, qrec, areq, aev, apol, arec,
                      dreq, dev, dpol, drec, oin, opol, orec, creq, cpol, crec) -> bool:
    pairs = (
        (e.source_observation_input_digest, oin.input_digest),
        (e.source_observation_policy_digest, opol.policy_digest),
        (e.source_observation_record_digest, orec.record_digest),
        (e.source_candidate_request_digest, creq.request_digest),
        (e.source_candidate_policy_digest, cpol.policy_digest),
        (e.source_candidate_record_digest, crec.candidate_digest),
        (e.source_dependency_evidence_digest, dev.evidence_digest),
        (e.source_dependency_review_request_digest, dreq.request_digest),
        (e.source_dependency_review_policy_digest, dpol.policy_digest),
        (e.source_dependency_review_record_digest, drec.record_digest),
        (e.source_authority_evidence_digest, aev.evidence_digest),
        (e.source_authority_review_request_digest, areq.request_digest),
        (e.source_authority_review_policy_digest, apol.policy_digest),
        (e.source_authority_review_record_digest, arec.record_digest),
        (e.source_quiescence_evidence_digest, qev.evidence_digest),
        (e.source_quiescence_review_request_digest, qreq.request_digest),
        (e.source_quiescence_review_policy_digest, qpol.policy_digest),
        (e.source_quiescence_review_record_digest, qrec.record_digest),
    )
    return all(left == right for left, right in pairs)


def construct_apoptosis_external_review(
    request: ApoptosisExternalReviewRequest,
    external_evidence: ApoptosisExternalReviewEvidence,
    external_policy: ApoptosisExternalReviewPolicy,
    qreq: ApoptosisQuiescenceReviewRequest, qev: ApoptosisQuiescenceEvidence,
    qpol: ApoptosisQuiescenceReviewPolicy, qrec: ApoptosisQuiescenceReviewRecord,
    areq: ApoptosisAuthorityReviewRequest, aev: ApoptosisAuthorityEvidence,
    apol: ApoptosisAuthorityReviewPolicy, arec: ApoptosisAuthorityReviewRecord,
    dreq: ApoptosisDependencyReviewRequest, dev: ApoptosisDependencyEvidence,
    dpol: ApoptosisDependencyReviewPolicy, drec: ApoptosisDependencyReviewRecord,
    oin: ApoptosisObservationInput, opol: ApoptosisObservationPolicy,
    orec: ApoptosisObservationRecord, creq: ApoptosisCandidateRequest,
    cpol: ApoptosisCandidatePolicy, crec: ApoptosisCandidateRecord,
) -> ApoptosisExternalReviewRecord:
    e = external_evidence
    source_valid = _source_valid(qreq, qev, qpol, qrec, areq, aev, apol, arec,
                                 dreq, dev, dpol, drec, oin, opol, orec, creq, cpol, crec)
    source_clear = qrec.status == QUIESCENCE_REVIEW_CLEAR and qrec.quiescence_review_record_issued and qrec.quiescence_clear_for_external_review
    subject_binding = (request.subject_id, request.subject_kind, request.subject_version) == (qrec.subject_id, qrec.subject_kind, qrec.subject_version) == (e.subject_id, e.subject_kind, e.subject_version)
    artifact_binding = _artifact_binding(e, qreq, qev, qpol, qrec, areq, aev, apol, arec,
                                         dreq, dev, dpol, drec, oin, opol, orec, creq, cpol, crec)
    identity_binding = request.review_id == e.external_review_id and request.reviewer_id == e.external_reviewer_id and request.reviewer_organization_id == e.external_reviewer_organization_id
    excluded = {request.subject_id, crec.issuer_id, drec.reviewer_id, arec.reviewer_id,
                aev.responsible_authority_id, qrec.reviewer_id, e.quiescence_evidence_producer_id}
    prior_independent = request.reviewer_id not in excluded
    auth_independent = request.reviewer_id != request.future_authorization_authority_id
    exec_independent = request.reviewer_id != request.future_execution_authority_id
    time_order = e.review_requested_at_epoch_seconds <= e.captured_at_epoch_seconds <= e.review_completed_at_epoch_seconds == request.completed_at_epoch_seconds
    delay = request.completed_at_epoch_seconds - qrec.reviewed_at_epoch_seconds
    age = request.completed_at_epoch_seconds - e.captured_at_epoch_seconds
    review_delay_valid = 0 <= delay <= external_policy.max_review_delay_seconds
    evidence_fresh = 0 <= age <= external_policy.max_evidence_age_seconds
    review_not_expired = request.completed_at_epoch_seconds <= e.review_expiry_at_epoch_seconds
    checks = dict(
        policy_valid=not apoptosis_external_review_policy_issues(external_policy),
        request_valid=not apoptosis_external_review_request_issues(request),
        evidence_valid=not apoptosis_external_review_evidence_issues(e),
        source_recomputed_valid=source_valid, source_quiescence_clear=source_clear,
        source_subject_binding_valid=subject_binding,
        source_artifact_binding_valid=artifact_binding,
        reviewer_allowed=request.reviewer_id in external_policy.allowed_reviewer_ids,
        reviewer_organization_allowed=request.reviewer_organization_id in external_policy.allowed_reviewer_organization_ids,
        reviewer_identity_binding_valid=identity_binding,
        reviewer_qualified=e.reviewer_qualification_verified,
        reviewer_independence_declared=e.reviewer_independence_declared,
        reviewer_independent=prior_independent and auth_independent and exec_independent,
        independent_from_prior_chain=prior_independent,
        independent_from_future_authorization_authority=auth_independent,
        independent_from_future_execution_authority=exec_independent,
        objective_allowed=request.objective in external_policy.allowed_objectives,
        review_delay_valid=review_delay_valid, evidence_fresh=evidence_fresh,
        review_time_order_valid=time_order, review_not_expired=review_not_expired,
        conflict_disclosure_complete=e.conflict_disclosure_complete,
        material_conflict_present=e.material_conflict_present,
        review_scope_complete=e.review_scope_complete,
        review_methodology_present=bool(e.review_methodology_digest),
        evidence_receipt_complete=e.review_evidence_receipt_complete,
        appeal_route_available=e.appeal_route_available,
        dissent_route_available=e.dissent_route_available,
        protected_core_excluded=e.protected_core_excluded,
        institutional_hold_active=e.institutional_hold_active,
        emergency_state_active=e.emergency_state_active,
    )
    base_names = (
        "policy_valid", "request_valid", "evidence_valid", "source_recomputed_valid",
        "source_quiescence_clear", "source_subject_binding_valid",
        "source_artifact_binding_valid", "reviewer_allowed",
        "reviewer_organization_allowed", "reviewer_identity_binding_valid",
        "reviewer_independent", "independent_from_prior_chain",
        "independent_from_future_authorization_authority",
        "independent_from_future_execution_authority", "objective_allowed",
        "review_delay_valid", "evidence_fresh", "review_time_order_valid", "review_not_expired",
    )
    if not all(checks[name] for name in base_names):
        status, reason = EXTERNAL_REVIEW_REJECTED, "external_review_source_request_policy_or_binding_invalid"
    else:
        blockers = (
            (e.emergency_state_active, "emergency_state_active"),
            (e.institutional_hold_active, "institutional_hold_active"),
            (not e.protected_core_excluded, "protected_core_not_excluded"),
            (not e.reviewer_qualification_verified, "reviewer_qualification_not_verified"),
            (not e.reviewer_independence_declared, "reviewer_independence_not_declared"),
            (not e.conflict_disclosure_complete, "conflict_disclosure_incomplete"),
            (e.material_conflict_present, "material_conflict_present"),
            (not e.review_scope_complete, "review_scope_incomplete"),
            (not e.review_methodology_digest, "review_methodology_missing"),
            (not e.review_evidence_receipt_complete, "review_evidence_receipt_incomplete"),
            (not e.appeal_route_available, "appeal_route_missing"),
            (not e.dissent_route_available, "dissent_route_missing"),
        )
        hit = next(((True, reason) for condition, reason in blockers if condition), None)
        status, reason = (EXTERNAL_REVIEW_BLOCKED, hit[1]) if hit else (EXTERNAL_REVIEW_CLEAR, "external_review_clear_for_independent_authorization_only")
    issued = status != EXTERNAL_REVIEW_REJECTED
    clear = status == EXTERNAL_REVIEW_CLEAR
    checks.update(
        external_clear_for_independent_authorization=clear,
        external_review_record_issued=issued,
        independent_authorization_required_next=clear,
        **{name: False for name in _EFFECT_RECORD},
    )
    values = dict(
        review_id=request.review_id, status=status, reason=reason,
        policy_digest=external_policy.policy_digest, request_digest=request.request_digest,
        external_review_evidence_digest=e.evidence_digest,
        source_quiescence_review_id=request.source_quiescence_review_id,
        source_quiescence_review_record_digest=request.source_quiescence_review_record_digest,
        subject_id=request.subject_id, subject_kind=request.subject_kind,
        subject_version=request.subject_version, reviewer_id=request.reviewer_id,
        reviewer_organization_id=request.reviewer_organization_id,
        objective=request.objective, requested_at_epoch_seconds=request.requested_at_epoch_seconds,
        completed_at_epoch_seconds=request.completed_at_epoch_seconds,
        future_authorization_authority_id=request.future_authorization_authority_id,
        future_execution_authority_id=request.future_execution_authority_id,
        checks=checks,
        evidence_digests={
            "external_review_policy": external_policy.policy_digest,
            "external_review_request": request.request_digest,
            "external_review_evidence": e.evidence_digest,
            "source_quiescence_review_record": qrec.record_digest,
            "source_quiescence_review_request": qreq.request_digest,
            "source_quiescence_evidence": qev.evidence_digest,
            "source_authority_review_record": arec.record_digest,
            "source_dependency_review_record": drec.record_digest,
            "source_candidate_record": crec.candidate_digest,
            "source_observation_record": orec.record_digest,
        },
        record_digest="",
    )
    for name in (item.name for item in fields(ApoptosisExternalReviewRecord)):
        if name not in values and name not in {"version", "record_digest"}:
            values[name] = checks[name]
    record = ApoptosisExternalReviewRecord(**values)
    return replace(record, record_digest=apoptosis_external_review_record_digest(record))


def review_apoptosis_external(*args, **kwargs) -> ApoptosisExternalReviewRecord:
    record = construct_apoptosis_external_review(*args, **kwargs)
    issues = apoptosis_external_review_record_issues(record, *args, **kwargs)
    if issues:
        raise ValueError(f"apoptosis_external_review_record_invalid:{issues[0]}")
    return record


def apoptosis_external_review_record_issues(record: ApoptosisExternalReviewRecord, *args, **kwargs) -> tuple[str, ...]:
    expected = construct_apoptosis_external_review(*args, **kwargs)
    issues: list[str] = []
    if record.to_dict() != expected.to_dict():
        issues.append("apoptosis_external_review_recomputation_mismatch")
    if record.status not in (EXTERNAL_REVIEW_CLEAR, EXTERNAL_REVIEW_BLOCKED, EXTERNAL_REVIEW_REJECTED):
        issues.append("apoptosis_external_review_status_invalid")
    if record.status == EXTERNAL_REVIEW_CLEAR and (not record.external_review_record_issued or not record.external_clear_for_independent_authorization or not record.independent_authorization_required_next):
        issues.append("apoptosis_external_review_clear_gate_invalid")
    if record.status == EXTERNAL_REVIEW_BLOCKED and (not record.external_review_record_issued or record.external_clear_for_independent_authorization or record.independent_authorization_required_next):
        issues.append("apoptosis_external_review_blocked_advanced")
    if record.status == EXTERNAL_REVIEW_REJECTED and record.external_review_record_issued:
        issues.append("apoptosis_external_review_rejected_record_issued")
    if any(getattr(record, name) for name in _EFFECT_RECORD):
        issues.append("apoptosis_external_review_execution_effect_performed")
    if record.record_digest != apoptosis_external_review_record_digest(record):
        issues.append("apoptosis_external_review_record_digest_mismatch")
    return tuple(issues)


__all__ = [
    "build_apoptosis_external_review_policy", "apoptosis_external_review_policy_issues",
    "build_apoptosis_external_review_evidence", "apoptosis_external_review_evidence_issues",
    "build_apoptosis_external_review_request", "apoptosis_external_review_request_issues",
    "construct_apoptosis_external_review", "review_apoptosis_external",
    "apoptosis_external_review_record_issues",
]
