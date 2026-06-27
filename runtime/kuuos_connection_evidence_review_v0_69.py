#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_connection_evidence_review_binding_v0_69 import (
    review_attestation_issues,
    review_request_issues,
    valid_epoch,
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
    ExternalEvidenceReviewAttestation,
    ExternalEvidenceReviewRecord,
    record_digest,
)
from runtime.kuuos_connection_evidence_v0_68 import validate_connection_evidence_capsule
from runtime.kuuos_connection_evidence_types_v0_68 import ConnectionEvidenceCapsule
from runtime.kuuos_connection_orbit_types_v0_67 import ConnectionOrbitValidationReceipt
from runtime.kuuos_connection_shadow_types_v0_66 import ConnectionShadowReceipt
from runtime.kuuos_os_curvature_holonomy_v0_61 import OSGaugeBundle


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
    issues.extend(review_request_issues(
        capsule,
        request,
        current_epoch=current_epoch,
    ))
    issues.extend(review_attestation_issues(
        capsule,
        request,
        attestation,
        current_epoch=current_epoch,
    ))
    issues = list(dict.fromkeys(issues))
    warnings: list[str] = []

    if issues:
        status = BLOCKED
    elif attestation.decision == APPROVE_EVIDENCE:
        status = READY
    elif attestation.decision == REJECT_EVIDENCE:
        status = REJECTED
        warnings.append("external_reviewer_rejected_evidence")
    elif attestation.decision == REQUEST_MORE_EVIDENCE:
        status = MORE_EVIDENCE_REQUIRED
        warnings.append("external_reviewer_requested_more_evidence")
    else:
        status = BLOCKED

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
        production_apply_allowed=(
            not issues and attestation.production_apply_allowed
        ),
        live_effect_performed=False,
        state_write_performed=False,
        authority_widened=False,
        rollback_target_replaced=False,
        blockers=tuple(issues),
        warnings=tuple(warnings),
        record_digest="",
    )
    return replace(record, record_digest=record_digest(record))


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
    if record.record_digest != record_digest(record):
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

    if record.blockers:
        expected_status = BLOCKED
        expected_permission = False
    elif record.decision == APPROVE_EVIDENCE:
        expected_status = READY
        expected_permission = True
    elif record.decision == REJECT_EVIDENCE:
        expected_status = REJECTED
        expected_permission = False
    elif record.decision == REQUEST_MORE_EVIDENCE:
        expected_status = MORE_EVIDENCE_REQUIRED
        expected_permission = False
    else:
        expected_status = BLOCKED
        expected_permission = False

    if record.status != expected_status:
        issues.append("evidence_review_record_status_invalid")
    if record.production_apply_allowed != expected_permission:
        issues.append("evidence_review_record_permission_invalid")
    if record.production_apply_allowed != attestation.production_apply_allowed and not record.blockers:
        issues.append("evidence_review_record_attestation_permission_mismatch")
    if record.live_effect_performed:
        issues.append("evidence_review_record_live_effect_detected")
    if record.state_write_performed:
        issues.append("evidence_review_record_state_write_detected")
    if record.authority_widened:
        issues.append("evidence_review_record_authority_widened")
    if record.rollback_target_replaced:
        issues.append("evidence_review_record_rollback_replaced")
    if not valid_epoch(current_epoch):
        issues.append("evidence_review_record_epoch_invalid")
    elif not (
        request.valid_from_epoch <= current_epoch <= request.valid_through_epoch
        and attestation.valid_from_epoch <= current_epoch <= attestation.valid_through_epoch
    ):
        issues.append("evidence_review_record_outside_validity_window")
    return tuple(dict.fromkeys(issues))
