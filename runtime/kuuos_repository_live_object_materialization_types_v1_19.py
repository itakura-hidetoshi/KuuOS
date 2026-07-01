#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_live_object_materialization_v1_19"

OBJECT_MATERIALIZED = "LIVE_BLOB_OBJECT_MATERIALIZED"
OBJECT_REUSED = "EXACT_LIVE_BLOB_OBJECT_REUSED"
OBJECT_REJECTED = "LIVE_BLOB_OBJECT_REJECTED"
OBJECT_ERROR = "LIVE_BLOB_OBJECT_ERROR"

SANDBOX_MARKER_FILENAME = "kuuos-live-object-materialization-sandbox-v1_19"


@dataclass(frozen=True)
class RepositoryLiveObjectMaterializationPolicy:
    policy_id: str
    authorized_executor_ids: tuple[str, ...]
    allowed_repository_path_digests: tuple[str, ...]
    allowed_git_executable_names: tuple[str, ...]
    max_payload_bytes: int
    max_command_timeout_seconds: int
    max_output_bytes: int
    require_committed_v118_result: bool
    require_sandbox_marker: bool
    require_sha1_object_format: bool
    require_exact_candidate_oid: bool
    allow_exact_existing_object_reuse: bool
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


def repository_live_object_materialization_policy_digest(
    policy: RepositoryLiveObjectMaterializationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryLiveObjectMaterializationRequest:
    operation_id: str
    repository_path: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    v118_result_digest: str
    executor_id: str
    sandbox_marker_token: str
    payload_sha256: str
    payload_size_bytes: int
    expected_blob_oid: str
    requested_at_epoch_seconds: int
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_live_object_materialization_request_digest(
    request: RepositoryLiveObjectMaterializationRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class LiveObjectGitCommandReceipt:
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


def live_object_git_command_receipt_digest(
    receipt: LiveObjectGitCommandReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryLiveObjectMaterializationResult:
    operation_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    v118_result_digest: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    executor_id: str
    payload_sha256: str
    payload_size_bytes: int
    expected_blob_oid: str
    candidate_blob_oid: str
    observed_object_type: str
    observed_object_size_bytes: int
    observed_payload_sha256: str
    policy_valid: bool
    request_valid: bool
    payload_binding_exact: bool
    v118_result_valid: bool
    v118_result_committed: bool
    request_binding_exact: bool
    executor_authorized: bool
    repository_path_allowed: bool
    sandbox_marker_present: bool
    sandbox_marker_exact: bool
    object_format_sha1: bool
    candidate_oid_exact: bool
    object_existed_before: bool
    object_present_after: bool
    object_type_blob: bool
    object_size_exact: bool
    object_content_exact: bool
    write_command_attempted: bool
    write_command_succeeded: bool
    object_database_write_performed: bool
    exact_existing_object_reused: bool
    live_git_command_invoked: bool
    live_repository_mutated: bool
    reference_write_performed: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    reflog_write_performed: bool
    push_performed: bool
    signing_performed: bool
    command_receipts: tuple[LiveObjectGitCommandReceipt, ...]
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


def repository_live_object_materialization_result_digest(
    result: RepositoryLiveObjectMaterializationResult,
) -> str:
    payload = result.to_dict()
    payload.pop("result_digest", None)
    return canonical_digest(payload)
