#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_atomic_checkpoint_creation_v1_02"
CHECKPOINT_CREATION_COMMITTED = "REPOSITORY_ATOMIC_CHECKPOINT_CREATION_COMMITTED"
CHECKPOINT_CREATION_ABORTED = "REPOSITORY_ATOMIC_CHECKPOINT_CREATION_ABORTED"
ZERO_OID = "0" * 40


@dataclass(frozen=True)
class RepositoryAtomicCheckpointCreationPolicy:
    policy_id: str
    authorized_executor_ids: tuple[str, ...]
    max_execution_duration_seconds: int
    max_checkpoint_state_age_seconds: int
    max_nonce_registry_age_seconds: int
    require_atomic_compare_and_swap_nonexistence: bool
    require_atomic_nonce_consumption: bool
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
        payload = asdict(self)
        payload["authorized_executor_ids"] = list(self.authorized_executor_ids)
        return payload


def repository_atomic_checkpoint_creation_policy_digest(
    policy: RepositoryAtomicCheckpointCreationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointState:
    state_id: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    current_oid: str
    direct: bool
    symbolic: bool
    reference_store_source: bool
    working_tree_source: bool
    reflog_source: bool
    remote_source: bool
    sequence_number: int
    observed_at_epoch_seconds: int
    state_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_state_digest(state: RepositoryCheckpointState) -> str:
    payload = state.to_dict()
    payload.pop("state_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointNonceRegistry:
    registry_id: str
    authority_id: str
    upstream_snapshot_digest: str
    consumed_nonces: tuple[str, ...]
    revoked_nonces: tuple[str, ...]
    sequence_number: int
    observed_at_epoch_seconds: int
    registry_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["consumed_nonces"] = list(self.consumed_nonces)
        payload["revoked_nonces"] = list(self.revoked_nonces)
        return payload


def repository_checkpoint_nonce_registry_digest(
    registry: RepositoryCheckpointNonceRegistry,
) -> str:
    payload = registry.to_dict()
    payload.pop("registry_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryAtomicCheckpointCreationRequest:
    request_id: str
    transaction_id: str
    authorization_certificate_digest: str
    authorization_scope_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_old_oid: str
    proposed_new_oid: str
    authorization_nonce: str
    executor_id: str
    create_requested: bool
    overwrite_requested: bool
    delete_requested: bool
    force_update_requested: bool
    tag_creation_requested: bool
    push_requested: bool
    requested_at_epoch_seconds: int
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_atomic_checkpoint_creation_request_digest(
    request: RepositoryAtomicCheckpointCreationRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryAtomicCheckpointCreationResult:
    transaction_id: str
    status: str
    authorization_certificate_digest: str
    execution_policy_digest: str
    request_digest: str
    source_checkpoint_state_digest: str
    final_checkpoint_state_digest: str
    source_nonce_registry_digest: str
    final_nonce_registry_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_old_oid: str
    proposed_new_oid: str
    authorization_nonce: str
    executor_id: str
    execution_started_at_epoch_seconds: int
    execution_completed_at_epoch_seconds: int
    authorization_valid: bool
    authorization_granted: bool
    authorization_binding_exact: bool
    execution_policy_valid: bool
    request_valid: bool
    request_binding_exact: bool
    executor_authorized: bool
    checkpoint_state_valid: bool
    checkpoint_state_binding_exact: bool
    checkpoint_state_fresh: bool
    checkpoint_reference_direct: bool
    checkpoint_reference_not_symbolic: bool
    checkpoint_reference_store_source: bool
    checkpoint_working_tree_ignored: bool
    checkpoint_reflog_ignored: bool
    checkpoint_remote_ignored: bool
    checkpoint_absent_before_creation: bool
    current_oid_matches_expected_zero: bool
    nonce_registry_valid: bool
    nonce_registry_authority_exact: bool
    nonce_registry_snapshot_bound: bool
    nonce_registry_fresh: bool
    nonce_unused: bool
    nonce_not_revoked: bool
    authorization_not_expired_at_execution: bool
    execution_duration_within_policy: bool
    no_future_evidence: bool
    compare_and_swap_nonexistence_required: bool
    compare_and_swap_attempted: bool
    compare_and_swap_succeeded: bool
    atomic_nonce_consumption_required: bool
    atomic_checkpoint_nonce_transition: bool
    checkpoint_creation_transition_committed: bool
    checkpoint_state_mutated: bool
    checkpoint_created: bool
    nonce_consumed: bool
    failure_preserved_checkpoint_state: bool
    failure_preserved_nonce_registry: bool
    checkpoint_overwrite_performed: bool
    force_update_performed: bool
    reference_delete_performed: bool
    branch_updated: bool
    tag_updated: bool
    remote_reference_updated: bool
    push_performed: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    object_database_write_performed: bool
    reflog_write_performed: bool
    signing_performed: bool
    live_git_command_invoked: bool
    live_repository_mutated: bool
    result_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_atomic_checkpoint_creation_result_digest(
    result: RepositoryAtomicCheckpointCreationResult,
) -> str:
    payload = result.to_dict()
    payload.pop("result_digest", None)
    return canonical_digest(payload)
