#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.v105_checkpoint_stability_policy_types import VERSION


@dataclass(frozen=True)
class RepositoryCheckpointStabilityCertificate:
    certificate_id: str
    status: str
    failure_kind: str
    creation_receipt_digest: str
    stability_policy_digest: str
    delayed_observation_digest: str
    reachability_observation_digest: str
    namespace_observation_digest: str
    transaction_id: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_oid: str
    evaluated_at_epoch_seconds: int
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_stability_certificate_digest(
    certificate: RepositoryCheckpointStabilityCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
