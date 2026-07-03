from __future__ import annotations

from dataclasses import fields, replace

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    LifecycleOperationCompletionPolicyV015,
    policy_digest,
)


def make_policy(
    policy_id: str,
    *,
    allowed_completion_reviewer_ids: tuple[str, ...],
    allowed_completion_reviewer_organization_ids: tuple[str, ...],
    allowed_target_resource_ids: tuple[str, ...],
    max_completion_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
    max_scope_items: int = 32,
) -> LifecycleOperationCompletionPolicyV015:
    value = LifecycleOperationCompletionPolicyV015(
        policy_id=policy_id,
        allowed_completion_reviewer_ids=canon(allowed_completion_reviewer_ids),
        allowed_completion_reviewer_organization_ids=canon(
            allowed_completion_reviewer_organization_ids
        ),
        allowed_target_resource_ids=canon(allowed_target_resource_ids),
        max_completion_delay_seconds=max_completion_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_scope_items=max_scope_items,
        require_complete_source_recomputation=True,
        require_started_source_operation=True,
        require_exact_source_artifact_binding=True,
        require_exact_completion_reviewer_binding=True,
        require_exact_route_binding=True,
        require_completion_reviewer_operator_separation=True,
        require_completion_reviewer_prior_actor_separation=True,
        require_completion_reviewer_mandate=True,
        require_completion_reviewer_qualification=True,
        require_completion_reviewer_identity_confirmation=True,
        require_conflict_disclosure=True,
        require_jurisdiction=True,
        require_completion_readiness=True,
        require_operation_execution_finished=True,
        require_execution_result_integrity=True,
        require_all_scope_items_accounted=True,
        require_all_reversible_steps_accounted=True,
        require_no_irreversible_steps=True,
        require_target_post_state_evidence=True,
        require_protected_resource_integrity=True,
        require_protected_core_integrity=True,
        require_resource_reservation_release=True,
        require_monitoring_completion=True,
        require_evidence_capture_completion=True,
        require_no_unresolved_stop_condition=True,
        require_abort_not_triggered=True,
        require_no_pending_rollback=True,
        require_no_pending_recovery=True,
        operation_completion_artifact_only=True,
        lifecycle_state_read_only=True,
        repository_read_only=True,
        policy_digest="",
    )
    value = replace(value, policy_digest=policy_digest(value))
    issues = policy_issues(value)
    if issues:
        raise ValueError(f"lifecycle_operation_completion_policy_invalid:{issues[0]}")
    return value


def policy_issues(value: LifecycleOperationCompletionPolicyV015) -> tuple[str, ...]:
    issues: list[str] = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    for name in (
        "allowed_completion_reviewer_ids",
        "allowed_completion_reviewer_organization_ids",
        "allowed_target_resource_ids",
    ):
        items = getattr(value, name)
        if not items or items != canon(items):
            issues.append(f"{name}_invalid")
    if min(
        value.max_completion_delay_seconds,
        value.max_evidence_age_seconds,
        value.max_scope_items,
    ) <= 0:
        issues.append("bound_invalid")
    guards = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name.startswith("require_")
    ) + (
        value.operation_completion_artifact_only,
        value.lifecycle_state_read_only,
        value.repository_read_only,
    )
    if not all(guards):
        issues.append("required_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)
