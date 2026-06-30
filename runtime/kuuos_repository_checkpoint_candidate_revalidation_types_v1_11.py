#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_candidate_revalidation_v1_11"
REVALIDATION_VALID = "CHECKPOINT_CANDIDATE_REVALIDATION_VALID"
REVALIDATION_REJECTED = "CHECKPOINT_CANDIDATE_REVALIDATION_REJECTED"
REASON_FULL_REVALIDATION_PASSED = "FULL_V109_REVALIDATION_PASSED"
REASON_CANDIDATE_STALE = "CANDIDATE_STALE"
REASON_INVALID_EVIDENCE = "INVALID_EVIDENCE"


@dataclass(frozen=True)
class RepositoryCheckpointCandidateRevalidationPolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    max_candidate_age_seconds: int
    require_complete_v109_revalidation: bool
    require_exact_repository_binding: bool
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


def repository_checkpoint_candidate_revalidation_policy_digest(
    policy: RepositoryCheckpointCandidateRevalidationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointCandidateRevalidationReceipt:
    receipt_id: str
    status: str
    reason: str
    candidate_digest: str
    revalidation_policy_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    candidate_evaluated_at_epoch_seconds: int
    revalidated_at_epoch_seconds: int
    full_v109_revalidation_passed: bool
    repository_binding_exact: bool
    candidate_fresh: bool
    repository_change_authority_granted: bool
    execution_performed: bool
    live_git_command_invoked: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_candidate_revalidation_receipt_digest(
    receipt: RepositoryCheckpointCandidateRevalidationReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
