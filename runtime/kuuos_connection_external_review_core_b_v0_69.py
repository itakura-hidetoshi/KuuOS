#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from runtime.kuuos_connection_evidence_review_attestation_v0_69 import (
    ATTESTATION_VERSION,
    ExternalEvidenceReviewAttestation,
    attestation_digest,
    exact_review_scope,
)
from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    ALLOWED_DECISIONS,
    EXTERNAL_REVIEWER_CLASS,
    ConnectionEvidenceReviewRequest,
)
from runtime.kuuos_connection_evidence_types_v0_68 import ConnectionEvidenceCapsule


def valid_epoch(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def review_attestation_issues(
    capsule: ConnectionEvidenceCapsule,
    request: ConnectionEvidenceReviewRequest,
    attestation: ExternalEvidenceReviewAttestation,
    *,
    current_epoch: int,
) -> tuple[str, ...]:
    issues: list[str] = []
    if attestation.version != ATTESTATION_VERSION:
        issues.append("evidence_review_attestation_version_invalid")
    if attestation.attestation_digest != attestation_digest(attestation):
        issues.append("evidence_review_attestation_digest_invalid")
    if not attestation.attestation_id or not attestation.reviewer_id:
        issues.append("evidence_review_attestation_identity_missing")
    if attestation.reviewer_id != request.assigned_reviewer_id:
        issues.append("evidence_review_reviewer_identity_mismatch")
    if attestation.reviewer_class != request.assigned_reviewer_class:
        issues.append("evidence_review_reviewer_class_mismatch")
    if attestation.reviewer_class != EXTERNAL_REVIEWER_CLASS:
        issues.append("evidence_review_reviewer_class_invalid")
    if attestation.decision not in ALLOWED_DECISIONS:
        issues.append("evidence_review_decision_invalid")

    expected = (
        request.request_digest,
        capsule.capsule_digest,
        capsule.source_bundle_digest,
        capsule.rollback_bundle_digest,
        capsule.candidate_connection_digest,
    )
    actual = (
        attestation.bound_request_digest,
        attestation.bound_evidence_capsule_digest,
        attestation.bound_source_bundle_digest,
        attestation.bound_rollback_bundle_digest,
        attestation.bound_candidate_connection_digest,
    )
    if actual != expected:
        issues.append("evidence_review_attestation_digest_chain_mismatch")
    if attestation.allowed_scopes != exact_review_scope():
        issues.append("evidence_review_attestation_scope_invalid")
    if attestation.production_apply_allowed:
        issues.append("evidence_review_production_apply_forbidden")
    if attestation.live_effect_allowed:
        issues.append("evidence_review_live_effect_forbidden")
    flags = (
        not attestation.state_write_allowed,
        not attestation.authority_widening_allowed,
        not attestation.rollback_replacement_allowed,
    )
    if not all(flags):
        issues.append("evidence_review_attestation_boundary_invalid")

    start = attestation.valid_from_epoch
    end = attestation.valid_through_epoch
    if not valid_epoch(current_epoch) or not valid_epoch(start) or not valid_epoch(end):
        issues.append("evidence_review_epoch_invalid")
    elif start > end:
        issues.append("evidence_review_validity_window_invalid")
    else:
        if not start <= current_epoch <= end:
            issues.append("evidence_review_outside_validity_window")
        if start < capsule.valid_from_epoch or end > capsule.valid_through_epoch:
            issues.append("evidence_review_window_exceeds_capsule")
    return tuple(issues)
