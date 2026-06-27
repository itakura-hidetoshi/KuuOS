#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_connection_evidence_review_attestation_v0_69 import (
    ExternalEvidenceReviewAttestation,
)
from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    APPROVE_EVIDENCE,
    ConnectionEvidenceReviewRequest,
)
from runtime.kuuos_connection_evidence_types_v0_68 import ConnectionEvidenceCapsule
from runtime.kuuos_connection_external_review_core_b_v0_69 import (
    review_attestation_issues as legacy_review_attestation_issues,
    valid_epoch,
)


def review_attestation_issues(
    capsule: ConnectionEvidenceCapsule,
    request: ConnectionEvidenceReviewRequest,
    attestation: ExternalEvidenceReviewAttestation,
    *,
    current_epoch: int,
) -> tuple[str, ...]:
    issues = list(legacy_review_attestation_issues(
        capsule,
        request,
        attestation,
        current_epoch=current_epoch,
    ))
    expected = attestation.decision == APPROVE_EVIDENCE
    if expected and attestation.production_apply_allowed:
        issues = [
            issue for issue in issues
            if issue != "evidence_review_production_apply_forbidden"
        ]
    if attestation.production_apply_allowed != expected:
        issues.append("evidence_review_decision_flag_mismatch")
    return tuple(dict.fromkeys(issues))
