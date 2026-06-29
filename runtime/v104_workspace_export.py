#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import shutil
import tempfile

from runtime.v104_workspace_helpers import (
    canonical_repository_path,
    repository_checkpoint_evolution_workspace_issues,
)
from runtime.v104_workspace_serialization import (
    repository_checkpoint_evolution_workspace_from_dict,
)

EXPORT_VERSION = "kuuos_repository_checkpoint_workspace_export_v1_04"


def materialize_repository_checkpoint_evolution_workspace(
    workspace,
    destination,
):
    issues = repository_checkpoint_evolution_workspace_issues(workspace)
    if issues:
        raise ValueError(f"workspace_invalid:{issues[0]}")
    target = Path(destination)
    if target.exists() or target.is_symlink():
        raise FileExistsError("workspace_destination_exists")
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{target.name}.kuuos-v104-",
            dir=str(target.parent),
        )
    )
    try:
        written = []
        for file in workspace.files:
            canonical_repository_path(file.path)
            output = staging.joinpath(*file.path.split("/"))
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(file.content, encoding="utf-8", newline="")
            output.chmod(0o755 if file.executable else 0o644)
            written.append(file.path)
        staging.rename(target)
        return tuple(written)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


__all__ = [
    "materialize_repository_checkpoint_evolution_workspace",
    "repository_checkpoint_evolution_workspace_from_dict",
]
