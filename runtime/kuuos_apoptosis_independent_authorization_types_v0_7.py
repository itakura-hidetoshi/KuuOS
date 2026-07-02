#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_apoptosis_independent_authorization_v0_7"

INDEPENDENT_AUTHORIZATION_APPROVED = (
    "APOPTOSIS_INDEPENDENT_AUTHORIZATION_APPROVED_FOR_BOUNDED_EXECUTION_PREPARATION"
)
INDEPENDENT_AUTHORIZATION_DENIED = "APOPTOSIS_INDEPENDENT_AUTHORIZATION_DENIED"
INDEPENDENT_AUTHORIZATION_REJECTED = "APOPTOSIS_INDEPENDENT_AUTHORIZATION_REJECTED"

OBJECTIVE_INDEPENDENT_AUTHORIZATION_ONLY = "DECIDE_INDEPENDENT_AUTHORIZATION_ONLY"


@dataclass(frozen=True)
class ApoptosisIndependentAuthorizationPolicy:
    policy_id: str
    allowed_authority_ids: tuple[str, ...]
    allowed_authority_organization_ids: tuple[str, ...]
    allowed_objectives: tuple[str, ...]
    max_authorization_delay_seconds: int
    max_evidence_age_seconds: int
    require_source_external_review_recomputation: bool
    require_clear_external_review_source: bool
    require_source_subject_binding: bool
    require_source_artifact_binding: bool
    require_external_authority_designation_binding: bool
    require_authority_mandate: bool
    require_authority_qualification: bool
    require_independent_authority: bool
    require_conflict_disclosure: bool
    require_no_material_conflict: bool
    require_jurisdiction: bool
    require_quorum: bool
    require_reasoned_decision: bool
    require_proportionality_review: bool
    require_less_restrictive_alternatives_review: bool
    require_irreversibility_review: bool
    require_human_impact_review: bool
    require_appeal_route: bool
    require_dissent_route: bool
    require_protected_core_exclusion: bool
    require_no_institutional_hold: bool
    require_no_emergency_state: bool
    require_authorization_not_expired: bool
    require_execution_authority_separation: bool
    allow_authorization_record_issuance: bool
    allow_authorization_decision: bool
    allow_bounded_execution_preparation_next: bool
    allow_execution_request: bool
    allow_execution_decision: bool
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
        payload["allowed_authority_ids"] = list(self.allowed_authority_ids)
        payload["allowed_authority_organization_ids"] = list(
            self.allowed_authority_organization_ids
        )
        payload["allowed_objectives"] = list(self.allowed_objectives)
        return payload


def apoptosis_independent_authorization_policy_digest(
    policy: ApoptosisIndependentAuthorizationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisIndependentAuthorizationEvidence:
    evidence_id: str
    authorization_id: str
    authorization_authority_id: str
    authorization_authority_organization_id: str
    external_reviewer_id: str
    authority_mandate_receipt_digest: str
    authority_mandate_verified: bool
    authority_qualification_receipt_digest: str
    authority_qualification_verified: bool
    authority_independence_declaration_digest: str
    authority_independence_declared: bool
    conflict_of_interest_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    jurisdiction_receipt_digest: str
    jurisdiction_verified: bool
    quorum_receipt_digest: str
    quorum_satisfied: bool
    decision_rationale_digest: str
    reasoned_decision_complete: bool
    proportionality_review_digest: str
    proportionality_satisfied: bool
    alternatives_review_digest: str
    less_restrictive_alternatives_exhausted: bool
    irreversibility_review_digest: str
    irreversibility_review_complete: bool
    human_impact_review_digest: str
    human_impact_review_complete: bool
    subject_id: str
    subject_kind: str
    subject_version: str
    source_external_review_id: str
    source_observation_input_digest: str
    source_observation_policy_digest: str
    source_observation_record_digest: str
    source_candidate_request_digest: str
    source_candidate_policy_digest: str
    source_candidate_record_digest: str
    source_dependency_evidence_digest: str
    source_dependency_review_request_digest: str
    source_dependency_review_policy_digest: str
    source_dependency_review_record_digest: str
    source_authority_evidence_digest: str
    source_authority_review_request_digest: str
    source_authority_review_policy_digest: str
    source_authority_review_record_digest: str
    source_quiescence_evidence_digest: str
    source_quiescence_review_request_digest: str
    source_quiescence_review_policy_digest: str
    source_quiescence_review_record_digest: str
    source_external_review_evidence_digest: str
    source_external_review_request_digest: str
    source_external_review_policy_digest: str
    source_external_review_record_digest: str
    authorization_requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    authorization_completed_at_epoch_seconds: int
    authorization_expiry_at_epoch_seconds: int
    appeal_route_digest: str
    appeal_route_available: bool
    dissent_route_digest: str
    dissent_route_available: bool
    minority_opinion_receipt_digest: str
    protected_core_excluded: bool
    institutional_hold_active: bool
    emergency_state_active: bool
    evidence_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apoptosis_independent_authorization_evidence_digest(
    evidence: ApoptosisIndependentAuthorizationEvidence,
) -> str:
    payload = evidence.to_dict()
    payload.pop("evidence_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisIndependentAuthorizationRequest:
    authorization_id: str
    authority_id: str
    authority_organization_id: str
    objective: str
    requested_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    source_external_review_id: str
    source_external_review_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    authorization_evidence_digest: str
    future_execution_authority_id: str
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apoptosis_independent_authorization_request_digest(
    request: ApoptosisIndependentAuthorizationRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisIndependentAuthorizationRecord:
    authorization_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    authorization_evidence_digest: str
    source_external_review_id: str
    source_external_review_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    authority_id: str
    authority_organization_id: str
    objective: str
    requested_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    future_execution_authority_id: str
    source_recomputed_valid: bool
    source_external_review_clear: bool
    source_subject_binding_valid: bool
    source_artifact_binding_valid: bool
    external_authority_designation_binding_valid: bool
    authority_allowed: bool
    authority_organization_allowed: bool
    authority_identity_binding_valid: bool
    authority_mandate_verified: bool
    authority_qualification_verified: bool
    authority_independence_declared: bool
    authority_independent: bool
    independent_from_prior_chain: bool
    independent_from_future_execution_authority: bool
    objective_allowed: bool
    authorization_delay_valid: bool
    evidence_valid: bool
    evidence_fresh: bool
    authorization_time_order_valid: bool
    authorization_not_expired: bool
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    jurisdiction_verified: bool
    quorum_satisfied: bool
    reasoned_decision_complete: bool
    proportionality_satisfied: bool
    less_restrictive_alternatives_exhausted: bool
    irreversibility_review_complete: bool
    human_impact_review_complete: bool
    appeal_route_available: bool
    dissent_route_available: bool
    protected_core_excluded: bool
    institutional_hold_active: bool
    emergency_state_active: bool
    authorization_record_issued: bool
    authorization_decision_made: bool
    authorization_approved: bool
    authorization_denied: bool
    bounded_execution_preparation_allowed_next: bool
    execution_authority_required_next: bool
    execution_request_issued: bool
    execution_decision_made: bool
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


def apoptosis_independent_authorization_record_digest(
    record: ApoptosisIndependentAuthorizationRecord,
) -> str:
    payload = record.to_dict()
    payload.pop("record_digest", None)
    return canonical_digest(payload)
