#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import hashlib
import re
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_atomic_application_receipt_v0_92 import (
    repository_atomic_application_receipt_issues,
)
from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    APPLICATION_APPLIED,
    RepositoryAtomicApplicationReceipt,
)
from runtime.kuuos_repository_commit_candidate_types_v0_93 import (
    CANDIDATE_CERTIFIED,
    GIT_OBJECT_FORMAT_SHA1,
    REGULAR_FILE_MODE,
    TREE_MODE,
    RepositoryBlobCandidate,
    RepositoryCommitCandidateCertificate,
    RepositoryCommitCandidatePolicy,
    RepositoryCommitIdentity,
    RepositoryTreeCandidate,
    repository_commit_candidate_certificate_digest,
    repository_commit_candidate_policy_digest,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_TIMEZONE = re.compile(r"^[+-][0-9]{4}$")


def git_object_oid(kind: str, payload: bytes) -> str:
    if kind not in ("blob", "tree", "commit"):
        raise ValueError("git_object_kind_invalid")
    header = f"{kind} {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def git_object_payload_digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def build_repository_commit_candidate_policy(
    policy_id: str,
    *,
    max_file_count: int,
    max_total_utf8_bytes: int,
) -> RepositoryCommitCandidatePolicy:
    policy = RepositoryCommitCandidatePolicy(
        policy_id=policy_id,
        git_object_format=GIT_OBJECT_FORMAT_SHA1,
        max_file_count=max_file_count,
        max_total_utf8_bytes=max_total_utf8_bytes,
        regular_file_mode=REGULAR_FILE_MODE,
        require_complete_text_snapshot=True,
        require_single_parent=True,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_commit_candidate_policy_digest(policy),
    )
    issues = repository_commit_candidate_policy_issues(policy)
    if issues:
        raise ValueError(f"commit_candidate_policy_invalid:{issues[0]}")
    return policy


