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
    request = ConnectionEvidenceReviewRequest(
        request_id=request_id,
        requested_by=requested_by,
        assigned_reviewer_id=assigned_reviewer_id,
        assigned_reviewer_class=assigned_reviewer_class,
        evidence_capsule_digest=capsule.capsule_digest,
        source_bundle_digest=capsule.source_bundle_digest,
        rollback_bundle_digest=capsule.rollback_bundle_digest,
        candidate_connection_digest=capsule.candidate_connection_digest,
        requested_scope=REVIEW_SCOPE,
        evidence_only=True,
        live_effect_requested=False,
        state_write_requested=False,
        authority_widening_requested=False,
        rollback_replacement_requested=False,
        request_digest="",
    )
    return replace(request, request_digest=request_digest(request))


def seal_external_review_attestation(
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
    attestation = ExternalEvidenceReviewAttestation(
        attestation_id=attestation_id,
        reviewer_id=reviewer_id,
        reviewer_class=reviewer_class,
        decision=decision,
        bound_request_digest=request.request_digest,
        bound_evidence_capsule_digest=request.evidence_capsule_digest,
        bound_source_bundle_digest=request.source_bundle_digest,
        bound_rollback_bundle_digest=request.rollback_bundle_digest,
        bound_candidate_connection_digest=request.candidate_connection_digest,
        allowed_scopes=exact_review_scope(),
        valid_from_epoch=valid_from_epoch,
        valid_through_epoch=valid_through_epoch,
        production_apply_allowed=False,
        live_effect_allowed=False,
        state_write_allowed=False,
        authority_widening_allowed=False,
        rollback_replacement_allowed=False,
        attestation_digest="",
    )
    return replace(attestation, attestation_digest=attestation_digest(attestation))
