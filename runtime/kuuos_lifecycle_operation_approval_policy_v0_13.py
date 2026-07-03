from __future__ import annotations

from dataclasses import fields, replace

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import (
    LifecycleOperationApprovalPolicyV013,
    policy_digest,
)


def make_policy(
    policy_id: str,
    *,
    allowed_operation_approver_ids: tuple[str, ...],
    allowed_operation_approver_organization_ids: tuple[str, ...],
    allowed_future_operator_ids: tuple[str, ...],
    allowed_target_resource_ids: tuple[str, ...],
    max_approval_delay_seconds: int = 3_600,
    max_evidence_age_seconds: int = 600,
    max_approval_expiry_seconds: int = 3_600,
    max_operation_start_delay_seconds: int = 900,
    max_operation_window_seconds: int = 900,
    max_scope_items: int = 32,
) -> LifecycleOperationApprovalPolicyV013:
    value = LifecycleOperationApprovalPolicyV013(
        policy_id=policy_id,
        allowed_operation_approver_ids=canon(allowed_operation_approver_ids),
        allowed_operation_approver_organization_ids=canon(
            allowed_operation_approver_organization_ids
        ),
        allowed_future_operator_ids=canon(allowed_future_operator_ids),
        allowed_target_resource_ids=canon(allowed_target_resource_ids),
        max_approval_delay_seconds=max_approval_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_approval_expiry_seconds=max_approval_expiry_seconds,
        max_operation_start_delay_seconds=max_operation_start_delay_seconds,
        max_operation_window_seconds=max_operation_window_seconds,
        max_scope_items=max_scope_items,
        require_complete_source_recomputation=True,
        require_approved_source_authorization=True,
        require_exact_route_binding=True,
        require_operation_approver_mandate=True,
        require_operation_approver_qualification=True,
        require_operation_approver_independence=True,
        require_conflict_disclosure=True,
        require_jurisdiction=True,
        require_quorum=True,
        require_reasoned_approval=True,
        require_proportionality_review=True,
        require_operator_acknowledgement=True,
        require_execution_package_integrity=True,
        require_resource_reservation=True,
        require_exact_scope_binding=True,
        require_rollback_readiness=True,
        require_recovery_readiness=True,
        require_stop_conditions=True,
        require_abort_channel=True,
        require_human_oversight=True,
        require_monitoring=True,
        require_evidence_capture=True,
        require_simulation=True,
        require_no_irreversible_steps=True,
        require_protected_core_exclusion=True,
        require_role_separation=True,
        operation_approval_artifact_only=True,
        lifecycle_read_only=True,
        policy_digest="",
    )
    value = replace(value, policy_digest=policy_digest(value))
    issues = policy_issues(value)
    if issues:
        raise ValueError(f"lifecycle_operation_approval_policy_invalid:{issues[0]}")
    return value


def policy_issues(
    value: LifecycleOperationApprovalPolicyV013,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    for name in (
        "allowed_operation_approver_ids",
        "allowed_operation_approver_organization_ids",
        "allowed_future_operator_ids",
        "allowed_target_resource_ids",
    ):
        items = getattr(value, name)
        if not items or items != canon(items):
            issues.append(f"{name}_invalid")
    if min(
        value.max_approval_delay_seconds,
        value.max_evidence_age_seconds,
        value.max_approval_expiry_seconds,
        value.max_operation_start_delay_seconds,
        value.max_operation_window_seconds,
        value.max_scope_items,
    ) <= 0:
        issues.append("bound_invalid")
    guards = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name.startswith("require_")
    ) + (
        value.operation_approval_artifact_only,
        value.lifecycle_read_only,
    )
    if not all(guards):
        issues.append("required_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)
