#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_cas_single_use_authorization_v1_15"
AUTHORIZATION_GRANTED = "CHECKPOINT_CAS_SINGLE_USE_AUTHORIZATION_GRANTED"
AUTHORIZATION_DENIED = "CHECKPOINT_CAS_SINGLE_USE_AUTHORIZATION_DENIED"
AUTHORIZATION_REJECTED = "CHECKPOINT_CAS_SINGLE_USE_AUTHORIZATION_REJECTED"
REASON_READY_AUTHORIZED = "READY_REQUEST_SINGLE_USE_AUTHORIZED"
REASON_DENIAL_PRESERVED = "UPSTREAM_REQUEST_DENIAL_PRESERVED"
REASON_INVALID_AUTHORIZATION = "INVALID_SINGLE_USE_AUTHORIZATION_EVIDENCE"


@dataclass(frozen=True)
class RepositoryCheckpointCasAuthorizationPolicy:
    policy_id: str
    allowed_authority_ids: tuple[str, ...]
    max_nonce_status_age_seconds: int
    require_valid_v114_request: bool
    require_exact_nonce_request_binding: bool
    require_unused_nonce: bool
    require_unrevoked_nonce: bool
    require_single_use_scope: bool
    authorization_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_authority_ids"] = list(self.allowed_authority_ids)
        return payload


def repository_checkpoint_cas_authorization_policy_digest(
    policy: RepositoryCheckpointCasAuthorizationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointCasAuthorizationNonceStatusReceipt:
    status_id: str
    authorization_nonce: str
    authorization_request_digest: str
    authority_id: str
    checked_at_epoch_seconds: int
    registry_snapshot_digest: str
    consumed: bool
    revoked: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_cas_authorization_nonce_status_receipt_digest(
    receipt: RepositoryCheckpointCasAuthorizationNonceStatusReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointCasSingleUseAuthorizationCertificate:
    authorization_id: str
    status: str
    reason: str
    authorization_request_digest: str
    authorization_policy_digest: str
    nonce_status_receipt_digest: str
    authority_id: str
    authorization_nonce: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    observed_current_oid: str
    proposed_checkpoint_oid: str
    request_expires_at_epoch_seconds: int
    evaluated_at_epoch_seconds: int
    request_valid: bool
    policy_valid: bool
    denial_preserved: bool
    nonce_status_required: bool
    nonce_status_valid: bool
    nonce_request_binding_exact: bool
    nonce_authority_allowed: bool
    nonce_status_fresh: bool
    nonce_unused: bool
    nonce_not_revoked: bool
    authorization_not_expired: bool
    single_use_scope_exact: bool
    authorization_granted: bool
    execution_performed: bool
    live_git_command_invoked: bool
    reference_mutated: bool
    nonce_consumed: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_cas_single_use_authorization_certificate_digest(
    certificate: RepositoryCheckpointCasSingleUseAuthorizationCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
