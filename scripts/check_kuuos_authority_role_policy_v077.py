#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_authority_role_policy_v0_77 import (
    AUTHORITY_BLOCKED,
    AUTHORITY_GRANTED,
    PRODUCTION_CONTEXT,
    RESEARCH_CONTEXT,
    ROLE_AGGREGATED,
    ROLE_SEPARATED,
    build_authority_role_policy,
    evaluate_application_authority,
)
from runtime.kuuos_memory_review_identity_v0_74 import EXTERNAL_REVIEWER
from runtime.kuuos_memory_review_receipt_v0_74 import (
    APPROVE_MEMORY_SELECTION,
    MemoryReviewReceipt,
    memory_review_receipt_digest,
)
from runtime.kuuos_memory_selection_review_v0_74 import REVIEW_APPROVED


def approved_review() -> MemoryReviewReceipt:
    unsigned = MemoryReviewReceipt(
        REVIEW_APPROVED,
        APPROVE_MEMORY_SELECTION,
        "request-v077",
        "selection-v077",
        "solo-developer",
        EXTERNAL_REVIEWER,
        "history-v077",
        "source-kernel-v077",
        "family-v077",
        "member-v077",
        "deformation-v077",
        "selected-kernel-v077",
        "selected-connection-v077",
        "source-kernel-v077",
        100,
        200,
        150,
        True,
        False,
        False,
        False,
        False,
        (),
        "",
    )
    return replace(
        unsigned,
        receipt_digest=memory_review_receipt_digest(unsigned),
    )


def main() -> int:
    review = approved_review()
    solo_research = build_authority_role_policy(
        "solo-research-v077", ROLE_AGGREGATED, RESEARCH_CONTEXT
    )
    solo_production = build_authority_role_policy(
        "solo-production-v077", ROLE_AGGREGATED, PRODUCTION_CONTEXT
    )

    research = evaluate_application_authority(review, solo_research)
    production = evaluate_application_authority(review, solo_production)

    assert research.status == AUTHORITY_GRANTED
    assert production.status == AUTHORITY_GRANTED
    assert research.independent_approval_required is False
    assert production.independent_approval_required is False

    separated = build_authority_role_policy(
        "separated-production-v077", ROLE_SEPARATED, PRODUCTION_CONTEXT
    )
    missing = evaluate_application_authority(review, separated)
    assert missing.status == AUTHORITY_BLOCKED
    assert "independent_authority_approval_required" in missing.issues

    granted = evaluate_application_authority(
        review,
        separated,
        independent_approval_valid=True,
        independent_actor_id="authority-owner-beta",
    )
    assert granted.status == AUTHORITY_GRANTED

    same_actor = evaluate_application_authority(
        review,
        separated,
        independent_approval_valid=True,
        independent_actor_id=review.reviewer_id,
    )
    assert same_actor.status == AUTHORITY_BLOCKED
    assert "independent_authority_actor_not_independent" in same_actor.issues

    print(json.dumps({
        "status": "KUUOS_AUTHORITY_ROLE_TOPOLOGY_V0_77_VALIDATED",
        "checks": [
            "solo-research-needs-no-independent-approval",
            "solo-production-needs-no-independent-approval",
            "operating-context-does-not-force-role-separation",
            "separated-topology-requires-independent-approval",
            "separated-topology-requires-distinct-actor",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
