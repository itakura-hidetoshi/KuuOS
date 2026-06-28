#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_authority_role_policy_v0_76 import (
    AUTHORITY_BLOCKED,
    AUTHORITY_GRANTED,
    PRODUCTION_CONTEXT,
    RESEARCH_CONTEXT,
    ROLE_AGGREGATED,
    ROLE_SEPARATED,
    authority_role_policy_digest,
    build_authority_role_policy,
    build_independent_authority_approval,
    evaluate_application_authority,
)
from runtime.kuuos_memory_review_identity_v0_74 import EXTERNAL_REVIEWER
from runtime.kuuos_memory_review_receipt_v0_74 import (
    APPROVE_MEMORY_SELECTION,
    REJECT_MEMORY_SELECTION,
    MemoryReviewReceipt,
    memory_review_receipt_digest,
)
from runtime.kuuos_memory_selection_review_v0_74 import REVIEW_APPROVED, REVIEW_REJECTED


def signed_review(
    *,
    status: str = REVIEW_APPROVED,
    decision: str = APPROVE_MEMORY_SELECTION,
    application_authority: bool = True,
    reviewer_id: str = "solo-developer",
) -> MemoryReviewReceipt:
    unsigned = MemoryReviewReceipt(
        status,
        decision,
        "review-request-digest-v076",
        "selection-record-digest-v076",
        reviewer_id,
        EXTERNAL_REVIEWER,
        "history-digest-v076",
        "source-kernel-digest-v076",
        "family-digest-v076",
        "member-digest-v076",
        "deformation-digest-v076",
        "selected-kernel-digest-v076",
        "selected-connection-digest-v076",
        "source-kernel-digest-v076",
        100,
        200,
        150,
        application_authority,
        False,
        False,
        False,
        False,
        (),
        "",
    )
    return replace(unsigned, receipt_digest=memory_review_receipt_digest(unsigned))


def main() -> int:
    approved = signed_review()
    solo_research = build_authority_role_policy(
        "solo-research-v076", ROLE_AGGREGATED, RESEARCH_CONTEXT
    )
    solo_production = build_authority_role_policy(
        "solo-production-v076", ROLE_AGGREGATED, PRODUCTION_CONTEXT
    )

    research_decision = evaluate_application_authority(approved, solo_research, 160)
    production_decision = evaluate_application_authority(approved, solo_production, 160)

    assert research_decision.status == AUTHORITY_GRANTED
    assert production_decision.status == AUTHORITY_GRANTED
    assert research_decision.application_authority
    assert production_decision.application_authority
    assert research_decision.independent_approval_required is False
    assert production_decision.independent_approval_required is False
    assert research_decision.independent_approval_digest == ""
    assert production_decision.independent_approval_digest == ""

    separated = build_authority_role_policy(
        "separated-production-v076", ROLE_SEPARATED, PRODUCTION_CONTEXT
    )
    missing_independent = evaluate_application_authority(approved, separated, 160)
    assert missing_independent.status == AUTHORITY_BLOCKED
    assert missing_independent.application_authority is False
    assert "independent_authority_approval_required" in missing_independent.issues

    independent = build_independent_authority_approval(
        "independent-approval-v076",
        approved,
        "authority-owner-beta",
        "AUTHORITY_OWNER",
        True,
        100,
        200,
        155,
    )
    separated_granted = evaluate_application_authority(
        approved, separated, 160, independent
    )
    assert separated_granted.status == AUTHORITY_GRANTED
    assert separated_granted.application_authority

    same_actor = build_independent_authority_approval(
        "same-actor-approval-v076",
        approved,
        approved.reviewer_id,
        "AUTHORITY_OWNER",
        True,
        100,
        200,
        155,
    )
    same_actor_blocked = evaluate_application_authority(
        approved, separated, 160, same_actor
    )
    assert same_actor_blocked.status == AUTHORITY_BLOCKED
    assert "independent_authority_actor_not_independent" in same_actor_blocked.issues

    rejected = signed_review(
        status=REVIEW_REJECTED,
        decision=REJECT_MEMORY_SELECTION,
        application_authority=False,
    )
    rejected_decision = evaluate_application_authority(rejected, solo_production, 160)
    assert rejected_decision.status == AUTHORITY_BLOCKED
    assert "authority_review_not_approved" in rejected_decision.issues
    assert "authority_review_application_authority_missing" in rejected_decision.issues

    tampered_policy = replace(solo_production, policy_id="tampered-policy-v076")
    assert tampered_policy.policy_digest != authority_role_policy_digest(tampered_policy)
    tampered_decision = evaluate_application_authority(approved, tampered_policy, 160)
    assert tampered_decision.status == AUTHORITY_BLOCKED
    assert "authority_role_policy_digest_mismatch" in tampered_decision.issues

    print(json.dumps({
        "status": "KUUOS_AUTHORITY_ROLE_TOPOLOGY_V0_76_VALIDATED",
        "solo_research_decision_digest": research_decision.decision_digest,
        "solo_production_decision_digest": production_decision.decision_digest,
        "separated_decision_digest": separated_granted.decision_digest,
        "checks": [
            "solo-research-needs-no-independent-approval",
            "solo-production-needs-no-independent-approval",
            "operating-context-does-not-force-role-separation",
            "separated-topology-requires-independent-approval",
            "same-actor-independent-approval-rejected",
            "nonapproval-rejected",
            "policy-tamper-rejected",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
