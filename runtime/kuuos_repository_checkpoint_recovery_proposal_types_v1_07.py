#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_recovery_proposal_v1_07"
RECOVERY_NOT_NEEDED = "REPOSITORY_CHECKPOINT_RECOVERY_NOT_NEEDED"
RECOVERY_PROPOSED = "REPOSITORY_CHECKPOINT_RECOVERY_PROPOSED"
RECOVERY_REJECTED = "REPOSITORY_CHECKPOINT_RECOVERY_REJECTED"
ACTION_NONE = "NO_REPOSITORY_CHANGE"
ACTION_RESTORE_CHECKPOINT_REFERENCE = "PROPOSE_RESTORE_CHECKPOINT_REFERENCE"
ZERO_OID = "0" * 40


@dataclass(frozen=True)
class RepositoryCheckpointRecoveryProposalPolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    authorized_proposer_ids: tuple[str, ...]
    max_review_record_age_seconds: int
    max_proposal_lifetime_seconds: int
    require_exact_compare_and_swap: bool
    require_external_human_decision: bool
    read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_repository_ids"] = list(self.allowed_repository_ids)
        payload["allowed_checkpoint_references"] = list(
            self.allowed_checkpoint_references
        )
        payload["authorized_proposer_ids"] = list(self.authorized_proposer_ids)
        return payload


def repository_checkpoint_recovery_proposal_policy_digest(
    policy: RepositoryCheckpointRecoveryProposalPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointRecoveryProposal:
    proposal_id: str
    status: str
    action: str
    discrepancy_kind: str
    review_record_digest: str
    proposal_policy_digest: str
    proposer_id: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    proposed_target_oid: str
    external_human_decision_required: bool
    proposed_at_epoch_seconds: int
    expires_at_epoch_seconds: int
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    proposal_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_recovery_proposal_digest(
    proposal: RepositoryCheckpointRecoveryProposal,
) -> str:
    payload = proposal.to_dict()
    payload.pop("proposal_digest", None)
    return canonical_digest(payload)
