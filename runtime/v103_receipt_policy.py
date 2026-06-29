#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_creation_receipt_v1_03"
RECEIPT_CONFIRMED = "REPOSITORY_CHECKPOINT_CREATION_RECEIPT_CONFIRMED"
RECEIPT_REJECTED = "REPOSITORY_CHECKPOINT_CREATION_RECEIPT_REJECTED"


@dataclass(frozen=True)
class RepositoryCheckpointCreationReceiptPolicy:
    policy_id: str
    authorized_observer_ids: tuple[str, ...]
    max_report_age_seconds: int
    max_observation_age_seconds: int
    max_external_duration_seconds: int
    required_absent_effects: tuple[str, ...]
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["authorized_observer_ids"] = list(self.authorized_observer_ids)
        payload["required_absent_effects"] = list(self.required_absent_effects)
        return payload


def repository_checkpoint_creation_receipt_policy_digest(
    policy: RepositoryCheckpointCreationReceiptPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)
