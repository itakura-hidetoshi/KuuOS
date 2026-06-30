#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_candidate_v1_09"
CANDIDATE_NONE = "CHECKPOINT_CANDIDATE_NONE"
CANDIDATE_READY = "CHECKPOINT_CANDIDATE_READY"
CANDIDATE_REJECTED = "CHECKPOINT_CANDIDATE_REJECTED"
REASON_CLEAN_NOOP = "CLEAN_NOOP"
REASON_CREATION_ROUTE_AVAILABLE = "CREATION_ROUTE_AVAILABLE"
REASON_CHECKPOINT_INTERFACE_REQUIRED = "CHECKPOINT_INTERFACE_REQUIRED"
REASON_INVALID_EVIDENCE = "INVALID_EVIDENCE"


@dataclass(frozen=True)
class RepositoryCheckpointCandidatePolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    max_gate_age_seconds: int
    require_complete_v108_revalidation: bool
    require_exact_repository_binding: bool
    require_distinct_nonzero_oids: bool
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


def repository_checkpoint_candidate_policy_digest(
    policy: RepositoryCheckpointCandidatePolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointCandidate:
    candidate_id: str
    status: str
    reason: str
    namespace_gate_decision_digest: str
    candidate_policy_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    proposed_checkpoint_oid: str
    dedicated_checkpoint_interface_required: bool
    human_review_required: bool
    repository_change_authority_granted: bool
    execution_performed: bool
    evaluated_at_epoch_seconds: int
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    candidate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_candidate_digest(
    candidate: RepositoryCheckpointCandidate,
) -> str:
    payload = candidate.to_dict()
    payload.pop("candidate_digest", None)
    return canonical_digest(payload)
