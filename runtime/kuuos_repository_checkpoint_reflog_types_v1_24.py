#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_reflog_v1_24"

REFLOG_RECORDED = "CHECKPOINT_REFLOG_RECORDED"
REFLOG_REUSED = "EXACT_CHECKPOINT_REFLOG_REUSED"
REFLOG_REJECTED = "CHECKPOINT_REFLOG_REJECTED"
REFLOG_ERROR = "CHECKPOINT_REFLOG_ERROR"

AUTHORITY_MARKER_FILENAME = "kuuos-checkpoint-reflog-authority-v1_24"


@dataclass(frozen=True)
class RepositoryCheckpointReflogPolicy:
    policy_id: str
    authorized_executor_ids: tuple[str, ...]
    allowed_repository_path_digests: tuple[str, ...]
    allowed_git_executable_names: tuple[str, ...]
    max_message_bytes: int
    max_command_timeout_seconds: int
    max_output_bytes: int
    require_valid_v121_request: bool
    require_accepted_v121_result: bool
    require_valid_v123_request: bool
    require_accepted_v123_result: bool
    require_exact_cross_stage_binding: bool
    require_checkpoint_namespace: bool
    require_current_ref_exact: bool
    require_old_and_new_objects_present: bool
    require_authority_marker: bool
    require_dedicated_reflog_path: bool
    require_absent_or_exact_existing_reflog: bool
    require_exact_single_entry: bool
    require_reference_unchanged: bool
    require_protected_surfaces_unchanged: bool
    allow_exact_existing_reflog_reuse: bool
    live_checkpoint_reflog_write_enabled: bool
    allow_object_database_write: bool
    allow_reference_write: bool
    allow_index_write: bool
    allow_working_tree_write: bool
    allow_other_reflog_write: bool
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


def repository_checkpoint_reflog_policy_digest(
    policy: RepositoryCheckpointReflogPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointReflogRequest:
    operation_id: str
    repository_path: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    v121_request_digest: str
    v121_result_digest: str
    v123_request_digest: str
    v123_result_digest: str
    checkpoint_reference: str
    transition_old_oid: str
    transition_new_oid: str
    executor_id: str
    authority_marker_token: str
    committer_name: str
    committer_email: str
    recorded_at_epoch_seconds: int
    timezone_offset: str
    message: str
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_reflog_request_digest(
    request: RepositoryCheckpointReflogRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class CheckpointReflogGitCommandReceipt:
    sequence_number: int
    operation: str
    argv: tuple[str, ...]
    cwd_digest: str
    environment_digest: str
    target_ref_digest: str
    target_reflog_path_digest: str
    return_code: int
    stdout_digest: str
    stderr_digest: str
    stdout_size_bytes: int
    stderr_size_bytes: int
    timed_out: bool
    shell_used: bool
    optional_locks_disabled: bool
    mutating_command: bool
    fixed_argument_shape: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["argv"] = list(self.argv)
        return payload


def checkpoint_reflog_git_command_receipt_digest(
    receipt: CheckpointReflogGitCommandReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointReflogResult:
    operation_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    v121_request_digest: str
    v121_result_digest: str
    v123_request_digest: str
    v123_result_digest: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    transition_old_oid: str
    transition_new_oid: str
    executor_id: str
    target_reflog_path_digest: str
    policy_valid: bool
    request_valid: bool
    v121_request_valid: bool
    v121_result_valid: bool
    v121_result_accepted: bool
    v123_request_valid: bool
    v123_result_valid: bool
    v123_result_accepted: bool
    cross_stage_binding_exact: bool
    executor_authorized: bool
    repository_path_allowed: bool
    checkpoint_namespace_exact: bool
    authority_marker_present: bool
    authority_marker_exact: bool
    current_ref_exact_before: bool
    current_ref_exact_after: bool
    old_object_present: bool
    new_object_present: bool
    target_reflog_path_exact: bool
    target_reflog_existed_before: bool
    target_reflog_present_after: bool
    target_reflog_entry_exact: bool
    target_reflog_single_entry: bool
    exact_existing_reflog_reused: bool
    reflog_write_command_attempted: bool
    reflog_write_command_succeeded: bool
    live_git_command_invoked: bool
    live_repository_mutated: bool
    checkpoint_reflog_write_performed: bool
    other_reflog_write_performed: bool
    current_object_database_write_performed: bool
    current_reference_write_performed: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    push_performed: bool
    signing_performed: bool
    prior_object_database_write_performed: bool
    prior_checkpoint_reference_write_performed: bool
    prior_dedicated_index_write_performed: bool
    prior_sandbox_working_tree_write_performed: bool
    command_receipts: tuple[CheckpointReflogGitCommandReceipt, ...]
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


def repository_checkpoint_reflog_result_digest(
    result: RepositoryCheckpointReflogResult,
) -> str:
    payload = result.to_dict()
    payload.pop("result_digest", None)
    return canonical_digest(payload)
