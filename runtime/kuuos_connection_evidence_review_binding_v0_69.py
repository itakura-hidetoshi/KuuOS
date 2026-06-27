#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    ALLOWED_DECISIONS,
    APPROVE_EVIDENCE,
    ATTESTATION_VERSION,
    REQUEST_VERSION,
    REVIEWER_CLASS,
    REVIEW_SCOPE,
    ConnectionEvidenceReviewRequest,
    ExternalEvidenceReviewAttestation,
    attestation_digest,
    request_digest,
)
from runtime.kuuos_connection_evidence_types_v0_68 import (
    READY as EVIDENCE_READY,
    ConnectionEvidenceCapsule,
    capsule_digest,
)


def valid_epoch(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def build_external_review_request(
    capsule: ConnectionEvidenceCapsule,
    *,
    request_id: str,
    requested_by: str,
    assigned_reviewer_id: str,
    valid_from_epoch: int,
    valid_through_epoch: int,
    assigned_reviewer_class: str = REVIEWER_CLASS,
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
    if assigned_reviewer_class != REVIEWER_CLASS:
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
        valid_from_epoch=valid_from_epoch,
        valid_through_epoch=valid_through_epoch,
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
    reviewer_class: str = REVIEWER_CLASS,
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
        allowed_scopes=(REVIEW_SCOPE,),
        valid_from_epoch=valid_from_epoch,
        valid_through_epoch=valid_through_epoch,
        production_apply_allowed=decision == APPROVE_EVIDENCE,
        live_effect_allowed=False,
        state_write_allowed=False,
        authority_widening_allowed=False,
        rollback_replacement_allowed=False,
        attestation_digest="",
    )
    return replace(attestation, attestation_digest=attestation_digest(attestation))


def review_request_issues(
    capsule: ConnectionEvidenceCapsule,
    request: ConnectionEvidenceReviewRequest,
    *,
    current_epoch: int,
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
    if request.assigned_reviewer_class != REVIEWER_CLASS:
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
    if request.rollback_bundle_digest != request.source_bundle_digest:
        issues.append("evidence_review_request_rollback_binding_invalid")
    if not all(valid_epoch(value) for value in (
        current_epoch,
        request.valid_from_epoch,
        request.valid_through_epoch,
    )):
        issues.append("evidence_review_request_epoch_invalid")
    elif request.valid_from_epoch > request.valid_through_epoch:
        issues.append("evidence_review_request_window_invalid")
    else:
        if not request.valid_from_epoch <= current_epoch <= request.valid_through_epoch:
            issues.append("evidence_review_request_outside_validity_window")
        if (
            request.valid_from_epoch < capsule.valid_from_epoch
            or request.valid_through_epoch > capsule.valid_through_epoch
        ):
            issues.append("evidence_review_request_window_exceeds_capsule")
    return tuple(dict.fromkeys(issues))


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
    if attestation.reviewer_class != REVIEWER_CLASS:
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
    if attestation.allowed_scopes != (REVIEW_SCOPE,):
        issues.append("evidence_review_attestation_scope_invalid")
    expected_permission = attestation.decision == APPROVE_EVIDENCE
    if attestation.production_apply_allowed != expected_permission:
        issues.append("evidence_review_decision_permission_mismatch")
    if attestation.live_effect_allowed:
        issues.append("evidence_review_unrecorded_live_effect")
    if attestation.state_write_allowed:
        issues.append("evidence_review_unrecorded_state_write")
    if attestation.authority_widening_allowed:
        issues.append("evidence_review_authority_widening")
    if attestation.rollback_replacement_allowed:
        issues.append("evidence_review_rollback_replacement")

    if not all(valid_epoch(value) for value in (
        current_epoch,
        attestation.valid_from_epoch,
        attestation.valid_through_epoch,
    )):
        issues.append("evidence_review_attestation_epoch_invalid")
    elif attestation.valid_from_epoch > attestation.valid_through_epoch:
        issues.append("evidence_review_validity_window_invalid")
    else:
        if not attestation.valid_from_epoch <= current_epoch <= attestation.valid_through_epoch:
            issues.append("evidence_review_outside_validity_window")
        if (
            attestation.valid_from_epoch < request.valid_from_epoch
            or attestation.valid_through_epoch > request.valid_through_epoch
        ):
            issues.append("evidence_review_window_exceeds_request")
    return tuple(dict.fromkeys(issues))
