#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import re

from runtime.kuuos_repository_checkpoint_reflog_types_v1_24 import (
    RepositoryCheckpointReflogPolicy,
    RepositoryCheckpointReflogRequest,
    repository_checkpoint_reflog_policy_digest,
    repository_checkpoint_reflog_request_digest,
)
from runtime.kuuos_repository_constructed_commit_publication_types_v1_21 import (
    RepositoryConstructedCommitPublicationRequest,
    RepositoryConstructedCommitPublicationResult,
)
from runtime.kuuos_repository_sandbox_worktree_types_v1_23 import (
    RepositorySandboxWorktreeRequest,
    RepositorySandboxWorktreeResult,
)
from runtime.v120_tree_commit_materialization_policy import repository_path_digest

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_SAFE_OPERATION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$")
_CHECKPOINT_REF = re.compile(r"^refs/kuuos/checkpoints/[A-Za-z0-9._/-]+$")
_EMAIL = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+$")
_MESSAGE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._:/()@+-]{0,159}$")


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def valid_checkpoint_reference(value: str) -> bool:
    return bool(
        _CHECKPOINT_REF.fullmatch(value)
        and ".." not in value
        and "//" not in value
        and not value.endswith("/")
        and "\x00" not in value
    )


def valid_oid(value: str) -> bool:
    return bool(_HEX40.fullmatch(value) and value != "0" * 40)


