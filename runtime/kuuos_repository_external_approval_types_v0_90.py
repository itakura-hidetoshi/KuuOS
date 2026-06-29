#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_external_approval_v0_90"

APPROVAL_ACCEPTED = "REPOSITORY_EVOLUTION_EXTERNAL_APPROVAL_ACCEPTED"
APPROVAL_REJECTED = "REPOSITORY_EVOLUTION_EXTERNAL_APPROVAL_REJECTED"

DECISION_APPROVE = "APPROVE"
DECISION_REJECT = "REJECT"


@dataclass(frozen=True)
class RepositoryExternalApprovalPolicy:
    policy_id: str
    authorized_approver_ids: tuple[str, ...]
    authorized_verifier_ids: tuple[str, ...]
    authorized_revocation_authority_ids: tuple[str, ...]
    authorized_approver_key_binding_digests: tuple[str, ...]
    allowed_signature_algorithms: tuple[str, ...]
    max_admission_certificate_age_seconds: int
    max_approval_lifetime_seconds: int
    max_verification_age_seconds: int
    max_revocation_status_age_seconds: int
    require_distinct_approver_and_verifier: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_external_approval_policy_digest(
    policy: RepositoryExternalApprovalPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


def repository_approver_key_binding_digest(
    approver_id: str,
    signing_key_id: str,
) -> str:
    return canonical_digest({
        "approver_id": approver_id,
        "signing_key_id": signing_key_id,
    })


@dataclass(frozen=True)
class RepositoryExternalApprovalAttestation:
    approval_id: str
    admission_certificate_digest: str
    approval_policy_digest: str
    approver_id: str
    decision: str
    issued_at_epoch_seconds: int
    expires_at_epoch_seconds: int
    signature_algorithm: str
    signing_key_id: str
    signed_payload_digest: str
    signature_digest: str
    attestation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_external_approval_signed_payload_digest(
    attestation: RepositoryExternalApprovalAttestation,
) -> str:
    return canonical_digest({
        "approval_id": attestation.approval_id,
        "admission_certificate_digest": attestation.admission_certificate_digest,
        "approval_policy_digest": attestation.approval_policy_digest,
        "approver_id": attestation.approver_id,
        "decision": attestation.decision,
        "issued_at_epoch_seconds": attestation.issued_at_epoch_seconds,
        "expires_at_epoch_seconds": attestation.expires_at_epoch_seconds,
        "signature_algorithm": attestation.signature_algorithm,
        "signing_key_id": attestation.signing_key_id,
        "version": attestation.version,
    })


def repository_external_approval_attestation_digest(
    attestation: RepositoryExternalApprovalAttestation,
) -> str:
    payload = attestation.to_dict()
    payload.pop("attestation_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositorySignatureVerificationReceipt:
    verification_id: str
    attestation_digest: str
    verifier_id: str
    verified_at_epoch_seconds: int
    signature_algorithm: str
    signing_key_id: str
    signed_payload_digest: str
    signature_digest: str
    signature_verified: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_signature_verification_receipt_digest(
    receipt: RepositorySignatureVerificationReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryApprovalRevocationStatusReceipt:
    status_id: str
    attestation_digest: str
    approval_policy_digest: str
    authority_id: str
    checked_at_epoch_seconds: int
    registry_snapshot_digest: str
    revoked: bool
    revocation_effective_at_epoch_seconds: int
    revocation_reason_digest: str
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_approval_revocation_status_receipt_digest(
    receipt: RepositoryApprovalRevocationStatusReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryEvolutionExternalApprovalCertificate:
    receipt_id: str
    status: str
    admission_certificate_digest: str
    approval_policy_digest: str
    approval_attestation_digest: str
    signature_verification_receipt_digest: str
    revocation_status_receipt_digest: str
    evaluated_at_epoch_seconds: int
    admission_proposal_bound: bool
    policy_binding_exact: bool
    attestation_binding_exact: bool
    decision_approve: bool
    approver_authorized: bool
    approver_key_authorized: bool
    verifier_authorized: bool
    revocation_authority_authorized: bool
    signature_algorithm_allowed: bool
    distinct_approval_roles: bool
    signed_payload_binding_exact: bool
    signature_metadata_binding_exact: bool
    signature_verified: bool
    time_order_valid: bool
    admission_certificate_fresh: bool
    approval_lifetime_within_policy: bool
    approval_not_expired: bool
    verification_fresh: bool
    revocation_status_fresh: bool
    no_future_evidence: bool
    revocation_status_valid: bool
    not_revoked: bool
    external_approval_granted: bool
    application_authorization_eligible: bool
    patch_application_authority_granted: bool
    commit_authority_granted: bool
    reference_mutation_authority_granted: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_evolution_external_approval_certificate_digest(
    certificate: RepositoryEvolutionExternalApprovalCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
