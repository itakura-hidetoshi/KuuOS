#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_connection_evidence_types_v0_68 import ConnectionEvidenceCapsule
from runtime.kuuos_external_evidence_review_request_v0_69 import (
    external_review_request_blockers,
)
from runtime.kuuos_external_evidence_review_types_v0_69 import (
    ALLOWED_DECISIONS,
    ALLOWED_REVIEWER_CLASSES,
    APPROVE_EVIDENCE,
    BLOCKED,
    READY,
    REJECT_EVIDENCE,
    REQUEST_MORE_EVIDENCE,
    REVIEW_SCOPE,
    ExternalEvidenceReviewReceipt,
    ExternalEvidenceReviewRequest,
    receipt_digest,
)
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest


def _review_status(decision: str, blocked: bool) -> str:
    if blocked:
        return BLOCKED
    return {
        APPROVE_EVIDENCE: READY,
        REJECT_EVIDENCE: "EVIDENCE_REJECTED",
        REQUEST_MORE_EVIDENCE: "MORE_EVIDENCE_REQUIRED",
    }[decision]


def review_external_evidence(
    capsule: ConnectionEvidenceCapsule,
    request: ExternalEvidenceReviewRequest,
    *,
    review_id: str,
    reviewer_id: str,
    reviewer_class: str,
    decision: str,
    rationale: str,
    current_epoch: int,
) -> ExternalEvidenceReviewReceipt:
    blockers = list(external_review_request_blockers(request, capsule, current_epoch=current_epoch))
    if not review_id:
        blockers.append("external_review_id_missing")
    if not reviewer_id:
        blockers.append("external_reviewer_identity_missing")
    if reviewer_class not in ALLOWED_REVIEWER_CLASSES:
        blockers.append("external_reviewer_class_invalid")
    if decision not in ALLOWED_DECISIONS:
        blockers.append("external_review_decision_invalid")
    if not rationale.strip():
        blockers.append("external_review_rationale_missing")
    unique = tuple(dict.fromkeys(blockers))
    receipt = ExternalEvidenceReviewReceipt(
        status=_review_status(decision, bool(unique)) if decision in ALLOWED_DECISIONS else BLOCKED,
        review_id=review_id,
        request_digest=request.request_digest,
        evidence_capsule_digest=capsule.capsule_digest,
        source_bundle_digest=capsule.source_bundle_digest,
        rollback_bundle_digest=capsule.rollback_bundle_digest,
        candidate_connection_digest=capsule.candidate_connection_digest,
        reviewer_id=reviewer_id,
        reviewer_class=reviewer_class,
        decision=decision,
        rationale_digest=canonical_digest({"rationale": rationale}),
        valid_from_epoch=request.valid_from_epoch,
        valid_through_epoch=request.valid_through_epoch,
        review_scope=REVIEW_SCOPE,
        immutable_receipt=True,
        next_stage_candidate=not unique and decision == APPROVE_EVIDENCE,
        blockers=unique,
        receipt_digest="",
    )
    return replace(receipt, receipt_digest=receipt_digest(receipt))


def validate_external_evidence_review(
    receipt: ExternalEvidenceReviewReceipt,
    request: ExternalEvidenceReviewRequest,
    capsule: ConnectionEvidenceCapsule,
    *,
    rationale: str,
    current_epoch: int,
) -> tuple[str, ...]:
    blockers = list(external_review_request_blockers(request, capsule, current_epoch=current_epoch))
    if receipt.receipt_digest != receipt_digest(receipt):
        blockers.append("external_review_receipt_digest_invalid")
    if receipt.blockers:
        blockers.append("external_review_receipt_has_blockers")
    if not receipt.immutable_receipt:
        blockers.append("external_review_receipt_not_immutable")
    if receipt.review_scope != REVIEW_SCOPE:
        blockers.append("external_review_receipt_scope_invalid")
    if receipt.reviewer_class not in ALLOWED_REVIEWER_CLASSES or not receipt.reviewer_id:
        blockers.append("external_review_reviewer_binding_invalid")
    if receipt.decision not in ALLOWED_DECISIONS:
        blockers.append("external_review_receipt_decision_invalid")
    if receipt.rationale_digest != canonical_digest({"rationale": rationale}):
        blockers.append("external_review_rationale_binding_mismatch")
    bindings = (
        (receipt.request_digest, request.request_digest, "request"),
        (receipt.evidence_capsule_digest, capsule.capsule_digest, "capsule"),
        (receipt.source_bundle_digest, capsule.source_bundle_digest, "source"),
        (receipt.rollback_bundle_digest, capsule.rollback_bundle_digest, "rollback"),
        (receipt.candidate_connection_digest, capsule.candidate_connection_digest, "candidate"),
        (receipt.valid_from_epoch, request.valid_from_epoch, "valid_from"),
        (receipt.valid_through_epoch, request.valid_through_epoch, "valid_through"),
    )
    for actual, expected, name in bindings:
        if actual != expected:
            blockers.append(f"external_review_receipt_{name}_binding_mismatch")
    expected_candidate = receipt.decision == APPROVE_EVIDENCE
    if receipt.next_stage_candidate != expected_candidate:
        blockers.append("external_review_decision_candidate_mismatch")
    if receipt.decision in ALLOWED_DECISIONS and receipt.status != _review_status(receipt.decision, False):
        blockers.append("external_review_receipt_status_invalid")
    return tuple(dict.fromkeys(blockers))
