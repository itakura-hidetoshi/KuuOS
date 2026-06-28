#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class GovernanceMode(str, Enum):
    SOLO_RESEARCH = "SOLO_RESEARCH"
    TEAM_RESEARCH = "TEAM_RESEARCH"
    PRODUCTION = "PRODUCTION"


@dataclass(frozen=True)
class GovernanceModePolicy:
    mode: GovernanceMode
    independent_authority_approval_required: bool
    role_aggregation_permitted: bool
    future_role_separation_supported: bool = True

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["mode"] = self.mode.value
        return payload


SOLO_RESEARCH_POLICY = GovernanceModePolicy(
    mode=GovernanceMode.SOLO_RESEARCH,
    independent_authority_approval_required=False,
    role_aggregation_permitted=True,
)

TEAM_RESEARCH_AGGREGATED_POLICY = GovernanceModePolicy(
    mode=GovernanceMode.TEAM_RESEARCH,
    independent_authority_approval_required=False,
    role_aggregation_permitted=True,
)

TEAM_RESEARCH_SEPARATED_POLICY = GovernanceModePolicy(
    mode=GovernanceMode.TEAM_RESEARCH,
    independent_authority_approval_required=True,
    role_aggregation_permitted=False,
)

PRODUCTION_POLICY = GovernanceModePolicy(
    mode=GovernanceMode.PRODUCTION,
    independent_authority_approval_required=True,
    role_aggregation_permitted=False,
)


def governance_mode_policy_issues(policy: GovernanceModePolicy) -> tuple[str, ...]:
    issues: list[str] = []

    if not policy.future_role_separation_supported:
        issues.append("future_role_separation_not_supported")

    if policy.mode is GovernanceMode.SOLO_RESEARCH:
        if policy.independent_authority_approval_required:
            issues.append("solo_research_independent_approval_must_not_be_required")
        if not policy.role_aggregation_permitted:
            issues.append("solo_research_role_aggregation_must_be_permitted")

    elif policy.mode is GovernanceMode.TEAM_RESEARCH:
        if (
            policy.role_aggregation_permitted
            == policy.independent_authority_approval_required
        ):
            issues.append("team_research_policy_is_internally_inconsistent")

    elif policy.mode is GovernanceMode.PRODUCTION:
        if not policy.independent_authority_approval_required:
            issues.append("production_independent_approval_required")
        if policy.role_aggregation_permitted:
            issues.append("production_role_aggregation_forbidden")

    else:
        issues.append("unknown_governance_mode")

    return tuple(issues)


def governance_mode_policy_valid(policy: GovernanceModePolicy) -> bool:
    return not governance_mode_policy_issues(policy)
