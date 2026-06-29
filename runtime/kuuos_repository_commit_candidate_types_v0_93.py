#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_commit_candidate_v0_93"
CANDIDATE_CERTIFIED = "REPOSITORY_COMMIT_CANDIDATE_CERTIFIED"
GIT_OBJECT_FORMAT_SHA1 = "sha1"
REGULAR_FILE_MODE = "100644"
EXECUTABLE_FILE_MODE = "100755"
SYMLINK_MODE = "120000"
GITLINK_MODE = "160000"
TREE_MODE = "40000"
LEAF_MODES = (
    REGULAR_FILE_MODE,
    EXECUTABLE_FILE_MODE,
    SYMLINK_MODE,
    GITLINK_MODE,
)


@dataclass(frozen=True)
class RepositoryCommitIdentity:
    name: str
    email: str
    timestamp: int
    timezone: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepositoryCommitCandidatePolicy:
    policy_id: str
    git_object_format: str
    max_file_count: int
    max_total_utf8_bytes: int
    default_regular_file_mode: str
    require_parent_tree_inventory: bool
    require_single_parent: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_commit_candidate_policy_digest(
    policy: RepositoryCommitCandidatePolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryParentTreeEntry:
    path: str
    mode: str
    git_object_oid: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepositoryParentTreeInventory:
    parent_commit_sha: str
    entries: tuple[RepositoryParentTreeEntry, ...]
    object_database_read: bool
    working_tree_read: bool
    inventory_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "parent_commit_sha": self.parent_commit_sha,
            "entries": [entry.to_dict() for entry in self.entries],
            "object_database_read": self.object_database_read,
            "working_tree_read": self.working_tree_read,
            "inventory_digest": self.inventory_digest,
            "version": self.version,
        }


def repository_parent_tree_inventory_digest(
    inventory: RepositoryParentTreeInventory,
) -> str:
    payload = inventory.to_dict()
    payload.pop("inventory_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryBlobCandidate:
    path: str
    mode: str
    utf8_size: int
    content_digest: str
    git_blob_oid: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositoryTreeCandidate:
    directory: str
    entry_names: tuple[str, ...]
    entry_modes: tuple[str, ...]
    entry_oids: tuple[str, ...]
    git_tree_oid: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositoryCommitCandidateCertificate:
    candidate_id: str
    status: str
    application_receipt_digest: str
    application_transaction_id: str
    parent_commit_sha: str
    parent_tree_inventory_digest: str
    final_snapshot_digest: str
    commit_policy_digest: str
    git_object_format: str
    blob_candidates: tuple[RepositoryBlobCandidate, ...]
    tree_candidates: tuple[RepositoryTreeCandidate, ...]
    root_tree_oid: str
    author: RepositoryCommitIdentity
    committer: RepositoryCommitIdentity
    message: str
    commit_payload_digest: str
    candidate_commit_oid: str
    file_count: int
    text_blob_candidate_count: int
    retained_parent_entry_count: int
    total_utf8_bytes: int
    application_receipt_valid: bool
    application_applied: bool
    application_snapshot_bound: bool
    parent_commit_bound: bool
    parent_tree_inventory_valid: bool
    parent_inventory_commit_bound: bool
    complete_parent_path_coverage: bool
    parent_modes_preserved: bool
    paths_canonical: bool
    path_topology_valid: bool
    file_count_within_policy: bool
    byte_count_within_policy: bool
    blob_candidates_exact: bool
    tree_candidates_exact: bool
    root_tree_exact: bool
    identities_valid: bool
    message_valid: bool
    commit_payload_exact: bool
    candidate_oid_exact: bool
    deterministic_candidate: bool
    object_database_write_performed: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    commit_created: bool
    reference_mutated: bool
    signing_performed: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blob_candidates"] = [item.to_dict() for item in self.blob_candidates]
        payload["tree_candidates"] = [item.to_dict() for item in self.tree_candidates]
        payload["author"] = self.author.to_dict()
        payload["committer"] = self.committer.to_dict()
        return payload


def repository_commit_candidate_certificate_digest(
    certificate: RepositoryCommitCandidateCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
