#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import fields, replace

from runtime.kuuos_apoptosis_authority_review_types_v0_4 import (
    ApoptosisAuthorityEvidence,
    ApoptosisAuthorityReviewPolicy,
    ApoptosisAuthorityReviewRecord,
    ApoptosisAuthorityReviewRequest,
)
from runtime.kuuos_apoptosis_candidate_types_v0_2 import (
    ApoptosisCandidatePolicy,
    ApoptosisCandidateRecord,
    ApoptosisCandidateRequest,
)
from runtime.kuuos_apoptosis_dependency_review_types_v0_3 import (
    ApoptosisDependencyEvidence,
    ApoptosisDependencyReviewPolicy,
    ApoptosisDependencyReviewRecord,
    ApoptosisDependencyReviewRequest,
)
from runtime.kuuos_apoptosis_external_review_types_v0_6 import (
    EXTERNAL_REVIEW_CLEAR,
    ApoptosisExternalReviewEvidence,
    ApoptosisExternalReviewPolicy,
    ApoptosisExternalReviewRecord,
    ApoptosisExternalReviewRequest,
)
from runtime.kuuos_apoptosis_external_review_v0_6 import (
    apoptosis_external_review_evidence_issues,
    apoptosis_external_review_policy_issues,
    apoptosis_external_review_record_issues,
    apoptosis_external_review_request_issues,
)
from runtime.kuuos_apoptosis_observation_types_v0_1 import (
    ApoptosisObservationInput,
    ApoptosisObservationPolicy,
    ApoptosisObservationRecord,
)
from runtime.kuuos_apoptosis_quiescence_review_types_v0_5 import (
    ApoptosisQuiescenceEvidence,
    ApoptosisQuiescenceReviewPolicy,
    ApoptosisQuiescenceReviewRecord,
    ApoptosisQuiescenceReviewRequest,
)
from runtime.kuuos_apoptosis_independent_authorization_types_v0_7 import (
    INDEPENDENT_AUTHORIZATION_APPROVED,
    INDEPENDENT_AUTHORIZATION_DENIED,
    INDEPENDENT_AUTHORIZATION_REJECTED,
    OBJECTIVE_INDEPENDENT_AUTHORIZATION_ONLY,
    ApoptosisIndependentAuthorizationEvidence,
    ApoptosisIndependentAuthorizationPolicy,
    ApoptosisIndependentAuthorizationRecord,
    ApoptosisIndependentAuthorizationRequest,
    apoptosis_independent_authorization_evidence_digest,
    apoptosis_independent_authorization_policy_digest,
    apoptosis_independent_authorization_record_digest,
    apoptosis_independent_authorization_request_digest,
)


