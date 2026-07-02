#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_apoptosis_quiescence_review_v0_5"

QUIESCENCE_REVIEW_CLEAR = (
    "APOPTOSIS_QUIESCENCE_REVIEW_CLEAR_FOR_EXTERNAL_REVIEW"
)
QUIESCENCE_REVIEW_BLOCKED = "APOPTOSIS_QUIESCENCE_REVIEW_BLOCKED"
QUIESCENCE_REVIEW_REJECTED = "APOPTOSIS_QUIESCENCE_REVIEW_REJECTED"

OBJECTIVE_QUIESCENCE_SAFETY_ONLY = "ASSESS_QUIESCENCE_SAFETY_ONLY"


@dataclass(frozen=True)
class ApoptosisQuiescenceReviewPolicy:
    policy_id: str
    allowed_reviewer_ids: tuple[str, ...]
    allowed_objectives: tuple[str, ...]
    max_review_delay_seconds: int
    max_evidence_age_seconds: int
    minimum_grace_period_seconds: int
    require_source_authority_review_recomputation: bool
    require_clear_authority_source: bool
    require_source_subject_binding: bool
    require_execution_snapshot_binding: bool
    require_independent_reviewer: bool
    require_complete_quiescence_closure: bool
    require_no_active_execution: bool
    require_no_pending_work: bool
    require_no_active_lease: bool
    require_new_intake_stopped: bool
    require_no_open_intake_channel: bool
    require_no_blocking_external_dependency: bool
    require_verified_drain: bool
    require_verified_checkpoint: bool
    require_verified_recovery_route: bool
    require_reentry_possible: bool
    require_valid_quiescence_time_order: bool
    require_grace_period_elapsed: bool
    require_no_emergency_operation: bool
    require_external_review_next: bool
    require_independent_authorization_next: bool
    allow_quiescence_review_record_issuance: bool
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


def apoptosis_quiescence_review_policy_digest(
    policy: ApoptosisQuiescenceReviewPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisQuiescenceEvidence:
    evidence_id: str
    subject_id: str
    subject_kind: str
    subject_version: str
    captured_at_epoch_seconds: int
    execution_snapshot_digest: str
    work_snapshot_digest: str
    intake_snapshot_digest: str
    state_checkpoint_digest: str
    drain_plan_digest: str
    recovery_route_digest: str
    active_execution_ids: tuple[str, ...]
    pending_work_ids: tuple[str, ...]
    critical_pending_work_ids: tuple[str, ...]
    active_lease_ids: tuple[str, ...]
    intake_channel_ids: tuple[str, ...]
    open_intake_channel_ids: tuple[str, ...]
    blocking_external_dependency_ids: tuple[str, ...]
    quiescence_closure_complete: bool
    new_intake_stopped: bool
    drain_verified: bool
    checkpoint_verified: bool
    recovery_route_verified: bool
    reentry_possible: bool
    quiescence_started_at_epoch_seconds: int
    last_activity_at_epoch_seconds: int
    emergency_operation_active: bool
    evidence_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for field_name in (
            "active_execution_ids",
            "pending_work_ids",
            "critical_pending_work_ids",
            "active_lease_ids",
            "intake_channel_ids",
            "open_intake_channel_ids",
            "blocking_external_dependency_ids",
        ):
            payload[field_name] = list(getattr(self, field_name))
        return payload


def apoptosis_quiescence_evidence_digest(
    evidence: ApoptosisQuiescenceEvidence,
) -> str:
    payload = evidence.to_dict()
    payload.pop("evidence_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisQuiescenceReviewRequest:
    review_id: str
    reviewer_id: str
    objective: str
    reviewed_at_epoch_seconds: int
    source_authority_review_id: str
    source_authority_review_digest: str
    source_authority_review_request_digest: str
    source_authority_review_policy_digest: str
    source_authority_evidence_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    execution_snapshot_digest: str
    quiescence_evidence_digest: str
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apoptosis_quiescence_review_request_digest(
    request: ApoptosisQuiescenceReviewRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class ApoptosisQuiescenceReviewRecord:
    review_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    source_authority_review_id: str
    source_authority_review_digest: str
    source_authority_review_request_digest: str
    source_authority_review_policy_digest: str
    source_authority_evidence_digest: str
    quiescence_evidence_digest: str
    subject_id: str
    subject_kind: str
    subject_version: str
    reviewer_id: str
    objective: str
    reviewed_at_epoch_seconds: int
    source_recomputed_valid: bool
    source_authority_clear: bool
    source_subject_binding_valid: bool
    source_execution_snapshot_binding_valid: bool
    source_authority_review_binding_valid: bool
    reviewer_allowed: bool
    reviewer_independent: bool
    objective_allowed: bool
    review_delay_valid: bool
    evidence_valid: bool
    evidence_fresh: bool
    evidence_subject_binding_valid: bool
    evidence_snapshot_binding_valid: bool
    quiescence_closure_complete: bool
    active_execution_present: bool
    pending_work_present: bool
    critical_pending_work_present: bool
    active_lease_present: bool
    new_intake_stopped: bool
    open_intake_present: bool
    blocking_external_dependency_present: bool
    drain_verified: bool
    checkpoint_verified: bool
    recovery_route_verified: bool
    reentry_possible: bool
    quiescence_time_order_valid: bool
    grace_period_elapsed: bool
    emergency_operation_active: bool
    quiescence_clear_for_external_review: bool
    quiescence_review_record_issued: bool
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


def apoptosis_quiescence_review_record_digest(
    record: ApoptosisQuiescenceReviewRecord,
) -> str:
    payload = record.to_dict()
    payload.pop("record_digest", None)
    return canonical_digest(payload)
