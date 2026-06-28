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

VERSION = "kuuos_authority_role_topology_v0_76"

ROLE_AGGREGATED = "ROLE_AGGREGATED"
ROLE_SEPARATED = "ROLE_SEPARATED"
ALLOWED_ROLE_TOPOLOGIES = frozenset({ROLE_AGGREGATED, ROLE_SEPARATED})

RESEARCH_CONTEXT = "RESEARCH"
PRODUCTION_CONTEXT = "PRODUCTION"
ALLOWED_OPERATING_CONTEXTS = frozenset({RESEARCH_CONTEXT, PRODUCTION_CONTEXT})

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
        if self.role_topology not in ALLOWED_ROLE_TOPOLOGIES:
            raise ValueError("authority_role_topology_not_allowed")
        if self.operating_context not in ALLOWED_OPERATING_CONTEXTS:
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
    unsigned = AuthorityRolePolicy(
        policy_id,
        role_topology,
        operating_context,
        "",
    )
    return replace(unsigned, policy_digest=authority_role_policy_digest(unsigned))


@dataclass(frozen=True)
class IndependentAuthorityApproval:
    approval_id: str
    review_receipt_digest: str
    authority_actor_id: str
    authority_actor_class: str
    approved: bool
    valid_from_epoch: int
    valid_until_epoch: int
    issued_at_epoch: int
    approval_digest: str
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.approval_id:
            raise ValueError("independent_authority_approval_id_missing")
        if not self.review_receipt_digest:
            raise ValueError("independent_authority_review_binding_missing")
        if not self.authority_actor_id:
            raise ValueError("independent_authority_actor_id_missing")
        if not self.authority_actor_class:
            raise ValueError("independent_authority_actor_class_missing")
        if self.valid_from_epoch > self.valid_until_epoch:
            raise ValueError("independent_authority_validity_window_invalid")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def independent_authority_approval_digest(
    approval: IndependentAuthorityApproval,
) -> str:
    payload = approval.to_dict()
    payload.pop("approval_digest", None)
    return canonical_digest(payload)


def build_independent_authority_approval(
    approval_id: str,
    review: MemoryReviewReceipt,
    authority_actor_id: str,
    authority_actor_class: str,
    approved: bool,
    valid_from_epoch: int,
    valid_until_epoch: int,
    issued_at_epoch: int,
) -> IndependentAuthorityApproval:
    unsigned = IndependentAuthorityApproval(
        approval_id,
        review.receipt_digest,
        authority_actor_id,
        authority_actor_class,
        approved,
        valid_from_epoch,
        valid_until_epoch,
        issued_at_epoch,
        "",
    )
    return replace(
        unsigned,
        approval_digest=independent_authority_approval_digest(unsigned),
    )


@dataclass(frozen=True)
class ApplicationAuthorityDecision:
    status: str
    review_receipt_digest: str
    policy_digest: str
    role_topology: str
    operating_context: str
    independent_approval_required: bool
    independent_approval_digest: str
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
    evaluated_at_epoch: int,
    independent_approval: IndependentAuthorityApproval | None = None,
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

    independent_digest = ""
    if policy.independent_approval_required:
        if independent_approval is None:
            issues.append("independent_authority_approval_required")
        else:
            independent_digest = independent_approval.approval_digest
            if (
                independent_approval.approval_digest
                != independent_authority_approval_digest(independent_approval)
            ):
                issues.append("independent_authority_approval_digest_mismatch")
            if independent_approval.review_receipt_digest != review.receipt_digest:
                issues.append("independent_authority_review_binding_mismatch")
            if not independent_approval.approved:
                issues.append("independent_authority_approval_denied")
            if independent_approval.authority_actor_id == review.reviewer_id:
                issues.append("independent_authority_actor_not_independent")
            if not (
                independent_approval.valid_from_epoch
                <= evaluated_at_epoch
                <= independent_approval.valid_until_epoch
            ):
                issues.append("independent_authority_outside_validity_window")
            if independent_approval.issued_at_epoch > evaluated_at_epoch:
                issues.append("independent_authority_approval_from_future")

    issues = list(dict.fromkeys(issues))
    authority = not issues
    status = AUTHORITY_GRANTED if authority else AUTHORITY_BLOCKED
    unsigned = ApplicationAuthorityDecision(
        status,
        review.receipt_digest,
        policy.policy_digest,
        policy.role_topology,
        policy.operating_context,
        policy.independent_approval_required,
        independent_digest,
        authority,
        tuple(issues),
        "",
    )
    return replace(
        unsigned,
        decision_digest=application_authority_decision_digest(unsigned),
    )
