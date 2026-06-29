#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re

from runtime.kuuos_repository_checkpoint_stability_types_v1_04 import (
    RepositoryCheckpointReachabilityObservation,
    RepositoryDelayedCheckpointObservation,
    repository_checkpoint_reachability_observation_digest,
    repository_delayed_checkpoint_observation_digest,
)
from runtime.v104_checkpoint_stability_policy import CHECKPOINT_PREFIX

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def build_repository_delayed_checkpoint_observation(
    observation_id: str,
    observer_id: str,
    creation_receipt,
    creation_result,
    *,
    observed_oid: str,
    reference_present: bool,
    sequence_number: int,
    observed_at_epoch_seconds: int,
    direct: bool = True,
    symbolic: bool = False,
    reference_store_read: bool = True,
    object_database_read: bool = True,
    working_tree_read: bool = False,
    reflog_read: bool = False,
    remote_read: bool = False,
    overwrite_observed: bool = False,
    force_update_observed: bool = False,
) -> RepositoryDelayedCheckpointObservation:
    observation = RepositoryDelayedCheckpointObservation(
        observation_id=observation_id,
        observer_id=observer_id,
        transaction_id=creation_result.transaction_id,
        creation_receipt_digest=creation_receipt.receipt_digest,
        repository_id=creation_result.repository_id,
        git_dir_fingerprint=creation_result.git_dir_fingerprint,
        checkpoint_reference=creation_result.checkpoint_reference,
        expected_oid=creation_result.proposed_new_oid,
        observed_oid=observed_oid,
        reference_present=reference_present,
        direct=direct,
        symbolic=symbolic,
        reference_store_read=reference_store_read,
        object_database_read=object_database_read,
        working_tree_read=working_tree_read,
        reflog_read=reflog_read,
        remote_read=remote_read,
        overwrite_observed=overwrite_observed,
        force_update_observed=force_update_observed,
        sequence_number=sequence_number,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        observation_digest="",
    )
    observation = replace(
        observation,
        observation_digest=repository_delayed_checkpoint_observation_digest(
            observation
        ),
    )
    issues = repository_delayed_checkpoint_observation_issues(observation)
    if issues:
        raise ValueError(f"delayed_checkpoint_observation_invalid:{issues[0]}")
    return observation


def repository_delayed_checkpoint_observation_issues(
    observation: RepositoryDelayedCheckpointObservation,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        observation.observation_id,
        observation.observer_id,
        observation.transaction_id,
        observation.creation_receipt_digest,
        observation.repository_id,
        observation.checkpoint_reference,
    )
    if any(not value for value in required):
        issues.append("delayed_checkpoint_required_field_missing")
    if not _HEX64.fullmatch(observation.creation_receipt_digest):
        issues.append("delayed_checkpoint_receipt_digest_invalid")
    if not _HEX64.fullmatch(observation.git_dir_fingerprint):
        issues.append("delayed_checkpoint_git_dir_invalid")
    if not _HEX40.fullmatch(observation.expected_oid):
        issues.append("delayed_checkpoint_expected_oid_invalid")
    if not _HEX40.fullmatch(observation.observed_oid):
        issues.append("delayed_checkpoint_observed_oid_invalid")
    if not observation.checkpoint_reference.startswith(CHECKPOINT_PREFIX):
        issues.append("delayed_checkpoint_reference_invalid")
    if observation.sequence_number < 0:
        issues.append("delayed_checkpoint_sequence_negative")
    if observation.observed_at_epoch_seconds < 0:
        issues.append("delayed_checkpoint_time_negative")
    if (
        observation.observation_digest
        != repository_delayed_checkpoint_observation_digest(observation)
    ):
        issues.append("delayed_checkpoint_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_reachability_observation(
    observation_id: str,
    observer_id: str,
    creation_receipt,
    creation_result,
    *,
    object_present: bool,
    object_type: str,
    sequence_number: int,
    observed_at_epoch_seconds: int,
    object_database_read: bool = True,
    working_tree_read: bool = False,
    reflog_read: bool = False,
    remote_read: bool = False,
) -> RepositoryCheckpointReachabilityObservation:
    observation = RepositoryCheckpointReachabilityObservation(
        observation_id=observation_id,
        observer_id=observer_id,
        transaction_id=creation_result.transaction_id,
        creation_receipt_digest=creation_receipt.receipt_digest,
        repository_id=creation_result.repository_id,
        git_dir_fingerprint=creation_result.git_dir_fingerprint,
        checkpoint_reference=creation_result.checkpoint_reference,
        object_oid=creation_result.proposed_new_oid,
        object_present=object_present,
        object_type=object_type,
        object_database_read=object_database_read,
        working_tree_read=working_tree_read,
        reflog_read=reflog_read,
        remote_read=remote_read,
        sequence_number=sequence_number,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        observation_digest="",
    )
    observation = replace(
        observation,
        observation_digest=repository_checkpoint_reachability_observation_digest(
            observation
        ),
    )
    issues = repository_checkpoint_reachability_observation_issues(observation)
    if issues:
        raise ValueError(f"checkpoint_reachability_observation_invalid:{issues[0]}")
    return observation


def repository_checkpoint_reachability_observation_issues(
    observation: RepositoryCheckpointReachabilityObservation,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        observation.observation_id,
        observation.observer_id,
        observation.transaction_id,
        observation.creation_receipt_digest,
        observation.repository_id,
        observation.checkpoint_reference,
        observation.object_type,
    )
    if any(not value for value in required):
        issues.append("checkpoint_reachability_required_field_missing")
    if not _HEX64.fullmatch(observation.creation_receipt_digest):
        issues.append("checkpoint_reachability_receipt_digest_invalid")
    if not _HEX64.fullmatch(observation.git_dir_fingerprint):
        issues.append("checkpoint_reachability_git_dir_invalid")
    if not _HEX40.fullmatch(observation.object_oid):
        issues.append("checkpoint_reachability_oid_invalid")
    if observation.sequence_number < 0:
        issues.append("checkpoint_reachability_sequence_negative")
    if observation.observed_at_epoch_seconds < 0:
        issues.append("checkpoint_reachability_time_negative")
    if (
        observation.observation_digest
        != repository_checkpoint_reachability_observation_digest(observation)
    ):
        issues.append("checkpoint_reachability_digest_mismatch")
    return tuple(issues)
