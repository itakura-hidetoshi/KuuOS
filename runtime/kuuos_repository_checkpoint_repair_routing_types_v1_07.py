#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_repair_routing_v1_07"
ROUTE_NOOP = "CHECKPOINT_REPAIR_ROUTE_NOOP"
ROUTE_AUTOMATIC = "CHECKPOINT_REPAIR_ROUTE_AUTOMATIC"
ROUTE_REJECTED = "CHECKPOINT_REPAIR_ROUTE_REJECTED"
PRIMITIVE_NONE = "NONE"
PRIMITIVE_ATOMIC_CHECKPOINT_CREATION_V1_02 = (
    "ATOMIC_CHECKPOINT_CREATION_V1_02"
)
PRIMITIVE_ATOMIC_REFERENCE_UPDATE_V0_97 = "ATOMIC_REFERENCE_UPDATE_V0_97"


@dataclass(frozen=True)
class RepositoryCheckpointRepairRoutingPolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    max_review_age_seconds: int
    allow_checkpoint_creation_route: bool
    allow_reference_update_route: bool
    require_complete_v106_revalidation: bool
    require_exact_repository_binding: bool
    require_read_only_routing: bool
    execute_live_git: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_repository_ids"] = list(self.allowed_repository_ids)
        payload["allowed_checkpoint_references"] = list(
            self.allowed_checkpoint_references
        )
        return payload


def repository_checkpoint_repair_routing_policy_digest(
    policy: RepositoryCheckpointRepairRoutingPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointRepairRoute:
    route_id: str
    status: str
    primitive: str
    review_record_digest: str
    routing_policy_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_old_oid: str
    proposed_new_oid: str
    automatic_route_eligible: bool
    human_review_required: bool
    repository_change_authority_granted: bool
    live_git_execution_performed: bool
    routed_at_epoch_seconds: int
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    route_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_repair_route_digest(
    route: RepositoryCheckpointRepairRoute,
) -> str:
    payload = route.to_dict()
    payload.pop("route_digest", None)
    return canonical_digest(payload)
