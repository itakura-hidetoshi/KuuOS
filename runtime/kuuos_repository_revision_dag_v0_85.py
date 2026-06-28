#!/usr/bin/env python3
from __future__ import annotations

from collections import deque
from dataclasses import replace
import heapq
from typing import Iterable

from runtime.kuuos_repository_certificate_chain_types_v0_82 import (
    RepositoryCertificateChainRecord,
)
from runtime.kuuos_repository_certificate_chain_v0_82 import (
    certificate_chain_record_issues,
)
from runtime.kuuos_repository_merge_certificate_types_v0_84 import (
    RepositoryMergeCertificate,
)
from runtime.kuuos_repository_merge_certificate_v0_84 import (
    repository_merge_certificate_issues,
)
from runtime.kuuos_repository_revision_dag_types_v0_85 import (
    LINEAR_EDGE,
    MERGE_LEFT_EDGE,
    MERGE_RIGHT_EDGE,
    RepositoryRevisionDagCertificate,
    RepositoryRevisionDagEdge,
    repository_revision_dag_certificate_digest,
)


def _common_prefix(
    left: tuple[str, ...],
    right: tuple[str, ...],
) -> tuple[str, ...]:
    prefix: list[str] = []
    for left_sha, right_sha in zip(left, right):
        if left_sha != right_sha:
            break
        prefix.append(left_sha)
    return tuple(prefix)


