#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_frontier_certificate_v0_86"


@dataclass(frozen=True)
class RepositoryFrontierCoveragePath:
    source_commit_sha: str
    frontier_commit_sha: str
    commit_shas: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositoryFrontierCertificate:
    frontier_id: str
    dag_id: str
    dag_certificate_digest: str
    chain_id: str
    root_commit_sha: str
    edge_digests: tuple[str, ...]
    frontier_commit_shas: tuple[str, ...]
    coverage_path_digests: tuple[str, ...]
    node_count: int
    frontier_count: int
    max_frontier_size: int
    source_dag_valid: bool
    source_edges_bound: bool
    exact_terminal_frontier: bool
    frontier_nonempty: bool
    frontier_antichain: bool
    all_nodes_frontier_covered: bool
    merged_ancestors_excluded: bool
    normal_form_preserved: bool
    external_approval_required: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_frontier_certificate_digest(
    certificate: RepositoryFrontierCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
