#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_reference_update_authorization_v0_96"
AUTHORIZATION_GRANTED = "REPOSITORY_REFERENCE_UPDATE_AUTHORIZATION_GRANTED"
AUTHORIZATION_REJECTED = "REPOSITORY_REFERENCE_UPDATE_AUTHORIZATION_REJECTED"
ZERO_OID = "0" * 40


@dataclass(frozen=True)
class RepositoryReferenceUpdatePolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_references: tuple[str, ...]
    authorized_nonce_authority_ids: tuple[str, ...]
    max_authorization_lifetime_seconds: int
    max_reference_observation_age_seconds: int
    max_ancestry_certificate_age_seconds: int
    max_nonce_status_age_seconds: int
    max_ancestry_depth: int
    require_compare_and_swap: bool
    require_fast_forward: bool
    require_direct_local_branch: bool
    require_reference_store_source: bool
    require_object_database_ancestry: bool
    require_working_tree_ignored: bool
    allow_force_update: bool
    allow_reference_delete: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_reference_update_policy_digest(
    policy: RepositoryReferenceUpdatePolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryReferenceObservation:
    observation_id: str
    repository_id: str
    git_dir_fingerprint: str
    target_reference: str
    observed_oid: str
    rechecked_oid: str
    direct: bool
    symbolic: bool
    reference_store_read: bool
    working_tree_read: bool
    observed_at_epoch_seconds: int
    rechecked_at_epoch_seconds: int
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_reference_observation_digest(
    observation: RepositoryReferenceObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryReferenceAncestryCertificate:
    certificate_id: str
    repository_id: str
    git_dir_fingerprint: str
    target_reference: str
    old_oid: str
    new_oid: str
    path_oids: tuple[str, ...]
    depth: int
    candidate_certificate_digest: str
    object_database_observation_digest: str
    object_database_read: bool
    working_tree_read: bool
    observed_at_epoch_seconds: int
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["path_oids"] = list(self.path_oids)
        return payload


def repository_reference_ancestry_certificate_digest(
    certificate: RepositoryReferenceAncestryCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryReferenceUpdateScope:
    scope_id: str
    materialization_receipt_digest: str
    authorization_policy_digest: str
    reference_observation_digest: str
    ancestry_certificate_digest: str
    repository_id: str
    git_dir_fingerprint: str
    target_reference: str
    expected_old_oid: str
    proposed_new_oid: str
    force_update_requested: bool
    delete_requested: bool
    authorization_nonce: str
    issued_at_epoch_seconds: int
    expires_at_epoch_seconds: int
    scope_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_reference_update_scope_digest(
    scope: RepositoryReferenceUpdateScope,
) -> str:
    payload = scope.to_dict()
    payload.pop("scope_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryReferenceUpdateNonceStatusReceipt:
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


def repository_reference_update_nonce_status_receipt_digest(
    receipt: RepositoryReferenceUpdateNonceStatusReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryReferenceUpdateAuthorizationCertificate:
    authorization_id: str
    status: str
    materialization_receipt_digest: str
    authorization_policy_digest: str
    reference_update_scope_digest: str
    reference_observation_digest: str
    ancestry_certificate_digest: str
    nonce_status_receipt_digest: str
    repository_id: str
    git_dir_fingerprint: str
    target_reference: str
    expected_old_oid: str
    proposed_new_oid: str
    evaluated_at_epoch_seconds: int
    materialization_receipt_valid: bool
    materialization_receipt_committed: bool
    materialization_receipt_binding_exact: bool
    repository_allowed: bool
    repository_identity_exact: bool
    reference_name_valid: bool
    reference_normalized: bool
    reference_allowed: bool
    reference_direct: bool
    reference_not_symbolic: bool
    reference_not_head: bool
    reference_not_tag: bool
    reference_not_remote: bool
    reference_not_notes: bool
    reference_not_replace: bool
    reference_not_deleted: bool
    reference_observation_bound: bool
    reference_observation_fresh: bool
    reference_store_source: bool
    reference_working_tree_ignored: bool
    reference_unchanged_since_observation: bool
    old_oid_exact: bool
    new_oid_exact: bool
    candidate_commit_bound: bool
    candidate_commit_present: bool
    source_parent_unchanged: bool
    ancestry_certificate_bound: bool
    fast_forward_verified: bool
    ancestry_depth_within_policy: bool
    ancestry_object_database_source: bool
    ancestry_working_tree_ignored: bool
    nonce_authority_authorized: bool
    nonce_scope_bound: bool
    nonce_status_fresh: bool
    nonce_unused: bool
    nonce_not_revoked: bool
    authorization_lifetime_within_policy: bool
    authorization_not_expired: bool
    no_future_evidence: bool
    compare_and_swap_required: bool
    single_use_reference_update_eligible: bool
    reference_update_authority_granted: bool
    force_update_authorized: bool
    reference_delete_authorized: bool
    reference_update_performed: bool
    reference_mutated: bool
    branch_updated: bool
    head_updated: bool
    tag_updated: bool
    remote_reference_updated: bool
    push_performed: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    object_database_write_performed: bool
    signing_performed: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_reference_update_authorization_certificate_digest(
    certificate: RepositoryReferenceUpdateAuthorizationCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
