#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_apoptosis_candidate_types_v0_2 import (
    CANDIDATE_PROPOSED,
    CANDIDATE_REJECTED,
    OBJECTIVE_GOVERNED_EVALUATION_ONLY,
    ApoptosisCandidatePolicy,
    ApoptosisCandidateRecord,
    ApoptosisCandidateRequest,
    apoptosis_candidate_policy_digest,
    apoptosis_candidate_record_digest,
    apoptosis_candidate_request_digest,
)
from runtime.kuuos_apoptosis_observation_types_v0_1 import (
    OBSERVATION_REVIEW_RECOMMENDED,
    ApoptosisObservationInput,
    ApoptosisObservationPolicy,
    ApoptosisObservationRecord,
)
from runtime.kuuos_apoptosis_observation_v0_1 import (
    apoptosis_observation_input_issues,
    apoptosis_observation_policy_issues,
    apoptosis_observation_record_issues,
)
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def apoptosis_candidate_rationale_digest(
    record: ApoptosisObservationRecord,
) -> str:
    return canonical_digest(
        {
            "source_observation_id": record.observation_id,
            "source_record_digest": record.record_digest,
            "replacement_signal": record.replacement_signal,
            "repeated_failure_signal": record.repeated_failure_signal,
            "inactivity_signal": record.inactivity_signal,
            "unresolved_incident_signal": record.unresolved_incident_signal,
            "degradation_signal_present": record.degradation_signal_present,
            "active_dependencies_present": record.active_dependencies_present,
            "active_authorities_present": record.active_authorities_present,
            "active_executions_present": record.active_executions_present,
        }
    )


def build_apoptosis_candidate_policy(
    policy_id: str,
    *,
    allowed_issuer_ids: tuple[str, ...],
    allowed_objectives: tuple[str, ...] = (OBJECTIVE_GOVERNED_EVALUATION_ONLY,),
    max_candidate_delay_seconds: int = 86_400,
) -> ApoptosisCandidatePolicy:
    policy = ApoptosisCandidatePolicy(
        policy_id=policy_id,
        allowed_issuer_ids=_canonical(allowed_issuer_ids),
        allowed_objectives=_canonical(allowed_objectives),
        max_candidate_delay_seconds=max_candidate_delay_seconds,
        require_source_recomputation=True,
        require_review_recommended_source=True,
        require_source_non_protected=True,
        require_source_no_hold=True,
        require_provenance_binding=True,
        require_dependency_binding=True,
        require_authority_binding=True,
        require_independent_dependency_review=True,
        require_independent_authority_review=True,
        require_independent_quiescence_review=True,
        require_external_review=True,
        require_independent_authorization=True,
        allow_candidate_artifact_issuance=True,
        allow_authority_revocation=False,
        allow_quiescence_transition=False,
        allow_terminal_transition=False,
        allow_tombstone_write=False,
        allow_physical_deletion=False,
        allow_live_git_execution=False,
        allow_repository_mutation=False,
        policy_digest="",
    )
    policy = replace(policy, policy_digest=apoptosis_candidate_policy_digest(policy))
    issues = apoptosis_candidate_policy_issues(policy)
    if issues:
        raise ValueError(f"apoptosis_candidate_policy_invalid:{issues[0]}")
    return policy


