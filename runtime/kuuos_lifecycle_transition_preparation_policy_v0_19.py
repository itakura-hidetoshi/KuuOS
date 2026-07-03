from __future__ import annotations

from dataclasses import fields, replace

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_transition_preparation_types_v0_19 import (
    LifecycleTransitionPreparationPolicyV019,
    policy_digest,
)


def make_policy(
    policy_id: str,
    *,
    allowed_transition_preparer_ids: tuple[str, ...],
    allowed_transition_preparer_organization_ids: tuple[str, ...],
    allowed_transition_approver_ids: tuple[str, ...],
    allowed_future_transition_operator_ids: tuple[str, ...],
    allowed_transition_kinds: tuple[str, ...],
    allowed_action_kinds: tuple[str, ...],
    allowed_target_resource_ids: tuple[str, ...],
    max_preparation_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
    max_package_expiry_seconds: int = 1800,
    max_approval_delay_seconds: int = 900,
    max_execution_window_seconds: int = 900,
    max_steps: int = 16,
) -> LifecycleTransitionPreparationPolicyV019:
    value = LifecycleTransitionPreparationPolicyV019(
        policy_id=policy_id,
        allowed_transition_preparer_ids=canon(allowed_transition_preparer_ids),
        allowed_transition_preparer_organization_ids=canon(
            allowed_transition_preparer_organization_ids
        ),
        allowed_transition_approver_ids=canon(allowed_transition_approver_ids),
        allowed_future_transition_operator_ids=canon(
            allowed_future_transition_operator_ids
        ),
        allowed_transition_kinds=canon(allowed_transition_kinds),
        allowed_action_kinds=canon(allowed_action_kinds),
        allowed_target_resource_ids=canon(allowed_target_resource_ids),
        max_preparation_delay_seconds=max_preparation_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_package_expiry_seconds=max_package_expiry_seconds,
        max_approval_delay_seconds=max_approval_delay_seconds,
        max_execution_window_seconds=max_execution_window_seconds,
        max_steps=max_steps,
        require_complete_source_recomputation=True,
        require_approved_source_transition_decision=True,
        require_exact_source_artifact_binding=True,
        require_exact_state_and_rule_binding=True,
        require_ordered_bounded_steps=True,
        require_step_chain_continuity=True,
        require_rollback_plan=True,
        require_recovery_plan=True,
        require_monitoring_plan=True,
        require_evidence_capture_plan=True,
        require_resource_reservation=True,
        require_authority_continuity_plan=True,
        require_irreversible_exception_justification=True,
        require_stop_conditions=True,
        require_preparer_source_binding=True,
        require_preparer_prior_actor_separation=True,
        require_preparer_organization_separation=True,
        require_approver_role_separation=True,
        require_future_operator_role_separation=True,
        require_preparer_mandate=True,
        require_preparer_qualification=True,
        require_preparer_identity_confirmation=True,
        require_conflict_disclosure=True,
        require_jurisdiction=True,
        require_preparation_readiness=True,
        require_no_unresolved_anomaly=True,
        require_no_recovery_in_progress=True,
        require_no_institutional_hold=True,
        require_no_emergency_state=True,
        transition_preparation_artifact_only=True,
        lifecycle_state_read_only=True,
        repository_read_only=True,
        policy_digest="",
    )
    value = replace(value, policy_digest=policy_digest(value))
    issues = policy_issues(value)
    if issues:
        raise ValueError(f"lifecycle_transition_preparation_policy_invalid:{issues[0]}")
    return value


def policy_issues(value: LifecycleTransitionPreparationPolicyV019) -> tuple[str, ...]:
    issues: list[str] = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    for name in (
        "allowed_transition_preparer_ids",
        "allowed_transition_preparer_organization_ids",
        "allowed_transition_approver_ids",
        "allowed_future_transition_operator_ids",
        "allowed_transition_kinds",
        "allowed_action_kinds",
        "allowed_target_resource_ids",
    ):
        items = getattr(value, name)
        if not items or items != canon(items):
            issues.append(f"{name}_invalid")
    if min(
        value.max_preparation_delay_seconds,
        value.max_evidence_age_seconds,
        value.max_package_expiry_seconds,
        value.max_approval_delay_seconds,
        value.max_execution_window_seconds,
        value.max_steps,
    ) <= 0:
        issues.append("bound_invalid")
    guards = tuple(
        getattr(value, field.name)
        for field in fields(value)
        if field.name.startswith("require_")
    ) + (
        value.transition_preparation_artifact_only,
        value.lifecycle_state_read_only,
        value.repository_read_only,
    )
    if not all(guards):
        issues.append("required_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)
