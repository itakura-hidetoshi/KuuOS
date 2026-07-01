#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import hashlib
from pathlib import Path
import re

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_bounded_tree_commit_types_v1_20 import (
    RepositoryBoundedTreeCommitPolicy,
    RepositoryBoundedTreeCommitRequest,
    repository_bounded_tree_commit_policy_digest,
    repository_bounded_tree_commit_request_digest,
)
from runtime.kuuos_repository_checkpoint_live_ref_cas_types_v1_18 import (
    RepositoryCheckpointLiveRefCasResult,
)
from runtime.kuuos_repository_commit_candidate_types_v0_93 import (
    RepositoryCommitCandidateCertificate,
    RepositoryCommitIdentity,
    RepositoryTreeCandidate,
)
from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    RepositoryLiveObjectMaterializationResult,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def repository_path_digest(path: Path) -> str:
    return canonical_digest({"path": str(path.expanduser().resolve())})


def git_object_oid(kind: str, payload: bytes) -> str:
    if kind not in ("tree", "commit"):
        raise ValueError("v120_object_kind_invalid")
    header = f"{kind} {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def tree_candidate_payload(candidate: RepositoryTreeCandidate) -> bytes:
    if not (
        len(candidate.entry_names)
        == len(candidate.entry_modes)
        == len(candidate.entry_oids)
    ):
        raise ValueError("v120_tree_candidate_shape_invalid")
    body = bytearray()
    for name, mode, oid in zip(
        candidate.entry_names,
        candidate.entry_modes,
        candidate.entry_oids,
    ):
        if not name or "/" in name or "\0" in name or not _HEX40.fullmatch(oid):
            raise ValueError("v120_tree_entry_invalid")
        body.extend(f"{mode} {name}\0".encode("utf-8"))
        body.extend(bytes.fromhex(oid))
    return bytes(body)


def _identity_line(identity: RepositoryCommitIdentity) -> str:
    return (
        f"{identity.name} <{identity.email}> "
        f"{identity.timestamp} {identity.timezone}"
    )


def commit_candidate_payload(
    candidate: RepositoryCommitCandidateCertificate,
) -> bytes:
    text = (
        f"tree {candidate.root_tree_oid}\n"
        f"parent {candidate.parent_commit_sha}\n"
        f"author {_identity_line(candidate.author)}\n"
        f"committer {_identity_line(candidate.committer)}\n"
        "\n"
        f"{candidate.message}"
    )
    return text.encode("utf-8")


def unique_tree_candidates_in_write_order(
    candidate: RepositoryCommitCandidateCertificate,
) -> tuple[RepositoryTreeCandidate, ...]:
    by_oid: dict[str, RepositoryTreeCandidate] = {}
    for tree in candidate.tree_candidates:
        payload = tree_candidate_payload(tree)
        if git_object_oid("tree", payload) != tree.git_tree_oid:
            raise ValueError("v120_tree_candidate_oid_mismatch")
        existing = by_oid.get(tree.git_tree_oid)
        if existing is not None and tree_candidate_payload(existing) != payload:
            raise ValueError("v120_tree_candidate_oid_collision")
        by_oid[tree.git_tree_oid] = tree
    return tuple(
        sorted(
            by_oid.values(),
            key=lambda tree: (-tree.directory.count("/"), -bool(tree.directory), tree.directory),
        )
    )


def build_repository_bounded_tree_commit_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    allowed_repository_path_digests: tuple[str, ...],
    max_tree_count: int = 256,
    max_total_payload_bytes: int = 8_000_000,
    max_command_timeout_seconds: int = 30,
    max_output_bytes: int = 8_000_000,
) -> RepositoryBoundedTreeCommitPolicy:
    policy = RepositoryBoundedTreeCommitPolicy(
        policy_id=policy_id,
        authorized_executor_ids=tuple(sorted(set(authorized_executor_ids))),
        allowed_repository_path_digests=tuple(
            sorted(set(allowed_repository_path_digests))
        ),
        allowed_git_executable_names=("git",),
        max_tree_count=max_tree_count,
        max_total_payload_bytes=max_total_payload_bytes,
        max_command_timeout_seconds=max_command_timeout_seconds,
        max_output_bytes=max_output_bytes,
        require_certified_v093_candidate=True,
        require_committed_v118_frontier=True,
        require_exact_v119_blob_results=True,
        require_sandbox_marker=True,
        require_sha1_object_format=True,
        allow_exact_existing_object_reuse=True,
        live_tree_write_enabled=True,
        live_commit_write_enabled=True,
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
        policy_digest=repository_bounded_tree_commit_policy_digest(policy),
    )
    issues = repository_bounded_tree_commit_policy_issues(policy)
    if issues:
        raise ValueError(f"bounded_tree_commit_policy_invalid:{issues[0]}")
    return policy


