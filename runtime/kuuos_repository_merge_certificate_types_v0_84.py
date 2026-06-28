#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_merge_certificate_v0_84"


@dataclass(frozen=True)
class RepositoryMergeObservation:
    repository_label: str
    left_parent_sha: str
    right_parent_sha: str
    merge_commit_sha: str
    merge_parent_shas: tuple[str, ...]
    left_changed_paths: tuple[str, ...]
    right_changed_paths: tuple[str, ...]
    union_changed_paths: tuple[str, ...]
    overlapping_changed_paths: tuple[str, ...]
    inventory_paths: tuple[str, ...]
    left_snapshot_digest: str
    right_snapshot_digest: str
    merge_snapshot_digest: str
    object_database_read: bool
    working_tree_read: bool
    observation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_merge_observation_digest(
    observation: RepositoryMergeObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("observation_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryMergeCertificate:
    merge_id: str
    chain_id: str
    root_commit_sha: str
    fork_commit_sha: str
    left_record_digest: str
    right_record_digest: str
    left_commit_sha: str
    right_commit_sha: str
    merge_commit_sha: str
    observation_digest: str
    merge_normal_form_certificate_digest: str
    merge_score: int
    common_prefix_length: int
    left_suffix_commit_shas: tuple[str, ...]
    right_suffix_commit_shas: tuple[str, ...]
    parent_order_exact: bool
    branch_histories_disjoint_after_fork: bool
    changed_paths_disjoint: bool
    merge_normal_form_preserved: bool
    external_approval_required: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_merge_certificate_digest(
    certificate: RepositoryMergeCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
