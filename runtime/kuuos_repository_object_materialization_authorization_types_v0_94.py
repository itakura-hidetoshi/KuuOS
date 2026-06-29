#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_object_materialization_authorization_v0_94"
AUTHORIZATION_GRANTED = "REPOSITORY_OBJECT_MATERIALIZATION_AUTHORIZATION_GRANTED"
AUTHORIZATION_REJECTED = "REPOSITORY_OBJECT_MATERIALIZATION_AUTHORIZATION_REJECTED"
GIT_OBJECT_FORMAT_SHA1 = "sha1"
OBJECT_KINDS = ("blob", "commit", "tree")


@dataclass(frozen=True)
class RepositoryObjectMaterializationAuthorizationPolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    authorized_nonce_authority_ids: tuple[str, ...]
    allowed_object_kinds: tuple[str, ...]
    max_authorization_lifetime_seconds: int
    max_observation_age_seconds: int
    max_nonce_status_age_seconds: int
    max_new_object_count: int
    max_new_payload_bytes: int
    require_object_database_source: bool
    require_working_tree_ignored: bool
    require_reference_nonmutation: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_object_materialization_authorization_policy_digest(
    policy: RepositoryObjectMaterializationAuthorizationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCandidateObject:
    kind: str
    oid: str
    payload_size: int
    payload_digest: str
    origins: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositoryObjectDatabaseEntry:
    kind: str
    oid: str
    payload_size: int
    payload_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepositoryObjectDatabaseObservation:
    observation_id: str
    repository_id: str
    git_dir_fingerprint: str
    object_format: str
    source_commit_sha: str
    queried_oids: tuple[str, ...]
    existing_objects: tuple[RepositoryObjectDatabaseEntry, ...]
    object_database_read: bool
    working_tree_read: bool
    observed_at_epoch_seconds: int
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "observation_id": self.observation_id,
            "repository_id": self.repository_id,
            "git_dir_fingerprint": self.git_dir_fingerprint,
            "object_format": self.object_format,
            "source_commit_sha": self.source_commit_sha,
            "queried_oids": list(self.queried_oids),
            "existing_objects": [entry.to_dict() for entry in self.existing_objects],
            "object_database_read": self.object_database_read,
            "working_tree_read": self.working_tree_read,
            "observed_at_epoch_seconds": self.observed_at_epoch_seconds,
            "receipt_digest": self.receipt_digest,
            "version": self.version,
        }


def repository_object_database_observation_digest(
    observation: RepositoryObjectDatabaseObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryObjectMaterializationScope:
    scope_id: str
    candidate_certificate_digest: str
    authorization_policy_digest: str
    object_database_observation_digest: str
    repository_id: str
    git_dir_fingerprint: str
    parent_commit_sha: str
    candidate_commit_oid: str
    authorization_nonce: str
    issued_at_epoch_seconds: int
    expires_at_epoch_seconds: int
    scope_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_object_materialization_scope_digest(
    scope: RepositoryObjectMaterializationScope,
) -> str:
    payload = scope.to_dict()
    payload.pop("scope_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryObjectMaterializationNonceStatusReceipt:
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


def repository_object_materialization_nonce_status_receipt_digest(
    receipt: RepositoryObjectMaterializationNonceStatusReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryObjectMaterializationPlanItem:
    kind: str
    oid: str
    payload_size: int
    payload_digest: str
    origins: tuple[str, ...]
    already_present_exact: bool
    write_required: bool
    write_order: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepositoryObjectMaterializationAuthorizationCertificate:
    authorization_id: str
    status: str
    candidate_certificate_digest: str
    authorization_policy_digest: str
    materialization_scope_digest: str
    object_database_observation_digest: str
    nonce_status_receipt_digest: str
    repository_id: str
    git_dir_fingerprint: str
    parent_commit_sha: str
    candidate_commit_oid: str
    plan_items: tuple[RepositoryObjectMaterializationPlanItem, ...]
    unique_candidate_object_count: int
    reused_existing_object_count: int
    new_object_count: int
    new_payload_bytes: int
    evaluated_at_epoch_seconds: int
    candidate_certificate_valid: bool
    candidate_binding_exact: bool
    policy_binding_exact: bool
    scope_binding_exact: bool
    observation_binding_exact: bool
    repository_allowed: bool
    repository_identity_exact: bool
    object_format_exact: bool
    source_parent_present: bool
    queried_object_set_exact: bool
    candidate_object_payloads_exact: bool
    existing_objects_collision_free: bool
    existing_objects_reused_exactly: bool
    object_order_deterministic: bool
    object_kinds_allowed: bool
    object_count_within_policy: bool
    payload_bytes_within_policy: bool
    observation_fresh: bool
    object_database_source: bool
    working_tree_ignored: bool
    nonce_authority_authorized: bool
    nonce_scope_bound: bool
    nonce_status_fresh: bool
    nonce_unused: bool
    nonce_not_revoked: bool
    authorization_lifetime_within_policy: bool
    authorization_not_expired: bool
    no_future_evidence: bool
    reference_nonmutation_required: bool
    materialization_authorization_granted: bool
    single_use_materialization_eligible: bool
    object_database_write_authority_granted: bool
    commit_object_materialization_authority_granted: bool
    object_database_write_performed: bool
    commit_object_written: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    reference_mutation_authority_granted: bool
    reference_mutated: bool
    signing_performed: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["plan_items"] = [item.to_dict() for item in self.plan_items]
        return payload


def repository_object_materialization_authorization_certificate_digest(
    certificate: RepositoryObjectMaterializationAuthorizationCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
