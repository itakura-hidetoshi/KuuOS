#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_evolution_workspace_types_v1_04 import (
    repository_checkpoint_evolution_workspace_digest,
)
from runtime.v104_workspace_helpers import (
    initialize_repository_checkpoint_evolution_workspace,
    repository_checkpoint_evolution_workspace_issues,
    repository_checkpoint_workspace_seed_issues,
)


def reset_repository_checkpoint_evolution_workspace(workspace, seed):
    issues = repository_checkpoint_evolution_workspace_issues(workspace)
    seed_issues = repository_checkpoint_workspace_seed_issues(seed)
    if issues:
        raise ValueError(f"workspace_invalid:{issues[0]}")
    if seed_issues:
        raise ValueError(f"workspace_seed_invalid:{seed_issues[0]}")
    if workspace.seed_digest != seed.seed_digest:
        raise ValueError("workspace_reset_seed_mismatch")
    reset = initialize_repository_checkpoint_evolution_workspace(
        workspace.workspace_id,
        seed,
    )
    reset = replace(reset, sequence_number=workspace.sequence_number + 1)
    return replace(
        reset,
        workspace_digest=repository_checkpoint_evolution_workspace_digest(reset),
    )


def fork_repository_checkpoint_evolution_workspace(workspace_id, seed):
    return initialize_repository_checkpoint_evolution_workspace(workspace_id, seed)


def repository_checkpoint_workspace_diff(seed, workspace):
    seed_issues = repository_checkpoint_workspace_seed_issues(seed)
    workspace_issues = repository_checkpoint_evolution_workspace_issues(workspace)
    if seed_issues:
        raise ValueError(f"workspace_seed_invalid:{seed_issues[0]}")
    if workspace_issues:
        raise ValueError(f"workspace_invalid:{workspace_issues[0]}")
    if workspace.seed_digest != seed.seed_digest:
        raise ValueError("workspace_diff_seed_mismatch")
    before = {file.path: file for file in seed.files}
    after = {file.path: file for file in workspace.files}
    added = tuple(sorted(set(after) - set(before)))
    deleted = tuple(sorted(set(before) - set(after)))
    modified = tuple(
        sorted(
            path
            for path in set(before) & set(after)
            if before[path].content_digest != after[path].content_digest
            or before[path].executable != after[path].executable
        )
    )
    changed = tuple(sorted(set(added + modified + deleted)))
    return {
        "seed_digest": seed.seed_digest,
        "workspace_digest": workspace.workspace_digest,
        "added_paths": list(added),
        "modified_paths": list(modified),
        "deleted_paths": list(deleted),
        "changed_paths": list(changed),
    }
