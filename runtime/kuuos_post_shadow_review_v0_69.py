#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    ALLOWED_DECISIONS,
    APPROVE_EVIDENCE,
    ATTESTATION_VERSION,
    BLOCKED,
    EXTERNAL_REVIEWER_CLASS,
    MORE_EVIDENCE_REQUIRED,
    READY,
    REJECT_EVIDENCE,
    REJECTED,
    REQUEST_MORE_EVIDENCE,
    REQUEST_VERSION,
    REVIEW_SCOPE,
    ConnectionEvidenceReviewRequest,
    ExternalEvidenceReviewAttestation,
    ExternalEvidenceReviewRecord,
    attestation_digest,
    evidence_review_record_digest,
    request_digest,
)
from runtime.kuuos_connection_evidence_v0_68 import validate_connection_evidence_capsule
from runtime.kuuos_connection_evidence_types_v0_68 import (
    READY as EVIDENCE_READY,
    ConnectionEvidenceCapsule,
    capsule_digest,
)
from runtime.kuuos_connection_orbit_types_v0_67 import ConnectionOrbitValidationReceipt
from runtime.kuuos_connection_shadow_types_v0_66 import ConnectionShadowReceipt
from runtime.kuuos_os_curvature_holonomy_v0_61 import OSGaugeBundle


def _valid_epoch(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


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
        allowed_scopes=(REVIEW_SCOPE,),
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


def _request_issues(
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
    boundaries = (
        request.evidence_only,
        not request.live_effect_requested,
        not request.state_write_requested,
        not request.authority_widening_requested,
        not request.rollback_replacement_requested,
    )
    if not all(boundaries):
        issues.append("evidence_review_request_boundary_invalid")
    return tuple(issues)


def _attestation_issues(
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
    if attestation.allowed_scopes != (REVIEW_SCOPE,):
        issues.append("evidence_review_attestation_scope_invalid")
    if attestation.production_apply_allowed:
        issues.append("evidence_review_production_apply_forbidden")
    if attestation.live_effect_allowed:
        issues.append("evidence_review_live_effect_forbidden")
    boundaries = (
        not attestation.state_write_allowed,
        not attestation.authority_widening_allowed,
        not attestation.rollback_replacement_allowed,
    )
    if not all(boundaries):
        issues.append("evidence_review_attestation_boundary_invalid")
    start = attestation.valid_from_epoch
    end = attestation.valid_through_epoch
    if not _valid_epoch(current_epoch) or not _valid_epoch(start) or not _valid_epoch(end):
        issues.append("evidence_review_epoch_invalid")
    elif start > end:
        issues.append("evidence_review_validity_window_invalid")
    else:
        if not start <= current_epoch <= end:
            issues.append("evidence_review_outside_validity_window")
        if start < capsule.valid_from_epoch or end > capsule.valid_through_epoch:
            issues.append("evidence_review_window_exceeds_capsule")
    return tuple(issues)


def evaluate_external_evidence_review(
    capsule: ConnectionEvidenceCapsule,
    source_bundle: OSGaugeBundle,
    shadow_bundle: OSGaugeBundle,
    shadow_receipt: ConnectionShadowReceipt,
    gauge_validation: ConnectionOrbitValidationReceipt,
    request: ConnectionEvidenceReviewRequest,
    attestation: ExternalEvidenceReviewAttestation,
    *,
    current_epoch: int,
) -> ExternalEvidenceReviewRecord:
    issues = list(validate_connection_evidence_capsule(
        capsule,
        source_bundle,
        shadow_bundle,
        shadow_receipt,
        gauge_validation,
        current_epoch=current_epoch,
    ))
    issues.extend(_request_issues(capsule, request))
    issues.extend(_attestation_issues(
        capsule,
        request,
        attestation,
        current_epoch=current_epoch,
    ))
    issues = list(dict.fromkeys(issues))
    warnings: list[str] = []
    if issues:
        status = BLOCKED
        admission_candidate = False
    elif attestation.decision == APPROVE_EVIDENCE:
        status = READY
        admission_candidate = True
    elif attestation.decision == REJECT_EVIDENCE:
        status = REJECTED
        admission_candidate = False
        warnings.append("external_reviewer_rejected_evidence")
    elif attestation.decision == REQUEST_MORE_EVIDENCE:
        status = MORE_EVIDENCE_REQUIRED
        admission_candidate = False
        warnings.append("external_reviewer_requested_more_evidence")
    else:
        status = BLOCKED
        admission_candidate = False
    record = ExternalEvidenceReviewRecord(
        status=status,
        request_digest=request.request_digest,
        attestation_digest=attestation.attestation_digest,
        evidence_capsule_digest=capsule.capsule_digest,
        source_bundle_digest=capsule.source_bundle_digest,
        rollback_bundle_digest=capsule.rollback_bundle_digest,
        candidate_connection_digest=capsule.candidate_connection_digest,
        reviewer_id=attestation.reviewer_id,
        reviewer_class=attestation.reviewer_class,
        decision=attestation.decision,
        review_scope=REVIEW_SCOPE,
        governed_admission_candidate=admission_candidate,
        review_only=True,
        live_effect_allowed=False,
        state_write_performed=False,
        authority_widened=False,
        rollback_target_replaced=False,
        blockers=tuple(issues),
        warnings=tuple(warnings),
        record_digest="",
    )
    return replace(record, record_digest=evidence_review_record_digest(record))
