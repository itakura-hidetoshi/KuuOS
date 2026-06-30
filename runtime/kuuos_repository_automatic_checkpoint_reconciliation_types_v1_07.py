#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_automatic_checkpoint_reconciliation_v1_07"
RECONCILIATION_NOOP = "REPOSITORY_CHECKPOINT_RECONCILIATION_NOOP"
RECONCILIATION_RECOVERY_RECOMMENDED = "REPOSITORY_CHECKPOINT_RECOVERY_RECOMMENDED"
RECONCILIATION_REJECTED = "REPOSITORY_CHECKPOINT_RECONCILIATION_REJECTED"
ACTION_NONE = "NONE"
ACTION_RECOVER_LOST = "RECOVER_LOST_CHECKPOINT"
ACTION_RECOVER_SUBSTITUTED = "RECOVER_SUBSTITUTED_CHECKPOINT"


@dataclass(frozen=True)
class RepositoryCheckpointReconciliationPolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    max_review_age_seconds: int
    automatic_decision: bool
    human_review_required: bool
    read_only: bool
    repository_change_authority_granted: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_repository_ids"] = list(self.allowed_repository_ids)
        payload["allowed_checkpoint_references"] = list(self.allowed_checkpoint_references)
        return payload


def repository_checkpoint_reconciliation_policy_digest(
    policy: RepositoryCheckpointReconciliationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointReconciliationDecision:
    decision_id: str
    status: str
    action: str
    discrepancy_kind: str
    review_record_digest: str
    reconciliation_policy_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    current_oid: str
    target_oid: str
    decided_at_epoch_seconds: int
    automatic_decision: bool
    human_review_required: bool
    recovery_recommended: bool
    repository_change_authority_granted: bool
    checks: dict[str, bool]
    decision_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_reconciliation_decision_digest(
    decision: RepositoryCheckpointReconciliationDecision,
) -> str:
    payload = decision.to_dict()
    payload.pop("decision_digest", None)
    return canonical_digest(payload)
