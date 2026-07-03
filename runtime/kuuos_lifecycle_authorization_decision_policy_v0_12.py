from __future__ import annotations

from dataclasses import fields, replace

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    LifecycleAuthorizationDecisionPolicyV012,
    policy_digest,
)


def make_policy(
    policy_id: str,
    *,
    allowed_authorization_decision_maker_ids: tuple[str, ...],
    allowed_authorization_decision_maker_organization_ids: tuple[str, ...],
    allowed_target_resource_ids: tuple[str, ...],
    max_decision_delay_seconds: int = 86_400,
    max_evidence_age_seconds: int = 3_600,
    max_decision_expiry_seconds: int = 86_400,
    max_operation_approval_delay_seconds: int = 3_600,
    max_operation_window_seconds: int = 900,
    max_scope_items: int = 32,
) -> LifecycleAuthorizationDecisionPolicyV012:
    value = LifecycleAuthorizationDecisionPolicyV012(
        policy_id=policy_id,
        allowed_authorization_decision_maker_ids=canon(
            allowed_authorization_decision_maker_ids
        ),
        allowed_authorization_decision_maker_organization_ids=canon(
            allowed_authorization_decision_maker_organization_ids
        ),
        allowed_target_resource_ids=canon(allowed_target_resource_ids),
        max_decision_delay_seconds=max_decision_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_decision_expiry_seconds=max_decision_expiry_seconds,
        max_operation_approval_delay_seconds=max_operation_approval_delay_seconds,
        max_operation_window_seconds=max_operation_window_seconds,
        max_scope_items=max_scope_items,
        require_complete_source_recomputation=True,
        require_clear_source_review=True,
        require_designated_decision_maker_binding=True,
        require_decision_maker_mandate=True,
        require_decision_maker_qualification=True,
        require_decision_maker_independence=True,
        require_conflict_disclosure=True,
        require_jurisdiction=True,
        require_quorum=True,
        require_reasoned_decision=True,
        require_proportionality_review=True,
        require_less_restrictive_alternatives_review=True,
        require_irreversibility_review=True,
        require_human_impact_review=True,
        require_exact_scope_binding=True,
        require_package_safety=True,
        require_operation_approval_route=True,
        require_appeal_route=True,
        require_dissent_route=True,
        require_minority_opinion_record=True,
        require_role_separation=True,
        authorization_decision_artifact_only=True,
        lifecycle_read_only=True,
        policy_digest="",
    )
    value = replace(value, policy_digest=policy_digest(value))
    issues = policy_issues(value)
    if issues:
        raise ValueError(
            f"lifecycle_authorization_decision_policy_invalid:{issues[0]}"
        )
    return value


def policy_issues(
    value: LifecycleAuthorizationDecisionPolicyV012,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    for name in (
        "allowed_authorization_decision_maker_ids",
        "allowed_authorization_decision_maker_organization_ids",
        "allowed_target_resource_ids",
    ):
        items = getattr(value, name)
        if not items or items != canon(items):
            issues.append(f"{name}_invalid")
    if min(
        value.max_decision_delay_seconds,
        value.max_evidence_age_seconds,
        value.max_decision_expiry_seconds,
        value.max_operation_approval_delay_seconds,
        value.max_operation_window_seconds,
        value.max_scope_items,
    ) <= 0:
        issues.append("bound_invalid")
    guards = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name.startswith("require_")
    ) + (
        value.authorization_decision_artifact_only,
        value.lifecycle_read_only,
    )
    if not all(guards):
        issues.append("required_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)
