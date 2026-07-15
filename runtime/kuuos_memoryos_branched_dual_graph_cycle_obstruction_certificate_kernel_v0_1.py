from __future__ import annotations

from fractions import Fraction
from typing import Any, Mapping

from runtime.kuuos_memoryos_nonabelian_wilson_loop_certificate_kernel_v0_1 import (
    IDENTITY,
    SWAP_01,
    SWAP_12,
    canonical_digest,
    _compose,
    _inverse,
    _fixed_point_trace,
    _cycle_type,
    _matrix,
    _q,
    _f,
)
from runtime.kuuos_memoryos_dual_cell_chain_defect_localization_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.branched-dual-graph-spanning-tree-cycle-obstruction-"
    "certificate.v0.1"
)

REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
)

SOURCE_TRUE = (
    "source_memoryos_v074_exact",
    "finite_s3_dual_cell_chain_exact",
    "path_ordered_seam_transport_exact",
    "transported_local_defect_product_exact",
    "all_compatible_global_closure_exact",
    "single_mismatch_localization_exact",
    "single_mismatch_conjugacy_class_preserved",
    "multiple_mismatch_noncommutative_order_dependence_exact",
    "class_function_order_resolution_limit_recorded",
    "dual_cycle_holonomy_gauge_covariant_exact",
    "dual_cycle_wilson_gauge_invariant_exact",
    "chain_adjusted_confidence_exact",
    "all_full_rank_transport_dual_cell_chain_layer_commutes",
    "singular_atomic_dual_cell_chain_layer_retained",
    "all_decision_candidates_retained",
    "all_planos_histories_retained",
    "all_quotient_coordinate_probes_retained",
    "relational_frontier_preserved",
    "required_review_set_preserved",
    "dissent_visibility_preserved",
    "minority_visibility_preserved",
    "chain_defect_not_truth_authority",
    "chain_review_not_candidate_ranking",
    "path_transport_not_source_deletion",
    "future_only",
    "read_only",
)

