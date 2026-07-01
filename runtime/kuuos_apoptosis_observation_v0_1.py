#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_apoptosis_observation_types_v0_1 import (
    OBSERVATION_NO_ACTION,
    OBSERVATION_PROTECTED,
    OBSERVATION_REJECTED,
    OBSERVATION_REVIEW_RECOMMENDED,
    SUBJECT_AGENT,
    SUBJECT_AUTHORITY_LINEAGE,
    SUBJECT_CHECKPOINT,
    SUBJECT_MEMORY_LINEAGE,
    SUBJECT_MODULE,
    ApoptosisObservationInput,
    ApoptosisObservationPolicy,
    ApoptosisObservationRecord,
    apoptosis_observation_input_digest,
    apoptosis_observation_policy_digest,
    apoptosis_observation_record_digest,
)

DEFAULT_SUBJECT_KINDS = (
    SUBJECT_MODULE,
    SUBJECT_AGENT,
    SUBJECT_MEMORY_LINEAGE,
    SUBJECT_AUTHORITY_LINEAGE,
    SUBJECT_CHECKPOINT,
)


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_apoptosis_observation_policy(
    policy_id: str,
    *,
    protected_subject_ids: tuple[str, ...],
    allowed_subject_kinds: tuple[str, ...] = DEFAULT_SUBJECT_KINDS,
    max_evidence_age_seconds: int = 86_400,
    repeated_failure_threshold: int = 3,
    inactivity_threshold_seconds: int = 2_592_000,
) -> ApoptosisObservationPolicy:
    policy = ApoptosisObservationPolicy(
        policy_id=policy_id,
        allowed_subject_kinds=_canonical(allowed_subject_kinds),
        protected_subject_ids=_canonical(protected_subject_ids),
        max_evidence_age_seconds=max_evidence_age_seconds,
        repeated_failure_threshold=repeated_failure_threshold,
        inactivity_threshold_seconds=inactivity_threshold_seconds,
        require_complete_evidence=True,
        require_provenance=True,
        require_dependency_snapshot=True,
        require_authority_snapshot=True,
        require_external_review_for_recommendation=True,
        require_independent_candidate_stage=True,
        require_independent_authorization=True,
        require_read_only_observation=True,
        allow_candidate_issuance=False,
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
        policy_digest=apoptosis_observation_policy_digest(policy),
    )
    issues = apoptosis_observation_policy_issues(policy)
    if issues:
        raise ValueError(f"apoptosis_observation_policy_invalid:{issues[0]}")
    return policy


