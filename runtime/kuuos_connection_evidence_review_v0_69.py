#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    ALLOWED_DECISIONS,
    ALLOWED_REVIEWER_CLASSES,
    APPROVE_EVIDENCE,
    ATTESTATION_VERSION,
    BLOCKED,
    MORE_EVIDENCE_REQUIRED,
    NEXT_STAGE_SCOPE,
    READY,
    REJECT_EVIDENCE,
    REJECTED,
    REQUEST_MORE_EVIDENCE,
    REQUEST_VERSION,
    REVIEW_SCOPE,
    VERSION,
    ConnectionEvidenceReviewAttestation,
    ConnectionEvidenceReviewReceipt,
    ConnectionEvidenceReviewRequest,
    attestation_digest,
    receipt_digest,
    request_digest,
)
from runtime.kuuos_connection_evidence_types_v0_68 import (
    READY as EVIDENCE_READY,
    REVIEW_SCOPE as EVIDENCE_REVIEW_SCOPE,
    ConnectionEvidenceCapsule,
    capsule_digest,
)
from runtime.kuuos_connection_evidence_v0_68 import (
    validate_connection_evidence_capsule,
)
from runtime.kuuos_connection_orbit_types_v0_67 import (
    ConnectionOrbitValidationReceipt,
)
from runtime.kuuos_connection_shadow_types_v0_66 import ConnectionShadowReceipt
from runtime.kuuos_os_curvature_holonomy_v0_61 import OSGaugeBundle


def _valid_epoch(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def build_connection_evidence_review_request(
    capsule: ConnectionEvidenceCapsule,
    *,
    request_id: str,
    requested_by: str,
    assigned_reviewer_id: str,
    assigned_reviewer_class: str,
) -> ConnectionEvidenceReviewRequest:
    if capsule.capsule_digest != capsule_digest(capsule):
        raise ValueError("evidence_capsule_digest_invalid")
    if capsule.status != EVIDENCE_READY or capsule.blockers:
        raise ValueError("evidence_capsule_not_ready")
    if capsule.review_scope != EVIDENCE_REVIEW_SCOPE:
        raise ValueError("evidence_capsule_scope_invalid")
    if not capsule.evidence_only or not capsule.candidate_only:
        raise ValueError("evidence_capsule_boundary_invalid")
    if capsule.live_effect_allowed or capsule.state_write_allowed:
        raise ValueError("evidence_capsule_live_scope_invalid")
    if capsule.authority_widening_allowed:
        raise ValueError("evidence_capsule_authority_scope_invalid")
    if capsule.rollback_bundle_digest != capsule.source_bundle_digest:
        raise ValueError("evidence_capsule_rollback_binding_invalid")
    if not request_id or not requested_by or not assigned_reviewer_id:
        raise ValueError("evidence_review_request_identity_missing")
    if assigned_reviewer_class not in ALLOWED_REVIEWER_CLASSES:
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
        review_only=True,
        live_effect_requested=False,
        state_write_requested=False,
        authority_widening_requested=False,
        rollback_replacement_requested=False,
        request_digest="",
    )
    return replace(request, request_digest=request_digest(request))


