#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    RepositoryAtomicApplicationPolicy,
    RepositoryAuthorizationNonceEntry,
    RepositoryAuthorizationNonceRegistry,
    RepositoryAuthorizedPatchBundle,
    RepositoryRollbackMaterial,
    repository_atomic_application_policy_digest,
    repository_authorization_nonce_registry_digest,
    repository_authorized_patch_bundle_digest,
    repository_rollback_material_digest,
)
from runtime.kuuos_repository_structure_types_v0_79 import (
    RepositoryPatch,
    RepositorySnapshot,
)


def _canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def repository_atomic_application_policy_issues(
    policy: RepositoryAtomicApplicationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("atomic_application_policy_id_missing")
    if policy.authorized_executor_ids != _canonical_strings(
        policy.authorized_executor_ids
    ):
        issues.append("atomic_application_executor_ids_not_canonical")
    if not policy.authorized_executor_ids:
        issues.append("atomic_application_executor_ids_empty")
    if any(value <= 0 for value in (
        policy.max_application_duration_seconds,
        policy.max_patch_count,
        policy.max_changed_path_count,
    )):
        issues.append("atomic_application_policy_bound_invalid")
    if not policy.require_exact_changed_paths:
        issues.append("atomic_application_exact_paths_not_required")
    if not policy.require_result_normal_form:
        issues.append("atomic_application_normal_form_not_required")
    if policy.policy_digest != repository_atomic_application_policy_digest(policy):
        issues.append("atomic_application_policy_digest_mismatch")
    return tuple(issues)


def build_repository_atomic_application_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    max_application_duration_seconds: int,
    max_patch_count: int,
    max_changed_path_count: int,
) -> RepositoryAtomicApplicationPolicy:
    policy = RepositoryAtomicApplicationPolicy(
        policy_id=policy_id,
        authorized_executor_ids=_canonical_strings(authorized_executor_ids),
        max_application_duration_seconds=max_application_duration_seconds,
        max_patch_count=max_patch_count,
        max_changed_path_count=max_changed_path_count,
        require_exact_changed_paths=True,
        require_result_normal_form=True,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_atomic_application_policy_digest(policy),
    )
    issues = repository_atomic_application_policy_issues(policy)
    if issues:
        raise ValueError(f"atomic_application_policy_invalid:{issues[0]}")
    return policy


def repository_authorized_patch_bundle_issues(
    bundle: RepositoryAuthorizedPatchBundle,
) -> tuple[str, ...]:
    issues: list[str] = []
    paths = tuple(patch.path for patch in bundle.patches)
    if not bundle.bundle_id or not bundle.source_snapshot_digest:
        issues.append("authorized_patch_bundle_binding_missing")
    if not bundle.patches:
        issues.append("authorized_patch_bundle_empty")
    if paths != tuple(sorted(paths)):
        issues.append("authorized_patch_bundle_paths_not_canonical")
    if len(paths) != len(set(paths)):
        issues.append("authorized_patch_bundle_duplicate_path")
    if any(
        not patch.path
        or not patch.before_digest
        or not patch.repair_kind
        or not patch.reason
        for patch in bundle.patches
    ):
        issues.append("authorized_patch_bundle_patch_invalid")
    if bundle.bundle_digest != repository_authorized_patch_bundle_digest(bundle):
        issues.append("authorized_patch_bundle_digest_mismatch")
    return tuple(issues)


def build_repository_authorized_patch_bundle(
    bundle_id: str,
    source_snapshot: RepositorySnapshot,
    patches: tuple[RepositoryPatch, ...],
) -> RepositoryAuthorizedPatchBundle:
    bundle = RepositoryAuthorizedPatchBundle(
        bundle_id=bundle_id,
        source_snapshot_digest=source_snapshot.digest,
        patches=tuple(sorted(patches, key=lambda patch: patch.path)),
        bundle_digest="",
    )
    bundle = replace(
        bundle,
        bundle_digest=repository_authorized_patch_bundle_digest(bundle),
    )
    issues = repository_authorized_patch_bundle_issues(bundle)
    if issues:
        raise ValueError(f"authorized_patch_bundle_invalid:{issues[0]}")
    return bundle


def repository_authorization_nonce_registry_issues(
    registry: RepositoryAuthorizationNonceRegistry,
) -> tuple[str, ...]:
    issues: list[str] = []
    keys = tuple(
        (entry.authorization_nonce, entry.authorization_scope_digest)
        for entry in registry.entries
    )
    if not registry.registry_id:
        issues.append("authorization_nonce_registry_id_missing")
    if keys != tuple(sorted(keys)):
        issues.append("authorization_nonce_registry_not_canonical")
    if len(keys) != len(set(keys)):
        issues.append("authorization_nonce_registry_duplicate_entry")
    if any(not nonce or not scope for nonce, scope in keys):
        issues.append("authorization_nonce_registry_binding_missing")
    if registry.registry_digest != repository_authorization_nonce_registry_digest(
        registry
    ):
        issues.append("authorization_nonce_registry_digest_mismatch")
    return tuple(issues)


def build_repository_authorization_nonce_registry(
    registry_id: str,
    entries: tuple[RepositoryAuthorizationNonceEntry, ...],
) -> RepositoryAuthorizationNonceRegistry:
    registry = RepositoryAuthorizationNonceRegistry(
        registry_id=registry_id,
        entries=tuple(
            sorted(
                entries,
                key=lambda entry: (
                    entry.authorization_nonce,
                    entry.authorization_scope_digest,
                ),
            )
        ),
        registry_digest="",
    )
    registry = replace(
        registry,
        registry_digest=repository_authorization_nonce_registry_digest(registry),
    )
    issues = repository_authorization_nonce_registry_issues(registry)
    if issues:
        raise ValueError(f"authorization_nonce_registry_invalid:{issues[0]}")
    return registry


def build_repository_rollback_material(
    source_snapshot: RepositorySnapshot,
    candidate_snapshot: RepositorySnapshot,
    changed_paths: tuple[str, ...],
) -> RepositoryRollbackMaterial:
    source_texts = source_snapshot.texts
    candidate_texts = candidate_snapshot.texts
    material = RepositoryRollbackMaterial(
        source_snapshot_digest=source_snapshot.digest,
        candidate_snapshot_digest=candidate_snapshot.digest,
        inverse_patches=tuple(
            RepositoryPatch(
                path=path,
                before_digest=canonical_digest(candidate_texts[path]),
                after_text=source_texts[path],
                repair_kind="atomic_application_rollback_v0_92",
                reason="restore exact authorized source snapshot",
            )
            for path in sorted(changed_paths)
        ),
        material_digest="",
    )
    return replace(
        material,
        material_digest=repository_rollback_material_digest(material),
    )


def repository_rollback_material_issues(
    material: RepositoryRollbackMaterial,
) -> tuple[str, ...]:
    issues: list[str] = []
    paths = tuple(patch.path for patch in material.inverse_patches)
    if paths != tuple(sorted(paths)) or len(paths) != len(set(paths)):
        issues.append("rollback_material_paths_not_canonical")
    if not material.source_snapshot_digest or not material.candidate_snapshot_digest:
        issues.append("rollback_material_snapshot_binding_missing")
    if material.material_digest != repository_rollback_material_digest(material):
        issues.append("rollback_material_digest_mismatch")
    return tuple(issues)
