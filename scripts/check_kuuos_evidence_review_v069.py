#!/usr/bin/env python3
from __future__ import annotations

import json

from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    APPROVE_EVIDENCE,
    BLOCKED,
    MORE_EVIDENCE_REQUIRED,
    READY,
    REJECT_EVIDENCE,
    REJECTED,
    REQUEST_MORE_EVIDENCE,
)
from runtime.kuuos_connection_evidence_review_v0_69 import (
    evaluate_external_evidence_review,
)
from runtime.kuuos_connection_evidence_review_validation_v0_69 import (
    validate_external_evidence_review_record,
)
from runtime.kuuos_connection_evidence_v0_68 import build_connection_evidence_capsule
from runtime.kuuos_connection_external_review_v0_69 import (
    build_external_review_request,
    seal_external_review_attestation,
)
from scripts.check_kuuos_evidence_v068 import evidence_chain


def review_inputs():
    source, shadow, shadow_record, gauge_validation = evidence_chain()
    capsule = build_connection_evidence_capsule(
        source,
        shadow,
        shadow_record,
        gauge_validation,
        capsule_id="external-review-evidence-v069",
        valid_from_epoch=10,
        valid_through_epoch=20,
    )
    request = build_external_review_request(
        capsule,
        request_id="external-review-request-v069",
        requested_by="kuuos-governance",
        assigned_reviewer_id="reviewer-v069",
    )
    return source, shadow, shadow_record, gauge_validation, capsule, request


def decide(request, decision):
    return seal_external_review_attestation(
        request,
        attestation_id=f"attestation-{decision.lower()}-v069",
        reviewer_id="reviewer-v069",
        decision=decision,
        valid_from_epoch=12,
        valid_through_epoch=18,
    )


def run_review(inputs, attestation, current_epoch=15):
    source, shadow, shadow_record, gauge_validation, capsule, request = inputs
    return evaluate_external_evidence_review(
        capsule,
        source,
        shadow,
        shadow_record,
        gauge_validation,
        request,
        attestation,
        current_epoch=current_epoch,
    )


def main() -> int:
    inputs = review_inputs()
    capsule, request = inputs[4], inputs[5]
    checks: list[str] = []

    approval = decide(request, APPROVE_EVIDENCE)
    assert approval.production_apply_allowed is True
    approved = run_review(inputs, approval)
    assert approved.status == READY
    assert approved.governed_admission_candidate
    assert approved.review_only
    assert approved.live_effect_allowed is False
    assert approved.state_write_performed is False
    assert approved.authority_widened is False
    assert approved.rollback_target_replaced is False
    assert validate_external_evidence_review_record(
        approved,
        capsule,
        request,
        approval,
        current_epoch=15,
    ) == ()
    checks.append("approve-binds-production-permission")

    rejection = decide(request, REJECT_EVIDENCE)
    assert rejection.production_apply_allowed is False
    rejected = run_review(inputs, rejection)
    assert rejected.status == REJECTED
    assert rejected.governed_admission_candidate is False

    more_attestation = decide(request, REQUEST_MORE_EVIDENCE)
    assert more_attestation.production_apply_allowed is False
    more = run_review(inputs, more_attestation)
    assert more.status == MORE_EVIDENCE_REQUIRED
    assert more.governed_admission_candidate is False
    checks.append("explicit-decisions")

    expired = run_review(inputs, approval, current_epoch=21)
    assert expired.status == BLOCKED
    assert "evidence_capsule_outside_validity_window" in expired.blockers
    checks.append("expired-evidence")

    print(json.dumps({
        "status": "KUUOS_V0_69_VALIDATED",
        "checks": checks,
        "check_count": len(checks),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
