#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import re

from runtime.kuuos_repository_dedicated_index_types_v1_22 import (
    RepositoryDedicatedIndexRequest,
    RepositoryDedicatedIndexResult,
)
from runtime.kuuos_repository_sandbox_worktree_types_v1_23 import (
    SANDBOX_DIRECTORY_PREFIX,
    RepositorySandboxWorktreePolicy,
    RepositorySandboxWorktreeRequest,
    repository_sandbox_worktree_policy_digest,
    repository_sandbox_worktree_request_digest,
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


def sandbox_directory_name(operation_id: str) -> str:
    return f"{SANDBOX_DIRECTORY_PREFIX}{operation_id}"


def build_repository_sandbox_worktree_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    allowed_repository_path_digests: tuple[str, ...],
    max_worktree_entries: int = 16,
    max_worktree_path_bytes: int = 255,
    max_total_file_bytes: int = 1048576,
    max_command_timeout_seconds: int = 10,
    max_output_bytes: int = 131072,
) -> RepositorySandboxWorktreePolicy:
    policy = RepositorySandboxWorktreePolicy(
        policy_id=policy_id,
        authorized_executor_ids=_canonical(authorized_executor_ids),
        allowed_repository_path_digests=_canonical(allowed_repository_path_digests),
        allowed_git_executable_names=("git",),
        max_worktree_entries=max_worktree_entries,
        max_worktree_path_bytes=max_worktree_path_bytes,
        max_total_file_bytes=max_total_file_bytes,
        max_command_timeout_seconds=max_command_timeout_seconds,
        max_output_bytes=max_output_bytes,
        require_valid_v122_request=True,
        require_accepted_v122_result=True,
        require_exact_index_binding=True,
        require_dedicated_sandbox_path=True,
        require_sandbox_marker=True,
        require_exact_file_contents=True,
        require_exact_file_modes=True,
        require_no_extra_entries=True,
        require_dedicated_index_unchanged=True,
        require_canonical_index_unchanged=True,
        require_repository_root_unchanged=True,
        allow_exact_existing_sandbox_reuse=True,
        live_sandbox_worktree_write_enabled=True,
        allow_object_database_write=False,
        allow_reference_write=False,
        allow_dedicated_index_write=False,
        allow_canonical_index_write=False,
        allow_repository_root_worktree_write=False,
        allow_reflog_write=False,
        allow_push=False,
        allow_signing=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_sandbox_worktree_policy_digest(policy),
    )
    issues = repository_sandbox_worktree_policy_issues(policy)
    if issues:
        raise ValueError(f"sandbox_worktree_policy_invalid:{issues[0]}")
    return policy


