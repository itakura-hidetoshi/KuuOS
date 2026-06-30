#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_atomic_cas_transition_v1_16"

TRANSITION_COMMITTED = "CHECKPOINT_ATOMIC_CAS_TRANSITION_COMMITTED"
TRANSITION_ABORTED = "CHECKPOINT_ATOMIC_CAS_TRANSITION_ABORTED"


@dataclass(frozen=True)
class RepositoryCheckpointAtomicCasTransitionPolicy:
    policy_id: str
    authorized_executor_ids: tuple[str, ...]
    max_execution_duration_seconds: int
    max_reference_state_age_seconds: int
    max_nonce_registry_age_seconds: int
    require_atomic_compare_and_swap: bool
    require_atomic_nonce_consumption: bool
    require_checkpoint_namespace: bool
    require_reference_store_source: bool
    require_working_tree_ignored: bool
    allow_force_update: bool
    allow_reference_delete: bool
    allow_push: bool
    modeled_transition_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["authorized_executor_ids"] = list(self.authorized_executor_ids)
        return payload


def repository_checkpoint_atomic_cas_transition_policy_digest(
    policy: RepositoryCheckpointAtomicCasTransitionPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointReferenceState:
    state_id: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    current_oid: str
    direct: bool
    symbolic: bool
    reference_store_source: bool
    working_tree_source: bool
    sequence_number: int
    observed_at_epoch_seconds: int
    state_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_reference_state_digest(
    state: RepositoryCheckpointReferenceState,
) -> str:
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
class RepositoryCheckpointAtomicCasTransitionRequest:
    transaction_id: str
    authorization_certificate_digest: str
    decision_policy_digest: str
    request_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    proposed_checkpoint_oid: str
    authorization_nonce: str
    executor_id: str
    force_update_requested: bool
    delete_requested: bool
    push_requested: bool
    requested_at_epoch_seconds: int
    request_digest_v116: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_atomic_cas_transition_request_digest(
    request: RepositoryCheckpointAtomicCasTransitionRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest_v116", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointAtomicCasTransitionResult:
    transaction_id: str
    status: str
    authorization_certificate_digest: str
    execution_policy_digest: str
    transition_request_digest: str
    source_reference_state_digest: str
    final_reference_state_digest: str
    source_nonce_registry_digest: str
    final_nonce_registry_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    proposed_checkpoint_oid: str
    authorization_nonce: str
    executor_id: str
    execution_started_at_epoch_seconds: int
    execution_completed_at_epoch_seconds: int
    authorization_valid: bool
    authorization_granted: bool
    authorization_binding_exact: bool
    execution_policy_valid: bool
    transition_request_valid: bool
    transition_request_binding_exact: bool
    executor_authorized: bool
    reference_state_valid: bool
    reference_state_binding_exact: bool
    reference_state_fresh: bool
    reference_direct: bool
    reference_not_symbolic: bool
    reference_store_source: bool
    reference_working_tree_ignored: bool
    current_oid_matches_expected: bool
    nonce_registry_valid: bool
    nonce_registry_authority_exact: bool
    nonce_registry_snapshot_bound: bool
    nonce_registry_fresh: bool
    nonce_unused: bool
    nonce_not_revoked: bool
    authorization_not_expired_at_execution: bool
    execution_duration_within_policy: bool
    no_future_evidence: bool
    compare_and_swap_required: bool
    compare_and_swap_attempted: bool
    compare_and_swap_succeeded: bool
    atomic_nonce_consumption_required: bool
    atomic_reference_nonce_transition: bool
    transition_committed: bool
    modeled_reference_state_mutated: bool
    modeled_nonce_registry_mutated: bool
    nonce_consumed: bool
    failure_preserved_reference_state: bool
    failure_preserved_nonce_registry: bool
    force_update_performed: bool
    reference_delete_performed: bool
    push_performed: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    object_database_write_performed: bool
    reflog_write_performed: bool
    signing_performed: bool
    live_git_command_invoked: bool
    live_repository_mutated: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    result_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_atomic_cas_transition_result_digest(
    result: RepositoryCheckpointAtomicCasTransitionResult,
) -> str:
    payload = result.to_dict()
    payload.pop("result_digest", None)
    return canonical_digest(payload)
