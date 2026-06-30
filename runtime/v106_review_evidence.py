#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re

from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import (
    RepositoryCheckpointReviewObservation,
    RepositoryCheckpointReviewPolicy,
    repository_checkpoint_review_observation_digest,
    repository_checkpoint_review_policy_digest,
)

CHECKPOINT_PREFIX = "refs/kuuos/checkpoints/"
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_checkpoint_review_policy(
    policy_id: str,
    *,
    allowed_repository_ids: tuple[str, ...],
    allowed_checkpoint_references: tuple[str, ...],
    authorized_observer_ids: tuple[str, ...],
    max_observation_age_seconds: int,
) -> RepositoryCheckpointReviewPolicy:
    policy = RepositoryCheckpointReviewPolicy(
        policy_id=policy_id,
        allowed_repository_ids=_canonical(allowed_repository_ids),
        allowed_checkpoint_references=_canonical(allowed_checkpoint_references),
        authorized_observer_ids=_canonical(authorized_observer_ids),
        max_observation_age_seconds=max_observation_age_seconds,
        require_direct_reference=True,
        require_reference_store_source=True,
        require_object_database_source=True,
        read_only=True,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_review_policy_digest(policy),
    )
    issues = repository_checkpoint_review_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_review_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_review_policy_issues(
    policy: RepositoryCheckpointReviewPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("review_policy_id_missing")
    for values, name in (
        (policy.allowed_repository_ids, "allowed_repository_ids"),
        (policy.allowed_checkpoint_references, "allowed_checkpoint_references"),
        (policy.authorized_observer_ids, "authorized_observer_ids"),
    ):
        if not values:
            issues.append(f"{name}_empty")
        if values != _canonical(values):
            issues.append(f"{name}_not_canonical")
        if any(not value for value in values):
            issues.append(f"{name}_contains_empty")
    if any(
        not reference.startswith(CHECKPOINT_PREFIX)
        for reference in policy.allowed_checkpoint_references
    ):
        issues.append("review_policy_reference_outside_namespace")
    if policy.max_observation_age_seconds <= 0:
        issues.append("review_policy_age_invalid")
    if not all(
        (
            policy.require_direct_reference,
            policy.require_reference_store_source,
            policy.require_object_database_source,
            policy.read_only,
        )
    ):
        issues.append("review_policy_safeguard_disabled")
    if policy.policy_digest != repository_checkpoint_review_policy_digest(policy):
        issues.append("review_policy_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_review_observation(
    observation_id: str,
    observer_id: str,
    stability_certificate,
    *,
    reference_present: bool,
    observed_oid: str,
    rechecked_oid: str,
    target_object_present: bool,
    target_object_type: str,
    observed_at_epoch_seconds: int,
    rechecked_at_epoch_seconds: int,
    direct: bool = True,
    symbolic: bool = False,
    reference_store_read: bool = True,
    object_database_read: bool = True,
    working_tree_read: bool = False,
    reflog_read: bool = False,
    remote_read: bool = False,
) -> RepositoryCheckpointReviewObservation:
    observation = RepositoryCheckpointReviewObservation(
        observation_id=observation_id,
        observer_id=observer_id,
        stability_certificate_digest=stability_certificate.certificate_digest,
        repository_id=stability_certificate.repository_id,
        git_dir_fingerprint=stability_certificate.git_dir_fingerprint,
        checkpoint_reference=stability_certificate.checkpoint_reference,
        expected_oid=stability_certificate.expected_oid,
        reference_present=reference_present,
        observed_oid=observed_oid,
        rechecked_oid=rechecked_oid,
        target_object_present=target_object_present,
        target_object_type=target_object_type,
        direct=direct,
        symbolic=symbolic,
        reference_store_read=reference_store_read,
        object_database_read=object_database_read,
        working_tree_read=working_tree_read,
        reflog_read=reflog_read,
        remote_read=remote_read,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        rechecked_at_epoch_seconds=rechecked_at_epoch_seconds,
        observation_digest="",
    )
    observation = replace(
        observation,
        observation_digest=repository_checkpoint_review_observation_digest(
            observation
        ),
    )
    issues = repository_checkpoint_review_observation_issues(observation)
    if issues:
        raise ValueError(f"checkpoint_review_observation_invalid:{issues[0]}")
    return observation


def repository_checkpoint_review_observation_issues(
    observation: RepositoryCheckpointReviewObservation,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        observation.observation_id,
        observation.observer_id,
        observation.stability_certificate_digest,
        observation.repository_id,
        observation.git_dir_fingerprint,
        observation.checkpoint_reference,
        observation.target_object_type,
    )
    if any(not value for value in required):
        issues.append("review_observation_required_field_missing")
    if not _HEX64.fullmatch(observation.stability_certificate_digest):
        issues.append("review_observation_stability_digest_invalid")
    if not _HEX64.fullmatch(observation.git_dir_fingerprint):
        issues.append("review_observation_git_dir_invalid")
    for value, name in (
        (observation.expected_oid, "expected_oid"),
        (observation.observed_oid, "observed_oid"),
        (observation.rechecked_oid, "rechecked_oid"),
    ):
        if not _HEX40.fullmatch(value):
            issues.append(f"review_observation_{name}_invalid")
    if not observation.checkpoint_reference.startswith(CHECKPOINT_PREFIX):
        issues.append("review_observation_reference_outside_namespace")
    if observation.observed_at_epoch_seconds < 0:
        issues.append("review_observation_time_negative")
    if observation.rechecked_at_epoch_seconds < observation.observed_at_epoch_seconds:
        issues.append("review_observation_recheck_before_observation")
    if (
        observation.observation_digest
        != repository_checkpoint_review_observation_digest(observation)
    ):
        issues.append("review_observation_digest_mismatch")
    return tuple(issues)