def seal_connection_evidence_review_attestation(
    request: ConnectionEvidenceReviewRequest,
    *,
    attestation_id: str,
    reviewer_id: str,
    reviewer_class: str,
    decision: str,
    valid_from_epoch: int,
    valid_through_epoch: int,
) -> ConnectionEvidenceReviewAttestation:
    if not attestation_id or not reviewer_id:
        raise ValueError("evidence_review_attestation_identity_missing")
    if reviewer_id != request.assigned_reviewer_id:
        raise ValueError("evidence_review_reviewer_identity_mismatch")
    if reviewer_class != request.assigned_reviewer_class:
        raise ValueError("evidence_review_reviewer_class_mismatch")
    if reviewer_class not in ALLOWED_REVIEWER_CLASSES:
        raise ValueError("evidence_review_reviewer_class_invalid")
    if decision not in ALLOWED_DECISIONS:
        raise ValueError("evidence_review_decision_invalid")

    attestation = ConnectionEvidenceReviewAttestation(
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
    return replace(
        attestation,
        attestation_digest=attestation_digest(attestation),
    )


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
    if request.assigned_reviewer_class not in ALLOWED_REVIEWER_CLASSES:
        issues.append("evidence_review_assigned_reviewer_class_invalid")
    bindings = (
        (request.evidence_capsule_digest, capsule.capsule_digest, "capsule"),
        (request.source_bundle_digest, capsule.source_bundle_digest, "source"),
        (request.rollback_bundle_digest, capsule.rollback_bundle_digest, "rollback"),
        (
            request.candidate_connection_digest,
            capsule.candidate_connection_digest,
            "candidate",
        ),
    )
    for actual, expected, name in bindings:
        if actual != expected:
            issues.append(f"evidence_review_request_{name}_binding_mismatch")
    if request.rollback_bundle_digest != request.source_bundle_digest:
        issues.append("evidence_review_request_rollback_source_mismatch")
    if request.requested_scope != REVIEW_SCOPE:
        issues.append("evidence_review_request_scope_invalid")
    boundaries = (
        request.review_only,
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
    attestation: ConnectionEvidenceReviewAttestation,
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
    if attestation.reviewer_class not in ALLOWED_REVIEWER_CLASSES:
        issues.append("evidence_review_reviewer_class_invalid")
    if attestation.decision not in ALLOWED_DECISIONS:
        issues.append("evidence_review_decision_invalid")

    bindings = (
        (attestation.bound_request_digest, request.request_digest, "request"),
        (
            attestation.bound_evidence_capsule_digest,
            capsule.capsule_digest,
            "capsule",
        ),
        (
            attestation.bound_source_bundle_digest,
            capsule.source_bundle_digest,
            "source",
        ),
        (
            attestation.bound_rollback_bundle_digest,
            capsule.rollback_bundle_digest,
            "rollback",
        ),
        (
            attestation.bound_candidate_connection_digest,
            capsule.candidate_connection_digest,
            "candidate",
        ),
    )
    for actual, expected, name in bindings:
        if actual != expected:
            issues.append(f"evidence_review_attestation_{name}_binding_mismatch")
    if attestation.bound_rollback_bundle_digest != attestation.bound_source_bundle_digest:
        issues.append("evidence_review_attestation_rollback_source_mismatch")
    if attestation.allowed_scopes != (REVIEW_SCOPE,):
        issues.append("evidence_review_attestation_scope_invalid")
    if attestation.production_apply_allowed:
        issues.append("evidence_review_production_apply_forbidden")
    if attestation.live_effect_allowed:
        issues.append("evidence_review_live_effect_forbidden")
    if attestation.state_write_allowed:
        issues.append("evidence_review_state_write_forbidden")
    if attestation.authority_widening_allowed:
        issues.append("evidence_review_authority_widening_forbidden")
    if attestation.rollback_replacement_allowed:
        issues.append("evidence_review_rollback_replacement_forbidden")

    start = attestation.valid_from_epoch
    end = attestation.valid_through_epoch
    if not _valid_epoch(current_epoch):
        issues.append("evidence_review_current_epoch_invalid")
    if not _valid_epoch(start):
        issues.append("evidence_review_valid_from_epoch_invalid")
    if not _valid_epoch(end):
        issues.append("evidence_review_valid_through_epoch_invalid")
    if _valid_epoch(start) and _valid_epoch(end):
        if start > end:
            issues.append("evidence_review_validity_window_invalid")
        else:
            if start < capsule.valid_from_epoch or end > capsule.valid_through_epoch:
                issues.append("evidence_review_window_exceeds_capsule")
            if _valid_epoch(current_epoch) and not start <= current_epoch <= end:
                issues.append("evidence_review_outside_validity_window")
    return tuple(issues)


def external_evidence_review_blockers(
    capsule: ConnectionEvidenceCapsule,
    source_bundle: OSGaugeBundle,
    shadow_bundle: OSGaugeBundle,
    shadow_receipt: ConnectionShadowReceipt,
    gauge_validation: ConnectionOrbitValidationReceipt,
    request: ConnectionEvidenceReviewRequest,
    attestation: ConnectionEvidenceReviewAttestation,
    *,
    current_epoch: int,
) -> tuple[str, ...]:
    issues = list(
        validate_connection_evidence_capsule(
            capsule,
            source_bundle,
            shadow_bundle,
            shadow_receipt,
            gauge_validation,
            current_epoch=current_epoch,
        )
    )
    issues.extend(_request_issues(capsule, request))
    issues.extend(
        _attestation_issues(
            capsule,
            request,
            attestation,
            current_epoch=current_epoch,
        )
    )
    return tuple(dict.fromkeys(issues))


def _decision_result(
    decision: str,
    blocked: bool,
) -> tuple[str, bool, tuple[str, ...]]:
    if blocked:
        return BLOCKED, False, ()
    if decision == APPROVE_EVIDENCE:
        return READY, True, ()
    if decision == REJECT_EVIDENCE:
        return REJECTED, False, ("external_reviewer_rejected_evidence",)
    if decision == REQUEST_MORE_EVIDENCE:
        return (
            MORE_EVIDENCE_REQUIRED,
            False,
            ("external_reviewer_requested_more_evidence",),
        )
    return BLOCKED, False, ()


def evaluate_external_evidence_review(
    capsule: ConnectionEvidenceCapsule,
    source_bundle: OSGaugeBundle,
    shadow_bundle: OSGaugeBundle,
    shadow_receipt: ConnectionShadowReceipt,
    gauge_validation: ConnectionOrbitValidationReceipt,
    request: ConnectionEvidenceReviewRequest,
    attestation: ConnectionEvidenceReviewAttestation,
    *,
    current_epoch: int,
) -> ConnectionEvidenceReviewReceipt:
    blockers = external_evidence_review_blockers(
        capsule,
        source_bundle,
        shadow_bundle,
        shadow_receipt,
        gauge_validation,
        request,
        attestation,
        current_epoch=current_epoch,
    )
    status, admission_candidate, warnings = _decision_result(
        attestation.decision,
        bool(blockers),
    )
    receipt = ConnectionEvidenceReviewReceipt(
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
        next_stage_scope=NEXT_STAGE_SCOPE,
        governed_admission_candidate=admission_candidate,
        production_apply_ready=False,
        review_only=True,
        live_effect_performed=False,
        state_write_performed=False,
        authority_widened=False,
        rollback_target_replaced=False,
        immutable_receipt=True,
        blockers=blockers,
        warnings=warnings,
        receipt_digest="",
    )
    return replace(receipt, receipt_digest=receipt_digest(receipt))


def validate_external_evidence_review_receipt(
    receipt: ConnectionEvidenceReviewReceipt,
    capsule: ConnectionEvidenceCapsule,
    source_bundle: OSGaugeBundle,
    shadow_bundle: OSGaugeBundle,
    shadow_receipt: ConnectionShadowReceipt,
    gauge_validation: ConnectionOrbitValidationReceipt,
    request: ConnectionEvidenceReviewRequest,
    attestation: ConnectionEvidenceReviewAttestation,
    *,
    current_epoch: int,
) -> tuple[str, ...]:
    issues: list[str] = []
    expected_blockers = external_evidence_review_blockers(
        capsule,
        source_bundle,
        shadow_bundle,
        shadow_receipt,
        gauge_validation,
        request,
        attestation,
        current_epoch=current_epoch,
    )
    expected_status, expected_candidate, expected_warnings = _decision_result(
        attestation.decision,
        bool(expected_blockers),
    )

    if receipt.version != VERSION:
        issues.append("evidence_review_receipt_version_invalid")
    if receipt.receipt_digest != receipt_digest(receipt):
        issues.append("evidence_review_receipt_digest_invalid")
    bindings = (
        (receipt.request_digest, request.request_digest, "request"),
        (
            receipt.attestation_digest,
            attestation.attestation_digest,
            "attestation",
        ),
        (receipt.evidence_capsule_digest, capsule.capsule_digest, "capsule"),
        (receipt.source_bundle_digest, capsule.source_bundle_digest, "source"),
        (
            receipt.rollback_bundle_digest,
            capsule.rollback_bundle_digest,
            "rollback",
        ),
        (
            receipt.candidate_connection_digest,
            capsule.candidate_connection_digest,
            "candidate",
        ),
        (receipt.reviewer_id, attestation.reviewer_id, "reviewer_identity"),
        (receipt.reviewer_class, attestation.reviewer_class, "reviewer_class"),
        (receipt.decision, attestation.decision, "decision"),
    )
    for actual, expected, name in bindings:
        if actual != expected:
            issues.append(f"evidence_review_receipt_{name}_binding_mismatch")
    if receipt.review_scope != REVIEW_SCOPE:
        issues.append("evidence_review_receipt_scope_invalid")
    if receipt.next_stage_scope != NEXT_STAGE_SCOPE:
        issues.append("evidence_review_receipt_next_scope_invalid")
    boundaries = (
        receipt.review_only,
        not receipt.production_apply_ready,
        not receipt.live_effect_performed,
        not receipt.state_write_performed,
        not receipt.authority_widened,
        not receipt.rollback_target_replaced,
        receipt.immutable_receipt,
    )
    if not all(boundaries):
        issues.append("evidence_review_receipt_boundary_invalid")
    if receipt.rollback_bundle_digest != receipt.source_bundle_digest:
        issues.append("evidence_review_receipt_rollback_source_mismatch")
    if receipt.status != expected_status:
        issues.append("evidence_review_receipt_status_invalid")
    if receipt.governed_admission_candidate != expected_candidate:
        issues.append("evidence_review_receipt_candidate_scope_invalid")
    if receipt.blockers != expected_blockers:
        issues.append("evidence_review_receipt_blocker_binding_invalid")
    if receipt.warnings != expected_warnings:
        issues.append("evidence_review_receipt_warning_binding_invalid")
    return tuple(dict.fromkeys(issues))
