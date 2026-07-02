from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import (
    LifecycleBoundedRequestPolicyV010,
    policy_digest,
)


def canon(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def make_policy(
    policy_id: str,
    *,
    allowed_requester_ids: tuple[str, ...],
    allowed_requester_organization_ids: tuple[str, ...],
    allowed_decision_authority_ids: tuple[str, ...],
    allowed_target_resource_ids: tuple[str, ...],
    max_request_delay_seconds: int = 86_400,
    max_evidence_age_seconds: int = 3_600,
    max_request_expiry_seconds: int = 86_400,
    max_operation_window_seconds: int = 900,
    max_scope_items: int = 32,
) -> LifecycleBoundedRequestPolicyV010:
    value = LifecycleBoundedRequestPolicyV010(
        policy_id=policy_id,
        allowed_requester_ids=canon(allowed_requester_ids),
        allowed_requester_organization_ids=canon(
            allowed_requester_organization_ids
        ),
        allowed_decision_authority_ids=canon(allowed_decision_authority_ids),
        allowed_target_resource_ids=canon(allowed_target_resource_ids),
        max_request_delay_seconds=max_request_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_request_expiry_seconds=max_request_expiry_seconds,
        max_operation_window_seconds=max_operation_window_seconds,
        max_scope_items=max_scope_items,
        require_complete_source_recomputation=True,
        require_clear_source_review=True,
        require_requester_qualification=True,
        require_requester_independence=True,
        require_conflict_disclosure=True,
        require_exact_scope_binding=True,
        require_package_safety=True,
        require_decision_route=True,
        require_appeal_route=True,
        require_dissent_route=True,
        require_authority_operator_separation=True,
        request_artifact_only=True,
        lifecycle_read_only=True,
        policy_digest="",
    )
    value = replace(value, policy_digest=policy_digest(value))
    issues = policy_issues(value)
    if issues:
        raise ValueError(f"lifecycle_request_policy_invalid:{issues[0]}")
    return value


def policy_issues(value: LifecycleBoundedRequestPolicyV010) -> tuple[str, ...]:
    issues: list[str] = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    for name in (
        "allowed_requester_ids",
        "allowed_requester_organization_ids",
        "allowed_decision_authority_ids",
        "allowed_target_resource_ids",
    ):
        items = getattr(value, name)
        if not items or items != canon(items):
            issues.append(f"{name}_invalid")
    if min(
        value.max_request_delay_seconds,
        value.max_evidence_age_seconds,
        value.max_request_expiry_seconds,
        value.max_operation_window_seconds,
        value.max_scope_items,
    ) <= 0:
        issues.append("bound_invalid")
    guards = (
        value.require_complete_source_recomputation,
        value.require_clear_source_review,
        value.require_requester_qualification,
        value.require_requester_independence,
        value.require_conflict_disclosure,
        value.require_exact_scope_binding,
        value.require_package_safety,
        value.require_decision_route,
        value.require_appeal_route,
        value.require_dissent_route,
        value.require_authority_operator_separation,
        value.request_artifact_only,
        value.lifecycle_read_only,
    )
    if not all(guards):
        issues.append("required_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)
