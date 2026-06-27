#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    EXTERNAL_REVIEWER_CLASS,
    REVIEW_SCOPE,
    ConnectionEvidenceReviewRequest,
    request_digest,
)
from runtime.kuuos_connection_evidence_types_v0_68 import (
    READY as EVIDENCE_READY,
    ConnectionEvidenceCapsule,
    capsule_digest,
)


def build_external_review_request(
    capsule: ConnectionEvidenceCapsule,
    *,
    request_id: str,
    requested_by: str,
    assigned_reviewer_id: str,
    assigned_reviewer_class: str = EXTERNAL_REVIEWER_CLASS,
) -> ConnectionEvidenceReviewRequest:
    if capsule.status != EVIDENCE_READY or capsule.blockers:
        raise ValueError("evidence_capsule_not_ready")
    if capsule.capsule_digest != capsule_digest(capsule):
        raise ValueError("evidence_capsule_digest_invalid")
    if not capsule.evidence_only or not capsule.candidate_only:
        raise ValueError("evidence_capsule_boundary_invalid")
    if capsule.live_effect_allowed or capsule.state_write_allowed:
        raise ValueError("evidence_capsule_live_scope_invalid")
    if capsule.authority_widening_allowed:
        raise ValueError("evidence_capsule_authority_scope_invalid")
    if not request_id or not requested_by or not assigned_reviewer_id:
        raise ValueError("evidence_review_request_identity_missing")
    if assigned_reviewer_class != EXTERNAL_REVIEWER_CLASS:
        raise ValueError("evidence_review_reviewer_class_invalid")
    value = ConnectionEvidenceReviewRequest(
        request_id,
        requested_by,
        assigned_reviewer_id,
        assigned_reviewer_class,
        capsule.capsule_digest,
        capsule.source_bundle_digest,
        capsule.rollback_bundle_digest,
        capsule.candidate_connection_digest,
        REVIEW_SCOPE,
        True,
        False,
        False,
        False,
        False,
        "",
    )
    return replace(value, request_digest=request_digest(value))
