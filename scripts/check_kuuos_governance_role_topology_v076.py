#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_governance_role_topology_v0_76 import (
    ALLOWED_GOVERNANCE_MODES,
    PRODUCTION,
    ROLE_TOPOLOGY_ACCEPTED,
    ROLE_TOPOLOGY_BLOCKED,
    build_governance_role_policy,
    evaluate_governance_role_topology,
    governance_role_policy_digest,
    governance_role_topology_receipt_digest,
)
from runtime.kuuos_memory_review_receipt_v0_74 import (
    APPROVE_MEMORY_SELECTION,
    MemoryReviewReceipt,
    memory_review_receipt_digest,
)
from runtime.kuuos_memory_selection_review_v0_74 import REVIEW_APPROVED


def approved_review() -> MemoryReviewReceipt:
    review = MemoryReviewReceipt(
        REVIEW_APPROVED,
        APPROVE_MEMORY_SELECTION,
        "request-digest",
        "selection-record-digest",
        "reviewer-alpha",
        "external-reviewer",
        "source-history-digest",
        "source-kernel-digest",
        "family-digest",
        "selected-member-digest",
        "selected-deformation-digest",
        "selected-kernel-digest",
        "selected-connection-digest",
        "source-kernel-digest",
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
    return replace(review, receipt_digest=memory_review_receipt_digest(review))


def main() -> int:
    review = approved_review()

    for mode in sorted(ALLOWED_GOVERNANCE_MODES):
        shared_policy = build_governance_role_policy(
            f"{mode.lower()}-shared",
            mode,
            independent_authority_approval_required=False,
        )
        shared = evaluate_governance_role_topology(review, shared_policy)
        assert shared.status == ROLE_TOPOLOGY_ACCEPTED
        assert shared.same_actor
        assert shared.application_authority_preserved
        assert not shared.independent_authority_approval_required
        assert not shared.issues

        independent_policy = build_governance_role_policy(
            f"{mode.lower()}-independent",
            mode,
            independent_authority_approval_required=True,
        )
        same_actor_blocked = evaluate_governance_role_topology(
            review,
            independent_policy,
        )
        assert same_actor_blocked.status == ROLE_TOPOLOGY_BLOCKED
        assert "governance_role_independent_authority_actor_required" in (
            same_actor_blocked.issues
        )

        distinct_actor = evaluate_governance_role_topology(
            review,
            independent_policy,
            authority_actor_id="authority-beta",
        )
        assert distinct_actor.status == ROLE_TOPOLOGY_ACCEPTED
        assert not distinct_actor.same_actor
        assert distinct_actor.application_authority_preserved

    production_shared = build_governance_role_policy(
        "production-shared",
        PRODUCTION,
        independent_authority_approval_required=False,
    )
    production_result = evaluate_governance_role_topology(
        review,
        production_shared,
    )
    assert production_result.status == ROLE_TOPOLOGY_ACCEPTED
    assert production_result.same_actor
    assert production_result.application_authority_preserved

    tampered_policy = replace(
        production_shared,
        independent_authority_approval_required=True,
    )
    tampered_policy_result = evaluate_governance_role_topology(
        review,
        tampered_policy,
        authority_actor_id="authority-beta",
    )
    assert tampered_policy_result.status == ROLE_TOPOLOGY_BLOCKED
    assert "governance_role_policy_digest_mismatch" in tampered_policy_result.issues

    invalid_mode_policy = replace(
        production_shared,
        governance_mode="PRODUCTION_REQUIRES_INDEPENDENCE",
        policy_digest="",
    )
    invalid_mode_policy = replace(
        invalid_mode_policy,
        policy_digest=governance_role_policy_digest(invalid_mode_policy),
    )
    invalid_mode_result = evaluate_governance_role_topology(
        review,
        invalid_mode_policy,
    )
    assert invalid_mode_result.status == ROLE_TOPOLOGY_BLOCKED
    assert "governance_role_policy_mode_invalid" in invalid_mode_result.issues

    tampered_review = replace(
        review,
        production_application_authority=False,
    )
    tampered_review_result = evaluate_governance_role_topology(
        tampered_review,
        production_shared,
    )
    assert tampered_review_result.status == ROLE_TOPOLOGY_BLOCKED
    assert "governance_role_review_receipt_digest_mismatch" in (
        tampered_review_result.issues
    )
    assert "governance_role_application_authority_missing" in (
        tampered_review_result.issues
    )

    assert production_result.receipt_digest == (
        governance_role_topology_receipt_digest(production_result)
    )

    try:
        build_governance_role_policy(
            "invalid",
            "PRODUCTION_ONLY_INDEPENDENT",
        )
    except ValueError as exc:
        assert str(exc) == "governance_role_policy_mode_invalid"
    else:
        raise AssertionError("invalid governance mode was accepted")

    print(json.dumps({
        "status": "KUUOS_GOVERNANCE_ROLE_TOPOLOGY_V0_76_VALIDATED",
        "production_same_actor_allowed": True,
        "governance_mode_determines_independence": False,
        "independent_approval_configurable_in_every_mode": True,
        "review_receipt_digest": review.receipt_digest,
        "production_policy_digest": production_shared.policy_digest,
        "production_topology_receipt_digest": production_result.receipt_digest,
        "checks": [
            "all-modes-support-shared-actor-policy",
            "all-modes-support-independent-actor-policy",
            "production-does-not-force-independent-approval",
            "policy-tamper-rejected",
            "invalid-mode-rejected",
            "review-tamper-rejected",
            "no-immediate-write-or-live-application",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
