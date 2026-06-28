#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_governance_role_topology_v0_77 import (
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

        separated_policy = build_governance_role_policy(
            f"{mode.lower()}-separated",
            mode,
            independent_authority_approval_required=True,
        )
        same_actor_blocked = evaluate_governance_role_topology(
            review,
            separated_policy,
        )
        assert same_actor_blocked.status == ROLE_TOPOLOGY_BLOCKED
        assert "governance_role_independent_authority_actor_required" in (
            same_actor_blocked.issues
        )

        distinct_actor = evaluate_governance_role_topology(
            review,
            separated_policy,
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

    unknown_mode_policy = replace(
        production_shared,
        governance_mode="UNKNOWN_MODE",
        policy_digest="",
    )
    unknown_mode_policy = replace(
        unknown_mode_policy,
        policy_digest=governance_role_policy_digest(unknown_mode_policy),
    )
    unknown_mode_result = evaluate_governance_role_topology(
        review,
        unknown_mode_policy,
    )
    assert unknown_mode_result.status == ROLE_TOPOLOGY_BLOCKED
    assert "governance_role_policy_mode_invalid" in unknown_mode_result.issues

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

    print(json.dumps({
        "status": "KUUOS_GOVERNANCE_ROLE_TOPOLOGY_V0_77_VALIDATED",
        "mode_determines_topology": False,
        "topology_configurable_in_every_mode": True,
        "production_uses_configured_policy": True,
        "review_receipt_digest": review.receipt_digest,
        "production_policy_digest": production_shared.policy_digest,
        "topology_receipt_digest": production_result.receipt_digest,
        "checks": [
            "shared-policy-in-every-mode",
            "separated-policy-in-every-mode",
            "mode-topology-orthogonality",
            "policy-tamper-rejected",
            "unknown-mode-rejected",
            "review-tamper-rejected",
            "no-immediate-effect",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
