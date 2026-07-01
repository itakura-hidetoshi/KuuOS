#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import LimitedTreeEntry

VERSION = "kuuos_repository_sandbox_worktree_v1_23"

WORKTREE_MATERIALIZED = "SANDBOX_WORKING_TREE_MATERIALIZED"
WORKTREE_REUSED = "EXACT_SANDBOX_WORKING_TREE_REUSED"
WORKTREE_REJECTED = "SANDBOX_WORKING_TREE_REJECTED"
WORKTREE_ERROR = "SANDBOX_WORKING_TREE_ERROR"

SANDBOX_MARKER_FILENAME = "kuuos-sandbox-worktree-authority-v1_23"
SANDBOX_DIRECTORY_PREFIX = ".kuuos-worktree-v1_23-"


@dataclass(frozen=True)
class RepositorySandboxWorktreePolicy:
    policy_id: str
    authorized_executor_ids: tuple[str, ...]
    allowed_repository_path_digests: tuple[str, ...]
    allowed_git_executable_names: tuple[str, ...]
    max_worktree_entries: int
    max_worktree_path_bytes: int
    max_total_file_bytes: int
    max_command_timeout_seconds: int
    max_output_bytes: int
    require_valid_v122_request: bool
    require_accepted_v122_result: bool
    require_exact_index_binding: bool
    require_dedicated_sandbox_path: bool
    require_sandbox_marker: bool
    require_exact_file_contents: bool
    require_exact_file_modes: bool
    require_no_extra_entries: bool
    require_dedicated_index_unchanged: bool
    require_canonical_index_unchanged: bool
    require_repository_root_unchanged: bool
    allow_exact_existing_sandbox_reuse: bool
    live_sandbox_worktree_write_enabled: bool
    allow_object_database_write: bool
    allow_reference_write: bool
    allow_dedicated_index_write: bool
    allow_canonical_index_write: bool
    allow_repository_root_worktree_write: bool
    allow_reflog_write: bool
    allow_push: bool
    allow_signing: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["authorized_executor_ids"] = list(self.authorized_executor_ids)
        payload["allowed_repository_path_digests"] = list(self.allowed_repository_path_digests)
        payload["allowed_git_executable_names"] = list(self.allowed_git_executable_names)
        return payload


def repository_sandbox_worktree_policy_digest(
    policy: RepositorySandboxWorktreePolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositorySandboxWorktreeRequest:
    operation_id: str
    repository_path: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    v122_request_digest: str
    v122_result_digest: str
    executor_id: str
    sandbox_marker_token: str
    dedicated_index_filename: str
    sandbox_directory_name: str
    tree_entries: tuple[LimitedTreeEntry, ...]
    expected_tree_oid: str
    published_commit_oid: str
    requested_at_epoch_seconds: int
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["tree_entries"] = [entry.to_dict() for entry in self.tree_entries]
        return payload


def repository_sandbox_worktree_request_digest(
    request: RepositorySandboxWorktreeRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class SandboxWorktreeGitCommandReceipt:
    sequence_number: int
    operation: str
    argv: tuple[str, ...]
    cwd_digest: str
    index_path_digest: str
    sandbox_path_digest: str
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


def sandbox_worktree_git_command_receipt_digest(
    receipt: SandboxWorktreeGitCommandReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositorySandboxWorktreeResult:
    operation_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    v122_request_digest: str
    v122_result_digest: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    executor_id: str
    dedicated_index_filename: str
    dedicated_index_path_digest: str
    sandbox_directory_name: str
    sandbox_path_digest: str
    expected_tree_oid: str
    published_commit_oid: str
    policy_valid: bool
    request_valid: bool
    v122_request_valid: bool
    v122_result_valid: bool
    v122_result_accepted: bool
    request_binding_exact: bool
    executor_authorized: bool
    repository_path_allowed: bool
    sandbox_marker_present: bool
    sandbox_marker_exact: bool
    dedicated_index_path_exact: bool
    dedicated_index_present: bool
    sandbox_path_exact: bool
    sandbox_existed_before: bool
    sandbox_present_after: bool
    sandbox_files_exact: bool
    sandbox_modes_exact: bool
    sandbox_has_no_extra_entries: bool
    dedicated_index_unchanged: bool
    canonical_index_unchanged: bool
    repository_root_unchanged: bool
    checkout_command_attempted: bool
    checkout_command_succeeded: bool
    exact_existing_sandbox_reused: bool
    live_git_command_invoked: bool
    live_repository_mutated: bool
    sandbox_working_tree_write_performed: bool
    repository_root_working_tree_write_performed: bool
    dedicated_index_write_performed: bool
    canonical_index_write_performed: bool
    current_object_database_write_performed: bool
    current_reference_write_performed: bool
    reflog_write_performed: bool
    push_performed: bool
    signing_performed: bool
    prior_object_database_write_performed: bool
    prior_checkpoint_reference_write_performed: bool
    prior_dedicated_index_write_performed: bool
    command_receipts: tuple[SandboxWorktreeGitCommandReceipt, ...]
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    result_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["command_receipts"] = [receipt.to_dict() for receipt in self.command_receipts]
        return payload


def repository_sandbox_worktree_result_digest(
    result: RepositorySandboxWorktreeResult,
) -> str:
    payload = result.to_dict()
    payload.pop("result_digest", None)
    return canonical_digest(payload)
