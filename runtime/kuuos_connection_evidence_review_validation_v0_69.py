#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_connection_evidence_review_attestation_v0_69 import (
    ExternalEvidenceReviewAttestation,
)
from runtime.kuuos_connection_evidence_review_record_v0_69 import (
    ExternalEvidenceReviewRecord,
    evidence_review_record_digest,
)
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
)
from runtime.kuuos_connection_evidence_types_v0_68 import ConnectionEvidenceCapsule
from runtime.kuuos_connection_external_review_core_b_v0_69 import valid_epoch


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
    boundaries = (
        record.review_only,
        not record.live_effect_allowed,
        not record.state_write_performed,
        not record.authority_widened,
        not record.rollback_target_replaced,
    )
    if not all(boundaries):
        issues.append("evidence_review_record_boundary_invalid")

    if record.blockers:
        expected_status, expected_candidate = BLOCKED, False
    elif record.decision == APPROVE_EVIDENCE:
        expected_status, expected_candidate = READY, True
    elif record.decision == REJECT_EVIDENCE:
        expected_status, expected_candidate = REJECTED, False
    elif record.decision == REQUEST_MORE_EVIDENCE:
        expected_status, expected_candidate = MORE_EVIDENCE_REQUIRED, False
    else:
        expected_status, expected_candidate = BLOCKED, False
    if record.status != expected_status:
        issues.append("evidence_review_record_status_invalid")
    if record.governed_admission_candidate != expected_candidate:
        issues.append("evidence_review_record_candidate_scope_invalid")

    if not valid_epoch(current_epoch):
        issues.append("evidence_review_record_epoch_invalid")
    elif not (
        capsule.valid_from_epoch <= current_epoch <= capsule.valid_through_epoch
        and attestation.valid_from_epoch <= current_epoch <= attestation.valid_through_epoch
    ):
        issues.append("evidence_review_record_outside_validity_window")
    return tuple(dict.fromkeys(issues))
