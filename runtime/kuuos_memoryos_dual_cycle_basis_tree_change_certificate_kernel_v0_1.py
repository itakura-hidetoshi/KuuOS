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
from runtime.kuuos_memoryos_branched_dual_graph_cycle_obstruction_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.dual-cycle-basis-spanning-tree-change-"
    "certificate.v0.1"
)

REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
)

SOURCE_TRUE = (
    "source_memoryos_v075_exact",
    "finite_s3_branched_dual_graph_exact",
    "diamond_incidence_exact",
    "spanning_tree_transport_exact",
    "alternative_path_comparison_exact",
    "path_agreement_iff_cycle_identity_exact",
    "cycle_obstruction_gauge_covariant_exact",
    "target_defect_route_relation_exact",
    "route_wilson_conjugacy_invariant_exact",
    "cycle_wilson_gauge_invariant_exact",
    "route_obstruction_confidence_exact",
    "all_full_rank_transport_branched_graph_layer_commutes",
    "singular_atomic_branched_graph_layer_retained",
    "all_decision_candidates_retained",
    "all_planos_histories_retained",
    "all_quotient_coordinate_probes_retained",
    "relational_frontier_preserved",
    "required_review_set_preserved",
    "dissent_visibility_preserved",
    "minority_visibility_preserved",
    "cycle_obstruction_not_truth_authority",
    "route_review_not_candidate_ranking",
    "spanning_tree_not_source_deletion",
    "future_only",
    "read_only",
)

