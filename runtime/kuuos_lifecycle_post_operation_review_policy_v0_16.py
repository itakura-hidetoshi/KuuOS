from __future__ import annotations

from dataclasses import fields, replace

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import (
    LifecyclePostOperationReviewPolicyV016,
    policy_digest,
)


def make_policy(
    policy_id: str,
    *,
    allowed_post_operation_reviewer_ids: tuple[str, ...],
    allowed_post_operation_reviewer_organization_ids: tuple[str, ...],
    allowed_target_resource_ids: tuple[str, ...],
    max_review_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
    max_scope_items: int = 32,
) -> LifecyclePostOperationReviewPolicyV016:
    value = LifecyclePostOperationReviewPolicyV016(
        policy_id=policy_id,
        allowed_post_operation_reviewer_ids=canon(
            allowed_post_operation_reviewer_ids
        ),
        allowed_post_operation_reviewer_organization_ids=canon(
            allowed_post_operation_reviewer_organization_ids
        ),
        allowed_target_resource_ids=canon(allowed_target_resource_ids),
        max_review_delay_seconds=max_review_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_scope_items=max_scope_items,
        require_complete_source_recomputation=True,
        require_completed_source_operation=True,
        require_exact_source_artifact_binding=True,
        require_exact_post_operation_reviewer_binding=True,
        require_exact_route_binding=True,
        require_post_operation_reviewer_completion_reviewer_separation=True,
        require_post_operation_reviewer_prior_actor_separation=True,
        require_post_operation_reviewer_organization_separation=True,
        require_post_operation_reviewer_mandate=True,
        require_post_operation_reviewer_qualification=True,
        require_post_operation_reviewer_identity_confirmation=True,
        require_conflict_disclosure=True,
        require_jurisdiction=True,
        require_review_readiness=True,
        require_intended_observed_result_comparison=True,
        require_target_post_state_review=True,
        require_collateral_effect_review=True,
        require_protected_resource_continuity=True,
        require_protected_core_continuity=True,
        require_monitoring_evidence_review=True,
        require_completion_evidence_review=True,
        require_no_unresolved_anomaly=True,
        require_no_rollback=True,
        require_no_recovery=True,
        post_operation_review_artifact_only=True,
        lifecycle_state_read_only=True,
        repository_read_only=True,
        policy_digest="",
    )
    value = replace(value, policy_digest=policy_digest(value))
    issues = policy_issues(value)
    if issues:
        raise ValueError(f"lifecycle_post_operation_review_policy_invalid:{issues[0]}")
    return value


def policy_issues(
    value: LifecyclePostOperationReviewPolicyV016,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    for name in (
        "allowed_post_operation_reviewer_ids",
        "allowed_post_operation_reviewer_organization_ids",
        "allowed_target_resource_ids",
    ):
        items = getattr(value, name)
        if not items or items != canon(items):
            issues.append(f"{name}_invalid")
    if min(
        value.max_review_delay_seconds,
        value.max_evidence_age_seconds,
        value.max_scope_items,
    ) <= 0:
        issues.append("bound_invalid")
    guards = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name.startswith("require_")
    ) + (
        value.post_operation_review_artifact_only,
        value.lifecycle_state_read_only,
        value.repository_read_only,
    )
    if not all(guards):
        issues.append("required_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)
