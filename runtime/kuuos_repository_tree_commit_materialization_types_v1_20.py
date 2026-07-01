#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_tree_commit_materialization_v1_20"

TREE_COMMIT_MATERIALIZED = "LIMITED_TREE_COMMIT_OBJECTS_MATERIALIZED"
TREE_COMMIT_REUSED = "EXACT_LIMITED_TREE_COMMIT_OBJECTS_REUSED"
TREE_COMMIT_REJECTED = "LIMITED_TREE_COMMIT_OBJECTS_REJECTED"
TREE_COMMIT_ERROR = "LIMITED_TREE_COMMIT_OBJECTS_ERROR"

SANDBOX_MARKER_FILENAME = "kuuos-tree-commit-materialization-sandbox-v1_20"


@dataclass(frozen=True)
class LimitedTreeEntry:
    mode: str
    path: str
    blob_oid: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class RepositoryTreeCommitMaterializationPolicy:
    policy_id: str
    authorized_executor_ids: tuple[str, ...]
    allowed_repository_path_digests: tuple[str, ...]
    allowed_git_executable_names: tuple[str, ...]
    max_tree_entries: int
    max_tree_path_bytes: int
    max_commit_message_bytes: int
    max_command_timeout_seconds: int
    max_output_bytes: int
    require_materialized_or_reused_v119_result: bool
    require_sandbox_marker: bool
    require_sha1_object_format: bool
    require_exact_tree_oid: bool
    require_exact_commit_oid: bool
    require_single_parent: bool
    allow_exact_existing_tree_reuse: bool
    allow_exact_existing_commit_reuse: bool
    live_object_database_write_enabled: bool
    allow_reference_write: bool
    allow_index_write: bool
    allow_working_tree_write: bool
    allow_reflog_write: bool
    allow_push: bool
    allow_signing: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["authorized_executor_ids"] = list(self.authorized_executor_ids)
        payload["allowed_repository_path_digests"] = list(
            self.allowed_repository_path_digests
        )
        payload["allowed_git_executable_names"] = list(
            self.allowed_git_executable_names
        )
        return payload


def repository_tree_commit_materialization_policy_digest(
    policy: RepositoryTreeCommitMaterializationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryTreeCommitMaterializationRequest:
    operation_id: str
    repository_path: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    v119_result_digest: str
    executor_id: str
    sandbox_marker_token: str
    tree_entries: tuple[LimitedTreeEntry, ...]
    expected_tree_oid: str
    parent_commit_oid: str
    author_name: str
    author_email: str
    committer_name: str
    committer_email: str
    commit_epoch_seconds: int
    commit_timezone: str
    commit_message_sha256: str
    commit_message_size_bytes: int
    expected_commit_oid: str
    requested_at_epoch_seconds: int
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["tree_entries"] = [entry.to_dict() for entry in self.tree_entries]
        return payload


def repository_tree_commit_materialization_request_digest(
    request: RepositoryTreeCommitMaterializationRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class TreeCommitGitCommandReceipt:
    sequence_number: int
    operation: str
    argv: tuple[str, ...]
    cwd_digest: str
    stdin_digest: str
    stdin_size_bytes: int
    return_code: int
    stdout_digest: str
    stderr_digest: str
    stdout_size_bytes: int
    stderr_size_bytes: int
    timed_out: bool
    shell_used: bool
    mutating_command: bool
    fixed_argument_shape: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["argv"] = list(self.argv)
        return payload


def tree_commit_git_command_receipt_digest(
    receipt: TreeCommitGitCommandReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryTreeCommitMaterializationResult:
    operation_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    v119_result_digest: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    executor_id: str
    expected_tree_oid: str
    candidate_tree_oid: str
    expected_commit_oid: str
    candidate_commit_oid: str
    parent_commit_oid: str
    policy_valid: bool
    request_valid: bool
    v119_result_valid: bool
    v119_result_accepted: bool
    request_binding_exact: bool
    executor_authorized: bool
    repository_path_allowed: bool
    sandbox_marker_present: bool
    sandbox_marker_exact: bool
    object_format_sha1: bool
    tree_binding_exact: bool
    commit_binding_exact: bool
    referenced_blobs_exact: bool
    parent_commit_exact: bool
    tree_existed_before: bool
    commit_existed_before: bool
    tree_present_after: bool
    commit_present_after: bool
    tree_type_exact: bool
    commit_type_exact: bool
    tree_content_exact: bool
    commit_content_exact: bool
    tree_write_command_attempted: bool
    tree_write_command_succeeded: bool
    commit_write_command_attempted: bool
    commit_write_command_succeeded: bool
    tree_object_database_write_performed: bool
    commit_object_database_write_performed: bool
    object_database_write_performed: bool
    exact_existing_tree_reused: bool
    exact_existing_commit_reused: bool
    live_git_command_invoked: bool
    live_repository_mutated: bool
    reference_write_performed: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    reflog_write_performed: bool
    push_performed: bool
    signing_performed: bool
    command_receipts: tuple[TreeCommitGitCommandReceipt, ...]
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    result_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["command_receipts"] = [
            receipt.to_dict() for receipt in self.command_receipts
        ]
        return payload


def repository_tree_commit_materialization_result_digest(
    result: RepositoryTreeCommitMaterializationResult,
) -> str:
    payload = result.to_dict()
    payload.pop("result_digest", None)
    return canonical_digest(payload)