def repository_bounded_tree_commit_policy_issues(
    policy: RepositoryBoundedTreeCommitPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("v120_policy_id_missing")
    if not policy.authorized_executor_ids:
        issues.append("v120_policy_executor_allowlist_empty")
    if not policy.allowed_repository_path_digests:
        issues.append("v120_policy_repository_allowlist_empty")
    if policy.allowed_git_executable_names != ("git",):
        issues.append("v120_policy_git_executable_invalid")
    if policy.max_tree_count <= 0 or policy.max_total_payload_bytes <= 0:
        issues.append("v120_policy_payload_bound_invalid")
    if policy.max_command_timeout_seconds <= 0 or policy.max_output_bytes <= 0:
        issues.append("v120_policy_command_bound_invalid")
    required = (
        policy.require_certified_v093_candidate,
        policy.require_committed_v118_frontier,
        policy.require_exact_v119_blob_results,
        policy.require_sandbox_marker,
        policy.require_sha1_object_format,
        policy.allow_exact_existing_object_reuse,
        policy.live_tree_write_enabled,
        policy.live_commit_write_enabled,
    )
    if not all(required):
        issues.append("v120_policy_required_guard_disabled")
    forbidden = (
        policy.allow_reference_write,
        policy.allow_index_write,
        policy.allow_working_tree_write,
        policy.allow_reflog_write,
        policy.allow_push,
        policy.allow_signing,
    )
    if any(forbidden):
        issues.append("v120_policy_forbidden_effect_enabled")
    if policy.policy_digest != repository_bounded_tree_commit_policy_digest(policy):
        issues.append("v120_policy_digest_mismatch")
    return tuple(issues)


def build_repository_bounded_tree_commit_request(
    operation_id: str,
    repository_path: str,
    candidate: RepositoryCommitCandidateCertificate,
    v118_result: RepositoryCheckpointLiveRefCasResult,
    v119_results: tuple[RepositoryLiveObjectMaterializationResult, ...],
    *,
    executor_id: str,
    sandbox_marker_token: str,
    requested_at_epoch_seconds: int,
) -> RepositoryBoundedTreeCommitRequest:
    if not v119_results:
        raise ValueError("v120_v119_results_empty")
    root = Path(repository_path).expanduser().resolve()
    trees = unique_tree_candidates_in_write_order(candidate)
    request = RepositoryBoundedTreeCommitRequest(
        operation_id=operation_id,
        repository_path=str(root),
        repository_path_digest=repository_path_digest(root),
        repository_id=v118_result.repository_id,
        git_dir_fingerprint=v118_result.git_dir_fingerprint,
        candidate_certificate_digest=candidate.certificate_digest,
        v118_result_digest=v118_result.result_digest,
        v119_result_digests=tuple(
            sorted(set(result.result_digest for result in v119_results))
        ),
        executor_id=executor_id,
        sandbox_marker_token=sandbox_marker_token,
        expected_parent_commit_oid=candidate.parent_commit_sha,
        expected_tree_oids=tuple(sorted(tree.git_tree_oid for tree in trees)),
        expected_root_tree_oid=candidate.root_tree_oid,
        expected_commit_oid=candidate.candidate_commit_oid,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=repository_bounded_tree_commit_request_digest(request),
    )
    issues = repository_bounded_tree_commit_request_issues(request)
    if issues:
        raise ValueError(f"bounded_tree_commit_request_invalid:{issues[0]}")
    return request


def repository_bounded_tree_commit_request_issues(
    request: RepositoryBoundedTreeCommitRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not request.operation_id or not request.repository_path:
        issues.append("v120_request_identity_missing")
    if not _HEX64.fullmatch(request.repository_path_digest):
        issues.append("v120_request_repository_path_digest_invalid")
    if not request.repository_id or not request.git_dir_fingerprint:
        issues.append("v120_request_repository_binding_missing")
    if not _HEX64.fullmatch(request.candidate_certificate_digest):
        issues.append("v120_request_candidate_digest_invalid")
    if not _HEX64.fullmatch(request.v118_result_digest):
        issues.append("v120_request_v118_digest_invalid")
    canonical_v119 = tuple(sorted(set(request.v119_result_digests)))
    if not request.v119_result_digests or canonical_v119 != request.v119_result_digests:
        issues.append("v120_request_v119_digests_invalid")
    if any(not _HEX64.fullmatch(item) for item in request.v119_result_digests):
        issues.append("v120_request_v119_digest_invalid")
    if not request.executor_id or not _HEX64.fullmatch(request.sandbox_marker_token):
        issues.append("v120_request_executor_or_marker_invalid")
    if not _HEX40.fullmatch(request.expected_parent_commit_oid):
        issues.append("v120_request_parent_oid_invalid")
    if not request.expected_tree_oids or tuple(sorted(request.expected_tree_oids)) != request.expected_tree_oids:
        issues.append("v120_request_tree_oids_invalid")
    if any(not _HEX40.fullmatch(item) for item in request.expected_tree_oids):
        issues.append("v120_request_tree_oid_invalid")
    if not _HEX40.fullmatch(request.expected_root_tree_oid):
        issues.append("v120_request_root_tree_oid_invalid")
    if not _HEX40.fullmatch(request.expected_commit_oid):
        issues.append("v120_request_commit_oid_invalid")
    if request.requested_at_epoch_seconds < 0:
        issues.append("v120_request_timestamp_invalid")
    if request.request_digest != repository_bounded_tree_commit_request_digest(request):
        issues.append("v120_request_digest_mismatch")
    return tuple(issues)
