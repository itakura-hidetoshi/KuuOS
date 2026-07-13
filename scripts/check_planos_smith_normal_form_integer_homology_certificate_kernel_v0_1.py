#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_smith_normal_form_integer_homology_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_smith_normal_form_integer_homology_certificate,
    compute_integer_homology_input_digest,
)


def vertices() -> list[dict]:
    return [
        {"vertex_id": vertex, "source_vertex_digest": f"source-vertex-{vertex}"}
        for vertex in ["A", "B", "C", "D", "E", "F"]
    ]


def edges() -> list[dict]:
    pairs = [
        "AB", "AC", "AD", "AE", "AF",
        "BC", "BD", "BE", "BF",
        "CD", "CE", "CF",
        "DE", "DF", "EF",
    ]
    return [
        {
            "edge_id": f"edge-{pair}",
            "vertex_ids": list(pair),
            "source_edge_digest": f"source-edge-{pair}",
        }
        for pair in pairs
    ]


def triangles() -> list[dict]:
    triples = [
        "ABC", "ABD", "ACE", "ADF", "AEF",
        "BCF", "BDE", "BEF", "CDE", "CDF",
    ]
    return [
        {
            "triangle_id": f"triangle-{triple}",
            "vertex_ids": list(triple),
            "source_triangle_digest": f"source-triangle-{triple}",
        }
        for triple in triples
    ]


def build(**overrides):
    vertex_records = overrides.pop("vertex_records", vertices())
    edge_records = overrides.pop("oriented_edge_records", edges())
    triangle_records = overrides.pop("oriented_triangle_records", triangles())
    claimed = overrides.pop("claimed_smith_diagonal", [1] * 9 + [2])
    h0 = overrides.pop("expected_h0_free_rank", 1)
    h1 = overrides.pop("expected_h1_free_rank", 0)
    h2 = overrides.pop("expected_h2_free_rank", 0)
    torsion = overrides.pop("expected_torsion_invariant_factors", [2])
    digest = overrides.pop(
        "smith_input_digest",
        compute_integer_homology_input_digest(
            vertex_records=vertex_records,
            oriented_edge_records=edge_records,
            oriented_triangle_records=triangle_records,
            claimed_smith_diagonal=claimed,
            expected_h0_free_rank=h0,
            expected_h1_free_rank=h1,
            expected_h2_free_rank=h2,
            expected_torsion_invariant_factors=torsion,
        ),
    )
    args = {
        "source_chain_homology_certificate_digest": "planos-v1-15-chain-homology-certificate",
        "source_nerve_certificate_digest": "planos-v1-14-nerve-certificate",
        "smith_input_digest": digest,
        "vertex_records": vertex_records,
        "oriented_edge_records": edge_records,
        "oriented_triangle_records": triangle_records,
        "claimed_smith_diagonal": claimed,
        "expected_h0_free_rank": h0,
        "expected_h1_free_rank": h1,
        "expected_h2_free_rank": h2,
        "expected_torsion_invariant_factors": torsion,
        "maximum_basis_size": 20,
    }
    args.update(overrides)
    return build_smith_normal_form_integer_homology_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    cert = result.certificate
    assert cert["connected_component_count"] == 1
    assert cert["cycle_lattice_rank"] == 10
    assert cert["smith_rank"] == 10
    assert cert["smith_diagonal"] == [1] * 9 + [2]
    assert cert["torsion_invariant_factors"] == [2]
    assert cert["integer_h1_decomposition"] == {
        "free_rank": 0,
        "torsion_invariant_factors": [2],
    }
    assert cert["h0_free_rank"] == 1
    assert cert["h1_free_rank"] == 0
    assert cert["h2_free_rank"] == 0
    assert len(cert["spanning_forest_tree_edge_ids"]) == 5
    assert len(cert["fundamental_cycle_chord_edge_ids"]) == 10
    for name in (
        "boundary_squared_zero_verified",
        "fundamental_cycle_basis_verified",
        "triangle_boundaries_reconstructed_in_cycle_basis",
        "smith_diagonal_recomputed_by_unimodular_operations",
        "smith_divisibility_chain_verified",
        "integer_homology_decomposition_verified",
        "torsion_invariant_factors_retained",
        "finite_integral_chain_complex_only",
        "unimodular_transform_matrices_not_retained",
        "higher_dimensional_homology_not_computed",
        "persistent_homology_not_computed",
        "global_integer_homology_not_claimed",
        "classical_cech_homology_equivalence_not_claimed",
        "global_topological_invariant_not_claimed",
        "candidate_identity_retained",
        "source_chain_homology_certificate_not_mutated",
        "source_nerve_certificate_not_mutated",
        "persistent_world_state_unchanged",
        "history_read_only",
        "smith_normal_form_grants_no_authority",
        "integer_homology_grants_no_authority",
        "torsion_invariant_grants_no_authority",
        "topological_obstruction_grants_no_authority",
        "future_only",
    ):
        assert cert[name] is True
    assert cert["decision_selection_performed"] is False
    assert cert["active_now"] is False
    assert cert["execution_permission"] is False

    blocked = [
        build(source_chain_homology_certificate_digest=""),
        build(source_nerve_certificate_digest=""),
        build(smith_input_digest="stale"),
        build(vertex_records=[]),
        build(oriented_edge_records=[]),
        build(oriented_triangle_records=[]),
        build(claimed_smith_diagonal=[]),
        build(claimed_smith_diagonal=[2, 3]),
        build(expected_h0_free_rank=-1),
        build(expected_h1_free_rank=1),
        build(expected_h2_free_rank=1),
        build(expected_torsion_invariant_factors=[]),
        build(expected_torsion_invariant_factors=[4]),
        build(maximum_basis_size=5),
    ]

    duplicate_vertex = vertices()
    duplicate_vertex[1]["vertex_id"] = duplicate_vertex[0]["vertex_id"]
    blocked.append(build(vertex_records=duplicate_vertex))

    duplicate_edge = edges()
    duplicate_edge[1]["vertex_ids"] = duplicate_edge[0]["vertex_ids"]
    blocked.append(build(oriented_edge_records=duplicate_edge))

    duplicate_triangle = triangles()
    duplicate_triangle[1]["vertex_ids"] = duplicate_triangle[0]["vertex_ids"]
    blocked.append(build(oriented_triangle_records=duplicate_triangle))

    missing_vertex_edge = edges()
    missing_vertex_edge[0]["vertex_ids"] = ["A", "Z"]
    blocked.append(build(oriented_edge_records=missing_vertex_edge))

    missing_boundary_edge = edges()[:-1]
    blocked.append(build(oriented_edge_records=missing_boundary_edge))

    wrong_smith = [1] * 10
    blocked.append(build(claimed_smith_diagonal=wrong_smith))

    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    tampered = deepcopy(triangles())
    stale_digest = compute_integer_homology_input_digest(
        vertex_records=vertices(),
        oriented_edge_records=edges(),
        oriented_triangle_records=tampered,
        claimed_smith_diagonal=[1] * 9 + [2],
        expected_h0_free_rank=1,
        expected_h1_free_rank=0,
        expected_h2_free_rank=0,
        expected_torsion_invariant_factors=[2],
    )
    tampered[0]["source_triangle_digest"] = "tampered"
    item = build(oriented_triangle_records=tampered, smith_input_digest=stale_digest)
    assert item.status != STATUS_READY and item.certificate is None

    print(
        "PASS: PlanOS Smith Normal Form and Integer Homology Certificate Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
