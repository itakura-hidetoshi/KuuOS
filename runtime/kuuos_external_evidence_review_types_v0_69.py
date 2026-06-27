#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_external_evidence_review_v0_69"
REQUEST_READY = "READY_FOR_EXTERNAL_EVIDENCE_REVIEW"
REQUEST_BLOCKED = "EXTERNAL_EVIDENCE_REVIEW_REQUEST_BLOCKED"
REVIEW_BLOCKED = "EXTERNAL_EVIDENCE_REVIEW_BLOCKED"
APPROVE_EVIDENCE = "APPROVE_EVIDENCE"
REJECT_EVIDENCE = "REJECT_EVIDENCE"
REQUEST_MORE_EVIDENCE = "REQUEST_MORE_EVIDENCE"
APPROVED = "EVIDENCE_APPROVED_FOR_GOVERNED_PRODUCTION_ADMISSION"
REJECTED = "EVIDENCE_REJECTED"
MORE_EVIDENCE_REQUIRED = "MORE_EVIDENCE_REQUIRED"
REVIEW_SCOPE = "external_post_shadow_evidence_review"
HUMAN_REVIEWER = "HUMAN_REVIEWER"
GOVERNED_REVIEWER = "GOVERNED_REVIEWER"
ALLOWED_REVIEWER_CLASSES = (HUMAN_REVIEWER, GOVERNED_REVIEWER)
ALLOWED_DECISIONS = (APPROVE_EVIDENCE, REJECT_EVIDENCE, REQUEST_MORE_EVIDENCE)


@dataclass(frozen=True)
class ExternalEvidenceReviewRequest:
    status: str
    request_id: str
    review_scope: str
    evidence_capsule_digest: str
    source_bundle_digest: str
    rollback_bundle_digest: str
    candidate_connection_digest: str
    valid_from_epoch: int
    valid_through_epoch: int
    production_admission_requested: bool
    blockers: tuple[str, ...]
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return payload


@dataclass(frozen=True)
class ExternalEvidenceReviewReceipt:
    status: str
    review_id: str
    request_digest: str
    evidence_capsule_digest: str
    source_bundle_digest: str
    rollback_bundle_digest: str
    candidate_connection_digest: str
    reviewer_id: str
    reviewer_class: str
    review_scope: str
    decision: str
    rationale_digest: str
    valid_from_epoch: int
    valid_through_epoch: int
    production_admission_granted: bool
    live_effect_performed: bool
    state_write_performed: bool
    scope_widened: bool
    rollback_target_replaced: bool
    immutable_receipt: bool
    blockers: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return payload


def review_request_digest(request: ExternalEvidenceReviewRequest) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


def review_receipt_digest(receipt: ExternalEvidenceReviewReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
