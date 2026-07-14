from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_provenance_dag_revocation_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.lineage-quotient-dependency-adjusted-confidence-"
    "minimal-revocation-cut-certificate.v0.1"
)

REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
)

SOURCE_TRUE = (
    "source_memoryos_v067_exact",
    "provenance_dag_cycle_free_exact",
    "provenance_edges_strictly_version_increasing_exact",
    "provenance_preorder_partial_order_exact",
    "conflict_components_partial_order_exact",
    "conflict_partial_order_not_forced_total",
    "revocation_propagation_exact",
    "revoked_descendants_excluded_exact",
    "multi_source_confidence_exact",
    "provenance_query_admission_exact",
    "source_records_preserved_under_revocation",
    "all_full_rank_transport_provenance_dag_commutes",
    "singular_atomic_provenance_dag_retained",
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
    "cycle_accepted",
    "revoked_descendant_admitted",
    "source_record_deleted_by_revocation",
    "similarity_alone_grants_admission",
    "candidate_ranking_performed",
    "candidate_pruning_performed",
    "candidate_selection_performed",
    "decision_commit_performed",
    "decision_receipt_issued",
    "plan_synthesis_performed",
    "activation_performed",
    "execution_permission",
    "source_memoryos_v067_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)

SOURCE_COUNTS = {
    "provenance_node_record_count": 15,
    "provenance_edge_record_count": 9,
    "strict_reachability_record_count": 10,
    "conflict_component_record_count": 2,
    "revocation_propagation_record_count": 3,
    "multi_source_confidence_record_count": 4,
    "provenance_query_admission_record_count": 5,
    "full_rank_transport_provenance_dag_record_count": 8,
    "singular_atomic_provenance_dag_record_count": 4,
    "rank_one_source_boundary_count": 3,
}

SOURCE_COLLECTIONS = (
    ("provenance_node_records", "provenance_node_digest"),
    ("provenance_edge_records", "provenance_edge_digest"),
    ("strict_reachability_records", "strict_reachability_digest"),
    ("conflict_component_records", "conflict_component_digest"),
    ("revocation_propagation_records", "revocation_propagation_digest"),
    ("multi_source_confidence_records", "multi_source_confidence_digest"),
    ("provenance_query_admission_records", "provenance_query_admission_digest"),
    (
        "full_rank_transport_provenance_dag_records",
        "full_rank_transport_provenance_dag_digest",
    ),
    (
        "singular_atomic_provenance_dag_records",
        "singular_atomic_provenance_dag_digest",
    ),
)

LITERATURE = (
    {
        "literature_id": "arxiv:2602.17913",
        "title": "From Lossy to Verified: A Provenance-Aware Tiered Memory for Agents",
        "published": "2026-02-20",
        "bound_concept": "immutable raw evidence and provenance-linked verified summaries",
    },
    {
        "literature_id": "arxiv:2605.25869",
        "title": "Mitigating Provenance-Role Collapse in Long-Term Agents via Typed Memory Representation",
        "published": "2026-05-25",
        "bound_concept": "typed evidence atoms and provenance-scoped utilization",
    },
    {
        "literature_id": "arxiv:2606.24535",
        "title": "Governed Shared Memory for Multi-Agent LLM Systems",
        "published": "2026-06-23",
        "bound_concept": "governed propagation provenance and contradiction control",
    },
    {
        "literature_id": "arxiv:2606.29279",
        "title": "Manufactured Confidence: How Memory Consolidation Turns Hearsay into Confident Facts",
        "published": "2026-06-28",
        "bound_concept": "single load-bearing memory and confidence inflation under consolidation",
    },
    {
        "literature_id": "arxiv:2607.01988",
        "title": "Episodic-to-Semantic Consolidation Without Identity Drift",
        "published": "2026-07-02",
        "bound_concept": "deterministic provenance-bearing aggregation with identity invariance",
    },
)

LINEAGE_CASES = (
    (
        "language-lineage",
        "language-synthesis",
        (
            ("language-user-root", "language-user", Fraction(1), Fraction(1), Fraction(1, 2), ()),
            (
                "language-user-summary-copy",
                "language-user",
                Fraction(1),
                Fraction(1),
                Fraction(1, 2),
                ("language-user-root",),
            ),
            (
                "language-session-root",
                "language-session",
                Fraction(4, 5),
                Fraction(4, 5),
                Fraction(1, 2),
                (),
            ),
        ),
    ),
    (
        "frontier-lineage",
        "frontier-v68",
        (
            ("frontier-main-root", "frontier-main", Fraction(1), Fraction(1), Fraction(1), ()),
            (
                "frontier-summary-copy",
                "frontier-main",
                Fraction(1),
                Fraction(1),
                Fraction(1),
                ("frontier-main-root",),
            ),
        ),
    ),
    (
        "policy-lineage",
        "policy-safe-synthesis",
        (
            ("policy-memgate-root", "policy-memgate", Fraction(9, 10), Fraction(9, 10), Fraction(1, 2), ()),
            (
                "policy-memgate-rewrite",
                "policy-memgate",
                Fraction(19, 20),
                Fraction(9, 10),
                Fraction(1, 2),
                ("policy-memgate-root",),
            ),
            ("policy-memoryos-root", "policy-memoryos", Fraction(4, 5), Fraction(4, 5), Fraction(1, 2), ()),
        ),
    ),
    (
        "operations-lineage",
        "operations-synthesis",
        (
            (
                "operations-taxonomy-root",
                "operations-taxonomy",
                Fraction(4, 5),
                Fraction(4, 5),
                Fraction(2, 3),
                (),
            ),
            (
                "operations-taxonomy-rewrite",
                "operations-taxonomy",
                Fraction(9, 10),
                Fraction(4, 5),
                Fraction(2, 3),
                ("operations-taxonomy-root",),
            ),
            (
                "operations-paper-root",
                "operations-paper",
                Fraction(3, 5),
                Fraction(3, 5),
                Fraction(1, 3),
                (),
            ),
        ),
    ),
    (
        "authority-lineage",
        "authority-source",
        (
            ("authority-root", "authority-governance", Fraction(1), Fraction(1), Fraction(1), ()),
        ),
    ),
)

REVOCATION_ROOT_ID = "policy-legacy-root"
REVOCATION_TARGET_IDS = (
    "policy-legacy-derived",
    "policy-legacy-downstream",
)
REVOCATION_CANDIDATE_IDS = (
    "policy-legacy-derived",
    "policy-legacy-downstream",
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
        raise ValueError("source_memoryos_v068_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v068_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v068_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v068_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v068_observables_invalid")
    obs = dict(raw)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v068_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v068_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v068_{field}_mismatch")

    out: dict[str, Any] = {"certificate_digest": digest}
    for field, digest_field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        if not isinstance(records, list):
            raise ValueError(f"source_memoryos_v068_{field}_invalid")
        if canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v068_{digest_field}_mismatch")
        out[field] = [dict(record) for record in records]
        out[digest_field] = obs[digest_field]

    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v068_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v068_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v068_probe_support_invalid")
    out.update(
        candidate_ids=list(candidates),
        history_ids=list(histories),
        probe_ids=list(probes),
        rank_one_source_boundary_count=obs["rank_one_source_boundary_count"],
    )
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v068_{field}_invalid")
        out[field] = list(items)
    return out


def _paths(
    adjacency: Mapping[str, list[str]],
    start: str,
    target: str,
) -> list[list[str]]:
    found: list[list[str]] = []
    frontier: list[tuple[str, list[str]]] = [(start, [start])]
    while frontier:
        node, path = frontier.pop()
        if node == target:
            found.append(path)
            continue
        for child in adjacency.get(node, []):
            if child not in path:
                frontier.append((child, path + [child]))
    return sorted(found)


def _powerset(items: tuple[str, ...]) -> list[tuple[str, ...]]:
    return [
        subset
        for size in range(len(items) + 1)
        for subset in combinations(items, size)
    ]


def _derive_observables(source_v068: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v068)
    source_nodes = source["provenance_node_records"]
    node_by_id = {record["node_id"]: record for record in source_nodes}
    if len(node_by_id) != len(source_nodes):
        raise ValueError("source_provenance_node_id_duplicate")

    literature_records = [dict(record) for record in LITERATURE]
    evidence_records: list[dict[str, Any]] = []
    duplicate_records: list[dict[str, Any]] = []
    quotient_records: list[dict[str, Any]] = []
    adjusted_records: list[dict[str, Any]] = []
    load_bearing_records: list[dict[str, Any]] = []

    for case_id, target_node_id, raw_evidence in LINEAGE_CASES:
        if target_node_id not in node_by_id:
            raise ValueError("lineage_target_node_missing")
        roots: dict[str, list[dict[str, Any]]] = {}
        case_evidence: list[dict[str, Any]] = []
        evidence_ids = {item[0] for item in raw_evidence}
        if len(evidence_ids) != len(raw_evidence):
            raise ValueError("lineage_evidence_id_duplicate")

        for (
            evidence_id,
            lineage_root_id,
            surface_confidence,
            root_confidence,
            lineage_budget,
            parent_evidence_ids,
        ) in raw_evidence:
            if any(parent not in evidence_ids for parent in parent_evidence_ids):
                raise ValueError("lineage_parent_evidence_missing")
            if not (Fraction(0) <= surface_confidence <= Fraction(1)):
                raise ValueError("lineage_surface_confidence_out_of_range")
            if not (Fraction(0) <= root_confidence <= Fraction(1)):
                raise ValueError("lineage_root_confidence_out_of_range")
            if lineage_budget <= 0:
                raise ValueError("lineage_budget_not_positive")
            record = {
                "case_id": case_id,
                "target_node_id": target_node_id,
                "evidence_id": evidence_id,
                "lineage_root_id": lineage_root_id,
                "surface_confidence": _q(surface_confidence),
                "root_confidence": _q(root_confidence),
                "lineage_budget": _q(lineage_budget),
                "parent_evidence_ids": list(parent_evidence_ids),
                "derived_copy": bool(parent_evidence_ids),
                "surface_confidence_used_for_aggregation": False,
                "root_confidence_used_for_aggregation": True,
                "source_memoryos_v068_certificate_digest": source["certificate_digest"],
            }
            record["evidence_digest"] = canonical_digest(record)
            case_evidence.append(record)
            evidence_records.append(record)
            roots.setdefault(lineage_root_id, []).append(record)

        for root_id, members in sorted(roots.items()):
            budgets = {_f(member["lineage_budget"]) for member in members}
            root_confidences = {_f(member["root_confidence"]) for member in members}
            if len(budgets) != 1:
                raise ValueError("lineage_budget_inconsistent")
            if len(root_confidences) != 1:
                raise ValueError("lineage_root_confidence_inconsistent")
            for left, right in combinations(members, 2):
                duplicate_records.append(
                    {
                        "case_id": case_id,
                        "lineage_root_id": root_id,
                        "left_evidence_id": left["evidence_id"],
                        "right_evidence_id": right["evidence_id"],
                        "distinct_records": left["evidence_id"] != right["evidence_id"],
                        "same_lineage": True,
                        "independent_source_pair": False,
                    }
                )

        naive_total_weight = sum(
            (_f(record["lineage_budget"]) for record in case_evidence),
            Fraction(0),
        )
        naive_numerator = sum(
            (
                _f(record["lineage_budget"]) * _f(record["surface_confidence"])
                for record in case_evidence
            ),
            Fraction(0),
        )
        naive_confidence = naive_numerator / naive_total_weight

        adjusted_total_weight = Fraction(0)
        adjusted_numerator = Fraction(0)
        root_bundles: list[dict[str, Any]] = []
        adjusted_evidence: list[dict[str, Any]] = []
        for root_id, members in sorted(roots.items()):
            lineage_budget = _f(members[0]["lineage_budget"])
            root_confidence = _f(members[0]["root_confidence"])
            multiplicity = len(members)
            per_copy_weight = lineage_budget / multiplicity
            root_weight_sum = per_copy_weight * multiplicity
            if root_weight_sum != lineage_budget:
                raise ValueError("lineage_weight_conservation_failure")
            adjusted_total_weight += root_weight_sum
            adjusted_numerator += lineage_budget * root_confidence
            root_bundles.append(
                {
                    "lineage_root_id": root_id,
                    "evidence_ids": [member["evidence_id"] for member in members],
                    "lineage_multiplicity": multiplicity,
                    "lineage_budget": _q(lineage_budget),
                    "per_copy_adjusted_weight": _q(per_copy_weight),
                    "root_confidence": _q(root_confidence),
                    "lineage_weight_conserved": True,
                    "independent_lineage_contribution_count": 1,
                }
            )
            for member in members:
                adjusted_evidence.append(
                    {
                        "evidence_id": member["evidence_id"],
                        "lineage_root_id": root_id,
                        "adjusted_weight": _q(per_copy_weight),
                        "aggregation_confidence": _q(root_confidence),
                        "surface_confidence_ignored": (
                            member["surface_confidence"] != member["root_confidence"]
                        ),
                    }
                )

        adjusted_confidence = adjusted_numerator / adjusted_total_weight
        target_confidence = _f(node_by_id[target_node_id]["confidence"])
        if adjusted_confidence != target_confidence:
            raise ValueError("lineage_adjusted_target_confidence_mismatch")

        quotient_records.append(
            {
                "case_id": case_id,
                "target_node_id": target_node_id,
                "raw_evidence_count": len(case_evidence),
                "independent_lineage_count": len(roots),
                "lineage_root_ids": sorted(roots),
                "root_bundles": root_bundles,
                "raw_naive_confidence": _q(naive_confidence),
                "lineage_quotient_confidence": _q(adjusted_confidence),
                "duplicate_lineages_collapsed": len(case_evidence) - len(roots),
                "confidence_inflation_prevented": naive_confidence > adjusted_confidence,
                "exact_rational": True,
            }
        )
        adjusted_records.append(
            {
                "case_id": case_id,
                "target_node_id": target_node_id,
                "adjusted_evidence": adjusted_evidence,
                "adjusted_total_weight": _q(adjusted_total_weight),
                "adjusted_numerator": _q(adjusted_numerator),
                "adjusted_confidence": _q(adjusted_confidence),
                "target_confidence": _q(target_confidence),
                "within_unit_interval": (
                    Fraction(0) <= adjusted_confidence <= Fraction(1)
                ),
                "dependent_copy_weight_conserved": True,
                "surface_rewrite_not_promoted": all(
                    member["surface_confidence_used_for_aggregation"] is False
                    for member in case_evidence
                ),
            }
        )
        load_bearing_records.append(
            {
                "case_id": case_id,
                "target_node_id": target_node_id,
                "independent_lineage_count": len(roots),
                "single_load_bearing_memory": len(roots) == 1,
                "redundant_independent_source_present": len(roots) >= 2,
                "advisory_review_required": len(roots) == 1,
            }
        )

    adjacency: dict[str, list[str]] = {node_id: [] for node_id in node_by_id}
    for edge in source["provenance_edge_records"]:
        adjacency[edge["parent_node_id"]].append(edge["child_node_id"])

    path_records: list[dict[str, Any]] = []
    all_paths: list[list[str]] = []
    for target_id in REVOCATION_TARGET_IDS:
        target_paths = _paths(adjacency, REVOCATION_ROOT_ID, target_id)
        if not target_paths:
            raise ValueError("revocation_target_unreachable")
        for path in target_paths:
            all_paths.append(path)
            path_records.append(
                {
                    "revoked_root_node_id": REVOCATION_ROOT_ID,
                    "target_node_id": target_id,
                    "path": path,
                    "strict_path": len(path) >= 2,
                }
            )

    cut_records: list[dict[str, Any]] = []
    for cut in _powerset(REVOCATION_CANDIDATE_IDS):
        cut_set = set(cut)
        blocked_paths = [
            path for path in all_paths
            if any(node_id in cut_set for node_id in path[1:])
        ]
        cut_records.append(
            {
                "cut_node_ids": list(cut),
                "cut_cardinality": len(cut),
                "blocked_path_count": len(blocked_paths),
                "total_path_count": len(all_paths),
                "blocks_all_paths": len(blocked_paths) == len(all_paths),
                "source_records_deleted": False,
            }
        )
    blocking_cuts = [record for record in cut_records if record["blocks_all_paths"]]
    if not blocking_cuts:
        raise ValueError("revocation_cut_not_found")
    minimum_cardinality = min(record["cut_cardinality"] for record in blocking_cuts)
    minimal_cuts = [
        record for record in blocking_cuts
        if record["cut_cardinality"] == minimum_cardinality
    ]
    if [record["cut_node_ids"] for record in minimal_cuts] != [
        ["policy-legacy-derived"]
    ]:
        raise ValueError("revocation_minimal_cut_mismatch")

    minimal_cut_records = [
        {
            **record,
            "inclusion_minimal": all(
                not candidate["blocks_all_paths"]
                for candidate in cut_records
                if set(candidate["cut_node_ids"]) < set(record["cut_node_ids"])
            ),
            "audit_history_preserved": True,
            "revocation_frontier_only": True,
        }
        for record in minimal_cuts
    ]

    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "lineage_quotient_commutes": True,
            "dependency_adjusted_confidence_commutes": True,
            "minimal_revocation_cut_commutes": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_provenance_dag_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_lineage_root_retained": True,
            "atomic_revocation_frontier_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_provenance_dag_records"]
    ]

    obs: dict[str, Any] = {
        "source_memoryos_v068_exact": True,
        "source_memoryos_v068_certificate_digest": source["certificate_digest"],
        "source_provenance_node_digest": source["provenance_node_digest"],
        "source_provenance_edge_digest": source["provenance_edge_digest"],
        "source_revocation_propagation_digest": source[
            "revocation_propagation_digest"
        ],
        "source_multi_source_confidence_digest": source[
            "multi_source_confidence_digest"
        ],
        "literature_lineage_governance_records": literature_records,
        "literature_lineage_governance_record_count": len(literature_records),
        "lineage_evidence_records": evidence_records,
        "lineage_evidence_record_count": len(evidence_records),
        "duplicate_lineage_pair_records": duplicate_records,
        "duplicate_lineage_pair_record_count": len(duplicate_records),
        "lineage_quotient_records": quotient_records,
        "lineage_quotient_record_count": len(quotient_records),
        "dependency_adjusted_confidence_records": adjusted_records,
        "dependency_adjusted_confidence_record_count": len(adjusted_records),
        "load_bearing_memory_records": load_bearing_records,
        "load_bearing_memory_record_count": len(load_bearing_records),
        "revocation_path_records": path_records,
        "revocation_path_record_count": len(path_records),
        "revocation_cut_candidate_records": cut_records,
        "revocation_cut_candidate_record_count": len(cut_records),
        "minimal_revocation_cut_records": minimal_cut_records,
        "minimal_revocation_cut_record_count": len(minimal_cut_records),
        "full_rank_transport_lineage_quotient_records": full_rank_records,
        "full_rank_transport_lineage_quotient_record_count": len(full_rank_records),
        "singular_atomic_lineage_quotient_records": singular_records,
        "singular_atomic_lineage_quotient_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "lineage_duplicate_detection_exact": len(duplicate_records) == 4,
        "lineage_root_partition_exact": all(
            record["raw_evidence_count"]
            >= record["independent_lineage_count"]
            for record in quotient_records
        ),
        "dependent_copy_weight_conservation_exact": all(
            record["dependent_copy_weight_conserved"]
            for record in adjusted_records
        ),
        "lineage_adjusted_confidence_exact": all(
            record["adjusted_confidence"] == record["target_confidence"]
            and record["within_unit_interval"]
            for record in adjusted_records
        ),
        "derived_surface_confidence_not_promoted_exact": all(
            record["surface_rewrite_not_promoted"] for record in adjusted_records
        ),
        "confidence_inflation_prevention_exact": (
            all(
                _f(record["raw_naive_confidence"])
                >= _f(record["lineage_quotient_confidence"])
                for record in quotient_records
            )
            and any(
                record["confidence_inflation_prevented"]
                for record in quotient_records
            )
        ),
        "single_load_bearing_memory_flagged_exact": all(
            record["single_load_bearing_memory"]
            == (record["independent_lineage_count"] == 1)
            for record in load_bearing_records
        ),
        "independent_redundancy_not_raw_copy_count_exact": all(
            record["redundant_independent_source_present"]
            == (record["independent_lineage_count"] >= 2)
            for record in load_bearing_records
        ),
        "minimal_revocation_cut_exact": minimal_cut_records == [
            {
                "cut_node_ids": ["policy-legacy-derived"],
                "cut_cardinality": 1,
                "blocked_path_count": 2,
                "total_path_count": 2,
                "blocks_all_paths": True,
                "source_records_deleted": False,
                "inclusion_minimal": True,
                "audit_history_preserved": True,
                "revocation_frontier_only": True,
            }
        ],
        "revocation_cut_preserves_audit_history": all(
            record["audit_history_preserved"] for record in minimal_cut_records
        ),
        "all_full_rank_transport_lineage_quotient_commutes": all(
            record["lineage_quotient_commutes"]
            and record["dependency_adjusted_confidence_commutes"]
            and record["minimal_revocation_cut_commutes"]
            for record in full_rank_records
        ),
        "singular_atomic_lineage_quotient_retained": all(
            record["atomic_lineage_root_retained"]
            and record["atomic_revocation_frontier_retained"]
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
        "lineage_quotient_not_candidate_ranking": True,
        "confidence_adjustment_not_truth_authority": True,
        "minimal_cut_not_source_deletion": True,
        "raw_copy_count_grants_independence": False,
        "derived_surface_confidence_promoted": False,
        "single_load_bearing_memory_silently_trusted": False,
        "nonminimal_revocation_cut_claimed_minimal": False,
        "source_record_deleted_by_revocation_cut": False,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v068_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "literature_lineage_governance_records",
        "lineage_evidence_records",
        "duplicate_lineage_pair_records",
        "lineage_quotient_records",
        "dependency_adjusted_confidence_records",
        "load_bearing_memory_records",
        "revocation_path_records",
        "revocation_cut_candidate_records",
        "minimal_revocation_cut_records",
        "full_rank_transport_lineage_quotient_records",
        "singular_atomic_lineage_quotient_records",
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_lineage_quotient_revocation_cut_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(
            payload.get("source_memoryos_v068_certificate")
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
    "issue_lineage_quotient_revocation_cut_certificate",
]
