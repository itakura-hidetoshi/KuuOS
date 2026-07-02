#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_apoptosis_authority_review_v0_4"

AUTHORITY_REVIEW_CLEAR = "APOPTOSIS_AUTHORITY_REVIEW_CLEAR_FOR_QUIESCENCE_REVIEW"
AUTHORITY_REVIEW_BLOCKED = "APOPTOSIS_AUTHORITY_REVIEW_BLOCKED"
AUTHORITY_REVIEW_REJECTED = "APOPTOSIS_AUTHORITY_REVIEW_REJECTED"

OBJECTIVE_AUTHORITY_SAFETY_ONLY = "ASSESS_AUTHORITY_SAFETY_ONLY"


@dataclass(frozen=True)
class ApoptosisAuthorityReviewPolicy:
    policy_id: str
    allowed_reviewer_ids: tuple[str, ...]
    allowed_objectives: tuple[str, ...]
    max_review_delay_seconds: int
    max_evidence_age_seconds: int
    require_source_dependency_review_recomputation: bool
    require_clear_dependency_source: bool
    require_source_subject_binding: bool
    require_authority_snapshot_binding: bool
    require_complete_authority_closure: bool
    require_responsible_authority: bool
    require_responsibility_acknowledgement: bool
    require_independent_reviewer: bool
    require_no_subject_control_of_responsible_authority: bool
    require_no_institutional_hold: bool
    require_no_constitutional_protection: bool
    require_no_protected_authority: bool
    require_complete_delegation_chain: bool
    require_no_unresolved_authority: bool
    require_no_authority_cycle: bool
    require_no_emergency_override: bool
    require_quiescence_review_next: bool
    require_external_review_next: bool
    require_independent_authorization_next: bool
    allow_authority_review_record_issuance: bool
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
        payload["allowed_objectives"] = list(self.allowed_objectives)
        return payload


def apoptosis_authority_review_policy_digest(
    policy: ApoptosisAuthorityReviewPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisAuthorityEvidence:
    evidence_id: str
    subject_id: str
    subject_kind: str
    subject_version: str
    captured_at_epoch_seconds: int
    authority_snapshot_digest: str
    authority_graph_snapshot_digest: str
    responsible_authority_id: str
    active_authority_ids: tuple[str, ...]
    delegation_chain_ids: tuple[str, ...]
    protected_authority_ids: tuple[str, ...]
    unresolved_authority_ids: tuple[str, ...]
    cycle_member_ids: tuple[str, ...]
    authority_closure_complete: bool
    delegation_chain_complete: bool
    responsibility_acknowledged: bool
    subject_controls_responsible_authority: bool
    institutional_hold: bool
    constitutional_protected: bool
    emergency_override_active: bool
    evidence_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for field_name in (
            "active_authority_ids",
            "delegation_chain_ids",
            "protected_authority_ids",
            "unresolved_authority_ids",
            "cycle_member_ids",
        ):
            payload[field_name] = list(getattr(self, field_name))
        return payload


def apoptosis_authority_evidence_digest(
    evidence: ApoptosisAuthorityEvidence,
) -> str:
    payload = evidence.to_dict()
    payload.pop("evidence_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisAuthorityReviewRequest:
    review_id: str
    reviewer_id: str
    objective: str
    reviewed_at_epoch_seconds: int
    source_dependency_review_id: str
    source_dependency_review_digest: str
    source_dependency_review_request_digest: str
    source_dependency_review_policy_digest: str
    source_dependency_evidence_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    authority_snapshot_digest: str
    authority_evidence_digest: str
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apoptosis_authority_review_request_digest(
    request: ApoptosisAuthorityReviewRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisAuthorityReviewRecord:
    review_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    source_dependency_review_id: str
    source_dependency_review_digest: str
    source_dependency_review_request_digest: str
    source_dependency_review_policy_digest: str
    source_dependency_evidence_digest: str
    authority_evidence_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    reviewer_id: str
    objective: str
    reviewed_at_epoch_seconds: int
    source_recomputed_valid: bool
    source_dependency_clear: bool
    source_subject_binding_valid: bool
    source_authority_snapshot_binding_valid: bool
    source_dependency_review_binding_valid: bool
    reviewer_allowed: bool
    reviewer_independent: bool
    objective_allowed: bool
    review_delay_valid: bool
    evidence_valid: bool
    evidence_fresh: bool
    evidence_subject_binding_valid: bool
    evidence_snapshot_binding_valid: bool
    authority_closure_complete: bool
    responsible_authority_present: bool
    responsibility_acknowledged: bool
    delegation_chain_complete: bool
    subject_controls_responsible_authority: bool
    institutional_hold_present: bool
    constitutional_protection_present: bool
    protected_authority_present: bool
    unresolved_authority_present: bool
    authority_cycle_present: bool
    emergency_override_active: bool
    authority_clear_for_quiescence_review: bool
    authority_review_record_issued: bool
    quiescence_review_required_next: bool
    external_review_required_next: bool
    independent_authorization_required_next: bool
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


def apoptosis_authority_review_record_digest(
    record: ApoptosisAuthorityReviewRecord,
) -> str:
    payload = record.to_dict()
    payload.pop("record_digest", None)
    return canonical_digest(payload)
