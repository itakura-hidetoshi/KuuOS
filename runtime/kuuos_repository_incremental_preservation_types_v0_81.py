#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_incremental_preservation_v0_81"
GLOBAL_SCOPE_ID = "repository-global-alignment-scope"


@dataclass(frozen=True)
class AlignmentScopeFingerprint:
    scope_id: str
    scope_kind: str
    manifest_path: str
    member_paths: tuple[str, ...]
    member_digests: tuple[tuple[str, str], ...]
    scope_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def alignment_scope_digest(scope: AlignmentScopeFingerprint) -> str:
    payload = scope.to_dict()
    payload.pop("scope_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class AlignmentScopeIndex:
    snapshot_digest: str
    scopes: tuple[AlignmentScopeFingerprint, ...]
    index_digest: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["scopes"] = [scope.to_dict() for scope in self.scopes]
        return payload


def alignment_scope_index_digest(index: AlignmentScopeIndex) -> str:
    payload = index.to_dict()
    payload.pop("index_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class IncrementalScopeDelta:
    previous_snapshot_digest: str
    current_snapshot_digest: str
    changed_paths: tuple[str, ...]
    added_paths: tuple[str, ...]
    removed_paths: tuple[str, ...]
    reused_scope_ids: tuple[str, ...]
    invalidated_scope_ids: tuple[str, ...]
    added_scope_ids: tuple[str, ...]
    removed_scope_ids: tuple[str, ...]
    global_scope_changed: bool
    full_recheck_required: bool
    delta_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def incremental_scope_delta_digest(delta: IncrementalScopeDelta) -> str:
    payload = delta.to_dict()
    payload.pop("delta_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class IncrementalPreservationCertificate:
    previous_snapshot_digest: str
    current_snapshot_digest: str
    previous_certificate_digest: str
    previous_score: int
    current_score: int
    delta_digest: str
    reused_scope_ids: tuple[str, ...]
    rechecked_scope_ids: tuple[str, ...]
    rechecked_certificate_digests: tuple[str, ...]
    full_recheck_performed: bool
    full_certificate_digest: str
    previous_normal_form_bound: bool
    reused_scope_digests_equal: bool
    all_rechecked_scopes_at_zero: bool
    current_normal_form_preserved: bool
    external_approval_required: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def incremental_preservation_certificate_digest(
    certificate: IncrementalPreservationCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
