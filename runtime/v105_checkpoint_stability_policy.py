#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.v105_checkpoint_stability_policy_types import (
    RepositoryCheckpointStabilityPolicy,
    repository_checkpoint_stability_policy_digest,
)

CHECKPOINT_PREFIX = "refs/kuuos/checkpoints/"


def canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_checkpoint_stability_policy(
    policy_id: str,
    *,
    authorized_observer_ids: tuple[str, ...],
    min_stability_interval_seconds: int,
    max_stability_interval_seconds: int,
    max_observation_age_seconds: int,
    max_reachability_age_seconds: int,
) -> RepositoryCheckpointStabilityPolicy:
    policy = RepositoryCheckpointStabilityPolicy(
        policy_id=policy_id,
        authorized_observer_ids=canonical_strings(authorized_observer_ids),
        min_stability_interval_seconds=min_stability_interval_seconds,
        max_stability_interval_seconds=max_stability_interval_seconds,
        max_observation_age_seconds=max_observation_age_seconds,
        max_reachability_age_seconds=max_reachability_age_seconds,
        checkpoint_namespace_prefix=CHECKPOINT_PREFIX,
        require_direct_checkpoint_reference=True,
        require_reference_store_source=True,
        require_object_database_source=True,
        require_unique_checkpoint_name=True,
        immutable_by_default=True,
        allow_checkpoint_overwrite=False,
        allow_checkpoint_delete=False,
        allow_force_update=False,
        allow_branch_update=False,
        allow_tag_update=False,
        allow_remote_reference_update=False,
        allow_push=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_stability_policy_digest(policy),
    )
    issues = repository_checkpoint_stability_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_stability_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_stability_policy_issues(
    policy: RepositoryCheckpointStabilityPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id or not policy.authorized_observer_ids:
        issues.append("checkpoint_stability_policy_required_field_missing")
    if policy.authorized_observer_ids != canonical_strings(policy.authorized_observer_ids):
        issues.append("checkpoint_stability_observers_invalid")
    if policy.min_stability_interval_seconds <= 0:
        issues.append("checkpoint_stability_min_interval_invalid")
    if policy.max_stability_interval_seconds < policy.min_stability_interval_seconds:
        issues.append("checkpoint_stability_interval_bounds_invalid")
    if min(policy.max_observation_age_seconds, policy.max_reachability_age_seconds) <= 0:
        issues.append("checkpoint_stability_age_bound_invalid")
    return tuple(issues + _policy_boundary_issues(policy))


def _policy_boundary_issues(policy: RepositoryCheckpointStabilityPolicy) -> list[str]:
    issues: list[str] = []
    required = (
        policy.checkpoint_namespace_prefix == CHECKPOINT_PREFIX,
        policy.require_direct_checkpoint_reference,
        policy.require_reference_store_source,
        policy.require_object_database_source,
        policy.require_unique_checkpoint_name,
        policy.immutable_by_default,
    )
    if not all(required):
        issues.append("checkpoint_stability_safeguard_disabled")
    forbidden = (
        policy.allow_checkpoint_overwrite,
        policy.allow_checkpoint_delete,
        policy.allow_force_update,
        policy.allow_branch_update,
        policy.allow_tag_update,
        policy.allow_remote_reference_update,
        policy.allow_push,
    )
    if any(forbidden):
        issues.append("checkpoint_stability_mutation_authority_forbidden")
    if policy.policy_digest != repository_checkpoint_stability_policy_digest(policy):
        issues.append("checkpoint_stability_policy_digest_mismatch")
    return issues
