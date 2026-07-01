#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_live_ref_cas_v1_18"

LIVE_REF_CAS_COMMITTED = "CHECKPOINT_LIVE_REF_CAS_COMMITTED"
LIVE_REF_CAS_ABORTED = "CHECKPOINT_LIVE_REF_CAS_ABORTED"
LIVE_REF_CAS_REJECTED = "CHECKPOINT_LIVE_REF_CAS_REJECTED"
LIVE_REF_CAS_ERROR = "CHECKPOINT_LIVE_REF_CAS_ERROR"

SANDBOX_MARKER_FILENAME = "kuuos-live-mutation-sandbox-v1_18"


@dataclass(frozen=True)
class RepositoryCheckpointLiveRefCasPolicy:
    policy_id: str
    authorized_executor_ids: tuple[str, ...]
    allowed_repository_path_digests: tuple[str, ...]
    allowed_git_executable_names: tuple[str, ...]
    max_preflight_age_seconds: int
    max_execution_duration_seconds: int
    max_command_timeout_seconds: int
    max_output_bytes: int
    require_ready_v117_preflight: bool
    require_preflight_recomputation: bool
    require_exact_preflight_receipt_match: bool
    require_sandbox_marker: bool
    require_atomic_update_ref: bool
    require_checkpoint_namespace: bool
    require_no_existing_target_reflog: bool
    live_reference_update_enabled: bool
    allow_force_update: bool
    allow_reference_delete: bool
    allow_head_update: bool
    allow_branch_update: bool
    allow_tag_update: bool
    allow_remote_reference_update: bool
    allow_push: bool
    allow_object_database_write: bool
    allow_index_write: bool
    allow_working_tree_write: bool
    allow_reflog_write: bool
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


def repository_checkpoint_live_ref_cas_policy_digest(
    policy: RepositoryCheckpointLiveRefCasPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointLiveRefCasRequest:
    execution_id: str
    repository_path: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    proposed_checkpoint_oid: str
    transition_result_digest: str
    preflight_policy_digest: str
    preflight_request_digest: str
    preflight_receipt_digest: str
    executor_id: str
    sandbox_marker_token: str
    requested_at_epoch_seconds: int
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_live_ref_cas_request_digest(
    request: RepositoryCheckpointLiveRefCasRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class LiveRefCasCommandReceipt:
    sequence_number: int
    operation: str
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
    mutating_command: bool
    fixed_argument_shape: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["argv"] = list(self.argv)
        return payload


def live_ref_cas_command_receipt_digest(
    receipt: LiveRefCasCommandReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointLiveRefCasResult:
    execution_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    transition_result_digest: str
    supplied_preflight_receipt_digest: str
    recomputed_preflight_receipt_digest: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    observed_before_oid: str
    proposed_checkpoint_oid: str
    observed_after_oid: str
    executor_id: str
    execution_started_at_epoch_seconds: int
    execution_completed_at_epoch_seconds: int
    policy_valid: bool
    request_valid: bool
    request_binding_exact: bool
    executor_authorized: bool
    repository_path_allowed: bool
    preflight_ready: bool
    preflight_fresh: bool
    preflight_recomputed: bool
    preflight_receipt_exact: bool
    sandbox_marker_present: bool
    sandbox_marker_exact: bool
    checkpoint_reference_valid: bool
    checkpoint_reference_direct: bool
    target_reflog_absent_before: bool
    target_reflog_absent_after: bool
    current_oid_matches_expected: bool
    proposed_object_exists: bool
    execution_duration_within_policy: bool
    no_future_evidence: bool
    update_ref_attempted: bool
    update_ref_succeeded: bool
    post_update_verified: bool
    reference_cas_committed: bool
    live_git_command_invoked: bool
    live_repository_mutated: bool
    checkpoint_reference_write_performed: bool
    object_database_write_performed: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    reflog_write_performed: bool
    force_update_performed: bool
    reference_delete_performed: bool
    head_updated: bool
    branch_updated: bool
    tag_updated: bool
    remote_reference_updated: bool
    push_performed: bool
    signing_performed: bool
    command_receipts: tuple[LiveRefCasCommandReceipt, ...]
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


def repository_checkpoint_live_ref_cas_result_digest(
    result: RepositoryCheckpointLiveRefCasResult,
) -> str:
    payload = result.to_dict()
    payload.pop("result_digest", None)
    return canonical_digest(payload)