def apoptosis_observation_policy_issues(
    policy: ApoptosisObservationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("apoptosis_policy_id_missing")
    if policy.allowed_subject_kinds != _canonical(policy.allowed_subject_kinds):
        issues.append("apoptosis_subject_kinds_not_canonical")
    if not policy.allowed_subject_kinds:
        issues.append("apoptosis_subject_kinds_empty")
    if not set(policy.allowed_subject_kinds).issubset(DEFAULT_SUBJECT_KINDS):
        issues.append("apoptosis_subject_kind_unknown")
    if policy.protected_subject_ids != _canonical(policy.protected_subject_ids):
        issues.append("apoptosis_protected_subject_ids_not_canonical")
    if policy.max_evidence_age_seconds <= 0:
        issues.append("apoptosis_evidence_age_bound_invalid")
    if policy.repeated_failure_threshold <= 0:
        issues.append("apoptosis_failure_threshold_invalid")
    if policy.inactivity_threshold_seconds <= 0:
        issues.append("apoptosis_inactivity_threshold_invalid")
    if not all(
        (
            policy.require_complete_evidence,
            policy.require_provenance,
            policy.require_dependency_snapshot,
            policy.require_authority_snapshot,
            policy.require_external_review_for_recommendation,
            policy.require_independent_candidate_stage,
            policy.require_independent_authorization,
            policy.require_read_only_observation,
        )
    ):
        issues.append("apoptosis_required_guard_disabled")
    if any(
        (
            policy.allow_candidate_issuance,
            policy.allow_authority_revocation,
            policy.allow_quiescence_transition,
            policy.allow_terminal_transition,
            policy.allow_tombstone_write,
            policy.allow_physical_deletion,
            policy.allow_live_git_execution,
            policy.allow_repository_mutation,
        )
    ):
        issues.append("apoptosis_observation_effect_enabled")
    if policy.policy_digest != apoptosis_observation_policy_digest(policy):
        issues.append("apoptosis_policy_digest_mismatch")
    return tuple(issues)


def build_apoptosis_observation_input(
    observation_id: str,
    subject_id: str,
    subject_kind: str,
    subject_version: str,
    *,
    provenance_digest: str,
    dependency_snapshot_digest: str,
    authority_snapshot_digest: str,
    usage_evidence_digest: str,
    risk_evidence_digest: str,
    replacement_evidence_digest: str,
    observed_at_epoch_seconds: int,
    evidence_captured_at_epoch_seconds: int,
    active_dependency_count: int,
    active_authority_count: int,
    active_execution_count: int,
    unresolved_incident_count: int,
    repeated_failure_count: int,
    inactive_for_seconds: int,
    replacement_verified: bool,
    evidence_complete: bool,
    constitutional_protected: bool,
    institutional_hold: bool,
) -> ApoptosisObservationInput:
    observation = ApoptosisObservationInput(
        observation_id=observation_id,
        subject_id=subject_id,
        subject_kind=subject_kind,
        subject_version=subject_version,
        provenance_digest=provenance_digest,
        dependency_snapshot_digest=dependency_snapshot_digest,
        authority_snapshot_digest=authority_snapshot_digest,
        usage_evidence_digest=usage_evidence_digest,
        risk_evidence_digest=risk_evidence_digest,
        replacement_evidence_digest=replacement_evidence_digest,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        evidence_captured_at_epoch_seconds=evidence_captured_at_epoch_seconds,
        active_dependency_count=active_dependency_count,
        active_authority_count=active_authority_count,
        active_execution_count=active_execution_count,
        unresolved_incident_count=unresolved_incident_count,
        repeated_failure_count=repeated_failure_count,
        inactive_for_seconds=inactive_for_seconds,
        replacement_verified=replacement_verified,
        evidence_complete=evidence_complete,
        constitutional_protected=constitutional_protected,
        institutional_hold=institutional_hold,
        input_digest="",
    )
    observation = replace(
        observation,
        input_digest=apoptosis_observation_input_digest(observation),
    )
    issues = apoptosis_observation_input_issues(observation)
    if issues:
        raise ValueError(f"apoptosis_observation_input_invalid:{issues[0]}")
    return observation


def apoptosis_observation_input_issues(
    observation: ApoptosisObservationInput,
) -> tuple[str, ...]:
    issues: list[str] = []
    for field_name in ("observation_id", "subject_id", "subject_kind", "subject_version"):
        if not getattr(observation, field_name):
            issues.append(f"apoptosis_{field_name}_missing")
    for field_name in (
        "provenance_digest",
        "dependency_snapshot_digest",
        "authority_snapshot_digest",
        "usage_evidence_digest",
        "risk_evidence_digest",
        "replacement_evidence_digest",
    ):
        if not getattr(observation, field_name):
            issues.append(f"apoptosis_{field_name}_missing")
    if observation.observed_at_epoch_seconds < 0:
        issues.append("apoptosis_observed_at_invalid")
    if observation.evidence_captured_at_epoch_seconds < 0:
        issues.append("apoptosis_evidence_captured_at_invalid")
    if observation.observed_at_epoch_seconds < observation.evidence_captured_at_epoch_seconds:
        issues.append("apoptosis_evidence_from_future")
    for field_name in (
        "active_dependency_count",
        "active_authority_count",
        "active_execution_count",
        "unresolved_incident_count",
        "repeated_failure_count",
        "inactive_for_seconds",
    ):
        if getattr(observation, field_name) < 0:
            issues.append(f"apoptosis_{field_name}_negative")
    if observation.input_digest != apoptosis_observation_input_digest(observation):
        issues.append("apoptosis_input_digest_mismatch")
    return tuple(issues)


def construct_apoptosis_observation(
    observation: ApoptosisObservationInput,
    policy: ApoptosisObservationPolicy,
) -> ApoptosisObservationRecord:
    policy_valid = not apoptosis_observation_policy_issues(policy)
    input_valid = not apoptosis_observation_input_issues(observation)
    age = observation.observed_at_epoch_seconds - observation.evidence_captured_at_epoch_seconds
    evidence_fresh = bool(
        input_valid and 0 <= age <= policy.max_evidence_age_seconds
    )
    provenance_present = bool(observation.provenance_digest)
    dependency_snapshot_present = bool(observation.dependency_snapshot_digest)
    authority_snapshot_present = bool(observation.authority_snapshot_digest)
    evidence_complete = bool(observation.evidence_complete)
    subject_kind_allowed = observation.subject_kind in policy.allowed_subject_kinds
    protected_subject = bool(
        observation.constitutional_protected
        or observation.subject_id in policy.protected_subject_ids
    )
    institutional_hold_present = bool(observation.institutional_hold)

    replacement_signal = bool(observation.replacement_verified)
    repeated_failure_signal = bool(
        observation.repeated_failure_count >= policy.repeated_failure_threshold
    )
    inactivity_signal = bool(
        observation.inactive_for_seconds >= policy.inactivity_threshold_seconds
    )
    unresolved_incident_signal = bool(observation.unresolved_incident_count > 0)
    degradation_signal_present = any(
        (
            replacement_signal,
            repeated_failure_signal,
            inactivity_signal,
            unresolved_incident_signal,
        )
    )

    base_valid = all(
        (
            policy_valid,
            input_valid,
            evidence_fresh,
            evidence_complete,
            provenance_present,
            dependency_snapshot_present,
            authority_snapshot_present,
            subject_kind_allowed,
        )
    )
    blocked = protected_subject or institutional_hold_present
    if not base_valid:
        status = OBSERVATION_REJECTED
        reason = "observation_evidence_or_policy_invalid"
    elif blocked:
        status = OBSERVATION_PROTECTED
        reason = "subject_protected_or_held"
    elif degradation_signal_present:
        status = OBSERVATION_REVIEW_RECOMMENDED
        reason = "degradation_signal_requires_independent_review"
    else:
        status = OBSERVATION_NO_ACTION
        reason = "no_apoptosis_review_signal"

    review_recommended = status == OBSERVATION_REVIEW_RECOMMENDED
    active_dependencies_present = observation.active_dependency_count > 0
    active_authorities_present = observation.active_authority_count > 0
    active_executions_present = observation.active_execution_count > 0

    checks = {
        "policy_valid": policy_valid,
        "input_valid": input_valid,
        "evidence_fresh": evidence_fresh,
        "evidence_complete": evidence_complete,
        "provenance_present": provenance_present,
        "dependency_snapshot_present": dependency_snapshot_present,
        "authority_snapshot_present": authority_snapshot_present,
        "subject_kind_allowed": subject_kind_allowed,
        "protected_subject": protected_subject,
        "institutional_hold_present": institutional_hold_present,
        "degradation_signal_present": degradation_signal_present,
        "dependency_review_required": review_recommended,
        "authority_review_required": review_recommended,
        "quiescence_review_required": review_recommended,
        "external_review_required": review_recommended,
        "independent_candidate_stage_required": review_recommended,
        "independent_authorization_required": review_recommended,
        "apoptosis_candidate_issued": False,
        "authority_revocation_performed": False,
        "quiescence_transition_performed": False,
        "terminal_transition_performed": False,
        "tombstone_write_performed": False,
        "physical_deletion_performed": False,
        "live_git_execution_performed": False,
        "repository_mutation_performed": False,
    }
    record = ApoptosisObservationRecord(
        observation_id=observation.observation_id,
        status=status,
        reason=reason,
        policy_digest=policy.policy_digest,
        input_digest=observation.input_digest,
        subject_id=observation.subject_id,
        subject_kind=observation.subject_kind,
        subject_version=observation.subject_version,
        observed_at_epoch_seconds=observation.observed_at_epoch_seconds,
        input_valid=input_valid,
        evidence_fresh=evidence_fresh,
        evidence_complete=evidence_complete,
        provenance_present=provenance_present,
        dependency_snapshot_present=dependency_snapshot_present,
        authority_snapshot_present=authority_snapshot_present,
        subject_kind_allowed=subject_kind_allowed,
        protected_subject=protected_subject,
        institutional_hold_present=institutional_hold_present,
        replacement_signal=replacement_signal,
        repeated_failure_signal=repeated_failure_signal,
        inactivity_signal=inactivity_signal,
        unresolved_incident_signal=unresolved_incident_signal,
        degradation_signal_present=degradation_signal_present,
        active_dependencies_present=active_dependencies_present,
        active_authorities_present=active_authorities_present,
        active_executions_present=active_executions_present,
        dependency_review_required=review_recommended,
        authority_review_required=review_recommended,
        quiescence_review_required=review_recommended,
        external_review_required=review_recommended,
        independent_candidate_stage_required=review_recommended,
        independent_authorization_required=review_recommended,
        apoptosis_candidate_issued=False,
        authority_revocation_performed=False,
        quiescence_transition_performed=False,
        terminal_transition_performed=False,
        tombstone_write_performed=False,
        physical_deletion_performed=False,
        live_git_execution_performed=False,
        repository_mutation_performed=False,
        checks=checks,
        evidence_digests={
            "provenance": observation.provenance_digest,
            "dependency_snapshot": observation.dependency_snapshot_digest,
            "authority_snapshot": observation.authority_snapshot_digest,
            "usage": observation.usage_evidence_digest,
            "risk": observation.risk_evidence_digest,
            "replacement": observation.replacement_evidence_digest,
            "policy": policy.policy_digest,
            "input": observation.input_digest,
        },
        record_digest="",
    )
    return replace(record, record_digest=apoptosis_observation_record_digest(record))


def observe_apoptosis_signal(
    observation: ApoptosisObservationInput,
    policy: ApoptosisObservationPolicy,
) -> ApoptosisObservationRecord:
    record = construct_apoptosis_observation(observation, policy)
    issues = apoptosis_observation_record_issues(record, observation, policy)
    if issues:
        raise ValueError(f"apoptosis_observation_record_invalid:{issues[0]}")
    return record


def apoptosis_observation_record_issues(
    record: ApoptosisObservationRecord,
    observation: ApoptosisObservationInput,
    policy: ApoptosisObservationPolicy,
) -> tuple[str, ...]:
    expected = construct_apoptosis_observation(observation, policy)
    issues: list[str] = []
    if record.to_dict() != expected.to_dict():
        issues.append("apoptosis_observation_recomputation_mismatch")
    if record.status not in (
        OBSERVATION_NO_ACTION,
        OBSERVATION_REVIEW_RECOMMENDED,
        OBSERVATION_PROTECTED,
        OBSERVATION_REJECTED,
    ):
        issues.append("apoptosis_observation_status_invalid")
    if record.status == OBSERVATION_REVIEW_RECOMMENDED:
        if not all(
            (
                record.dependency_review_required,
                record.authority_review_required,
                record.quiescence_review_required,
                record.external_review_required,
                record.independent_candidate_stage_required,
                record.independent_authorization_required,
            )
        ):
            issues.append("apoptosis_review_gate_missing")
    if any(
        (
            record.apoptosis_candidate_issued,
            record.authority_revocation_performed,
            record.quiescence_transition_performed,
            record.terminal_transition_performed,
            record.tombstone_write_performed,
            record.physical_deletion_performed,
            record.live_git_execution_performed,
            record.repository_mutation_performed,
        )
    ):
        issues.append("apoptosis_observation_effect_performed")
    if record.record_digest != apoptosis_observation_record_digest(record):
        issues.append("apoptosis_observation_record_digest_mismatch")
    return tuple(issues)


__all__ = [
    "build_apoptosis_observation_policy",
    "apoptosis_observation_policy_issues",
    "build_apoptosis_observation_input",
    "apoptosis_observation_input_issues",
    "construct_apoptosis_observation",
    "observe_apoptosis_signal",
    "apoptosis_observation_record_issues",
]
