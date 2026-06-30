#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_validated_cas_intake_v1_12"
INTAKE_READY = "CHECKPOINT_VALIDATED_CAS_INTAKE_READY"
INTAKE_CONFLICT = "CHECKPOINT_VALIDATED_CAS_INTAKE_CONFLICT"
INTAKE_REJECTED = "CHECKPOINT_VALIDATED_CAS_INTAKE_REJECTED"
REASON_VALIDATED_READY = "VALIDATED_CONTRACT_READY"
REASON_VALIDATED_CONFLICT = "VALIDATED_CONTRACT_CONFLICT"
REASON_INVALID_BINDING = "INVALID_VALIDATION_CONTRACT_BINDING"


@dataclass(frozen=True)
class RepositoryCheckpointValidatedCasIntakePolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    require_valid_v111_receipt: bool
    require_valid_v110_contract: bool
    require_exact_candidate_binding: bool
    require_exact_oid_binding: bool
    read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_repository_ids"] = list(self.allowed_repository_ids)
        payload["allowed_checkpoint_references"] = list(
            self.allowed_checkpoint_references
        )
        return payload


def repository_checkpoint_validated_cas_intake_policy_digest(
    policy: RepositoryCheckpointValidatedCasIntakePolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointValidatedCasIntake:
    intake_id: str
    status: str
    reason: str
    validation_digest: str
    contract_digest: str
    candidate_digest: str
    policy_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    observed_current_oid: str
    proposed_checkpoint_oid: str
    upstream_chain_revalidated: bool
    validation_receipt_valid: bool
    contract_valid: bool
    candidate_binding_exact: bool
    repository_binding_exact: bool
    checkpoint_binding_exact: bool
    oid_binding_exact: bool
    compare_and_swap_required: bool
    repository_change_authority_granted: bool
    execution_performed: bool
    live_git_command_invoked: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    intake_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_validated_cas_intake_digest(
    intake: RepositoryCheckpointValidatedCasIntake,
) -> str:
    payload = intake.to_dict()
    payload.pop("intake_digest", None)
    return canonical_digest(payload)
