#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_finite_simplicial_chain_homology_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_finite_simplicial_chain_homology_certificate,
)
from runtime.kuuos_planos_finite_simplicial_chain_homology_certificate_support_v0_1 import (
    compute_chain_complex_input_digest,
)


def vertices() -> list[dict]:
    return [
        {"vertex_id": vertex, "source_vertex_digest": f"nerve-vertex-{vertex}"}
        for vertex in ("A", "B", "C", "D")
    ]


def edges() -> list[dict]:
    return [
        {"edge_id": "AB", "vertex_ids": ["A", "B"], "source_edge_digest": "edge-AB"},
        {"edge_id": "AC", "vertex_ids": ["A", "C"], "source_edge_digest": "edge-AC"},
        {"edge_id": "AD", "vertex_ids": ["A", "D"], "source_edge_digest": "edge-AD"},
        {"edge_id": "BC", "vertex_ids": ["B", "C"], "source_edge_digest": "edge-BC"},
        {"edge_id": "CD", "vertex_ids": ["C", "D"], "source_edge_digest": "edge-CD"},
    ]


def triangles() -> list[dict]:
    return [
        {
            "triangle_id": "ABC",
            "vertex_ids": ["A", "B", "C"],
            "source_triangle_digest": "triangle-ABC",
        }
    ]


def one_chains() -> list[dict]:
    return [
        {
            "chain_id": "cycle-boundary-ABC",
            "edge_coefficients": {"AB": 1, "AC": -1, "BC": 1},
            "chain_role": "exact_cycle",
            "source_chain_digest": "one-chain-boundary-ABC",
        },
        {
            "chain_id": "cycle-hole-ACD",
            "edge_coefficients": {"AC": 1, "AD": -1, "CD": 1},
            "chain_role": "nontrivial_cycle",
            "source_chain_digest": "one-chain-hole-ACD",
        },
    ]


def two_chains() -> list[dict]:
    return [
        {
            "chain_id": "fill-ABC",
            "triangle_coefficients": {"ABC": 1},
            "source_chain_digest": "two-chain-fill-ABC",
        }
    ]


def exactness() -> list[dict]:
    return [
        {
            "witness_id": "exact-ABC",
            "one_chain_id": "cycle-boundary-ABC",
            "two_chain_id": "fill-ABC",
            "source_witness_digest": "exactness-witness-ABC",
        }
    ]


def nontriviality() -> list[dict]:
    return [
        {
            "witness_id": "nontrivial-ACD-over-Q",
            "one_chain_id": "cycle-hole-ACD",
            "coefficient_field": "Q",
            "source_witness_digest": "nontriviality-witness-ACD",
        }
    ]


