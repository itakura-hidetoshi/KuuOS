#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_apoptosis_authority_review_types_v0_4 import (
    AUTHORITY_REVIEW_BLOCKED,
    AUTHORITY_REVIEW_CLEAR,
    AUTHORITY_REVIEW_REJECTED,
    OBJECTIVE_AUTHORITY_SAFETY_ONLY,
    ApoptosisAuthorityEvidence,
    ApoptosisAuthorityReviewPolicy,
    ApoptosisAuthorityReviewRecord,
    ApoptosisAuthorityReviewRequest,
    apoptosis_authority_evidence_digest,
    apoptosis_authority_review_policy_digest,
    apoptosis_authority_review_record_digest,
    apoptosis_authority_review_request_digest,
)
from runtime.kuuos_apoptosis_candidate_types_v0_2 import (
    ApoptosisCandidatePolicy,
    ApoptosisCandidateRecord,
    ApoptosisCandidateRequest,
)
from runtime.kuuos_apoptosis_dependency_review_types_v0_3 import (
    DEPENDENCY_REVIEW_CLEAR,
    ApoptosisDependencyEvidence,
    ApoptosisDependencyReviewPolicy,
    ApoptosisDependencyReviewRecord,
    ApoptosisDependencyReviewRequest,
)
from runtime.kuuos_apoptosis_dependency_review_v0_3 import (
    apoptosis_dependency_evidence_issues,
    apoptosis_dependency_review_policy_issues,
    apoptosis_dependency_review_record_issues,
    apoptosis_dependency_review_request_issues,
)
from runtime.kuuos_apoptosis_observation_types_v0_1 import (
    ApoptosisObservationInput,
    ApoptosisObservationPolicy,
    ApoptosisObservationRecord,
)


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_apoptosis_authority_review_policy(
    policy_id: str,
    *,
    allowed_reviewer_ids: tuple[str, ...],
    allowed_objectives: tuple[str, ...] = (OBJECTIVE_AUTHORITY_SAFETY_ONLY,),
    max_review_delay_seconds: int = 86_400,
    max_evidence_age_seconds: int = 3_600,
) -> ApoptosisAuthorityReviewPolicy:
    policy = ApoptosisAuthorityReviewPolicy(
        policy_id=policy_id,
        allowed_reviewer_ids=_canonical(allowed_reviewer_ids),
        allowed_objectives=_canonical(allowed_objectives),
        max_review_delay_seconds=max_review_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        require_source_dependency_review_recomputation=True,
        require_clear_dependency_source=True,
        require_source_subject_binding=True,
        require_authority_snapshot_binding=True,
        require_complete_authority_closure=True,
        require_responsible_authority=True,
        require_responsibility_acknowledgement=True,
        require_independent_reviewer=True,
        require_no_subject_control_of_responsible_authority=True,
        require_no_institutional_hold=True,
        require_no_constitutional_protection=True,
        require_no_protected_authority=True,
        require_complete_delegation_chain=True,
        require_no_unresolved_authority=True,
        require_no_authority_cycle=True,
        require_no_emergency_override=True,
        require_quiescence_review_next=True,
        require_external_review_next=True,
        require_independent_authorization_next=True,
        allow_authority_review_record_issuance=True,
        allow_authority_revocation=False,
        allow_quiescence_transition=False,
        allow_terminal_transition=False,
        allow_tombstone_write=False,
        allow_physical_deletion=False,
        allow_live_git_execution=False,
        allow_repository_mutation=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=apoptosis_authority_review_policy_digest(policy),
    )
    issues = apoptosis_authority_review_policy_issues(policy)
    if issues:
        raise ValueError(f"apoptosis_authority_review_policy_invalid:{issues[0]}")
    return policy


