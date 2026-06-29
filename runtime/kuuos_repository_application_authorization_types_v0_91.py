#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_git_revision_types_v0_83 import GitRevisionObservation

VERSION = "kuuos_repository_application_authorization_v0_91"

AUTHORIZATION_GRANTED = "REPOSITORY_APPLICATION_AUTHORIZATION_GRANTED"
AUTHORIZATION_REJECTED = "REPOSITORY_APPLICATION_AUTHORIZATION_REJECTED"


@dataclass(frozen=True)
class RepositoryApplicationAuthorizationPolicy:
    policy_id: str
    authorized_nonce_authority_ids: tuple[str, ...]
    protected_paths: tuple[str, ...]
    max_authorization_lifetime_seconds: int
    max_source_observation_age_seconds: int
    max_nonce_status_age_seconds: int
    max_allowed_path_count: int
    max_patch_count: int
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_application_authorization_policy_digest(
    policy: RepositoryApplicationAuthorizationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryApplicationScope:
    scope_id: str
    external_approval_certificate_digest: str
    admission_certificate_digest: str
    authorization_policy_digest: str
    patch_bundle_digest: str
    patch_count: int
    source_commit_sha: str
    source_snapshot_digest: str
    allowed_paths: tuple[str, ...]
    expected_changed_paths: tuple[str, ...]
    authorization_nonce: str
    issued_at_epoch_seconds: int
    expires_at_epoch_seconds: int
    scope_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_application_scope_digest(
    scope: RepositoryApplicationScope,
) -> str:
    payload = scope.to_dict()
    payload.pop("scope_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryApplicationSourceStateReceipt:
    source_state_id: str
    observed_at_epoch_seconds: int
    revision_observation: GitRevisionObservation
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_application_source_state_receipt_digest(
    receipt: RepositoryApplicationSourceStateReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryAuthorizationNonceStatusReceipt:
    status_id: str
    authorization_nonce: str
    authorization_scope_digest: str
    authority_id: str
    checked_at_epoch_seconds: int
    registry_snapshot_digest: str
    consumed: bool
    revoked: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_authorization_nonce_status_receipt_digest(
    receipt: RepositoryAuthorizationNonceStatusReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryApplicationAuthorizationCertificate:
    authorization_id: str
    status: str
    external_approval_certificate_digest: str
    admission_certificate_digest: str
    authorization_policy_digest: str
    application_scope_digest: str
    patch_bundle_digest: str
    source_state_receipt_digest: str
    nonce_status_receipt_digest: str
    source_commit_sha: str
    source_snapshot_digest: str
    allowed_paths: tuple[str, ...]
    expected_changed_paths: tuple[str, ...]
    authorization_nonce: str
    evaluated_at_epoch_seconds: int
    external_approval_bound: bool
    admission_binding_exact: bool
    policy_binding_exact: bool
    scope_binding_exact: bool
    patch_bundle_bound: bool
    paths_canonical: bool
    expected_paths_nonempty: bool
    expected_paths_within_allowed_scope: bool
    protected_paths_excluded: bool
    path_count_within_policy: bool
    patch_count_within_policy: bool
    source_commit_unchanged: bool
    source_snapshot_unchanged: bool
    source_observation_fresh: bool
    object_database_source: bool
    working_tree_ignored: bool
    nonce_authority_authorized: bool
    nonce_status_fresh: bool
    nonce_unused: bool
    nonce_not_revoked: bool
    authorization_lifetime_within_policy: bool
    authorization_not_expired: bool
    no_future_evidence: bool
    application_authorization_granted: bool
    single_use_application_eligible: bool
    patch_application_executed: bool
    commit_authority_granted: bool
    reference_mutation_authority_granted: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_application_authorization_certificate_digest(
    certificate: RepositoryApplicationAuthorizationCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
