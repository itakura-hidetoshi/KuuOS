#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_memory_review_receipt_v0_74 import (
    MemoryReviewReceipt,
    memory_review_receipt_digest,
)
from runtime.kuuos_memory_selection_review_v0_74 import REVIEW_APPROVED

VERSION = "kuuos_governance_role_topology_v0_76"

SOLO_RESEARCH = "SOLO_RESEARCH"
TEAM_RESEARCH = "TEAM_RESEARCH"
PRODUCTION = "PRODUCTION"
ALLOWED_GOVERNANCE_MODES = frozenset({
    SOLO_RESEARCH,
    TEAM_RESEARCH,
    PRODUCTION,
})

ROLE_TOPOLOGY_ACCEPTED = "GOVERNANCE_ROLE_TOPOLOGY_ACCEPTED"
ROLE_TOPOLOGY_BLOCKED = "GOVERNANCE_ROLE_TOPOLOGY_BLOCKED"


@dataclass(frozen=True)
class GovernanceRolePolicy:
    policy_id: str
    governance_mode: str
    independent_authority_approval_required: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def governance_role_policy_digest(policy: GovernanceRolePolicy) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


def build_governance_role_policy(
    policy_id: str,
    governance_mode: str,
    independent_authority_approval_required: bool = False,
) -> GovernanceRolePolicy:
    if not policy_id:
        raise ValueError("governance_role_policy_id_required")
    if governance_mode not in ALLOWED_GOVERNANCE_MODES:
        raise ValueError("governance_role_policy_mode_invalid")
    policy = GovernanceRolePolicy(
        policy_id,
        governance_mode,
        independent_authority_approval_required,
        "",
    )
    return replace(policy, policy_digest=governance_role_policy_digest(policy))


@dataclass(frozen=True)
class GovernanceRoleTopologyReceipt:
    status: str
    review_receipt_digest: str
    policy_digest: str
    governance_mode: str
    reviewer_id: str
    authority_actor_id: str
    independent_authority_approval_required: bool
    same_actor: bool
    application_authority_preserved: bool
    writes_enabled: bool
    live_application_enabled: bool
    permission_expansion_enabled: bool
    issues: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["issues"] = list(self.issues)
        return payload


def governance_role_topology_receipt_digest(
    receipt: GovernanceRoleTopologyReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


def evaluate_governance_role_topology(
    review: MemoryReviewReceipt,
    policy: GovernanceRolePolicy,
    authority_actor_id: str | None = None,
) -> GovernanceRoleTopologyReceipt:
    issues: list[str] = []

    if policy.policy_digest != governance_role_policy_digest(policy):
        issues.append("governance_role_policy_digest_mismatch")
    if policy.governance_mode not in ALLOWED_GOVERNANCE_MODES:
        issues.append("governance_role_policy_mode_invalid")
    if review.receipt_digest != memory_review_receipt_digest(review):
        issues.append("governance_role_review_receipt_digest_mismatch")
    if review.status != REVIEW_APPROVED:
        issues.append("governance_role_review_not_approved")
    if not review.production_application_authority:
        issues.append("governance_role_application_authority_missing")
    if review.issues:
        issues.append("governance_role_review_contains_issues")
    if review.writes_enabled:
        issues.append("governance_role_review_write_enabled")
    if review.live_application_enabled:
        issues.append("governance_role_review_live_application_enabled")
    if review.permission_expansion_enabled:
        issues.append("governance_role_review_permission_expansion_enabled")
    if review.rollback_target_replacement_enabled:
        issues.append("governance_role_review_rollback_replacement_enabled")

    resolved_authority_actor_id = authority_actor_id or review.reviewer_id
    if not resolved_authority_actor_id:
        issues.append("governance_role_authority_actor_required")

    same_actor = resolved_authority_actor_id == review.reviewer_id
    if policy.independent_authority_approval_required and same_actor:
        issues.append("governance_role_independent_authority_actor_required")

    issues = list(dict.fromkeys(issues))
    accepted = not issues
    receipt = GovernanceRoleTopologyReceipt(
        ROLE_TOPOLOGY_ACCEPTED if accepted else ROLE_TOPOLOGY_BLOCKED,
        review.receipt_digest,
        policy.policy_digest,
        policy.governance_mode,
        review.reviewer_id,
        resolved_authority_actor_id,
        policy.independent_authority_approval_required,
        same_actor,
        accepted and review.production_application_authority,
        False,
        False,
        False,
        tuple(issues),
        "",
    )
    return replace(
        receipt,
        receipt_digest=governance_role_topology_receipt_digest(receipt),
    )
