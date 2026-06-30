#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.v105_checkpoint_stability_policy_types import VERSION


@dataclass(frozen=True)
class RepositoryCheckpointNamespaceObservation:
    observation_id: str
    observer_id: str
    transaction_id: str
    creation_receipt_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_namespace_prefix: str
    checkpoint_reference: str
    observed_checkpoint_references: tuple[str, ...]
    conflicting_reference_names: tuple[str, ...]
    target_occurrences: int
    reference_store_read: bool
    working_tree_read: bool
    reflog_read: bool
    remote_read: bool
    sequence_number: int
    observed_at_epoch_seconds: int
    observation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["observed_checkpoint_references"] = list(
            self.observed_checkpoint_references
        )
        payload["conflicting_reference_names"] = list(
            self.conflicting_reference_names
        )
        return payload


def repository_checkpoint_namespace_observation_digest(
    observation: RepositoryCheckpointNamespaceObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("observation_digest", None)
    return canonical_digest(payload)
