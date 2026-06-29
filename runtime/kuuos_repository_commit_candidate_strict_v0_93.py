#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    RepositoryAtomicApplicationReceipt,
)
from runtime.kuuos_repository_commit_candidate_types_v0_93 import (
    RepositoryCommitCandidateCertificate,
    RepositoryCommitCandidatePolicy,
    RepositoryCommitIdentity,
)
from runtime.kuuos_repository_commit_candidate_v0_93 import (
    certify_repository_commit_candidate as _certify_repository_commit_candidate,
    repository_commit_candidate_certificate_issues as _base_certificate_issues,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


def _snapshot_utf8_size(snapshot: RepositorySnapshot) -> int:
    return sum(len(text.encode("utf-8")) for _, text in snapshot.text_files)


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
    if len(snapshot.text_files) > policy.max_file_count:
        raise ValueError("commit_candidate_file_count_exceeds_policy")
    if _snapshot_utf8_size(snapshot) > policy.max_total_utf8_bytes:
        raise ValueError("commit_candidate_byte_count_exceeds_policy")
    certificate = _certify_repository_commit_candidate(
        candidate_id,
        application_receipt,
        snapshot,
        policy,
        author=author,
        committer=committer,
        message=message,
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
    issues = list(
        _base_certificate_issues(
            certificate,
            application_receipt,
            snapshot,
            policy,
        )
    )
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
    return tuple(issues)