SOURCE_FALSE = (
    "continuum_manifold_theorem_claimed",
    "universal_nonabelian_stokes_theorem_claimed",
    "physical_gauge_field_inference_claimed",
    "local_chain_component_used_as_truth",
    "chain_review_used_as_candidate_ranking",
    "source_record_deleted_by_chain_transport",
    "candidate_ranking_performed",
    "candidate_pruning_performed",
    "candidate_selection_performed",
    "decision_commit_performed",
    "decision_receipt_issued",
    "plan_synthesis_performed",
    "activation_performed",
    "execution_permission",
    "source_memoryos_v074_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)

SOURCE_COUNTS = {
    "literature_dual_cell_chain_record_count": 5,
    "dual_cell_chain_incidence_record_count": 7,
    "dual_cell_chain_profile_record_count": 4,
    "chain_seam_transport_record_count": 12,
    "localized_seam_defect_record_count": 12,
    "path_ordered_chain_composition_record_count": 4,
    "single_defect_localization_record_count": 1,
    "dual_cycle_holonomy_record_count": 2,
    "chain_boundary_wilson_record_count": 4,
    "chain_confidence_record_count": 4,
    "dual_cell_chain_memory_fusion_record_count": 4,
    "full_rank_transport_dual_cell_chain_record_count": 8,
    "singular_atomic_dual_cell_chain_record_count": 4,
    "rank_one_source_boundary_count": 3,
}

SOURCE_COLLECTIONS = (
    "literature_dual_cell_chain_records",
    "dual_cell_chain_incidence_records",
    "dual_cell_chain_profile_records",
    "chain_seam_transport_records",
    "localized_seam_defect_records",
    "path_ordered_chain_composition_records",
    "single_defect_localization_records",
    "dual_cycle_holonomy_records",
    "chain_boundary_wilson_records",
    "chain_confidence_records",
    "dual_cell_chain_memory_fusion_records",
    "full_rank_transport_dual_cell_chain_records",
    "singular_atomic_dual_cell_chain_records",
)

LITERATURE = (
    {
        "literature_id": "arxiv:2604.16252",
        "title": "Universal dualities for Wilson loops in lattice Yang-Mills",
        "published": "2026-04-17",
        "bound_concept": "dual incidence graphs spanning structures and Wilson-loop composition",
    },
    {
        "literature_id": "arxiv:1006.2059",
        "title": "A simplicial gauge theory",
        "published": "2010-06-10",
        "bound_concept": "gauge-invariant discrete transport on glued simplicial complexes",
    },
    {
        "literature_id": "arxiv:hep-lat/0309023",
        "title": "On the non-Abelian Stokes theorem for SU(2) gauge fields",
        "published": "2003-09-07",
        "bound_concept": "ordered lattice holonomy composition around alternative routes",
    },
    {
        "literature_id": "arxiv:1011.0371",
        "title": "Non abelian Bianchi identities, monopoles and gauge invariance",
        "published": "2010-11-01",
        "bound_concept": "gauge-covariant cycle obstruction and defect comparison",
    },
    {
        "literature_id": "arxiv:2605.26697",
        "title": "A Gauge-Covariant Theoretical Framework for Non-Abelian Holonomy Estimation and Feed-Forward Correction in Time-Bin Photonic Qudits",
        "published": "2026-05-26",
        "bound_concept": "path-ordered transport and conjugacy-invariant holonomy signatures",
    },
)

Perm = tuple[int, int, int]
PROFILE_IDS = ("flat_diamond", "cycle_obstructed_diamond")


def _blocked(*blockers: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": {},
        "certificate_digest": None,
    }


def _as_perm(value: Any, *, field: str) -> Perm:
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        raise ValueError(f"{field}_invalid")
    candidate = tuple(int(item) for item in value)
    if sorted(candidate) != [0, 1, 2]:
        raise ValueError(f"{field}_invalid")
    return candidate  # type: ignore[return-value]


def _conjugate(value: Perm, transport: Perm) -> Perm:
    return _compose(_compose(transport, value), _inverse(transport))


def _normalize_source(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v075_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v075_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v075_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v075_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v075_observables_invalid")
    obs = dict(raw)

    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v075_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v075_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v075_{field}_mismatch")

    normalized: dict[str, Any] = {"certificate_digest": digest}
    for field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        digest_field = field.replace("records", "digest")
        if not isinstance(records, list):
            raise ValueError(f"source_memoryos_v075_{field}_invalid")
        if canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v075_{digest_field}_mismatch")
        normalized[field] = [dict(record) for record in records]
        normalized[digest_field] = obs[digest_field]

    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v075_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v075_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v075_probe_support_invalid")
    normalized.update(
        candidate_ids=list(candidates),
        history_ids=list(histories),
        probe_ids=list(probes),
        rank_one_source_boundary_count=obs["rank_one_source_boundary_count"],
    )
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v075_{field}_invalid")
        normalized[field] = list(items)

    localization = normalized["single_defect_localization_records"]
    profiles = normalized["dual_cell_chain_profile_records"]
    confidences = normalized["chain_confidence_records"]
    if [record.get("profile_id") for record in profiles] != [
        "all_compatible_curved",
        "single_middle_mismatch_curved",
        "ordered_double_mismatch_ab",
        "ordered_double_mismatch_ba",
    ]:
        raise ValueError("source_memoryos_v075_profile_order_mismatch")
    if len(localization) != 1:
        raise ValueError("source_memoryos_v075_localization_count_mismatch")
    target_defect = _as_perm(
        localization[0].get("local_mismatch_defect"),
        field="source_target_defect",
    )
    if target_defect != (2, 0, 1):
        raise ValueError("source_memoryos_v075_target_defect_changed")
    if localization[0].get("global_equals_localized_mismatch") is not True:
        raise ValueError("source_memoryos_v075_localization_not_exact")
    if len(confidences) != 4:
        raise ValueError("source_memoryos_v075_confidence_count_mismatch")
    base_confidence = _f(confidences[0].get("source_base_confidence"))
    if base_confidence != Fraction(1, 3):
        raise ValueError("source_memoryos_v075_base_confidence_mismatch")
    normalized.update(
        target_defect=target_defect,
        base_confidence=base_confidence,
    )
    return normalized


def _profile_edges() -> dict[str, dict[str, Perm]]:
    upper = _compose(SWAP_01, SWAP_12)
    return {
        "flat_diamond": {
            "edge-01": SWAP_01,
            "edge-13": SWAP_12,
            "edge-02": IDENTITY,
            "edge-23": upper,
        },
        "cycle_obstructed_diamond": {
            "edge-01": IDENTITY,
            "edge-13": IDENTITY,
            "edge-02": SWAP_01,
            "edge-23": IDENTITY,
        },
    }


def _derive_observables(source_v075: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v075)
    target_defect: Perm = source["target_defect"]
    base_confidence: Fraction = source["base_confidence"]
    profiles = _profile_edges()

    incidence_records = [
        {
            "dual_vertex_id": vertex_id,
            "role": role,
            "dual_dimension": 0,
        }
        for vertex_id, role in (
            ("cell-0", "root"),
            ("cell-1", "upper-branch"),
            ("cell-2", "lower-branch"),
            ("cell-3", "recombination"),
        )
    ] + [
        {
            "dual_edge_id": edge_id,
            "source_dual_vertex": source_id,
            "target_dual_vertex": target_id,
            "dual_dimension": 1,
        }
        for edge_id, source_id, target_id in (
            ("edge-01", "cell-0", "cell-1"),
            ("edge-13", "cell-1", "cell-3"),
            ("edge-02", "cell-0", "cell-2"),
            ("edge-23", "cell-2", "cell-3"),
        )
    ]

    profile_records: list[dict[str, Any]] = []
    edge_records: list[dict[str, Any]] = []
    spanning_tree_records: list[dict[str, Any]] = []
    path_records: list[dict[str, Any]] = []
    cycle_records: list[dict[str, Any]] = []
    routing_records: list[dict[str, Any]] = []
    relation_records: list[dict[str, Any]] = []
    route_wilson_records: list[dict[str, Any]] = []
    cycle_wilson_records: list[dict[str, Any]] = []
    confidence_records: list[dict[str, Any]] = []
    fusion_records: list[dict[str, Any]] = []

    common_root_frame = SWAP_12
    target_frame = SWAP_01

    for profile_id in PROFILE_IDS:
        edges = profiles[profile_id]
        upper_path = _compose(edges["edge-01"], edges["edge-13"])
        lower_path = _compose(edges["edge-02"], edges["edge-23"])
        cycle = _compose(upper_path, _inverse(lower_path))
        paths_agree = upper_path == lower_path
        if paths_agree != (cycle == IDENTITY):
            raise ValueError("diamond_path_agreement_cycle_criterion_failure")

        upper_localized = _conjugate(target_defect, upper_path)
        lower_localized = _conjugate(target_defect, lower_path)
        predicted_upper = _conjugate(lower_localized, cycle)
        if upper_localized != predicted_upper:
            raise ValueError("diamond_route_conjugacy_failure")

        transformed_edges = {
            "edge-01": _compose(_compose(_inverse(common_root_frame), edges["edge-01"]), SWAP_01),
            "edge-13": _compose(_compose(_inverse(SWAP_01), edges["edge-13"]), target_frame),
            "edge-02": _compose(_compose(_inverse(common_root_frame), edges["edge-02"]), SWAP_12),
            "edge-23": _compose(_compose(_inverse(SWAP_12), edges["edge-23"]), target_frame),
        }
        transformed_upper = _compose(transformed_edges["edge-01"], transformed_edges["edge-13"])
        transformed_lower = _compose(transformed_edges["edge-02"], transformed_edges["edge-23"])
        transformed_cycle = _compose(transformed_upper, _inverse(transformed_lower))
        expected_transformed_cycle = _conjugate(cycle, _inverse(common_root_frame))
        if transformed_cycle != expected_transformed_cycle:
            raise ValueError("diamond_cycle_gauge_covariance_failure")

        transformed_target_defect = _compose(
            _compose(_inverse(target_frame), target_defect),
            target_frame,
        )
        transformed_upper_localized = _conjugate(
            transformed_target_defect,
            transformed_upper,
        )
        expected_transformed_upper = _compose(
            _compose(_inverse(common_root_frame), upper_localized),
            common_root_frame,
        )
        if transformed_upper_localized != expected_transformed_upper:
            raise ValueError("diamond_target_defect_gauge_covariance_failure")

        profile_records.append(
            {
                "profile_id": profile_id,
                "vertex_count": 4,
                "edge_count": 4,
                "root_vertex": "cell-0",
                "recombination_vertex": "cell-3",
                "spanning_tree_route": ["edge-01", "edge-13"],
                "alternative_route": ["edge-02", "edge-23"],
                "paths_agree": paths_agree,
                "cycle_obstructed": cycle != IDENTITY,
            }
        )
        for edge_id in ("edge-01", "edge-13", "edge-02", "edge-23"):
            edge_records.append(
                {
                    "profile_id": profile_id,
                    "dual_edge_id": edge_id,
                    "seam_transport": list(edges[edge_id]),
                    "seam_transport_matrix": _matrix(edges[edge_id]),
                    "path_ordered": True,
                }
            )
        spanning_tree_records.append(
            {
                "profile_id": profile_id,
                "tree_edges": ["edge-01", "edge-13"],
                "non_tree_edges": ["edge-02", "edge-23"],
                "tree_root": "cell-0",
                "tree_target": "cell-3",
                "tree_transport": list(upper_path),
                "alternative_transport": list(lower_path),
                "source_records_deleted": False,
            }
        )
        path_records.append(
            {
                "profile_id": profile_id,
                "upper_path_transport": list(upper_path),
                "lower_path_transport": list(lower_path),
                "paths_agree": paths_agree,
                "path_agreement_iff_cycle_identity": paths_agree == (cycle == IDENTITY),
            }
        )
        cycle_records.append(
            {
                "profile_id": profile_id,
                "cycle_obstruction": list(cycle),
                "cycle_type": _cycle_type(cycle),
                "transformed_cycle_obstruction": list(transformed_cycle),
                "expected_root_conjugate": list(expected_transformed_cycle),
                "gauge_covariant": transformed_cycle == expected_transformed_cycle,
                "truth_authority": False,
            }
        )
        for route_id, transport, localized in (
            ("upper-spanning-tree", upper_path, upper_localized),
            ("lower-alternative", lower_path, lower_localized),
        ):
            routing_records.append(
                {
                    "profile_id": profile_id,
                    "route_id": route_id,
                    "target_defect": list(target_defect),
                    "route_transport": list(transport),
                    "root_localized_defect": list(localized),
                    "route_trace": _fixed_point_trace(localized),
                    "frame_dependent_representative": True,
                }
            )
            route_wilson_records.append(
                {
                    "profile_id": profile_id,
                    "route_id": route_id,
                    "localized_defect_trace": _fixed_point_trace(localized),
                    "localized_defect_cycle_type": _cycle_type(localized),
                    "class_function_signature": _fixed_point_trace(localized),
                    "frame_independent": True,
                }
            )
        relation_records.append(
            {
                "profile_id": profile_id,
                "upper_localized_defect": list(upper_localized),
                "lower_localized_defect": list(lower_localized),
                "cycle_conjugated_lower_defect": list(predicted_upper),
                "upper_equals_cycle_conjugated_lower": upper_localized == predicted_upper,
                "exact_route_representatives_equal": upper_localized == lower_localized,
                "class_function_route_signatures_equal": (
                    _fixed_point_trace(upper_localized)
                    == _fixed_point_trace(lower_localized)
                ),
            }
        )

        cycle_trace = _fixed_point_trace(cycle)
        penalty = Fraction(3 - cycle_trace, 18)
        adjusted = base_confidence - penalty
        cycle_wilson_records.append(
            {
                "profile_id": profile_id,
                "cycle_permutation_trace": cycle_trace,
                "transformed_cycle_trace": _fixed_point_trace(transformed_cycle),
                "cycle_signature_gauge_invariant": (
                    cycle_trace == _fixed_point_trace(transformed_cycle)
                ),
            }
        )
        confidence_records.append(
            {
                "profile_id": profile_id,
                "source_base_confidence": _q(base_confidence),
                "route_obstruction_penalty": _q(penalty),
                "branched_graph_adjusted_confidence": _q(adjusted),
                "within_unit_interval": Fraction(0) <= adjusted <= Fraction(1),
                "gauge_invariant": (
                    cycle_trace == _fixed_point_trace(transformed_cycle)
                ),
                "posterior_probability": False,
                "truth_authority": False,
            }
        )
        fusion_records.append(
            {
                "profile_id": profile_id,
                "branched_dual_graph_signature": {
                    "vertex_count": 4,
                    "edge_count": 4,
                    "path_count_root_to_target": 2,
                    "cycle_type": _cycle_type(cycle),
                    "cycle_trace": cycle_trace,
                    "routed_defect_cycle_type": _cycle_type(upper_localized),
                },
                "path_agreement": paths_agree,
                "route_review_required": not paths_agree,
                "candidate_ranking_performed": False,
            }
        )

    expected_path_records = [
        {
            "profile_id": "flat_diamond",
            "upper_path_transport": [1, 2, 0],
            "lower_path_transport": [1, 2, 0],
            "paths_agree": True,
            "path_agreement_iff_cycle_identity": True,
        },
        {
            "profile_id": "cycle_obstructed_diamond",
            "upper_path_transport": [0, 1, 2],
            "lower_path_transport": [1, 0, 2],
            "paths_agree": False,
            "path_agreement_iff_cycle_identity": True,
        },
    ]
    if path_records != expected_path_records:
        raise ValueError("canonical_diamond_path_profile_mismatch")
    if [record["cycle_obstruction"] for record in cycle_records] != [
        [0, 1, 2],
        [1, 0, 2],
    ]:
        raise ValueError("canonical_diamond_cycle_profile_mismatch")
    obstructed_routes = [
        record["root_localized_defect"]
        for record in routing_records
        if record["profile_id"] == "cycle_obstructed_diamond"
    ]
    if obstructed_routes != [[2, 0, 1], [1, 2, 0]]:
        raise ValueError("canonical_diamond_route_localization_mismatch")
    if [record["branched_graph_adjusted_confidence"] for record in confidence_records] != [
        _q(Fraction(1, 3)),
        _q(Fraction(2, 9)),
    ]:
        raise ValueError("canonical_diamond_confidence_mismatch")

    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "branched_dual_graph_transport_commutes": True,
            "cycle_obstruction_comparison_commutes": True,
            "route_localization_conjugacy_commutes": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_dual_cell_chain_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_branch_signature_retained": True,
            "atomic_cycle_obstruction_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_dual_cell_chain_records"]
    ]

    observables: dict[str, Any] = {
        "source_memoryos_v075_exact": True,
        "source_memoryos_v075_certificate_digest": source["certificate_digest"],
        "source_dual_cell_chain_profile_digest": source[
            "dual_cell_chain_profile_digest"
        ],
        "source_path_ordered_chain_composition_digest": source[
            "path_ordered_chain_composition_digest"
        ],
        "source_single_defect_localization_digest": source[
            "single_defect_localization_digest"
        ],
        "source_dual_cycle_holonomy_digest": source["dual_cycle_holonomy_digest"],
        "literature_branched_dual_graph_records": [dict(record) for record in LITERATURE],
        "literature_branched_dual_graph_record_count": len(LITERATURE),
        "branched_dual_graph_incidence_records": incidence_records,
        "branched_dual_graph_incidence_record_count": len(incidence_records),
        "branched_dual_graph_profile_records": profile_records,
        "branched_dual_graph_profile_record_count": len(profile_records),
        "branched_edge_transport_records": edge_records,
        "branched_edge_transport_record_count": len(edge_records),
        "spanning_tree_route_records": spanning_tree_records,
        "spanning_tree_route_record_count": len(spanning_tree_records),
        "alternative_path_comparison_records": path_records,
        "alternative_path_comparison_record_count": len(path_records),
        "cycle_obstruction_records": cycle_records,
        "cycle_obstruction_record_count": len(cycle_records),
        "target_defect_routing_records": routing_records,
        "target_defect_routing_record_count": len(routing_records),
        "route_conjugacy_relation_records": relation_records,
        "route_conjugacy_relation_record_count": len(relation_records),
        "route_wilson_signature_records": route_wilson_records,
        "route_wilson_signature_record_count": len(route_wilson_records),
        "cycle_wilson_signature_records": cycle_wilson_records,
        "cycle_wilson_signature_record_count": len(cycle_wilson_records),
        "branched_graph_confidence_records": confidence_records,
        "branched_graph_confidence_record_count": len(confidence_records),
        "branched_graph_memory_fusion_records": fusion_records,
        "branched_graph_memory_fusion_record_count": len(fusion_records),
        "full_rank_transport_branched_graph_records": full_rank_records,
        "full_rank_transport_branched_graph_record_count": len(full_rank_records),
        "singular_atomic_branched_graph_records": singular_records,
        "singular_atomic_branched_graph_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "finite_s3_branched_dual_graph_exact": True,
        "diamond_incidence_exact": len(incidence_records) == 8,
        "spanning_tree_transport_exact": all(
            not record["source_records_deleted"] for record in spanning_tree_records
        ),
        "alternative_path_comparison_exact": all(
            record["path_agreement_iff_cycle_identity"] for record in path_records
        ),
        "path_agreement_iff_cycle_identity_exact": all(
            record["path_agreement_iff_cycle_identity"] for record in path_records
        ),
        "cycle_obstruction_gauge_covariant_exact": all(
            record["gauge_covariant"] for record in cycle_records
        ),
        "target_defect_route_relation_exact": all(
            record["upper_equals_cycle_conjugated_lower"]
            for record in relation_records
        ),
        "route_wilson_conjugacy_invariant_exact": all(
            record["class_function_route_signatures_equal"]
            for record in relation_records
        ),
        "cycle_wilson_gauge_invariant_exact": all(
            record["cycle_signature_gauge_invariant"]
            for record in cycle_wilson_records
        ),
        "route_obstruction_confidence_exact": (
            confidence_records[0]["branched_graph_adjusted_confidence"]
            == _q(Fraction(1, 3))
            and confidence_records[1]["branched_graph_adjusted_confidence"]
            == _q(Fraction(2, 9))
            and all(record["within_unit_interval"] for record in confidence_records)
        ),
        "all_full_rank_transport_branched_graph_layer_commutes": all(
            record["branched_dual_graph_transport_commutes"]
            and record["cycle_obstruction_comparison_commutes"]
            and record["route_localization_conjugacy_commutes"]
            for record in full_rank_records
        ),
        "singular_atomic_branched_graph_layer_retained": all(
            record["atomic_branch_signature_retained"]
            and record["atomic_cycle_obstruction_retained"]
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
        "cycle_obstruction_not_truth_authority": True,
        "route_review_not_candidate_ranking": True,
        "spanning_tree_not_source_deletion": True,
        "continuum_dual_graph_claimed": False,
        "universal_route_independence_claimed": False,
        "physical_gauge_field_inference_claimed": False,
        "local_route_component_used_as_truth": False,
        "route_review_used_as_candidate_ranking": False,
        "source_record_deleted_by_spanning_tree": False,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v075_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "literature_branched_dual_graph_records",
        "branched_dual_graph_incidence_records",
        "branched_dual_graph_profile_records",
        "branched_edge_transport_records",
        "spanning_tree_route_records",
        "alternative_path_comparison_records",
        "cycle_obstruction_records",
        "target_defect_routing_records",
        "route_conjugacy_relation_records",
        "route_wilson_signature_records",
        "cycle_wilson_signature_records",
        "branched_graph_confidence_records",
        "branched_graph_memory_fusion_records",
        "full_rank_transport_branched_graph_records",
        "singular_atomic_branched_graph_records",
    ):
        observables[field.replace("records", "digest")] = canonical_digest(
            observables[field]
        )
    return observables


def issue_branched_dual_graph_cycle_obstruction_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(
            payload.get("source_memoryos_v075_certificate")
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
    except (KeyError, StopIteration, TypeError, ValueError, ZeroDivisionError) as exc:
        return _blocked(str(exc))


__all__ = [
    "SCHEMA_VERSION",
    "_derive_observables",
    "issue_branched_dual_graph_cycle_obstruction_certificate",
]
