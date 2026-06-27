#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_connection_evidence_review_v0_69"
REQUEST_VERSION = "kuuos_connection_evidence_review_request_v0_69"
ATTESTATION_VERSION = "kuuos_connection_evidence_review_attestation_v0_69"

APPROVE_EVIDENCE = "APPROVE_EVIDENCE"
REJECT_EVIDENCE = "REJECT_EVIDENCE"
REQUEST_MORE_EVIDENCE = "REQUEST_MORE_EVIDENCE"
ALLOWED_DECISIONS = {
    APPROVE_EVIDENCE,
    REJECT_EVIDENCE,
    REQUEST_MORE_EVIDENCE,
}

READY = "READY_FOR_GOVERNED_ADMISSION_CANDIDATE"
REJECTED = "EVIDENCE_REVIEW_REJECTED"
MORE_EVIDENCE_REQUIRED = "MORE_EVIDENCE_REQUIRED"
BLOCKED = "CONNECTION_EVIDENCE_REVIEW_BLOCKED"

REVIEW_SCOPE = "external_post_shadow_evidence_review"
NEXT_STAGE_SCOPE = "governed_connection_admission_candidate"

EXTERNAL_HUMAN_REVIEWER = "external_human_reviewer"
GOVERNED_EVIDENCE_REVIEWER = "governed_evidence_reviewer"
ALLOWED_REVIEWER_CLASSES = {
    EXTERNAL_HUMAN_REVIEWER,
    GOVERNED_EVIDENCE_REVIEWER,
}


@dataclass(frozen=True)
class ConnectionEvidenceReviewRequest:
    request_id: str
    requested_by: str
    assigned_reviewer_id: str
    assigned_reviewer_class: str
    evidence_capsule_digest: str
    source_bundle_digest: str
    rollback_bundle_digest: str
    candidate_connection_digest: str
    requested_scope: str
    review_only: bool
    live_effect_requested: bool
    state_write_requested: bool
    authority_widening_requested: bool
    rollback_replacement_requested: bool
    request_digest: str
    version: str = REQUEST_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ConnectionEvidenceReviewAttestation:
    attestation_id: str
    reviewer_id: str
    reviewer_class: str
    decision: str
    bound_request_digest: str
    bound_evidence_capsule_digest: str
    bound_source_bundle_digest: str
    bound_rollback_bundle_digest: str
    bound_candidate_connection_digest: str
    allowed_scopes: tuple[str, ...]
    valid_from_epoch: int
    valid_through_epoch: int
    production_apply_allowed: bool
    live_effect_allowed: bool
    state_write_allowed: bool
    authority_widening_allowed: bool
    rollback_replacement_allowed: bool
    attestation_digest: str
    version: str = ATTESTATION_VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_scopes"] = list(self.allowed_scopes)
        return payload


@dataclass(frozen=True)
class ConnectionEvidenceReviewReceipt:
    status: str
    request_digest: str
    attestation_digest: str
    evidence_capsule_digest: str
    source_bundle_digest: str
    rollback_bundle_digest: str
    candidate_connection_digest: str
    reviewer_id: str
    reviewer_class: str
    decision: str
    review_scope: str
    next_stage_scope: str
    governed_admission_candidate: bool
    production_apply_ready: bool
    review_only: bool
    live_effect_performed: bool
    state_write_performed: bool
    authority_widened: bool
    rollback_target_replaced: bool
    immutable_receipt: bool
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        payload["warnings"] = list(self.warnings)
        return payload


def _digest_without(payload: dict[str, Any], field: str) -> str:
    value = dict(payload)
    value.pop(field, None)
    return canonical_digest(value)


def request_digest(request: ConnectionEvidenceReviewRequest) -> str:
    return _digest_without(request.to_dict(), "request_digest")


def attestation_digest(attestation: ConnectionEvidenceReviewAttestation) -> str:
    return _digest_without(attestation.to_dict(), "attestation_digest")


def receipt_digest(receipt: ConnectionEvidenceReviewReceipt) -> str:
    return _digest_without(receipt.to_dict(), "receipt_digest")
