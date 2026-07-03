from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_transition_preparation_types_v0_19 import (
    LifecycleTransitionStepV019,
    step_digest,
)


def make_step(
    *,
    step_id: str,
    sequence_number: int,
    action_kind: str,
    target_resource_id: str,
    expected_pre_state_digest: str,
    proposed_post_state_digest: str,
    reversible: bool,
    rollback_step_id: str,
    evidence_capture_digest: str,
    stop_condition_digest: str,
) -> LifecycleTransitionStepV019:
    value = LifecycleTransitionStepV019(
        step_id=step_id,
        sequence_number=sequence_number,
        action_kind=action_kind,
        target_resource_id=target_resource_id,
        expected_pre_state_digest=expected_pre_state_digest,
        proposed_post_state_digest=proposed_post_state_digest,
        reversible=reversible,
        rollback_step_id=rollback_step_id,
        evidence_capture_digest=evidence_capture_digest,
        stop_condition_digest=stop_condition_digest,
        step_digest="",
    )
    value = replace(value, step_digest=step_digest(value))
    issues = step_issues(value)
    if issues:
        raise ValueError(f"lifecycle_transition_step_invalid:{issues[0]}")
    return value


def step_issues(value: LifecycleTransitionStepV019) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        value.step_id,
        value.action_kind,
        value.target_resource_id,
        value.expected_pre_state_digest,
        value.proposed_post_state_digest,
        value.evidence_capture_digest,
        value.stop_condition_digest,
    )
    if not all(required):
        issues.append("step_required_field_missing")
    if value.sequence_number <= 0:
        issues.append("step_sequence_invalid")
    if value.expected_pre_state_digest == value.proposed_post_state_digest:
        issues.append("step_has_no_state_change")
    if value.reversible and not value.rollback_step_id:
        issues.append("reversible_step_rollback_missing")
    if value.step_digest != step_digest(value):
        issues.append("step_digest_mismatch")
    return tuple(issues)
