#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_revision_dag_v0_85"
LINEAR_EDGE = "LINEAR"
MERGE_LEFT_EDGE = "MERGE_LEFT"
MERGE_RIGHT_EDGE = "MERGE_RIGHT"


@dataclass(frozen=True)
class RepositoryRevisionDagEdge:
    parent_commit_sha: str
    child_commit_sha: str
    source_certificate_digest: str
    edge_kind: str
    parent_position: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositoryRevisionDagCertificate:
    dag_id: str
    chain_id: str
    root_commit_sha: str
    chain_record_digests: tuple[str, ...]
    merge_certificate_digests: tuple[str, ...]
    node_commit_shas: tuple[str, ...]
    edge_digests: tuple[str, ...]
    topological_commit_shas: tuple[str, ...]
    tip_commit_shas: tuple[str, ...]
    node_count: int
    edge_count: int
    max_nodes: int
    max_edges: int
    source_certificates_valid: bool
    source_reference_closure: bool
    single_root: bool
    parent_arity_valid: bool
    all_nodes_reachable: bool
    acyclic: bool
    normal_form_preserved: bool
    external_approval_required: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_revision_dag_certificate_digest(
    certificate: RepositoryRevisionDagCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
