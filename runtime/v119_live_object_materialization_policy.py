#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import hashlib
from pathlib import Path
import re

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_checkpoint_live_ref_cas_types_v1_18 import (
    RepositoryCheckpointLiveRefCasResult,
)
from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    RepositoryLiveObjectMaterializationPolicy,
    RepositoryLiveObjectMaterializationRequest,
    repository_live_object_materialization_policy_digest,
    repository_live_object_materialization_request_digest,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def repository_path_digest(path: str | Path) -> str:
    return canonical_digest({"path": str(Path(path).expanduser().resolve())})


def git_blob_oid(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def build_repository_live_object_materialization_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    allowed_repository_path_digests: tuple[str, ...],
    max_payload_bytes: int = 65536,
    max_command_timeout_seconds: int = 10,
    max_output_bytes: int = 131072,
) -> RepositoryLiveObjectMaterializationPolicy:
    policy = RepositoryLiveObjectMaterializationPolicy(
        policy_id=policy_id,
        authorized_executor_ids=_canonical(authorized_executor_ids),
        allowed_repository_path_digests=_canonical(
            allowed_repository_path_digests
        ),
        allowed_git_executable_names=("git",),
        max_payload_bytes=max_payload_bytes,
        max_command_timeout_seconds=max_command_timeout_seconds,
        max_output_bytes=max_output_bytes,
        require_committed_v118_result=True,
        require_sandbox_marker=True,
        require_sha1_object_format=True,
        require_exact_candidate_oid=True,
        allow_exact_existing_object_reuse=True,
        live_object_database_write_enabled=True,
        allow_reference_write=False,
        allow_index_write=False,
        allow_working_tree_write=False,
        allow_reflog_write=False,
        allow_push=False,
        allow_signing=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_live_object_materialization_policy_digest(policy),
    )
    issues = repository_live_object_materialization_policy_issues(policy)
    if issues:
        raise ValueError(f"live_object_materialization_policy_invalid:{issues[0]}")
    return policy


def repository_live_object_materialization_policy_issues(
    policy: RepositoryLiveObjectMaterializationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("live_object_materialization_policy_id_missing")
    if policy.authorized_executor_ids != _canonical(
        policy.authorized_executor_ids
    ) or not policy.authorized_executor_ids:
        issues.append("live_object_materialization_executor_allowlist_invalid")
    if policy.allowed_repository_path_digests != _canonical(
        policy.allowed_repository_path_digests
    ) or not policy.allowed_repository_path_digests:
        issues.append("live_object_materialization_repository_allowlist_invalid")
    if any(
        not _HEX64.fullmatch(value)
        for value in policy.allowed_repository_path_digests
    ):
        issues.append("live_object_materialization_repository_digest_invalid")
    if policy.allowed_git_executable_names != ("git",):
        issues.append("live_object_materialization_git_allowlist_invalid")
    if min(
        policy.max_payload_bytes,
        policy.max_command_timeout_seconds,
        policy.max_output_bytes,
    ) <= 0 or policy.max_output_bytes < policy.max_payload_bytes:
        issues.append("live_object_materialization_bound_invalid")
    if not all(
        (
            policy.require_committed_v118_result,
            policy.require_sandbox_marker,
            policy.require_sha1_object_format,
            policy.require_exact_candidate_oid,
            policy.allow_exact_existing_object_reuse,
            policy.live_object_database_write_enabled,
        )
    ):
        issues.append("live_object_materialization_required_guard_disabled")
    if any(
        (
            policy.allow_reference_write,
            policy.allow_index_write,
            policy.allow_working_tree_write,
            policy.allow_reflog_write,
            policy.allow_push,
            policy.allow_signing,
        )
    ):
        issues.append("live_object_materialization_forbidden_capability_enabled")
    if policy.policy_digest != repository_live_object_materialization_policy_digest(
        policy
    ):
        issues.append("live_object_materialization_policy_digest_mismatch")
    return tuple(issues)


def build_repository_live_object_materialization_request(
    operation_id: str,
    repository_path: str,
    v118_result: RepositoryCheckpointLiveRefCasResult,
    payload: bytes,
    *,
    executor_id: str,
    sandbox_marker_token: str,
    requested_at_epoch_seconds: int,
) -> RepositoryLiveObjectMaterializationRequest:
    request = RepositoryLiveObjectMaterializationRequest(
        operation_id=operation_id,
        repository_path=repository_path,
        repository_path_digest=repository_path_digest(repository_path),
        repository_id=v118_result.repository_id,
        git_dir_fingerprint=v118_result.git_dir_fingerprint,
        v118_result_digest=v118_result.result_digest,
        executor_id=executor_id,
        sandbox_marker_token=sandbox_marker_token,
        payload_sha256=hashlib.sha256(payload).hexdigest(),
        payload_size_bytes=len(payload),
        expected_blob_oid=git_blob_oid(payload),
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=repository_live_object_materialization_request_digest(
            request
        ),
    )
    issues = repository_live_object_materialization_request_issues(request)
    if issues:
        raise ValueError(f"live_object_materialization_request_invalid:{issues[0]}")
    return request


def repository_live_object_materialization_request_issues(
    request: RepositoryLiveObjectMaterializationRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        request.operation_id,
        request.repository_path,
        request.repository_path_digest,
        request.repository_id,
        request.git_dir_fingerprint,
        request.v118_result_digest,
        request.executor_id,
        request.sandbox_marker_token,
        request.payload_sha256,
        request.expected_blob_oid,
    )
    if any(not value for value in required):
        issues.append("live_object_materialization_required_field_missing")
    if not Path(request.repository_path).is_absolute() or "\x00" in request.repository_path:
        issues.append("live_object_materialization_repository_path_invalid")
    for digest in (
        request.repository_path_digest,
        request.git_dir_fingerprint,
        request.v118_result_digest,
        request.payload_sha256,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("live_object_materialization_digest_invalid")
            break
    if not _HEX64.fullmatch(request.sandbox_marker_token):
        issues.append("live_object_materialization_marker_token_invalid")
    if request.payload_size_bytes < 0:
        issues.append("live_object_materialization_payload_size_invalid")
    if not _HEX40.fullmatch(request.expected_blob_oid):
        issues.append("live_object_materialization_blob_oid_invalid")
    if request.requested_at_epoch_seconds < 0:
        issues.append("live_object_materialization_request_time_invalid")
    if request.request_digest != repository_live_object_materialization_request_digest(
        request
    ):
        issues.append("live_object_materialization_request_digest_mismatch")
    return tuple(issues)
