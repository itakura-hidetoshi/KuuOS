#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

from runtime.kuuos_repository_constructed_commit_publication_types_v1_21 import (
    COMMIT_PUBLISHED,
)
from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import (
    TREE_COMMIT_MATERIALIZED,
    TREE_COMMIT_REUSED,
    LimitedTreeEntry,
)
from runtime.v120_tree_commit_materialization_policy import (
    repository_tree_commit_materialization_request_issues,
)
from runtime.v120_tree_commit_materialization_result import (
    repository_tree_commit_materialization_result_issues,
)
from runtime.v121_constructed_commit_publication_result import (
    repository_constructed_commit_publication_result_issues,
)


def file_sha256(path: Path) -> str:
    if not path.is_file() or path.is_symlink():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_index_entries(payload: bytes) -> tuple[LimitedTreeEntry, ...] | None:
    entries: list[LimitedTreeEntry] = []
    if not payload:
        return ()
    for record in payload.split(b"\0"):
        if not record:
            continue
        try:
            metadata, encoded_path = record.split(b"\t", 1)
            mode, oid, stage = metadata.decode("ascii").split(" ")
            path = encoded_path.decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            return None
        if stage != "0":
            return None
        entries.append(LimitedTreeEntry(mode=mode, path=path, blob_oid=oid))
    return tuple(sorted(entries, key=lambda entry: entry.path.encode("utf-8")))


def validate_upstream_binding(request, v120_request, v120_result, v121_result):
    v120_request_valid = not repository_tree_commit_materialization_request_issues(
        v120_request
    )
    v120_result_valid = not repository_tree_commit_materialization_result_issues(
        v120_result
    )
    v120_accepted = bool(
        v120_result_valid
        and v120_result.status in (TREE_COMMIT_MATERIALIZED, TREE_COMMIT_REUSED)
        and v120_result.tree_present_after
        and v120_result.commit_present_after
        and v120_result.tree_type_exact
        and v120_result.commit_type_exact
        and v120_result.tree_content_exact
        and v120_result.commit_content_exact
        and not v120_result.index_write_performed
        and not v120_result.working_tree_write_performed
        and not v120_result.reflog_write_performed
    )
    v121_result_valid = not repository_constructed_commit_publication_result_issues(
        v121_result
    )
    v121_accepted = bool(
        v121_result_valid
        and v121_result.status == COMMIT_PUBLISHED
        and v121_result.reference_cas_committed
        and v121_result.observed_after_oid == v121_result.constructed_commit_oid
        and not v121_result.current_object_database_write_performed
        and not v121_result.index_write_performed
        and not v121_result.working_tree_write_performed
        and not v121_result.reflog_write_performed
    )
    binding_exact = bool(
        request.repository_path_digest == v120_result.repository_path_digest
        and request.repository_id
        == v120_result.repository_id
        == v121_result.repository_id
        and request.git_dir_fingerprint
        == v120_result.git_dir_fingerprint
        == v121_result.git_dir_fingerprint
        and request.v120_request_digest
        == v120_request.request_digest
        == v120_result.request_digest
        and request.v120_result_digest
        == v120_result.result_digest
        == v121_result.v120_result_digest
        and request.v121_result_digest == v121_result.result_digest
        and request.tree_entries == v120_request.tree_entries
        and request.expected_tree_oid
        == v120_request.expected_tree_oid
        == v120_result.expected_tree_oid
        and request.published_commit_oid
        == v120_result.expected_commit_oid
        == v121_result.constructed_commit_oid
        and request.executor_id == v121_result.executor_id
    )
    return (
        v120_request_valid,
        v120_result_valid,
        v120_accepted,
        v121_result_valid,
        v121_accepted,
        binding_exact,
    )
