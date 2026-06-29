#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.v105_checkpoint_stability_policy_types import VERSION


@dataclass(frozen=True)
class RepositoryCheckpointReachabilityObservation:
    observation_id: str
    observer_id: str
    transaction_id: str
    creation_receipt_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    object_oid: str
    object_present: bool
    object_type: str
    object_database_read: bool
    working_tree_read: bool
    reflog_read: bool
    remote_read: bool
    sequence_number: int
    observed_at_epoch_seconds: int
    observation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_reachability_observation_digest(
    observation: RepositoryCheckpointReachabilityObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("observation_digest", None)
    return canonical_digest(payload)
