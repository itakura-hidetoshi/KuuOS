#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_connection_evidence_review_types_v0_69 import VERSION
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest


@dataclass(frozen=True)
class ExternalEvidenceReviewRecord:
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
    governed_admission_candidate: bool
    review_only: bool
    live_effect_allowed: bool
    state_write_performed: bool
    authority_widened: bool
    rollback_target_replaced: bool
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    record_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        payload["warnings"] = list(self.warnings)
        return payload


def evidence_review_record_digest(record: ExternalEvidenceReviewRecord) -> str:
    payload = record.to_dict()
    payload.pop("record_digest", None)
    return canonical_digest(payload)
