#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_repository_checkpoint_evolution_workspace_types_v1_04 import (
    RepositoryCheckpointEvolutionWorkspace,
    RepositoryCheckpointWorkspaceFile,
)
from runtime.v104_workspace_helpers import (
    repository_checkpoint_evolution_workspace_issues,
)


def repository_checkpoint_evolution_workspace_from_dict(
    payload: Mapping[str, Any],
) -> RepositoryCheckpointEvolutionWorkspace:
    files = tuple(
        RepositoryCheckpointWorkspaceFile(**dict(item))
        for item in payload.get("files", [])
    )
    workspace = RepositoryCheckpointEvolutionWorkspace(
        workspace_id=str(payload.get("workspace_id", "")),
        seed_digest=str(payload.get("seed_digest", "")),
        repository_id=str(payload.get("repository_id", "")),
        git_dir_fingerprint=str(payload.get("git_dir_fingerprint", "")),
        checkpoint_reference=str(payload.get("checkpoint_reference", "")),
        checkpoint_oid=str(payload.get("checkpoint_oid", "")),
        candidate_id=str(payload.get("candidate_id", "")),
        status=str(payload.get("status", "")),
        files=files,
        applied_operation_digests=tuple(
            payload.get("applied_operation_digests", [])
        ),
        changed_paths=tuple(payload.get("changed_paths", [])),
        sequence_number=int(payload.get("sequence_number", -1)),
        tree_digest=str(payload.get("tree_digest", "")),
        workspace_digest=str(payload.get("workspace_digest", "")),
        version=str(payload.get("version", "")),
    )
    issues = repository_checkpoint_evolution_workspace_issues(workspace)
    if issues:
        raise ValueError(f"workspace_json_invalid:{issues[0]}")
    return workspace
