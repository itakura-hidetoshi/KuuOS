#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re

from runtime.kuuos_repository_checkpoint_stability_types_v1_04 import (
    RepositoryCheckpointNamespaceObservation,
    repository_checkpoint_namespace_observation_digest,
)
from runtime.v104_checkpoint_stability_policy import (
    CHECKPOINT_PREFIX,
    canonical_strings,
)

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def build_repository_checkpoint_namespace_observation(
    observation_id: str,
    observer_id: str,
    creation_receipt,
    creation_result,
    *,
    observed_checkpoint_references: tuple[str, ...],
    conflicting_reference_names: tuple[str, ...] = (),
    sequence_number: int,
    observed_at_epoch_seconds: int,
    reference_store_read: bool = True,
    working_tree_read: bool = False,
    reflog_read: bool = False,
    remote_read: bool = False,
) -> RepositoryCheckpointNamespaceObservation:
    canonical_references = canonical_strings(observed_checkpoint_references)
    canonical_conflicts = canonical_strings(conflicting_reference_names)
    target_occurrences = sum(
        1
        for value in observed_checkpoint_references
        if value == creation_result.checkpoint_reference
    )
    observation = RepositoryCheckpointNamespaceObservation(
        observation_id=observation_id,
        observer_id=observer_id,
        transaction_id=creation_result.transaction_id,
        creation_receipt_digest=creation_receipt.receipt_digest,
        repository_id=creation_result.repository_id,
        git_dir_fingerprint=creation_result.git_dir_fingerprint,
        checkpoint_namespace_prefix=CHECKPOINT_PREFIX,
        checkpoint_reference=creation_result.checkpoint_reference,
        observed_checkpoint_references=canonical_references,
        conflicting_reference_names=canonical_conflicts,
        target_occurrences=target_occurrences,
        reference_store_read=reference_store_read,
        working_tree_read=working_tree_read,
        reflog_read=reflog_read,
        remote_read=remote_read,
        sequence_number=sequence_number,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        observation_digest="",
    )
    observation = replace(
        observation,
        observation_digest=repository_checkpoint_namespace_observation_digest(
            observation
        ),
    )
    issues = repository_checkpoint_namespace_observation_issues(observation)
    if issues:
        raise ValueError(f"checkpoint_namespace_observation_invalid:{issues[0]}")
    return observation


def repository_checkpoint_namespace_observation_issues(
    observation: RepositoryCheckpointNamespaceObservation,
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
        issues.append("checkpoint_namespace_required_field_missing")
    if not _HEX64.fullmatch(observation.creation_receipt_digest):
        issues.append("checkpoint_namespace_receipt_digest_invalid")
    if not _HEX64.fullmatch(observation.git_dir_fingerprint):
        issues.append("checkpoint_namespace_git_dir_invalid")
    if observation.checkpoint_namespace_prefix != CHECKPOINT_PREFIX:
        issues.append("checkpoint_namespace_prefix_invalid")
    if observation.observed_checkpoint_references != canonical_strings(
        observation.observed_checkpoint_references
    ):
        issues.append("checkpoint_namespace_references_not_canonical")
    if observation.conflicting_reference_names != canonical_strings(
        observation.conflicting_reference_names
    ):
        issues.append("checkpoint_namespace_conflicts_not_canonical")
    if observation.target_occurrences < 0:
        issues.append("checkpoint_namespace_occurrences_negative")
    if observation.sequence_number < 0:
        issues.append("checkpoint_namespace_sequence_negative")
    if observation.observed_at_epoch_seconds < 0:
        issues.append("checkpoint_namespace_time_negative")
    if (
        observation.observation_digest
        != repository_checkpoint_namespace_observation_digest(observation)
    ):
        issues.append("checkpoint_namespace_digest_mismatch")
    return tuple(issues)
