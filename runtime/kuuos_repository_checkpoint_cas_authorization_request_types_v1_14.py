#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_cas_authorization_request_v1_14"
REQUEST_READY = "CHECKPOINT_CAS_AUTHORIZATION_REQUEST_READY"
REQUEST_DENIED = "CHECKPOINT_CAS_AUTHORIZATION_REQUEST_DENIED"
REQUEST_REJECTED = "CHECKPOINT_CAS_AUTHORIZATION_REQUEST_REJECTED"
REASON_COHERENT_READY = "COHERENT_READY_REQUEST"
REASON_COHERENT_CONFLICT = "COHERENT_CONFLICT_DENIAL"
REASON_INVALID_REQUEST = "INVALID_CAS_AUTHORIZATION_REQUEST"


@dataclass(frozen=True)
class RepositoryCheckpointCasAuthorizationRequestPolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    max_request_lifetime_seconds: int
    require_coherent_v113_receipt: bool
    require_ready_status_for_request: bool
    require_single_use_authorization: bool
    request_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_repository_ids"] = list(self.allowed_repository_ids)
        payload["allowed_checkpoint_references"] = list(
            self.allowed_checkpoint_references
        )
        return payload


def repository_checkpoint_cas_authorization_request_policy_digest(
    policy: RepositoryCheckpointCasAuthorizationRequestPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointCasAuthorizationRequest:
    request_id: str
    status: str
    reason: str
    coherence_digest: str
    request_policy_digest: str
    requester_id: str
    authorization_nonce: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    observed_current_oid: str
    proposed_checkpoint_oid: str
    issued_at_epoch_seconds: int
    expires_at_epoch_seconds: int
    coherence_receipt_valid: bool
    repository_allowed: bool
    checkpoint_reference_allowed: bool
    lifetime_within_policy: bool
    request_not_expired_at_issue: bool
    nonce_present: bool
    single_use_authorization_required: bool
    authorization_granted: bool
    execution_performed: bool
    live_git_command_invoked: bool
    reference_mutated: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_cas_authorization_request_digest(
    request: RepositoryCheckpointCasAuthorizationRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)
