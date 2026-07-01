#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import hashlib
from pathlib import Path
import re

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    RepositoryLiveObjectMaterializationResult,
)
from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import (
    LimitedTreeEntry,
    RepositoryTreeCommitMaterializationPolicy,
    RepositoryTreeCommitMaterializationRequest,
    repository_tree_commit_materialization_policy_digest,
    repository_tree_commit_materialization_request_digest,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_SAFE_PATH = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._'()-]*$")
_SAFE_EMAIL = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+$")
_ALLOWED_MODES = ("100644", "100755")


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def repository_path_digest(path: str | Path) -> str:
    return canonical_digest({"path": str(Path(path).expanduser().resolve())})


def canonical_tree_entries(
    entries: tuple[LimitedTreeEntry, ...],
) -> tuple[LimitedTreeEntry, ...]:
    return tuple(sorted(entries, key=lambda entry: entry.path.encode("utf-8")))


def limited_tree_payload(entries: tuple[LimitedTreeEntry, ...]) -> bytes:
    chunks: list[bytes] = []
    for entry in canonical_tree_entries(entries):
        chunks.append(entry.mode.encode("ascii"))
        chunks.append(b" ")
        chunks.append(entry.path.encode("utf-8"))
        chunks.append(b"\0")
        chunks.append(bytes.fromhex(entry.blob_oid))
    return b"".join(chunks)


def limited_tree_mktree_input(entries: tuple[LimitedTreeEntry, ...]) -> bytes:
    return b"".join(
        f"{entry.mode} blob {entry.blob_oid}\t{entry.path}\n".encode("utf-8")
        for entry in canonical_tree_entries(entries)
    )


def git_object_oid(object_type: str, payload: bytes) -> str:
    header = f"{object_type} {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def git_tree_oid(entries: tuple[LimitedTreeEntry, ...]) -> str:
    return git_object_oid("tree", limited_tree_payload(entries))


def normalize_commit_message(message: str) -> bytes:
    if "\x00" in message or "\r" in message:
        raise ValueError("tree_commit_message_invalid")
    normalized = message.rstrip("\n") + "\n"
    return normalized.encode("utf-8")


def limited_commit_payload(
    *,
    tree_oid: str,
    parent_commit_oid: str,
    author_name: str,
    author_email: str,
    committer_name: str,
    committer_email: str,
    commit_epoch_seconds: int,
    commit_timezone: str,
    message: str,
) -> bytes:
    message_bytes = normalize_commit_message(message)
    header = (
        f"tree {tree_oid}\n"
        f"parent {parent_commit_oid}\n"
        f"author {author_name} <{author_email}> {commit_epoch_seconds} {commit_timezone}\n"
        f"committer {committer_name} <{committer_email}> {commit_epoch_seconds} {commit_timezone}\n"
        "\n"
    ).encode("utf-8")
    return header + message_bytes


def git_commit_oid(**kwargs) -> str:
    return git_object_oid("commit", limited_commit_payload(**kwargs))


def build_repository_tree_commit_materialization_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    allowed_repository_path_digests: tuple[str, ...],
    max_tree_entries: int = 16,
    max_tree_path_bytes: int = 255,
    max_commit_message_bytes: int = 4096,
    max_command_timeout_seconds: int = 10,
    max_output_bytes: int = 131072,
) -> RepositoryTreeCommitMaterializationPolicy:
    policy = RepositoryTreeCommitMaterializationPolicy(
        policy_id=policy_id,
        authorized_executor_ids=_canonical(authorized_executor_ids),
        allowed_repository_path_digests=_canonical(allowed_repository_path_digests),
        allowed_git_executable_names=("git",),
        max_tree_entries=max_tree_entries,
        max_tree_path_bytes=max_tree_path_bytes,
        max_commit_message_bytes=max_commit_message_bytes,
        max_command_timeout_seconds=max_command_timeout_seconds,
        max_output_bytes=max_output_bytes,
        require_materialized_or_reused_v119_result=True,
        require_sandbox_marker=True,
        require_sha1_object_format=True,
        require_exact_tree_oid=True,
        require_exact_commit_oid=True,
        require_single_parent=True,
        allow_exact_existing_tree_reuse=True,
        allow_exact_existing_commit_reuse=True,
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
        policy_digest=repository_tree_commit_materialization_policy_digest(policy),
    )
    issues = repository_tree_commit_materialization_policy_issues(policy)
    if issues:
        raise ValueError(f"tree_commit_materialization_policy_invalid:{issues[0]}")
    return policy


