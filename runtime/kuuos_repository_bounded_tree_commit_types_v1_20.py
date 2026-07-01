#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_bounded_tree_commit_v1_20"

TREE_COMMIT_MATERIALIZED = "LIVE_TREE_COMMIT_OBJECTS_MATERIALIZED"
TREE_COMMIT_REUSED = "EXACT_LIVE_TREE_COMMIT_OBJECTS_REUSED"
TREE_COMMIT_REJECTED = "LIVE_TREE_COMMIT_OBJECTS_REJECTED"
TREE_COMMIT_ERROR = "LIVE_TREE_COMMIT_OBJECTS_ERROR"

SANDBOX_MARKER_FILENAME = "kuuos-bounded-tree-commit-sandbox-v1_20"


@dataclass(frozen=True)
class RepositoryBoundedTreeCommitPolicy:
    policy_id: str
    authorized_executor_ids: tuple[str, ...]
    allowed_repository_path_digests: tuple[str, ...]
    allowed_git_executable_names: tuple[str, ...]
    max_tree_count: int
    max_total_payload_bytes: int
    max_command_timeout_seconds: int
    max_output_bytes: int
    require_certified_v093_candidate: bool
    require_committed_v118_frontier: bool
    require_exact_v119_blob_results: bool
    require_sandbox_marker: bool
    require_sha1_object_format: bool
    allow_exact_existing_object_reuse: bool
    live_tree_write_enabled: bool
    live_commit_write_enabled: bool
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


def repository_bounded_tree_commit_policy_digest(
    policy: RepositoryBoundedTreeCommitPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryBoundedTreeCommitRequest:
    operation_id: str
    repository_path: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    candidate_certificate_digest: str
    v118_result_digest: str
    v119_result_digests: tuple[str, ...]
    executor_id: str
    sandbox_marker_token: str
    expected_parent_commit_oid: str
    expected_tree_oids: tuple[str, ...]
    expected_root_tree_oid: str
    expected_commit_oid: str
    requested_at_epoch_seconds: int
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["v119_result_digests"] = list(self.v119_result_digests)
        payload["expected_tree_oids"] = list(self.expected_tree_oids)
        return payload


def repository_bounded_tree_commit_request_digest(
    request: RepositoryBoundedTreeCommitRequest,
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
class RepositoryBoundedTreeCommitResult:
    operation_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    candidate_certificate_digest: str
    v119_result_digests: tuple[str, ...]
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    executor_id: str
    expected_tree_oids: tuple[str, ...]
    observed_tree_oids: tuple[str, ...]
    expected_root_tree_oid: str
    observed_root_tree_oid: str
    expected_commit_oid: str
    observed_commit_oid: str
    policy_valid: bool
    request_valid: bool
    candidate_valid: bool
    request_binding_exact: bool
    v119_results_valid: bool
    blob_result_coverage_exact: bool
    executor_authorized: bool
    repository_path_allowed: bool
    sandbox_marker_present: bool
    sandbox_marker_exact: bool
    object_format_sha1: bool
    parent_commit_present: bool
    parent_commit_type_exact: bool
    referenced_objects_present: bool
    referenced_object_types_exact: bool
    tree_payloads_exact: bool
    commit_payload_exact: bool
    tree_objects_present_after: bool
    commit_object_present_after: bool
    tree_objects_type_exact: bool
    commit_object_type_exact: bool
    tree_objects_content_exact: bool
    commit_object_content_exact: bool
    tree_write_count: int
    commit_write_count: int
    tree_reuse_count: int
    commit_reused: bool
    object_database_write_performed: bool
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
        payload["v119_result_digests"] = list(self.v119_result_digests)
        payload["expected_tree_oids"] = list(self.expected_tree_oids)
        payload["observed_tree_oids"] = list(self.observed_tree_oids)
        payload["command_receipts"] = [
            receipt.to_dict() for receipt in self.command_receipts
        ]
        return payload


def repository_bounded_tree_commit_result_digest(
    result: RepositoryBoundedTreeCommitResult,
) -> str:
    payload = result.to_dict()
    payload.pop("result_digest", None)
    return canonical_digest(payload)
