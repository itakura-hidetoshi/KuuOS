#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_connection_evidence_review_types_v0_69 import REVIEW_SCOPE
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

ATTESTATION_VERSION = "kuuos_connection_evidence_review_attestation_v0_69"


@dataclass(frozen=True)
class ExternalEvidenceReviewAttestation:
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
    state_write_allowed: bool
    authority_widening_allowed: bool
    rollback_replacement_allowed: bool
    attestation_digest: str
    version: str = ATTESTATION_VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_scopes"] = list(self.allowed_scopes)
        return payload


def attestation_digest(attestation: ExternalEvidenceReviewAttestation) -> str:
    payload = attestation.to_dict()
    payload.pop("attestation_digest", None)
    return canonical_digest(payload)


def exact_review_scope() -> tuple[str, ...]:
    return (REVIEW_SCOPE,)
