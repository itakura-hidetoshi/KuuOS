#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import re

from runtime.kuuos_repository_constructed_commit_publication_types_v1_21 import (
    RepositoryConstructedCommitPublicationResult,
)
from runtime.kuuos_repository_dedicated_index_types_v1_22 import (
    INDEX_FILENAME_PREFIX,
    RepositoryDedicatedIndexPolicy,
    RepositoryDedicatedIndexRequest,
    repository_dedicated_index_policy_digest,
    repository_dedicated_index_request_digest,
)
from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import (
    RepositoryTreeCommitMaterializationRequest,
    RepositoryTreeCommitMaterializationResult,
)
from runtime.v120_tree_commit_materialization_policy import (
    canonical_tree_entries,
    limited_tree_entry_issues,
    repository_path_digest,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_SAFE_OPERATION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$")


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def dedicated_index_filename(operation_id: str) -> str:
    return f"{INDEX_FILENAME_PREFIX}{operation_id}.index"


def build_repository_dedicated_index_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    allowed_repository_path_digests: tuple[str, ...],
    max_index_entries: int = 16,
    max_index_path_bytes: int = 255,
    max_command_timeout_seconds: int = 10,
    max_output_bytes: int = 131072,
) -> RepositoryDedicatedIndexPolicy:
    policy = RepositoryDedicatedIndexPolicy(
        policy_id=policy_id,
        authorized_executor_ids=_canonical(authorized_executor_ids),
        allowed_repository_path_digests=_canonical(allowed_repository_path_digests),
        allowed_git_executable_names=("git",),
        max_index_entries=max_index_entries,
        max_index_path_bytes=max_index_path_bytes,
        max_command_timeout_seconds=max_command_timeout_seconds,
        max_output_bytes=max_output_bytes,
        require_valid_v120_request=True,
        require_accepted_v120_result=True,
        require_accepted_v121_result=True,
        require_exact_tree_binding=True,
        require_dedicated_index_path=True,
        require_sandbox_marker=True,
        require_canonical_index_unchanged=True,
        require_exact_index_entries=True,
        allow_exact_existing_index_reuse=True,
        live_dedicated_index_write_enabled=True,
        allow_object_database_write=False,
        allow_reference_write=False,
        allow_canonical_index_write=False,
        allow_working_tree_write=False,
        allow_reflog_write=False,
        allow_push=False,
        allow_signing=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_dedicated_index_policy_digest(policy),
    )
    issues = repository_dedicated_index_policy_issues(policy)
    if issues:
        raise ValueError(f"dedicated_index_policy_invalid:{issues[0]}")
    return policy


