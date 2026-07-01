#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat

from runtime.kuuos_repository_dedicated_index_types_v1_22 import (
    INDEX_MATERIALIZED,
    INDEX_REUSED,
)
from runtime.v122_dedicated_index_policy import (
    repository_dedicated_index_request_issues,
)
from runtime.v122_dedicated_index_result import (
    repository_dedicated_index_result_issues,
)


def file_sha256(path: Path) -> str:
    if not path.is_file() or path.is_symlink():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_oid(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def repository_root_snapshot(root: Path, sandbox_name: str):
    rows = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] in (".git", sandbox_name):
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
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                )
            )
        else:
            rows.append((str(relative), "other", stat.S_IFMT(mode)))
    return tuple(rows)


def inspect_sandbox(sandbox: Path, entries, max_total_bytes: int):
    if not sandbox.is_dir() or sandbox.is_symlink():
        return False, False, False, 0
    expected = {entry.path: entry for entry in entries}
    actual_names = set()
    files_exact = True
    modes_exact = True
    total_bytes = 0
    for path in sandbox.iterdir():
        actual_names.add(path.name)
        if path.name not in expected or path.is_symlink() or not path.is_file():
            files_exact = False
            modes_exact = False
            continue
        payload = path.read_bytes()
        total_bytes += len(payload)
        entry = expected[path.name]
        if git_blob_oid(payload) != entry.blob_oid:
            files_exact = False
        actual_exec = bool(path.stat().st_mode & stat.S_IXUSR)
        expected_exec = entry.mode == "100755"
        if actual_exec != expected_exec:
            modes_exact = False
    no_extra = actual_names == set(expected)
    if total_bytes > max_total_bytes:
        files_exact = False
    return files_exact, modes_exact, no_extra, total_bytes


def validate_upstream_binding(request, v122_request, v122_result):
    v122_request_valid = not repository_dedicated_index_request_issues(v122_request)
    v122_result_valid = not repository_dedicated_index_result_issues(v122_result)
    v122_accepted = bool(
        v122_result_valid
        and v122_result.status in (INDEX_MATERIALIZED, INDEX_REUSED)
        and v122_result.dedicated_index_present_after
        and v122_result.index_entries_exact
        and v122_result.canonical_index_unchanged
        and not v122_result.current_object_database_write_performed
        and not v122_result.current_reference_write_performed
        and not v122_result.working_tree_write_performed
        and not v122_result.reflog_write_performed
    )
    binding_exact = bool(
        request.repository_path_digest == v122_result.repository_path_digest
        and request.repository_id == v122_result.repository_id
        and request.git_dir_fingerprint == v122_result.git_dir_fingerprint
        and request.v122_request_digest
        == v122_request.request_digest
        == v122_result.request_digest
        and request.v122_result_digest == v122_result.result_digest
        and request.executor_id == v122_result.executor_id
        and request.dedicated_index_filename
        == v122_request.dedicated_index_filename
        == v122_result.dedicated_index_filename
        and request.tree_entries == v122_request.tree_entries
        and request.expected_tree_oid
        == v122_request.expected_tree_oid
        == v122_result.expected_tree_oid
        and request.published_commit_oid
        == v122_request.published_commit_oid
        == v122_result.published_commit_oid
    )
    return v122_request_valid, v122_result_valid, v122_accepted, binding_exact
