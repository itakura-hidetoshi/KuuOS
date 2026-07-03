from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import (
    LifecycleStateV018,
    LifecycleTransitionRuleV018,
    lifecycle_state_digest,
    transition_rule_digest,
)


def make_state(
    *,
    authority_state: str,
    quiescence_state: str,
    terminal_state: str,
    resource_state: str,
    state_revision: int,
) -> LifecycleStateV018:
    value = LifecycleStateV018(
        authority_state=authority_state,
        quiescence_state=quiescence_state,
        terminal_state=terminal_state,
        resource_state=resource_state,
        state_revision=state_revision,
        state_digest="",
    )
    value = replace(value, state_digest=lifecycle_state_digest(value))
    issues = state_issues(value)
    if issues:
        raise ValueError(f"lifecycle_state_invalid:{issues[0]}")
    return value


def state_issues(value: LifecycleStateV018) -> tuple[str, ...]:
    issues: list[str] = []
    if not all(
        (
            value.authority_state,
            value.quiescence_state,
            value.terminal_state,
            value.resource_state,
        )
    ):
        issues.append("state_component_missing")
    if value.state_revision < 0:
        issues.append("state_revision_negative")
    if value.state_digest != lifecycle_state_digest(value):
        issues.append("state_digest_mismatch")
    return tuple(issues)


def make_transition_rule(
    *,
    rule_id: str,
    current_state: LifecycleStateV018,
    transition_kind: str,
    target_state: LifecycleStateV018,
    policy_basis_digest: str,
    reversible_or_exception_required: bool = True,
    authority_continuity_required: bool = True,
    active: bool = True,
) -> LifecycleTransitionRuleV018:
    value = LifecycleTransitionRuleV018(
        rule_id=rule_id,
        current_state_digest=current_state.state_digest,
        transition_kind=transition_kind,
        target_state_digest=target_state.state_digest,
        policy_basis_digest=policy_basis_digest,
        reversible_or_exception_required=reversible_or_exception_required,
        authority_continuity_required=authority_continuity_required,
        active=active,
        rule_digest="",
    )
    value = replace(value, rule_digest=transition_rule_digest(value))
    issues = transition_rule_issues(value)
    if issues:
        raise ValueError(f"lifecycle_transition_rule_invalid:{issues[0]}")
    return value


def transition_rule_issues(
    value: LifecycleTransitionRuleV018,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not all(
        (
            value.rule_id,
            value.current_state_digest,
            value.transition_kind,
            value.target_state_digest,
            value.policy_basis_digest,
        )
    ):
        issues.append("transition_rule_field_missing")
    if value.current_state_digest == value.target_state_digest:
        issues.append("transition_rule_no_state_change")
    if value.rule_digest != transition_rule_digest(value):
        issues.append("transition_rule_digest_mismatch")
    return tuple(issues)


def allowed_transition(
    current_state: LifecycleStateV018,
    transition_kind: str,
    target_state: LifecycleStateV018,
    rule: LifecycleTransitionRuleV018,
) -> bool:
    return all(
        (
            not state_issues(current_state),
            not state_issues(target_state),
            not transition_rule_issues(rule),
            rule.active,
            rule.current_state_digest == current_state.state_digest,
            rule.transition_kind == transition_kind,
            rule.target_state_digest == target_state.state_digest,
            current_state.state_digest != target_state.state_digest,
            target_state.state_revision > current_state.state_revision,
        )
    )
