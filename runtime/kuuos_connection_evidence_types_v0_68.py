#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_connection_evidence_capsule_v0_68"
READY = "READY_FOR_EXTERNAL_EVIDENCE_REVIEW"
BLOCKED = "CONNECTION_EVIDENCE_CAPSULE_BLOCKED"
REVIEW_SCOPE = "post_shadow_connection_review"


@dataclass(frozen=True)
class ConnectionEvidenceCapsule:
    status: str
    capsule_id: str
    review_scope: str
    source_bundle_digest: str
    shadow_bundle_digest: str
    staging_package_digest: str
    shadow_receipt_digest: str
    gauge_validation_digest: str
    candidate_connection_digest: str
    rollback_bundle_digest: str
    sample_count: int
    valid_from_epoch: int
    valid_through_epoch: int
    evidence_only: bool
    candidate_only: bool
    live_effect_allowed: bool
    state_write_allowed: bool
    authority_widening_allowed: bool
    blockers: tuple[str, ...]
    capsule_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return payload


def capsule_digest(capsule: ConnectionEvidenceCapsule) -> str:
    payload = capsule.to_dict()
    payload.pop("capsule_digest", None)
    return canonical_digest(payload)
