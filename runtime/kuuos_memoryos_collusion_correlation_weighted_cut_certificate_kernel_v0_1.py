from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_lineage_quotient_revocation_cut_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.collusion-correlation-effective-lineage-robust-confidence-"
    "weighted-revocation-cut-certificate.v0.1"
)

REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
)

SOURCE_TRUE = (
    "source_memoryos_v068_exact",
    "lineage_duplicate_detection_exact",
    "lineage_root_partition_exact",
    "dependent_copy_weight_conservation_exact",
    "lineage_adjusted_confidence_exact",
    "derived_surface_confidence_not_promoted_exact",
    "confidence_inflation_prevention_exact",
    "single_load_bearing_memory_flagged_exact",
    "independent_redundancy_not_raw_copy_count_exact",
    "minimal_revocation_cut_exact",
    "revocation_cut_preserves_audit_history",
    "all_full_rank_transport_lineage_quotient_commutes",
    "singular_atomic_lineage_quotient_retained",
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
    "raw_copy_count_grants_independence",
    "derived_surface_confidence_promoted",
    "single_load_bearing_memory_silently_trusted",
    "nonminimal_revocation_cut_claimed_minimal",
    "source_record_deleted_by_revocation_cut",
    "candidate_ranking_performed",
    "candidate_pruning_performed",
    "candidate_selection_performed",
    "decision_commit_performed",
    "decision_receipt_issued",
    "plan_synthesis_performed",
    "activation_performed",
    "execution_permission",
    "source_memoryos_v068_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)

SOURCE_COUNTS = {
    "literature_lineage_governance_record_count": 5,
    "lineage_evidence_record_count": 12,
    "duplicate_lineage_pair_record_count": 4,
    "lineage_quotient_record_count": 5,
    "dependency_adjusted_confidence_record_count": 5,
    "load_bearing_memory_record_count": 5,
    "revocation_path_record_count": 2,
    "revocation_cut_candidate_record_count": 4,
    "minimal_revocation_cut_record_count": 1,
    "full_rank_transport_lineage_quotient_record_count": 8,
    "singular_atomic_lineage_quotient_record_count": 4,
    "rank_one_source_boundary_count": 3,
}

SOURCE_COLLECTIONS = (
    ("literature_lineage_governance_records", "literature_lineage_governance_digest"),
    ("lineage_evidence_records", "lineage_evidence_digest"),
    ("duplicate_lineage_pair_records", "duplicate_lineage_pair_digest"),
    ("lineage_quotient_records", "lineage_quotient_digest"),
    (
        "dependency_adjusted_confidence_records",
        "dependency_adjusted_confidence_digest",
    ),
    ("load_bearing_memory_records", "load_bearing_memory_digest"),
    ("revocation_path_records", "revocation_path_digest"),
    ("revocation_cut_candidate_records", "revocation_cut_candidate_digest"),
    ("minimal_revocation_cut_records", "minimal_revocation_cut_digest"),
    (
        "full_rank_transport_lineage_quotient_records",
        "full_rank_transport_lineage_quotient_digest",
    ),
    (
        "singular_atomic_lineage_quotient_records",
        "singular_atomic_lineage_quotient_digest",
    ),
)

LITERATURE = (
    {
        "literature_id": "arxiv:2604.01151",
        "title": "Detecting Multi-Agent Collusion Through Multi-Agent Interpretability",
        "published": "2026-04-01",
        "bound_concept": "multi-signal group-level collusion detection",
    },
    {
        "literature_id": "arxiv:2606.04990",
        "title": "From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents",
        "published": "2026-06-03",
        "bound_concept": "claim-level evidence tracing and execution provenance",
    },
    {
        "literature_id": "arxiv:2605.04264",
        "title": "Governed Collaborative Memory as Artificial Selection in LLM-Based Multi-Agent Systems",
        "published": "2026-05-05",
        "bound_concept": "governed shared-memory persistence and correction pathways",
    },
    {
        "literature_id": "arxiv:2106.00088",
        "title": "Robust Aggregation of Correlated Information",
        "published": "2021-05-31",
        "bound_concept": "robust aggregation when source correlation is uncertain",
    },
    {
        "literature_id": "arxiv:2102.06805",
        "title": "The Structure of Minimum Vertex Cuts",
        "published": "2021-02-12",
        "bound_concept": "finite minimum vertex-cut structure",
    },
)

SOURCE_AGENTS = (
    (
        "source-a",
        "lineage-a",
        Fraction(19, 20),
        "shared-provenance-x",
        "behavior-alpha",
        7,
    ),
    (
        "source-b",
        "lineage-b",
        Fraction(19, 20),
        "shared-provenance-x",
        "behavior-alpha",
        7,
    ),
    (
        "source-c",
        "lineage-c",
        Fraction(3, 5),
        "independent-provenance-c",
        "behavior-gamma",
        11,
    ),
    (
        "source-d",
        "lineage-d",
        Fraction(7, 10),
        "independent-provenance-d",
        "behavior-delta",
        13,
    ),
)

PAIR_SIGNALS = (
    ("source-a", "source-b", Fraction(3, 4), Fraction(7, 8), True),
    ("source-a", "source-c", Fraction(1, 4), Fraction(1, 5), False),
    ("source-a", "source-d", Fraction(0), Fraction(1, 10), False),
    ("source-b", "source-c", Fraction(1, 4), Fraction(1, 5), False),
    ("source-b", "source-d", Fraction(0), Fraction(1, 10), False),
    ("source-c", "source-d", Fraction(0), Fraction(1, 8), False),
)

CORRELATED_PAIR = frozenset(("source-a", "source-b"))
CORRELATED_RHO = Fraction(3, 4)

REVOCATION_NODES = (
    "legacy-root",
    "legacy-hub",
    "legacy-branch-a",
    "legacy-branch-b",
    "legacy-leaf-a",
    "legacy-leaf-b",
)

REVOCATION_EDGES = (
    ("legacy-root", "legacy-hub"),
    ("legacy-hub", "legacy-branch-a"),
    ("legacy-hub", "legacy-branch-b"),
    ("legacy-branch-a", "legacy-leaf-a"),
    ("legacy-branch-b", "legacy-leaf-b"),
)

REVOCATION_PATHS = (
    (
        "legacy-root",
        "legacy-hub",
        "legacy-branch-a",
        "legacy-leaf-a",
    ),
    (
        "legacy-root",
        "legacy-hub",
        "legacy-branch-b",
        "legacy-leaf-b",
    ),
)

REVOCATION_CANDIDATES = (
    "legacy-hub",
    "legacy-branch-a",
    "legacy-branch-b",
    "legacy-leaf-a",
    "legacy-leaf-b",
)

REVOCATION_COSTS = {
    "legacy-hub": Fraction(3),
    "legacy-branch-a": Fraction(1),
    "legacy-branch-b": Fraction(1),
    "legacy-leaf-a": Fraction(2),
    "legacy-leaf-b": Fraction(2),
}


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


def _powerset(items: tuple[str, ...]) -> list[tuple[str, ...]]:
    return [
        subset
        for size in range(len(items) + 1)
        for subset in combinations(items, size)
    ]


def _normalize_source(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v069_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v069_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v069_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v069_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v069_observables_invalid")
    obs = dict(raw)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v069_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v069_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v069_{field}_mismatch")

    out: dict[str, Any] = {"certificate_digest": digest}
    for field, digest_field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        if not isinstance(records, list):
            raise ValueError(f"source_memoryos_v069_{field}_invalid")
        if canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v069_{digest_field}_mismatch")
        out[field] = [dict(record) for record in records]
        out[digest_field] = obs[digest_field]

    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v069_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v069_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v069_probe_support_invalid")
    out.update(
        candidate_ids=list(candidates),
        history_ids=list(histories),
        probe_ids=list(probes),
        rank_one_source_boundary_count=obs["rank_one_source_boundary_count"],
    )
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v069_{field}_invalid")
        out[field] = list(items)
    return out


def _derive_observables(source_v069: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v069)

    literature_records = [dict(record) for record in LITERATURE]

    agent_records: list[dict[str, Any]] = []
    confidence_by_id: dict[str, Fraction] = {}
    lineage_by_id: dict[str, str] = {}
    for (
        source_id,
        lineage_root_id,
        confidence,
        provenance_family,
        behavioral_key,
        support_window,
    ) in SOURCE_AGENTS:
        record = {
            "source_id": source_id,
            "lineage_root_id": lineage_root_id,
            "confidence": _q(confidence),
            "provenance_family": provenance_family,
            "behavioral_key": behavioral_key,
            "support_window": support_window,
            "source_memoryos_v069_certificate_digest": source["certificate_digest"],
        }
        record["source_agent_digest"] = canonical_digest(record)
        agent_records.append(record)
        confidence_by_id[source_id] = confidence
        lineage_by_id[source_id] = lineage_root_id

    pair_records: list[dict[str, Any]] = []
    suspected_records: list[dict[str, Any]] = []
    for left, right, provenance_overlap, behavioral_correlation, synchronized in PAIR_SIGNALS:
        distinct = lineage_by_id[left] != lineage_by_id[right]
        suspected = (
            distinct
            and provenance_overlap >= Fraction(1, 2)
            and behavioral_correlation >= Fraction(3, 4)
            and synchronized
        )
        record = {
            "pair_id": f"{left}::{right}",
            "left_source_id": left,
            "right_source_id": right,
            "left_lineage_root_id": lineage_by_id[left],
            "right_lineage_root_id": lineage_by_id[right],
            "distinct_lineages": distinct,
            "provenance_overlap": _q(provenance_overlap),
            "behavioral_correlation": _q(behavioral_correlation),
            "synchronized_support": synchronized,
            "suspected_collusion": suspected,
            "multi_signal_rule": True,
        }
        pair_records.append(record)
        if suspected:
            suspected_records.append(dict(record))

    if [record["pair_id"] for record in suspected_records] != ["source-a::source-b"]:
        raise ValueError("canonical_collusion_pair_mismatch")

    parent: dict[str, str] = {source_id: source_id for source_id in confidence_by_id}

    def find(item: str) -> str:
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union(left: str, right: str) -> None:
        root_left = find(left)
        root_right = find(right)
        if root_left != root_right:
            parent[max(root_left, root_right)] = min(root_left, root_right)

    for record in suspected_records:
        union(record["left_source_id"], record["right_source_id"])

    components: dict[str, list[str]] = {}
    for source_id in sorted(confidence_by_id):
        components.setdefault(find(source_id), []).append(source_id)

    component_records: list[dict[str, Any]] = []
    for ordinal, members in enumerate(sorted(components.values()), start=1):
        representative_confidence = min(confidence_by_id[item] for item in members)
        component_records.append(
            {
                "component_id": f"component-{ordinal}",
                "source_ids": members,
                "source_count": len(members),
                "representative_confidence": _q(representative_confidence),
                "collusion_component": len(members) > 1,
                "component_weight_budget": _q(Fraction(1)),
                "copies_counted_independently": False,
            }
        )

    if [record["source_ids"] for record in component_records] != [
        ["source-a", "source-b"],
        ["source-c"],
        ["source-d"],
    ]:
        raise ValueError("collusion_component_partition_mismatch")

    source_ids = [record["source_id"] for record in agent_records]
    correlation_records: list[dict[str, Any]] = []
    full_correlation: dict[tuple[str, str], Fraction] = {}
    for left_index, left in enumerate(source_ids):
        for right_index, right in enumerate(source_ids):
            if left == right:
                rho = Fraction(1)
            elif frozenset((left, right)) == CORRELATED_PAIR:
                rho = CORRELATED_RHO
            else:
                rho = Fraction(0)
            full_correlation[(left, right)] = rho
            if left_index <= right_index:
                correlation_records.append(
                    {
                        "left_source_id": left,
                        "right_source_id": right,
                        "correlation": _q(rho),
                        "diagonal": left == right,
                        "symmetric": True,
                    }
                )

    weights = {source_id: Fraction(1) for source_id in source_ids}
    total_weight = sum(weights.values(), Fraction(0))
    quadratic = sum(
        (
            weights[left] * full_correlation[(left, right)] * weights[right]
            for left in source_ids
            for right in source_ids
        ),
        Fraction(0),
    )
    effective_count = total_weight * total_weight / quadratic
    baseline_quadratic = sum((weight * weight for weight in weights.values()), Fraction(0))
    baseline_effective_count = total_weight * total_weight / baseline_quadratic
    if effective_count != Fraction(32, 11):
        raise ValueError("effective_independent_source_count_mismatch")

    effective_records = [
        {
            "profile_id": "independent-baseline",
            "raw_source_count": len(source_ids),
            "total_weight": _q(total_weight),
            "correlation_quadratic_form": _q(baseline_quadratic),
            "effective_independent_source_count": _q(baseline_effective_count),
            "correlation_adjusted": False,
        },
        {
            "profile_id": "observed-correlation",
            "raw_source_count": len(source_ids),
            "total_weight": _q(total_weight),
            "correlation_quadratic_form": _q(quadratic),
            "effective_independent_source_count": _q(effective_count),
            "correlation_adjusted": True,
        },
    ]

    naive_confidence = sum(confidence_by_id.values(), Fraction(0)) / len(source_ids)
    robust_numerator = sum(
        (_f(record["representative_confidence"]) for record in component_records),
        Fraction(0),
    )
    robust_confidence = robust_numerator / len(component_records)
    if naive_confidence != Fraction(4, 5):
        raise ValueError("naive_collusive_confidence_mismatch")
    if robust_confidence != Fraction(3, 4):
        raise ValueError("robust_component_confidence_mismatch")

    robust_records = [
        {
            "profile_id": "canonical-collusion-profile",
            "raw_source_count": len(source_ids),
            "collusion_component_count": len(component_records),
            "raw_naive_confidence": _q(naive_confidence),
            "component_capped_numerator": _q(robust_numerator),
            "component_capped_confidence": _q(robust_confidence),
            "confidence_inflation_removed": _q(naive_confidence - robust_confidence),
            "within_unit_interval": Fraction(0) <= robust_confidence <= Fraction(1),
            "collusive_component_weight_capped_at_one": True,
            "exact_rational": True,
        }
    ]

    node_records = [
        {
            "node_id": node_id,
            "revocation_cost": (
                _q(REVOCATION_COSTS[node_id])
                if node_id in REVOCATION_COSTS
                else None
            ),
            "source_record_deleted": False,
        }
        for node_id in REVOCATION_NODES
    ]
    edge_records = [
        {"parent_node_id": parent_id, "child_node_id": child_id}
        for parent_id, child_id in REVOCATION_EDGES
    ]
    path_records = [
        {
            "path_id": f"path-{index}",
            "path": list(path),
            "target_node_id": path[-1],
        }
        for index, path in enumerate(REVOCATION_PATHS, start=1)
    ]

    cut_records: list[dict[str, Any]] = []
    for cut in _powerset(REVOCATION_CANDIDATES):
        cut_set = set(cut)
        blocks = [
            path
            for path in REVOCATION_PATHS
            if any(node_id in cut_set for node_id in path[1:])
        ]
        cut_weight = sum((REVOCATION_COSTS[node_id] for node_id in cut), Fraction(0))
        cut_records.append(
            {
                "cut_node_ids": list(cut),
                "cut_cardinality": len(cut),
                "cut_weight": _q(cut_weight),
                "blocked_path_count": len(blocks),
                "total_path_count": len(REVOCATION_PATHS),
                "blocks_all_paths": len(blocks) == len(REVOCATION_PATHS),
                "source_records_deleted": False,
            }
        )

    blocking = [record for record in cut_records if record["blocks_all_paths"]]
    minimum_cardinality = min(record["cut_cardinality"] for record in blocking)
    minimum_cardinality_cuts = [
        record for record in blocking if record["cut_cardinality"] == minimum_cardinality
    ]
    minimum_weight = min(_f(record["cut_weight"]) for record in blocking)
    minimum_weight_cuts = [
        record for record in blocking if _f(record["cut_weight"]) == minimum_weight
    ]
    if [record["cut_node_ids"] for record in minimum_cardinality_cuts] != [
        ["legacy-hub"]
    ]:
        raise ValueError("minimum_cardinality_cut_mismatch")
    if [record["cut_node_ids"] for record in minimum_weight_cuts] != [
        ["legacy-branch-a", "legacy-branch-b"]
    ]:
        raise ValueError("minimum_weighted_cut_mismatch")

    minimum_weight_records = [
        {
            **record,
            "minimum_weight": True,
            "unique_minimum_weight": len(minimum_weight_cuts) == 1,
            "audit_history_preserved": True,
            "revocation_frontier_only": True,
        }
        for record in minimum_weight_cuts
    ]

    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "collusion_gate_commutes": True,
            "correlation_adjustment_commutes": True,
            "robust_confidence_commutes": True,
            "weighted_revocation_cut_commutes": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_lineage_quotient_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_collusion_component_retained": True,
            "atomic_weighted_revocation_frontier_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_lineage_quotient_records"]
    ]

    obs: dict[str, Any] = {
        "source_memoryos_v069_exact": True,
        "source_memoryos_v069_certificate_digest": source["certificate_digest"],
        "source_lineage_evidence_digest": source["lineage_evidence_digest"],
        "source_lineage_quotient_digest": source["lineage_quotient_digest"],
        "source_dependency_adjusted_confidence_digest": source[
            "dependency_adjusted_confidence_digest"
        ],
        "source_minimal_revocation_cut_digest": source["minimal_revocation_cut_digest"],
        "literature_collusion_robustness_records": literature_records,
        "literature_collusion_robustness_record_count": len(literature_records),
        "source_agent_records": agent_records,
        "source_agent_record_count": len(agent_records),
        "collusion_pair_signal_records": pair_records,
        "collusion_pair_signal_record_count": len(pair_records),
        "suspected_collusion_pair_records": suspected_records,
        "suspected_collusion_pair_record_count": len(suspected_records),
        "collusion_component_records": component_records,
        "collusion_component_record_count": len(component_records),
        "correlation_matrix_entry_records": correlation_records,
        "correlation_matrix_entry_record_count": len(correlation_records),
        "effective_independent_source_count_records": effective_records,
        "effective_independent_source_count_record_count": len(effective_records),
        "robust_confidence_records": robust_records,
        "robust_confidence_record_count": len(robust_records),
        "weighted_revocation_node_records": node_records,
        "weighted_revocation_node_record_count": len(node_records),
        "weighted_revocation_edge_records": edge_records,
        "weighted_revocation_edge_record_count": len(edge_records),
        "weighted_revocation_path_records": path_records,
        "weighted_revocation_path_record_count": len(path_records),
        "weighted_revocation_cut_candidate_records": cut_records,
        "weighted_revocation_cut_candidate_record_count": len(cut_records),
        "minimum_weighted_revocation_cut_records": minimum_weight_records,
        "minimum_weighted_revocation_cut_record_count": len(minimum_weight_records),
        "full_rank_transport_collusion_robustness_records": full_rank_records,
        "full_rank_transport_collusion_robustness_record_count": len(full_rank_records),
        "singular_atomic_collusion_robustness_records": singular_records,
        "singular_atomic_collusion_robustness_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "collusion_signal_fusion_exact": (
            len(suspected_records) == 1
            and suspected_records[0]["pair_id"] == "source-a::source-b"
        ),
        "distinct_lineage_collusion_detected_exact": all(
            record["distinct_lineages"] for record in suspected_records
        ),
        "correlation_matrix_symmetric_exact": all(
            record["symmetric"] for record in correlation_records
        ),
        "effective_independent_source_count_exact": (
            _f(effective_records[0]["effective_independent_source_count"])
            == Fraction(4)
            and _f(effective_records[1]["effective_independent_source_count"])
            == Fraction(32, 11)
        ),
        "positive_correlation_reduces_effective_count": effective_count < baseline_effective_count,
        "component_capped_robust_confidence_exact": (
            robust_records[0]["component_capped_confidence"] == _q(Fraction(3, 4))
            and robust_records[0]["raw_naive_confidence"] == _q(Fraction(4, 5))
        ),
        "collusive_component_not_double_counted": all(
            not record["copies_counted_independently"]
            for record in component_records
            if record["collusion_component"]
        ),
        "confidence_inflation_removed_exact": robust_records[0][
            "confidence_inflation_removed"
        ] == _q(Fraction(1, 20)),
        "minimum_weighted_revocation_cut_exact": minimum_weight_records == [
            {
                "cut_node_ids": ["legacy-branch-a", "legacy-branch-b"],
                "cut_cardinality": 2,
                "cut_weight": _q(Fraction(2)),
                "blocked_path_count": 2,
                "total_path_count": 2,
                "blocks_all_paths": True,
                "source_records_deleted": False,
                "minimum_weight": True,
                "unique_minimum_weight": True,
                "audit_history_preserved": True,
                "revocation_frontier_only": True,
            }
        ],
        "minimum_weight_cut_differs_from_minimum_cardinality_cut": (
            minimum_cardinality_cuts[0]["cut_node_ids"] == ["legacy-hub"]
            and minimum_cardinality_cuts[0]["cut_weight"] == _q(Fraction(3))
            and minimum_weight_records[0]["cut_cardinality"] == 2
        ),
        "weighted_revocation_cut_preserves_audit_history": all(
            record["audit_history_preserved"] for record in minimum_weight_records
        ),
        "all_full_rank_transport_collusion_robustness_commutes": all(
            record["collusion_gate_commutes"]
            and record["correlation_adjustment_commutes"]
            and record["robust_confidence_commutes"]
            and record["weighted_revocation_cut_commutes"]
            for record in full_rank_records
        ),
        "singular_atomic_collusion_robustness_retained": all(
            record["atomic_collusion_component_retained"]
            and record["atomic_weighted_revocation_frontier_retained"]
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
        "collusion_detection_not_candidate_ranking": True,
        "robust_confidence_not_truth_authority": True,
        "weighted_cut_not_source_deletion": True,
        "single_signal_collusion_claimed": False,
        "collusive_copies_counted_independently": False,
        "raw_source_count_used_as_effective_count": False,
        "minimum_cardinality_cut_claimed_weight_optimal": False,
        "source_record_deleted_by_weighted_cut": False,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v069_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "literature_collusion_robustness_records",
        "source_agent_records",
        "collusion_pair_signal_records",
        "suspected_collusion_pair_records",
        "collusion_component_records",
        "correlation_matrix_entry_records",
        "effective_independent_source_count_records",
        "robust_confidence_records",
        "weighted_revocation_node_records",
        "weighted_revocation_edge_records",
        "weighted_revocation_path_records",
        "weighted_revocation_cut_candidate_records",
        "minimum_weighted_revocation_cut_records",
        "full_rank_transport_collusion_robustness_records",
        "singular_atomic_collusion_robustness_records",
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_collusion_correlation_weighted_cut_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(
            payload.get("source_memoryos_v069_certificate")
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
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        return _blocked(str(exc))


__all__ = [
    "SCHEMA_VERSION",
    "canonical_digest",
    "_derive_observables",
    "issue_collusion_correlation_weighted_cut_certificate",
]
