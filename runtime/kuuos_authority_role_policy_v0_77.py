#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_memory_review_receipt_v0_74 import (
    APPROVE_MEMORY_SELECTION,
    MemoryReviewReceipt,
    memory_review_receipt_digest,
)
from runtime.kuuos_memory_selection_review_v0_74 import REVIEW_APPROVED

VERSION = "kuuos_authority_role_topology_v0_77"

ROLE_AGGREGATED = "ROLE_AGGREGATED"
ROLE_SEPARATED = "ROLE_SEPARATED"
RESEARCH_CONTEXT = "RESEARCH"
PRODUCTION_CONTEXT = "PRODUCTION"

AUTHORITY_GRANTED = "APPLICATION_AUTHORITY_GRANTED"
AUTHORITY_BLOCKED = "APPLICATION_AUTHORITY_BLOCKED"


@dataclass(frozen=True)
class AuthorityRolePolicy:
    policy_id: str
    role_topology: str
    operating_context: str
    policy_digest: str
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.policy_id:
            raise ValueError("authority_role_policy_id_missing")
        if self.role_topology not in {ROLE_AGGREGATED, ROLE_SEPARATED}:
            raise ValueError("authority_role_topology_not_allowed")
        if self.operating_context not in {RESEARCH_CONTEXT, PRODUCTION_CONTEXT}:
            raise ValueError("authority_operating_context_not_allowed")

    @property
    def independent_approval_required(self) -> bool:
        return self.role_topology == ROLE_SEPARATED

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def authority_role_policy_digest(policy: AuthorityRolePolicy) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


def build_authority_role_policy(
    policy_id: str,
    role_topology: str,
    operating_context: str,
) -> AuthorityRolePolicy:
    unsigned = AuthorityRolePolicy(policy_id, role_topology, operating_context, "")
    return replace(unsigned, policy_digest=authority_role_policy_digest(unsigned))


@dataclass(frozen=True)
class ApplicationAuthorityDecision:
    status: str
    role_topology: str
    operating_context: str
    independent_approval_required: bool
    application_authority: bool
    issues: tuple[str, ...]
    decision_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["issues"] = list(self.issues)
        return payload


def application_authority_decision_digest(
    decision: ApplicationAuthorityDecision,
) -> str:
    payload = decision.to_dict()
    payload.pop("decision_digest", None)
    return canonical_digest(payload)


def evaluate_application_authority(
    review: MemoryReviewReceipt,
    policy: AuthorityRolePolicy,
    independent_approval_valid: bool = False,
    independent_actor_id: str = "",
) -> ApplicationAuthorityDecision:
    issues: list[str] = []

    if review.receipt_digest != memory_review_receipt_digest(review):
        issues.append("authority_review_receipt_digest_mismatch")
    if review.status != REVIEW_APPROVED:
        issues.append("authority_review_not_approved")
    if review.decision != APPROVE_MEMORY_SELECTION:
        issues.append("authority_review_decision_not_approval")
    if not review.production_application_authority:
        issues.append("authority_review_application_authority_missing")
    if policy.policy_digest != authority_role_policy_digest(policy):
        issues.append("authority_role_policy_digest_mismatch")

    if policy.independent_approval_required:
        if not independent_approval_valid:
            issues.append("independent_authority_approval_required")
        if not independent_actor_id:
            issues.append("independent_authority_actor_missing")
        elif independent_actor_id == review.reviewer_id:
            issues.append("independent_authority_actor_not_independent")

    issues = list(dict.fromkeys(issues))
    granted = not issues
    unsigned = ApplicationAuthorityDecision(
        AUTHORITY_GRANTED if granted else AUTHORITY_BLOCKED,
        policy.role_topology,
        policy.operating_context,
        policy.independent_approval_required,
        granted,
        tuple(issues),
        "",
    )
    return replace(
        unsigned,
        decision_digest=application_authority_decision_digest(unsigned),
    )
