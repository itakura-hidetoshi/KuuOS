#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    EXTERNAL_REVIEWER_CLASS,
    REQUEST_VERSION,
    REVIEW_SCOPE,
    ConnectionEvidenceReviewRequest,
    request_digest,
)
from runtime.kuuos_connection_evidence_types_v0_68 import ConnectionEvidenceCapsule


def review_request_issues(
    capsule: ConnectionEvidenceCapsule,
    request: ConnectionEvidenceReviewRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    if request.version != REQUEST_VERSION:
        issues.append("evidence_review_request_version_invalid")
    if request.request_digest != request_digest(request):
        issues.append("evidence_review_request_digest_invalid")
    if not request.request_id or not request.requested_by:
        issues.append("evidence_review_request_identity_missing")
    if not request.assigned_reviewer_id:
        issues.append("evidence_review_assigned_reviewer_missing")
    if request.assigned_reviewer_class != EXTERNAL_REVIEWER_CLASS:
        issues.append("evidence_review_assigned_reviewer_class_invalid")
    expected = (
        capsule.capsule_digest,
        capsule.source_bundle_digest,
        capsule.rollback_bundle_digest,
        capsule.candidate_connection_digest,
    )
    actual = (
        request.evidence_capsule_digest,
        request.source_bundle_digest,
        request.rollback_bundle_digest,
        request.candidate_connection_digest,
    )
    if actual != expected:
        issues.append("evidence_review_request_digest_chain_mismatch")
    if request.requested_scope != REVIEW_SCOPE:
        issues.append("evidence_review_request_scope_invalid")
    flags = (
        request.evidence_only,
        not request.live_effect_requested,
        not request.state_write_requested,
        not request.authority_widening_requested,
        not request.rollback_replacement_requested,
    )
    if not all(flags):
        issues.append("evidence_review_request_boundary_invalid")
    return tuple(issues)
