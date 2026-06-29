#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_structure_types_v0_79 import RepositoryPatch

VERSION = "kuuos_repository_atomic_application_v0_92"

APPLICATION_APPLIED = "REPOSITORY_ATOMIC_APPLICATION_APPLIED"
APPLICATION_ABORTED = "REPOSITORY_ATOMIC_APPLICATION_ABORTED"


@dataclass(frozen=True)
class RepositoryAtomicApplicationPolicy:
    policy_id: str
    authorized_executor_ids: tuple[str, ...]
    max_application_duration_seconds: int
    max_patch_count: int
    max_changed_path_count: int
    require_exact_changed_paths: bool
    require_result_normal_form: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_atomic_application_policy_digest(
    policy: RepositoryAtomicApplicationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryAuthorizedPatchBundle:
    bundle_id: str
    source_snapshot_digest: str
    patches: tuple[RepositoryPatch, ...]
    bundle_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "source_snapshot_digest": self.source_snapshot_digest,
            "patches": [patch.to_dict() for patch in self.patches],
            "bundle_digest": self.bundle_digest,
            "version": self.version,
        }


def repository_authorized_patch_bundle_digest(
    bundle: RepositoryAuthorizedPatchBundle,
) -> str:
    payload = bundle.to_dict()
    payload.pop("bundle_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryAuthorizationNonceEntry:
    authorization_nonce: str
    authorization_scope_digest: str
    consumed: bool
    revoked: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepositoryAuthorizationNonceRegistry:
    registry_id: str
    entries: tuple[RepositoryAuthorizationNonceEntry, ...]
    registry_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "registry_id": self.registry_id,
            "entries": [entry.to_dict() for entry in self.entries],
            "registry_digest": self.registry_digest,
            "version": self.version,
        }


def repository_authorization_nonce_registry_digest(
    registry: RepositoryAuthorizationNonceRegistry,
) -> str:
    payload = registry.to_dict()
    payload.pop("registry_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryRollbackMaterial:
    source_snapshot_digest: str
    candidate_snapshot_digest: str
    inverse_patches: tuple[RepositoryPatch, ...]
    material_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_snapshot_digest": self.source_snapshot_digest,
            "candidate_snapshot_digest": self.candidate_snapshot_digest,
            "inverse_patches": [patch.to_dict() for patch in self.inverse_patches],
            "material_digest": self.material_digest,
            "version": self.version,
        }


def repository_rollback_material_digest(
    material: RepositoryRollbackMaterial,
) -> str:
    payload = material.to_dict()
    payload.pop("material_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryNonceConsumptionReceipt:
    transaction_id: str
    authorization_nonce: str
    authorization_scope_digest: str
    registry_before_digest: str
    registry_after_digest: str
    consumed_before: bool
    consumed_after: bool
    revoked: bool
    application_committed: bool
    atomic_with_application: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_nonce_consumption_receipt_digest(
    receipt: RepositoryNonceConsumptionReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryAtomicApplicationReceipt:
    transaction_id: str
    status: str
    authorization_certificate_digest: str
    application_scope_digest: str
    application_policy_digest: str
    patch_bundle_digest: str
    source_commit_sha: str
    source_snapshot_digest: str
    candidate_snapshot_digest: str
    final_snapshot_digest: str
    source_observation_digest: str
    candidate_observation_digest: str
    final_observation_digest: str
    normal_form_certificate_digest: str
    rollback_material_digest: str
    nonce_consumption_receipt_digest: str
    registry_before_digest: str
    registry_after_digest: str
    expected_changed_paths: tuple[str, ...]
    actual_changed_paths: tuple[str, ...]
    executor_id: str
    started_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    authorization_valid: bool
    authorization_scope_bound: bool
    authorization_not_expired_at_completion: bool
    application_policy_bound: bool
    executor_authorized: bool
    transaction_time_order_valid: bool
    duration_within_policy: bool
    patch_bundle_bound: bool
    patch_count_within_policy: bool
    patch_paths_unique: bool
    patch_paths_exact: bool
    patch_before_digests_exact: bool
    source_commit_unchanged: bool
    source_snapshot_unchanged: bool
    object_database_source: bool
    working_tree_ignored: bool
    nonce_registry_bound: bool
    nonce_unused_before: bool
    nonce_not_revoked: bool
    actual_changed_paths_exact: bool
    result_snapshot_materialized: bool
    result_observation_exact: bool
    result_normal_form_certified: bool
    rollback_material_exact: bool
    nonce_consumption_committed: bool
    application_effect_committed: bool
    atomic_state_transition: bool
    failure_no_effect: bool
    isolated_snapshot_only: bool
    live_repository_write_performed: bool
    commit_created: bool
    reference_mutated: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_atomic_application_receipt_digest(
    receipt: RepositoryAtomicApplicationReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
