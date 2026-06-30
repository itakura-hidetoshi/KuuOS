#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_restore_authorization_types_v1_06 import (
    RepositoryCheckpointRestorePolicy,
    repository_checkpoint_restore_policy_digest,
)

CHECKPOINT_PREFIX = "refs/kuuos/checkpoints/"


def canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_checkpoint_restore_policy(
    policy_id: str,
    *,
    allowed_repository_ids: tuple[str, ...],
    allowed_checkpoint_references: tuple[str, ...],
    authorized_observer_ids: tuple[str, ...],
    authorized_approver_ids: tuple[str, ...],
    authorized_approver_classes: tuple[str, ...],
    authorized_executor_ids: tuple[str, ...],
    authorized_nonce_authority_ids: tuple[str, ...],
    max_authorization_lifetime_seconds: int,
    max_observation_age_seconds: int,
    max_approval_age_seconds: int,
    max_nonce_status_age_seconds: int,
) -> RepositoryCheckpointRestorePolicy:
    policy = RepositoryCheckpointRestorePolicy(
        policy_id=policy_id,
        allowed_repository_ids=canonical_strings(allowed_repository_ids),
        allowed_checkpoint_references=canonical_strings(allowed_checkpoint_references),
        authorized_observer_ids=canonical_strings(authorized_observer_ids),
        authorized_approver_ids=canonical_strings(authorized_approver_ids),
        authorized_approver_classes=canonical_strings(authorized_approver_classes),
        authorized_executor_ids=canonical_strings(authorized_executor_ids),
        authorized_nonce_authority_ids=canonical_strings(authorized_nonce_authority_ids),
        max_authorization_lifetime_seconds=max_authorization_lifetime_seconds,
        max_observation_age_seconds=max_observation_age_seconds,
        max_approval_age_seconds=max_approval_age_seconds,
        max_nonce_status_age_seconds=max_nonce_status_age_seconds,
        require_human_approval=True,
        require_exact_compare_and_swap=True,
        require_direct_checkpoint_reference=True,
        require_reference_store_source=True,
        require_object_database_source=True,
        allow_lost_reference_restore=True,
        allow_substituted_reference_restore=True,
        allow_generic_overwrite=False,
        allow_reference_delete=False,
        allow_force_update=False,
        allow_branch_update=False,
        allow_tag_update=False,
        allow_remote_reference_update=False,
        allow_push=False,
        policy_digest="",
    )
    policy = replace(policy, policy_digest=repository_checkpoint_restore_policy_digest(policy))
    issues = repository_checkpoint_restore_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_restore_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_restore_policy_issues(
    policy: RepositoryCheckpointRestorePolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("restore_policy_id_missing")
    for values, name in (
        (policy.allowed_repository_ids, "allowed_repository_ids"),
        (policy.allowed_checkpoint_references, "allowed_checkpoint_references"),
        (policy.authorized_observer_ids, "authorized_observer_ids"),
        (policy.authorized_approver_ids, "authorized_approver_ids"),
        (policy.authorized_approver_classes, "authorized_approver_classes"),
        (policy.authorized_executor_ids, "authorized_executor_ids"),
        (policy.authorized_nonce_authority_ids, "authorized_nonce_authority_ids"),
    ):
        if not values:
            issues.append(f"{name}_empty")
        if values != canonical_strings(values):
            issues.append(f"{name}_not_canonical")
        if any(not value for value in values):
            issues.append(f"{name}_contains_empty")
    if any(not ref.startswith(CHECKPOINT_PREFIX) for ref in policy.allowed_checkpoint_references):
        issues.append("restore_policy_reference_outside_checkpoint_namespace")
    if any(value <= 0 for value in (
        policy.max_authorization_lifetime_seconds,
        policy.max_observation_age_seconds,
        policy.max_approval_age_seconds,
        policy.max_nonce_status_age_seconds,
    )):
        issues.append("restore_policy_duration_invalid")
    if not all((
        policy.require_human_approval,
        policy.require_exact_compare_and_swap,
        policy.require_direct_checkpoint_reference,
        policy.require_reference_store_source,
        policy.require_object_database_source,
        policy.allow_lost_reference_restore,
        policy.allow_substituted_reference_restore,
    )):
        issues.append("restore_policy_required_safeguard_disabled")
    if any((
        policy.allow_generic_overwrite,
        policy.allow_reference_delete,
        policy.allow_force_update,
        policy.allow_branch_update,
        policy.allow_tag_update,
        policy.allow_remote_reference_update,
        policy.allow_push,
    )):
        issues.append("restore_policy_forbidden_authority_enabled")
    if policy.policy_digest != repository_checkpoint_restore_policy_digest(policy):
        issues.append("restore_policy_digest_mismatch")
    return tuple(issues)