def repository_sandbox_worktree_policy_issues(
    policy: RepositorySandboxWorktreePolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("sandbox_worktree_policy_id_missing")
    if (
        policy.authorized_executor_ids != _canonical(policy.authorized_executor_ids)
        or not policy.authorized_executor_ids
    ):
        issues.append("sandbox_worktree_executor_allowlist_invalid")
    if (
        policy.allowed_repository_path_digests
        != _canonical(policy.allowed_repository_path_digests)
        or not policy.allowed_repository_path_digests
    ):
        issues.append("sandbox_worktree_repository_allowlist_invalid")
    if any(
        not _HEX64.fullmatch(value)
        for value in policy.allowed_repository_path_digests
    ):
        issues.append("sandbox_worktree_repository_digest_invalid")
    if policy.allowed_git_executable_names != ("git",):
        issues.append("sandbox_worktree_git_allowlist_invalid")
    if min(
        policy.max_worktree_entries,
        policy.max_worktree_path_bytes,
        policy.max_total_file_bytes,
        policy.max_command_timeout_seconds,
        policy.max_output_bytes,
    ) <= 0:
        issues.append("sandbox_worktree_bound_invalid")
    required = (
        policy.require_valid_v122_request,
        policy.require_accepted_v122_result,
        policy.require_exact_index_binding,
        policy.require_dedicated_sandbox_path,
        policy.require_sandbox_marker,
        policy.require_exact_file_contents,
        policy.require_exact_file_modes,
        policy.require_no_extra_entries,
        policy.require_dedicated_index_unchanged,
        policy.require_canonical_index_unchanged,
        policy.require_repository_root_unchanged,
        policy.allow_exact_existing_sandbox_reuse,
        policy.live_sandbox_worktree_write_enabled,
    )
    if not all(required):
        issues.append("sandbox_worktree_required_guard_disabled")
    forbidden = (
        policy.allow_object_database_write,
        policy.allow_reference_write,
        policy.allow_dedicated_index_write,
        policy.allow_canonical_index_write,
        policy.allow_repository_root_worktree_write,
        policy.allow_reflog_write,
        policy.allow_push,
        policy.allow_signing,
    )
    if any(forbidden):
        issues.append("sandbox_worktree_forbidden_capability_enabled")
    if policy.policy_digest != repository_sandbox_worktree_policy_digest(policy):
        issues.append("sandbox_worktree_policy_digest_mismatch")
    return tuple(issues)


def build_repository_sandbox_worktree_request(
    operation_id: str,
    repository_path: str,
    v122_request: RepositoryDedicatedIndexRequest,
    v122_result: RepositoryDedicatedIndexResult,
    *,
    executor_id: str,
    sandbox_marker_token: str,
    requested_at_epoch_seconds: int,
) -> RepositorySandboxWorktreeRequest:
    request = RepositorySandboxWorktreeRequest(
        operation_id=operation_id,
        repository_path=str(Path(repository_path).expanduser().resolve()),
        repository_path_digest=repository_path_digest(repository_path),
        repository_id=v122_result.repository_id,
        git_dir_fingerprint=v122_result.git_dir_fingerprint,
        v122_request_digest=v122_request.request_digest,
        v122_result_digest=v122_result.result_digest,
        executor_id=executor_id,
        sandbox_marker_token=sandbox_marker_token,
        dedicated_index_filename=v122_result.dedicated_index_filename,
        sandbox_directory_name=sandbox_directory_name(operation_id),
        tree_entries=canonical_tree_entries(v122_request.tree_entries),
        expected_tree_oid=v122_result.expected_tree_oid,
        published_commit_oid=v122_result.published_commit_oid,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=repository_sandbox_worktree_request_digest(request),
    )
    issues = repository_sandbox_worktree_request_issues(request)
    if issues:
        raise ValueError(f"sandbox_worktree_request_invalid:{issues[0]}")
    return request


def repository_sandbox_worktree_request_issues(
    request: RepositorySandboxWorktreeRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        request.operation_id,
        request.repository_path,
        request.repository_path_digest,
        request.repository_id,
        request.git_dir_fingerprint,
        request.v122_request_digest,
        request.v122_result_digest,
        request.executor_id,
        request.sandbox_marker_token,
        request.dedicated_index_filename,
        request.sandbox_directory_name,
        request.expected_tree_oid,
        request.published_commit_oid,
    )
    if any(not value for value in required):
        issues.append("sandbox_worktree_required_field_missing")
    if not _SAFE_OPERATION.fullmatch(request.operation_id):
        issues.append("sandbox_worktree_operation_id_invalid")
    if request.sandbox_directory_name != sandbox_directory_name(request.operation_id):
        issues.append("sandbox_worktree_directory_name_invalid")
    if not Path(request.repository_path).is_absolute() or "\x00" in request.repository_path:
        issues.append("sandbox_worktree_repository_path_invalid")
    for digest in (
        request.repository_path_digest,
        request.git_dir_fingerprint,
        request.v122_request_digest,
        request.v122_result_digest,
        request.sandbox_marker_token,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("sandbox_worktree_digest_invalid")
            break
    for oid in (request.expected_tree_oid, request.published_commit_oid):
        if not _HEX40.fullmatch(oid) or oid == "0" * 40:
            issues.append("sandbox_worktree_oid_invalid")
            break
    if not request.tree_entries or request.tree_entries != canonical_tree_entries(request.tree_entries):
        issues.append("sandbox_worktree_entries_not_canonical")
    if len({entry.path for entry in request.tree_entries}) != len(request.tree_entries):
        issues.append("sandbox_worktree_duplicate_path")
    for entry in request.tree_entries:
        if limited_tree_entry_issues(entry, max_path_bytes=255):
            issues.append("sandbox_worktree_entry_invalid")
            break
    if request.requested_at_epoch_seconds < 0:
        issues.append("sandbox_worktree_time_invalid")
    if request.request_digest != repository_sandbox_worktree_request_digest(request):
        issues.append("sandbox_worktree_request_digest_mismatch")
    return tuple(issues)
