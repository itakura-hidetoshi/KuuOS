#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_connection_evidence_review_attestation_v0_69 import (
    ExternalEvidenceReviewAttestation,
    attestation_digest,
    exact_review_scope,
)
from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    EXTERNAL_REVIEWER_CLASS,
    ConnectionEvidenceReviewRequest,
)


def seal_review_only_attestation(
    request: ConnectionEvidenceReviewRequest,
    *,
    attestation_id: str,
    reviewer_id: str,
    decision: str,
    valid_from_epoch: int,
    valid_through_epoch: int,
    reviewer_class: str = EXTERNAL_REVIEWER_CLASS,
) -> ExternalEvidenceReviewAttestation:
    if not attestation_id or not reviewer_id:
        raise ValueError("evidence_review_attestation_identity_missing")
    value = ExternalEvidenceReviewAttestation(
        attestation_id,
        reviewer_id,
        reviewer_class,
        decision,
        request.request_digest,
        request.evidence_capsule_digest,
        request.source_bundle_digest,
        request.rollback_bundle_digest,
        request.candidate_connection_digest,
        exact_review_scope(),
        valid_from_epoch,
        valid_through_epoch,
        False,
        False,
        False,
        False,
        "",
    )
    return replace(value, attestation_digest=attestation_digest(value))