def repository_commit_candidate_policy_issues(
    policy: RepositoryCommitCandidatePolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("commit_candidate_policy_id_missing")
    if policy.git_object_format != GIT_OBJECT_FORMAT_SHA1:
        issues.append("commit_candidate_object_format_invalid")
    if policy.max_file_count <= 0 or policy.max_total_utf8_bytes <= 0:
        issues.append("commit_candidate_policy_bound_invalid")
    if policy.regular_file_mode != REGULAR_FILE_MODE:
        issues.append("commit_candidate_file_mode_invalid")
    if not policy.require_complete_text_snapshot:
        issues.append("commit_candidate_complete_snapshot_not_required")
    if not policy.require_single_parent:
        issues.append("commit_candidate_single_parent_not_required")
    if policy.policy_digest != repository_commit_candidate_policy_digest(policy):
        issues.append("commit_candidate_policy_digest_mismatch")
    return tuple(issues)


def repository_commit_identity_issues(
    identity: RepositoryCommitIdentity,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not identity.name or any(char in identity.name for char in "<>\n\r\0"):
        issues.append("commit_identity_name_invalid")
    if (
        not identity.email
        or "@" not in identity.email
        or any(char.isspace() for char in identity.email)
        or any(char in identity.email for char in "<>\n\r\0")
    ):
        issues.append("commit_identity_email_invalid")
    if identity.timestamp < 0:
        issues.append("commit_identity_timestamp_invalid")
    if not _TIMEZONE.fullmatch(identity.timezone):
        issues.append("commit_identity_timezone_invalid")
    else:
        hour = int(identity.timezone[1:3])
        minute = int(identity.timezone[3:5])
        if minute >= 60 or hour > 14 or (hour == 14 and minute != 0):
            issues.append("commit_identity_timezone_out_of_range")
    return tuple(issues)


def normalize_commit_message(message: str) -> str:
    if "\0" in message or "\r" in message:
        raise ValueError("commit_message_control_character_invalid")
    normalized = message.rstrip("\n")
    if not normalized.strip():
        raise ValueError("commit_message_empty")
    return normalized + "\n"


def repository_commit_message_issues(message: str) -> tuple[str, ...]:
    issues: list[str] = []
    if not message or not message.strip():
        issues.append("commit_message_empty")
    if "\0" in message or "\r" in message:
        issues.append("commit_message_control_character_invalid")
    if not message.endswith("\n") or message.endswith("\n\n"):
        issues.append("commit_message_not_canonical")
    return tuple(issues)


def repository_snapshot_commit_candidate_issues(
    snapshot: RepositorySnapshot,
) -> tuple[str, ...]:
    issues: list[str] = []
    paths = snapshot.all_paths
    text_paths = tuple(path for path, _ in snapshot.text_files)
    if len(paths) != len(set(paths)):
        issues.append("commit_snapshot_duplicate_path")
    if len(text_paths) != len(set(text_paths)):
        issues.append("commit_snapshot_duplicate_text_path")
    if set(paths) != set(text_paths):
        issues.append("commit_snapshot_not_complete_text_snapshot")

    canonical_paths = tuple(sorted(set(paths) | set(text_paths)))
    for path in canonical_paths:
        segments = path.split("/")
        if (
            not path
            or path.startswith("/")
            or path.endswith("/")
            or "\\" in path
            or "\0" in path
            or any(segment in ("", ".", "..") for segment in segments)
            or any("\n" in segment or "\r" in segment for segment in segments)
        ):
            issues.append("commit_snapshot_path_invalid")
            break

    path_set = set(canonical_paths)
    for path in canonical_paths:
        parts = path.split("/")
        for index in range(1, len(parts)):
            if "/".join(parts[:index]) in path_set:
                issues.append("commit_snapshot_path_topology_invalid")
                return tuple(issues)
    return tuple(issues)


def _identity_line(identity: RepositoryCommitIdentity) -> str:
    return (
        f"{identity.name} <{identity.email}> "
        f"{identity.timestamp} {identity.timezone}"
    )


def _commit_payload(
    root_tree_oid: str,
    parent_commit_sha: str,
    author: RepositoryCommitIdentity,
    committer: RepositoryCommitIdentity,
    message: str,
) -> bytes:
    text = (
        f"tree {root_tree_oid}\n"
        f"parent {parent_commit_sha}\n"
        f"author {_identity_line(author)}\n"
        f"committer {_identity_line(committer)}\n"
        "\n"
        f"{message}"
    )
    return text.encode("utf-8")


def _blob_candidates(
    snapshot: RepositorySnapshot,
    mode: str,
) -> tuple[RepositoryBlobCandidate, ...]:
    return tuple(
        RepositoryBlobCandidate(
            path=path,
            mode=mode,
            utf8_size=len(text.encode("utf-8")),
            content_digest=canonical_digest(text),
            git_blob_oid=git_object_oid("blob", text.encode("utf-8")),
        )
        for path, text in sorted(snapshot.text_files, key=lambda item: item[0])
    )


def _tree_candidates(
    blobs: tuple[RepositoryBlobCandidate, ...],
) -> tuple[tuple[RepositoryTreeCandidate, ...], str]:
    root: dict[str, Any] = {}
    for blob in blobs:
        node = root
        parts = blob.path.split("/")
        for segment in parts[:-1]:
            child = node.setdefault(segment, {})
            if not isinstance(child, dict):
                raise ValueError("commit_tree_path_topology_invalid")
            node = child
        if parts[-1] in node:
            raise ValueError("commit_tree_duplicate_entry")
        node[parts[-1]] = blob

    trees: list[RepositoryTreeCandidate] = []

    def walk(node: dict[str, Any], directory: str) -> str:
        resolved: list[tuple[str, str, str, bool]] = []
        for name, value in node.items():
            if isinstance(value, dict):
                child_directory = f"{directory}/{name}" if directory else name
                oid = walk(value, child_directory)
                resolved.append((name, TREE_MODE, oid, True))
            else:
                resolved.append((name, value.mode, value.git_blob_oid, False))
        resolved.sort(
            key=lambda item: item[0].encode("utf-8") + (b"/" if item[3] else b"")
        )
        body = b"".join(
            f"{mode} {name}\0".encode("utf-8") + bytes.fromhex(oid)
            for name, mode, oid, _ in resolved
        )
        tree_oid = git_object_oid("tree", body)
        trees.append(
            RepositoryTreeCandidate(
                directory=directory,
                entry_names=tuple(item[0] for item in resolved),
                entry_modes=tuple(item[1] for item in resolved),
                entry_oids=tuple(item[2] for item in resolved),
                git_tree_oid=tree_oid,
            )
        )
        return tree_oid

    root_oid = walk(root, "")
    return tuple(sorted(trees, key=lambda tree: tree.directory)), root_oid


def _construct_certificate(
    candidate_id: str,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    policy: RepositoryCommitCandidatePolicy,
    author: RepositoryCommitIdentity,
    committer: RepositoryCommitIdentity,
    message: str,
) -> RepositoryCommitCandidateCertificate:
    normalized_message = normalize_commit_message(message)
    blobs = _blob_candidates(snapshot, policy.regular_file_mode)
    trees, root_oid = _tree_candidates(blobs)
    commit_payload = _commit_payload(
        root_oid,
        application_receipt.source_commit_sha,
        author,
        committer,
        normalized_message,
    )
    total_bytes = sum(blob.utf8_size for blob in blobs)
    certificate = RepositoryCommitCandidateCertificate(
        candidate_id=candidate_id,
        status=CANDIDATE_CERTIFIED,
        application_receipt_digest=application_receipt.receipt_digest,
        application_transaction_id=application_receipt.transaction_id,
        parent_commit_sha=application_receipt.source_commit_sha,
        final_snapshot_digest=snapshot.digest,
        commit_policy_digest=policy.policy_digest,
        git_object_format=policy.git_object_format,
        blob_candidates=blobs,
        tree_candidates=trees,
        root_tree_oid=root_oid,
        author=author,
        committer=committer,
        message=normalized_message,
        commit_payload_digest=git_object_payload_digest(commit_payload),
        candidate_commit_oid=git_object_oid("commit", commit_payload),
        file_count=len(blobs),
        total_utf8_bytes=total_bytes,
        application_receipt_valid=True,
        application_applied=True,
        application_snapshot_bound=True,
        parent_commit_bound=True,
        snapshot_complete=True,
        paths_canonical=True,
        path_topology_valid=True,
        file_count_within_policy=len(blobs) <= policy.max_file_count,
        byte_count_within_policy=total_bytes <= policy.max_total_utf8_bytes,
        blob_candidates_exact=True,
        tree_candidates_exact=True,
        root_tree_exact=True,
        identities_valid=True,
        message_valid=True,
        commit_payload_exact=True,
        candidate_oid_exact=True,
        deterministic_candidate=True,
        object_database_write_performed=False,
        index_write_performed=False,
        working_tree_write_performed=False,
        commit_created=False,
        reference_mutated=False,
        signing_performed=False,
        certificate_digest="",
    )
    return replace(
        certificate,
        certificate_digest=repository_commit_candidate_certificate_digest(certificate),
    )


def certify_repository_commit_candidate(
    candidate_id: str,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    policy: RepositoryCommitCandidatePolicy,
    *,
    author: RepositoryCommitIdentity,
    committer: RepositoryCommitIdentity,
    message: str,
) -> RepositoryCommitCandidateCertificate:
    if not candidate_id:
        raise ValueError("commit_candidate_id_missing")
    receipt_issues = repository_atomic_application_receipt_issues(application_receipt)
    if receipt_issues:
        raise ValueError(f"atomic_application_receipt_invalid:{receipt_issues[0]}")
    if application_receipt.status != APPLICATION_APPLIED:
        raise ValueError("commit_candidate_application_not_applied")
    if not application_receipt.application_effect_committed:
        raise ValueError("commit_candidate_application_effect_not_committed")
    if application_receipt.final_snapshot_digest != snapshot.digest:
        raise ValueError("commit_candidate_snapshot_binding_mismatch")
    if not _HEX40.fullmatch(application_receipt.source_commit_sha):
        raise ValueError("commit_candidate_parent_sha_invalid")

    policy_issues = repository_commit_candidate_policy_issues(policy)
    if policy_issues:
        raise ValueError(f"commit_candidate_policy_invalid:{policy_issues[0]}")
    snapshot_issues = repository_snapshot_commit_candidate_issues(snapshot)
    if snapshot_issues:
        raise ValueError(f"commit_candidate_snapshot_invalid:{snapshot_issues[0]}")
    if len(snapshot.text_files) > policy.max_file_count:
        raise ValueError("commit_candidate_file_count_exceeds_policy")
    total_utf8_bytes = sum(
        len(text.encode("utf-8")) for _, text in snapshot.text_files
    )
    if total_utf8_bytes > policy.max_total_utf8_bytes:
        raise ValueError("commit_candidate_byte_count_exceeds_policy")

    identity_issues = (
        repository_commit_identity_issues(author)
        + repository_commit_identity_issues(committer)
    )
    if identity_issues:
        raise ValueError(f"commit_candidate_identity_invalid:{identity_issues[0]}")

    certificate = _construct_certificate(
        candidate_id,
        application_receipt,
        snapshot,
        policy,
        author,
        committer,
        message,
    )
    issues = repository_commit_candidate_certificate_issues(
        certificate,
        application_receipt,
        snapshot,
        policy,
    )
    if issues:
        raise ValueError(f"commit_candidate_certificate_invalid:{issues[0]}")
    return certificate


def repository_commit_candidate_certificate_issues(
    certificate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    policy: RepositoryCommitCandidatePolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if repository_atomic_application_receipt_issues(application_receipt):
        issues.append("commit_candidate_application_receipt_invalid")
        return tuple(issues)
    if application_receipt.status != APPLICATION_APPLIED:
        issues.append("commit_candidate_application_not_applied")
    if not application_receipt.application_effect_committed:
        issues.append("commit_candidate_application_effect_not_committed")
    if application_receipt.final_snapshot_digest != snapshot.digest:
        issues.append("commit_candidate_snapshot_binding_mismatch")
    if not _HEX40.fullmatch(application_receipt.source_commit_sha):
        issues.append("commit_candidate_parent_sha_invalid")
    if repository_commit_candidate_policy_issues(policy):
        issues.append("commit_candidate_policy_invalid")
        return tuple(issues)
    if repository_snapshot_commit_candidate_issues(snapshot):
        issues.append("commit_candidate_snapshot_invalid")
        return tuple(issues)
    if repository_commit_identity_issues(certificate.author):
        issues.append("commit_candidate_author_invalid")
    if repository_commit_identity_issues(certificate.committer):
        issues.append("commit_candidate_committer_invalid")
    if repository_commit_message_issues(certificate.message):
        issues.append("commit_candidate_message_invalid")

    try:
        expected = _construct_certificate(
            certificate.candidate_id,
            application_receipt,
            snapshot,
            policy,
            certificate.author,
            certificate.committer,
            certificate.message,
        )
    except ValueError as error:
        issues.append(str(error))
        return tuple(issues)

    if certificate.to_dict() != expected.to_dict():
        issues.append("commit_candidate_recomputation_mismatch")
    if certificate.status != CANDIDATE_CERTIFIED:
        issues.append("commit_candidate_status_invalid")

    required_true = (
        certificate.application_receipt_valid,
        certificate.application_applied,
        certificate.application_snapshot_bound,
        certificate.parent_commit_bound,
        certificate.snapshot_complete,
        certificate.paths_canonical,
        certificate.path_topology_valid,
        certificate.file_count_within_policy,
        certificate.byte_count_within_policy,
        certificate.blob_candidates_exact,
        certificate.tree_candidates_exact,
        certificate.root_tree_exact,
        certificate.identities_valid,
        certificate.message_valid,
        certificate.commit_payload_exact,
        certificate.candidate_oid_exact,
        certificate.deterministic_candidate,
    )
    if not all(required_true):
        issues.append("commit_candidate_required_invariant_false")

    if certificate.object_database_write_performed:
        issues.append("commit_candidate_object_database_write_performed")
    if certificate.index_write_performed:
        issues.append("commit_candidate_index_write_performed")
    if certificate.working_tree_write_performed:
        issues.append("commit_candidate_working_tree_write_performed")
    if certificate.commit_created:
        issues.append("commit_candidate_commit_created")
    if certificate.reference_mutated:
        issues.append("commit_candidate_reference_mutated")
    if certificate.signing_performed:
        issues.append("commit_candidate_signing_performed")
    if certificate.certificate_digest != repository_commit_candidate_certificate_digest(
        certificate
    ):
        issues.append("commit_candidate_certificate_digest_mismatch")
    return tuple(issues)
