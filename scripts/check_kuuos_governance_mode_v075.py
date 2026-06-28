#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_governance_mode_v0_75 import (
    GovernanceModePolicy,
    PRODUCTION_POLICY,
    SOLO_RESEARCH_POLICY,
    TEAM_RESEARCH_AGGREGATED_POLICY,
    TEAM_RESEARCH_SEPARATED_POLICY,
    governance_mode_policy_issues,
    governance_mode_policy_valid,
)


def assert_invalid(policy: GovernanceModePolicy, expected_issue: str) -> None:
    issues = governance_mode_policy_issues(policy)
    assert not governance_mode_policy_valid(policy)
    assert expected_issue in issues


def main() -> int:
    assert governance_mode_policy_valid(SOLO_RESEARCH_POLICY)
    assert SOLO_RESEARCH_POLICY.role_aggregation_permitted
    assert not SOLO_RESEARCH_POLICY.independent_authority_approval_required

    assert governance_mode_policy_valid(TEAM_RESEARCH_AGGREGATED_POLICY)
    assert governance_mode_policy_valid(TEAM_RESEARCH_SEPARATED_POLICY)

    assert governance_mode_policy_valid(PRODUCTION_POLICY)
    assert PRODUCTION_POLICY.independent_authority_approval_required
    assert not PRODUCTION_POLICY.role_aggregation_permitted

    assert_invalid(
        replace(
            SOLO_RESEARCH_POLICY,
            independent_authority_approval_required=True,
        ),
        "solo_research_independent_approval_must_not_be_required",
    )
    assert_invalid(
        replace(SOLO_RESEARCH_POLICY, role_aggregation_permitted=False),
        "solo_research_role_aggregation_must_be_permitted",
    )
    assert_invalid(
        replace(
            TEAM_RESEARCH_AGGREGATED_POLICY,
            independent_authority_approval_required=True,
        ),
        "team_research_policy_is_internally_inconsistent",
    )
    assert_invalid(
        replace(PRODUCTION_POLICY, role_aggregation_permitted=True),
        "production_role_aggregation_forbidden",
    )
    assert_invalid(
        replace(
            PRODUCTION_POLICY,
            independent_authority_approval_required=False,
        ),
        "production_independent_approval_required",
    )
    assert_invalid(
        replace(SOLO_RESEARCH_POLICY, future_role_separation_supported=False),
        "future_role_separation_not_supported",
    )

    print(
        json.dumps(
            {
                "status": "KUUOS_GOVERNANCE_MODE_V0_75_VALIDATED",
                "default_policy": SOLO_RESEARCH_POLICY.to_dict(),
                "checks": [
                    "solo-research-role-aggregation-permitted",
                    "solo-research-independent-approval-not-required",
                    "team-research-aggregated-policy-valid",
                    "team-research-separated-policy-valid",
                    "team-research-inconsistent-policy-rejected",
                    "production-independent-approval-required",
                    "production-role-aggregation-forbidden",
                    "future-role-separation-preserved",
                    "v0.74-review-path-unchanged",
                ],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
