#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_external_evidence_review_v0_69"
APPROVE_EVIDENCE = "APPROVE_EVIDENCE"
REJECT_EVIDENCE = "REJECT_EVIDENCE"
REQUEST_MORE_EVIDENCE = "REQUEST_MORE_EVIDENCE"
ALLOWED_DECISIONS = (APPROVE_EVIDENCE, REJECT_EVIDENCE, REQUEST_MORE_EVIDENCE)
REVIEW_SCOPE = "external_post_shadow_evidence_review"
ALLOWED_REVIEWER_CLASSES = ("HUMAN_REVIEWER", "GOVERNED_REVIEWER")
READY = "READY_FOR_EXTERNAL_EVIDENCE_REVIEW"
BLOCKED = "EXTERNAL_EVIDENCE_REVIEW_BLOCKED"


@dataclass(frozen=True)
class ExternalEvidenceReviewRequest:
    request_id: str
    evidence_capsule_digest: str
    source_bundle_digest: str
    rollback_bundle_digest: str
    candidate_connection_digest: str
    valid_from_epoch: int
    valid_through_epoch: int
    review_scope: str
    request_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


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
    decision: str
    rationale_digest: str
    valid_from_epoch: int
    valid_through_epoch: int
    review_scope: str
    immutable_receipt: bool
    next_stage_candidate: bool
    blockers: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return payload


def request_digest(request: ExternalEvidenceReviewRequest) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


def receipt_digest(receipt: ExternalEvidenceReviewReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
