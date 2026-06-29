#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    RepositoryAtomicApplicationReceipt,
)
from runtime.kuuos_repository_commit_candidate_types_v0_93 import (
    RepositoryCommitCandidateCertificate,
    RepositoryCommitCandidatePolicy,
    RepositoryCommitIdentity,
    RepositoryParentTreeInventory,
)
from runtime.kuuos_repository_commit_candidate_v0_93 import (
    certify_repository_commit_candidate as _certify_repository_commit_candidate,
    repository_commit_candidate_certificate_issues as _base_certificate_issues,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


def certify_repository_commit_candidate(
    candidate_id: str,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    policy: RepositoryCommitCandidatePolicy,
    *,
    author: RepositoryCommitIdentity,
    committer: RepositoryCommitIdentity,
    message: str,
) -> RepositoryCommitCandidateCertificate:
    certificate = _certify_repository_commit_candidate(
        candidate_id,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        policy,
        author=author,
        committer=committer,
        message=message,
    )
    issues = repository_commit_candidate_certificate_issues(
        certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        policy,
    )
    if issues:
        raise ValueError(f"commit_candidate_certificate_invalid:{issues[0]}")
    return certificate


def repository_commit_candidate_certificate_issues(
    certificate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    policy: RepositoryCommitCandidatePolicy,
) -> tuple[str, ...]:
    return _base_certificate_issues(
        certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        policy,
    )
