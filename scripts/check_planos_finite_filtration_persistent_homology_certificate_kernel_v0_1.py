#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_finite_filtration_persistent_homology_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_finite_filtration_persistent_homology_certificate,
)
from runtime.kuuos_planos_finite_filtration_persistent_homology_certificate_support_v0_1 import (
    compute_persistent_homology_input_digest,
)


def vertices() -> list[dict]:
    return [
        {
            "vertex_id": vertex,
            "filtration": 0,
            "source_vertex_digest": f"source-filtered-vertex-{vertex}",
        }
        for vertex in ["A", "B", "C"]
    ]


def edges() -> list[dict]:
    return [
        {
            "edge_id": f"edge-{pair}",
            "vertex_ids": list(pair),
            "filtration": 1,
            "source_edge_digest": f"source-filtered-edge-{pair}",
        }
        for pair in ["AB", "AC", "BC"]
    ]


def triangles() -> list[dict]:
    return [
        {
            "triangle_id": "triangle-ABC",
            "vertex_ids": ["A", "B", "C"],
            "filtration": 2,
            "source_triangle_digest": "source-filtered-triangle-ABC",
        }
    ]


def stages() -> list[int]:
    return [0, 1, 2]


def stage_smith_data() -> list[dict]:
    return [
        {"stage": 0, "vertex_count": 3, "edge_count": 0, "triangle_count": 0, "h0_free_rank": 3, "h1_free_rank": 0, "h2_free_rank": 0, "h1_smith_diagonal": [], "h1_torsion_invariant_factors": []},
        {"stage": 1, "vertex_count": 3, "edge_count": 3, "triangle_count": 0, "h0_free_rank": 1, "h1_free_rank": 1, "h2_free_rank": 0, "h1_smith_diagonal": [], "h1_torsion_invariant_factors": []},
        {"stage": 2, "vertex_count": 3, "edge_count": 3, "triangle_count": 1, "h0_free_rank": 1, "h1_free_rank": 0, "h2_free_rank": 0, "h1_smith_diagonal": [1], "h1_torsion_invariant_factors": []},
    ]


def barcode_intervals() -> list[dict]:
    return [
        {"interval_id": "H0:vertex-B->edge-AB", "dimension": 0, "birth": 0, "death": 1, "birth_simplex_id": "vertex-B", "death_simplex_id": "edge-AB"},
        {"interval_id": "H0:vertex-C->edge-AC", "dimension": 0, "birth": 0, "death": 1, "birth_simplex_id": "vertex-C", "death_simplex_id": "edge-AC"},
        {"interval_id": "H0:vertex-A->inf", "dimension": 0, "birth": 0, "death": None, "birth_simplex_id": "vertex-A", "death_simplex_id": ""},
        {"interval_id": "H1:edge-BC->triangle-ABC", "dimension": 1, "birth": 1, "death": 2, "birth_simplex_id": "edge-BC", "death_simplex_id": "triangle-ABC"},
    ]


def persistent_betti() -> list[dict]:
    return [
        {"stage": 0, "beta0": 3, "beta1": 0, "beta2": 0},
        {"stage": 1, "beta0": 1, "beta1": 1, "beta2": 0},
        {"stage": 2, "beta0": 1, "beta1": 0, "beta2": 0},
    ]