def build(**overrides):
    vertex_records = overrides.pop("vertex_records", vertices())
    edge_records = overrides.pop("oriented_edge_records", edges())
    triangle_records = overrides.pop("oriented_triangle_records", triangles())
    one_records = overrides.pop("one_chain_records", one_chains())
    two_records = overrides.pop("two_chain_records", two_chains())
    exact_records = overrides.pop("exactness_witnesses", exactness())
    nontrivial_records = overrides.pop("nontriviality_witnesses", nontriviality())
    digest = overrides.pop(
        "chain_complex_input_digest",
        compute_chain_complex_input_digest(
            vertex_records=vertex_records,
            oriented_edge_records=edge_records,
            oriented_triangle_records=triangle_records,
            one_chain_records=one_records,
            two_chain_records=two_records,
            exactness_witnesses=exact_records,
            nontriviality_witnesses=nontrivial_records,
        ),
    )
    args = {
        "source_nerve_certificate_digest": "planos-v1-14-finite-nerve-certificate",
        "source_finite_cover_certificate_digest": "planos-v1-13-finite-cover-certificate",
        "chain_complex_input_digest": digest,
        "vertex_records": vertex_records,
        "oriented_edge_records": edge_records,
        "oriented_triangle_records": triangle_records,
        "one_chain_records": one_records,
        "two_chain_records": two_records,
        "exactness_witnesses": exact_records,
        "nontriviality_witnesses": nontrivial_records,
        "maximum_absolute_chain_coefficient": 4,
    }
    args.update(overrides)
    return build_finite_simplicial_chain_homology_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    cert = result.certificate
    assert cert["rank_boundary_one_over_q"] == 3
    assert cert["rank_boundary_two_over_q"] == 1
    assert cert["betti_zero_over_q"] == 1
    assert cert["betti_one_over_q"] == 1
    assert cert["betti_two_over_q"] == 0
    assert cert["finite_euler_characteristic"] == 0
    assert cert["betti_euler_characteristic"] == 0
    assert cert["exactness_witnesses"][0]["boundary_matches_one_cycle"] is True
    assert cert["nontriviality_witnesses"][0]["not_in_rational_boundary_image"] is True
    for name in (
        "finite_simplicial_basis_retained",
        "boundary_one_recomputed",
        "boundary_two_recomputed",
        "boundary_squared_zero",
        "declared_one_chains_are_cycles",
        "exact_cycle_fillings_verified",
        "rational_nonboundary_witnesses_verified",
        "finite_betti_numbers_recomputed",
        "finite_euler_poincare_identity_verified",
        "bounded_first_homology_obstruction_retained",
        "integer_chain_coefficients_bounded",
        "finite_chain_complex_only",
        "rational_homology_only",
        "integral_torsion_not_computed",
        "persistent_homology_not_computed",
        "global_homology_not_claimed",
        "classical_cech_homology_equivalence_not_claimed",
        "global_topological_invariant_not_claimed",
        "candidate_identity_retained",
        "source_nerve_certificate_not_mutated",
        "source_finite_cover_certificate_not_mutated",
        "persistent_world_state_unchanged",
        "history_read_only",
        "chain_complex_grants_no_authority",
        "homology_witness_grants_no_authority",
        "topological_obstruction_grants_no_authority",
        "future_only",
    ):
        assert cert[name] is True
    assert cert["decision_selection_performed"] is False
    assert cert["active_now"] is False
    assert cert["execution_permission"] is False

    blocked = [
        build(source_nerve_certificate_digest=""),
        build(source_finite_cover_certificate_digest=""),
        build(chain_complex_input_digest="stale"),
        build(vertex_records=[]),
        build(oriented_edge_records=[]),
        build(oriented_triangle_records=[]),
        build(one_chain_records=[]),
        build(two_chain_records=[]),
        build(exactness_witnesses=[]),
        build(nontriviality_witnesses=[]),
        build(maximum_absolute_chain_coefficient=0),
    ]

    duplicate_vertex = vertices()
    duplicate_vertex[1]["vertex_id"] = "A"
    blocked.append(build(vertex_records=duplicate_vertex))

    loop_edge = edges()
    loop_edge[0]["vertex_ids"] = ["A", "A"]
    blocked.append(build(oriented_edge_records=loop_edge))

    duplicate_edge = edges()
    duplicate_edge[1]["vertex_ids"] = ["B", "A"]
    blocked.append(build(oriented_edge_records=duplicate_edge))

    missing_boundary_edge = [edge for edge in edges() if edge["edge_id"] != "BC"]
    blocked.append(build(oriented_edge_records=missing_boundary_edge))

    unknown_basis = one_chains()
    unknown_basis[0]["edge_coefficients"]["ZZ"] = 1
    blocked.append(build(one_chain_records=unknown_basis))

    noninteger = one_chains()
    noninteger[0]["edge_coefficients"]["AB"] = 0.5
    blocked.append(build(one_chain_records=noninteger))

    excessive = one_chains()
    excessive[0]["edge_coefficients"]["AB"] = 5
    blocked.append(build(one_chain_records=excessive))

    noncycle = one_chains()
    noncycle[1]["edge_coefficients"] = {"AC": 1}
    blocked.append(build(one_chain_records=noncycle))

    wrong_fill = two_chains()
    wrong_fill[0]["triangle_coefficients"]["ABC"] = -1
    blocked.append(build(two_chain_records=wrong_fill))

    fake_nontrivial = nontriviality()
    fake_nontrivial[0]["one_chain_id"] = "cycle-boundary-ABC"
    blocked.append(build(nontriviality_witnesses=fake_nontrivial))

    wrong_field = nontriviality()
    wrong_field[0]["coefficient_field"] = "Z"
    blocked.append(build(nontriviality_witnesses=wrong_field))

    missing_exact_chain = exactness()
    missing_exact_chain[0]["two_chain_id"] = "missing"
    blocked.append(build(exactness_witnesses=missing_exact_chain))

    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    tampered = deepcopy(edges())
    stale_digest = compute_chain_complex_input_digest(
        vertex_records=vertices(),
        oriented_edge_records=tampered,
        oriented_triangle_records=triangles(),
        one_chain_records=one_chains(),
        two_chain_records=two_chains(),
        exactness_witnesses=exactness(),
        nontriviality_witnesses=nontriviality(),
    )
    tampered[0]["source_edge_digest"] = "tampered"
    item = build(oriented_edge_records=tampered, chain_complex_input_digest=stale_digest)
    assert item.status != STATUS_READY and item.certificate is None

    print(
        "PASS: PlanOS Finite Simplicial Chain Complex and Homology Certificate Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