def build_repository_checkpoint_reflog_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    allowed_repository_path_digests: tuple[str, ...],
    max_message_bytes: int = 160,
    max_command_timeout_seconds: int = 10,
    max_output_bytes: int = 131072,
) -> RepositoryCheckpointReflogPolicy:
    policy = RepositoryCheckpointReflogPolicy(
        policy_id=policy_id,
        authorized_executor_ids=_canonical(authorized_executor_ids),
        allowed_repository_path_digests=_canonical(
            allowed_repository_path_digests
        ),
        allowed_git_executable_names=("git",),
        max_message_bytes=max_message_bytes,
        max_command_timeout_seconds=max_command_timeout_seconds,
        max_output_bytes=max_output_bytes,
        require_valid_v121_request=True,
        require_accepted_v121_result=True,
        require_valid_v123_request=True,
        require_accepted_v123_result=True,
        require_exact_cross_stage_binding=True,
        require_checkpoint_namespace=True,
        require_current_ref_exact=True,
        require_old_and_new_objects_present=True,
        require_authority_marker=True,
        require_dedicated_reflog_path=True,
        require_absent_or_exact_existing_reflog=True,
        require_exact_single_entry=True,
        require_reference_unchanged=True,
        require_protected_surfaces_unchanged=True,
        allow_exact_existing_reflog_reuse=True,
        live_checkpoint_reflog_write_enabled=True,
        allow_object_database_write=False,
        allow_reference_write=False,
        allow_index_write=False,
        allow_working_tree_write=False,
        allow_other_reflog_write=False,
        allow_push=False,
        allow_signing=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_reflog_policy_digest(policy),
    )
    issues = repository_checkpoint_reflog_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_reflog_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_reflog_policy_issues(
    policy: RepositoryCheckpointReflogPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_reflog_policy_id_missing")
    if (
        policy.authorized_executor_ids
        != _canonical(policy.authorized_executor_ids)
        or not policy.authorized_executor_ids
    ):
        issues.append("checkpoint_reflog_executor_allowlist_invalid")
    if (
        policy.allowed_repository_path_digests
        != _canonical(policy.allowed_repository_path_digests)
        or not policy.allowed_repository_path_digests
    ):
        issues.append("checkpoint_reflog_repository_allowlist_invalid")
    if any(
        not _HEX64.fullmatch(value)
        for value in policy.allowed_repository_path_digests
    ):
        issues.append("checkpoint_reflog_repository_digest_invalid")
    if policy.allowed_git_executable_names != ("git",):
        issues.append("checkpoint_reflog_git_allowlist_invalid")
    if min(
        policy.max_message_bytes,
        policy.max_command_timeout_seconds,
        policy.max_output_bytes,
    ) <= 0:
        issues.append("checkpoint_reflog_bound_invalid")
    required = (
        policy.require_valid_v121_request,
        policy.require_accepted_v121_result,
        policy.require_valid_v123_request,
        policy.require_accepted_v123_result,
        policy.require_exact_cross_stage_binding,
        policy.require_checkpoint_namespace,
        policy.require_current_ref_exact,
        policy.require_old_and_new_objects_present,
        policy.require_authority_marker,
        policy.require_dedicated_reflog_path,
        policy.require_absent_or_exact_existing_reflog,
        policy.require_exact_single_entry,
        policy.require_reference_unchanged,
        policy.require_protected_surfaces_unchanged,
        policy.allow_exact_existing_reflog_reuse,
        policy.live_checkpoint_reflog_write_enabled,
    )
    if not all(required):
        issues.append("checkpoint_reflog_required_guard_disabled")
    forbidden = (
        policy.allow_object_database_write,
        policy.allow_reference_write,
        policy.allow_index_write,
        policy.allow_working_tree_write,
        policy.allow_other_reflog_write,
        policy.allow_push,
        policy.allow_signing,
    )
    if any(forbidden):
        issues.append("checkpoint_reflog_forbidden_capability_enabled")
    if policy.policy_digest != repository_checkpoint_reflog_policy_digest(policy):
        issues.append("checkpoint_reflog_policy_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_reflog_request(
    operation_id: str,
    repository_path: str,
    v121_request: RepositoryConstructedCommitPublicationRequest,
    v121_result: RepositoryConstructedCommitPublicationResult,
    v123_request: RepositorySandboxWorktreeRequest,
    v123_result: RepositorySandboxWorktreeResult,
    *,
    executor_id: str,
    authority_marker_token: str,
    committer_name: str,
    committer_email: str,
    recorded_at_epoch_seconds: int,
    message: str,
) -> RepositoryCheckpointReflogRequest:
    request = RepositoryCheckpointReflogRequest(
        operation_id=operation_id,
        repository_path=str(Path(repository_path).expanduser().resolve()),
        repository_path_digest=repository_path_digest(repository_path),
        repository_id=v121_result.repository_id,
        git_dir_fingerprint=v121_result.git_dir_fingerprint,
        v121_request_digest=v121_request.request_digest,
        v121_result_digest=v121_result.result_digest,
        v123_request_digest=v123_request.request_digest,
        v123_result_digest=v123_result.result_digest,
        checkpoint_reference=v121_result.checkpoint_reference,
        transition_old_oid=v121_result.expected_current_oid,
        transition_new_oid=v121_result.constructed_commit_oid,
        executor_id=executor_id,
        authority_marker_token=authority_marker_token,
        committer_name=committer_name,
        committer_email=committer_email,
        recorded_at_epoch_seconds=recorded_at_epoch_seconds,
        timezone_offset="+0000",
        message=message,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=repository_checkpoint_reflog_request_digest(request),
    )
    issues = repository_checkpoint_reflog_request_issues(request)
    if issues:
        raise ValueError(f"checkpoint_reflog_request_invalid:{issues[0]}")
    return request


def repository_checkpoint_reflog_request_issues(
    request: RepositoryCheckpointReflogRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        request.operation_id,
        request.repository_path,
        request.repository_path_digest,
        request.repository_id,
        request.git_dir_fingerprint,
        request.v121_request_digest,
        request.v121_result_digest,
        request.v123_request_digest,
        request.v123_result_digest,
        request.checkpoint_reference,
        request.transition_old_oid,
        request.transition_new_oid,
        request.executor_id,
        request.authority_marker_token,
        request.committer_name,
        request.committer_email,
        request.timezone_offset,
        request.message,
    )
    if any(not value for value in required):
        issues.append("checkpoint_reflog_required_field_missing")
    if not _SAFE_OPERATION.fullmatch(request.operation_id):
        issues.append("checkpoint_reflog_operation_id_invalid")
    if not Path(request.repository_path).is_absolute() or "\x00" in request.repository_path:
        issues.append("checkpoint_reflog_repository_path_invalid")
    for digest in (
        request.repository_path_digest,
        request.git_dir_fingerprint,
        request.v121_request_digest,
        request.v121_result_digest,
        request.v123_request_digest,
        request.v123_result_digest,
        request.authority_marker_token,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("checkpoint_reflog_digest_invalid")
            break
    if not valid_checkpoint_reference(request.checkpoint_reference):
        issues.append("checkpoint_reflog_reference_invalid")
    if not valid_oid(request.transition_old_oid) or not valid_oid(
        request.transition_new_oid
    ):
        issues.append("checkpoint_reflog_oid_invalid")
    if request.transition_old_oid == request.transition_new_oid:
        issues.append("checkpoint_reflog_oid_not_distinct")
    if (
        len(request.committer_name.encode("utf-8")) > 80
        or any(ch in request.committer_name for ch in "<>\x00\r\n")
        or request.committer_name.strip() != request.committer_name
    ):
        issues.append("checkpoint_reflog_committer_name_invalid")
    if (
        len(request.committer_email.encode("ascii", errors="ignore")) > 160
        or not _EMAIL.fullmatch(request.committer_email)
        or ".." in request.committer_email
    ):
        issues.append("checkpoint_reflog_committer_email_invalid")
    if request.timezone_offset != "+0000":
        issues.append("checkpoint_reflog_timezone_invalid")
    if (
        not _MESSAGE.fullmatch(request.message)
        or request.message.strip() != request.message
        or "  " in request.message
    ):
        issues.append("checkpoint_reflog_message_invalid")
    if request.recorded_at_epoch_seconds < 0:
        issues.append("checkpoint_reflog_time_invalid")
    if request.request_digest != repository_checkpoint_reflog_request_digest(
        request
    ):
        issues.append("checkpoint_reflog_request_digest_mismatch")
    return tuple(issues)
