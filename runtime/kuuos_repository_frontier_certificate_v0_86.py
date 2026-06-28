#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from runtime.kuuos_repository_frontier_certificate_types_v0_86 import (
    RepositoryFrontierCertificate,
    RepositoryFrontierCoveragePath,
    repository_frontier_certificate_digest,
)
from runtime.kuuos_repository_revision_dag_types_v0_85 import (
    RepositoryRevisionDagCertificate,
    RepositoryRevisionDagEdge,
)
from runtime.kuuos_repository_revision_dag_v0_85 import (
    repository_revision_dag_certificate_issues,
)


def repository_frontier_certificate_issues(
    certificate: RepositoryFrontierCertificate,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not certificate.frontier_id:
        issues.append("frontier_id_missing")
    if not certificate.dag_id:
        issues.append("dag_id_missing")
    if not certificate.dag_certificate_digest:
        issues.append("dag_certificate_digest_missing")
    if not certificate.chain_id:
        issues.append("chain_id_missing")
    if not certificate.root_commit_sha:
        issues.append("root_commit_missing")
    if certificate.certificate_digest != repository_frontier_certificate_digest(
        certificate
    ):
        issues.append("certificate_digest_mismatch")
    if certificate.frontier_count != len(certificate.frontier_commit_shas):
        issues.append("frontier_count_mismatch")
    if certificate.node_count != len(certificate.coverage_path_digests):
        issues.append("coverage_path_count_mismatch")
    if certificate.frontier_count > certificate.max_frontier_size:
        issues.append("frontier_bound_exceeded")
    if tuple(sorted(set(certificate.edge_digests))) != certificate.edge_digests:
        issues.append("edge_digests_not_canonical")
    if tuple(sorted(set(certificate.frontier_commit_shas))) != (
        certificate.frontier_commit_shas
    ):
        issues.append("frontier_commits_not_canonical")
    if len(set(certificate.coverage_path_digests)) != len(
        certificate.coverage_path_digests
    ):
        issues.append("coverage_path_replay_detected")
    for field_name, valid in (
        ("source_dag_invalid", certificate.source_dag_valid),
        ("source_edges_not_bound", certificate.source_edges_bound),
        ("terminal_frontier_not_exact", certificate.exact_terminal_frontier),
        ("frontier_empty", certificate.frontier_nonempty),
        ("frontier_not_antichain", certificate.frontier_antichain),
        ("node_not_frontier_covered", certificate.all_nodes_frontier_covered),
        ("merged_ancestor_retained", certificate.merged_ancestors_excluded),
        ("normal_form_not_preserved", certificate.normal_form_preserved),
    ):
        if not valid:
            issues.append(field_name)
    if certificate.external_approval_required:
        issues.append("unexpected_external_approval")
    return tuple(issues)


def _canonical_edges(
    edges: Iterable[RepositoryRevisionDagEdge],
) -> tuple[RepositoryRevisionDagEdge, ...]:
    return tuple(sorted(
        edges,
        key=lambda edge: (
            edge.child_commit_sha,
            edge.parent_position,
            edge.parent_commit_sha,
            edge.source_certificate_digest,
        ),
    ))


def _canonical_coverage_paths(
    nodes: tuple[str, ...],
    topological: tuple[str, ...],
    children: dict[str, tuple[str, ...]],
    frontier: tuple[str, ...],
) -> tuple[RepositoryFrontierCoveragePath, ...]:
    frontier_set = set(frontier)
    best_path: dict[str, tuple[str, ...]] = {}
    for node in reversed(topological):
        if node in frontier_set:
            best_path[node] = (node,)
            continue
        candidates = [
            (node,) + best_path[child]
            for child in children[node]
            if child in best_path
        ]
        if not candidates:
            raise ValueError("frontier_coverage_missing")
        best_path[node] = min(candidates, key=lambda path: (len(path), path))

    paths: list[RepositoryFrontierCoveragePath] = []
    for node in nodes:
        path = best_path.get(node)
        if path is None:
            raise ValueError("frontier_coverage_missing")
        paths.append(RepositoryFrontierCoveragePath(node, path[-1], path))
    return tuple(paths)


def certify_repository_frontier(
    frontier_id: str,
    edges: Iterable[RepositoryRevisionDagEdge],
    dag_certificate: RepositoryRevisionDagCertificate,
    max_frontier_size: int = 4096,
) -> tuple[tuple[RepositoryFrontierCoveragePath, ...], RepositoryFrontierCertificate]:
    if not frontier_id:
        raise ValueError("frontier_id_missing")
    if max_frontier_size <= 0:
        raise ValueError("max_frontier_size_invalid")

    source_issues = repository_revision_dag_certificate_issues(dag_certificate)
    if source_issues:
        raise ValueError(f"revision_dag_certificate_invalid:{source_issues[0]}")

    canonical_edges = _canonical_edges(tuple(edges))
    edge_digests = tuple(sorted(edge.digest for edge in canonical_edges))
    if len(set(edge_digests)) != len(edge_digests):
        raise ValueError("frontier_edge_replay_detected")
    if edge_digests != dag_certificate.edge_digests:
        raise ValueError("frontier_edge_binding_mismatch")
    if len(canonical_edges) != dag_certificate.edge_count:
        raise ValueError("frontier_edge_count_mismatch")

    nodes = dag_certificate.node_commit_shas
    node_set = set(nodes)
    children_lists: dict[str, list[str]] = {node: [] for node in nodes}
    positions = {
        node: index
        for index, node in enumerate(dag_certificate.topological_commit_shas)
    }
    for edge in canonical_edges:
        if edge.parent_commit_sha not in node_set:
            raise ValueError("frontier_edge_parent_missing")
        if edge.child_commit_sha not in node_set:
            raise ValueError("frontier_edge_child_missing")
        if positions[edge.parent_commit_sha] >= positions[edge.child_commit_sha]:
            raise ValueError("frontier_edge_topological_order_invalid")
        children_lists[edge.parent_commit_sha].append(edge.child_commit_sha)

    children = {
        node: tuple(sorted(set(values)))
        for node, values in children_lists.items()
    }
    frontier = tuple(sorted(node for node in nodes if not children[node]))
    exact_terminal_frontier = frontier == dag_certificate.tip_commit_shas
    if not exact_terminal_frontier:
        raise ValueError("frontier_tip_binding_mismatch")
    if not frontier:
        raise ValueError("repository_frontier_empty")
    if len(frontier) > max_frontier_size:
        raise ValueError("repository_frontier_bound_exceeded")

    coverage_paths = _canonical_coverage_paths(
        nodes,
        dag_certificate.topological_commit_shas,
        children,
        frontier,
    )
    if len({path.source_commit_sha for path in coverage_paths}) != len(nodes):
        raise ValueError("frontier_coverage_source_replay")
    if {path.source_commit_sha for path in coverage_paths} != node_set:
        raise ValueError("frontier_coverage_source_mismatch")

    frontier_set = set(frontier)
    frontier_antichain = all(not children[tip] for tip in frontier)
    all_nodes_covered = all(
        path.commit_shas
        and path.commit_shas[0] == path.source_commit_sha
        and path.commit_shas[-1] == path.frontier_commit_sha
        and path.frontier_commit_sha in frontier_set
        and all(
            right in children[left]
            for left, right in zip(path.commit_shas, path.commit_shas[1:])
        )
        for path in coverage_paths
    )
    merged_ancestors_excluded = all(
        node not in frontier_set
        for node in nodes
        if children[node]
    )

    certificate = RepositoryFrontierCertificate(
        frontier_id,
        dag_certificate.dag_id,
        dag_certificate.certificate_digest,
        dag_certificate.chain_id,
        dag_certificate.root_commit_sha,
        edge_digests,
        frontier,
        tuple(path.digest for path in coverage_paths),
        dag_certificate.node_count,
        len(frontier),
        max_frontier_size,
        True,
        True,
        exact_terminal_frontier,
        True,
        frontier_antichain,
        all_nodes_covered,
        merged_ancestors_excluded,
        dag_certificate.normal_form_preserved,
        False,
        "",
    )
    certificate = replace(
        certificate,
        certificate_digest=repository_frontier_certificate_digest(certificate),
    )
    issues = repository_frontier_certificate_issues(certificate)
    if issues:
        raise ValueError(f"repository_frontier_certificate_invalid:{issues[0]}")
    return coverage_paths, certificate
