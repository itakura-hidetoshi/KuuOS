from __future__ import annotations

from dataclasses import fields, replace

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    LifecycleDecisionReviewPolicyV011,
    policy_digest,
)


def make_policy(
    policy_id: str,
    *,
    allowed_decision_reviewer_ids: tuple[str, ...],
    allowed_decision_reviewer_organization_ids: tuple[str, ...],
    allowed_authorization_decision_maker_ids: tuple[str, ...],
    allowed_target_resource_ids: tuple[str, ...],
    max_review_delay_seconds: int = 86_400,
    max_evidence_age_seconds: int = 3_600,
    max_review_expiry_seconds: int = 86_400,
    max_operation_window_seconds: int = 900,
    max_scope_items: int = 32,
) -> LifecycleDecisionReviewPolicyV011:
    value = LifecycleDecisionReviewPolicyV011(
        policy_id=policy_id,
        allowed_decision_reviewer_ids=canon(allowed_decision_reviewer_ids),
        allowed_decision_reviewer_organization_ids=canon(
            allowed_decision_reviewer_organization_ids
        ),
        allowed_authorization_decision_maker_ids=canon(
            allowed_authorization_decision_maker_ids
        ),
        allowed_target_resource_ids=canon(allowed_target_resource_ids),
        max_review_delay_seconds=max_review_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_review_expiry_seconds=max_review_expiry_seconds,
        max_operation_window_seconds=max_operation_window_seconds,
        max_scope_items=max_scope_items,
        require_complete_source_recomputation=True,
        require_issued_source_request=True,
        require_reviewer_qualification=True,
        require_reviewer_independence=True,
        require_conflict_disclosure=True,
        require_exact_scope_binding=True,
        require_package_safety=True,
        require_authorization_route=True,
        require_appeal_route=True,
        require_dissent_route=True,
        require_minority_opinion_record=True,
        require_role_separation=True,
        review_artifact_only=True,
        lifecycle_read_only=True,
        policy_digest="",
    )
    value = replace(value, policy_digest=policy_digest(value))
    issues = policy_issues(value)
    if issues:
        raise ValueError(f"lifecycle_decision_review_policy_invalid:{issues[0]}")
    return value


def policy_issues(value: LifecycleDecisionReviewPolicyV011) -> tuple[str, ...]:
    issues: list[str] = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    for name in (
        "allowed_decision_reviewer_ids",
        "allowed_decision_reviewer_organization_ids",
        "allowed_authorization_decision_maker_ids",
        "allowed_target_resource_ids",
    ):
        items = getattr(value, name)
        if not items or items != canon(items):
            issues.append(f"{name}_invalid")
    if min(
        value.max_review_delay_seconds,
        value.max_evidence_age_seconds,
        value.max_review_expiry_seconds,
        value.max_operation_window_seconds,
        value.max_scope_items,
    ) <= 0:
        issues.append("bound_invalid")
    guards = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name.startswith("require_")
    ) + (value.review_artifact_only, value.lifecycle_read_only)
    if not all(guards):
        issues.append("required_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)