def repository_dedicated_index_policy_issues(
    policy: RepositoryDedicatedIndexPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("dedicated_index_policy_id_missing")
    if policy.authorized_executor_ids != _canonical(policy.authorized_executor_ids) or not policy.authorized_executor_ids:
        issues.append("dedicated_index_executor_allowlist_invalid")
    if policy.allowed_repository_path_digests != _canonical(policy.allowed_repository_path_digests) or not policy.allowed_repository_path_digests:
        issues.append("dedicated_index_repository_allowlist_invalid")
    if any(not _HEX64.fullmatch(value) for value in policy.allowed_repository_path_digests):
        issues.append("dedicated_index_repository_digest_invalid")
    if policy.allowed_git_executable_names != ("git",):
        issues.append("dedicated_index_git_allowlist_invalid")
    if min(
        policy.max_index_entries,
        policy.max_index_path_bytes,
        policy.max_command_timeout_seconds,
        policy.max_output_bytes,
    ) <= 0:
        issues.append("dedicated_index_bound_invalid")
    required = (
        policy.require_valid_v120_request,
        policy.require_accepted_v120_result,
        policy.require_accepted_v121_result,
        policy.require_exact_tree_binding,
        policy.require_dedicated_index_path,
        policy.require_sandbox_marker,
        policy.require_canonical_index_unchanged,
        policy.require_exact_index_entries,
        policy.allow_exact_existing_index_reuse,
        policy.live_dedicated_index_write_enabled,
    )
    if not all(required):
        issues.append("dedicated_index_required_guard_disabled")
    forbidden = (
        policy.allow_object_database_write,
        policy.allow_reference_write,
        policy.allow_canonical_index_write,
        policy.allow_working_tree_write,
        policy.allow_reflog_write,
        policy.allow_push,
        policy.allow_signing,
    )
    if any(forbidden):
        issues.append("dedicated_index_forbidden_capability_enabled")
    if policy.policy_digest != repository_dedicated_index_policy_digest(policy):
        issues.append("dedicated_index_policy_digest_mismatch")
    return tuple(issues)


def build_repository_dedicated_index_request(
    operation_id: str,
    repository_path: str,
    v120_request: RepositoryTreeCommitMaterializationRequest,
    v120_result: RepositoryTreeCommitMaterializationResult,
    v121_result: RepositoryConstructedCommitPublicationResult,
    *,
    executor_id: str,
    sandbox_marker_token: str,
    requested_at_epoch_seconds: int,
) -> RepositoryDedicatedIndexRequest:
    request = RepositoryDedicatedIndexRequest(
        operation_id=operation_id,
        repository_path=str(Path(repository_path).expanduser().resolve()),
        repository_path_digest=repository_path_digest(repository_path),
        repository_id=v120_result.repository_id,
        git_dir_fingerprint=v120_result.git_dir_fingerprint,
        v120_request_digest=v120_request.request_digest,
        v120_result_digest=v120_result.result_digest,
        v121_result_digest=v121_result.result_digest,
        executor_id=executor_id,
        sandbox_marker_token=sandbox_marker_token,
        dedicated_index_filename=dedicated_index_filename(operation_id),
        tree_entries=canonical_tree_entries(v120_request.tree_entries),
        expected_tree_oid=v120_result.expected_tree_oid,
        published_commit_oid=v121_result.constructed_commit_oid,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=repository_dedicated_index_request_digest(request),
    )
    issues = repository_dedicated_index_request_issues(request)
    if issues:
        raise ValueError(f"dedicated_index_request_invalid:{issues[0]}")
    return request


def repository_dedicated_index_request_issues(
    request: RepositoryDedicatedIndexRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        request.operation_id,
        request.repository_path,
        request.repository_path_digest,
        request.repository_id,
        request.git_dir_fingerprint,
        request.v120_request_digest,
        request.v120_result_digest,
        request.v121_result_digest,
        request.executor_id,
        request.sandbox_marker_token,
        request.dedicated_index_filename,
        request.expected_tree_oid,
        request.published_commit_oid,
    )
    if any(not value for value in required):
        issues.append("dedicated_index_required_field_missing")
    if not _SAFE_OPERATION.fullmatch(request.operation_id):
        issues.append("dedicated_index_operation_id_invalid")
    if request.dedicated_index_filename != dedicated_index_filename(request.operation_id):
        issues.append("dedicated_index_filename_invalid")
    if not Path(request.repository_path).is_absolute() or "\x00" in request.repository_path:
        issues.append("dedicated_index_repository_path_invalid")
    for digest in (
        request.repository_path_digest,
        request.git_dir_fingerprint,
        request.v120_request_digest,
        request.v120_result_digest,
        request.v121_result_digest,
        request.sandbox_marker_token,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("dedicated_index_digest_invalid")
            break
    for oid in (request.expected_tree_oid, request.published_commit_oid):
        if not _HEX40.fullmatch(oid) or oid == "0" * 40:
            issues.append("dedicated_index_oid_invalid")
            break
    if not request.tree_entries or request.tree_entries != canonical_tree_entries(request.tree_entries):
        issues.append("dedicated_index_entries_not_canonical")
    if len({entry.path for entry in request.tree_entries}) != len(request.tree_entries):
        issues.append("dedicated_index_duplicate_path")
    for entry in request.tree_entries:
        if limited_tree_entry_issues(entry, max_path_bytes=255):
            issues.append("dedicated_index_entry_invalid")
            break
    if request.requested_at_epoch_seconds < 0:
        issues.append("dedicated_index_time_invalid")
    if request.request_digest != repository_dedicated_index_request_digest(request):
        issues.append("dedicated_index_request_digest_mismatch")
    return tuple(issues)
