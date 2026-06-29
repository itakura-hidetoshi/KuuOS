#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_alignment_normal_form_types_v0_80 import (
    AlignmentNormalFormCertificate,
    normal_form_certificate_digest,
)
from runtime.kuuos_repository_atomic_application_contracts_v0_92 import (
    build_repository_authorization_nonce_registry,
    build_repository_authorized_patch_bundle,
    repository_rollback_material_issues,
)
from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    RepositoryAuthorizationNonceRegistry,
    RepositoryAuthorizedPatchBundle,
    RepositoryRollbackMaterial,
)
from runtime.kuuos_repository_application_authorization_types_v0_91 import (
    RepositoryApplicationScope,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


def apply_patch_bundle_to_snapshot(
    source_snapshot: RepositorySnapshot,
    bundle: RepositoryAuthorizedPatchBundle,
) -> tuple[RepositorySnapshot, bool]:
    texts = source_snapshot.texts
    for patch in bundle.patches:
        current = texts.get(patch.path)
        if current is None or canonical_digest(current) != patch.before_digest:
            return source_snapshot, False
        texts[patch.path] = patch.after_text
    return (
        RepositorySnapshot(
            root_label=source_snapshot.root_label,
            all_paths=source_snapshot.all_paths,
            text_files=tuple(sorted(texts.items())),
        ),
        True,
    )


def changed_paths(
    source_snapshot: RepositorySnapshot,
    target_snapshot: RepositorySnapshot,
) -> tuple[str, ...]:
    source_texts = source_snapshot.texts
    target_texts = target_snapshot.texts
    return tuple(
        sorted(
            path
            for path in set(source_texts) | set(target_texts)
            if source_texts.get(path) != target_texts.get(path)
        )
    )


def normal_form_certificate_matches_snapshot(
    certificate: AlignmentNormalFormCertificate,
    snapshot: RepositorySnapshot,
) -> bool:
    return all((
        certificate.certificate_digest
        == normal_form_certificate_digest(certificate),
        certificate.initial_snapshot_digest == snapshot.digest,
        certificate.initial_score == 0,
        certificate.explored_state_count == 1,
        certificate.explored_transition_count == 0,
        certificate.terminal_snapshot_digests == (snapshot.digest,),
        certificate.terminal_scores == (0,),
        certificate.all_transitions_strictly_decreasing,
        certificate.all_terminals_fixed_points,
        certificate.unique_terminal,
        certificate.unique_terminal_digest == snapshot.digest,
        certificate.deterministic_trace_matches_terminal,
        not certificate.external_approval_required,
    ))


def rollback_material_restores_source(
    material: RepositoryRollbackMaterial,
    source_snapshot: RepositorySnapshot,
    candidate_snapshot: RepositorySnapshot,
) -> bool:
    if repository_rollback_material_issues(material):
        return False
    if material.source_snapshot_digest != source_snapshot.digest:
        return False
    if material.candidate_snapshot_digest != candidate_snapshot.digest:
        return False
    if not material.inverse_patches:
        return candidate_snapshot.digest == source_snapshot.digest
    bundle = build_repository_authorized_patch_bundle(
        "rollback-verification-v092",
        candidate_snapshot,
        material.inverse_patches,
    )
    restored, before_exact = apply_patch_bundle_to_snapshot(
        candidate_snapshot,
        bundle,
    )
    return before_exact and restored.digest == source_snapshot.digest


def matching_nonce_entries(
    registry: RepositoryAuthorizationNonceRegistry,
    scope: RepositoryApplicationScope,
):
    return tuple(
        entry
        for entry in registry.entries
        if entry.authorization_nonce == scope.authorization_nonce
        and entry.authorization_scope_digest == scope.scope_digest
    )


def registry_with_nonce_marked_used(
    registry: RepositoryAuthorizationNonceRegistry,
    scope: RepositoryApplicationScope,
) -> RepositoryAuthorizationNonceRegistry:
    return build_repository_authorization_nonce_registry(
        registry.registry_id,
        tuple(
            replace(entry, consumed=True)
            if entry.authorization_nonce == scope.authorization_nonce
            and entry.authorization_scope_digest == scope.scope_digest
            else entry
            for entry in registry.entries
        ),
    )
