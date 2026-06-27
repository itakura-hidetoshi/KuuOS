#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_connection_evidence_review_attestation_v0_69 import ExternalEvidenceReviewAttestation
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
    ConnectionEvidenceReviewRequest,
)
from runtime.kuuos_connection_evidence_v0_68 import validate_connection_evidence_capsule
from runtime.kuuos_connection_evidence_types_v0_68 import ConnectionEvidenceCapsule
from runtime.kuuos_connection_external_review_core_a_v0_69 import review_request_issues
from runtime.kuuos_connection_external_review_permission_v0_69 import review_attestation_issues
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
    issues.extend(review_request_issues(capsule, request))
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