def _canon(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


_REQUIRED_POLICY = (
    "require_source_external_review_recomputation",
    "require_clear_external_review_source",
    "require_source_subject_binding",
    "require_source_artifact_binding",
    "require_external_authority_designation_binding",
    "require_authority_mandate",
    "require_authority_qualification",
    "require_independent_authority",
    "require_conflict_disclosure",
    "require_no_material_conflict",
    "require_jurisdiction",
    "require_quorum",
    "require_reasoned_decision",
    "require_proportionality_review",
    "require_less_restrictive_alternatives_review",
    "require_irreversibility_review",
    "require_human_impact_review",
    "require_appeal_route",
    "require_dissent_route",
    "require_protected_core_exclusion",
    "require_no_institutional_hold",
    "require_no_emergency_state",
    "require_authorization_not_expired",
    "require_execution_authority_separation",
    "allow_authorization_record_issuance",
    "allow_authorization_decision",
    "allow_bounded_execution_preparation_next",
)
_EFFECT_POLICY = (
    "allow_execution_request",
    "allow_execution_decision",
    "allow_authority_revocation",
    "allow_quiescence_transition",
    "allow_terminal_transition",
    "allow_tombstone_write",
    "allow_physical_deletion",
    "allow_live_git_execution",
    "allow_repository_mutation",
)
_EFFECT_RECORD = (
    "execution_request_issued",
    "execution_decision_made",
    "authority_revocation_performed",
    "quiescence_transition_performed",
    "terminal_transition_performed",
    "tombstone_write_performed",
    "physical_deletion_performed",
    "live_git_execution_performed",
    "repository_mutation_performed",
)


def build_apoptosis_independent_authorization_policy(
    policy_id: str,
    *,
    allowed_authority_ids: tuple[str, ...],
    allowed_authority_organization_ids: tuple[str, ...],
    allowed_objectives: tuple[str, ...] = (
        OBJECTIVE_INDEPENDENT_AUTHORIZATION_ONLY,
    ),
    max_authorization_delay_seconds: int = 86_400,
    max_evidence_age_seconds: int = 3_600,
) -> ApoptosisIndependentAuthorizationPolicy:
    values = dict(
        policy_id=policy_id,
        allowed_authority_ids=_canon(allowed_authority_ids),
        allowed_authority_organization_ids=_canon(
            allowed_authority_organization_ids
        ),
        allowed_objectives=_canon(allowed_objectives),
        max_authorization_delay_seconds=max_authorization_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        policy_digest="",
    )
    values.update({name: True for name in _REQUIRED_POLICY})
    values.update({name: False for name in _EFFECT_POLICY})
    policy = ApoptosisIndependentAuthorizationPolicy(**values)
    policy = replace(
        policy,
        policy_digest=apoptosis_independent_authorization_policy_digest(policy),
    )
    issues = apoptosis_independent_authorization_policy_issues(policy)
    if issues:
        raise ValueError(
            f"apoptosis_independent_authorization_policy_invalid:{issues[0]}"
        )
    return policy


def apoptosis_independent_authorization_policy_issues(
    policy: ApoptosisIndependentAuthorizationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("apoptosis_independent_authorization_policy_id_missing")
    for name in (
        "allowed_authority_ids",
        "allowed_authority_organization_ids",
    ):
        values = getattr(policy, name)
        if not values or values != _canon(values):
            issues.append(
                f"apoptosis_independent_authorization_{name}_invalid"
            )
    if policy.allowed_objectives != (
        OBJECTIVE_INDEPENDENT_AUTHORIZATION_ONLY,
    ):
        issues.append(
            "apoptosis_independent_authorization_objective_scope_invalid"
        )
    if (
        policy.max_authorization_delay_seconds <= 0
        or policy.max_evidence_age_seconds <= 0
    ):
        issues.append(
            "apoptosis_independent_authorization_time_bound_invalid"
        )
    if not all(getattr(policy, name) for name in _REQUIRED_POLICY):
        issues.append(
            "apoptosis_independent_authorization_required_guard_disabled"
        )
    if any(getattr(policy, name) for name in _EFFECT_POLICY):
        issues.append(
            "apoptosis_independent_authorization_execution_effect_enabled"
        )
    if (
        policy.policy_digest
        != apoptosis_independent_authorization_policy_digest(policy)
    ):
        issues.append(
            "apoptosis_independent_authorization_policy_digest_mismatch"
        )
    return tuple(issues)


def build_apoptosis_independent_authorization_evidence(
    **values,
) -> ApoptosisIndependentAuthorizationEvidence:
    if "external_request" in values:
        xreq = values.pop("external_request")
        xev = values.pop("external_evidence")
        xpol = values.pop("external_policy")
        xrec = values.pop("external_record")
        qreq = values.pop("quiescence_request")
        qev = values.pop("quiescence_evidence")
        qpol = values.pop("quiescence_policy")
        qrec = values.pop("quiescence_record")
        areq = values.pop("authority_request")
        aev = values.pop("authority_evidence")
        apol = values.pop("authority_policy")
        arec = values.pop("authority_record")
        dreq = values.pop("dependency_request")
        dev = values.pop("dependency_evidence")
        dpol = values.pop("dependency_policy")
        drec = values.pop("dependency_record")
        oin = values.pop("observation_input")
        opol = values.pop("observation_policy")
        orec = values.pop("observation_record")
        creq = values.pop("candidate_request")
        cpol = values.pop("candidate_policy")
        crec = values.pop("candidate_record")
        values.update(
            subject_id=xrec.subject_id,
            subject_kind=xrec.subject_kind,
            subject_version=xrec.subject_version,
            source_external_review_id=xrec.review_id,
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
            source_external_review_evidence_digest=xev.evidence_digest,
            source_external_review_request_digest=xreq.request_digest,
            source_external_review_policy_digest=xpol.policy_digest,
            source_external_review_record_digest=xrec.record_digest,
        )
    evidence = ApoptosisIndependentAuthorizationEvidence(
        evidence_digest="",
        **values,
    )
    evidence = replace(
        evidence,
        evidence_digest=apoptosis_independent_authorization_evidence_digest(
            evidence
        ),
    )
    issues = apoptosis_independent_authorization_evidence_issues(evidence)
    if issues:
        raise ValueError(
            f"apoptosis_independent_authorization_evidence_invalid:{issues[0]}"
        )
    return evidence


def apoptosis_independent_authorization_evidence_issues(
    evidence: ApoptosisIndependentAuthorizationEvidence,
) -> tuple[str, ...]:
    issues: list[str] = []
    optional = {
        "evidence_digest",
        "version",
        "authority_mandate_receipt_digest",
        "authority_qualification_receipt_digest",
        "authority_independence_declaration_digest",
        "conflict_of_interest_disclosure_digest",
        "jurisdiction_receipt_digest",
        "quorum_receipt_digest",
        "decision_rationale_digest",
        "proportionality_review_digest",
        "alternatives_review_digest",
        "irreversibility_review_digest",
        "human_impact_review_digest",
    }
    for item in fields(evidence):
        value = getattr(evidence, item.name)
        if item.name.endswith("_epoch_seconds") and value < 0:
            issues.append(
                f"apoptosis_independent_authorization_{item.name}_invalid"
            )
        elif item.type == "str" and item.name not in optional and not value:
            issues.append(
                f"apoptosis_independent_authorization_{item.name}_missing"
            )
    if (
        evidence.evidence_digest
        != apoptosis_independent_authorization_evidence_digest(evidence)
    ):
        issues.append(
            "apoptosis_independent_authorization_evidence_digest_mismatch"
        )
    return tuple(issues)


def build_apoptosis_independent_authorization_request(
    authorization_id: str,
    authority_id: str,
    authority_organization_id: str,
    requested_at_epoch_seconds: int,
    completed_at_epoch_seconds: int,
    external_record: ApoptosisExternalReviewRecord,
    authorization_evidence: ApoptosisIndependentAuthorizationEvidence,
    *,
    objective: str = OBJECTIVE_INDEPENDENT_AUTHORIZATION_ONLY,
    future_execution_authority_id: str,
) -> ApoptosisIndependentAuthorizationRequest:
    request = ApoptosisIndependentAuthorizationRequest(
        authorization_id=authorization_id,
        authority_id=authority_id,
        authority_organization_id=authority_organization_id,
        objective=objective,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        source_external_review_id=external_record.review_id,
        source_external_review_record_digest=external_record.record_digest,
        subject_id=external_record.subject_id,
        subject_kind=external_record.subject_kind,
        subject_version=external_record.subject_version,
        authorization_evidence_digest=authorization_evidence.evidence_digest,
        future_execution_authority_id=future_execution_authority_id,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=apoptosis_independent_authorization_request_digest(
            request
        ),
    )
    issues = apoptosis_independent_authorization_request_issues(request)
    if issues:
        raise ValueError(
            f"apoptosis_independent_authorization_request_invalid:{issues[0]}"
        )
    return request


def apoptosis_independent_authorization_request_issues(
    request: ApoptosisIndependentAuthorizationRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    for item in fields(request):
        value = getattr(request, item.name)
        if item.name.endswith("_epoch_seconds") and value < 0:
            issues.append(
                f"apoptosis_independent_authorization_{item.name}_invalid"
            )
        elif (
            item.type == "str"
            and item.name not in {"request_digest", "version"}
            and not value
        ):
            issues.append(
                f"apoptosis_independent_authorization_{item.name}_missing"
            )
    if (
        request.request_digest
        != apoptosis_independent_authorization_request_digest(request)
    ):
        issues.append(
            "apoptosis_independent_authorization_request_digest_mismatch"
        )
    return tuple(issues)


def _source_valid(
    xreq,
    xev,
    xpol,
    xrec,
    qreq,
    qev,
    qpol,
    qrec,
    areq,
    aev,
    apol,
    arec,
    dreq,
    dev,
    dpol,
    drec,
    oin,
    opol,
    orec,
    creq,
    cpol,
    crec,
) -> bool:
    return not (
        apoptosis_external_review_request_issues(xreq)
        or apoptosis_external_review_evidence_issues(xev)
        or apoptosis_external_review_policy_issues(xpol)
        or apoptosis_external_review_record_issues(
            xrec,
            xreq,
            xev,
            xpol,
            qreq,
            qev,
            qpol,
            qrec,
            areq,
            aev,
            apol,
            arec,
            dreq,
            dev,
            dpol,
            drec,
            oin,
            opol,
            orec,
            creq,
            cpol,
            crec,
        )
    )


def _artifact_binding(
    evidence,
    xreq,
    xev,
    xpol,
    xrec,
    qreq,
    qev,
    qpol,
    qrec,
    areq,
    aev,
    apol,
    arec,
    dreq,
    dev,
    dpol,
    drec,
    oin,
    opol,
    orec,
    creq,
    cpol,
    crec,
) -> bool:
    pairs = (
        (evidence.source_observation_input_digest, oin.input_digest),
        (evidence.source_observation_policy_digest, opol.policy_digest),
        (evidence.source_observation_record_digest, orec.record_digest),
        (evidence.source_candidate_request_digest, creq.request_digest),
        (evidence.source_candidate_policy_digest, cpol.policy_digest),
        (evidence.source_candidate_record_digest, crec.candidate_digest),
        (evidence.source_dependency_evidence_digest, dev.evidence_digest),
        (
            evidence.source_dependency_review_request_digest,
            dreq.request_digest,
        ),
        (evidence.source_dependency_review_policy_digest, dpol.policy_digest),
        (evidence.source_dependency_review_record_digest, drec.record_digest),
        (evidence.source_authority_evidence_digest, aev.evidence_digest),
        (evidence.source_authority_review_request_digest, areq.request_digest),
        (evidence.source_authority_review_policy_digest, apol.policy_digest),
        (evidence.source_authority_review_record_digest, arec.record_digest),
        (evidence.source_quiescence_evidence_digest, qev.evidence_digest),
        (
            evidence.source_quiescence_review_request_digest,
            qreq.request_digest,
        ),
        (evidence.source_quiescence_review_policy_digest, qpol.policy_digest),
        (evidence.source_quiescence_review_record_digest, qrec.record_digest),
        (evidence.source_external_review_evidence_digest, xev.evidence_digest),
        (evidence.source_external_review_request_digest, xreq.request_digest),
        (evidence.source_external_review_policy_digest, xpol.policy_digest),
        (evidence.source_external_review_record_digest, xrec.record_digest),
    )
    return all(left == right for left, right in pairs)


def construct_apoptosis_independent_authorization(
    request: ApoptosisIndependentAuthorizationRequest,
    evidence: ApoptosisIndependentAuthorizationEvidence,
    policy: ApoptosisIndependentAuthorizationPolicy,
    xreq: ApoptosisExternalReviewRequest,
    xev: ApoptosisExternalReviewEvidence,
    xpol: ApoptosisExternalReviewPolicy,
    xrec: ApoptosisExternalReviewRecord,
    qreq: ApoptosisQuiescenceReviewRequest,
    qev: ApoptosisQuiescenceEvidence,
    qpol: ApoptosisQuiescenceReviewPolicy,
    qrec: ApoptosisQuiescenceReviewRecord,
    areq: ApoptosisAuthorityReviewRequest,
    aev: ApoptosisAuthorityEvidence,
    apol: ApoptosisAuthorityReviewPolicy,
    arec: ApoptosisAuthorityReviewRecord,
    dreq: ApoptosisDependencyReviewRequest,
    dev: ApoptosisDependencyEvidence,
    dpol: ApoptosisDependencyReviewPolicy,
    drec: ApoptosisDependencyReviewRecord,
    oin: ApoptosisObservationInput,
    opol: ApoptosisObservationPolicy,
    orec: ApoptosisObservationRecord,
    creq: ApoptosisCandidateRequest,
    cpol: ApoptosisCandidatePolicy,
    crec: ApoptosisCandidateRecord,
) -> ApoptosisIndependentAuthorizationRecord:
    source_valid = _source_valid(
        xreq,
        xev,
        xpol,
        xrec,
        qreq,
        qev,
        qpol,
        qrec,
        areq,
        aev,
        apol,
        arec,
        dreq,
        dev,
        dpol,
        drec,
        oin,
        opol,
        orec,
        creq,
        cpol,
        crec,
    )
    source_clear = (
        xrec.status == EXTERNAL_REVIEW_CLEAR
        and xrec.external_review_record_issued
        and xrec.external_clear_for_independent_authorization
        and xrec.independent_authorization_required_next
    )
    subject_binding = (
        request.subject_id,
        request.subject_kind,
        request.subject_version,
    ) == (
        xrec.subject_id,
        xrec.subject_kind,
        xrec.subject_version,
    ) == (
        evidence.subject_id,
        evidence.subject_kind,
        evidence.subject_version,
    )
    artifact_binding = _artifact_binding(
        evidence,
        xreq,
        xev,
        xpol,
        xrec,
        qreq,
        qev,
        qpol,
        qrec,
        areq,
        aev,
        apol,
        arec,
        dreq,
        dev,
        dpol,
        drec,
        oin,
        opol,
        orec,
        creq,
        cpol,
        crec,
    )
    designation_binding = (
        request.authority_id == xrec.future_authorization_authority_id
        and evidence.authorization_authority_id
        == xrec.future_authorization_authority_id
    )
    identity_binding = (
        request.authorization_id == evidence.authorization_id
        and request.authority_id == evidence.authorization_authority_id
        and request.authority_organization_id
        == evidence.authorization_authority_organization_id
    )
    prior_ids = {
        request.subject_id,
        crec.issuer_id,
        drec.reviewer_id,
        arec.reviewer_id,
        aev.responsible_authority_id,
        qrec.reviewer_id,
        xrec.reviewer_id,
        xev.quiescence_evidence_producer_id,
    }
    prior_independent = request.authority_id not in prior_ids
    execution_independent = (
        request.authority_id != request.future_execution_authority_id
    )
    time_order = (
        evidence.authorization_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.authorization_completed_at_epoch_seconds
        == request.completed_at_epoch_seconds
    )
    delay = request.completed_at_epoch_seconds - xrec.completed_at_epoch_seconds
    age = request.completed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    delay_valid = 0 <= delay <= policy.max_authorization_delay_seconds
    evidence_fresh = 0 <= age <= policy.max_evidence_age_seconds
    not_expired = (
        request.completed_at_epoch_seconds
        <= evidence.authorization_expiry_at_epoch_seconds
    )
    checks = dict(
        policy_valid=not apoptosis_independent_authorization_policy_issues(
            policy
        ),
        request_valid=not apoptosis_independent_authorization_request_issues(
            request
        ),
        evidence_valid=not apoptosis_independent_authorization_evidence_issues(
            evidence
        ),
        source_recomputed_valid=source_valid,
        source_external_review_clear=source_clear,
        source_subject_binding_valid=subject_binding,
        source_artifact_binding_valid=artifact_binding,
        external_authority_designation_binding_valid=designation_binding,
        authority_allowed=request.authority_id in policy.allowed_authority_ids,
        authority_organization_allowed=(
            request.authority_organization_id
            in policy.allowed_authority_organization_ids
        ),
        authority_identity_binding_valid=identity_binding,
        authority_mandate_verified=evidence.authority_mandate_verified,
        authority_qualification_verified=(
            evidence.authority_qualification_verified
        ),
        authority_independence_declared=(
            evidence.authority_independence_declared
        ),
        authority_independent=prior_independent and execution_independent,
        independent_from_prior_chain=prior_independent,
        independent_from_future_execution_authority=execution_independent,
        objective_allowed=request.objective in policy.allowed_objectives,
        authorization_delay_valid=delay_valid,
        evidence_fresh=evidence_fresh,
        authorization_time_order_valid=time_order,
        authorization_not_expired=not_expired,
        conflict_disclosure_complete=evidence.conflict_disclosure_complete,
        material_conflict_present=evidence.material_conflict_present,
        jurisdiction_verified=evidence.jurisdiction_verified,
        quorum_satisfied=evidence.quorum_satisfied,
        reasoned_decision_complete=evidence.reasoned_decision_complete,
        proportionality_satisfied=evidence.proportionality_satisfied,
        less_restrictive_alternatives_exhausted=(
            evidence.less_restrictive_alternatives_exhausted
        ),
        irreversibility_review_complete=(
            evidence.irreversibility_review_complete
        ),
        human_impact_review_complete=evidence.human_impact_review_complete,
        appeal_route_available=evidence.appeal_route_available,
        dissent_route_available=evidence.dissent_route_available,
        protected_core_excluded=evidence.protected_core_excluded,
        institutional_hold_active=evidence.institutional_hold_active,
        emergency_state_active=evidence.emergency_state_active,
    )
    structural = (
        "policy_valid",
        "request_valid",
        "evidence_valid",
        "source_recomputed_valid",
        "source_external_review_clear",
        "source_subject_binding_valid",
        "source_artifact_binding_valid",
        "external_authority_designation_binding_valid",
        "authority_allowed",
        "authority_organization_allowed",
        "authority_identity_binding_valid",
        "authority_independent",
        "independent_from_prior_chain",
        "independent_from_future_execution_authority",
        "objective_allowed",
        "authorization_delay_valid",
        "evidence_fresh",
        "authorization_time_order_valid",
        "authorization_not_expired",
    )
    if not all(checks[name] for name in structural):
        status = INDEPENDENT_AUTHORIZATION_REJECTED
        reason = "independent_authorization_source_request_policy_or_binding_invalid"
    else:
        denials = (
            (evidence.emergency_state_active, "emergency_state_active"),
            (evidence.institutional_hold_active, "institutional_hold_active"),
            (not evidence.protected_core_excluded, "protected_core_not_excluded"),
            (not evidence.authority_mandate_verified, "authority_mandate_not_verified"),
            (
                not evidence.authority_qualification_verified,
                "authority_qualification_not_verified",
            ),
            (
                not evidence.authority_independence_declared,
                "authority_independence_not_declared",
            ),
            (
                not evidence.conflict_disclosure_complete,
                "conflict_disclosure_incomplete",
            ),
            (evidence.material_conflict_present, "material_conflict_present"),
            (not evidence.jurisdiction_verified, "jurisdiction_not_verified"),
            (not evidence.quorum_satisfied, "quorum_not_satisfied"),
            (
                not evidence.reasoned_decision_complete,
                "reasoned_decision_incomplete",
            ),
            (
                not evidence.proportionality_satisfied,
                "proportionality_not_satisfied",
            ),
            (
                not evidence.less_restrictive_alternatives_exhausted,
                "less_restrictive_alternatives_not_exhausted",
            ),
            (
                not evidence.irreversibility_review_complete,
                "irreversibility_review_incomplete",
            ),
            (
                not evidence.human_impact_review_complete,
                "human_impact_review_incomplete",
            ),
            (not evidence.appeal_route_available, "appeal_route_missing"),
            (not evidence.dissent_route_available, "dissent_route_missing"),
        )
        hit = next((reason for condition, reason in denials if condition), None)
        if hit is None:
            status = INDEPENDENT_AUTHORIZATION_APPROVED
            reason = "independent_authorization_approved_for_bounded_execution_preparation_only"
        else:
            status = INDEPENDENT_AUTHORIZATION_DENIED
            reason = hit
    issued = status != INDEPENDENT_AUTHORIZATION_REJECTED
    decision = status in (
        INDEPENDENT_AUTHORIZATION_APPROVED,
        INDEPENDENT_AUTHORIZATION_DENIED,
    )
    approved = status == INDEPENDENT_AUTHORIZATION_APPROVED
    denied = status == INDEPENDENT_AUTHORIZATION_DENIED
    checks.update(
        authorization_record_issued=issued,
        authorization_decision_made=decision,
        authorization_approved=approved,
        authorization_denied=denied,
        bounded_execution_preparation_allowed_next=approved,
        execution_authority_required_next=approved,
        **{name: False for name in _EFFECT_RECORD},
    )
    values = dict(
        authorization_id=request.authorization_id,
        status=status,
        reason=reason,
        policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        authorization_evidence_digest=evidence.evidence_digest,
        source_external_review_id=request.source_external_review_id,
        source_external_review_record_digest=(
            request.source_external_review_record_digest
        ),
        subject_id=request.subject_id,
        subject_kind=request.subject_kind,
        subject_version=request.subject_version,
        authority_id=request.authority_id,
        authority_organization_id=request.authority_organization_id,
        objective=request.objective,
        requested_at_epoch_seconds=request.requested_at_epoch_seconds,
        completed_at_epoch_seconds=request.completed_at_epoch_seconds,
        future_execution_authority_id=request.future_execution_authority_id,
        checks=checks,
        evidence_digests={
            "independent_authorization_policy": policy.policy_digest,
            "independent_authorization_request": request.request_digest,
            "independent_authorization_evidence": evidence.evidence_digest,
            "source_external_review_record": xrec.record_digest,
            "source_external_review_request": xreq.request_digest,
            "source_external_review_evidence": xev.evidence_digest,
            "source_quiescence_review_record": qrec.record_digest,
            "source_authority_review_record": arec.record_digest,
            "source_dependency_review_record": drec.record_digest,
            "source_candidate_record": crec.candidate_digest,
            "source_observation_record": orec.record_digest,
        },
        record_digest="",
    )
    for name in (
        item.name for item in fields(ApoptosisIndependentAuthorizationRecord)
    ):
        if name not in values and name not in {"version", "record_digest"}:
            values[name] = checks[name]
    record = ApoptosisIndependentAuthorizationRecord(**values)
    return replace(
        record,
        record_digest=apoptosis_independent_authorization_record_digest(record),
    )


def authorize_apoptosis_independently(
    *args,
    **kwargs,
) -> ApoptosisIndependentAuthorizationRecord:
    record = construct_apoptosis_independent_authorization(*args, **kwargs)
    issues = apoptosis_independent_authorization_record_issues(
        record,
        *args,
        **kwargs,
    )
    if issues:
        raise ValueError(
            f"apoptosis_independent_authorization_record_invalid:{issues[0]}"
        )
    return record


def apoptosis_independent_authorization_record_issues(
    record: ApoptosisIndependentAuthorizationRecord,
    *args,
    **kwargs,
) -> tuple[str, ...]:
    expected = construct_apoptosis_independent_authorization(*args, **kwargs)
    issues: list[str] = []
    if record.to_dict() != expected.to_dict():
        issues.append(
            "apoptosis_independent_authorization_recomputation_mismatch"
        )
    if record.status not in (
        INDEPENDENT_AUTHORIZATION_APPROVED,
        INDEPENDENT_AUTHORIZATION_DENIED,
        INDEPENDENT_AUTHORIZATION_REJECTED,
    ):
        issues.append("apoptosis_independent_authorization_status_invalid")
    if record.status == INDEPENDENT_AUTHORIZATION_APPROVED:
        if not (
            record.authorization_record_issued
            and record.authorization_decision_made
            and record.authorization_approved
            and not record.authorization_denied
            and record.bounded_execution_preparation_allowed_next
            and record.execution_authority_required_next
        ):
            issues.append(
                "apoptosis_independent_authorization_approved_gate_invalid"
            )
    if record.status == INDEPENDENT_AUTHORIZATION_DENIED:
        if not (
            record.authorization_record_issued
            and record.authorization_decision_made
            and not record.authorization_approved
            and record.authorization_denied
            and not record.bounded_execution_preparation_allowed_next
            and not record.execution_authority_required_next
        ):
            issues.append(
                "apoptosis_independent_authorization_denied_advanced"
            )
    if record.status == INDEPENDENT_AUTHORIZATION_REJECTED:
        if (
            record.authorization_record_issued
            or record.authorization_decision_made
            or record.authorization_approved
            or record.authorization_denied
            or record.bounded_execution_preparation_allowed_next
            or record.execution_authority_required_next
        ):
            issues.append(
                "apoptosis_independent_authorization_rejected_record_issued"
            )
    if any(getattr(record, name) for name in _EFFECT_RECORD):
        issues.append(
            "apoptosis_independent_authorization_execution_effect_performed"
        )
    if (
        record.record_digest
        != apoptosis_independent_authorization_record_digest(record)
    ):
        issues.append(
            "apoptosis_independent_authorization_record_digest_mismatch"
        )
    return tuple(issues)


__all__ = [
    "build_apoptosis_independent_authorization_policy",
    "apoptosis_independent_authorization_policy_issues",
    "build_apoptosis_independent_authorization_evidence",
    "apoptosis_independent_authorization_evidence_issues",
    "build_apoptosis_independent_authorization_request",
    "apoptosis_independent_authorization_request_issues",
    "construct_apoptosis_independent_authorization",
    "authorize_apoptosis_independently",
    "apoptosis_independent_authorization_record_issues",
]
