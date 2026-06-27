#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_connection_evidence_review_binding_v0_69 import (
    build_external_review_request,
    seal_external_review_attestation,
)
from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    APPROVE_EVIDENCE,
    BLOCKED,
    REJECT_EVIDENCE,
    REJECTED,
    REQUEST_MORE_EVIDENCE,
    MORE_EVIDENCE_REQUIRED,
    READY,
    attestation_digest,
)
from runtime.kuuos_connection_evidence_review_v0_69 import (
    evaluate_external_evidence_review,
    validate_external_evidence_review_record,
)
from runtime.kuuos_connection_evidence_v0_68 import build_connection_evidence_capsule
from scripts.check_kuuos_evidence_v068 import evidence_chain


def reseal(attestation, **changes):
    changed = replace(attestation, attestation_digest="", **changes)
    return replace(changed, attestation_digest=attestation_digest(changed))


def main() -> int:
    source, shadow, shadow_receipt, validation = evidence_chain()
    capsule = build_connection_evidence_capsule(
        source, shadow, shadow_receipt, validation,
        capsule_id="external-review-evidence-v069",
        valid_from_epoch=10,
        valid_through_epoch=20,
    )
    request = build_external_review_request(
        capsule,
        request_id="external-review-request-v069",
        requested_by="kuuos-governance",
        assigned_reviewer_id="reviewer-v069",
        valid_from_epoch=10,
        valid_through_epoch=20,
    )

    def decide(decision):
        return seal_external_review_attestation(
            request,
            attestation_id=f"attestation-{decision.lower()}-v069",
            reviewer_id="reviewer-v069",
            decision=decision,
            valid_from_epoch=12,
            valid_through_epoch=18,
        )

    def review(attestation, epoch=15):
        return evaluate_external_evidence_review(
            capsule, source, shadow, shadow_receipt, validation,
            request, attestation, current_epoch=epoch,
        )

    approval = decide(APPROVE_EVIDENCE)
    approved = review(approval)
    assert approval.production_apply_allowed is True
    assert approved.status == READY
    assert approved.production_apply_allowed is True
    assert approved.live_effect_performed is False
    assert validate_external_evidence_review_record(
        approved, capsule, request, approval, current_epoch=15,
    ) == ()

    rejection = decide(REJECT_EVIDENCE)
    assert rejection.production_apply_allowed is False
    assert review(rejection).status == REJECTED
    more = decide(REQUEST_MORE_EVIDENCE)
    assert more.production_apply_allowed is False
    assert review(more).status == MORE_EVIDENCE_REQUIRED

    missing = review(reseal(approval, production_apply_allowed=False))
    assert missing.status == BLOCKED
    assert "evidence_review_decision_permission_mismatch" in missing.blockers
    excess = review(reseal(rejection, production_apply_allowed=True))
    assert excess.status == BLOCKED
    assert "evidence_review_decision_permission_mismatch" in excess.blockers

    expired = review(approval, epoch=21)
    assert expired.status == BLOCKED
    tampered = replace(capsule, sample_count=capsule.sample_count + 1)
    tampered_record = evaluate_external_evidence_review(
        tampered, source, shadow, shadow_receipt, validation,
        request, approval, current_epoch=15,
    )
    assert "evidence_capsule_digest_invalid" in tampered_record.blockers

    print(json.dumps({
        "status": "KUUOS_V0_69_VALIDATED",
        "checks": [
            "approval-permission",
            "explicit-decisions",
            "permission-mismatch",
            "expiry-and-tamper",
        ],
        "check_count": 4,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
