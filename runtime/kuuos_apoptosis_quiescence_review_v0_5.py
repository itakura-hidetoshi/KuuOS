#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_apoptosis_authority_review_types_v0_4 import (
    AUTHORITY_REVIEW_CLEAR,
    ApoptosisAuthorityEvidence,
    ApoptosisAuthorityReviewPolicy,
    ApoptosisAuthorityReviewRecord,
    ApoptosisAuthorityReviewRequest,
)
from runtime.kuuos_apoptosis_authority_review_v0_4 import (
    apoptosis_authority_evidence_issues,
    apoptosis_authority_review_policy_issues,
    apoptosis_authority_review_record_issues,
    apoptosis_authority_review_request_issues,
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
from runtime.kuuos_apoptosis_observation_types_v0_1 import (
    ApoptosisObservationInput,
    ApoptosisObservationPolicy,
    ApoptosisObservationRecord,
)
from runtime.kuuos_apoptosis_quiescence_review_types_v0_5 import (
    OBJECTIVE_QUIESCENCE_SAFETY_ONLY,
    QUIESCENCE_REVIEW_BLOCKED,
    QUIESCENCE_REVIEW_CLEAR,
    QUIESCENCE_REVIEW_REJECTED,
    ApoptosisQuiescenceEvidence,
    ApoptosisQuiescenceReviewPolicy,
    ApoptosisQuiescenceReviewRecord,
    ApoptosisQuiescenceReviewRequest,
    apoptosis_quiescence_evidence_digest,
    apoptosis_quiescence_review_policy_digest,
    apoptosis_quiescence_review_record_digest,
    apoptosis_quiescence_review_request_digest,
)


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_apoptosis_quiescence_review_policy(
    policy_id: str,
    *,
    allowed_reviewer_ids: tuple[str, ...],
    allowed_objectives: tuple[str, ...] = (OBJECTIVE_QUIESCENCE_SAFETY_ONLY,),
    max_review_delay_seconds: int = 86_400,
    max_evidence_age_seconds: int = 3_600,
    minimum_grace_period_seconds: int = 300,
) -> ApoptosisQuiescenceReviewPolicy:
    policy = ApoptosisQuiescenceReviewPolicy(
        policy_id=policy_id,
        allowed_reviewer_ids=_canonical(allowed_reviewer_ids),
        allowed_objectives=_canonical(allowed_objectives),
        max_review_delay_seconds=max_review_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        minimum_grace_period_seconds=minimum_grace_period_seconds,
        require_source_authority_review_recomputation=True,
        require_clear_authority_source=True,
        require_source_subject_binding=True,
        require_execution_snapshot_binding=True,
        require_independent_reviewer=True,
        require_complete_quiescence_closure=True,
        require_no_active_execution=True,
        require_no_pending_work=True,
        require_no_active_lease=True,
        require_new_intake_stopped=True,
        require_no_open_intake_channel=True,
        require_no_blocking_external_dependency=True,
        require_verified_drain=True,
        require_verified_checkpoint=True,
        require_verified_recovery_route=True,
        require_reentry_possible=True,
        require_valid_quiescence_time_order=True,
        require_grace_period_elapsed=True,
        require_no_emergency_operation=True,
        require_external_review_next=True,
        require_independent_authorization_next=True,
        allow_quiescence_review_record_issuance=True,
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
        policy_digest=apoptosis_quiescence_review_policy_digest(policy),
    )
    issues = apoptosis_quiescence_review_policy_issues(policy)
    if issues:
        raise ValueError(f"apoptosis_quiescence_review_policy_invalid:{issues[0]}")
    return policy


def apoptosis_quiescence_review_policy_issues(
    policy: ApoptosisQuiescenceReviewPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("apoptosis_quiescence_review_policy_id_missing")
    if policy.allowed_reviewer_ids != _canonical(policy.allowed_reviewer_ids):
        issues.append("apoptosis_quiescence_reviewer_ids_not_canonical")
    if not policy.allowed_reviewer_ids:
        issues.append("apoptosis_quiescence_reviewer_ids_empty")
    if policy.allowed_objectives != _canonical(policy.allowed_objectives):
        issues.append("apoptosis_quiescence_objectives_not_canonical")
    if policy.allowed_objectives != (OBJECTIVE_QUIESCENCE_SAFETY_ONLY,):
        issues.append("apoptosis_quiescence_objective_scope_invalid")
    if policy.max_review_delay_seconds <= 0:
        issues.append("apoptosis_quiescence_review_delay_bound_invalid")
    if policy.max_evidence_age_seconds <= 0:
        issues.append("apoptosis_quiescence_evidence_age_bound_invalid")
    if policy.minimum_grace_period_seconds <= 0:
        issues.append("apoptosis_quiescence_grace_period_bound_invalid")
    if not all(
        (
            policy.require_source_authority_review_recomputation,
            policy.require_clear_authority_source,
            policy.require_source_subject_binding,
            policy.require_execution_snapshot_binding,
            policy.require_independent_reviewer,
            policy.require_complete_quiescence_closure,
            policy.require_no_active_execution,
            policy.require_no_pending_work,
            policy.require_no_active_lease,
            policy.require_new_intake_stopped,
            policy.require_no_open_intake_channel,
            policy.require_no_blocking_external_dependency,
            policy.require_verified_drain,
            policy.require_verified_checkpoint,
            policy.require_verified_recovery_route,
            policy.require_reentry_possible,
            policy.require_valid_quiescence_time_order,
            policy.require_grace_period_elapsed,
            policy.require_no_emergency_operation,
            policy.require_external_review_next,
            policy.require_independent_authorization_next,
            policy.allow_quiescence_review_record_issuance,
        )
    ):
        issues.append("apoptosis_quiescence_required_guard_disabled")
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
        issues.append("apoptosis_quiescence_execution_effect_enabled")
    if policy.policy_digest != apoptosis_quiescence_review_policy_digest(policy):
        issues.append("apoptosis_quiescence_review_policy_digest_mismatch")
    return tuple(issues)


def build_apoptosis_quiescence_evidence(
    evidence_id: str,
    subject_id: str,
    subject_kind: str,
    subject_version: str,
    *,
    captured_at_epoch_seconds: int,
    execution_snapshot_digest: str,
    work_snapshot_digest: str,
    intake_snapshot_digest: str,
    state_checkpoint_digest: str,
    drain_plan_digest: str,
    recovery_route_digest: str,
    active_execution_ids: tuple[str, ...],
    pending_work_ids: tuple[str, ...],
    critical_pending_work_ids: tuple[str, ...],
    active_lease_ids: tuple[str, ...],
    intake_channel_ids: tuple[str, ...],
    open_intake_channel_ids: tuple[str, ...],
    blocking_external_dependency_ids: tuple[str, ...],
    quiescence_closure_complete: bool,
    new_intake_stopped: bool,
    drain_verified: bool,
    checkpoint_verified: bool,
    recovery_route_verified: bool,
    reentry_possible: bool,
    quiescence_started_at_epoch_seconds: int,
    last_activity_at_epoch_seconds: int,
    emergency_operation_active: bool,
) -> ApoptosisQuiescenceEvidence:
    evidence = ApoptosisQuiescenceEvidence(
        evidence_id=evidence_id,
        subject_id=subject_id,
        subject_kind=subject_kind,
        subject_version=subject_version,
        captured_at_epoch_seconds=captured_at_epoch_seconds,
        execution_snapshot_digest=execution_snapshot_digest,
        work_snapshot_digest=work_snapshot_digest,
        intake_snapshot_digest=intake_snapshot_digest,
        state_checkpoint_digest=state_checkpoint_digest,
        drain_plan_digest=drain_plan_digest,
        recovery_route_digest=recovery_route_digest,
        active_execution_ids=_canonical(active_execution_ids),
        pending_work_ids=_canonical(pending_work_ids),
        critical_pending_work_ids=_canonical(critical_pending_work_ids),
        active_lease_ids=_canonical(active_lease_ids),
        intake_channel_ids=_canonical(intake_channel_ids),
        open_intake_channel_ids=_canonical(open_intake_channel_ids),
        blocking_external_dependency_ids=_canonical(
            blocking_external_dependency_ids
        ),
        quiescence_closure_complete=quiescence_closure_complete,
        new_intake_stopped=new_intake_stopped,
        drain_verified=drain_verified,
        checkpoint_verified=checkpoint_verified,
        recovery_route_verified=recovery_route_verified,
        reentry_possible=reentry_possible,
        quiescence_started_at_epoch_seconds=(
            quiescence_started_at_epoch_seconds
        ),
        last_activity_at_epoch_seconds=last_activity_at_epoch_seconds,
        emergency_operation_active=emergency_operation_active,
        evidence_digest="",
    )
    evidence = replace(
        evidence,
        evidence_digest=apoptosis_quiescence_evidence_digest(evidence),
    )
    issues = apoptosis_quiescence_evidence_issues(evidence)
    if issues:
        raise ValueError(f"apoptosis_quiescence_evidence_invalid:{issues[0]}")
    return evidence


def apoptosis_quiescence_evidence_issues(
    evidence: ApoptosisQuiescenceEvidence,
) -> tuple[str, ...]:
    issues: list[str] = []
    for field_name in (
        "evidence_id",
        "subject_id",
        "subject_kind",
        "subject_version",
        "execution_snapshot_digest",
        "work_snapshot_digest",
        "intake_snapshot_digest",
        "state_checkpoint_digest",
        "drain_plan_digest",
        "recovery_route_digest",
    ):
        if not getattr(evidence, field_name):
            issues.append(f"apoptosis_quiescence_{field_name}_missing")
    for field_name in (
        "captured_at_epoch_seconds",
        "quiescence_started_at_epoch_seconds",
        "last_activity_at_epoch_seconds",
    ):
        if getattr(evidence, field_name) < 0:
            issues.append(f"apoptosis_quiescence_{field_name}_invalid")
    for field_name in (
        "active_execution_ids",
        "pending_work_ids",
        "critical_pending_work_ids",
        "active_lease_ids",
        "intake_channel_ids",
        "open_intake_channel_ids",
        "blocking_external_dependency_ids",
    ):
        values = getattr(evidence, field_name)
        if values != _canonical(values):
            issues.append(f"apoptosis_quiescence_{field_name}_not_canonical")
        if any(not value for value in values):
            issues.append(f"apoptosis_quiescence_{field_name}_contains_empty")
    if not set(evidence.critical_pending_work_ids).issubset(
        set(evidence.pending_work_ids)
    ):
        issues.append("apoptosis_quiescence_critical_work_not_pending")
    if not set(evidence.open_intake_channel_ids).issubset(
        set(evidence.intake_channel_ids)
    ):
        issues.append("apoptosis_quiescence_open_intake_not_declared")
    if evidence.evidence_digest != apoptosis_quiescence_evidence_digest(evidence):
        issues.append("apoptosis_quiescence_evidence_digest_mismatch")
    return tuple(issues)


def build_apoptosis_quiescence_review_request(
    review_id: str,
    reviewer_id: str,
    reviewed_at_epoch_seconds: int,
    authority_request: ApoptosisAuthorityReviewRequest,
    authority_policy: ApoptosisAuthorityReviewPolicy,
    authority_evidence: ApoptosisAuthorityEvidence,
    authority_record: ApoptosisAuthorityReviewRecord,
    quiescence_evidence: ApoptosisQuiescenceEvidence,
    *,
    objective: str = OBJECTIVE_QUIESCENCE_SAFETY_ONLY,
) -> ApoptosisQuiescenceReviewRequest:
    request = ApoptosisQuiescenceReviewRequest(
        review_id=review_id,
        reviewer_id=reviewer_id,
        objective=objective,
        reviewed_at_epoch_seconds=reviewed_at_epoch_seconds,
        source_authority_review_id=authority_record.review_id,
        source_authority_review_digest=authority_record.record_digest,
        source_authority_review_request_digest=authority_request.request_digest,
        source_authority_review_policy_digest=authority_policy.policy_digest,
        source_authority_evidence_digest=authority_evidence.evidence_digest,
        subject_id=authority_record.subject_id,
        subject_kind=authority_record.subject_kind,
        subject_version=authority_record.subject_version,
        execution_snapshot_digest=quiescence_evidence.execution_snapshot_digest,
        quiescence_evidence_digest=quiescence_evidence.evidence_digest,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=apoptosis_quiescence_review_request_digest(request),
    )
    issues = apoptosis_quiescence_review_request_issues(request)
    if issues:
        raise ValueError(f"apoptosis_quiescence_review_request_invalid:{issues[0]}")
    return request


def apoptosis_quiescence_review_request_issues(
    request: ApoptosisQuiescenceReviewRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    for field_name in (
        "review_id",
        "reviewer_id",
        "objective",
        "source_authority_review_id",
        "source_authority_review_digest",
        "source_authority_review_request_digest",
        "source_authority_review_policy_digest",
        "source_authority_evidence_digest",
        "subject_id",
        "subject_kind",
        "subject_version",
        "execution_snapshot_digest",
        "quiescence_evidence_digest",
    ):
        if not getattr(request, field_name):
            issues.append(f"apoptosis_quiescence_{field_name}_missing")
    if request.reviewed_at_epoch_seconds < 0:
        issues.append("apoptosis_quiescence_reviewed_at_invalid")
    if request.request_digest != apoptosis_quiescence_review_request_digest(request):
        issues.append("apoptosis_quiescence_review_request_digest_mismatch")
    return tuple(issues)


def _source_authority_review_valid(
    authority_request: ApoptosisAuthorityReviewRequest,
    authority_evidence: ApoptosisAuthorityEvidence,
    authority_policy: ApoptosisAuthorityReviewPolicy,
    authority_record: ApoptosisAuthorityReviewRecord,
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
        apoptosis_authority_review_request_issues(authority_request)
        or apoptosis_authority_evidence_issues(authority_evidence)
        or apoptosis_authority_review_policy_issues(authority_policy)
        or apoptosis_authority_review_record_issues(
            authority_record,
            authority_request,
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
    )


def construct_apoptosis_quiescence_review(
    request: ApoptosisQuiescenceReviewRequest,
    quiescence_evidence: ApoptosisQuiescenceEvidence,
    quiescence_policy: ApoptosisQuiescenceReviewPolicy,
    authority_request: ApoptosisAuthorityReviewRequest,
    authority_evidence: ApoptosisAuthorityEvidence,
    authority_policy: ApoptosisAuthorityReviewPolicy,
    authority_record: ApoptosisAuthorityReviewRecord,
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
) -> ApoptosisQuiescenceReviewRecord:
    policy_valid = not apoptosis_quiescence_review_policy_issues(
        quiescence_policy
    )
    request_valid = not apoptosis_quiescence_review_request_issues(request)
    evidence_valid = not apoptosis_quiescence_evidence_issues(
        quiescence_evidence
    )
    source_recomputed_valid = _source_authority_review_valid(
        authority_request,
        authority_evidence,
        authority_policy,
        authority_record,
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
    source_authority_clear = bool(
        authority_record.status == AUTHORITY_REVIEW_CLEAR
        and authority_record.authority_review_record_issued
        and authority_record.authority_clear_for_quiescence_review
        and authority_record.quiescence_review_required_next
    )
    source_subject_binding_valid = all(
        (
            request.subject_id
            == authority_record.subject_id
            == candidate_record.subject_id,
            request.subject_kind
            == authority_record.subject_kind
            == candidate_record.subject_kind,
            request.subject_version
            == authority_record.subject_version
            == candidate_record.subject_version,
        )
    )
    source_execution_snapshot_binding_valid = (
        request.execution_snapshot_digest
        == quiescence_evidence.execution_snapshot_digest
    )
    source_authority_review_binding_valid = all(
        (
            request.source_authority_review_id == authority_record.review_id,
            request.source_authority_review_digest == authority_record.record_digest,
            request.source_authority_review_request_digest
            == authority_request.request_digest,
            request.source_authority_review_policy_digest
            == authority_policy.policy_digest,
            request.source_authority_evidence_digest
            == authority_evidence.evidence_digest,
        )
    )
    reviewer_allowed = request.reviewer_id in quiescence_policy.allowed_reviewer_ids
    excluded_reviewer_ids = {
        request.subject_id,
        candidate_record.issuer_id,
        dependency_record.reviewer_id,
        authority_record.reviewer_id,
        authority_evidence.responsible_authority_id,
    }
    reviewer_independent = request.reviewer_id not in excluded_reviewer_ids
    objective_allowed = request.objective in quiescence_policy.allowed_objectives
    review_delay = (
        request.reviewed_at_epoch_seconds
        - authority_record.reviewed_at_epoch_seconds
    )
    review_delay_valid = (
        0 <= review_delay <= quiescence_policy.max_review_delay_seconds
    )
    evidence_age = (
        request.reviewed_at_epoch_seconds
        - quiescence_evidence.captured_at_epoch_seconds
    )
    evidence_fresh = (
        0 <= evidence_age <= quiescence_policy.max_evidence_age_seconds
    )
    evidence_subject_binding_valid = all(
        (
            quiescence_evidence.subject_id == request.subject_id,
            quiescence_evidence.subject_kind == request.subject_kind,
            quiescence_evidence.subject_version == request.subject_version,
        )
    )
    evidence_snapshot_binding_valid = all(
        (
            request.quiescence_evidence_digest
            == quiescence_evidence.evidence_digest,
            request.execution_snapshot_digest
            == quiescence_evidence.execution_snapshot_digest,
        )
    )
    active_execution_present = bool(
        quiescence_evidence.active_execution_ids
    )
    pending_work_present = bool(quiescence_evidence.pending_work_ids)
    critical_pending_work_present = bool(
        quiescence_evidence.critical_pending_work_ids
    )
    active_lease_present = bool(quiescence_evidence.active_lease_ids)
    open_intake_present = bool(quiescence_evidence.open_intake_channel_ids)
    blocking_external_dependency_present = bool(
        quiescence_evidence.blocking_external_dependency_ids
    )
    quiescence_time_order_valid = all(
        (
            authority_record.reviewed_at_epoch_seconds
            <= quiescence_evidence.quiescence_started_at_epoch_seconds,
            quiescence_evidence.last_activity_at_epoch_seconds
            <= quiescence_evidence.quiescence_started_at_epoch_seconds,
            quiescence_evidence.quiescence_started_at_epoch_seconds
            <= quiescence_evidence.captured_at_epoch_seconds,
            quiescence_evidence.captured_at_epoch_seconds
            <= request.reviewed_at_epoch_seconds,
        )
    )
    grace_period_elapsed = bool(
        quiescence_time_order_valid
        and request.reviewed_at_epoch_seconds
        - quiescence_evidence.quiescence_started_at_epoch_seconds
        >= quiescence_policy.minimum_grace_period_seconds
    )

    base_valid = all(
        (
            policy_valid,
            request_valid,
            evidence_valid,
            source_recomputed_valid,
            source_authority_clear,
            source_subject_binding_valid,
            source_execution_snapshot_binding_valid,
            source_authority_review_binding_valid,
            reviewer_allowed,
            reviewer_independent,
            objective_allowed,
            review_delay_valid,
            evidence_fresh,
            evidence_subject_binding_valid,
            evidence_snapshot_binding_valid,
        )
    )
    quiescence_clear = all(
        (
            quiescence_evidence.quiescence_closure_complete,
            not active_execution_present,
            not pending_work_present,
            not critical_pending_work_present,
            not active_lease_present,
            quiescence_evidence.new_intake_stopped,
            not open_intake_present,
            not blocking_external_dependency_present,
            quiescence_evidence.drain_verified,
            quiescence_evidence.checkpoint_verified,
            quiescence_evidence.recovery_route_verified,
            quiescence_evidence.reentry_possible,
            quiescence_time_order_valid,
            grace_period_elapsed,
            not quiescence_evidence.emergency_operation_active,
        )
    )

    if not base_valid:
        status = QUIESCENCE_REVIEW_REJECTED
        reason = "quiescence_review_source_request_policy_or_evidence_invalid"
    elif quiescence_evidence.emergency_operation_active:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "emergency_operation_active"
    elif not quiescence_evidence.quiescence_closure_complete:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "quiescence_closure_incomplete"
    elif active_execution_present:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "active_execution_present"
    elif critical_pending_work_present:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "critical_pending_work_present"
    elif pending_work_present:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "pending_work_present"
    elif active_lease_present:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "active_lease_present"
    elif not quiescence_evidence.new_intake_stopped:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "new_intake_not_stopped"
    elif open_intake_present:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "open_intake_channel_present"
    elif blocking_external_dependency_present:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "blocking_external_dependency_present"
    elif not quiescence_evidence.drain_verified:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "drain_not_verified"
    elif not quiescence_evidence.checkpoint_verified:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "checkpoint_not_verified"
    elif not quiescence_evidence.recovery_route_verified:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "recovery_route_not_verified"
    elif not quiescence_evidence.reentry_possible:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "reentry_not_possible"
    elif not quiescence_time_order_valid:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "quiescence_time_order_invalid"
    elif not grace_period_elapsed:
        status = QUIESCENCE_REVIEW_BLOCKED
        reason = "grace_period_not_elapsed"
    else:
        status = QUIESCENCE_REVIEW_CLEAR
        reason = "quiescence_clear_for_external_review_only"

    valid_review = status in (QUIESCENCE_REVIEW_CLEAR, QUIESCENCE_REVIEW_BLOCKED)
    clear = status == QUIESCENCE_REVIEW_CLEAR
    checks = {
        "policy_valid": policy_valid,
        "request_valid": request_valid,
        "evidence_valid": evidence_valid,
        "source_recomputed_valid": source_recomputed_valid,
        "source_authority_clear": source_authority_clear,
        "source_subject_binding_valid": source_subject_binding_valid,
        "source_execution_snapshot_binding_valid": (
            source_execution_snapshot_binding_valid
        ),
        "source_authority_review_binding_valid": (
            source_authority_review_binding_valid
        ),
        "reviewer_allowed": reviewer_allowed,
        "reviewer_independent": reviewer_independent,
        "objective_allowed": objective_allowed,
        "review_delay_valid": review_delay_valid,
        "evidence_fresh": evidence_fresh,
        "evidence_subject_binding_valid": evidence_subject_binding_valid,
        "evidence_snapshot_binding_valid": evidence_snapshot_binding_valid,
        "quiescence_closure_complete": (
            quiescence_evidence.quiescence_closure_complete
        ),
        "active_execution_present": active_execution_present,
        "pending_work_present": pending_work_present,
        "critical_pending_work_present": critical_pending_work_present,
        "active_lease_present": active_lease_present,
        "new_intake_stopped": quiescence_evidence.new_intake_stopped,
        "open_intake_present": open_intake_present,
        "blocking_external_dependency_present": (
            blocking_external_dependency_present
        ),
        "drain_verified": quiescence_evidence.drain_verified,
        "checkpoint_verified": quiescence_evidence.checkpoint_verified,
        "recovery_route_verified": quiescence_evidence.recovery_route_verified,
        "reentry_possible": quiescence_evidence.reentry_possible,
        "quiescence_time_order_valid": quiescence_time_order_valid,
        "grace_period_elapsed": grace_period_elapsed,
        "emergency_operation_active": (
            quiescence_evidence.emergency_operation_active
        ),
        "quiescence_clear_for_external_review": clear,
        "quiescence_review_record_issued": valid_review,
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
    record = ApoptosisQuiescenceReviewRecord(
        review_id=request.review_id,
        status=status,
        reason=reason,
        policy_digest=quiescence_policy.policy_digest,
        request_digest=request.request_digest,
        source_authority_review_id=request.source_authority_review_id,
        source_authority_review_digest=request.source_authority_review_digest,
        source_authority_review_request_digest=(
            request.source_authority_review_request_digest
        ),
        source_authority_review_policy_digest=(
            request.source_authority_review_policy_digest
        ),
        source_authority_evidence_digest=(
            request.source_authority_evidence_digest
        ),
        quiescence_evidence_digest=request.quiescence_evidence_digest,
        subject_id=request.subject_id,
        subject_kind=request.subject_kind,
        subject_version=request.subject_version,
        reviewer_id=request.reviewer_id,
        objective=request.objective,
        reviewed_at_epoch_seconds=request.reviewed_at_epoch_seconds,
        source_recomputed_valid=source_recomputed_valid,
        source_authority_clear=source_authority_clear,
        source_subject_binding_valid=source_subject_binding_valid,
        source_execution_snapshot_binding_valid=(
            source_execution_snapshot_binding_valid
        ),
        source_authority_review_binding_valid=(
            source_authority_review_binding_valid
        ),
        reviewer_allowed=reviewer_allowed,
        reviewer_independent=reviewer_independent,
        objective_allowed=objective_allowed,
        review_delay_valid=review_delay_valid,
        evidence_valid=evidence_valid,
        evidence_fresh=evidence_fresh,
        evidence_subject_binding_valid=evidence_subject_binding_valid,
        evidence_snapshot_binding_valid=evidence_snapshot_binding_valid,
        quiescence_closure_complete=(
            quiescence_evidence.quiescence_closure_complete
        ),
        active_execution_present=active_execution_present,
        pending_work_present=pending_work_present,
        critical_pending_work_present=critical_pending_work_present,
        active_lease_present=active_lease_present,
        new_intake_stopped=quiescence_evidence.new_intake_stopped,
        open_intake_present=open_intake_present,
        blocking_external_dependency_present=(
            blocking_external_dependency_present
        ),
        drain_verified=quiescence_evidence.drain_verified,
        checkpoint_verified=quiescence_evidence.checkpoint_verified,
        recovery_route_verified=quiescence_evidence.recovery_route_verified,
        reentry_possible=quiescence_evidence.reentry_possible,
        quiescence_time_order_valid=quiescence_time_order_valid,
        grace_period_elapsed=grace_period_elapsed,
        emergency_operation_active=quiescence_evidence.emergency_operation_active,
        quiescence_clear_for_external_review=clear,
        quiescence_review_record_issued=valid_review,
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
            "quiescence_review_policy": quiescence_policy.policy_digest,
            "quiescence_review_request": request.request_digest,
            "quiescence_evidence": quiescence_evidence.evidence_digest,
            "execution_snapshot": quiescence_evidence.execution_snapshot_digest,
            "work_snapshot": quiescence_evidence.work_snapshot_digest,
            "intake_snapshot": quiescence_evidence.intake_snapshot_digest,
            "state_checkpoint": quiescence_evidence.state_checkpoint_digest,
            "drain_plan": quiescence_evidence.drain_plan_digest,
            "recovery_route": quiescence_evidence.recovery_route_digest,
            "source_authority_review_policy": authority_policy.policy_digest,
            "source_authority_review_request": authority_request.request_digest,
            "source_authority_evidence": authority_evidence.evidence_digest,
            "source_authority_review_record": authority_record.record_digest,
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
        record_digest=apoptosis_quiescence_review_record_digest(record),
    )


def review_apoptosis_quiescence(
    request: ApoptosisQuiescenceReviewRequest,
    quiescence_evidence: ApoptosisQuiescenceEvidence,
    quiescence_policy: ApoptosisQuiescenceReviewPolicy,
    authority_request: ApoptosisAuthorityReviewRequest,
    authority_evidence: ApoptosisAuthorityEvidence,
    authority_policy: ApoptosisAuthorityReviewPolicy,
    authority_record: ApoptosisAuthorityReviewRecord,
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
) -> ApoptosisQuiescenceReviewRecord:
    record = construct_apoptosis_quiescence_review(
        request,
        quiescence_evidence,
        quiescence_policy,
        authority_request,
        authority_evidence,
        authority_policy,
        authority_record,
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
    issues = apoptosis_quiescence_review_record_issues(
        record,
        request,
        quiescence_evidence,
        quiescence_policy,
        authority_request,
        authority_evidence,
        authority_policy,
        authority_record,
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
        raise ValueError(f"apoptosis_quiescence_review_record_invalid:{issues[0]}")
    return record


def apoptosis_quiescence_review_record_issues(
    record: ApoptosisQuiescenceReviewRecord,
    request: ApoptosisQuiescenceReviewRequest,
    quiescence_evidence: ApoptosisQuiescenceEvidence,
    quiescence_policy: ApoptosisQuiescenceReviewPolicy,
    authority_request: ApoptosisAuthorityReviewRequest,
    authority_evidence: ApoptosisAuthorityEvidence,
    authority_policy: ApoptosisAuthorityReviewPolicy,
    authority_record: ApoptosisAuthorityReviewRecord,
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
    expected = construct_apoptosis_quiescence_review(
        request,
        quiescence_evidence,
        quiescence_policy,
        authority_request,
        authority_evidence,
        authority_policy,
        authority_record,
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
        issues.append("apoptosis_quiescence_review_recomputation_mismatch")
    if record.status not in (
        QUIESCENCE_REVIEW_CLEAR,
        QUIESCENCE_REVIEW_BLOCKED,
        QUIESCENCE_REVIEW_REJECTED,
    ):
        issues.append("apoptosis_quiescence_review_status_invalid")
    if record.status == QUIESCENCE_REVIEW_CLEAR:
        if not record.quiescence_review_record_issued:
            issues.append("apoptosis_quiescence_clear_record_not_issued")
        if not record.quiescence_clear_for_external_review:
            issues.append("apoptosis_quiescence_clear_flag_missing")
        if not all(
            (
                record.external_review_required_next,
                record.independent_authorization_required_next,
            )
        ):
            issues.append("apoptosis_quiescence_next_review_gate_missing")
    if record.status == QUIESCENCE_REVIEW_BLOCKED:
        if not record.quiescence_review_record_issued:
            issues.append("apoptosis_quiescence_blocked_record_not_issued")
        if record.quiescence_clear_for_external_review:
            issues.append("apoptosis_quiescence_blocked_marked_clear")
        if any(
            (
                record.external_review_required_next,
                record.independent_authorization_required_next,
            )
        ):
            issues.append("apoptosis_quiescence_blocked_advanced")
    if record.status == QUIESCENCE_REVIEW_REJECTED:
        if record.quiescence_review_record_issued:
            issues.append("apoptosis_quiescence_rejected_record_issued")
        if record.quiescence_clear_for_external_review:
            issues.append("apoptosis_quiescence_rejected_marked_clear")
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
        issues.append("apoptosis_quiescence_execution_effect_performed")
    if record.record_digest != apoptosis_quiescence_review_record_digest(record):
        issues.append("apoptosis_quiescence_review_record_digest_mismatch")
    return tuple(issues)


__all__ = [
    "build_apoptosis_quiescence_review_policy",
    "apoptosis_quiescence_review_policy_issues",
    "build_apoptosis_quiescence_evidence",
    "apoptosis_quiescence_evidence_issues",
    "build_apoptosis_quiescence_review_request",
    "apoptosis_quiescence_review_request_issues",
    "construct_apoptosis_quiescence_review",
    "review_apoptosis_quiescence",
    "apoptosis_quiescence_review_record_issues",
]