def apoptosis_candidate_policy_issues(
    policy: ApoptosisCandidatePolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("apoptosis_candidate_policy_id_missing")
    if policy.allowed_issuer_ids != _canonical(policy.allowed_issuer_ids):
        issues.append("apoptosis_candidate_issuer_ids_not_canonical")
    if not policy.allowed_issuer_ids:
        issues.append("apoptosis_candidate_issuer_ids_empty")
    if policy.allowed_objectives != _canonical(policy.allowed_objectives):
        issues.append("apoptosis_candidate_objectives_not_canonical")
    if policy.allowed_objectives != (OBJECTIVE_GOVERNED_EVALUATION_ONLY,):
        issues.append("apoptosis_candidate_objective_scope_invalid")
    if policy.max_candidate_delay_seconds <= 0:
        issues.append("apoptosis_candidate_delay_bound_invalid")
    if not all(
        (
            policy.require_source_recomputation,
            policy.require_review_recommended_source,
            policy.require_source_non_protected,
            policy.require_source_no_hold,
            policy.require_provenance_binding,
            policy.require_dependency_binding,
            policy.require_authority_binding,
            policy.require_independent_dependency_review,
            policy.require_independent_authority_review,
            policy.require_independent_quiescence_review,
            policy.require_external_review,
            policy.require_independent_authorization,
            policy.allow_candidate_artifact_issuance,
        )
    ):
        issues.append("apoptosis_candidate_required_guard_disabled")
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
        issues.append("apoptosis_candidate_execution_effect_enabled")
    if policy.policy_digest != apoptosis_candidate_policy_digest(policy):
        issues.append("apoptosis_candidate_policy_digest_mismatch")
    return tuple(issues)


def build_apoptosis_candidate_request(
    candidate_id: str,
    issuer_id: str,
    issued_at_epoch_seconds: int,
    source_input: ApoptosisObservationInput,
    source_policy: ApoptosisObservationPolicy,
    source_record: ApoptosisObservationRecord,
    *,
    objective: str = OBJECTIVE_GOVERNED_EVALUATION_ONLY,
) -> ApoptosisCandidateRequest:
    request = ApoptosisCandidateRequest(
        candidate_id=candidate_id,
        issuer_id=issuer_id,
        objective=objective,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        source_observation_id=source_record.observation_id,
        source_observation_record_digest=source_record.record_digest,
        source_observation_input_digest=source_input.input_digest,
        source_observation_policy_digest=source_policy.policy_digest,
        subject_id=source_input.subject_id,
        subject_kind=source_input.subject_kind,
        subject_version=source_input.subject_version,
        provenance_digest=source_input.provenance_digest,
        dependency_snapshot_digest=source_input.dependency_snapshot_digest,
        authority_snapshot_digest=source_input.authority_snapshot_digest,
        rationale_digest=apoptosis_candidate_rationale_digest(source_record),
        request_digest="",
    )
    request = replace(
        request,
        request_digest=apoptosis_candidate_request_digest(request),
    )
    issues = apoptosis_candidate_request_issues(request)
    if issues:
        raise ValueError(f"apoptosis_candidate_request_invalid:{issues[0]}")
    return request


def apoptosis_candidate_request_issues(
    request: ApoptosisCandidateRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    for field_name in (
        "candidate_id",
        "issuer_id",
        "objective",
        "source_observation_id",
        "source_observation_record_digest",
        "source_observation_input_digest",
        "source_observation_policy_digest",
        "subject_id",
        "subject_kind",
        "subject_version",
        "provenance_digest",
        "dependency_snapshot_digest",
        "authority_snapshot_digest",
        "rationale_digest",
    ):
        if not getattr(request, field_name):
            issues.append(f"apoptosis_candidate_{field_name}_missing")
    if request.issued_at_epoch_seconds < 0:
        issues.append("apoptosis_candidate_issued_at_invalid")
    if request.request_digest != apoptosis_candidate_request_digest(request):
        issues.append("apoptosis_candidate_request_digest_mismatch")
    return tuple(issues)


def construct_apoptosis_candidate(
    request: ApoptosisCandidateRequest,
    source_input: ApoptosisObservationInput,
    source_policy: ApoptosisObservationPolicy,
    source_record: ApoptosisObservationRecord,
    candidate_policy: ApoptosisCandidatePolicy,
) -> ApoptosisCandidateRecord:
    policy_valid = not apoptosis_candidate_policy_issues(candidate_policy)
    request_valid = not apoptosis_candidate_request_issues(request)
    source_recomputed_valid = not (
        apoptosis_observation_policy_issues(source_policy)
        or apoptosis_observation_input_issues(source_input)
        or apoptosis_observation_record_issues(
            source_record,
            source_input,
            source_policy,
        )
    )
    source_review_recommended = (
        source_record.status == OBSERVATION_REVIEW_RECOMMENDED
        and source_record.degradation_signal_present
        and source_record.independent_candidate_stage_required
    )
    source_non_protected = not source_record.protected_subject
    source_no_hold = not source_record.institutional_hold_present
    source_subject_binding_valid = all(
        (
            request.source_observation_id == source_record.observation_id,
            request.subject_id == source_input.subject_id == source_record.subject_id,
            request.subject_kind == source_input.subject_kind == source_record.subject_kind,
            request.subject_version
            == source_input.subject_version
            == source_record.subject_version,
            request.source_observation_record_digest == source_record.record_digest,
            request.source_observation_input_digest == source_input.input_digest,
            request.source_observation_policy_digest == source_policy.policy_digest,
        )
    )
    source_provenance_binding_valid = (
        request.provenance_digest == source_input.provenance_digest
    )
    source_dependency_binding_valid = (
        request.dependency_snapshot_digest == source_input.dependency_snapshot_digest
    )
    source_authority_binding_valid = (
        request.authority_snapshot_digest == source_input.authority_snapshot_digest
    )
    source_rationale_binding_valid = (
        request.rationale_digest == apoptosis_candidate_rationale_digest(source_record)
    )
    issuer_allowed = request.issuer_id in candidate_policy.allowed_issuer_ids
    objective_allowed = request.objective in candidate_policy.allowed_objectives
    delay = request.issued_at_epoch_seconds - source_record.observed_at_epoch_seconds
    candidate_delay_valid = 0 <= delay <= candidate_policy.max_candidate_delay_seconds

    accepted = all(
        (
            policy_valid,
            request_valid,
            source_recomputed_valid,
            source_review_recommended,
            source_non_protected,
            source_no_hold,
            source_subject_binding_valid,
            source_provenance_binding_valid,
            source_dependency_binding_valid,
            source_authority_binding_valid,
            source_rationale_binding_valid,
            issuer_allowed,
            objective_allowed,
            candidate_delay_valid,
        )
    )
    status = CANDIDATE_PROPOSED if accepted else CANDIDATE_REJECTED
    reason = (
        "candidate_artifact_requires_independent_reviews_and_authorization"
        if accepted
        else "candidate_source_request_or_policy_invalid"
    )

    checks = {
        "policy_valid": policy_valid,
        "request_valid": request_valid,
        "source_recomputed_valid": source_recomputed_valid,
        "source_review_recommended": source_review_recommended,
        "source_non_protected": source_non_protected,
        "source_no_hold": source_no_hold,
        "source_subject_binding_valid": source_subject_binding_valid,
        "source_provenance_binding_valid": source_provenance_binding_valid,
        "source_dependency_binding_valid": source_dependency_binding_valid,
        "source_authority_binding_valid": source_authority_binding_valid,
        "source_rationale_binding_valid": source_rationale_binding_valid,
        "issuer_allowed": issuer_allowed,
        "objective_allowed": objective_allowed,
        "candidate_delay_valid": candidate_delay_valid,
        "dependency_review_required": accepted,
        "authority_review_required": accepted,
        "quiescence_review_required": accepted,
        "external_review_required": accepted,
        "independent_authorization_required": accepted,
        "candidate_artifact_issued": accepted,
        "authority_revocation_performed": False,
        "quiescence_transition_performed": False,
        "terminal_transition_performed": False,
        "tombstone_write_performed": False,
        "physical_deletion_performed": False,
        "live_git_execution_performed": False,
        "repository_mutation_performed": False,
    }
    record = ApoptosisCandidateRecord(
        candidate_id=request.candidate_id,
        status=status,
        reason=reason,
        policy_digest=candidate_policy.policy_digest,
        request_digest=request.request_digest,
        source_observation_id=request.source_observation_id,
        source_observation_record_digest=request.source_observation_record_digest,
        source_observation_input_digest=request.source_observation_input_digest,
        source_observation_policy_digest=request.source_observation_policy_digest,
        subject_id=request.subject_id,
        subject_kind=request.subject_kind,
        subject_version=request.subject_version,
        issuer_id=request.issuer_id,
        objective=request.objective,
        issued_at_epoch_seconds=request.issued_at_epoch_seconds,
        source_recomputed_valid=source_recomputed_valid,
        source_review_recommended=source_review_recommended,
        source_non_protected=source_non_protected,
        source_no_hold=source_no_hold,
        source_subject_binding_valid=source_subject_binding_valid,
        source_provenance_binding_valid=source_provenance_binding_valid,
        source_dependency_binding_valid=source_dependency_binding_valid,
        source_authority_binding_valid=source_authority_binding_valid,
        source_rationale_binding_valid=source_rationale_binding_valid,
        issuer_allowed=issuer_allowed,
        objective_allowed=objective_allowed,
        candidate_delay_valid=candidate_delay_valid,
        dependency_review_required=accepted,
        authority_review_required=accepted,
        quiescence_review_required=accepted,
        external_review_required=accepted,
        independent_authorization_required=accepted,
        candidate_artifact_issued=accepted,
        authority_revocation_performed=False,
        quiescence_transition_performed=False,
        terminal_transition_performed=False,
        tombstone_write_performed=False,
        physical_deletion_performed=False,
        live_git_execution_performed=False,
        repository_mutation_performed=False,
        checks=checks,
        evidence_digests={
            "candidate_policy": candidate_policy.policy_digest,
            "candidate_request": request.request_digest,
            "source_observation_policy": source_policy.policy_digest,
            "source_observation_input": source_input.input_digest,
            "source_observation_record": source_record.record_digest,
            "provenance": request.provenance_digest,
            "dependency_snapshot": request.dependency_snapshot_digest,
            "authority_snapshot": request.authority_snapshot_digest,
            "rationale": request.rationale_digest,
        },
        candidate_digest="",
    )
    return replace(
        record,
        candidate_digest=apoptosis_candidate_record_digest(record),
    )


def issue_apoptosis_candidate(
    request: ApoptosisCandidateRequest,
    source_input: ApoptosisObservationInput,
    source_policy: ApoptosisObservationPolicy,
    source_record: ApoptosisObservationRecord,
    candidate_policy: ApoptosisCandidatePolicy,
) -> ApoptosisCandidateRecord:
    record = construct_apoptosis_candidate(
        request,
        source_input,
        source_policy,
        source_record,
        candidate_policy,
    )
    issues = apoptosis_candidate_record_issues(
        record,
        request,
        source_input,
        source_policy,
        source_record,
        candidate_policy,
    )
    if issues:
        raise ValueError(f"apoptosis_candidate_record_invalid:{issues[0]}")
    return record


def apoptosis_candidate_record_issues(
    record: ApoptosisCandidateRecord,
    request: ApoptosisCandidateRequest,
    source_input: ApoptosisObservationInput,
    source_policy: ApoptosisObservationPolicy,
    source_record: ApoptosisObservationRecord,
    candidate_policy: ApoptosisCandidatePolicy,
) -> tuple[str, ...]:
    expected = construct_apoptosis_candidate(
        request,
        source_input,
        source_policy,
        source_record,
        candidate_policy,
    )
    issues: list[str] = []
    if record.to_dict() != expected.to_dict():
        issues.append("apoptosis_candidate_recomputation_mismatch")
    if record.status not in (CANDIDATE_PROPOSED, CANDIDATE_REJECTED):
        issues.append("apoptosis_candidate_status_invalid")
    if record.status == CANDIDATE_PROPOSED:
        if not record.candidate_artifact_issued:
            issues.append("apoptosis_candidate_artifact_not_issued")
        if not all(
            (
                record.dependency_review_required,
                record.authority_review_required,
                record.quiescence_review_required,
                record.external_review_required,
                record.independent_authorization_required,
            )
        ):
            issues.append("apoptosis_candidate_review_gate_missing")
    if record.status == CANDIDATE_REJECTED and record.candidate_artifact_issued:
        issues.append("apoptosis_rejected_candidate_artifact_issued")
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
        issues.append("apoptosis_candidate_execution_effect_performed")
    if record.candidate_digest != apoptosis_candidate_record_digest(record):
        issues.append("apoptosis_candidate_digest_mismatch")
    return tuple(issues)


__all__ = [
    "apoptosis_candidate_rationale_digest",
    "build_apoptosis_candidate_policy",
    "apoptosis_candidate_policy_issues",
    "build_apoptosis_candidate_request",
    "apoptosis_candidate_request_issues",
    "construct_apoptosis_candidate",
    "issue_apoptosis_candidate",
    "apoptosis_candidate_record_issues",
]