def repository_revision_dag_certificate_issues(
    certificate: RepositoryRevisionDagCertificate,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not certificate.dag_id:
        issues.append("dag_id_missing")
    if not certificate.chain_id:
        issues.append("chain_id_missing")
    if not certificate.root_commit_sha:
        issues.append("root_commit_missing")
    if certificate.certificate_digest != repository_revision_dag_certificate_digest(
        certificate
    ):
        issues.append("certificate_digest_mismatch")
    if certificate.node_count != len(certificate.node_commit_shas):
        issues.append("node_count_mismatch")
    if certificate.edge_count != len(certificate.edge_digests):
        issues.append("edge_count_mismatch")
    if certificate.node_count > certificate.max_nodes:
        issues.append("node_bound_exceeded")
    if certificate.edge_count > certificate.max_edges:
        issues.append("edge_bound_exceeded")
    if len(certificate.topological_commit_shas) != certificate.node_count:
        issues.append("topological_count_mismatch")
    if set(certificate.topological_commit_shas) != set(
        certificate.node_commit_shas
    ):
        issues.append("topological_node_mismatch")
    if tuple(sorted(set(certificate.node_commit_shas))) != (
        certificate.node_commit_shas
    ):
        issues.append("node_commits_not_canonical")
    if tuple(sorted(set(certificate.edge_digests))) != certificate.edge_digests:
        issues.append("edge_digests_not_canonical")
    if tuple(sorted(set(certificate.tip_commit_shas))) != (
        certificate.tip_commit_shas
    ):
        issues.append("tip_commits_not_canonical")
    for field_name, valid in (
        ("source_certificates_invalid", certificate.source_certificates_valid),
        ("source_reference_not_closed", certificate.source_reference_closure),
        ("single_root_missing", certificate.single_root),
        ("parent_arity_invalid", certificate.parent_arity_valid),
        ("unreachable_node_present", certificate.all_nodes_reachable),
        ("revision_cycle_detected", certificate.acyclic),
        ("normal_form_not_preserved", certificate.normal_form_preserved),
    ):
        if not valid:
            issues.append(field_name)
    if certificate.external_approval_required:
        issues.append("unexpected_external_approval")
    return tuple(issues)


def _validate_record_link(
    record: RepositoryCertificateChainRecord,
    previous: RepositoryCertificateChainRecord,
) -> None:
    if previous.chain_id != record.chain_id:
        raise ValueError("record_previous_chain_mismatch")
    if previous.root_commit_sha != record.root_commit_sha:
        raise ValueError("record_previous_root_mismatch")
    if previous.current_commit_sha != record.parent_commit_sha:
        raise ValueError("record_previous_commit_mismatch")
    if previous.current_snapshot_digest != record.previous_snapshot_digest:
        raise ValueError("record_previous_snapshot_mismatch")
    if previous.sequence + 1 != record.sequence:
        raise ValueError("record_sequence_discontinuity")
    if previous.max_chain_length != record.max_chain_length:
        raise ValueError("record_chain_bound_mismatch")
    if previous.commit_shas + (record.current_commit_sha,) != record.commit_shas:
        raise ValueError("record_commit_history_mismatch")


def _validate_merge_binding(
    certificate: RepositoryMergeCertificate,
    left: RepositoryCertificateChainRecord,
    right: RepositoryCertificateChainRecord,
) -> None:
    if left.chain_id != certificate.chain_id or right.chain_id != certificate.chain_id:
        raise ValueError("merge_parent_chain_mismatch")
    if (
        left.root_commit_sha != certificate.root_commit_sha
        or right.root_commit_sha != certificate.root_commit_sha
    ):
        raise ValueError("merge_parent_root_mismatch")
    if left.current_commit_sha != certificate.left_commit_sha:
        raise ValueError("merge_left_commit_mismatch")
    if right.current_commit_sha != certificate.right_commit_sha:
        raise ValueError("merge_right_commit_mismatch")
    if left.record_digest == right.record_digest or (
        left.current_commit_sha == right.current_commit_sha
    ):
        raise ValueError("merge_parents_not_distinct")
    if not left.current_normal_form_preserved:
        raise ValueError("merge_left_normal_form_not_preserved")
    if not right.current_normal_form_preserved:
        raise ValueError("merge_right_normal_form_not_preserved")
    if certificate.merge_score != 0:
        raise ValueError("merge_score_not_zero")

    prefix = _common_prefix(left.commit_shas, right.commit_shas)
    if not prefix:
        raise ValueError("merge_common_prefix_missing")
    if certificate.common_prefix_length != len(prefix):
        raise ValueError("merge_common_prefix_length_mismatch")
    if certificate.fork_commit_sha != prefix[-1]:
        raise ValueError("merge_fork_commit_mismatch")
    expected_left_suffix = left.commit_shas[len(prefix):]
    expected_right_suffix = right.commit_shas[len(prefix):]
    if not expected_left_suffix or not expected_right_suffix:
        raise ValueError("merge_branch_suffix_missing")
    if certificate.left_suffix_commit_shas != expected_left_suffix:
        raise ValueError("merge_left_suffix_mismatch")
    if certificate.right_suffix_commit_shas != expected_right_suffix:
        raise ValueError("merge_right_suffix_mismatch")
    if set(expected_left_suffix) & set(expected_right_suffix):
        raise ValueError("merge_branch_history_overlap")


def _topological_order(
    nodes: set[str],
    edges: tuple[RepositoryRevisionDagEdge, ...],
) -> tuple[tuple[str, ...], dict[str, int], dict[str, tuple[str, ...]]]:
    indegree = {node: 0 for node in nodes}
    children: dict[str, list[str]] = {node: [] for node in nodes}
    for edge in edges:
        if edge.parent_commit_sha not in nodes:
            raise ValueError("edge_parent_missing")
        if edge.child_commit_sha not in nodes:
            raise ValueError("edge_child_missing")
        indegree[edge.child_commit_sha] += 1
        children[edge.parent_commit_sha].append(edge.child_commit_sha)

    ready = [node for node, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    remaining = dict(indegree)
    order: list[str] = []
    while ready:
        node = heapq.heappop(ready)
        order.append(node)
        for child in sorted(children[node]):
            remaining[child] -= 1
            if remaining[child] == 0:
                heapq.heappush(ready, child)

    canonical_children = {
        node: tuple(sorted(set(values))) for node, values in children.items()
    }
    return tuple(order), indegree, canonical_children


def certify_repository_revision_dag(
    dag_id: str,
    chain_records: Iterable[RepositoryCertificateChainRecord],
    merge_certificates: Iterable[RepositoryMergeCertificate] = (),
    max_nodes: int = 4096,
    max_edges: int = 8192,
) -> tuple[tuple[RepositoryRevisionDagEdge, ...], RepositoryRevisionDagCertificate]:
    if not dag_id:
        raise ValueError("dag_id_missing")
    if max_nodes <= 0:
        raise ValueError("max_nodes_invalid")
    if max_edges <= 0:
        raise ValueError("max_edges_invalid")

    records = tuple(chain_records)
    merges = tuple(merge_certificates)
    if not records:
        raise ValueError("chain_records_empty")

    record_digests = tuple(record.record_digest for record in records)
    if len(set(record_digests)) != len(record_digests):
        raise ValueError("chain_record_replay_detected")
    merge_digests = tuple(certificate.certificate_digest for certificate in merges)
    if len(set(merge_digests)) != len(merge_digests):
        raise ValueError("merge_certificate_replay_detected")

    for record in records:
        issues = certificate_chain_record_issues(record)
        if issues:
            raise ValueError(f"chain_record_invalid:{issues[0]}")
        if record.current_score != 0:
            raise ValueError("chain_record_score_not_zero")
        if not record.current_normal_form_preserved:
            raise ValueError("chain_record_normal_form_not_preserved")
    for certificate in merges:
        issues = repository_merge_certificate_issues(certificate)
        if issues:
            raise ValueError(f"merge_certificate_invalid:{issues[0]}")

    chain_ids = {record.chain_id for record in records}
    chain_ids.update(certificate.chain_id for certificate in merges)
    if len(chain_ids) != 1:
        raise ValueError("revision_dag_chain_id_mismatch")
    chain_id = next(iter(chain_ids))

    root_shas = {record.root_commit_sha for record in records}
    root_shas.update(certificate.root_commit_sha for certificate in merges)
    if len(root_shas) != 1:
        raise ValueError("revision_dag_root_mismatch")
    root_commit_sha = next(iter(root_shas))

    genesis_records = tuple(record for record in records if record.sequence == 0)
    if len(genesis_records) != 1:
        raise ValueError("revision_dag_genesis_not_unique")
    genesis = genesis_records[0]
    if genesis.current_commit_sha != root_commit_sha:
        raise ValueError("revision_dag_genesis_root_mismatch")

    records_by_digest = {record.record_digest: record for record in records}
    records_by_commit: dict[str, RepositoryCertificateChainRecord] = {}
    for record in records:
        if record.current_commit_sha in records_by_commit:
            raise ValueError("revision_commit_reused")
        records_by_commit[record.current_commit_sha] = record

    edges: list[RepositoryRevisionDagEdge] = []
    for record in records:
        if record.sequence == 0:
            continue
        previous = records_by_digest.get(record.previous_record_digest)
        if previous is None:
            raise ValueError("previous_record_not_in_dag")
        _validate_record_link(record, previous)
        edges.append(RepositoryRevisionDagEdge(
            record.parent_commit_sha,
            record.current_commit_sha,
            record.record_digest,
            LINEAR_EDGE,
            0,
        ))

    merge_commits: set[str] = set()
    for certificate in merges:
        left = records_by_digest.get(certificate.left_record_digest)
        if left is None:
            raise ValueError("merge_left_record_not_in_dag")
        right = records_by_digest.get(certificate.right_record_digest)
        if right is None:
            raise ValueError("merge_right_record_not_in_dag")
        _validate_merge_binding(certificate, left, right)
        if certificate.merge_commit_sha in records_by_commit or (
            certificate.merge_commit_sha in merge_commits
        ):
            raise ValueError("revision_commit_reused")
        merge_commits.add(certificate.merge_commit_sha)
        edges.extend((
            RepositoryRevisionDagEdge(
                certificate.left_commit_sha,
                certificate.merge_commit_sha,
                certificate.certificate_digest,
                MERGE_LEFT_EDGE,
                0,
            ),
            RepositoryRevisionDagEdge(
                certificate.right_commit_sha,
                certificate.merge_commit_sha,
                certificate.certificate_digest,
                MERGE_RIGHT_EDGE,
                1,
            ),
        ))

    nodes = set(records_by_commit) | merge_commits
    canonical_edges = tuple(sorted(
        edges,
        key=lambda edge: (
            edge.child_commit_sha,
            edge.parent_position,
            edge.parent_commit_sha,
            edge.source_certificate_digest,
        ),
    ))
    if len(nodes) > max_nodes:
        raise ValueError("revision_dag_node_bound_exceeded")
    if len(canonical_edges) > max_edges:
        raise ValueError("revision_dag_edge_bound_exceeded")
    edge_digests = tuple(edge.digest for edge in canonical_edges)
    if len(set(edge_digests)) != len(edge_digests):
        raise ValueError("revision_dag_edge_replay_detected")

    topological, indegree, children = _topological_order(nodes, canonical_edges)
    roots = tuple(sorted(node for node, degree in indegree.items() if degree == 0))
    single_root = roots == (root_commit_sha,)
    if not single_root:
        raise ValueError("revision_dag_single_root_violation")
    acyclic = len(topological) == len(nodes)
    if not acyclic:
        raise ValueError("revision_dag_cycle_detected")

    parent_arity_valid = all(
        indegree[node] == (0 if node == root_commit_sha else 2 if node in merge_commits else 1)
        for node in nodes
    )
    if not parent_arity_valid:
        raise ValueError("revision_dag_parent_arity_invalid")

    reachable: set[str] = set()
    queue: deque[str] = deque((root_commit_sha,))
    while queue:
        node = queue.popleft()
        if node in reachable:
            continue
        reachable.add(node)
        queue.extend(children[node])
    all_reachable = reachable == nodes
    if not all_reachable:
        raise ValueError("revision_dag_unreachable_node")

    tips = tuple(sorted(node for node in nodes if not children[node]))
    normal_form_preserved = all(
        record.current_normal_form_preserved for record in records
    ) and all(certificate.merge_normal_form_preserved for certificate in merges)

    certificate = RepositoryRevisionDagCertificate(
        dag_id,
        chain_id,
        root_commit_sha,
        tuple(sorted(record_digests)),
        tuple(sorted(merge_digests)),
        tuple(sorted(nodes)),
        tuple(sorted(edge_digests)),
        topological,
        tips,
        len(nodes),
        len(canonical_edges),
        max_nodes,
        max_edges,
        True,
        True,
        single_root,
        parent_arity_valid,
        all_reachable,
        acyclic,
        normal_form_preserved,
        False,
        "",
    )
    certificate = replace(
        certificate,
        certificate_digest=repository_revision_dag_certificate_digest(certificate),
    )
    issues = repository_revision_dag_certificate_issues(certificate)
    if issues:
        raise ValueError(f"revision_dag_certificate_invalid:{issues[0]}")
    return canonical_edges, certificate
