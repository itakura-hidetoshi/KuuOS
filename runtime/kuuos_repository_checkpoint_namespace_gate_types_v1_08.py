#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_namespace_gate_v1_08"
GATE_NOOP = "CHECKPOINT_NAMESPACE_GATE_NOOP"
GATE_ACCEPTED = "CHECKPOINT_NAMESPACE_GATE_ACCEPTED"
GATE_REJECTED = "CHECKPOINT_NAMESPACE_GATE_REJECTED"
REASON_CLEAN = "CLEAN"
REASON_CREATION_ROUTE = "CREATION_ROUTE"
REASON_NAMESPACE_MISMATCH = "NAMESPACE_MISMATCH"
REASON_INVALID_ROUTE = "INVALID_ROUTE"


@dataclass(frozen=True)
class RepositoryCheckpointNamespaceGatePolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    max_route_age_seconds: int
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_repository_ids"] = list(self.allowed_repository_ids)
        payload["allowed_checkpoint_references"] = list(
            self.allowed_checkpoint_references
        )
        return payload


def repository_checkpoint_namespace_gate_policy_digest(
    policy: RepositoryCheckpointNamespaceGatePolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointNamespaceGateDecision:
    decision_id: str
    status: str
    reason: str
    route_digest: str
    policy_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_old_oid: str
    proposed_new_oid: str
    selected_route: str
    compatible: bool
    evaluated_at_epoch_seconds: int
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    decision_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_namespace_gate_decision_digest(
    decision: RepositoryCheckpointNamespaceGateDecision,
) -> str:
    payload = decision.to_dict()
    payload.pop("decision_digest", None)
    return canonical_digest(payload)
