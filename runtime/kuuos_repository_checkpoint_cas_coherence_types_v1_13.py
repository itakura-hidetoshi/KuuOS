#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_cas_coherence_v1_13"
COHERENCE_READY = "CHECKPOINT_CAS_COHERENCE_READY"
COHERENCE_CONFLICT = "CHECKPOINT_CAS_COHERENCE_CONFLICT"
COHERENCE_REJECTED = "CHECKPOINT_CAS_COHERENCE_REJECTED"
REASON_COHERENT_READY = "COHERENT_VALIDATED_CONTRACT_READY"
REASON_COHERENT_CONFLICT = "COHERENT_VALIDATED_CONTRACT_CONFLICT"
REASON_INCOHERENT_EVIDENCE = "INCOHERENT_CHECKPOINT_CAS_EVIDENCE"


@dataclass(frozen=True)
class RepositoryCheckpointCasCoherenceReceipt:
    receipt_id: str
    status: str
    reason: str
    contract_digest: str
    intake_digest: str
    candidate_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    observed_current_oid: str
    proposed_checkpoint_oid: str
    contract_digest_valid: bool
    contract_local_coherence: bool
    intake_digest_valid: bool
    intake_local_coherence: bool
    exact_contract_intake_binding: bool
    compare_and_swap_required: bool
    repository_change_authority_granted: bool
    execution_performed: bool
    live_git_command_invoked: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    coherence_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_cas_coherence_digest(
    receipt: RepositoryCheckpointCasCoherenceReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("coherence_digest", None)
    return canonical_digest(payload)
