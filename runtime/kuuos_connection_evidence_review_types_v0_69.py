#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_connection_external_evidence_review_v0_69"
REQUEST_VERSION = "kuuos_connection_evidence_review_request_v0_69"
REVIEW_SCOPE = "external_post_shadow_evidence_review"
EXTERNAL_REVIEWER_CLASS = "external_human_or_governed_evidence_reviewer"

APPROVE_EVIDENCE = "APPROVE_EVIDENCE"
REJECT_EVIDENCE = "REJECT_EVIDENCE"
REQUEST_MORE_EVIDENCE = "REQUEST_MORE_EVIDENCE"
ALLOWED_DECISIONS = {APPROVE_EVIDENCE, REJECT_EVIDENCE, REQUEST_MORE_EVIDENCE}

READY = "READY_FOR_GOVERNED_ADMISSION_CANDIDATE"
REJECTED = "EVIDENCE_REVIEW_REJECTED"
MORE_EVIDENCE_REQUIRED = "MORE_EVIDENCE_REQUIRED"
BLOCKED = "EXTERNAL_EVIDENCE_REVIEW_BLOCKED"


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
    evidence_only: bool
    live_effect_requested: bool
    state_write_requested: bool
    authority_widening_requested: bool
    rollback_replacement_requested: bool
    request_digest: str
    version: str = REQUEST_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def request_digest(request: ConnectionEvidenceReviewRequest) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)
