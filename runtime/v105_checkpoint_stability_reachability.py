#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.v105_checkpoint_stability_reachability_types import (
    RepositoryCheckpointReachabilityObservation,
    repository_checkpoint_reachability_observation_digest,
)
from runtime.v105_checkpoint_stability_reachability_validation import (
    repository_checkpoint_reachability_observation_issues,
)


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
        observation_digest=repository_checkpoint_reachability_observation_digest(observation),
    )
    issues = repository_checkpoint_reachability_observation_issues(observation)
    if issues:
        raise ValueError(f"checkpoint_reachability_observation_invalid:{issues[0]}")
    return observation
