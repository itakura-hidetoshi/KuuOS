#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat

from runtime.kuuos_repository_constructed_commit_publication_types_v1_21 import (
    COMMIT_PUBLISHED,
)
from runtime.kuuos_repository_sandbox_worktree_types_v1_23 import (
    WORKTREE_MATERIALIZED,
    WORKTREE_REUSED,
)
from runtime.v121_constructed_commit_publication_policy import (
    repository_constructed_commit_publication_request_issues,
)
from runtime.v121_constructed_commit_publication_result import (
    repository_constructed_commit_publication_result_issues,
)
from runtime.v123_sandbox_worktree_policy import (
    repository_sandbox_worktree_request_issues,
)
from runtime.v123_sandbox_worktree_result import (
    repository_sandbox_worktree_result_issues,
)


def file_digest(path: Path) -> str:
    if not path.is_file() or path.is_symlink():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_snapshot(root: Path):
    if not root.exists() or root.is_symlink():
        return ()
    rows = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        mode = os.lstat(path).st_mode
        if stat.S_ISLNK(mode):
            rows.append((str(relative), "symlink", os.readlink(path)))
        elif stat.S_ISDIR(mode):
            rows.append((str(relative), "dir", stat.S_IMODE(mode)))
        elif stat.S_ISREG(mode):
            rows.append(
                (
                    str(relative),
                    "file",
                    stat.S_IMODE(mode),
                    file_digest(path),
                )
            )
        else:
            rows.append((str(relative), "other", stat.S_IFMT(mode)))
    return tuple(rows)


def repository_root_snapshot(root: Path):
    rows = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] == ".git":
            continue
        mode = os.lstat(path).st_mode
        if stat.S_ISLNK(mode):
            rows.append((str(relative), "symlink", os.readlink(path)))
        elif stat.S_ISDIR(mode):
            rows.append((str(relative), "dir", stat.S_IMODE(mode)))
        elif stat.S_ISREG(mode):
            rows.append(
                (
                    str(relative),
                    "file",
                    stat.S_IMODE(mode),
                    file_digest(path),
                )
            )
        else:
            rows.append((str(relative), "other", stat.S_IFMT(mode)))
    return tuple(rows)


def protected_snapshot(
    root: Path,
    dedicated_index_filename: str,
    target_reflog_path: Path,
):
    git_dir = root / ".git"
    all_logs = tree_snapshot(git_dir / "logs")
    other_logs = tuple(
        row
        for row in all_logs
        if not (
            row
            and row[0]
            == str(target_reflog_path.relative_to(git_dir / "logs"))
        )
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


def target_reflog_path(git_dir: Path, checkpoint_reference: str) -> Path:
    return git_dir / "logs" / checkpoint_reference


def target_reflog_path_is_exact(
    git_dir: Path,
    checkpoint_reference: str,
    path: Path,
) -> bool:
    expected = target_reflog_path(git_dir, checkpoint_reference)
    if path != expected or path.is_symlink():
        return False
    current = git_dir
    for component in ("logs", *checkpoint_reference.split("/")):
        current = current / component
        if current.is_symlink():
            return False
    return True


def expected_reflog_entry(request) -> bytes:
    return (
        f"{request.transition_old_oid} {request.transition_new_oid} "
        f"{request.committer_name} <{request.committer_email}> "
        f"{request.recorded_at_epoch_seconds} {request.timezone_offset}"
        f"\t{request.message}\n"
    ).encode("utf-8")


def inspect_target_reflog(path: Path, request) -> tuple[bool, bool]:
    if not path.is_file() or path.is_symlink():
        return False, False
    payload = path.read_bytes()
    exact = payload == expected_reflog_entry(request)
    single = bool(payload.endswith(b"\n") and payload.count(b"\n") == 1)
    return exact, single


def validate_upstream_binding(
    request,
    v121_request,
    v121_result,
    v123_request,
    v123_result,
):
    v121_request_valid = not repository_constructed_commit_publication_request_issues(
        v121_request
    )
    v121_result_valid = not repository_constructed_commit_publication_result_issues(
        v121_result
    )
    v121_accepted = bool(
        v121_result_valid
        and v121_result.status == COMMIT_PUBLISHED
        and v121_result.reference_cas_committed
        and v121_result.checkpoint_reference_write_performed
        and v121_result.observed_after_oid == v121_result.constructed_commit_oid
        and not v121_result.current_object_database_write_performed
        and not v121_result.reflog_write_performed
    )
    v123_request_valid = not repository_sandbox_worktree_request_issues(
        v123_request
    )
    v123_result_valid = not repository_sandbox_worktree_result_issues(v123_result)
    v123_accepted = bool(
        v123_result_valid
        and v123_result.status in (WORKTREE_MATERIALIZED, WORKTREE_REUSED)
        and v123_result.sandbox_present_after
        and v123_result.sandbox_files_exact
        and v123_result.sandbox_modes_exact
        and v123_result.sandbox_has_no_extra_entries
        and v123_result.dedicated_index_unchanged
        and v123_result.canonical_index_unchanged
        and v123_result.repository_root_unchanged
        and not v123_result.current_object_database_write_performed
        and not v123_result.current_reference_write_performed
        and not v123_result.reflog_write_performed
    )
    binding_exact = bool(
        request.repository_path_digest
        == v121_result.repository_path_digest
        == v123_result.repository_path_digest
        and request.repository_id
        == v121_result.repository_id
        == v123_result.repository_id
        and request.git_dir_fingerprint
        == v121_result.git_dir_fingerprint
        == v123_result.git_dir_fingerprint
        and request.v121_request_digest
        == v121_request.request_digest
        == v121_result.request_digest
        and request.v121_result_digest == v121_result.result_digest
        and request.v123_request_digest
        == v123_request.request_digest
        == v123_result.request_digest
        and request.v123_result_digest == v123_result.result_digest
        and request.checkpoint_reference
        == v121_request.checkpoint_reference
        == v121_result.checkpoint_reference
        and request.transition_old_oid
        == v121_request.expected_current_oid
        == v121_result.expected_current_oid
        and request.transition_new_oid
        == v121_request.constructed_commit_oid
        == v121_result.constructed_commit_oid
        == v123_request.published_commit_oid
        == v123_result.published_commit_oid
        and request.executor_id
        == v121_request.executor_id
        == v121_result.executor_id
        == v123_request.executor_id
        == v123_result.executor_id
    )
    return (
        v121_request_valid,
        v121_result_valid,
        v121_accepted,
        v123_request_valid,
        v123_result_valid,
        v123_accepted,
        binding_exact,
    )
