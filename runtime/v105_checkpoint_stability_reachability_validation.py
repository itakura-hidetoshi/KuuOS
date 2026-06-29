#!/usr/bin/env python3
from __future__ import annotations

import re

from runtime.v105_checkpoint_stability_reachability_types import (
    RepositoryCheckpointReachabilityObservation,
    repository_checkpoint_reachability_observation_digest,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


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
    if observation.sequence_number < 0 or observation.observed_at_epoch_seconds < 0:
        issues.append("checkpoint_reachability_order_invalid")
    if observation.observation_digest != repository_checkpoint_reachability_observation_digest(observation):
        issues.append("checkpoint_reachability_digest_mismatch")
    return tuple(issues)
