from __future__ import annotations

from dataclasses import fields, replace

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import (
    LifecycleTransitionReviewPolicyV017,
    policy_digest,
)


def make_policy(
    policy_id: str,
    *,
    allowed_transition_reviewer_ids: tuple[str, ...],
    allowed_transition_reviewer_organization_ids: tuple[str, ...],
    allowed_transition_decision_maker_ids: tuple[str, ...],
    allowed_target_resource_ids: tuple[str, ...],
    allowed_transition_kinds: tuple[str, ...],
    max_review_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
    max_review_expiry_seconds: int = 1800,
    max_decision_delay_seconds: int = 900,
    max_scope_items: int = 32,
) -> LifecycleTransitionReviewPolicyV017:
    value = LifecycleTransitionReviewPolicyV017(
        policy_id=policy_id,
        allowed_transition_reviewer_ids=canon(allowed_transition_reviewer_ids),
        allowed_transition_reviewer_organization_ids=canon(
            allowed_transition_reviewer_organization_ids
        ),
        allowed_transition_decision_maker_ids=canon(
            allowed_transition_decision_maker_ids
        ),
        allowed_target_resource_ids=canon(allowed_target_resource_ids),
        allowed_transition_kinds=canon(allowed_transition_kinds),
        max_review_delay_seconds=max_review_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_review_expiry_seconds=max_review_expiry_seconds,
        max_decision_delay_seconds=max_decision_delay_seconds,
        max_scope_items=max_scope_items,
        require_complete_source_recomputation=True,
        require_reviewed_source_post_operation_review=True,
        require_exact_source_artifact_binding=True,
        require_exact_transition_reviewer_binding=True,
        require_exact_route_binding=True,
        require_transition_reviewer_source_reviewer_separation=True,
        require_transition_reviewer_prior_actor_separation=True,
        require_transition_reviewer_decision_maker_separation=True,
        require_transition_reviewer_organization_separation=True,
        require_transition_reviewer_mandate=True,
        require_transition_reviewer_qualification=True,
        require_transition_reviewer_identity_confirmation=True,
        require_conflict_disclosure=True,
        require_jurisdiction=True,
        require_review_readiness=True,
        require_transition_basis=True,
        require_necessity_assessment=True,
        require_proportionality_assessment=True,
        require_reversibility_assessment=True,
        require_dependency_clearance=True,
        require_authority_continuity=True,
        require_transition_state_compatibility=True,
        require_stakeholder_impact_assessment=True,
        require_legal_policy_compliance=True,
        require_appeal_route=True,
        require_dissent_route=True,
        require_minority_opinion_record=True,
        require_no_unresolved_anomaly=True,
        require_no_recovery=True,
        require_no_institutional_hold=True,
        require_no_emergency_state=True,
        transition_review_artifact_only=True,
        lifecycle_state_read_only=True,
        repository_read_only=True,
        policy_digest="",
    )
    value = replace(value, policy_digest=policy_digest(value))
    issues = policy_issues(value)
    if issues:
        raise ValueError(f"lifecycle_transition_review_policy_invalid:{issues[0]}")
    return value


def policy_issues(value: LifecycleTransitionReviewPolicyV017) -> tuple[str, ...]:
    issues: list[str] = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    for name in (
        "allowed_transition_reviewer_ids",
        "allowed_transition_reviewer_organization_ids",
        "allowed_transition_decision_maker_ids",
        "allowed_target_resource_ids",
        "allowed_transition_kinds",
    ):
        items = getattr(value, name)
        if not items or items != canon(items):
            issues.append(f"{name}_invalid")
    if min(
        value.max_review_delay_seconds,
        value.max_evidence_age_seconds,
        value.max_review_expiry_seconds,
        value.max_decision_delay_seconds,
        value.max_scope_items,
    ) <= 0:
        issues.append("bound_invalid")
    guards = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name.startswith("require_")
    ) + (
        value.transition_review_artifact_only,
        value.lifecycle_state_read_only,
        value.repository_read_only,
    )
    if not all(guards):
        issues.append("required_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)