def apoptosis_authority_review_policy_issues(
    policy: ApoptosisAuthorityReviewPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("apoptosis_authority_review_policy_id_missing")
    if policy.allowed_reviewer_ids != _canonical(policy.allowed_reviewer_ids):
        issues.append("apoptosis_authority_reviewer_ids_not_canonical")
    if not policy.allowed_reviewer_ids:
        issues.append("apoptosis_authority_reviewer_ids_empty")
    if policy.allowed_objectives != _canonical(policy.allowed_objectives):
        issues.append("apoptosis_authority_objectives_not_canonical")
    if policy.allowed_objectives != (OBJECTIVE_AUTHORITY_SAFETY_ONLY,):
        issues.append("apoptosis_authority_objective_scope_invalid")
    if policy.max_review_delay_seconds <= 0:
        issues.append("apoptosis_authority_review_delay_bound_invalid")
    if policy.max_evidence_age_seconds <= 0:
        issues.append("apoptosis_authority_evidence_age_bound_invalid")
    if not all(
        (
            policy.require_source_dependency_review_recomputation,
            policy.require_clear_dependency_source,
            policy.require_source_subject_binding,
            policy.require_authority_snapshot_binding,
            policy.require_complete_authority_closure,
            policy.require_responsible_authority,
            policy.require_responsibility_acknowledgement,
            policy.require_independent_reviewer,
            policy.require_no_subject_control_of_responsible_authority,
            policy.require_no_institutional_hold,
            policy.require_no_constitutional_protection,
            policy.require_no_protected_authority,
            policy.require_complete_delegation_chain,
            policy.require_no_unresolved_authority,
            policy.require_no_authority_cycle,
            policy.require_no_emergency_override,
            policy.require_quiescence_review_next,
            policy.require_external_review_next,
            policy.require_independent_authorization_next,
            policy.allow_authority_review_record_issuance,
        )
    ):
        issues.append("apoptosis_authority_required_guard_disabled")
    if any(
        (
            policy.allow_authority_revocation,
            policy.allow_quiescence_transition,
            policy.allow_terminal_transition,
            policy.allow_tombstone_write,
            policy.allow_physical_deletion,
            policy.allow_live_git_execution,
            policy.allow_repository_mutation,
        )
    ):
        issues.append("apoptosis_authority_execution_effect_enabled")
    if policy.policy_digest != apoptosis_authority_review_policy_digest(policy):
        issues.append("apoptosis_authority_review_policy_digest_mismatch")
    return tuple(issues)


def build_apoptosis_authority_evidence(
    evidence_id: str,
    subject_id: str,
    subject_kind: str,
    subject_version: str,
    *,
    captured_at_epoch_seconds: int,
    authority_snapshot_digest: str,
    authority_graph_snapshot_digest: str,
    responsible_authority_id: str,
    active_authority_ids: tuple[str, ...],
    delegation_chain_ids: tuple[str, ...],
    protected_authority_ids: tuple[str, ...],
    unresolved_authority_ids: tuple[str, ...],
    cycle_member_ids: tuple[str, ...],
    authority_closure_complete: bool,
    delegation_chain_complete: bool,
    responsibility_acknowledged: bool,
    subject_controls_responsible_authority: bool,
    institutional_hold: bool,
    constitutional_protected: bool,
    emergency_override_active: bool,
) -> ApoptosisAuthorityEvidence:
    evidence = ApoptosisAuthorityEvidence(
        evidence_id=evidence_id,
        subject_id=subject_id,
        subject_kind=subject_kind,
        subject_version=subject_version,
        captured_at_epoch_seconds=captured_at_epoch_seconds,
        authority_snapshot_digest=authority_snapshot_digest,
        authority_graph_snapshot_digest=authority_graph_snapshot_digest,
        responsible_authority_id=responsible_authority_id,
        active_authority_ids=_canonical(active_authority_ids),
        delegation_chain_ids=tuple(delegation_chain_ids),
        protected_authority_ids=_canonical(protected_authority_ids),
        unresolved_authority_ids=_canonical(unresolved_authority_ids),
        cycle_member_ids=_canonical(cycle_member_ids),
        authority_closure_complete=authority_closure_complete,
        delegation_chain_complete=delegation_chain_complete,
        responsibility_acknowledged=responsibility_acknowledged,
        subject_controls_responsible_authority=(
            subject_controls_responsible_authority
        ),
        institutional_hold=institutional_hold,
        constitutional_protected=constitutional_protected,
        emergency_override_active=emergency_override_active,
        evidence_digest="",
    )
    evidence = replace(
        evidence,
        evidence_digest=apoptosis_authority_evidence_digest(evidence),
    )
    issues = apoptosis_authority_evidence_issues(evidence)
    if issues:
        raise ValueError(f"apoptosis_authority_evidence_invalid:{issues[0]}")
    return evidence


def apoptosis_authority_evidence_issues(
    evidence: ApoptosisAuthorityEvidence,
) -> tuple[str, ...]:
    issues: list[str] = []
    for field_name in (
        "evidence_id",
        "subject_id",
        "subject_kind",
        "subject_version",
        "authority_snapshot_digest",
        "authority_graph_snapshot_digest",
    ):
        if not getattr(evidence, field_name):
            issues.append(f"apoptosis_authority_{field_name}_missing")
    if evidence.captured_at_epoch_seconds < 0:
        issues.append("apoptosis_authority_evidence_captured_at_invalid")
    for field_name in (
        "active_authority_ids",
        "protected_authority_ids",
        "unresolved_authority_ids",
        "cycle_member_ids",
    ):
        values = getattr(evidence, field_name)
        if values != _canonical(values):
            issues.append(f"apoptosis_authority_{field_name}_not_canonical")
        if any(not value for value in values):
            issues.append(f"apoptosis_authority_{field_name}_contains_empty")
    if any(not value for value in evidence.delegation_chain_ids):
        issues.append("apoptosis_authority_delegation_chain_contains_empty")
    if len(set(evidence.delegation_chain_ids)) != len(
        evidence.delegation_chain_ids
    ):
        issues.append("apoptosis_authority_delegation_chain_contains_duplicate")
    active = set(evidence.active_authority_ids)
    if evidence.responsible_authority_id and (
        evidence.responsible_authority_id not in active
    ):
        issues.append("apoptosis_authority_responsible_authority_not_active")
    if not set(evidence.delegation_chain_ids).issubset(active):
        issues.append("apoptosis_authority_delegation_chain_not_active")
    if not set(evidence.protected_authority_ids).issubset(active):
        issues.append("apoptosis_authority_protected_authority_not_active")
    if not set(evidence.unresolved_authority_ids).issubset(active):
        issues.append("apoptosis_authority_unresolved_authority_not_active")
    if not set(evidence.cycle_member_ids).issubset(active):
        issues.append("apoptosis_authority_cycle_member_not_active")
    if evidence.evidence_digest != apoptosis_authority_evidence_digest(evidence):
        issues.append("apoptosis_authority_evidence_digest_mismatch")
    return tuple(issues)


def build_apoptosis_authority_review_request(
    review_id: str,
    reviewer_id: str,
    reviewed_at_epoch_seconds: int,
    dependency_request: ApoptosisDependencyReviewRequest,
    dependency_policy: ApoptosisDependencyReviewPolicy,
    dependency_evidence: ApoptosisDependencyEvidence,
    dependency_record: ApoptosisDependencyReviewRecord,
    candidate_request: ApoptosisCandidateRequest,
    authority_evidence: ApoptosisAuthorityEvidence,
    *,
    objective: str = OBJECTIVE_AUTHORITY_SAFETY_ONLY,
) -> ApoptosisAuthorityReviewRequest:
    request = ApoptosisAuthorityReviewRequest(
        review_id=review_id,
        reviewer_id=reviewer_id,
        objective=objective,
        reviewed_at_epoch_seconds=reviewed_at_epoch_seconds,
        source_dependency_review_id=dependency_record.review_id,
        source_dependency_review_digest=dependency_record.record_digest,
        source_dependency_review_request_digest=dependency_request.request_digest,
        source_dependency_review_policy_digest=dependency_policy.policy_digest,
        source_dependency_evidence_digest=dependency_evidence.evidence_digest,
        subject_id=dependency_record.subject_id,
        subject_kind=dependency_record.subject_kind,
        subject_version=dependency_record.subject_version,
        authority_snapshot_digest=candidate_request.authority_snapshot_digest,
        authority_evidence_digest=authority_evidence.evidence_digest,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=apoptosis_authority_review_request_digest(request),
    )
    issues = apoptosis_authority_review_request_issues(request)
    if issues:
        raise ValueError(f"apoptosis_authority_review_request_invalid:{issues[0]}")
    return request


def apoptosis_authority_review_request_issues(
    request: ApoptosisAuthorityReviewRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    for field_name in (
        "review_id",
        "reviewer_id",
        "objective",
        "source_dependency_review_id",
        "source_dependency_review_digest",
        "source_dependency_review_request_digest",
        "source_dependency_review_policy_digest",
        "source_dependency_evidence_digest",
        "subject_id",
        "subject_kind",
        "subject_version",
        "authority_snapshot_digest",
        "authority_evidence_digest",
    ):
        if not getattr(request, field_name):
            issues.append(f"apoptosis_authority_{field_name}_missing")
    if request.reviewed_at_epoch_seconds < 0:
        issues.append("apoptosis_authority_reviewed_at_invalid")
    if request.request_digest != apoptosis_authority_review_request_digest(request):
        issues.append("apoptosis_authority_review_request_digest_mismatch")
    return tuple(issues)


def _source_dependency_review_valid(
    dependency_request: ApoptosisDependencyReviewRequest,
    dependency_evidence: ApoptosisDependencyEvidence,
    dependency_policy: ApoptosisDependencyReviewPolicy,
    dependency_record: ApoptosisDependencyReviewRecord,
    observation_input: ApoptosisObservationInput,
    observation_policy: ApoptosisObservationPolicy,
    observation_record: ApoptosisObservationRecord,
    candidate_request: ApoptosisCandidateRequest,
    candidate_policy: ApoptosisCandidatePolicy,
    candidate_record: ApoptosisCandidateRecord,
) -> bool:
    return not (
        apoptosis_dependency_review_request_issues(dependency_request)
        or apoptosis_dependency_evidence_issues(dependency_evidence)
        or apoptosis_dependency_review_policy_issues(dependency_policy)
        or apoptosis_dependency_review_record_issues(
            dependency_record,
            dependency_request,
            dependency_evidence,
            dependency_policy,
            observation_input,
            observation_policy,
            observation_record,
            candidate_request,
            candidate_policy,
            candidate_record,
        )
    )


def construct_apoptosis_authority_review(
    request: ApoptosisAuthorityReviewRequest,
    authority_evidence: ApoptosisAuthorityEvidence,
    authority_policy: ApoptosisAuthorityReviewPolicy,
    dependency_request: ApoptosisDependencyReviewRequest,
    dependency_evidence: ApoptosisDependencyEvidence,
    dependency_policy: ApoptosisDependencyReviewPolicy,
    dependency_record: ApoptosisDependencyReviewRecord,
    observation_input: ApoptosisObservationInput,
    observation_policy: ApoptosisObservationPolicy,
    observation_record: ApoptosisObservationRecord,
    candidate_request: ApoptosisCandidateRequest,
    candidate_policy: ApoptosisCandidatePolicy,
    candidate_record: ApoptosisCandidateRecord,
) -> ApoptosisAuthorityReviewRecord:
    policy_valid = not apoptosis_authority_review_policy_issues(authority_policy)
    request_valid = not apoptosis_authority_review_request_issues(request)
    evidence_valid = not apoptosis_authority_evidence_issues(authority_evidence)
    source_recomputed_valid = _source_dependency_review_valid(
        dependency_request,
        dependency_evidence,
        dependency_policy,
        dependency_record,
        observation_input,
        observation_policy,
        observation_record,
        candidate_request,
        candidate_policy,
        candidate_record,
    )
    source_dependency_clear = bool(
        dependency_record.status == DEPENDENCY_REVIEW_CLEAR
        and dependency_record.dependency_review_record_issued
        and dependency_record.dependency_clear_for_further_review
        and dependency_record.authority_review_required_next
    )
    source_subject_binding_valid = all(
        (
            request.subject_id == dependency_record.subject_id == candidate_record.subject_id,
            request.subject_kind == dependency_record.subject_kind == candidate_record.subject_kind,
            request.subject_version
            == dependency_record.subject_version
            == candidate_record.subject_version,
        )
    )
    source_authority_snapshot_binding_valid = all(
        (
            request.authority_snapshot_digest
            == candidate_request.authority_snapshot_digest,
            authority_evidence.authority_snapshot_digest
            == request.authority_snapshot_digest,
        )
    )
    source_dependency_review_binding_valid = all(
        (
            request.source_dependency_review_id == dependency_record.review_id,
            request.source_dependency_review_digest == dependency_record.record_digest,
            request.source_dependency_review_request_digest
            == dependency_request.request_digest,
            request.source_dependency_review_policy_digest
            == dependency_policy.policy_digest,
            request.source_dependency_evidence_digest
            == dependency_evidence.evidence_digest,
        )
    )
    reviewer_allowed = request.reviewer_id in authority_policy.allowed_reviewer_ids
    excluded_reviewer_ids = {
        request.subject_id,
        candidate_record.issuer_id,
        dependency_record.reviewer_id,
    }
    if authority_evidence.responsible_authority_id:
        excluded_reviewer_ids.add(authority_evidence.responsible_authority_id)
    reviewer_independent = request.reviewer_id not in excluded_reviewer_ids
    objective_allowed = request.objective in authority_policy.allowed_objectives
    review_delay = (
        request.reviewed_at_epoch_seconds
        - dependency_record.reviewed_at_epoch_seconds
    )
    review_delay_valid = (
        0 <= review_delay <= authority_policy.max_review_delay_seconds
    )
    evidence_age = (
        request.reviewed_at_epoch_seconds
        - authority_evidence.captured_at_epoch_seconds
    )
    evidence_fresh = (
        0 <= evidence_age <= authority_policy.max_evidence_age_seconds
    )
    evidence_subject_binding_valid = all(
        (
            authority_evidence.subject_id == request.subject_id,
            authority_evidence.subject_kind == request.subject_kind,
            authority_evidence.subject_version == request.subject_version,
        )
    )
    evidence_snapshot_binding_valid = all(
        (
            request.authority_evidence_digest == authority_evidence.evidence_digest,
            authority_evidence.authority_snapshot_digest
            == request.authority_snapshot_digest,
        )
    )
    responsible_authority_present = bool(
        authority_evidence.responsible_authority_id
        and authority_evidence.responsible_authority_id
        in set(authority_evidence.active_authority_ids)
    )
    protected_authority_present = bool(authority_evidence.protected_authority_ids)
    unresolved_authority_present = bool(
        authority_evidence.unresolved_authority_ids
    )
    authority_cycle_present = bool(authority_evidence.cycle_member_ids)

    base_valid = all(
        (
            policy_valid,
            request_valid,
            evidence_valid,
            source_recomputed_valid,
            source_dependency_clear,
            source_subject_binding_valid,
            source_authority_snapshot_binding_valid,
            source_dependency_review_binding_valid,
            reviewer_allowed,
            reviewer_independent,
            objective_allowed,
            review_delay_valid,
            evidence_fresh,
            evidence_subject_binding_valid,
            evidence_snapshot_binding_valid,
        )
    )
    authority_clear = all(
        (
            authority_evidence.authority_closure_complete,
            responsible_authority_present,
            authority_evidence.responsibility_acknowledged,
            authority_evidence.delegation_chain_complete,
            not authority_evidence.subject_controls_responsible_authority,
            not authority_evidence.institutional_hold,
            not authority_evidence.constitutional_protected,
            not protected_authority_present,
            not unresolved_authority_present,
            not authority_cycle_present,
            not authority_evidence.emergency_override_active,
        )
    )

    if not base_valid:
        status = AUTHORITY_REVIEW_REJECTED
        reason = "authority_review_source_request_policy_or_evidence_invalid"
    elif authority_evidence.institutional_hold:
        status = AUTHORITY_REVIEW_BLOCKED
        reason = "institutional_hold_present"
    elif authority_evidence.constitutional_protected:
        status = AUTHORITY_REVIEW_BLOCKED
        reason = "constitutional_protection_present"
    elif not authority_evidence.authority_closure_complete:
        status = AUTHORITY_REVIEW_BLOCKED
        reason = "authority_closure_incomplete"
    elif not responsible_authority_present:
        status = AUTHORITY_REVIEW_BLOCKED
        reason = "responsible_authority_absent"
    elif not authority_evidence.responsibility_acknowledged:
        status = AUTHORITY_REVIEW_BLOCKED
        reason = "responsibility_not_acknowledged"
    elif authority_evidence.subject_controls_responsible_authority:
        status = AUTHORITY_REVIEW_BLOCKED
        reason = "subject_controls_responsible_authority"
    elif not authority_evidence.delegation_chain_complete:
        status = AUTHORITY_REVIEW_BLOCKED
        reason = "delegation_chain_incomplete"
    elif protected_authority_present:
        status = AUTHORITY_REVIEW_BLOCKED
        reason = "protected_authority_present"
    elif unresolved_authority_present:
        status = AUTHORITY_REVIEW_BLOCKED
        reason = "unresolved_authority_present"
    elif authority_cycle_present:
        status = AUTHORITY_REVIEW_BLOCKED
        reason = "authority_cycle_present"
    elif authority_evidence.emergency_override_active:
        status = AUTHORITY_REVIEW_BLOCKED
        reason = "emergency_override_active"
    else:
        status = AUTHORITY_REVIEW_CLEAR
        reason = "authority_clear_for_quiescence_review_only"

    valid_review = status in (AUTHORITY_REVIEW_CLEAR, AUTHORITY_REVIEW_BLOCKED)
    clear = status == AUTHORITY_REVIEW_CLEAR
    checks = {
        "policy_valid": policy_valid,
        "request_valid": request_valid,
        "evidence_valid": evidence_valid,
        "source_recomputed_valid": source_recomputed_valid,
        "source_dependency_clear": source_dependency_clear,
        "source_subject_binding_valid": source_subject_binding_valid,
        "source_authority_snapshot_binding_valid": (
            source_authority_snapshot_binding_valid
        ),
        "source_dependency_review_binding_valid": (
            source_dependency_review_binding_valid
        ),
        "reviewer_allowed": reviewer_allowed,
        "reviewer_independent": reviewer_independent,
        "objective_allowed": objective_allowed,
        "review_delay_valid": review_delay_valid,
        "evidence_fresh": evidence_fresh,
        "evidence_subject_binding_valid": evidence_subject_binding_valid,
        "evidence_snapshot_binding_valid": evidence_snapshot_binding_valid,
        "authority_closure_complete": authority_evidence.authority_closure_complete,
        "responsible_authority_present": responsible_authority_present,
        "responsibility_acknowledged": authority_evidence.responsibility_acknowledged,
        "delegation_chain_complete": authority_evidence.delegation_chain_complete,
        "subject_controls_responsible_authority": (
            authority_evidence.subject_controls_responsible_authority
        ),
        "institutional_hold_present": authority_evidence.institutional_hold,
        "constitutional_protection_present": (
            authority_evidence.constitutional_protected
        ),
        "protected_authority_present": protected_authority_present,
        "unresolved_authority_present": unresolved_authority_present,
        "authority_cycle_present": authority_cycle_present,
        "emergency_override_active": authority_evidence.emergency_override_active,
        "authority_clear_for_quiescence_review": clear,
        "authority_review_record_issued": valid_review,
        "quiescence_review_required_next": clear,
        "external_review_required_next": clear,
        "independent_authorization_required_next": clear,
        "authority_revocation_performed": False,
        "quiescence_transition_performed": False,
        "terminal_transition_performed": False,
        "tombstone_write_performed": False,
        "physical_deletion_performed": False,
        "live_git_execution_performed": False,
        "repository_mutation_performed": False,
    }
    record = ApoptosisAuthorityReviewRecord(
        review_id=request.review_id,
        status=status,
        reason=reason,
        policy_digest=authority_policy.policy_digest,
        request_digest=request.request_digest,
        source_dependency_review_id=request.source_dependency_review_id,
        source_dependency_review_digest=request.source_dependency_review_digest,
        source_dependency_review_request_digest=(
            request.source_dependency_review_request_digest
        ),
        source_dependency_review_policy_digest=(
            request.source_dependency_review_policy_digest
        ),
        source_dependency_evidence_digest=(
            request.source_dependency_evidence_digest
        ),
        authority_evidence_digest=request.authority_evidence_digest,
        subject_id=request.subject_id,
        subject_kind=request.subject_kind,
        subject_version=request.subject_version,
        reviewer_id=request.reviewer_id,
        objective=request.objective,
        reviewed_at_epoch_seconds=request.reviewed_at_epoch_seconds,
        source_recomputed_valid=source_recomputed_valid,
        source_dependency_clear=source_dependency_clear,
        source_subject_binding_valid=source_subject_binding_valid,
        source_authority_snapshot_binding_valid=(
            source_authority_snapshot_binding_valid
        ),
        source_dependency_review_binding_valid=(
            source_dependency_review_binding_valid
        ),
        reviewer_allowed=reviewer_allowed,
        reviewer_independent=reviewer_independent,
        objective_allowed=objective_allowed,
        review_delay_valid=review_delay_valid,
        evidence_valid=evidence_valid,
        evidence_fresh=evidence_fresh,
        evidence_subject_binding_valid=evidence_subject_binding_valid,
        evidence_snapshot_binding_valid=evidence_snapshot_binding_valid,
        authority_closure_complete=authority_evidence.authority_closure_complete,
        responsible_authority_present=responsible_authority_present,
        responsibility_acknowledged=authority_evidence.responsibility_acknowledged,
        delegation_chain_complete=authority_evidence.delegation_chain_complete,
        subject_controls_responsible_authority=(
            authority_evidence.subject_controls_responsible_authority
        ),
        institutional_hold_present=authority_evidence.institutional_hold,
        constitutional_protection_present=(
            authority_evidence.constitutional_protected
        ),
        protected_authority_present=protected_authority_present,
        unresolved_authority_present=unresolved_authority_present,
        authority_cycle_present=authority_cycle_present,
        emergency_override_active=authority_evidence.emergency_override_active,
        authority_clear_for_quiescence_review=clear,
        authority_review_record_issued=valid_review,
        quiescence_review_required_next=clear,
        external_review_required_next=clear,
        independent_authorization_required_next=clear,
        authority_revocation_performed=False,
        quiescence_transition_performed=False,
        terminal_transition_performed=False,
        tombstone_write_performed=False,
        physical_deletion_performed=False,
        live_git_execution_performed=False,
        repository_mutation_performed=False,
        checks=checks,
        evidence_digests={
            "authority_review_policy": authority_policy.policy_digest,
            "authority_review_request": request.request_digest,
            "authority_evidence": authority_evidence.evidence_digest,
            "authority_snapshot": authority_evidence.authority_snapshot_digest,
            "authority_graph_snapshot": (
                authority_evidence.authority_graph_snapshot_digest
            ),
            "source_dependency_review_policy": dependency_policy.policy_digest,
            "source_dependency_review_request": dependency_request.request_digest,
            "source_dependency_evidence": dependency_evidence.evidence_digest,
            "source_dependency_review_record": dependency_record.record_digest,
            "source_candidate_policy": candidate_policy.policy_digest,
            "source_candidate_request": candidate_request.request_digest,
            "source_candidate_record": candidate_record.candidate_digest,
            "source_observation_policy": observation_policy.policy_digest,
            "source_observation_input": observation_input.input_digest,
            "source_observation_record": observation_record.record_digest,
        },
        record_digest="",
    )
    return replace(
        record,
        record_digest=apoptosis_authority_review_record_digest(record),
    )


def review_apoptosis_authority(
    request: ApoptosisAuthorityReviewRequest,
    authority_evidence: ApoptosisAuthorityEvidence,
    authority_policy: ApoptosisAuthorityReviewPolicy,
    dependency_request: ApoptosisDependencyReviewRequest,
    dependency_evidence: ApoptosisDependencyEvidence,
    dependency_policy: ApoptosisDependencyReviewPolicy,
    dependency_record: ApoptosisDependencyReviewRecord,
    observation_input: ApoptosisObservationInput,
    observation_policy: ApoptosisObservationPolicy,
    observation_record: ApoptosisObservationRecord,
    candidate_request: ApoptosisCandidateRequest,
    candidate_policy: ApoptosisCandidatePolicy,
    candidate_record: ApoptosisCandidateRecord,
) -> ApoptosisAuthorityReviewRecord:
    record = construct_apoptosis_authority_review(
        request,
        authority_evidence,
        authority_policy,
        dependency_request,
        dependency_evidence,
        dependency_policy,
        dependency_record,
        observation_input,
        observation_policy,
        observation_record,
        candidate_request,
        candidate_policy,
        candidate_record,
    )
    issues = apoptosis_authority_review_record_issues(
        record,
        request,
        authority_evidence,
        authority_policy,
        dependency_request,
        dependency_evidence,
        dependency_policy,
        dependency_record,
        observation_input,
        observation_policy,
        observation_record,
        candidate_request,
        candidate_policy,
        candidate_record,
    )
    if issues:
        raise ValueError(f"apoptosis_authority_review_record_invalid:{issues[0]}")
    return record


def apoptosis_authority_review_record_issues(
    record: ApoptosisAuthorityReviewRecord,
    request: ApoptosisAuthorityReviewRequest,
    authority_evidence: ApoptosisAuthorityEvidence,
    authority_policy: ApoptosisAuthorityReviewPolicy,
    dependency_request: ApoptosisDependencyReviewRequest,
    dependency_evidence: ApoptosisDependencyEvidence,
    dependency_policy: ApoptosisDependencyReviewPolicy,
    dependency_record: ApoptosisDependencyReviewRecord,
    observation_input: ApoptosisObservationInput,
    observation_policy: ApoptosisObservationPolicy,
    observation_record: ApoptosisObservationRecord,
    candidate_request: ApoptosisCandidateRequest,
    candidate_policy: ApoptosisCandidatePolicy,
    candidate_record: ApoptosisCandidateRecord,
) -> tuple[str, ...]:
    expected = construct_apoptosis_authority_review(
        request,
        authority_evidence,
        authority_policy,
        dependency_request,
        dependency_evidence,
        dependency_policy,
        dependency_record,
        observation_input,
        observation_policy,
        observation_record,
        candidate_request,
        candidate_policy,
        candidate_record,
    )
    issues: list[str] = []
    if record.to_dict() != expected.to_dict():
        issues.append("apoptosis_authority_review_recomputation_mismatch")
    if record.status not in (
        AUTHORITY_REVIEW_CLEAR,
        AUTHORITY_REVIEW_BLOCKED,
        AUTHORITY_REVIEW_REJECTED,
    ):
        issues.append("apoptosis_authority_review_status_invalid")
    if record.status == AUTHORITY_REVIEW_CLEAR:
        if not record.authority_review_record_issued:
            issues.append("apoptosis_authority_clear_record_not_issued")
        if not record.authority_clear_for_quiescence_review:
            issues.append("apoptosis_authority_clear_flag_missing")
        if not all(
            (
                record.quiescence_review_required_next,
                record.external_review_required_next,
                record.independent_authorization_required_next,
            )
        ):
            issues.append("apoptosis_authority_next_review_gate_missing")
    if record.status == AUTHORITY_REVIEW_BLOCKED:
        if not record.authority_review_record_issued:
            issues.append("apoptosis_authority_blocked_record_not_issued")
        if record.authority_clear_for_quiescence_review:
            issues.append("apoptosis_authority_blocked_marked_clear")
        if any(
            (
                record.quiescence_review_required_next,
                record.external_review_required_next,
                record.independent_authorization_required_next,
            )
        ):
            issues.append("apoptosis_authority_blocked_advanced")
    if record.status == AUTHORITY_REVIEW_REJECTED:
        if record.authority_review_record_issued:
            issues.append("apoptosis_authority_rejected_record_issued")
        if record.authority_clear_for_quiescence_review:
            issues.append("apoptosis_authority_rejected_marked_clear")
    if any(
        (
            record.authority_revocation_performed,
            record.quiescence_transition_performed,
            record.terminal_transition_performed,
            record.tombstone_write_performed,
            record.physical_deletion_performed,
            record.live_git_execution_performed,
            record.repository_mutation_performed,
        )
    ):
        issues.append("apoptosis_authority_execution_effect_performed")
    if record.record_digest != apoptosis_authority_review_record_digest(record):
        issues.append("apoptosis_authority_review_record_digest_mismatch")
    return tuple(issues)


__all__ = [
    "build_apoptosis_authority_review_policy",
    "apoptosis_authority_review_policy_issues",
    "build_apoptosis_authority_evidence",
    "apoptosis_authority_evidence_issues",
    "build_apoptosis_authority_review_request",
    "apoptosis_authority_review_request_issues",
    "construct_apoptosis_authority_review",
    "review_apoptosis_authority",
    "apoptosis_authority_review_record_issues",
]
