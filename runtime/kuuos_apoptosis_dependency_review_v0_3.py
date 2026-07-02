#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_apoptosis_candidate_types_v0_2 import (
    CANDIDATE_PROPOSED,
    ApoptosisCandidatePolicy,
    ApoptosisCandidateRecord,
    ApoptosisCandidateRequest,
)
from runtime.kuuos_apoptosis_candidate_v0_2 import (
    apoptosis_candidate_policy_issues,
    apoptosis_candidate_record_issues,
    apoptosis_candidate_request_issues,
)
from runtime.kuuos_apoptosis_dependency_review_types_v0_3 import (
    DEPENDENCY_REVIEW_BLOCKED,
    DEPENDENCY_REVIEW_CLEAR,
    DEPENDENCY_REVIEW_REJECTED,
    OBJECTIVE_DEPENDENCY_SAFETY_ONLY,
    ApoptosisDependencyEvidence,
    ApoptosisDependencyReviewPolicy,
    ApoptosisDependencyReviewRecord,
    ApoptosisDependencyReviewRequest,
    apoptosis_dependency_evidence_digest,
    apoptosis_dependency_review_policy_digest,
    apoptosis_dependency_review_record_digest,
    apoptosis_dependency_review_request_digest,
)
from runtime.kuuos_apoptosis_observation_types_v0_1 import (
    ApoptosisObservationInput,
    ApoptosisObservationPolicy,
    ApoptosisObservationRecord,
)
from runtime.kuuos_apoptosis_observation_v0_1 import (
    apoptosis_observation_input_issues,
    apoptosis_observation_policy_issues,
    apoptosis_observation_record_issues,
)


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_apoptosis_dependency_review_policy(
    policy_id: str,
    *,
    allowed_reviewer_ids: tuple[str, ...],
    allowed_objectives: tuple[str, ...] = (OBJECTIVE_DEPENDENCY_SAFETY_ONLY,),
    max_review_delay_seconds: int = 86_400,
    max_evidence_age_seconds: int = 3_600,
) -> ApoptosisDependencyReviewPolicy:
    policy = ApoptosisDependencyReviewPolicy(
        policy_id=policy_id,
        allowed_reviewer_ids=_canonical(allowed_reviewer_ids),
        allowed_objectives=_canonical(allowed_objectives),
        max_review_delay_seconds=max_review_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        require_source_candidate_recomputation=True,
        require_proposed_candidate=True,
        require_candidate_subject_binding=True,
        require_snapshot_binding=True,
        require_complete_closure=True,
        require_no_cycle_through_subject=True,
        require_no_orphaned_dependents=True,
        require_no_unresolved_dependencies=True,
        require_no_uncovered_critical_dependents=True,
        require_no_active_execution_dependence=True,
        require_replacement_coverage_for_dependents=True,
        require_authority_review_next=True,
        require_quiescence_review_next=True,
        require_external_review_next=True,
        require_independent_authorization_next=True,
        allow_dependency_review_record_issuance=True,
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
        policy_digest=apoptosis_dependency_review_policy_digest(policy),
    )
    issues = apoptosis_dependency_review_policy_issues(policy)
    if issues:
        raise ValueError(f"apoptosis_dependency_review_policy_invalid:{issues[0]}")
    return policy


