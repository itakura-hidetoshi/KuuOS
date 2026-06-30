#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_candidate_revalidation_types_v1_11 import (
    RepositoryCheckpointCandidateRevalidationPolicy,
    repository_checkpoint_candidate_revalidation_policy_digest,
)


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_checkpoint_candidate_revalidation_policy(
    policy_id: str,
    *,
    allowed_repository_ids: tuple[str, ...],
    allowed_checkpoint_references: tuple[str, ...],
    max_candidate_age_seconds: int,
) -> RepositoryCheckpointCandidateRevalidationPolicy:
    policy = RepositoryCheckpointCandidateRevalidationPolicy(
        policy_id=policy_id,
        allowed_repository_ids=_canonical(allowed_repository_ids),
        allowed_checkpoint_references=_canonical(allowed_checkpoint_references),
        max_candidate_age_seconds=max_candidate_age_seconds,
        require_complete_v109_revalidation=True,
        require_exact_repository_binding=True,
        read_only=True,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_candidate_revalidation_policy_digest(
            policy
        ),
    )
    issues = repository_checkpoint_candidate_revalidation_policy_issues(policy)
    if issues:
        raise ValueError(
            f"checkpoint_candidate_revalidation_policy_invalid:{issues[0]}"
        )
    return policy


def repository_checkpoint_candidate_revalidation_policy_issues(
    policy: RepositoryCheckpointCandidateRevalidationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_candidate_revalidation_policy_id_missing")
    if policy.allowed_repository_ids != _canonical(policy.allowed_repository_ids):
        issues.append(
            "checkpoint_candidate_revalidation_repository_ids_not_canonical"
        )
    if not policy.allowed_repository_ids:
        issues.append("checkpoint_candidate_revalidation_repository_ids_empty")
    if policy.allowed_checkpoint_references != _canonical(
        policy.allowed_checkpoint_references
    ):
        issues.append(
            "checkpoint_candidate_revalidation_references_not_canonical"
        )
    if not policy.allowed_checkpoint_references:
        issues.append("checkpoint_candidate_revalidation_references_empty")
    if policy.max_candidate_age_seconds <= 0:
        issues.append("checkpoint_candidate_revalidation_age_bound_invalid")
    required = (
        policy.require_complete_v109_revalidation,
        policy.require_exact_repository_binding,
        policy.read_only,
    )
    if not all(required):
        issues.append("checkpoint_candidate_revalidation_guard_disabled")
    if (
        policy.policy_digest
        != repository_checkpoint_candidate_revalidation_policy_digest(policy)
    ):
        issues.append(
            "checkpoint_candidate_revalidation_policy_digest_mismatch"
        )
    return tuple(issues)
