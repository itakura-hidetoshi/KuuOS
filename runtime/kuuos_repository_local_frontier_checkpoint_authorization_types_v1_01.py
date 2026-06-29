#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_local_frontier_checkpoint_authorization_v1_01"
AUTHORIZATION_GRANTED = "REPOSITORY_LOCAL_FRONTIER_CHECKPOINT_AUTHORIZATION_GRANTED"
AUTHORIZATION_REJECTED = "REPOSITORY_LOCAL_FRONTIER_CHECKPOINT_AUTHORIZATION_REJECTED"
ZERO_OID = "0" * 40
CHECKPOINT_NAMESPACE = "refs/kuuos/checkpoints/"


@dataclass(frozen=True)
class RepositoryLocalFrontierCheckpointPolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    authorized_nonce_authority_ids: tuple[str, ...]
    max_authorization_lifetime_seconds: int
    max_reference_observation_age_seconds: int
    max_nonce_status_age_seconds: int
    require_compare_and_swap_nonexistence: bool
    require_exact_final_tip: bool
    require_direct_checkpoint_reference: bool
    require_reference_store_source: bool
    require_working_tree_ignored: bool
    require_reflog_ignored: bool
    require_remote_ignored: bool
    allow_checkpoint_overwrite: bool
    allow_reference_delete: bool
    allow_force_update: bool
    allow_tag_creation: bool
    allow_push: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_local_frontier_checkpoint_policy_digest(
    policy: RepositoryLocalFrontierCheckpointPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointReferenceObservation:
    observation_id: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    observed_oid: str
    rechecked_oid: str
    direct: bool
    symbolic: bool
    reference_store_read: bool
    working_tree_read: bool
    reflog_read: bool
    remote_read: bool
    observed_at_epoch_seconds: int
    rechecked_at_epoch_seconds: int
    observation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_reference_observation_digest(
    observation: RepositoryCheckpointReferenceObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("observation_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryLocalFrontierCheckpointScope:
    scope_id: str
    finality_certificate_digest: str
    authorization_policy_digest: str
    checkpoint_observation_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_old_oid: str
    proposed_new_oid: str
    transaction_id: str
    create_requested: bool
    overwrite_requested: bool
    delete_requested: bool
    force_update_requested: bool
    tag_creation_requested: bool
    push_requested: bool
    authorization_nonce: str
    issued_at_epoch_seconds: int
    expires_at_epoch_seconds: int
    scope_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_local_frontier_checkpoint_scope_digest(
    scope: RepositoryLocalFrontierCheckpointScope,
) -> str:
    payload = scope.to_dict()
    payload.pop("scope_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryLocalFrontierCheckpointNonceStatusReceipt:
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


def repository_local_frontier_checkpoint_nonce_status_receipt_digest(
    receipt: RepositoryLocalFrontierCheckpointNonceStatusReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryLocalFrontierCheckpointAuthorizationCertificate:
    authorization_id: str
    status: str
    finality_certificate_digest: str
    authorization_policy_digest: str
    checkpoint_scope_digest: str
    checkpoint_observation_digest: str
    nonce_status_receipt_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_old_oid: str
    proposed_new_oid: str
    transaction_id: str
    evaluated_at_epoch_seconds: int
    finality_certificate_valid: bool
    finality_certificate_committed: bool
    finality_certificate_binding_exact: bool
    finality_history_bound: bool
    policy_valid: bool
    policy_binding_exact: bool
    repository_allowed: bool
    repository_identity_exact: bool
    checkpoint_name_valid: bool
    checkpoint_name_normalized: bool
    checkpoint_reference_allowed: bool
    checkpoint_namespace_exact: bool
    checkpoint_reference_direct: bool
    checkpoint_reference_not_symbolic: bool
    checkpoint_reference_not_head: bool
    checkpoint_reference_not_branch: bool
    checkpoint_reference_not_tag: bool
    checkpoint_reference_not_remote: bool
    checkpoint_reference_not_notes: bool
    checkpoint_reference_not_replace: bool
    checkpoint_observation_bound: bool
    checkpoint_observation_fresh: bool
    checkpoint_reference_store_source: bool
    checkpoint_working_tree_ignored: bool
    checkpoint_reflog_ignored: bool
    checkpoint_remote_ignored: bool
    checkpoint_unchanged_since_observation: bool
    checkpoint_absent: bool
    compare_and_swap_nonexistence_required: bool
    final_tip_exact: bool
    final_tip_present: bool
    nonce_authority_authorized: bool
    nonce_scope_bound: bool
    nonce_status_fresh: bool
    nonce_unused: bool
    nonce_not_revoked: bool
    authorization_lifetime_within_policy: bool
    authorization_not_expired: bool
    no_future_evidence: bool
    create_requested: bool
    overwrite_not_requested: bool
    delete_not_requested: bool
    force_update_not_requested: bool
    tag_creation_not_requested: bool
    push_not_requested: bool
    single_use_checkpoint_creation_eligible: bool
    checkpoint_creation_authority_granted: bool
    checkpoint_creation_authorized: bool
    checkpoint_overwrite_authorized: bool
    force_update_authorized: bool
    reference_delete_authorized: bool
    tag_creation_authorized: bool
    push_authorized: bool
    checkpoint_created: bool
    checkpoint_reference_mutated: bool
    branch_updated: bool
    tag_updated: bool
    remote_reference_updated: bool
    push_performed: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    object_database_write_performed: bool
    reflog_write_performed: bool
    signing_performed: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_local_frontier_checkpoint_authorization_certificate_digest(
    certificate: RepositoryLocalFrontierCheckpointAuthorizationCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