def build(**overrides):
    vertex_records = overrides.pop("filtered_vertex_records", vertices())
    edge_records = overrides.pop("filtered_edge_records", edges())
    triangle_records = overrides.pop("filtered_triangle_records", triangles())
    filtration_stages = overrides.pop("filtration_stages", stages())
    stage_claims = overrides.pop("claimed_stage_smith_data", stage_smith_data())
    intervals = overrides.pop("claimed_barcode_intervals", barcode_intervals())
    betti = overrides.pop("claimed_persistent_betti", persistent_betti())
    digest = overrides.pop(
        "persistent_homology_input_digest",
        compute_persistent_homology_input_digest(
            filtered_vertex_records=vertex_records,
            filtered_edge_records=edge_records,
            filtered_triangle_records=triangle_records,
            filtration_stages=filtration_stages,
            claimed_stage_smith_data=stage_claims,
            claimed_barcode_intervals=intervals,
            claimed_persistent_betti=betti,
        ),
    )
    args = {
        "source_integer_homology_certificate_digest": "planos-v1-16-integer-homology-certificate",
        "source_nerve_certificate_digest": "planos-v1-14-nerve-certificate",
        "persistent_homology_input_digest": digest,
        "filtered_vertex_records": vertex_records,
        "filtered_edge_records": edge_records,
        "filtered_triangle_records": triangle_records,
        "filtration_stages": filtration_stages,
        "claimed_stage_smith_data": stage_claims,
        "claimed_barcode_intervals": intervals,
        "claimed_persistent_betti": betti,
        "maximum_filtration_value": 10,
        "maximum_simplex_count": 20,
    }
    args.update(overrides)
    return build_finite_filtration_persistent_homology_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    cert = result.certificate
    assert cert["filtration_stages"] == [0, 1, 2]
    assert cert["stage_smith_data"] == stage_smith_data()
    assert cert["barcode_intervals"] == barcode_intervals()
    assert cert["persistent_betti"] == persistent_betti()
    assert cert["finite_interval_count"] == 3
    assert cert["infinite_interval_count"] == 1
    assert cert["coefficient_fields"] == {"stagewise_integer_homology": "Z", "barcode_reduction": "F2"}
    for name in (
        "face_closure_verified", "filtration_monotonicity_verified", "stagewise_integer_smith_data_recomputed",
        "f2_boundary_matrix_reduced", "birth_death_pairing_recomputed", "barcode_intervals_verified",
        "persistent_betti_verified", "finite_filtration_only", "dimensions_above_two_not_computed",
        "integer_persistence_module_not_computed", "zigzag_persistence_not_computed", "stability_theorem_not_claimed",
        "planning_space_persistent_homology_not_claimed", "global_topological_invariant_not_claimed",
        "barcode_does_not_rank_candidates", "candidate_identity_retained", "source_integer_homology_certificate_not_mutated",
        "source_nerve_certificate_not_mutated", "persistent_world_state_unchanged", "history_read_only",
        "persistent_homology_grants_no_authority", "barcode_interval_grants_no_authority",
        "persistent_betti_grants_no_authority", "topological_obstruction_grants_no_authority", "future_only",
    ):
        assert cert[name] is True
    assert cert["decision_selection_performed"] is False
    assert cert["active_now"] is False
    assert cert["execution_permission"] is False

    blocked = [
        build(source_integer_homology_certificate_digest=""),
        build(source_nerve_certificate_digest=""),
        build(persistent_homology_input_digest="stale"),
        build(filtered_vertex_records=[]),
        build(filtration_stages=[0, 2]),
        build(maximum_filtration_value=-1),
        build(maximum_simplex_count=3),
    ]
    duplicate_vertex = vertices(); duplicate_vertex[1]["vertex_id"] = duplicate_vertex[0]["vertex_id"]
    blocked.append(build(filtered_vertex_records=duplicate_vertex))
    duplicate_edge = edges(); duplicate_edge[1]["vertex_ids"] = duplicate_edge[0]["vertex_ids"]
    blocked.append(build(filtered_edge_records=duplicate_edge))
    early_edge = edges(); early_edge[0]["filtration"] = 0
    late_vertex = vertices(); late_vertex[0]["filtration"] = 1
    blocked.append(build(filtered_vertex_records=late_vertex, filtered_edge_records=early_edge))
    early_triangle = triangles(); early_triangle[0]["filtration"] = 0
    blocked.append(build(filtered_triangle_records=early_triangle))
    blocked.append(build(filtered_edge_records=edges()[:-1]))
    wrong_stage = stage_smith_data(); wrong_stage[1]["h1_free_rank"] = 0
    blocked.append(build(claimed_stage_smith_data=wrong_stage))
    wrong_barcode = barcode_intervals(); wrong_barcode[-1]["death"] = 3
    blocked.append(build(claimed_barcode_intervals=wrong_barcode))
    wrong_betti = persistent_betti(); wrong_betti[1]["beta1"] = 0
    blocked.append(build(claimed_persistent_betti=wrong_betti))
    collision_edges = edges(); collision_edges[0]["edge_id"] = "vertex-A"
    blocked.append(build(filtered_edge_records=collision_edges))
    for item in blocked:
        assert item.status != STATUS_READY and item.blockers and item.certificate is None

    tampered = deepcopy(triangles())
    stale_digest = compute_persistent_homology_input_digest(
        filtered_vertex_records=vertices(), filtered_edge_records=edges(), filtered_triangle_records=tampered,
        filtration_stages=stages(), claimed_stage_smith_data=stage_smith_data(),
        claimed_barcode_intervals=barcode_intervals(), claimed_persistent_betti=persistent_betti(),
    )
    tampered[0]["source_triangle_digest"] = "tampered"
    item = build(filtered_triangle_records=tampered, persistent_homology_input_digest=stale_digest)
    assert item.status != STATUS_READY and item.certificate is None

    print("PASS: PlanOS Finite Filtration Persistent Homology Certificate Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
