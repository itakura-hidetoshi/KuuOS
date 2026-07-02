from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_review_types_v0_9 import (
    LifecycleReviewPolicyV09,
    lifecycle_review_policy_digest,
)


def canon(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def make_policy(
    policy_id: str,
    *,
    allowed_reviewer_ids: tuple[str, ...],
    allowed_reviewer_organization_ids: tuple[str, ...],
    allowed_target_resource_ids: tuple[str, ...],
    max_review_delay_seconds: int = 86_400,
    max_evidence_age_seconds: int = 3_600,
    max_review_expiry_seconds: int = 86_400,
    max_execution_window_seconds: int = 900,
    max_scope_items: int = 32,
) -> LifecycleReviewPolicyV09:
    value = LifecycleReviewPolicyV09(
        policy_id=policy_id,
        allowed_reviewer_ids=canon(allowed_reviewer_ids),
        allowed_reviewer_organization_ids=canon(
            allowed_reviewer_organization_ids
        ),
        allowed_target_resource_ids=canon(allowed_target_resource_ids),
        max_review_delay_seconds=max_review_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_review_expiry_seconds=max_review_expiry_seconds,
        max_execution_window_seconds=max_execution_window_seconds,
        max_scope_items=max_scope_items,
        require_complete_source_recomputation=True,
        require_ready_source=True,
        require_qualification=True,
        require_independence=True,
        require_conflict_disclosure=True,
        require_package_safety=True,
        require_appeal_route=True,
        require_dissent_route=True,
        require_operator_separation=True,
        read_only=True,
        policy_digest="",
    )
    value = replace(value, policy_digest=lifecycle_review_policy_digest(value))
    issues = policy_issues(value)
    if issues:
        raise ValueError(f"execution_review_policy_invalid:{issues[0]}")
    return value


def policy_issues(value: LifecycleReviewPolicyV09) -> tuple[str, ...]:
    issues: list[str] = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    for name in (
        "allowed_reviewer_ids",
        "allowed_reviewer_organization_ids",
        "allowed_target_resource_ids",
    ):
        items = getattr(value, name)
        if not items or items != canon(items):
            issues.append(f"{name}_invalid")
    if min(
        value.max_review_delay_seconds,
        value.max_evidence_age_seconds,
        value.max_review_expiry_seconds,
        value.max_execution_window_seconds,
        value.max_scope_items,
    ) <= 0:
        issues.append("bound_invalid")
    guards = (
        value.require_complete_source_recomputation,
        value.require_ready_source,
        value.require_qualification,
        value.require_independence,
        value.require_conflict_disclosure,
        value.require_package_safety,
        value.require_appeal_route,
        value.require_dissent_route,
        value.require_operator_separation,
        value.read_only,
    )
    if not all(guards):
        issues.append("required_guard_disabled")
    if value.policy_digest != lifecycle_review_policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)
