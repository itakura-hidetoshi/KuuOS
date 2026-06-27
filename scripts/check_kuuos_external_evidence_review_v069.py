#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_connection_evidence_v0_68 import build_connection_evidence_capsule
from runtime.kuuos_external_evidence_review_request_v0_69 import (
    build_external_evidence_review_request,
    external_review_request_blockers,
)
from runtime.kuuos_external_evidence_review_types_v0_69 import (
    APPROVE_EVIDENCE,
    HUMAN_REVIEWER,
)
from runtime.kuuos_external_evidence_review_v0_69 import (
    review_external_evidence,
    validate_external_evidence_review,
)
from scripts.check_kuuos_evidence_v068 import evidence_chain


def main() -> int:
    source, shadow, shadow_receipt, gauge_validation = evidence_chain()
    capsule = build_connection_evidence_capsule(
        source,
        shadow,
        shadow_receipt,
        gauge_validation,
        capsule_id="connection-evidence-v069",
        valid_from_epoch=10,
        valid_through_epoch=20,
    )
    request = build_external_evidence_review_request(
        capsule,
        request_id="external-review-request-v069",
        valid_from_epoch=10,
        valid_through_epoch=20,
    )
    assert external_review_request_blockers(request, capsule, current_epoch=15) == ()

    rationale = "Evidence chain and rollback binding verified."
    receipt = review_external_evidence(
        capsule,
        request,
        review_id="external-review-v069",
        reviewer_id="reviewer-001",
        reviewer_class=HUMAN_REVIEWER,
        decision=APPROVE_EVIDENCE,
        rationale=rationale,
        current_epoch=15,
    )
    assert receipt.next_stage_candidate
    assert validate_external_evidence_review(
        receipt,
        request,
        capsule,
        rationale=rationale,
        current_epoch=15,
    ) == ()

    expired = external_review_request_blockers(request, capsule, current_epoch=21)
    assert "external_review_capsule_expired" in expired
    tampered = replace(capsule, sample_count=capsule.sample_count + 1)
    changed = external_review_request_blockers(request, tampered, current_epoch=15)
    assert "external_review_capsule_digest_invalid" in changed

    print(json.dumps({
        "status": "KUUOS_V0_69_VALIDATED",
        "checks": ["approve", "expiry", "tamper"],
        "check_count": 3,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
