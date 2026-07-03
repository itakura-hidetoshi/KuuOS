from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_transition_preparation_step_v0_19 import step_issues
from runtime.kuuos_lifecycle_transition_preparation_types_v0_19 import (
    LifecycleTransitionPackageV019,
    LifecycleTransitionStepV019,
    package_digest,
)


def make_package(
    *,
    package_id: str,
    source_transition_decision_id: str,
    transition_kind: str,
    expected_current_lifecycle_state_digest: str,
    proposed_target_lifecycle_state_digest: str,
    transition_rule_digest: str,
    steps: tuple[LifecycleTransitionStepV019, ...],
    rollback_plan_digest: str,
    recovery_plan_digest: str,
    monitoring_plan_digest: str,
    evidence_capture_plan_digest: str,
    resource_reservation_digest: str,
    authority_continuity_plan_digest: str,
    irreversible_exception_digest: str,
    aggregate_stop_conditions_digest: str,
    execution_window_start_epoch_seconds: int,
    execution_window_end_epoch_seconds: int,
) -> LifecycleTransitionPackageV019:
    value = LifecycleTransitionPackageV019(
        package_id=package_id,
        source_transition_decision_id=source_transition_decision_id,
        transition_kind=transition_kind,
        expected_current_lifecycle_state_digest=expected_current_lifecycle_state_digest,
        proposed_target_lifecycle_state_digest=proposed_target_lifecycle_state_digest,
        transition_rule_digest=transition_rule_digest,
        steps=steps,
        rollback_plan_digest=rollback_plan_digest,
        recovery_plan_digest=recovery_plan_digest,
        monitoring_plan_digest=monitoring_plan_digest,
        evidence_capture_plan_digest=evidence_capture_plan_digest,
        resource_reservation_digest=resource_reservation_digest,
        authority_continuity_plan_digest=authority_continuity_plan_digest,
        irreversible_exception_digest=irreversible_exception_digest,
        aggregate_stop_conditions_digest=aggregate_stop_conditions_digest,
        execution_window_start_epoch_seconds=execution_window_start_epoch_seconds,
        execution_window_end_epoch_seconds=execution_window_end_epoch_seconds,
        package_digest="",
    )
    value = replace(value, package_digest=package_digest(value))
    issues = package_issues(value)
    if issues:
        raise ValueError(f"lifecycle_transition_package_invalid:{issues[0]}")
    return value


def package_issues(value: LifecycleTransitionPackageV019) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        value.package_id,
        value.source_transition_decision_id,
        value.transition_kind,
        value.expected_current_lifecycle_state_digest,
        value.proposed_target_lifecycle_state_digest,
        value.transition_rule_digest,
        value.rollback_plan_digest,
        value.recovery_plan_digest,
        value.monitoring_plan_digest,
        value.evidence_capture_plan_digest,
        value.resource_reservation_digest,
        value.authority_continuity_plan_digest,
        value.aggregate_stop_conditions_digest,
    )
    if not all(required):
        issues.append("package_required_field_missing")
    if not value.steps:
        issues.append("package_steps_missing")
    if any(step_issues(step) for step in value.steps):
        issues.append("package_step_invalid")
    sequences = tuple(step.sequence_number for step in value.steps)
    if sequences != tuple(range(1, len(value.steps) + 1)):
        issues.append("package_step_order_invalid")
    if len({step.step_id for step in value.steps}) != len(value.steps):
        issues.append("package_step_id_duplicate")
    if value.steps:
        if value.steps[0].expected_pre_state_digest != value.expected_current_lifecycle_state_digest:
            issues.append("package_initial_state_binding_invalid")
        if value.steps[-1].proposed_post_state_digest != value.proposed_target_lifecycle_state_digest:
            issues.append("package_target_state_binding_invalid")
        for left, right in zip(value.steps, value.steps[1:]):
            if left.proposed_post_state_digest != right.expected_pre_state_digest:
                issues.append("package_step_chain_discontinuous")
                break
    if any(not step.reversible for step in value.steps) and not value.irreversible_exception_digest:
        issues.append("package_irreversible_exception_missing")
    if value.execution_window_start_epoch_seconds < 0 or value.execution_window_end_epoch_seconds <= value.execution_window_start_epoch_seconds:
        issues.append("package_execution_window_invalid")
    if value.package_digest != package_digest(value):
        issues.append("package_digest_mismatch")
    return tuple(issues)
