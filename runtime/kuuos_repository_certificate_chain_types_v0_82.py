#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_certificate_chain_v0_82"


@dataclass(frozen=True)
class RepositoryCertificateChainRecord:
    chain_id: str
    sequence: int
    root_commit_sha: str
    parent_commit_sha: str
    current_commit_sha: str
    previous_record_digest: str
    previous_snapshot_digest: str
    current_snapshot_digest: str
    declared_changed_paths: tuple[str, ...]
    computed_changed_paths: tuple[str, ...]
    scope_delta_digest: str
    reused_scope_ids: tuple[str, ...]
    rechecked_scope_ids: tuple[str, ...]
    rechecked_certificate_digests: tuple[str, ...]
    full_recheck_performed: bool
    current_score: int
    current_normal_form_preserved: bool
    commit_shas: tuple[str, ...]
    max_chain_length: int
    external_approval_required: bool
    record_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def certificate_chain_record_digest(
    record: RepositoryCertificateChainRecord,
) -> str:
    payload = record.to_dict()
    payload.pop("record_digest", None)
    return canonical_digest(payload)
