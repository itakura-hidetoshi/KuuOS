#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_incremental_preservation_types_v0_81 import (
    GLOBAL_SCOPE_ID,
    AlignmentScopeFingerprint,
    AlignmentScopeIndex,
    IncrementalScopeDelta,
    alignment_scope_digest,
    alignment_scope_index_digest,
    incremental_scope_delta_digest,
)
from runtime.kuuos_repository_structure_observer_v0_79 import (
    LAKEFILE,
    LEAN_AGGREGATE_ROOT,
    RUNTIME_ROOT,
    parse_repository_contracts,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot

ROOT_PATHS = (RUNTIME_ROOT, LEAN_AGGREGATE_ROOT, LAKEFILE)


def _path_digest(snapshot: RepositorySnapshot, path: str) -> str:
    texts = snapshot.texts
    return canonical_digest({
        "path": path,
        "present": path in set(snapshot.all_paths),
        "text": texts.get(path),
    })


def _scope(
    snapshot: RepositorySnapshot,
    scope_id: str,
    scope_kind: str,
    manifest_path: str,
    member_paths: tuple[str, ...],
) -> AlignmentScopeFingerprint:
    normalized = tuple(sorted(set(member_paths)))
    scope = AlignmentScopeFingerprint(
        scope_id,
        scope_kind,
        manifest_path,
        normalized,
        tuple((path, _path_digest(snapshot, path)) for path in normalized),
        "",
    )
    return replace(scope, scope_digest=alignment_scope_digest(scope))


def build_alignment_scope_index(
    snapshot: RepositorySnapshot,
) -> AlignmentScopeIndex:
    contracts, malformed = parse_repository_contracts(snapshot)
    manifest_paths = tuple(sorted(
        path
        for path, _ in snapshot.text_files
        if path.startswith("manifests/") and path.endswith(".json")
    ))
    workflow_paths = tuple(sorted(
        path
        for path, _ in snapshot.text_files
        if path.startswith(".github/workflows/")
        and path.endswith((".yml", ".yaml"))
    ))
    global_members = tuple(sorted(set(
        ROOT_PATHS + manifest_paths + workflow_paths + malformed
    )))
    scopes: list[AlignmentScopeFingerprint] = [
        _scope(
            snapshot,
            GLOBAL_SCOPE_ID,
            "GLOBAL",
            "",
            global_members,
        )
    ]
    for contract in contracts:
        members = tuple(sorted(set(
            ROOT_PATHS
            + (contract.manifest_path,)
            + contract.referenced_paths
        )))
        scopes.append(_scope(
            snapshot,
            f"contract:{contract.manifest_path}",
            "CONTRACT",
            contract.manifest_path,
            members,
        ))
    scopes.sort(key=lambda item: item.scope_id)
    index = AlignmentScopeIndex(snapshot.digest, tuple(scopes), "")
    return replace(index, index_digest=alignment_scope_index_digest(index))


def scope_snapshot(
    snapshot: RepositorySnapshot,
    scope: AlignmentScopeFingerprint,
) -> RepositorySnapshot:
    paths = set(scope.member_paths)
    return RepositorySnapshot(
        f"{snapshot.root_label}:{scope.scope_id}",
        tuple(sorted(path for path in snapshot.all_paths if path in paths)),
        tuple(sorted(
            (path, text)
            for path, text in snapshot.text_files
            if path in paths
        )),
    )


def _changed_paths(
    previous: RepositorySnapshot,
    current: RepositorySnapshot,
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    previous_paths = set(previous.all_paths)
    current_paths = set(current.all_paths)
    added = tuple(sorted(current_paths - previous_paths))
    removed = tuple(sorted(previous_paths - current_paths))
    common = previous_paths & current_paths
    previous_texts = previous.texts
    current_texts = current.texts
    modified = {
        path
        for path in common
        if previous_texts.get(path) != current_texts.get(path)
    }
    changed = tuple(sorted(set(added) | set(removed) | modified))
    return changed, added, removed


def compare_alignment_scope_indexes(
    previous_snapshot: RepositorySnapshot,
    current_snapshot: RepositorySnapshot,
) -> tuple[AlignmentScopeIndex, AlignmentScopeIndex, IncrementalScopeDelta]:
    previous_index = build_alignment_scope_index(previous_snapshot)
    current_index = build_alignment_scope_index(current_snapshot)
    previous_scopes = {scope.scope_id: scope for scope in previous_index.scopes}
    current_scopes = {scope.scope_id: scope for scope in current_index.scopes}
    previous_ids = set(previous_scopes)
    current_ids = set(current_scopes)
    added_scope_ids = tuple(sorted(current_ids - previous_ids))
    removed_scope_ids = tuple(sorted(previous_ids - current_ids))
    common_ids = previous_ids & current_ids
    reused = tuple(sorted(
        scope_id
        for scope_id in common_ids
        if previous_scopes[scope_id].scope_digest
        == current_scopes[scope_id].scope_digest
    ))
    invalidated = tuple(sorted(
        scope_id
        for scope_id in common_ids
        if previous_scopes[scope_id].scope_digest
        != current_scopes[scope_id].scope_digest
    ))
    changed, added, removed = _changed_paths(previous_snapshot, current_snapshot)
    global_changed = GLOBAL_SCOPE_ID in set(invalidated)
    full_recheck = bool(
        global_changed or added_scope_ids or removed_scope_ids
    )
    delta = IncrementalScopeDelta(
        previous_snapshot.digest,
        current_snapshot.digest,
        changed,
        added,
        removed,
        reused,
        invalidated,
        added_scope_ids,
        removed_scope_ids,
        global_changed,
        full_recheck,
        "",
    )
    return previous_index, current_index, replace(
        delta,
        delta_digest=incremental_scope_delta_digest(delta),
    )
