#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_cas_contract_v1_10"
CONTRACT_NONE = "CHECKPOINT_CAS_CONTRACT_NONE"
CONTRACT_READY = "CHECKPOINT_CAS_CONTRACT_READY"
CONTRACT_CONFLICT = "CHECKPOINT_CAS_CONTRACT_CONFLICT"
CONTRACT_REJECTED = "CHECKPOINT_CAS_CONTRACT_REJECTED"
REASON_NO_READY_CANDIDATE = "NO_READY_CANDIDATE"
REASON_EXPECTED_OID_CONFIRMED = "EXPECTED_OID_CONFIRMED"
REASON_CURRENT_OID_CHANGED = "CURRENT_OID_CHANGED"
REASON_INVALID_EVIDENCE = "INVALID_EVIDENCE"


@dataclass(frozen=True)
class RepositoryCheckpointCasPolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    require_ready_v109_candidate: bool
    require_exact_repository_binding: bool
    require_observed_oid_match: bool
    specification_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_repository_ids"] = list(self.allowed_repository_ids)
        payload["allowed_checkpoint_references"] = list(self.allowed_checkpoint_references)
        return payload


def repository_checkpoint_cas_policy_digest(policy: RepositoryCheckpointCasPolicy) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointCasContract:
    contract_id: str
    status: str
    reason: str
    candidate_digest: str
    policy_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    observed_current_oid: str
    proposed_checkpoint_oid: str
    compare_and_swap_required: bool
    checkpoint_namespace_only: bool
    repository_change_authority_granted: bool
    execution_performed: bool
    live_git_command_invoked: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    contract_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_cas_contract_digest(contract: RepositoryCheckpointCasContract) -> str:
    payload = contract.to_dict()
    payload.pop("contract_digest", None)
    return canonical_digest(payload)
