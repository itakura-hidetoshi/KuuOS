#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import LimitedTreeEntry

VERSION = "kuuos_repository_dedicated_index_v1_22"

INDEX_MATERIALIZED = "DEDICATED_TEMPORARY_INDEX_MATERIALIZED"
INDEX_REUSED = "EXACT_DEDICATED_TEMPORARY_INDEX_REUSED"
INDEX_REJECTED = "DEDICATED_TEMPORARY_INDEX_REJECTED"
INDEX_ERROR = "DEDICATED_TEMPORARY_INDEX_ERROR"

SANDBOX_MARKER_FILENAME = "kuuos-dedicated-index-sandbox-v1_22"
INDEX_FILENAME_PREFIX = "kuuos-index-v1_22-"


@dataclass(frozen=True)
class RepositoryDedicatedIndexPolicy:
    policy_id: str
    authorized_executor_ids: tuple[str, ...]
    allowed_repository_path_digests: tuple[str, ...]
    allowed_git_executable_names: tuple[str, ...]
    max_index_entries: int
    max_index_path_bytes: int
    max_command_timeout_seconds: int
    max_output_bytes: int
    require_valid_v120_request: bool
    require_accepted_v120_result: bool
    require_accepted_v121_result: bool
    require_exact_tree_binding: bool
    require_dedicated_index_path: bool
    require_sandbox_marker: bool
    require_canonical_index_unchanged: bool
    require_exact_index_entries: bool
    allow_exact_existing_index_reuse: bool
    live_dedicated_index_write_enabled: bool
    allow_object_database_write: bool
    allow_reference_write: bool
    allow_canonical_index_write: bool
    allow_working_tree_write: bool
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


def repository_dedicated_index_policy_digest(policy: RepositoryDedicatedIndexPolicy) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryDedicatedIndexRequest:
    operation_id: str
    repository_path: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    v120_request_digest: str
    v120_result_digest: str
    v121_result_digest: str
    executor_id: str
    sandbox_marker_token: str
    dedicated_index_filename: str
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


def repository_dedicated_index_request_digest(request: RepositoryDedicatedIndexRequest) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class DedicatedIndexGitCommandReceipt:
    sequence_number: int
    operation: str
    argv: tuple[str, ...]
    cwd_digest: str
    index_path_digest: str
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


def dedicated_index_git_command_receipt_digest(receipt: DedicatedIndexGitCommandReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryDedicatedIndexResult:
    operation_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    v120_request_digest: str
    v120_result_digest: str
    v121_result_digest: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    executor_id: str
    dedicated_index_filename: str
    dedicated_index_path_digest: str
    expected_tree_oid: str
    published_commit_oid: str
    policy_valid: bool
    request_valid: bool
    v120_request_valid: bool
    v120_result_valid: bool
    v120_result_accepted: bool
    v121_result_valid: bool
    v121_result_accepted: bool
    request_binding_exact: bool
    executor_authorized: bool
    repository_path_allowed: bool
    sandbox_marker_present: bool
    sandbox_marker_exact: bool
    dedicated_index_path_exact: bool
    dedicated_index_existed_before: bool
    dedicated_index_present_after: bool
    index_entries_exact: bool
    canonical_index_unchanged: bool
    read_tree_command_attempted: bool
    read_tree_command_succeeded: bool
    verify_index_command_attempted: bool
    verify_index_command_succeeded: bool
    exact_existing_index_reused: bool
    live_git_command_invoked: bool
    live_repository_mutated: bool
    dedicated_index_write_performed: bool
    canonical_index_write_performed: bool
    current_object_database_write_performed: bool
    current_reference_write_performed: bool
    working_tree_write_performed: bool
    reflog_write_performed: bool
    push_performed: bool
    signing_performed: bool
    prior_object_database_write_performed: bool
    prior_checkpoint_reference_write_performed: bool
    command_receipts: tuple[DedicatedIndexGitCommandReceipt, ...]
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    result_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["command_receipts"] = [receipt.to_dict() for receipt in self.command_receipts]
        return payload


def repository_dedicated_index_result_digest(result: RepositoryDedicatedIndexResult) -> str:
    payload = result.to_dict()
    payload.pop("result_digest", None)
    return canonical_digest(payload)
