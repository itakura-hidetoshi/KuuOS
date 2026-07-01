#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re

from runtime.kuuos_repository_checkpoint_live_ref_cas_types_v1_18 import (
    RepositoryCheckpointLiveRefCasRequest,
)
from runtime.kuuos_repository_constructed_commit_publication_types_v1_21 import (
    RepositoryConstructedCommitPublicationPolicy,
    RepositoryConstructedCommitPublicationRequest,
    repository_constructed_commit_publication_policy_digest,
    repository_constructed_commit_publication_request_digest,
)
from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import (
    RepositoryTreeCommitMaterializationResult,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_CHECKPOINT_REF = re.compile(r"^refs/kuuos/checkpoints/[A-Za-z0-9._/-]+$")


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def _valid_checkpoint_reference(value: str) -> bool:
    return bool(
        _CHECKPOINT_REF.fullmatch(value)
        and ".." not in value
        and "//" not in value
        and not value.endswith("/")
        and "\x00" not in value
    )


def _valid_oid(value: str) -> bool:
    return bool(_HEX40.fullmatch(value) and value != "0" * 40)


def build_repository_constructed_commit_publication_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    allowed_repository_path_digests: tuple[str, ...],
) -> RepositoryConstructedCommitPublicationPolicy:
    policy = RepositoryConstructedCommitPublicationPolicy(
        policy_id=policy_id,
        authorized_executor_ids=_canonical(authorized_executor_ids),
        allowed_repository_path_digests=_canonical(
            allowed_repository_path_digests
        ),
        require_valid_v120_result=True,
        require_exact_constructed_commit_binding=True,
        require_valid_v118_request=True,
        require_exact_v118_request_binding=True,
        live_reference_update_enabled=True,
        allow_object_database_write=False,
        allow_index_write=False,
        allow_working_tree_write=False,
        allow_reflog_write=False,
        allow_force_update=False,
        allow_reference_delete=False,
        allow_head_update=False,
        allow_branch_update=False,
        allow_tag_update=False,
        allow_remote_reference_update=False,
        allow_push=False,
        allow_signing=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_constructed_commit_publication_policy_digest(
            policy
        ),
    )
    issues = repository_constructed_commit_publication_policy_issues(policy)
    if issues:
        raise ValueError(f"constructed_commit_publication_policy_invalid:{issues[0]}")
    return policy


def repository_constructed_commit_publication_policy_issues(
    policy: RepositoryConstructedCommitPublicationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("constructed_commit_publication_policy_id_missing")
    if policy.authorized_executor_ids != _canonical(
        policy.authorized_executor_ids
    ) or not policy.authorized_executor_ids:
        issues.append("constructed_commit_publication_executor_allowlist_invalid")
    if policy.allowed_repository_path_digests != _canonical(
        policy.allowed_repository_path_digests
    ) or not policy.allowed_repository_path_digests:
        issues.append("constructed_commit_publication_repository_allowlist_invalid")
    if any(
        not _HEX64.fullmatch(value)
        for value in policy.allowed_repository_path_digests
    ):
        issues.append("constructed_commit_publication_repository_digest_invalid")
    if not all(
        (
            policy.require_valid_v120_result,
            policy.require_exact_constructed_commit_binding,
            policy.require_valid_v118_request,
            policy.require_exact_v118_request_binding,
            policy.live_reference_update_enabled,
        )
    ):
        issues.append("constructed_commit_publication_required_guard_disabled")
    if any(
        (
            policy.allow_object_database_write,
            policy.allow_index_write,
            policy.allow_working_tree_write,
            policy.allow_reflog_write,
            policy.allow_force_update,
            policy.allow_reference_delete,
            policy.allow_head_update,
            policy.allow_branch_update,
            policy.allow_tag_update,
            policy.allow_remote_reference_update,
            policy.allow_push,
            policy.allow_signing,
        )
    ):
        issues.append("constructed_commit_publication_forbidden_capability_enabled")
    if policy.policy_digest != repository_constructed_commit_publication_policy_digest(
        policy
    ):
        issues.append("constructed_commit_publication_policy_digest_mismatch")
    return tuple(issues)


def build_repository_constructed_commit_publication_request(
    publication_id: str,
    v120_result: RepositoryTreeCommitMaterializationResult,
    live_ref_cas_request: RepositoryCheckpointLiveRefCasRequest,
    *,
    requested_at_epoch_seconds: int,
) -> RepositoryConstructedCommitPublicationRequest:
    request = RepositoryConstructedCommitPublicationRequest(
        publication_id=publication_id,
        v120_result_digest=v120_result.result_digest,
        live_ref_cas_request_digest=live_ref_cas_request.request_digest,
        repository_path_digest=v120_result.repository_path_digest,
        repository_id=v120_result.repository_id,
        git_dir_fingerprint=v120_result.git_dir_fingerprint,
        checkpoint_reference=live_ref_cas_request.checkpoint_reference,
        expected_current_oid=live_ref_cas_request.expected_current_oid,
        constructed_commit_oid=v120_result.expected_commit_oid,
        executor_id=live_ref_cas_request.executor_id,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=repository_constructed_commit_publication_request_digest(
            request
        ),
    )
    issues = repository_constructed_commit_publication_request_issues(request)
    if issues:
        raise ValueError(f"constructed_commit_publication_request_invalid:{issues[0]}")
    return request


def repository_constructed_commit_publication_request_issues(
    request: RepositoryConstructedCommitPublicationRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        request.publication_id,
        request.v120_result_digest,
        request.live_ref_cas_request_digest,
        request.repository_path_digest,
        request.repository_id,
        request.git_dir_fingerprint,
        request.checkpoint_reference,
        request.executor_id,
    )
    if any(not value for value in required):
        issues.append("constructed_commit_publication_required_field_missing")
    for digest in (
        request.v120_result_digest,
        request.live_ref_cas_request_digest,
        request.repository_path_digest,
        request.git_dir_fingerprint,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("constructed_commit_publication_digest_invalid")
            break
    if not _valid_checkpoint_reference(request.checkpoint_reference):
        issues.append("constructed_commit_publication_reference_invalid")
    if not _valid_oid(request.expected_current_oid) or not _valid_oid(
        request.constructed_commit_oid
    ):
        issues.append("constructed_commit_publication_oid_invalid")
    if request.expected_current_oid == request.constructed_commit_oid:
        issues.append("constructed_commit_publication_oid_not_distinct")
    if request.requested_at_epoch_seconds < 0:
        issues.append("constructed_commit_publication_time_invalid")
    if request.request_digest != repository_constructed_commit_publication_request_digest(
        request
    ):
        issues.append("constructed_commit_publication_request_digest_mismatch")
    return tuple(issues)
