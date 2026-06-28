#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


def capture_explicit_repository_snapshot(
    root: Path,
    relative_paths: Iterable[str],
) -> RepositorySnapshot:
    root = root.resolve()
    normalized = tuple(sorted(set(relative_paths)))
    all_paths: list[str] = []
    text_files: list[tuple[str, str]] = []
    for relative in normalized:
        candidate = (root / relative).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"snapshot_path_outside_root:{relative}") from exc
        if not candidate.is_file():
            continue
        all_paths.append(relative)
        try:
            text = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        text_files.append((relative, text))
    return RepositorySnapshot(
        root.name,
        tuple(all_paths),
        tuple(text_files),
    )
