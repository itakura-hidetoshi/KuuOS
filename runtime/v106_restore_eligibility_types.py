#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_checkpoint_restore_authorization_types_v1_06 import VERSION

ELIGIBILITY_CONFIRMED = "REPOSITORY_CHECKPOINT_RESTORE_ELIGIBILITY_CONFIRMED"
ELIGIBILITY_REJECTED = "REPOSITORY_CHECKPOINT_RESTORE_ELIGIBILITY_REJECTED"


@dataclass(frozen=True)
class RepositoryCheckpointRestoreEligibilityCertificate:
    eligibility_id: str
    status: str
    failure_kind: str
    stability_certificate_digest: str
    restore_policy_digest: str
    restore_observation_digest: str
    restore_scope_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    restore_target_oid: str
    transaction_id: str
    executor_id: str
    authorization_nonce: str
    evaluated_at_epoch_seconds: int
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_restore_eligibility_certificate_digest(
    certificate: RepositoryCheckpointRestoreEligibilityCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
