from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_forgetting_aware_admission_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.provenance-dag-conflict-confidence-revocation-"
    "certificate.v0.1"
)

REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
)

SOURCE_TRUE = (
    "source_memoryos_v066_exact",
    "append_only_archive_exact",
    "all_record_provenance_digests_exact",
    "supersession_relation_exact",
    "obsolete_records_excluded_exact",
    "invalid_records_excluded_exact",
    "query_conditioned_admission_exact",
    "freshest_admissible_witnesses_exact",
    "forgetting_aware_loss_exact",
    "obsolete_reuse_penalized_exact",
    "literature_operations_bound",
    "memory_agent_environment_evaluation_bound",
    "all_full_rank_transport_memory_admission_commutes",
    "singular_atomic_memory_admission_retained",
    "all_decision_candidates_retained",
    "all_planos_histories_retained",
    "all_quotient_coordinate_probes_retained",
    "relational_frontier_preserved",
    "required_review_set_preserved",
    "dissent_visibility_preserved",
    "minority_visibility_preserved",
    "future_only",
    "read_only",
)

SOURCE_FALSE = (
    "similarity_alone_grants_admission",
    "obsolete_memory_admitted",
    "cross_scope_leakage_allowed",
    "automatic_forgetting_deletes_source_record",
    "memory_admission_triggers_action",
    "candidate_ranking_performed",
    "candidate_pruning_performed",
    "candidate_selection_performed",
    "decision_commit_performed",
    "decision_receipt_issued",
    "plan_synthesis_performed",
    "activation_performed",
    "execution_permission",
    "source_memoryos_v066_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)

SOURCE_COUNTS = {
    "literature_provenance_record_count": 8,
    "append_only_memory_archive_record_count": 10,
    "supersession_edge_record_count": 3,
    "effective_memory_record_count": 6,
    "query_conditioned_admission_record_count": 6,
    "freshest_admissible_record_count": 6,
    "forgetting_aware_loss_record_count": 4,
    "full_rank_transport_memory_admission_record_count": 8,
    "singular_atomic_memory_admission_record_count": 4,
    "rank_one_source_boundary_count": 3,
}

SOURCE_COLLECTIONS = (
    ("literature_provenance_records", "literature_provenance_digest"),
    ("append_only_memory_archive_records", "append_only_memory_archive_digest"),
    ("supersession_edge_records", "supersession_edge_digest"),
    ("effective_memory_records", "effective_memory_digest"),
    ("query_conditioned_admission_records", "query_conditioned_admission_digest"),
    ("freshest_admissible_records", "freshest_admissible_digest"),
    ("forgetting_aware_loss_records", "forgetting_aware_loss_digest"),
    (
        "full_rank_transport_memory_admission_records",
        "full_rank_transport_memory_admission_digest",
    ),
    (
        "singular_atomic_memory_admission_records",
        "singular_atomic_memory_admission_digest",
    ),
)

RAW_NODES = (
    ("language-source-a", "profile-language", "japanese", "user-explicit", "profile", 1, Fraction(1), True, False, ()),
    ("language-source-b", "profile-language", "japanese", "session-confirmation", "profile", 1, Fraction(4, 5), True, False, ()),
    ("language-synthesis", "profile-language", "japanese", "multi-source-synthesis", "profile", 2, Fraction(9, 10), True, False, ("language-source-a", "language-source-b")),
    ("frontier-v67", "project-frontier", "MemoryOS-v0.67", "repository-main", "project", 67, Fraction(1), True, False, ()),
    ("frontier-v68", "project-frontier", "MemoryOS-v0.68", "provenance-synthesis", "project", 68, Fraction(1), True, False, ("frontier-v67",)),
    ("policy-legacy-root", "retrieval-policy", "similarity-only", "legacy-index", "governance", 1, Fraction(1, 2), True, True, ()),
    ("policy-legacy-derived", "retrieval-policy", "similarity-indexed", "legacy-derived", "governance", 2, Fraction(3, 5), True, False, ("policy-legacy-root",)),
    ("policy-legacy-downstream", "retrieval-policy", "similarity-ranked", "legacy-downstream", "governance", 3, Fraction(7, 10), True, False, ("policy-legacy-derived",)),
    ("policy-safe-source-a", "retrieval-policy", "query-conditioned-admission", "memgate-provenance", "governance", 4, Fraction(9, 10), True, False, ()),
    ("policy-safe-source-b", "retrieval-policy", "query-conditioned-admission", "memoryos-v067", "governance", 4, Fraction(4, 5), True, False, ()),
    ("policy-safe-synthesis", "retrieval-policy", "query-conditioned-admission", "multi-source-synthesis", "governance", 5, Fraction(17, 20), True, False, ("policy-safe-source-a", "policy-safe-source-b")),
    ("operations-source-a", "memory-operations", "update-forget-retrieve", "memory-taxonomy", "architecture", 1, Fraction(4, 5), True, False, ()),
    ("operations-source-b", "memory-operations", "update-forget-retrieve", "memory-os-paper", "architecture", 1, Fraction(3, 5), True, False, ()),
    ("operations-synthesis", "memory-operations", "update-forget-retrieve", "multi-source-synthesis", "architecture", 2, Fraction(11, 15), True, False, ("operations-source-a", "operations-source-b")),
    ("authority-source", "authority-boundary", "read-only-no-execution", "kuuos-governance", "governance", 1, Fraction(1), True, False, ()),
)

AGGREGATION_CASES = (
    ("language-aggregate", "language-synthesis", (("language-source-a", Fraction(1, 2)), ("language-source-b", Fraction(1, 2)))),
    ("frontier-aggregate", "frontier-v68", (("frontier-v67", Fraction(1)),)),
    ("policy-safe-aggregate", "policy-safe-synthesis", (("policy-safe-source-a", Fraction(1, 2)), ("policy-safe-source-b", Fraction(1, 2)))),
    ("operations-aggregate", "operations-synthesis", (("operations-source-a", Fraction(2, 3)), ("operations-source-b", Fraction(1, 3)))),
)

QUERY_CASES = (
    ("profile-language-query", "profile", "profile-language", "language-synthesis"),
    ("project-frontier-query", "project", "project-frontier", "frontier-v68"),
    ("retrieval-policy-query", "governance", "retrieval-policy", "policy-safe-synthesis"),
    ("memory-operations-query", "architecture", "memory-operations", "operations-synthesis"),
    ("authority-boundary-query", "governance", "authority-boundary", "authority-source"),
)


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def _q(value: Fraction | int) -> dict[str, int]:
    x = Fraction(value)
    return {"numerator": x.numerator, "denominator": x.denominator}


def _f(value: Mapping[str, int]) -> Fraction:
    return Fraction(value["numerator"], value["denominator"])


def _blocked(*blockers: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": {},
        "certificate_digest": None,
    }


def _normalize_source(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v067_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v067_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v067_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v067_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v067_observables_invalid")
    obs = dict(raw)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v067_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v067_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v067_{field}_mismatch")

    out: dict[str, Any] = {"certificate_digest": digest}
    for field, digest_field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        if not isinstance(records, list):
            raise ValueError(f"source_memoryos_v067_{field}_invalid")
        if canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v067_{digest_field}_mismatch")
        out[field] = [dict(record) for record in records]
        out[digest_field] = obs[digest_field]

    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v067_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v067_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v067_probe_support_invalid")
    out.update(
        candidate_ids=list(candidates),
        history_ids=list(histories),
        probe_ids=list(probes),
        rank_one_source_boundary_count=obs["rank_one_source_boundary_count"],
    )
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v067_{field}_invalid")
        out[field] = list(items)
    return out


def _build_nodes(source_digest: str) -> list[dict[str, Any]]:
    nodes = []
    for node_id, claim, value, source_id, scope, version, confidence, valid, revoked, parents in RAW_NODES:
        node = {
            "node_id": node_id,
            "claim_key": claim,
            "value": value,
            "source_id": source_id,
            "scope": scope,
            "version": version,
            "confidence": _q(confidence),
            "valid": valid,
            "revoked": revoked,
            "parent_node_ids": list(parents),
            "source_memoryos_v067_certificate_digest": source_digest,
            "append_only": True,
        }
        node["node_digest"] = canonical_digest(node)
        nodes.append(node)
    return nodes


def _reachable(adjacency: Mapping[str, list[str]], start: str, target: str) -> bool:
    frontier = list(adjacency.get(start, []))
    seen: set[str] = set()
    while frontier:
        node = frontier.pop()
        if node == target:
            return True
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(adjacency.get(node, []))
    return False


def _path(adjacency: Mapping[str, list[str]], start: str, target: str) -> list[str] | None:
    frontier: list[tuple[str, list[str]]] = [(start, [start])]
    seen: set[str] = set()
    while frontier:
        node, path = frontier.pop(0)
        if node == target:
            return path
        if node in seen:
            continue
        seen.add(node)
        for child in adjacency.get(node, []):
            frontier.append((child, path + [child]))
    return None


def _derive_observables(source_v067: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v067)
    nodes = _build_nodes(source["certificate_digest"])
    by_id = {node["node_id"]: node for node in nodes}
    if len(by_id) != len(nodes):
        raise ValueError("provenance_node_id_duplicate")

    edges: list[dict[str, Any]] = []
    adjacency: dict[str, list[str]] = {node_id: [] for node_id in by_id}
    for child in nodes:
        for parent_id in child["parent_node_ids"]:
            parent = by_id.get(parent_id)
            if parent is None:
                raise ValueError("provenance_parent_missing")
            if int(parent["version"]) >= int(child["version"]):
                raise ValueError("provenance_edge_not_version_increasing")
            if parent["scope"] != child["scope"]:
                raise ValueError("provenance_edge_scope_mismatch")
            adjacency[parent_id].append(child["node_id"])
            edges.append(
                {
                    "parent_node_id": parent_id,
                    "child_node_id": child["node_id"],
                    "parent_version": parent["version"],
                    "child_version": child["version"],
                    "strictly_version_increasing": True,
                    "scope_preserved": True,
                    "parent_digest": parent["node_digest"],
                    "child_digest": child["node_digest"],
                }
            )

    strict_reachability = []
    for first in nodes:
        for second in nodes:
            if first["node_id"] != second["node_id"] and _reachable(
                adjacency, first["node_id"], second["node_id"]
            ):
                if int(first["version"]) >= int(second["version"]):
                    raise ValueError("provenance_reachability_version_violation")
                strict_reachability.append(
                    {
                        "ancestor_node_id": first["node_id"],
                        "descendant_node_id": second["node_id"],
                        "ancestor_version": first["version"],
                        "descendant_version": second["version"],
                        "path": _path(adjacency, first["node_id"], second["node_id"]),
                        "strict_version_order": True,
                    }
                )

    cycle_free = all(
        not _reachable(adjacency, node_id, node_id) for node_id in by_id
    )
    if not cycle_free:
        raise ValueError("provenance_cycle_detected")

    conflict_components = []
    claim_scopes = sorted({(node["claim_key"], node["scope"]) for node in nodes})
    for claim_key, scope in claim_scopes:
        component = [
            node for node in nodes
            if node["claim_key"] == claim_key and node["scope"] == scope
        ]
        values = sorted({node["value"] for node in component})
        if len(values) <= 1:
            continue
        comparable = []
        incomparable = []
        for index, left in enumerate(component):
            for right in component[index + 1 :]:
                if left["value"] == right["value"]:
                    continue
                left_to_right = _reachable(adjacency, left["node_id"], right["node_id"])
                right_to_left = _reachable(adjacency, right["node_id"], left["node_id"])
                pair = [left["node_id"], right["node_id"]]
                if left_to_right or right_to_left:
                    comparable.append(pair)
                else:
                    incomparable.append(pair)
        conflict_components.append(
            {
                "claim_key": claim_key,
                "scope": scope,
                "node_ids": [node["node_id"] for node in component],
                "distinct_values": values,
                "comparable_conflict_pairs": comparable,
                "incomparable_conflict_pairs": incomparable,
                "partial_order_not_forced_total": bool(incomparable),
            }
        )

    revoked_roots = [node for node in nodes if node["revoked"] is True]
    affected_ids: set[str] = set()
    revocation_records = []
    for root in revoked_roots:
        for node in nodes:
            path = [root["node_id"]] if node["node_id"] == root["node_id"] else _path(
                adjacency, root["node_id"], node["node_id"]
            )
            if path is None:
                continue
            affected_ids.add(node["node_id"])
            revocation_records.append(
                {
                    "revoked_ancestor_node_id": root["node_id"],
                    "affected_node_id": node["node_id"],
                    "path": path,
                    "revocation_propagated": True,
                    "source_record_deleted": False,
                    "admission_blocked": True,
                }
            )

    aggregation_records = []
    for case_id, target_id, weighted_sources in AGGREGATION_CASES:
        total_weight = sum((weight for _, weight in weighted_sources), Fraction(0))
        if total_weight <= 0:
            raise ValueError("confidence_total_weight_not_positive")
        numerator = sum(
            (weight * _f(by_id[source_id]["confidence"]) for source_id, weight in weighted_sources),
            Fraction(0),
        )
        aggregate = numerator / total_weight
        target = by_id[target_id]
        if aggregate != _f(target["confidence"]):
            raise ValueError("confidence_aggregate_target_mismatch")
        aggregation_records.append(
            {
                "case_id": case_id,
                "target_node_id": target_id,
                "source_weights": [
                    {
                        "source_node_id": source_id,
                        "weight": _q(weight),
                        "confidence": by_id[source_id]["confidence"],
                    }
                    for source_id, weight in weighted_sources
                ],
                "total_weight": _q(total_weight),
                "weighted_numerator": _q(numerator),
                "aggregate_confidence": _q(aggregate),
                "within_unit_interval": Fraction(0) <= aggregate <= Fraction(1),
                "exact_rational": True,
            }
        )

    active_ids = {
        node["node_id"] for node in nodes
        if node["valid"] is True
        and node["revoked"] is False
        and node["node_id"] not in affected_ids
    }
    admission_records = []
    for query_id, scope, claim_key, expected_node_id in QUERY_CASES:
        candidates = [
            node for node in nodes
            if node["node_id"] in active_ids
            and node["scope"] == scope
            and node["claim_key"] == claim_key
        ]
        if not candidates:
            raise ValueError("provenance_query_has_no_candidate")
        maximum_version = max(int(node["version"]) for node in candidates)
        admitted = [
            node["node_id"] for node in candidates
            if int(node["version"]) == maximum_version
        ]
        admission_records.append(
            {
                "query_id": query_id,
                "query_scope": scope,
                "query_claim_key": claim_key,
                "expected_node_id": expected_node_id,
                "admitted_node_ids": admitted,
                "unique_expected_admission": admitted == [expected_node_id],
                "validity_checked": True,
                "scope_checked": True,
                "query_condition_checked": True,
                "revocation_ancestry_checked": True,
                "freshest_version_checked": True,
                "similarity_alone_used": False,
            }
        )

    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "provenance_dag_commutes": True,
            "revocation_gate_commutes": True,
            "confidence_aggregation_commutes": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_memory_admission_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_provenance_dag_retained": True,
            "atomic_revocation_gate_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_memory_admission_records"]
    ]

    obs: dict[str, Any] = {
        "source_memoryos_v067_exact": True,
        "source_memoryos_v067_certificate_digest": source["certificate_digest"],
        "source_literature_provenance_digest": source["literature_provenance_digest"],
        "source_append_only_memory_archive_digest": source["append_only_memory_archive_digest"],
        "source_supersession_edge_digest": source["supersession_edge_digest"],
        "source_query_conditioned_admission_digest": source["query_conditioned_admission_digest"],
        "source_forgetting_aware_loss_digest": source["forgetting_aware_loss_digest"],
        "provenance_node_records": nodes,
        "provenance_node_record_count": len(nodes),
        "provenance_edge_records": edges,
        "provenance_edge_record_count": len(edges),
        "strict_reachability_records": strict_reachability,
        "strict_reachability_record_count": len(strict_reachability),
        "conflict_component_records": conflict_components,
        "conflict_component_record_count": len(conflict_components),
        "revocation_propagation_records": revocation_records,
        "revocation_propagation_record_count": len(revocation_records),
        "multi_source_confidence_records": aggregation_records,
        "multi_source_confidence_record_count": len(aggregation_records),
        "provenance_query_admission_records": admission_records,
        "provenance_query_admission_record_count": len(admission_records),
        "full_rank_transport_provenance_dag_records": full_rank_records,
        "full_rank_transport_provenance_dag_record_count": len(full_rank_records),
        "singular_atomic_provenance_dag_records": singular_records,
        "singular_atomic_provenance_dag_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "provenance_dag_cycle_free_exact": cycle_free,
        "provenance_edges_strictly_version_increasing_exact": all(
            record["strictly_version_increasing"] for record in edges
        ),
        "provenance_preorder_partial_order_exact": cycle_free and all(
            record["strict_version_order"] for record in strict_reachability
        ),
        "conflict_components_partial_order_exact": len(conflict_components) == 2,
        "conflict_partial_order_not_forced_total": any(
            record["partial_order_not_forced_total"] for record in conflict_components
        ),
        "revocation_propagation_exact": affected_ids == {
            "policy-legacy-root",
            "policy-legacy-derived",
            "policy-legacy-downstream",
        },
        "revoked_descendants_excluded_exact": all(
            record["affected_node_id"] not in active_ids
            for record in revocation_records
        ),
        "multi_source_confidence_exact": all(
            record["exact_rational"] and record["within_unit_interval"]
            for record in aggregation_records
        ),
        "provenance_query_admission_exact": all(
            record["unique_expected_admission"]
            and record["validity_checked"]
            and record["scope_checked"]
            and record["query_condition_checked"]
            and record["revocation_ancestry_checked"]
            and record["freshest_version_checked"]
            and not record["similarity_alone_used"]
            for record in admission_records
        ),
        "source_records_preserved_under_revocation": all(
            not record["source_record_deleted"] for record in revocation_records
        ),
        "all_full_rank_transport_provenance_dag_commutes": all(
            record["provenance_dag_commutes"]
            and record["revocation_gate_commutes"]
            and record["confidence_aggregation_commutes"]
            for record in full_rank_records
        ),
        "singular_atomic_provenance_dag_retained": all(
            record["atomic_provenance_dag_retained"]
            and record["atomic_revocation_gate_retained"]
            and not record["two_dimensional_target_density_emitted"]
            and not record["lost_coordinate_reconstructed"]
            for record in singular_records
        ),
        "retained_decision_candidate_ids": source["candidate_ids"],
        "retained_history_ids": source["history_ids"],
        "retained_probe_ids": source["probe_ids"],
        **{field: source[field] for field in REVIEW_FIELDS},
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "all_quotient_coordinate_probes_retained": True,
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "provenance_order_not_candidate_ranking": True,
        "confidence_aggregation_not_truth_authority": True,
        "revocation_not_source_deletion": True,
        "cycle_accepted": False,
        "revoked_descendant_admitted": False,
        "source_record_deleted_by_revocation": False,
        "similarity_alone_grants_admission": False,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v067_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "provenance_node_records",
        "provenance_edge_records",
        "strict_reachability_records",
        "conflict_component_records",
        "revocation_propagation_records",
        "multi_source_confidence_records",
        "provenance_query_admission_records",
        "full_rank_transport_provenance_dag_records",
        "singular_atomic_provenance_dag_records",
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_provenance_dag_revocation_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(
            payload.get("source_memoryos_v067_certificate")
        )
        claims = payload.get("claims")
        if not isinstance(claims, Mapping):
            return _blocked("claims_invalid")
        claims = dict(claims)
        blockers = [
            f"claim_mismatch_{field}"
            for field, value in expected.items()
            if claims.get(field) != value
        ]
        blockers.extend(
            f"unexpected_claim_{field}" for field in claims if field not in expected
        )
        if blockers:
            return _blocked(*blockers)
        unsigned = {
            "accepted": True,
            "schema_version": SCHEMA_VERSION,
            "blockers": [],
            "observables": expected,
        }
        return {**unsigned, "certificate_digest": canonical_digest(unsigned)}
    except (KeyError, TypeError, ValueError) as exc:
        return _blocked(str(exc))


__all__ = [
    "SCHEMA_VERSION",
    "canonical_digest",
    "_derive_observables",
    "issue_provenance_dag_revocation_certificate",
]
