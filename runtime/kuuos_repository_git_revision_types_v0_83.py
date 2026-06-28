#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_git_revision_adapter_v0_83"


@dataclass(frozen=True)
class GitRevisionObservation:
    repository_label: str
    parent_commit_sha: str
    current_commit_sha: str
    current_parent_shas: tuple[str, ...]
    changed_paths: tuple[str, ...]
    inventory_paths: tuple[str, ...]
    parent_snapshot_digest: str
    current_snapshot_digest: str
    object_database_read: bool
    working_tree_read: bool
    observation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def git_revision_observation_digest(
    observation: GitRevisionObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("observation_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class GitRevisionAdapterReceipt:
    mode: str
    observation_digest: str
    chain_record_digest: str
    parent_relation_verified: bool
    changed_paths_exact: bool
    snapshots_from_object_database: bool
    working_tree_ignored: bool
    external_approval_required: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def git_revision_adapter_receipt_digest(
    receipt: GitRevisionAdapterReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
