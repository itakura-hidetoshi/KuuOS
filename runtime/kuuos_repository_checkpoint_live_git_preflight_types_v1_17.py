#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_live_git_preflight_v1_17"

PREFLIGHT_READY = "CHECKPOINT_LIVE_GIT_PREFLIGHT_READY"
PREFLIGHT_REJECTED = "CHECKPOINT_LIVE_GIT_PREFLIGHT_REJECTED"
PREFLIGHT_ERROR = "CHECKPOINT_LIVE_GIT_PREFLIGHT_ERROR"


@dataclass(frozen=True)
class RepositoryCheckpointLiveGitPreflightPolicy:
    policy_id: str
    allowed_git_executable_names: tuple[str, ...]
    allowed_read_only_subcommands: tuple[str, ...]
    max_command_timeout_seconds: int
    max_command_count: int
    max_output_bytes: int
    require_optional_locks_disabled: bool
    require_no_shell: bool
    require_checkpoint_namespace: bool
    require_committed_v116_transition: bool
    live_git_read_only_enabled: bool
    allow_live_git_mutation: bool
    allow_object_write: bool
    allow_index_write: bool
    allow_working_tree_write: bool
    allow_reflog_write: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_git_executable_names"] = list(
            self.allowed_git_executable_names
        )
        payload["allowed_read_only_subcommands"] = list(
            self.allowed_read_only_subcommands
        )
        return payload


def repository_checkpoint_live_git_preflight_policy_digest(
    policy: RepositoryCheckpointLiveGitPreflightPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointLiveGitPreflightRequest:
    preflight_id: str
    repository_path: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    proposed_checkpoint_oid: str
    transition_result_digest: str
    requested_at_epoch_seconds: int
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_live_git_preflight_request_digest(
    request: RepositoryCheckpointLiveGitPreflightRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class LiveGitCommandReceipt:
    sequence_number: int
    argv: tuple[str, ...]
    cwd_digest: str
    return_code: int
    stdout_digest: str
    stderr_digest: str
    stdout_size_bytes: int
    stderr_size_bytes: int
    timed_out: bool
    optional_locks_disabled: bool
    shell_used: bool
    read_only_command: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["argv"] = list(self.argv)
        return payload


def live_git_command_receipt_digest(receipt: LiveGitCommandReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointLiveGitPreflightReceipt:
    preflight_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    transition_result_digest: str
    repository_path_digest: str
    resolved_repository_root_digest: str
    resolved_git_dir_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    observed_current_oid: str
    proposed_checkpoint_oid: str
    transition_valid: bool
    transition_committed: bool
    transition_binding_exact: bool
    repository_path_valid: bool
    repository_root_resolved: bool
    git_directory_resolved: bool
    repository_non_bare: bool
    checkpoint_reference_valid: bool
    checkpoint_reference_exists: bool
    checkpoint_reference_direct: bool
    observed_oid_matches_expected: bool
    expected_object_exists: bool
    proposed_object_exists: bool
    command_policy_valid: bool
    all_commands_bounded: bool
    all_commands_read_only: bool
    optional_locks_disabled: bool
    shell_used: bool
    live_git_command_invoked: bool
    live_repository_mutated: bool
    object_database_write_performed: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    reflog_write_performed: bool
    command_receipts: tuple[LiveGitCommandReceipt, ...]
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["command_receipts"] = [
            receipt.to_dict() for receipt in self.command_receipts
        ]
        return payload


def repository_checkpoint_live_git_preflight_receipt_digest(
    receipt: RepositoryCheckpointLiveGitPreflightReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
