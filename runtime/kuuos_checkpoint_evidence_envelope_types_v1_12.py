#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_checkpoint_evidence_envelope_v1_12"
ENVELOPE_READY = "CHECKPOINT_EVIDENCE_ENVELOPE_READY"
ENVELOPE_CONFLICT = "CHECKPOINT_EVIDENCE_ENVELOPE_CONFLICT"
ENVELOPE_NONE = "CHECKPOINT_EVIDENCE_ENVELOPE_NONE"
ENVELOPE_REJECTED = "CHECKPOINT_EVIDENCE_ENVELOPE_REJECTED"


@dataclass(frozen=True)
class CheckpointEvidenceEnvelope:
    envelope_id: str
    status: str
    contract_digest: str
    validation_digest: str
    candidate_digest: str
    repository_id: str
    checkpoint_reference: str
    expected_current_oid: str
    observed_current_oid: str
    proposed_checkpoint_oid: str
    contract_valid: bool
    validation_valid: bool
    candidate_match: bool
    repository_match: bool
    checkpoint_match: bool
    expected_oid_match: bool
    proposed_oid_match: bool
    upstream_revalidated: bool
    eligible: bool
    operation_performed: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    envelope_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def checkpoint_evidence_envelope_digest(envelope: CheckpointEvidenceEnvelope) -> str:
    payload = envelope.to_dict()
    payload.pop("envelope_digest", None)
    return canonical_digest(payload)
