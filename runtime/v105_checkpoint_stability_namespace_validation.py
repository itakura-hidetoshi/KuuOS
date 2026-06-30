#!/usr/bin/env python3
from __future__ import annotations

import re

from runtime.v105_checkpoint_stability_namespace_types import (
    RepositoryCheckpointNamespaceObservation,
    repository_checkpoint_namespace_observation_digest,
)
from runtime.v105_checkpoint_stability_policy import CHECKPOINT_PREFIX, canonical_strings

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


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
    if observation.sequence_number < 0 or observation.observed_at_epoch_seconds < 0:
        issues.append("checkpoint_namespace_order_invalid")
    if observation.observation_digest != repository_checkpoint_namespace_observation_digest(observation):
        issues.append("checkpoint_namespace_digest_mismatch")
    return tuple(issues)
