#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_stability_v1_05"
STABILITY_CONFIRMED = "REPOSITORY_CHECKPOINT_STABILITY_CONFIRMED"
STABILITY_REJECTED = "REPOSITORY_CHECKPOINT_STABILITY_REJECTED"
FAILURE_NONE = "NONE"
FAILURE_EVIDENCE_INVALID = "EVIDENCE_INVALID"
FAILURE_CHECKPOINT_LOST = "CHECKPOINT_LOST"
FAILURE_CHECKPOINT_SUBSTITUTED = "CHECKPOINT_SUBSTITUTED"
FAILURE_NAME_CONFLICT = "CHECKPOINT_NAME_CONFLICT"
FAILURE_UNREACHABLE = "CHECKPOINT_OBJECT_UNREACHABLE"
FAILURE_UNSTABLE_WINDOW = "CHECKPOINT_UNSTABLE_WINDOW"
ZERO_OID = "0" * 40


@dataclass(frozen=True)
class RepositoryCheckpointStabilityPolicy:
    policy_id: str
    authorized_observer_ids: tuple[str, ...]
    min_stability_interval_seconds: int
    max_stability_interval_seconds: int
    max_observation_age_seconds: int
    max_reachability_age_seconds: int
    checkpoint_namespace_prefix: str
    require_direct_checkpoint_reference: bool
    require_reference_store_source: bool
    require_object_database_source: bool
    require_unique_checkpoint_name: bool
    immutable_by_default: bool
    allow_checkpoint_overwrite: bool
    allow_checkpoint_delete: bool
    allow_force_update: bool
    allow_branch_update: bool
    allow_tag_update: bool
    allow_remote_reference_update: bool
    allow_push: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["authorized_observer_ids"] = list(self.authorized_observer_ids)
        return payload


def repository_checkpoint_stability_policy_digest(
    policy: RepositoryCheckpointStabilityPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)
