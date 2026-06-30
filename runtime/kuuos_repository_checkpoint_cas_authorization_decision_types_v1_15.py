#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_cas_authorization_decision_v1_15"

EXTERNAL_GRANT = "EXTERNAL_CHECKPOINT_CAS_AUTHORIZATION_GRANT"
EXTERNAL_DENY = "EXTERNAL_CHECKPOINT_CAS_AUTHORIZATION_DENY"

DECISION_GRANTED = "CHECKPOINT_CAS_AUTHORIZATION_GRANTED"
DECISION_DENIED = "CHECKPOINT_CAS_AUTHORIZATION_DENIED"
DECISION_REJECTED = "CHECKPOINT_CAS_AUTHORIZATION_REJECTED"

REASON_VALID_GRANT = "VALID_SINGLE_USE_CHECKPOINT_CAS_AUTHORIZATION"
REASON_VALID_DENIAL = "VALID_CHECKPOINT_CAS_AUTHORIZATION_DENIAL"
REASON_INVALID_DECISION = "INVALID_CHECKPOINT_CAS_AUTHORIZATION_DECISION"


@dataclass(frozen=True)
class RepositoryCheckpointCasAuthorizationDecisionPolicy:
    policy_id: str
    authorized_decision_authority_ids: tuple[str, ...]
    authorized_nonce_authority_ids: tuple[str, ...]
    max_decision_lifetime_seconds: int
    max_nonce_status_age_seconds: int
    require_ready_v114_request_for_grant: bool
    require_external_signature_verification: bool
    require_nonce_unused: bool
    require_nonce_not_revoked: bool
    decision_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["authorized_decision_authority_ids"] = list(
            self.authorized_decision_authority_ids
        )
        payload["authorized_nonce_authority_ids"] = list(
            self.authorized_nonce_authority_ids
        )
        return payload


def repository_checkpoint_cas_authorization_decision_policy_digest(
    policy: RepositoryCheckpointCasAuthorizationDecisionPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointCasExternalAuthorizationDecisionReceipt:
    decision_id: str
    request_digest: str
    request_policy_digest: str
    coherence_digest: str
    authorization_nonce: str
    authority_id: str
    decision: str
    issued_at_epoch_seconds: int
    expires_at_epoch_seconds: int
    signature_verification_receipt_digest: str
    revocation_status_receipt_digest: str
    signature_valid: bool
    authority_identity_verified: bool
    decision_not_revoked: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_cas_external_authorization_decision_receipt_digest(
    receipt: RepositoryCheckpointCasExternalAuthorizationDecisionReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointCasAuthorizationNonceStatusReceipt:
    status_id: str
    authorization_nonce: str
    request_digest: str
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
class RepositoryCheckpointCasAuthorizationDecisionCertificate:
    authorization_id: str
    status: str
    reason: str
    request_digest: str
    request_policy_digest: str
    coherence_digest: str
    decision_policy_digest: str
    external_decision_receipt_digest: str
    nonce_status_receipt_digest: str
    requester_id: str
    decision_authority_id: str
    nonce_authority_id: str
    authorization_nonce: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    observed_current_oid: str
    proposed_checkpoint_oid: str
    evaluated_at_epoch_seconds: int
    request_valid: bool
    request_ready: bool
    request_binding_exact: bool
    decision_policy_valid: bool
    external_decision_receipt_valid: bool
    decision_binding_exact: bool
    decision_authority_authorized: bool
    signature_verification_valid: bool
    authority_identity_verified: bool
    decision_not_revoked: bool
    decision_lifetime_within_policy: bool
    decision_within_request_lifetime: bool
    authorization_not_expired: bool
    nonce_status_receipt_valid: bool
    nonce_scope_bound: bool
    nonce_authority_authorized: bool
    nonce_status_fresh: bool
    nonce_unused: bool
    nonce_not_revoked: bool
    no_future_evidence: bool
    external_grant: bool
    external_decision_accepted: bool
    authorization_granted: bool
    single_use_cas_eligible: bool
    nonce_consumed: bool
    execution_performed: bool
    live_git_command_invoked: bool
    reference_mutated: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_cas_authorization_decision_certificate_digest(
    certificate: RepositoryCheckpointCasAuthorizationDecisionCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
