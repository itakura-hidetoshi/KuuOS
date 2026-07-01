#!/usr/bin/env python3
from pathlib import Path

from runtime.v124_checkpoint_reflog_validation import (
    file_digest,
    repository_root_snapshot,
    tree_snapshot,
)


def protected_checkpoint_reflog_snapshot(
    root: Path,
    dedicated_index_filename: str,
    target_reflog_path: Path,
):
    git_dir = root / ".git"
    logs_root = git_dir / "logs"
    target_relative = target_reflog_path.relative_to(logs_root)
    ancestor_names = {
        str(Path(*target_relative.parts[:index]))
        for index in range(1, len(target_relative.parts))
    }
    excluded = ancestor_names | {str(target_relative)}
    other_logs = tuple(
        row
        for row in tree_snapshot(logs_root)
        if not row or row[0] not in excluded
    )
    return {
        "objects": tree_snapshot(git_dir / "objects"),
        "references": (
            tree_snapshot(git_dir / "refs"),
            file_digest(git_dir / "HEAD"),
            file_digest(git_dir / "packed-refs"),
        ),
        "standard_index": file_digest(git_dir / "index"),
        "dedicated_index": file_digest(git_dir / dedicated_index_filename),
        "working_tree": repository_root_snapshot(root),
        "other_logs": other_logs,
        "target_reflog": file_digest(target_reflog_path),
    }