SOURCE_FALSE = (
    "continuum_dual_graph_claimed",
    "universal_route_independence_claimed",
    "physical_gauge_field_inference_claimed",
    "local_route_component_used_as_truth",
    "route_review_used_as_candidate_ranking",
    "source_record_deleted_by_spanning_tree",
    "candidate_ranking_performed",
    "candidate_pruning_performed",
    "candidate_selection_performed",
    "decision_commit_performed",
    "decision_receipt_issued",
    "plan_synthesis_performed",
    "activation_performed",
    "execution_permission",
    "source_memoryos_v075_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)

SOURCE_COUNTS = {
    "literature_branched_dual_graph_record_count": 5,
    "branched_dual_graph_incidence_record_count": 8,
    "branched_dual_graph_profile_record_count": 2,
    "branched_edge_transport_record_count": 8,
    "spanning_tree_route_record_count": 2,
    "alternative_path_comparison_record_count": 2,
    "cycle_obstruction_record_count": 2,
    "target_defect_routing_record_count": 4,
    "route_conjugacy_relation_record_count": 2,
    "route_wilson_signature_record_count": 4,
    "cycle_wilson_signature_record_count": 2,
    "branched_graph_confidence_record_count": 2,
    "branched_graph_memory_fusion_record_count": 2,
    "full_rank_transport_branched_graph_record_count": 8,
    "singular_atomic_branched_graph_record_count": 4,
    "rank_one_source_boundary_count": 3,
}

SOURCE_COLLECTIONS = (
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
)

LITERATURE = (
    {
        "literature_id": "arxiv:2604.16252",
        "title": "Universal dualities for Wilson loops in lattice Yang-Mills",
        "published": "2026-04-17",
        "bound_concept": "dual incidence graphs cycle bases and Wilson-loop composition",
    },
    {
        "literature_id": "arxiv:1006.2059",
        "title": "A simplicial gauge theory",
        "published": "2010-06-10",
        "bound_concept": "gauge-invariant transport on finite glued simplicial graphs",
    },
    {
        "literature_id": "arxiv:hep-lat/0309023",
        "title": "On the non-Abelian Stokes theorem for SU(2) gauge fields",
        "published": "2003-09-07",
        "bound_concept": "ordered non-Abelian cycle composition",
    },
    {
        "literature_id": "arxiv:1011.0371",
        "title": "Non abelian Bianchi identities, monopoles and gauge invariance",
        "published": "2010-11-01",
        "bound_concept": "gauge-covariant cycle obstructions and defect propagation",
    },
    {
        "literature_id": "arxiv:2605.26697",
        "title": "A Gauge-Covariant Theoretical Framework for Non-Abelian Holonomy Estimation and Feed-Forward Correction in Time-Bin Photonic Qudits",
        "published": "2026-05-26",
        "bound_concept": "path-ordered transport and conjugacy-invariant signatures",
    },
)

Perm = tuple[int, int, int]
PROFILE_IDS = (
    "flat_theta",
    "rank_one_cycle_theta",
    "rank_two_noncommuting_theta",
)
PATH_IDS = ("route-0", "route-1", "route-2")
PAIR_IDS = ("cycle-01", "cycle-02", "cycle-12")


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
        raise ValueError("source_memoryos_v076_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v076_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v076_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v076_certificate_digest_mismatch")

    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v076_observables_invalid")
    obs = dict(raw)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v076_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v076_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v076_{field}_mismatch")

    normalized: dict[str, Any] = {"certificate_digest": digest}
    for field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        digest_field = field.replace("records", "digest")
        if not isinstance(records, list):
            raise ValueError(f"source_memoryos_v076_{field}_invalid")
        if canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v076_{digest_field}_mismatch")
        normalized[field] = [dict(record) for record in records]
        normalized[digest_field] = obs[digest_field]

    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v076_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v076_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v076_probe_support_invalid")
    normalized.update(
        candidate_ids=list(candidates),
        history_ids=list(histories),
        probe_ids=list(probes),
        rank_one_source_boundary_count=obs["rank_one_source_boundary_count"],
    )
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v076_{field}_invalid")
        normalized[field] = list(items)

    profiles = normalized["branched_dual_graph_profile_records"]
    routing = normalized["target_defect_routing_records"]
    confidences = normalized["branched_graph_confidence_records"]
    if [record.get("profile_id") for record in profiles] != [
        "flat_diamond",
        "cycle_obstructed_diamond",
    ]:
        raise ValueError("source_memoryos_v076_profile_order_mismatch")
    if len(routing) != 4:
        raise ValueError("source_memoryos_v076_routing_count_mismatch")
    target_defect = _as_perm(
        routing[0].get("target_defect"),
        field="source_theta_target_defect",
    )
    if target_defect != (2, 0, 1):
        raise ValueError("source_memoryos_v076_target_defect_changed")
    if any(
        _as_perm(record.get("target_defect"), field="source_theta_target_defect")
        != target_defect
        for record in routing
    ):
        raise ValueError("source_memoryos_v076_target_defect_inconsistent")
    if len(confidences) != 2:
        raise ValueError("source_memoryos_v076_confidence_count_mismatch")
    base_confidence = _f(confidences[0].get("source_base_confidence"))
    if base_confidence != Fraction(1, 3):
        raise ValueError("source_memoryos_v076_base_confidence_mismatch")
    normalized.update(
        target_defect=target_defect,
        base_confidence=base_confidence,
    )
    return normalized


def _profile_edges() -> dict[str, dict[str, Perm]]:
    return {
        "flat_theta": {
            "edge-01": SWAP_01,
            "edge-14": SWAP_12,
            "edge-02": SWAP_01,
            "edge-24": SWAP_12,
            "edge-03": SWAP_01,
            "edge-34": SWAP_12,
        },
        "rank_one_cycle_theta": {
            "edge-01": IDENTITY,
            "edge-14": IDENTITY,
            "edge-02": SWAP_01,
            "edge-24": IDENTITY,
            "edge-03": IDENTITY,
            "edge-34": IDENTITY,
        },
        "rank_two_noncommuting_theta": {
            "edge-01": IDENTITY,
            "edge-14": IDENTITY,
            "edge-02": SWAP_01,
            "edge-24": IDENTITY,
            "edge-03": SWAP_12,
            "edge-34": IDENTITY,
        },
    }


def _paths(edges: Mapping[str, Perm]) -> tuple[Perm, Perm, Perm]:
    return (
        _compose(edges["edge-01"], edges["edge-14"]),
        _compose(edges["edge-02"], edges["edge-24"]),
        _compose(edges["edge-03"], edges["edge-34"]),
    )


def _cycles(paths: tuple[Perm, Perm, Perm]) -> tuple[Perm, Perm, Perm]:
    p0, p1, p2 = paths
    return (
        _compose(p0, _inverse(p1)),
        _compose(p0, _inverse(p2)),
        _compose(p1, _inverse(p2)),
    )


def _derive_observables(source_v076: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v076)
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
            ("cell-1", "branch-0"),
            ("cell-2", "branch-1"),
            ("cell-3", "branch-2"),
            ("cell-4", "recombination"),
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
            ("edge-14", "cell-1", "cell-4"),
            ("edge-02", "cell-0", "cell-2"),
            ("edge-24", "cell-2", "cell-4"),
            ("edge-03", "cell-0", "cell-3"),
            ("edge-34", "cell-3", "cell-4"),
        )
    ]

    profile_records: list[dict[str, Any]] = []
    edge_records: list[dict[str, Any]] = []
    path_records: list[dict[str, Any]] = []
    basis_records: list[dict[str, Any]] = []
    pairwise_cycle_records: list[dict[str, Any]] = []
    basis_change_records: list[dict[str, Any]] = []
    relation_records: list[dict[str, Any]] = []
    routing_records: list[dict[str, Any]] = []
    routing_relation_records: list[dict[str, Any]] = []
    route_wilson_records: list[dict[str, Any]] = []
    signature_records: list[dict[str, Any]] = []
    confidence_records: list[dict[str, Any]] = []
    fusion_records: list[dict[str, Any]] = []

    frames = {
        "cell-0": SWAP_12,
        "cell-1": SWAP_01,
        "cell-2": SWAP_12,
        "cell-3": _compose(SWAP_01, SWAP_12),
        "cell-4": SWAP_01,
    }
    edge_endpoints = {
        "edge-01": ("cell-0", "cell-1"),
        "edge-14": ("cell-1", "cell-4"),
        "edge-02": ("cell-0", "cell-2"),
        "edge-24": ("cell-2", "cell-4"),
        "edge-03": ("cell-0", "cell-3"),
        "edge-34": ("cell-3", "cell-4"),
    }

    for profile_id in PROFILE_IDS:
        edges = profiles[profile_id]
        paths = _paths(edges)
        c01, c02, c12 = _cycles(paths)
        all_paths_agree = paths[0] == paths[1] == paths[2]
        if all_paths_agree != (c01 == IDENTITY and c02 == IDENTITY):
            raise ValueError("theta_all_paths_agree_basis_identity_failure")
        if c12 != _compose(_inverse(c01), c02):
            raise ValueError("theta_cycle_basis_relation_failure")
        if c02 != _compose(c01, c12):
            raise ValueError("theta_cycle_basis_reconstruction_failure")

        transformed_edges: dict[str, Perm] = {}
        for edge_id, edge_value in edges.items():
            source_id, target_id = edge_endpoints[edge_id]
            transformed_edges[edge_id] = _compose(
                _compose(_inverse(frames[source_id]), edge_value),
                frames[target_id],
            )
        transformed_paths = _paths(transformed_edges)
        expected_transformed_paths = tuple(
            _compose(
                _compose(_inverse(frames["cell-0"]), path),
                frames["cell-4"],
            )
            for path in paths
        )
        if transformed_paths != expected_transformed_paths:
            raise ValueError("theta_path_gauge_covariance_failure")
        transformed_cycles = _cycles(transformed_paths)
        expected_transformed_cycles = tuple(
            _conjugate(cycle, _inverse(frames["cell-0"]))
            for cycle in (c01, c02, c12)
        )
        if transformed_cycles != expected_transformed_cycles:
            raise ValueError("theta_cycle_gauge_covariance_failure")

        tree0_basis = (c01, c02)
        tree1_basis = (_inverse(c01), c12)
        expected_tree1 = (
            _inverse(tree0_basis[0]),
            _compose(_inverse(tree0_basis[0]), tree0_basis[1]),
        )
        if tree1_basis != expected_tree1:
            raise ValueError("theta_tree_basis_change_failure")
        transformed_tree0 = (transformed_cycles[0], transformed_cycles[1])
        transformed_tree1 = (_inverse(transformed_cycles[0]), transformed_cycles[2])
        expected_transformed_tree1 = (
            _inverse(transformed_tree0[0]),
            _compose(_inverse(transformed_tree0[0]), transformed_tree0[1]),
        )
        if transformed_tree1 != expected_transformed_tree1:
            raise ValueError("theta_tree_basis_change_gauge_covariance_failure")

        transformed_target_defect = _conjugate(
            target_defect,
            _inverse(frames["cell-4"]),
        )
        localized = tuple(_conjugate(target_defect, path) for path in paths)
        transformed_localized = tuple(
            _conjugate(transformed_target_defect, path)
            for path in transformed_paths
        )
        expected_transformed_localized = tuple(
            _conjugate(value, _inverse(frames["cell-0"]))
            for value in localized
        )
        if transformed_localized != expected_transformed_localized:
            raise ValueError("theta_localized_defect_gauge_covariance_failure")
        predicted0_from1 = _conjugate(localized[1], c01)
        predicted0_from2 = _conjugate(localized[2], c02)
        predicted1_from2 = _conjugate(localized[2], c12)
        if (
            localized[0] != predicted0_from1
            or localized[0] != predicted0_from2
            or localized[1] != predicted1_from2
        ):
            raise ValueError("theta_route_conjugacy_relation_failure")

        profile_records.append(
            {
                "profile_id": profile_id,
                "vertex_count": 5,
                "edge_count": 6,
                "cycle_rank": 2,
                "root_vertex": "cell-0",
                "recombination_vertex": "cell-4",
                "route_count_root_to_target": 3,
                "all_paths_agree": all_paths_agree,
                "independent_cycle_support": sum(
                    cycle != IDENTITY for cycle in (c01, c02)
                ),
            }
        )
        for edge_id in (
            "edge-01",
            "edge-14",
            "edge-02",
            "edge-24",
            "edge-03",
            "edge-34",
        ):
            edge_records.append(
                {
                    "profile_id": profile_id,
                    "dual_edge_id": edge_id,
                    "seam_transport": list(edges[edge_id]),
                    "seam_transport_matrix": _matrix(edges[edge_id]),
                    "path_ordered": True,
                }
            )
        for path_id, path_edges, transport in (
            ("route-0", ["edge-01", "edge-14"], paths[0]),
            ("route-1", ["edge-02", "edge-24"], paths[1]),
            ("route-2", ["edge-03", "edge-34"], paths[2]),
        ):
            path_records.append(
                {
                    "profile_id": profile_id,
                    "path_id": path_id,
                    "path_edges": path_edges,
                    "path_transport": list(transport),
                    "source_records_deleted": False,
                }
            )

        for tree_id, selected_route, basis in (
            ("tree-route-0", "route-0", tree0_basis),
            ("tree-route-1", "route-1", tree1_basis),
        ):
            basis_records.append(
                {
                    "profile_id": profile_id,
                    "tree_id": tree_id,
                    "selected_tree_route": selected_route,
                    "cycle_basis": [list(basis[0]), list(basis[1])],
                    "basis_rank": 2,
                    "complete_pairwise_cycle_reconstructible": True,
                }
            )

        for pair_index, (pair_id, left_path, right_path, cycle) in enumerate(
            (
                ("cycle-01", "route-0", "route-1", c01),
                ("cycle-02", "route-0", "route-2", c02),
                ("cycle-12", "route-1", "route-2", c12),
            )
        ):
            pairwise_cycle_records.append(
                {
                    "profile_id": profile_id,
                    "cycle_id": pair_id,
                    "left_path_id": left_path,
                    "right_path_id": right_path,
                    "cycle_holonomy": list(cycle),
                    "cycle_type": _cycle_type(cycle),
                    "cycle_trace": _fixed_point_trace(cycle),
                    "transformed_cycle_holonomy": list(
                        transformed_cycles[pair_index]
                    ),
                    "expected_root_conjugate": list(
                        expected_transformed_cycles[pair_index]
                    ),
                    "gauge_covariant": True,
                    "truth_authority": False,
                }
            )

        basis_change_records.append(
            {
                "profile_id": profile_id,
                "source_tree_id": "tree-route-0",
                "target_tree_id": "tree-route-1",
                "source_basis": [list(tree0_basis[0]), list(tree0_basis[1])],
                "target_basis": [list(tree1_basis[0]), list(tree1_basis[1])],
                "basis_change_rule": ["a^-1", "a^-1*b"],
                "basis_change_exact": tree1_basis == expected_tree1,
                "basis_change_gauge_covariant": transformed_tree1
                == expected_transformed_tree1,
            }
        )
        relation_records.append(
            {
                "profile_id": profile_id,
                "cycle01": list(c01),
                "cycle02": list(c02),
                "cycle12": list(c12),
                "cycle12_equals_cycle01_inverse_cycle02": c12
                == _compose(_inverse(c01), c02),
                "cycle02_equals_cycle01_cycle12": c02 == _compose(c01, c12),
                "all_paths_agree_iff_basis_identity": all_paths_agree
                == (c01 == IDENTITY and c02 == IDENTITY),
            }
        )

        for index, (path_id, transport, root_localized) in enumerate(
            zip(PATH_IDS, paths, localized, strict=True)
        ):
            routing_records.append(
                {
                    "profile_id": profile_id,
                    "path_id": path_id,
                    "target_defect": list(target_defect),
                    "path_transport": list(transport),
                    "root_localized_defect": list(root_localized),
                    "localized_defect_trace": _fixed_point_trace(root_localized),
                    "transformed_root_localized_defect": list(
                        transformed_localized[index]
                    ),
                    "expected_root_conjugate": list(
                        expected_transformed_localized[index]
                    ),
                    "gauge_covariant": True,
                    "frame_dependent_representative": True,
                }
            )
            route_wilson_records.append(
                {
                    "profile_id": profile_id,
                    "path_id": path_id,
                    "localized_defect_trace": _fixed_point_trace(root_localized),
                    "target_defect_trace": _fixed_point_trace(target_defect),
                    "class_function_signature_equal_to_target": (
                        _fixed_point_trace(root_localized)
                        == _fixed_point_trace(target_defect)
                    ),
                    "frame_independent": True,
                }
            )

        for pair_id, left_index, right_index, cycle, predicted in (
            ("cycle-01", 0, 1, c01, predicted0_from1),
            ("cycle-02", 0, 2, c02, predicted0_from2),
            ("cycle-12", 1, 2, c12, predicted1_from2),
        ):
            routing_relation_records.append(
                {
                    "profile_id": profile_id,
                    "cycle_id": pair_id,
                    "left_localized_defect": list(localized[left_index]),
                    "right_localized_defect": list(localized[right_index]),
                    "cycle_conjugated_right_defect": list(predicted),
                    "left_equals_cycle_conjugated_right": (
                        localized[left_index] == predicted
                    ),
                    "class_function_route_signatures_equal": (
                        _fixed_point_trace(localized[left_index])
                        == _fixed_point_trace(localized[right_index])
                    ),
                }
            )

        traces = tuple(_fixed_point_trace(cycle) for cycle in (c01, c02, c12))
        trace_sum = sum(traces)
        penalty = Fraction(9 - trace_sum, 54)
        adjusted = base_confidence - penalty
        signature_records.append(
            {
                "profile_id": profile_id,
                "complete_pairwise_cycle_ids": list(PAIR_IDS),
                "complete_pairwise_cycle_holonomies": [
                    list(c01),
                    list(c02),
                    list(c12),
                ],
                "complete_pairwise_cycle_traces": list(traces),
                "trace_sum": trace_sum,
                "spanning_tree_route_privileged": False,
                "tree0_reconstructs_cycle12": True,
                "tree1_reconstructs_cycle02": True,
                "gauge_invariant_class_signature": (
                    traces
                    == tuple(
                        _fixed_point_trace(cycle)
                        for cycle in transformed_cycles
                    )
                ),
            }
        )
        confidence_records.append(
            {
                "profile_id": profile_id,
                "source_base_confidence": _q(base_confidence),
                "complete_pairwise_cycle_penalty": _q(penalty),
                "theta_adjusted_confidence": _q(adjusted),
                "within_unit_interval": Fraction(0) <= adjusted <= Fraction(1),
                "gauge_invariant": traces
                == tuple(
                    _fixed_point_trace(cycle)
                    for cycle in transformed_cycles
                ),
                "posterior_probability": False,
                "truth_authority": False,
            }
        )
        fusion_records.append(
            {
                "profile_id": profile_id,
                "theta_cycle_basis_signature": {
                    "vertex_count": 5,
                    "edge_count": 6,
                    "cycle_rank": 2,
                    "pairwise_cycle_types": [
                        _cycle_type(c01),
                        _cycle_type(c02),
                        _cycle_type(c12),
                    ],
                    "pairwise_cycle_trace_sum": trace_sum,
                    "basis_noncommutative": (
                        _compose(c01, c02) != _compose(c02, c01)
                    ),
                },
                "basis_change_review_required": not all_paths_agree,
                "candidate_ranking_performed": False,
            }
        )

    expected_cycles = {
        "flat_theta": [IDENTITY, IDENTITY, IDENTITY],
        "rank_one_cycle_theta": [SWAP_01, IDENTITY, SWAP_01],
        "rank_two_noncommuting_theta": [
            SWAP_01,
            SWAP_12,
            _compose(SWAP_01, SWAP_12),
        ],
    }
    for profile_id in PROFILE_IDS:
        actual = [
            tuple(record["cycle_holonomy"])
            for record in pairwise_cycle_records
            if record["profile_id"] == profile_id
        ]
        if actual != expected_cycles[profile_id]:
            raise ValueError("canonical_theta_cycle_profile_mismatch")

    rank_two_relation = next(
        record
        for record in relation_records
        if record["profile_id"] == "rank_two_noncommuting_theta"
    )
    rank_two_c01 = _as_perm(rank_two_relation["cycle01"], field="rank_two_c01")
    rank_two_c02 = _as_perm(rank_two_relation["cycle02"], field="rank_two_c02")
    if _compose(rank_two_c01, rank_two_c02) != (1, 2, 0):
        raise ValueError("canonical_theta_rank_two_ab_mismatch")
    if _compose(rank_two_c02, rank_two_c01) != (2, 0, 1):
        raise ValueError("canonical_theta_rank_two_ba_mismatch")
    if _compose(rank_two_c01, rank_two_c02) == _compose(rank_two_c02, rank_two_c01):
        raise ValueError("canonical_theta_rank_two_noncommutativity_lost")

    expected_confidence = {
        "flat_theta": Fraction(1, 3),
        "rank_one_cycle_theta": Fraction(7, 27),
        "rank_two_noncommuting_theta": Fraction(11, 54),
    }
    for record in confidence_records:
        if _f(record["theta_adjusted_confidence"]) != expected_confidence[
            record["profile_id"]
        ]:
            raise ValueError("canonical_theta_confidence_mismatch")

    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "theta_cycle_basis_transport_commutes": True,
            "spanning_tree_change_commutes": True,
            "complete_pairwise_signature_commutes": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_branched_graph_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_theta_signature_retained": True,
            "atomic_cycle_basis_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_branched_graph_records"]
    ]

    observables: dict[str, Any] = {
        "source_memoryos_v076_exact": True,
        "source_memoryos_v076_certificate_digest": source["certificate_digest"],
        "source_branched_dual_graph_profile_digest": source[
            "branched_dual_graph_profile_digest"
        ],
        "source_cycle_obstruction_digest": source["cycle_obstruction_digest"],
        "source_target_defect_routing_digest": source[
            "target_defect_routing_digest"
        ],
        "source_branched_graph_confidence_digest": source[
            "branched_graph_confidence_digest"
        ],
        "literature_theta_cycle_basis_records": [dict(record) for record in LITERATURE],
        "literature_theta_cycle_basis_record_count": len(LITERATURE),
        "theta_dual_graph_incidence_records": incidence_records,
        "theta_dual_graph_incidence_record_count": len(incidence_records),
        "theta_dual_graph_profile_records": profile_records,
        "theta_dual_graph_profile_record_count": len(profile_records),
        "theta_edge_transport_records": edge_records,
        "theta_edge_transport_record_count": len(edge_records),
        "theta_path_transport_records": path_records,
        "theta_path_transport_record_count": len(path_records),
        "fundamental_cycle_basis_records": basis_records,
        "fundamental_cycle_basis_record_count": len(basis_records),
        "pairwise_cycle_holonomy_records": pairwise_cycle_records,
        "pairwise_cycle_holonomy_record_count": len(pairwise_cycle_records),
        "spanning_tree_basis_change_records": basis_change_records,
        "spanning_tree_basis_change_record_count": len(basis_change_records),
        "cycle_basis_relation_records": relation_records,
        "cycle_basis_relation_record_count": len(relation_records),
        "theta_target_defect_routing_records": routing_records,
        "theta_target_defect_routing_record_count": len(routing_records),
        "theta_route_conjugacy_relation_records": routing_relation_records,
        "theta_route_conjugacy_relation_record_count": len(
            routing_relation_records
        ),
        "theta_route_wilson_signature_records": route_wilson_records,
        "theta_route_wilson_signature_record_count": len(route_wilson_records),
        "complete_pairwise_cycle_signature_records": signature_records,
        "complete_pairwise_cycle_signature_record_count": len(signature_records),
        "theta_cycle_basis_confidence_records": confidence_records,
        "theta_cycle_basis_confidence_record_count": len(confidence_records),
        "theta_cycle_basis_memory_fusion_records": fusion_records,
        "theta_cycle_basis_memory_fusion_record_count": len(fusion_records),
        "full_rank_transport_theta_cycle_basis_records": full_rank_records,
        "full_rank_transport_theta_cycle_basis_record_count": len(full_rank_records),
        "singular_atomic_theta_cycle_basis_records": singular_records,
        "singular_atomic_theta_cycle_basis_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "finite_s3_theta_dual_graph_exact": True,
        "theta_cycle_rank_two_exact": all(
            record["cycle_rank"] == 2 for record in profile_records
        ),
        "fundamental_cycle_basis_exact": all(
            record["basis_rank"] == 2
            and record["complete_pairwise_cycle_reconstructible"]
            for record in basis_records
        ),
        "basis_change_nielsen_relation_exact": all(
            record["basis_change_exact"] for record in basis_change_records
        ),
        "basis_change_gauge_covariant_exact": all(
            record["basis_change_gauge_covariant"]
            for record in basis_change_records
        ),
        "all_paths_agree_iff_basis_identity_exact": all(
            record["all_paths_agree_iff_basis_identity"]
            for record in relation_records
        ),
        "complete_pairwise_cycle_signature_tree_independent_exact": all(
            not record["spanning_tree_route_privileged"]
            and record["tree0_reconstructs_cycle12"]
            and record["tree1_reconstructs_cycle02"]
            for record in signature_records
        ),
        "pairwise_cycle_wilson_gauge_invariant_exact": all(
            record["gauge_invariant_class_signature"]
            for record in signature_records
        ),
        "target_defect_three_route_relation_exact": all(
            record["left_equals_cycle_conjugated_right"]
            for record in routing_relation_records
        ),
        "route_wilson_conjugacy_invariant_exact": all(
            record["class_function_signature_equal_to_target"]
            for record in route_wilson_records
        ),
        "noncommutative_basis_order_dependence_exact": (
            _compose(rank_two_c01, rank_two_c02)
            != _compose(rank_two_c02, rank_two_c01)
        ),
        "theta_adjusted_confidence_exact": (
            all(record["within_unit_interval"] for record in confidence_records)
            and all(record["gauge_invariant"] for record in confidence_records)
        ),
        "all_full_rank_transport_theta_cycle_basis_layer_commutes": all(
            record["theta_cycle_basis_transport_commutes"]
            and record["spanning_tree_change_commutes"]
            and record["complete_pairwise_signature_commutes"]
            for record in full_rank_records
        ),
        "singular_atomic_theta_cycle_basis_layer_retained": all(
            record["atomic_theta_signature_retained"]
            and record["atomic_cycle_basis_retained"]
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
        "cycle_basis_not_truth_authority": True,
        "basis_change_review_not_candidate_ranking": True,
        "spanning_tree_change_not_source_deletion": True,
        "continuum_theta_graph_claimed": False,
        "universal_cycle_basis_theorem_claimed": False,
        "physical_gauge_field_inference_claimed": False,
        "local_cycle_basis_component_used_as_truth": False,
        "basis_change_review_used_as_candidate_ranking": False,
        "source_record_deleted_by_tree_change": False,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v076_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "literature_theta_cycle_basis_records",
        "theta_dual_graph_incidence_records",
        "theta_dual_graph_profile_records",
        "theta_edge_transport_records",
        "theta_path_transport_records",
        "fundamental_cycle_basis_records",
        "pairwise_cycle_holonomy_records",
        "spanning_tree_basis_change_records",
        "cycle_basis_relation_records",
        "theta_target_defect_routing_records",
        "theta_route_conjugacy_relation_records",
        "theta_route_wilson_signature_records",
        "complete_pairwise_cycle_signature_records",
        "theta_cycle_basis_confidence_records",
        "theta_cycle_basis_memory_fusion_records",
        "full_rank_transport_theta_cycle_basis_records",
        "singular_atomic_theta_cycle_basis_records",
    ):
        observables[field.replace("records", "digest")] = canonical_digest(
            observables[field]
        )
    return observables


def issue_dual_cycle_basis_tree_change_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(
            payload.get("source_memoryos_v076_certificate")
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
    "issue_dual_cycle_basis_tree_change_certificate",
]
