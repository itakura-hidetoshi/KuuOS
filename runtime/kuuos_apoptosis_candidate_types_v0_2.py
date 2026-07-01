#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_apoptosis_candidate_v0_2"

CANDIDATE_PROPOSED = "APOPTOSIS_CANDIDATE_PROPOSED"
CANDIDATE_REJECTED = "APOPTOSIS_CANDIDATE_REJECTED"

OBJECTIVE_GOVERNED_EVALUATION_ONLY = "EVALUATE_FOR_GOVERNED_APOPTOSIS_ONLY"


@dataclass(frozen=True)
class ApoptosisCandidatePolicy:
    policy_id: str
    allowed_issuer_ids: tuple[str, ...]
    allowed_objectives: tuple[str, ...]
    max_candidate_delay_seconds: int
    require_source_recomputation: bool
    require_review_recommended_source: bool
    require_source_non_protected: bool
    require_source_no_hold: bool
    require_provenance_binding: bool
    require_dependency_binding: bool
    require_authority_binding: bool
    require_independent_dependency_review: bool
    require_independent_authority_review: bool
    require_independent_quiescence_review: bool
    require_external_review: bool
    require_independent_authorization: bool
    allow_candidate_artifact_issuance: bool
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
        payload["allowed_issuer_ids"] = list(self.allowed_issuer_ids)
        payload["allowed_objectives"] = list(self.allowed_objectives)
        return payload


def apoptosis_candidate_policy_digest(policy: ApoptosisCandidatePolicy) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisCandidateRequest:
    candidate_id: str
    issuer_id: str
    objective: str
    issued_at_epoch_seconds: int
    source_observation_id: str
    source_observation_record_digest: str
    source_observation_input_digest: str
    source_observation_policy_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    provenance_digest: str
    dependency_snapshot_digest: str
    authority_snapshot_digest: str
    rationale_digest: str
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apoptosis_candidate_request_digest(request: ApoptosisCandidateRequest) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisCandidateRecord:
    candidate_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    source_observation_id: str
    source_observation_record_digest: str
    source_observation_input_digest: str
    source_observation_policy_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    issuer_id: str
    objective: str
    issued_at_epoch_seconds: int
    source_recomputed_valid: bool
    source_review_recommended: bool
    source_non_protected: bool
    source_no_hold: bool
    source_subject_binding_valid: bool
    source_provenance_binding_valid: bool
    source_dependency_binding_valid: bool
    source_authority_binding_valid: bool
    source_rationale_binding_valid: bool
    issuer_allowed: bool
    objective_allowed: bool
    candidate_delay_valid: bool
    dependency_review_required: bool
    authority_review_required: bool
    quiescence_review_required: bool
    external_review_required: bool
    independent_authorization_required: bool
    candidate_artifact_issued: bool
    authority_revocation_performed: bool
    quiescence_transition_performed: bool
    terminal_transition_performed: bool
    tombstone_write_performed: bool
    physical_deletion_performed: bool
    live_git_execution_performed: bool
    repository_mutation_performed: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    candidate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apoptosis_candidate_record_digest(record: ApoptosisCandidateRecord) -> str:
    payload = record.to_dict()
    payload.pop("candidate_digest", None)
    return canonical_digest(payload)
