#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_apoptosis_observation_v0_1"

OBSERVATION_NO_ACTION = "APOPTOSIS_OBSERVATION_NO_ACTION"
OBSERVATION_REVIEW_RECOMMENDED = "APOPTOSIS_OBSERVATION_REVIEW_RECOMMENDED"
OBSERVATION_PROTECTED = "APOPTOSIS_OBSERVATION_PROTECTED"
OBSERVATION_REJECTED = "APOPTOSIS_OBSERVATION_REJECTED"

SUBJECT_MODULE = "MODULE"
SUBJECT_AGENT = "AGENT"
SUBJECT_MEMORY_LINEAGE = "MEMORY_LINEAGE"
SUBJECT_AUTHORITY_LINEAGE = "AUTHORITY_LINEAGE"
SUBJECT_CHECKPOINT = "CHECKPOINT"


@dataclass(frozen=True)
class ApoptosisObservationPolicy:
    policy_id: str
    allowed_subject_kinds: tuple[str, ...]
    protected_subject_ids: tuple[str, ...]
    max_evidence_age_seconds: int
    repeated_failure_threshold: int
    inactivity_threshold_seconds: int
    require_complete_evidence: bool
    require_provenance: bool
    require_dependency_snapshot: bool
    require_authority_snapshot: bool
    require_external_review_for_recommendation: bool
    require_independent_candidate_stage: bool
    require_independent_authorization: bool
    require_read_only_observation: bool
    allow_candidate_issuance: bool
    allow_authority_revocation: bool
    allow_quiescence_transition: bool
    allow_terminal_transition: bool
    allow_tombstone_write: bool
    allow_physical_deletion: bool
    allow_live_git_execution: bool
    allow_repository_mutation: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_subject_kinds"] = list(self.allowed_subject_kinds)
        payload["protected_subject_ids"] = list(self.protected_subject_ids)
        return payload


def apoptosis_observation_policy_digest(
    policy: ApoptosisObservationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisObservationInput:
    observation_id: str
    subject_id: str
    subject_kind: str
    subject_version: str
    provenance_digest: str
    dependency_snapshot_digest: str
    authority_snapshot_digest: str
    usage_evidence_digest: str
    risk_evidence_digest: str
    replacement_evidence_digest: str
    observed_at_epoch_seconds: int
    evidence_captured_at_epoch_seconds: int
    active_dependency_count: int
    active_authority_count: int
    active_execution_count: int
    unresolved_incident_count: int
    repeated_failure_count: int
    inactive_for_seconds: int
    replacement_verified: bool
    evidence_complete: bool
    constitutional_protected: bool
    institutional_hold: bool
    input_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apoptosis_observation_input_digest(
    observation: ApoptosisObservationInput,
) -> str:
    payload = observation.to_dict()
    payload.pop("input_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisObservationRecord:
    observation_id: str
    status: str
    reason: str
    policy_digest: str
    input_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    observed_at_epoch_seconds: int
    input_valid: bool
    evidence_fresh: bool
    evidence_complete: bool
    provenance_present: bool
    dependency_snapshot_present: bool
    authority_snapshot_present: bool
    subject_kind_allowed: bool
    protected_subject: bool
    institutional_hold_present: bool
    replacement_signal: bool
    repeated_failure_signal: bool
    inactivity_signal: bool
    unresolved_incident_signal: bool
    degradation_signal_present: bool
    active_dependencies_present: bool
    active_authorities_present: bool
    active_executions_present: bool
    dependency_review_required: bool
    authority_review_required: bool
    quiescence_review_required: bool
    external_review_required: bool
    independent_candidate_stage_required: bool
    independent_authorization_required: bool
    apoptosis_candidate_issued: bool
    authority_revocation_performed: bool
    quiescence_transition_performed: bool
    terminal_transition_performed: bool
    tombstone_write_performed: bool
    physical_deletion_performed: bool
    live_git_execution_performed: bool
    repository_mutation_performed: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    record_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apoptosis_observation_record_digest(
    record: ApoptosisObservationRecord,
) -> str:
    payload = record.to_dict()
    payload.pop("record_digest", None)
    return canonical_digest(payload)
