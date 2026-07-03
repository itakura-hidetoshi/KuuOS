from __future__ import annotations

from dataclasses import fields, replace

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_operation_start_types_v0_14 import (
    LifecycleOperationStartPolicyV014,
    policy_digest,
)


def make_policy(
    policy_id: str,
    *,
    allowed_operator_ids: tuple[str, ...],
    allowed_operator_organization_ids: tuple[str, ...],
    allowed_target_resource_ids: tuple[str, ...],
    max_start_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
    max_operation_window_seconds: int = 900,
    max_scope_items: int = 32,
) -> LifecycleOperationStartPolicyV014:
    value = LifecycleOperationStartPolicyV014(
        policy_id=policy_id,
        allowed_operator_ids=canon(allowed_operator_ids),
        allowed_operator_organization_ids=canon(
            allowed_operator_organization_ids
        ),
        allowed_target_resource_ids=canon(allowed_target_resource_ids),
        max_start_delay_seconds=max_start_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_operation_window_seconds=max_operation_window_seconds,
        max_scope_items=max_scope_items,
        require_complete_source_recomputation=True,
        require_approved_source_operation_approval=True,
        require_exact_source_artifact_binding=True,
        require_exact_operator_binding=True,
        require_exact_route_binding=True,
        require_operator_approver_separation=True,
        require_operator_mandate=True,
        require_operator_qualification=True,
        require_operator_identity_confirmation=True,
        require_conflict_disclosure=True,
        require_jurisdiction=True,
        require_operator_readiness=True,
        require_start_authorization_acknowledgement=True,
        require_execution_package_reconfirmation=True,
        require_resource_reservation_reconfirmation=True,
        require_exact_scope_binding=True,
        require_rollback_reconfirmation=True,
        require_recovery_reconfirmation=True,
        require_stop_condition_reconfirmation=True,
        require_abort_channel_reconfirmation=True,
        require_human_oversight_reconfirmation=True,
        require_monitoring_reconfirmation=True,
        require_evidence_capture_reconfirmation=True,
        require_no_irreversible_steps=True,
        require_protected_core_exclusion=True,
        operation_start_artifact_only=True,
        lifecycle_state_read_only=True,
        repository_read_only=True,
        policy_digest="",
    )
    value = replace(value, policy_digest=policy_digest(value))
    issues = policy_issues(value)
    if issues:
        raise ValueError(f"lifecycle_operation_start_policy_invalid:{issues[0]}")
    return value


def policy_issues(value: LifecycleOperationStartPolicyV014) -> tuple[str, ...]:
    issues: list[str] = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    for name in (
        "allowed_operator_ids",
        "allowed_operator_organization_ids",
        "allowed_target_resource_ids",
    ):
        items = getattr(value, name)
        if not items or items != canon(items):
            issues.append(f"{name}_invalid")
    if min(
        value.max_start_delay_seconds,
        value.max_evidence_age_seconds,
        value.max_operation_window_seconds,
        value.max_scope_items,
    ) <= 0:
        issues.append("bound_invalid")
    guards = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name.startswith("require_")
    ) + (
        value.operation_start_artifact_only,
        value.lifecycle_state_read_only,
        value.repository_read_only,
    )
    if not all(guards):
        issues.append("required_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)
