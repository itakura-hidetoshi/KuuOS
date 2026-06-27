#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_connection_evidence_types_v0_68 import (
    READY as EVIDENCE_READY,
    REVIEW_SCOPE as EVIDENCE_SCOPE,
    ConnectionEvidenceCapsule,
    capsule_digest,
)
from runtime.kuuos_external_evidence_review_types_v0_69 import (
    REVIEW_SCOPE,
    ExternalEvidenceReviewRequest,
    request_digest,
)


def _valid_epoch(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def build_external_evidence_review_request(
    capsule: ConnectionEvidenceCapsule,
    *,
    request_id: str,
    valid_from_epoch: int,
    valid_through_epoch: int,
) -> ExternalEvidenceReviewRequest:
    request = ExternalEvidenceReviewRequest(
        request_id=request_id,
        evidence_capsule_digest=capsule.capsule_digest,
        source_bundle_digest=capsule.source_bundle_digest,
        rollback_bundle_digest=capsule.rollback_bundle_digest,
        candidate_connection_digest=capsule.candidate_connection_digest,
        valid_from_epoch=valid_from_epoch,
        valid_through_epoch=valid_through_epoch,
        review_scope=REVIEW_SCOPE,
        request_digest="",
    )
    return replace(request, request_digest=request_digest(request))


def external_review_request_blockers(
    request: ExternalEvidenceReviewRequest,
    capsule: ConnectionEvidenceCapsule,
    *,
    current_epoch: int,
) -> tuple[str, ...]:
    blockers: list[str] = []
    if request.request_digest != request_digest(request):
        blockers.append("external_review_request_digest_invalid")
    if not request.request_id:
        blockers.append("external_review_request_id_missing")
    if capsule.capsule_digest != capsule_digest(capsule):
        blockers.append("external_review_capsule_digest_invalid")
    if capsule.status != EVIDENCE_READY or capsule.blockers:
        blockers.append("external_review_capsule_not_ready")
    if capsule.review_scope != EVIDENCE_SCOPE:
        blockers.append("external_review_capsule_scope_invalid")
    if request.review_scope != REVIEW_SCOPE:
        blockers.append("external_review_scope_widened")
    bindings = (
        (request.evidence_capsule_digest, capsule.capsule_digest, "capsule"),
        (request.source_bundle_digest, capsule.source_bundle_digest, "source"),
        (request.rollback_bundle_digest, capsule.rollback_bundle_digest, "rollback"),
        (request.candidate_connection_digest, capsule.candidate_connection_digest, "candidate"),
    )
    for actual, expected, name in bindings:
        if actual != expected:
            blockers.append(f"external_review_{name}_binding_mismatch")
    if request.rollback_bundle_digest != request.source_bundle_digest:
        blockers.append("external_review_rollback_source_binding_mismatch")
    for value, name in (
        (request.valid_from_epoch, "valid_from"),
        (request.valid_through_epoch, "valid_through"),
        (current_epoch, "current"),
    ):
        if not _valid_epoch(value):
            blockers.append(f"external_review_{name}_epoch_invalid")
    if _valid_epoch(request.valid_from_epoch) and _valid_epoch(request.valid_through_epoch):
        if request.valid_from_epoch > request.valid_through_epoch:
            blockers.append("external_review_validity_window_invalid")
        if request.valid_from_epoch < capsule.valid_from_epoch:
            blockers.append("external_review_validity_starts_before_capsule")
        if request.valid_through_epoch > capsule.valid_through_epoch:
            blockers.append("external_review_validity_exceeds_capsule")
    if _valid_epoch(current_epoch):
        if not capsule.valid_from_epoch <= current_epoch <= capsule.valid_through_epoch:
            blockers.append("external_review_capsule_expired")
        if not request.valid_from_epoch <= current_epoch <= request.valid_through_epoch:
            blockers.append("external_review_request_expired")
    return tuple(dict.fromkeys(blockers))
