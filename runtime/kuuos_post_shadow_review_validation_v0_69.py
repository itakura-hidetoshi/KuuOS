#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    APPROVE_EVIDENCE,
    BLOCKED,
    MORE_EVIDENCE_REQUIRED,
    READY,
    REJECT_EVIDENCE,
    REJECTED,
    REQUEST_MORE_EVIDENCE,
    REVIEW_SCOPE,
    VERSION,
    ConnectionEvidenceReviewRequest,
    ExternalEvidenceReviewAttestation,
    ExternalEvidenceReviewRecord,
    evidence_review_record_digest,
)
from runtime.kuuos_connection_evidence_types_v0_68 import ConnectionEvidenceCapsule


def _valid_epoch(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def validate_external_evidence_review_record(
    record: ExternalEvidenceReviewRecord,
    capsule: ConnectionEvidenceCapsule,
    request: ConnectionEvidenceReviewRequest,
    attestation: ExternalEvidenceReviewAttestation,
    *,
    current_epoch: int,
) -> tuple[str, ...]:
    issues: list[str] = []
    if record.version != VERSION:
        issues.append("evidence_review_record_version_invalid")
    if record.record_digest != evidence_review_record_digest(record):
        issues.append("evidence_review_record_digest_invalid")
    expected = (
        request.request_digest,
        attestation.attestation_digest,
        capsule.capsule_digest,
        capsule.source_bundle_digest,
        capsule.rollback_bundle_digest,
        capsule.candidate_connection_digest,
        attestation.reviewer_id,
        attestation.reviewer_class,
        attestation.decision,
    )
    actual = (
        record.request_digest,
        record.attestation_digest,
        record.evidence_capsule_digest,
        record.source_bundle_digest,
        record.rollback_bundle_digest,
        record.candidate_connection_digest,
        record.reviewer_id,
        record.reviewer_class,
        record.decision,
    )
    if actual != expected:
        issues.append("evidence_review_record_digest_chain_mismatch")
    if record.review_scope != REVIEW_SCOPE:
        issues.append("evidence_review_record_scope_invalid")
    if not record.review_only:
        issues.append("evidence_review_record_not_review_only")
    if record.live_effect_allowed:
        issues.append("evidence_review_record_live_effect_invalid")
    return tuple(dict.fromkeys(issues))