def apoptosis_dependency_review_policy_issues(
    policy: ApoptosisDependencyReviewPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("apoptosis_dependency_review_policy_id_missing")
    if policy.allowed_reviewer_ids != _canonical(policy.allowed_reviewer_ids):
        issues.append("apoptosis_dependency_reviewer_ids_not_canonical")
    if not policy.allowed_reviewer_ids:
        issues.append("apoptosis_dependency_reviewer_ids_empty")
    if policy.allowed_objectives != _canonical(policy.allowed_objectives):
        issues.append("apoptosis_dependency_objectives_not_canonical")
    if policy.allowed_objectives != (OBJECTIVE_DEPENDENCY_SAFETY_ONLY,):
        issues.append("apoptosis_dependency_objective_scope_invalid")
    if policy.max_review_delay_seconds <= 0:
        issues.append("apoptosis_dependency_review_delay_bound_invalid")
    if policy.max_evidence_age_seconds <= 0:
        issues.append("apoptosis_dependency_evidence_age_bound_invalid")
    if not all(
        (
            policy.require_source_candidate_recomputation,
            policy.require_proposed_candidate,
            policy.require_candidate_subject_binding,
            policy.require_snapshot_binding,
            policy.require_complete_closure,
            policy.require_no_cycle_through_subject,
            policy.require_no_orphaned_dependents,
            policy.require_no_unresolved_dependencies,
            policy.require_no_uncovered_critical_dependents,
            policy.require_no_active_execution_dependence,
            policy.require_replacement_coverage_for_dependents,
            policy.require_authority_review_next,
            policy.require_quiescence_review_next,
            policy.require_external_review_next,
            policy.require_independent_authorization_next,
            policy.allow_dependency_review_record_issuance,
        )
    ):
        issues.append("apoptosis_dependency_required_guard_disabled")
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
        issues.append("apoptosis_dependency_execution_effect_enabled")
    if policy.policy_digest != apoptosis_dependency_review_policy_digest(policy):
        issues.append("apoptosis_dependency_review_policy_digest_mismatch")
    return tuple(issues)


def build_apoptosis_dependency_evidence(
    evidence_id: str,
    subject_id: str,
    subject_kind: str,
    subject_version: str,
    *,
    captured_at_epoch_seconds: int,
    dependency_snapshot_digest: str,
    graph_snapshot_digest: str,
    direct_dependency_ids: tuple[str, ...],
    direct_dependent_ids: tuple[str, ...],
    critical_dependent_ids: tuple[str, ...],
    replacement_covered_dependent_ids: tuple[str, ...],
    unresolved_dependency_ids: tuple[str, ...],
    cycle_member_ids: tuple[str, ...],
    active_execution_dependent_ids: tuple[str, ...],
    closure_complete: bool,
) -> ApoptosisDependencyEvidence:
    evidence = ApoptosisDependencyEvidence(
        evidence_id=evidence_id,
        subject_id=subject_id,
        subject_kind=subject_kind,
        subject_version=subject_version,
        captured_at_epoch_seconds=captured_at_epoch_seconds,
        dependency_snapshot_digest=dependency_snapshot_digest,
        graph_snapshot_digest=graph_snapshot_digest,
        direct_dependency_ids=_canonical(direct_dependency_ids),
        direct_dependent_ids=_canonical(direct_dependent_ids),
        critical_dependent_ids=_canonical(critical_dependent_ids),
        replacement_covered_dependent_ids=_canonical(
            replacement_covered_dependent_ids
        ),
        unresolved_dependency_ids=_canonical(unresolved_dependency_ids),
        cycle_member_ids=_canonical(cycle_member_ids),
        active_execution_dependent_ids=_canonical(
            active_execution_dependent_ids
        ),
        closure_complete=closure_complete,
        evidence_digest="",
    )
    evidence = replace(
        evidence,
        evidence_digest=apoptosis_dependency_evidence_digest(evidence),
    )
    issues = apoptosis_dependency_evidence_issues(evidence)
    if issues:
        raise ValueError(f"apoptosis_dependency_evidence_invalid:{issues[0]}")
    return evidence


def apoptosis_dependency_evidence_issues(
    evidence: ApoptosisDependencyEvidence,
) -> tuple[str, ...]:
    issues: list[str] = []
    for field_name in (
        "evidence_id",
        "subject_id",
        "subject_kind",
        "subject_version",
        "dependency_snapshot_digest",
        "graph_snapshot_digest",
    ):
        if not getattr(evidence, field_name):
            issues.append(f"apoptosis_dependency_{field_name}_missing")
    if evidence.captured_at_epoch_seconds < 0:
        issues.append("apoptosis_dependency_evidence_captured_at_invalid")
    tuple_fields = (
        "direct_dependency_ids",
        "direct_dependent_ids",
        "critical_dependent_ids",
        "replacement_covered_dependent_ids",
        "unresolved_dependency_ids",
        "cycle_member_ids",
        "active_execution_dependent_ids",
    )
    for field_name in tuple_fields:
        values = getattr(evidence, field_name)
        if values != _canonical(values):
            issues.append(f"apoptosis_dependency_{field_name}_not_canonical")
        if any(not value for value in values):
            issues.append(f"apoptosis_dependency_{field_name}_contains_empty")
    dependents = set(evidence.direct_dependent_ids)
    dependencies = set(evidence.direct_dependency_ids)
    if not set(evidence.critical_dependent_ids).issubset(dependents):
        issues.append("apoptosis_dependency_critical_dependents_not_direct")
    if not set(evidence.replacement_covered_dependent_ids).issubset(dependents):
        issues.append("apoptosis_dependency_replacement_coverage_not_direct")
    if not set(evidence.active_execution_dependent_ids).issubset(dependents):
        issues.append("apoptosis_dependency_active_execution_not_direct")
    if not set(evidence.unresolved_dependency_ids).issubset(dependencies):
        issues.append("apoptosis_dependency_unresolved_not_direct")
    if evidence.evidence_digest != apoptosis_dependency_evidence_digest(evidence):
        issues.append("apoptosis_dependency_evidence_digest_mismatch")
    return tuple(issues)


def build_apoptosis_dependency_review_request(
    review_id: str,
    reviewer_id: str,
    reviewed_at_epoch_seconds: int,
    candidate_request: ApoptosisCandidateRequest,
    candidate_policy: ApoptosisCandidatePolicy,
    candidate_record: ApoptosisCandidateRecord,
    evidence: ApoptosisDependencyEvidence,
    *,
    objective: str = OBJECTIVE_DEPENDENCY_SAFETY_ONLY,
) -> ApoptosisDependencyReviewRequest:
    request = ApoptosisDependencyReviewRequest(
        review_id=review_id,
        reviewer_id=reviewer_id,
        objective=objective,
        reviewed_at_epoch_seconds=reviewed_at_epoch_seconds,
        source_candidate_id=candidate_record.candidate_id,
        source_candidate_digest=candidate_record.candidate_digest,
        source_candidate_request_digest=candidate_request.request_digest,
        source_candidate_policy_digest=candidate_policy.policy_digest,
        subject_id=candidate_record.subject_id,
        subject_kind=candidate_record.subject_kind,
        subject_version=candidate_record.subject_version,
        dependency_snapshot_digest=candidate_request.dependency_snapshot_digest,
        dependency_evidence_digest=evidence.evidence_digest,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=apoptosis_dependency_review_request_digest(request),
    )
    issues = apoptosis_dependency_review_request_issues(request)
    if issues:
        raise ValueError(f"apoptosis_dependency_review_request_invalid:{issues[0]}")
    return request


def apoptosis_dependency_review_request_issues(
    request: ApoptosisDependencyReviewRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    for field_name in (
        "review_id",
        "reviewer_id",
        "objective",
        "source_candidate_id",
        "source_candidate_digest",
        "source_candidate_request_digest",
        "source_candidate_policy_digest",
        "subject_id",
        "subject_kind",
        "subject_version",
        "dependency_snapshot_digest",
        "dependency_evidence_digest",
    ):
        if not getattr(request, field_name):
            issues.append(f"apoptosis_dependency_{field_name}_missing")
    if request.reviewed_at_epoch_seconds < 0:
        issues.append("apoptosis_dependency_reviewed_at_invalid")
    if request.request_digest != apoptosis_dependency_review_request_digest(request):
        issues.append("apoptosis_dependency_review_request_digest_mismatch")
    return tuple(issues)


def _source_candidate_valid(
    observation_input: ApoptosisObservationInput,
    observation_policy: ApoptosisObservationPolicy,
    observation_record: ApoptosisObservationRecord,
    candidate_request: ApoptosisCandidateRequest,
    candidate_policy: ApoptosisCandidatePolicy,
    candidate_record: ApoptosisCandidateRecord,
) -> bool:
    return not (
        apoptosis_observation_input_issues(observation_input)
        or apoptosis_observation_policy_issues(observation_policy)
        or apoptosis_observation_record_issues(
            observation_record,
            observation_input,
            observation_policy,
        )
        or apoptosis_candidate_request_issues(candidate_request)
        or apoptosis_candidate_policy_issues(candidate_policy)
        or apoptosis_candidate_record_issues(
            candidate_record,
            candidate_request,
            observation_input,
            observation_policy,
            observation_record,
            candidate_policy,
        )
    )


def construct_apoptosis_dependency_review(
    request: ApoptosisDependencyReviewRequest,
    evidence: ApoptosisDependencyEvidence,
    review_policy: ApoptosisDependencyReviewPolicy,
    observation_input: ApoptosisObservationInput,
    observation_policy: ApoptosisObservationPolicy,
    observation_record: ApoptosisObservationRecord,
    candidate_request: ApoptosisCandidateRequest,
    candidate_policy: ApoptosisCandidatePolicy,
    candidate_record: ApoptosisCandidateRecord,
) -> ApoptosisDependencyReviewRecord:
    policy_valid = not apoptosis_dependency_review_policy_issues(review_policy)
    request_valid = not apoptosis_dependency_review_request_issues(request)
    evidence_valid = not apoptosis_dependency_evidence_issues(evidence)
    source_recomputed_valid = _source_candidate_valid(
        observation_input,
        observation_policy,
        observation_record,
        candidate_request,
        candidate_policy,
        candidate_record,
    )
    source_candidate_proposed = bool(
        candidate_record.status == CANDIDATE_PROPOSED
        and candidate_record.candidate_artifact_issued
        and candidate_record.dependency_review_required
    )
    source_subject_binding_valid = all(
        (
            request.subject_id
            == candidate_record.subject_id
            == candidate_request.subject_id,
            request.subject_kind
            == candidate_record.subject_kind
            == candidate_request.subject_kind,
            request.subject_version
            == candidate_record.subject_version
            == candidate_request.subject_version,
        )
    )
    source_dependency_snapshot_binding_valid = (
        request.dependency_snapshot_digest
        == candidate_request.dependency_snapshot_digest
        == evidence.dependency_snapshot_digest
    )
    source_candidate_binding_valid = all(
        (
            request.source_candidate_id == candidate_record.candidate_id,
            request.source_candidate_digest == candidate_record.candidate_digest,
            request.source_candidate_request_digest
            == candidate_request.request_digest,
            request.source_candidate_policy_digest == candidate_policy.policy_digest,
        )
    )
    reviewer_allowed = request.reviewer_id in review_policy.allowed_reviewer_ids
    objective_allowed = request.objective in review_policy.allowed_objectives
    review_delay = (
        request.reviewed_at_epoch_seconds
        - candidate_record.issued_at_epoch_seconds
    )
    review_delay_valid = (
        0 <= review_delay <= review_policy.max_review_delay_seconds
    )
    evidence_age = (
        request.reviewed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    )
    evidence_fresh = (
        0 <= evidence_age <= review_policy.max_evidence_age_seconds
    )
    evidence_subject_binding_valid = all(
        (
            evidence.subject_id == request.subject_id,
            evidence.subject_kind == request.subject_kind,
            evidence.subject_version == request.subject_version,
        )
    )
    evidence_snapshot_binding_valid = all(
        (
            request.dependency_evidence_digest == evidence.evidence_digest,
            evidence.dependency_snapshot_digest
            == request.dependency_snapshot_digest,
        )
    )

    dependents = set(evidence.direct_dependent_ids)
    replacement_covered = set(evidence.replacement_covered_dependent_ids)
    orphaned_dependents = dependents - replacement_covered
    uncovered_critical = (
        set(evidence.critical_dependent_ids) - replacement_covered
    )
    cycle_through_subject_present = bool(
        evidence.subject_id in set(evidence.cycle_member_ids)
        or evidence.subject_id in set(evidence.direct_dependency_ids)
        or evidence.subject_id in dependents
    )
    unresolved_dependencies_present = bool(evidence.unresolved_dependency_ids)
    orphaned_dependents_present = bool(orphaned_dependents)
    uncovered_critical_dependents_present = bool(uncovered_critical)
    active_execution_dependence_present = bool(
        evidence.active_execution_dependent_ids
    )
    replacement_coverage_complete = not orphaned_dependents_present

    base_valid = all(
        (
            policy_valid,
            request_valid,
            evidence_valid,
            source_recomputed_valid,
            source_candidate_proposed,
            source_subject_binding_valid,
            source_dependency_snapshot_binding_valid,
            source_candidate_binding_valid,
            reviewer_allowed,
            objective_allowed,
            review_delay_valid,
            evidence_fresh,
            evidence_subject_binding_valid,
            evidence_snapshot_binding_valid,
        )
    )
    dependency_clear = all(
        (
            evidence.closure_complete,
            not cycle_through_subject_present,
            not unresolved_dependencies_present,
            not orphaned_dependents_present,
            not uncovered_critical_dependents_present,
            not active_execution_dependence_present,
            replacement_coverage_complete,
        )
    )

    if not base_valid:
        status = DEPENDENCY_REVIEW_REJECTED
        reason = "dependency_review_source_request_policy_or_evidence_invalid"
    elif not evidence.closure_complete:
        status = DEPENDENCY_REVIEW_BLOCKED
        reason = "dependency_closure_incomplete"
    elif cycle_through_subject_present:
        status = DEPENDENCY_REVIEW_BLOCKED
        reason = "dependency_cycle_through_subject_present"
    elif unresolved_dependencies_present:
        status = DEPENDENCY_REVIEW_BLOCKED
        reason = "unresolved_dependencies_present"
    elif uncovered_critical_dependents_present:
        status = DEPENDENCY_REVIEW_BLOCKED
        reason = "critical_dependents_not_replacement_covered"
    elif active_execution_dependence_present:
        status = DEPENDENCY_REVIEW_BLOCKED
        reason = "active_execution_dependence_present"
    elif orphaned_dependents_present:
        status = DEPENDENCY_REVIEW_BLOCKED
        reason = "dependent_orphaning_risk_present"
    else:
        status = DEPENDENCY_REVIEW_CLEAR
        reason = "dependency_clear_for_further_review_only"

    valid_review = status in (DEPENDENCY_REVIEW_CLEAR, DEPENDENCY_REVIEW_BLOCKED)
    clear = status == DEPENDENCY_REVIEW_CLEAR
    checks = {
        "policy_valid": policy_valid,
        "request_valid": request_valid,
        "evidence_valid": evidence_valid,
        "source_recomputed_valid": source_recomputed_valid,
        "source_candidate_proposed": source_candidate_proposed,
        "source_subject_binding_valid": source_subject_binding_valid,
        "source_dependency_snapshot_binding_valid": (
            source_dependency_snapshot_binding_valid
        ),
        "source_candidate_binding_valid": source_candidate_binding_valid,
        "reviewer_allowed": reviewer_allowed,
        "objective_allowed": objective_allowed,
        "review_delay_valid": review_delay_valid,
        "evidence_fresh": evidence_fresh,
        "evidence_subject_binding_valid": evidence_subject_binding_valid,
        "evidence_snapshot_binding_valid": evidence_snapshot_binding_valid,
        "closure_complete": evidence.closure_complete,
        "cycle_through_subject_present": cycle_through_subject_present,
        "unresolved_dependencies_present": unresolved_dependencies_present,
        "orphaned_dependents_present": orphaned_dependents_present,
        "uncovered_critical_dependents_present": (
            uncovered_critical_dependents_present
        ),
        "active_execution_dependence_present": (
            active_execution_dependence_present
        ),
        "replacement_coverage_complete": replacement_coverage_complete,
        "dependency_clear_for_further_review": clear,
        "dependency_review_record_issued": valid_review,
        "authority_review_required_next": clear,
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
    record = ApoptosisDependencyReviewRecord(
        review_id=request.review_id,
        status=status,
        reason=reason,
        policy_digest=review_policy.policy_digest,
        request_digest=request.request_digest,
        source_candidate_id=request.source_candidate_id,
        source_candidate_digest=request.source_candidate_digest,
        source_candidate_request_digest=request.source_candidate_request_digest,
        source_candidate_policy_digest=request.source_candidate_policy_digest,
        dependency_evidence_digest=request.dependency_evidence_digest,
        subject_id=request.subject_id,
        subject_kind=request.subject_kind,
        subject_version=request.subject_version,
        reviewer_id=request.reviewer_id,
        objective=request.objective,
        reviewed_at_epoch_seconds=request.reviewed_at_epoch_seconds,
        source_recomputed_valid=source_recomputed_valid,
        source_candidate_proposed=source_candidate_proposed,
        source_subject_binding_valid=source_subject_binding_valid,
        source_dependency_snapshot_binding_valid=(
            source_dependency_snapshot_binding_valid
        ),
        source_candidate_binding_valid=source_candidate_binding_valid,
        reviewer_allowed=reviewer_allowed,
        objective_allowed=objective_allowed,
        review_delay_valid=review_delay_valid,
        evidence_valid=evidence_valid,
        evidence_fresh=evidence_fresh,
        evidence_subject_binding_valid=evidence_subject_binding_valid,
        evidence_snapshot_binding_valid=evidence_snapshot_binding_valid,
        closure_complete=evidence.closure_complete,
        cycle_through_subject_present=cycle_through_subject_present,
        unresolved_dependencies_present=unresolved_dependencies_present,
        orphaned_dependents_present=orphaned_dependents_present,
        uncovered_critical_dependents_present=(
            uncovered_critical_dependents_present
        ),
        active_execution_dependence_present=active_execution_dependence_present,
        replacement_coverage_complete=replacement_coverage_complete,
        dependency_clear_for_further_review=clear,
        dependency_review_record_issued=valid_review,
        authority_review_required_next=clear,
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
            "review_policy": review_policy.policy_digest,
            "review_request": request.request_digest,
            "dependency_evidence": evidence.evidence_digest,
            "dependency_snapshot": evidence.dependency_snapshot_digest,
            "dependency_graph_snapshot": evidence.graph_snapshot_digest,
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
        record_digest=apoptosis_dependency_review_record_digest(record),
    )


def review_apoptosis_dependencies(
    request: ApoptosisDependencyReviewRequest,
    evidence: ApoptosisDependencyEvidence,
    review_policy: ApoptosisDependencyReviewPolicy,
    observation_input: ApoptosisObservationInput,
    observation_policy: ApoptosisObservationPolicy,
    observation_record: ApoptosisObservationRecord,
    candidate_request: ApoptosisCandidateRequest,
    candidate_policy: ApoptosisCandidatePolicy,
    candidate_record: ApoptosisCandidateRecord,
) -> ApoptosisDependencyReviewRecord:
    record = construct_apoptosis_dependency_review(
        request,
        evidence,
        review_policy,
        observation_input,
        observation_policy,
        observation_record,
        candidate_request,
        candidate_policy,
        candidate_record,
    )
    issues = apoptosis_dependency_review_record_issues(
        record,
        request,
        evidence,
        review_policy,
        observation_input,
        observation_policy,
        observation_record,
        candidate_request,
        candidate_policy,
        candidate_record,
    )
    if issues:
        raise ValueError(f"apoptosis_dependency_review_record_invalid:{issues[0]}")
    return record


def apoptosis_dependency_review_record_issues(
    record: ApoptosisDependencyReviewRecord,
    request: ApoptosisDependencyReviewRequest,
    evidence: ApoptosisDependencyEvidence,
    review_policy: ApoptosisDependencyReviewPolicy,
    observation_input: ApoptosisObservationInput,
    observation_policy: ApoptosisObservationPolicy,
    observation_record: ApoptosisObservationRecord,
    candidate_request: ApoptosisCandidateRequest,
    candidate_policy: ApoptosisCandidatePolicy,
    candidate_record: ApoptosisCandidateRecord,
) -> tuple[str, ...]:
    expected = construct_apoptosis_dependency_review(
        request,
        evidence,
        review_policy,
        observation_input,
        observation_policy,
        observation_record,
        candidate_request,
        candidate_policy,
        candidate_record,
    )
    issues: list[str] = []
    if record.to_dict() != expected.to_dict():
        issues.append("apoptosis_dependency_review_recomputation_mismatch")
    if record.status not in (
        DEPENDENCY_REVIEW_CLEAR,
        DEPENDENCY_REVIEW_BLOCKED,
        DEPENDENCY_REVIEW_REJECTED,
    ):
        issues.append("apoptosis_dependency_review_status_invalid")
    if record.status == DEPENDENCY_REVIEW_CLEAR:
        if not record.dependency_review_record_issued:
            issues.append("apoptosis_dependency_clear_record_not_issued")
        if not record.dependency_clear_for_further_review:
            issues.append("apoptosis_dependency_clear_flag_missing")
        if not all(
            (
                record.authority_review_required_next,
                record.quiescence_review_required_next,
                record.external_review_required_next,
                record.independent_authorization_required_next,
            )
        ):
            issues.append("apoptosis_dependency_next_review_gate_missing")
    if record.status == DEPENDENCY_REVIEW_BLOCKED:
        if not record.dependency_review_record_issued:
            issues.append("apoptosis_dependency_blocked_record_not_issued")
        if record.dependency_clear_for_further_review:
            issues.append("apoptosis_dependency_blocked_marked_clear")
        if any(
            (
                record.authority_review_required_next,
                record.quiescence_review_required_next,
                record.external_review_required_next,
                record.independent_authorization_required_next,
            )
        ):
            issues.append("apoptosis_dependency_blocked_advanced")
    if record.status == DEPENDENCY_REVIEW_REJECTED:
        if record.dependency_review_record_issued:
            issues.append("apoptosis_dependency_rejected_record_issued")
        if record.dependency_clear_for_further_review:
            issues.append("apoptosis_dependency_rejected_marked_clear")
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
        issues.append("apoptosis_dependency_execution_effect_performed")
    if record.record_digest != apoptosis_dependency_review_record_digest(record):
        issues.append("apoptosis_dependency_review_record_digest_mismatch")
    return tuple(issues)


__all__ = [
    "build_apoptosis_dependency_review_policy",
    "apoptosis_dependency_review_policy_issues",
    "build_apoptosis_dependency_evidence",
    "apoptosis_dependency_evidence_issues",
    "build_apoptosis_dependency_review_request",
    "apoptosis_dependency_review_request_issues",
    "construct_apoptosis_dependency_review",
    "review_apoptosis_dependencies",
    "apoptosis_dependency_review_record_issues",
]
