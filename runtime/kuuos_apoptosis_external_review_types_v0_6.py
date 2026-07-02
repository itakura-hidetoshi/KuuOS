#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_apoptosis_external_review_v0_6"

EXTERNAL_REVIEW_CLEAR = (
    "APOPTOSIS_EXTERNAL_REVIEW_CLEAR_FOR_INDEPENDENT_AUTHORIZATION"
)
EXTERNAL_REVIEW_BLOCKED = "APOPTOSIS_EXTERNAL_REVIEW_BLOCKED"
EXTERNAL_REVIEW_REJECTED = "APOPTOSIS_EXTERNAL_REVIEW_REJECTED"

OBJECTIVE_EXTERNAL_REVIEW_ONLY = "ASSESS_EXTERNAL_REVIEW_ONLY"


@dataclass(frozen=True)
class ApoptosisExternalReviewPolicy:
    policy_id: str
    allowed_reviewer_ids: tuple[str, ...]
    allowed_reviewer_organization_ids: tuple[str, ...]
    allowed_objectives: tuple[str, ...]
    max_review_delay_seconds: int
    max_evidence_age_seconds: int
    require_source_quiescence_review_recomputation: bool
    require_clear_quiescence_source: bool
    require_source_subject_binding: bool
    require_source_artifact_binding: bool
    require_qualified_reviewer: bool
    require_independent_reviewer: bool
    require_conflict_disclosure: bool
    require_no_material_conflict: bool
    require_complete_review_scope: bool
    require_review_methodology: bool
    require_complete_evidence_receipt: bool
    require_appeal_route: bool
    require_dissent_route: bool
    require_protected_core_exclusion: bool
    require_no_institutional_hold: bool
    require_no_emergency_state: bool
    require_review_not_expired: bool
    require_future_authority_separation: bool
    require_independent_authorization_next: bool
    allow_external_review_record_issuance: bool
    allow_authorization_request: bool
    allow_authorization_decision: bool
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
        payload["allowed_reviewer_ids"] = list(self.allowed_reviewer_ids)
        payload["allowed_reviewer_organization_ids"] = list(
            self.allowed_reviewer_organization_ids
        )
        payload["allowed_objectives"] = list(self.allowed_objectives)
        return payload


def apoptosis_external_review_policy_digest(
    policy: ApoptosisExternalReviewPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisExternalReviewEvidence:
    evidence_id: str
    external_review_id: str
    external_reviewer_id: str
    external_reviewer_organization_id: str
    quiescence_evidence_producer_id: str
    reviewer_qualification_receipt_digest: str
    reviewer_qualification_verified: bool
    reviewer_independence_declaration_digest: str
    reviewer_independence_declared: bool
    conflict_of_interest_disclosure_digest: str
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    institutional_affiliation_digest: str
    review_scope: str
    review_scope_complete: bool
    review_methodology_digest: str
    review_evidence_receipt_digest: str
    review_evidence_receipt_complete: bool
    subject_id: str
    subject_kind: str
    subject_version: str
    source_quiescence_review_id: str
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
    review_requested_at_epoch_seconds: int
    captured_at_epoch_seconds: int
    review_completed_at_epoch_seconds: int
    review_expiry_at_epoch_seconds: int
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


def apoptosis_external_review_evidence_digest(
    evidence: ApoptosisExternalReviewEvidence,
) -> str:
    payload = evidence.to_dict()
    payload.pop("evidence_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisExternalReviewRequest:
    review_id: str
    reviewer_id: str
    reviewer_organization_id: str
    objective: str
    requested_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    source_quiescence_review_id: str
    source_quiescence_review_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    external_review_evidence_digest: str
    future_authorization_authority_id: str
    future_execution_authority_id: str
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apoptosis_external_review_request_digest(
    request: ApoptosisExternalReviewRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisExternalReviewRecord:
    review_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    external_review_evidence_digest: str
    source_quiescence_review_id: str
    source_quiescence_review_record_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    reviewer_id: str
    reviewer_organization_id: str
    objective: str
    requested_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    future_authorization_authority_id: str
    future_execution_authority_id: str
    source_recomputed_valid: bool
    source_quiescence_clear: bool
    source_subject_binding_valid: bool
    source_artifact_binding_valid: bool
    reviewer_allowed: bool
    reviewer_organization_allowed: bool
    reviewer_identity_binding_valid: bool
    reviewer_qualified: bool
    reviewer_independence_declared: bool
    reviewer_independent: bool
    independent_from_prior_chain: bool
    independent_from_future_authorization_authority: bool
    independent_from_future_execution_authority: bool
    objective_allowed: bool
    review_delay_valid: bool
    evidence_valid: bool
    evidence_fresh: bool
    review_time_order_valid: bool
    review_not_expired: bool
    conflict_disclosure_complete: bool
    material_conflict_present: bool
    review_scope_complete: bool
    review_methodology_present: bool
    evidence_receipt_complete: bool
    appeal_route_available: bool
    dissent_route_available: bool
    protected_core_excluded: bool
    institutional_hold_active: bool
    emergency_state_active: bool
    external_clear_for_independent_authorization: bool
    external_review_record_issued: bool
    independent_authorization_required_next: bool
    authorization_request_issued: bool
    authorization_decision_made: bool
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


def apoptosis_external_review_record_digest(
    record: ApoptosisExternalReviewRecord,
) -> str:
    payload = record.to_dict()
    payload.pop("record_digest", None)
    return canonical_digest(payload)