def repository_tree_commit_materialization_policy_issues(
    policy: RepositoryTreeCommitMaterializationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("tree_commit_materialization_policy_id_missing")
    if policy.authorized_executor_ids != _canonical(policy.authorized_executor_ids) or not policy.authorized_executor_ids:
        issues.append("tree_commit_materialization_executor_allowlist_invalid")
    if policy.allowed_repository_path_digests != _canonical(policy.allowed_repository_path_digests) or not policy.allowed_repository_path_digests:
        issues.append("tree_commit_materialization_repository_allowlist_invalid")
    if any(not _HEX64.fullmatch(value) for value in policy.allowed_repository_path_digests):
        issues.append("tree_commit_materialization_repository_digest_invalid")
    if policy.allowed_git_executable_names != ("git",):
        issues.append("tree_commit_materialization_git_allowlist_invalid")
    if min(
        policy.max_tree_entries,
        policy.max_tree_path_bytes,
        policy.max_commit_message_bytes,
        policy.max_command_timeout_seconds,
        policy.max_output_bytes,
    ) <= 0:
        issues.append("tree_commit_materialization_bound_invalid")
    if not all(
        (
            policy.require_materialized_or_reused_v119_result,
            policy.require_sandbox_marker,
            policy.require_sha1_object_format,
            policy.require_exact_tree_oid,
            policy.require_exact_commit_oid,
            policy.require_single_parent,
            policy.allow_exact_existing_tree_reuse,
            policy.allow_exact_existing_commit_reuse,
            policy.live_object_database_write_enabled,
        )
    ):
        issues.append("tree_commit_materialization_required_guard_disabled")
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
        issues.append("tree_commit_materialization_forbidden_capability_enabled")
    if policy.policy_digest != repository_tree_commit_materialization_policy_digest(policy):
        issues.append("tree_commit_materialization_policy_digest_mismatch")
    return tuple(issues)


def limited_tree_entry_issues(
    entry: LimitedTreeEntry,
    *,
    max_path_bytes: int,
) -> tuple[str, ...]:
    issues: list[str] = []
    encoded = entry.path.encode("utf-8", errors="strict")
    if entry.mode not in _ALLOWED_MODES:
        issues.append("tree_commit_entry_mode_invalid")
    if (
        not _SAFE_PATH.fullmatch(entry.path)
        or entry.path in (".", "..")
        or len(encoded) > max_path_bytes
    ):
        issues.append("tree_commit_entry_path_invalid")
    if not _HEX40.fullmatch(entry.blob_oid):
        issues.append("tree_commit_entry_blob_oid_invalid")
    return tuple(issues)


def build_repository_tree_commit_materialization_request(
    operation_id: str,
    repository_path: str,
    v119_result: RepositoryLiveObjectMaterializationResult,
    tree_entries: tuple[LimitedTreeEntry, ...],
    parent_commit_oid: str,
    message: str,
    *,
    executor_id: str,
    sandbox_marker_token: str,
    author_name: str,
    author_email: str,
    committer_name: str,
    committer_email: str,
    commit_epoch_seconds: int,
    requested_at_epoch_seconds: int,
) -> RepositoryTreeCommitMaterializationRequest:
    entries = canonical_tree_entries(tree_entries)
    tree_oid = git_tree_oid(entries)
    message_bytes = normalize_commit_message(message)
    commit_timezone = "+0000"
    commit_oid = git_commit_oid(
        tree_oid=tree_oid,
        parent_commit_oid=parent_commit_oid,
        author_name=author_name,
        author_email=author_email,
        committer_name=committer_name,
        committer_email=committer_email,
        commit_epoch_seconds=commit_epoch_seconds,
        commit_timezone=commit_timezone,
        message=message,
    )
    request = RepositoryTreeCommitMaterializationRequest(
        operation_id=operation_id,
        repository_path=repository_path,
        repository_path_digest=repository_path_digest(repository_path),
        repository_id=v119_result.repository_id,
        git_dir_fingerprint=v119_result.git_dir_fingerprint,
        v119_result_digest=v119_result.result_digest,
        executor_id=executor_id,
        sandbox_marker_token=sandbox_marker_token,
        tree_entries=entries,
        expected_tree_oid=tree_oid,
        parent_commit_oid=parent_commit_oid,
        author_name=author_name,
        author_email=author_email,
        committer_name=committer_name,
        committer_email=committer_email,
        commit_epoch_seconds=commit_epoch_seconds,
        commit_timezone=commit_timezone,
        commit_message_sha256=hashlib.sha256(message_bytes).hexdigest(),
        commit_message_size_bytes=len(message_bytes),
        expected_commit_oid=commit_oid,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=repository_tree_commit_materialization_request_digest(request),
    )
    issues = repository_tree_commit_materialization_request_issues(request)
    if issues:
        raise ValueError(f"tree_commit_materialization_request_invalid:{issues[0]}")
    return request


def repository_tree_commit_materialization_request_issues(
    request: RepositoryTreeCommitMaterializationRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        request.operation_id,
        request.repository_path,
        request.repository_path_digest,
        request.repository_id,
        request.git_dir_fingerprint,
        request.v119_result_digest,
        request.executor_id,
        request.sandbox_marker_token,
        request.expected_tree_oid,
        request.parent_commit_oid,
        request.author_name,
        request.author_email,
        request.committer_name,
        request.committer_email,
        request.commit_message_sha256,
        request.expected_commit_oid,
    )
    if any(not value for value in required):
        issues.append("tree_commit_materialization_required_field_missing")
    if not Path(request.repository_path).is_absolute() or "\x00" in request.repository_path:
        issues.append("tree_commit_materialization_repository_path_invalid")
    for digest in (
        request.repository_path_digest,
        request.git_dir_fingerprint,
        request.v119_result_digest,
        request.sandbox_marker_token,
        request.commit_message_sha256,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("tree_commit_materialization_digest_invalid")
            break
    for oid in (
        request.expected_tree_oid,
        request.parent_commit_oid,
        request.expected_commit_oid,
    ):
        if not _HEX40.fullmatch(oid):
            issues.append("tree_commit_materialization_oid_invalid")
            break
    if not request.tree_entries or request.tree_entries != canonical_tree_entries(request.tree_entries):
        issues.append("tree_commit_materialization_entries_not_canonical")
    if len({entry.path for entry in request.tree_entries}) != len(request.tree_entries):
        issues.append("tree_commit_materialization_duplicate_path")
    for entry in request.tree_entries:
        if limited_tree_entry_issues(entry, max_path_bytes=255):
            issues.append("tree_commit_materialization_entry_invalid")
            break
    if request.expected_tree_oid != git_tree_oid(request.tree_entries):
        issues.append("tree_commit_materialization_tree_oid_mismatch")
    if not _SAFE_NAME.fullmatch(request.author_name) or not _SAFE_NAME.fullmatch(request.committer_name):
        issues.append("tree_commit_materialization_identity_name_invalid")
    if not _SAFE_EMAIL.fullmatch(request.author_email) or not _SAFE_EMAIL.fullmatch(request.committer_email):
        issues.append("tree_commit_materialization_identity_email_invalid")
    if request.commit_timezone != "+0000":
        issues.append("tree_commit_materialization_timezone_invalid")
    if min(request.commit_epoch_seconds, request.requested_at_epoch_seconds) < 0:
        issues.append("tree_commit_materialization_time_invalid")
    if request.commit_message_size_bytes <= 0:
        issues.append("tree_commit_materialization_message_size_invalid")
    if request.request_digest != repository_tree_commit_materialization_request_digest(request):
        issues.append("tree_commit_materialization_request_digest_mismatch")
    return tuple(issues)
