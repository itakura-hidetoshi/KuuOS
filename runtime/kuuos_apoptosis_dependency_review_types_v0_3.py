#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_apoptosis_dependency_review_v0_3"

DEPENDENCY_REVIEW_CLEAR = (
    "APOPTOSIS_DEPENDENCY_REVIEW_CLEAR_FOR_FURTHER_REVIEW"
)
DEPENDENCY_REVIEW_BLOCKED = "APOPTOSIS_DEPENDENCY_REVIEW_BLOCKED"
DEPENDENCY_REVIEW_REJECTED = "APOPTOSIS_DEPENDENCY_REVIEW_REJECTED"

OBJECTIVE_DEPENDENCY_SAFETY_ONLY = "ASSESS_DEPENDENCY_SAFETY_ONLY"


@dataclass(frozen=True)
class ApoptosisDependencyReviewPolicy:
    policy_id: str
    allowed_reviewer_ids: tuple[str, ...]
    allowed_objectives: tuple[str, ...]
    max_review_delay_seconds: int
    max_evidence_age_seconds: int
    require_source_candidate_recomputation: bool
    require_proposed_candidate: bool
    require_candidate_subject_binding: bool
    require_snapshot_binding: bool
    require_complete_closure: bool
    require_no_cycle_through_subject: bool
    require_no_orphaned_dependents: bool
    require_no_unresolved_dependencies: bool
    require_no_uncovered_critical_dependents: bool
    require_no_active_execution_dependence: bool
    require_replacement_coverage_for_dependents: bool
    require_authority_review_next: bool
    require_quiescence_review_next: bool
    require_external_review_next: bool
    require_independent_authorization_next: bool
    allow_dependency_review_record_issuance: bool
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


def apoptosis_dependency_review_policy_digest(
    policy: ApoptosisDependencyReviewPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisDependencyEvidence:
    evidence_id: str
    subject_id: str
    subject_kind: str
    subject_version: str
    captured_at_epoch_seconds: int
    dependency_snapshot_digest: str
    graph_snapshot_digest: str
    direct_dependency_ids: tuple[str, ...]
    direct_dependent_ids: tuple[str, ...]
    critical_dependent_ids: tuple[str, ...]
    replacement_covered_dependent_ids: tuple[str, ...]
    unresolved_dependency_ids: tuple[str, ...]
    cycle_member_ids: tuple[str, ...]
    active_execution_dependent_ids: tuple[str, ...]
    closure_complete: bool
    evidence_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for field_name in (
            "direct_dependency_ids",
            "direct_dependent_ids",
            "critical_dependent_ids",
            "replacement_covered_dependent_ids",
            "unresolved_dependency_ids",
            "cycle_member_ids",
            "active_execution_dependent_ids",
        ):
            payload[field_name] = list(getattr(self, field_name))
        return payload


def apoptosis_dependency_evidence_digest(
    evidence: ApoptosisDependencyEvidence,
) -> str:
    payload = evidence.to_dict()
    payload.pop("evidence_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisDependencyReviewRequest:
    review_id: str
    reviewer_id: str
    objective: str
    reviewed_at_epoch_seconds: int
    source_candidate_id: str
    source_candidate_digest: str
    source_candidate_request_digest: str
    source_candidate_policy_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    dependency_snapshot_digest: str
    dependency_evidence_digest: str
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apoptosis_dependency_review_request_digest(
    request: ApoptosisDependencyReviewRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisDependencyReviewRecord:
    review_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    source_candidate_id: str
    source_candidate_digest: str
    source_candidate_request_digest: str
    source_candidate_policy_digest: str
    dependency_evidence_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    reviewer_id: str
    objective: str
    reviewed_at_epoch_seconds: int
    source_recomputed_valid: bool
    source_candidate_proposed: bool
    source_subject_binding_valid: bool
    source_dependency_snapshot_binding_valid: bool
    source_candidate_binding_valid: bool
    reviewer_allowed: bool
    objective_allowed: bool
    review_delay_valid: bool
    evidence_valid: bool
    evidence_fresh: bool
    evidence_subject_binding_valid: bool
    evidence_snapshot_binding_valid: bool
    closure_complete: bool
    cycle_through_subject_present: bool
    unresolved_dependencies_present: bool
    orphaned_dependents_present: bool
    uncovered_critical_dependents_present: bool
    active_execution_dependence_present: bool
    replacement_coverage_complete: bool
    dependency_clear_for_further_review: bool
    dependency_review_record_issued: bool
    authority_review_required_next: bool
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


def apoptosis_dependency_review_record_digest(
    record: ApoptosisDependencyReviewRecord,
) -> str:
    payload = record.to_dict()
    payload.pop("record_digest", None)
    return canonical_digest(payload)
