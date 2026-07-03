from __future__ import annotations

from dataclasses import fields, replace

from runtime.kuuos_lifecycle_request_policy_v0_10 import canon
from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import (
    LifecycleTransitionDecisionPolicyV018,
    policy_digest,
)


def make_policy(
    policy_id: str,
    *,
    allowed_transition_decision_maker_ids: tuple[str, ...],
    allowed_transition_decision_maker_organization_ids: tuple[str, ...],
    allowed_transition_preparer_ids: tuple[str, ...],
    allowed_transition_kinds: tuple[str, ...],
    max_decision_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
    max_decision_expiry_seconds: int = 1800,
    max_preparation_delay_seconds: int = 900,
) -> LifecycleTransitionDecisionPolicyV018:
    value = LifecycleTransitionDecisionPolicyV018(
        policy_id=policy_id,
        allowed_transition_decision_maker_ids=canon(
            allowed_transition_decision_maker_ids
        ),
        allowed_transition_decision_maker_organization_ids=canon(
            allowed_transition_decision_maker_organization_ids
        ),
        allowed_transition_preparer_ids=canon(allowed_transition_preparer_ids),
        allowed_transition_kinds=canon(allowed_transition_kinds),
        max_decision_delay_seconds=max_decision_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_decision_expiry_seconds=max_decision_expiry_seconds,
        max_preparation_delay_seconds=max_preparation_delay_seconds,
        require_complete_source_recomputation=True,
        require_clear_source_transition_review=True,
        require_exact_source_artifact_binding=True,
        require_exact_state_snapshot_binding=True,
        require_allowed_transition_relation=True,
        require_current_state_not_stale=True,
        require_decision_maker_source_reviewer_separation=True,
        require_decision_maker_prior_actor_separation=True,
        require_decision_maker_preparer_separation=True,
        require_decision_maker_organization_separation=True,
        require_decision_maker_mandate=True,
        require_decision_maker_qualification=True,
        require_decision_maker_identity_confirmation=True,
        require_conflict_disclosure=True,
        require_jurisdiction=True,
        require_decision_readiness=True,
        require_decision_rationale=True,
        require_denial_route=True,
        require_appeal_route=True,
        require_dissent_route=True,
        require_minority_opinion_record=True,
        require_no_unresolved_anomaly=True,
        require_no_recovery=True,
        require_no_institutional_hold=True,
        require_no_emergency_state=True,
        transition_decision_artifact_only=True,
        lifecycle_state_read_only=True,
        repository_read_only=True,
        policy_digest="",
    )
    value = replace(value, policy_digest=policy_digest(value))
    issues = policy_issues(value)
    if issues:
        raise ValueError(f"lifecycle_transition_decision_policy_invalid:{issues[0]}")
    return value


def policy_issues(value: LifecycleTransitionDecisionPolicyV018) -> tuple[str, ...]:
    issues: list[str] = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    for name in (
        "allowed_transition_decision_maker_ids",
        "allowed_transition_decision_maker_organization_ids",
        "allowed_transition_preparer_ids",
        "allowed_transition_kinds",
    ):
        items = getattr(value, name)
        if not items or items != canon(items):
            issues.append(f"{name}_invalid")
    if min(
        value.max_decision_delay_seconds,
        value.max_evidence_age_seconds,
        value.max_decision_expiry_seconds,
        value.max_preparation_delay_seconds,
    ) <= 0:
        issues.append("bound_invalid")
    guards = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name.startswith("require_")
    ) + (
        value.transition_decision_artifact_only,
        value.lifecycle_state_read_only,
        value.repository_read_only,
    )
    if not all(guards):
        issues.append("required_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)
