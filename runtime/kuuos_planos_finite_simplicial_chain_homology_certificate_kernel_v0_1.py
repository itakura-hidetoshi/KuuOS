#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime.kuuos_planos_finite_simplicial_chain_homology_certificate_support_v0_1 import (
    augment_with_column,
    boundary_matrices,
    canonical_digest,
    compute_chain_complex_input_digest,
    matrix_multiply,
    matrix_vector,
    normalize_edges,
    normalize_one_chains,
    normalize_triangles,
    normalize_two_chains,
    normalize_vertices,
    normalize_witnesses,
    rational_rank,
)

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"


@dataclass
class FiniteSimplicialChainHomologyCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def _blocked(blockers: list[str]):
    return FiniteSimplicialChainHomologyCertificateResult(
        STATUS_BLOCKED, sorted(set(blockers)), None
    )


def build_finite_simplicial_chain_homology_certificate(
    *,
    source_nerve_certificate_digest: str,
    source_finite_cover_certificate_digest: str,
    chain_complex_input_digest: str,
    vertex_records: list[dict],
    oriented_edge_records: list[dict],
    oriented_triangle_records: list[dict],
    one_chain_records: list[dict],
    two_chain_records: list[dict],
    exactness_witnesses: list[dict],
    nontriviality_witnesses: list[dict],
    maximum_absolute_chain_coefficient: int,
) -> FiniteSimplicialChainHomologyCertificateResult:
    blockers: list[str] = []
    for name, value in {
        "source_nerve_certificate_digest": source_nerve_certificate_digest,
        "source_finite_cover_certificate_digest": source_finite_cover_certificate_digest,
        "chain_complex_input_digest": chain_complex_input_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    if (
        not isinstance(maximum_absolute_chain_coefficient, int)
        or isinstance(maximum_absolute_chain_coefficient, bool)
        or maximum_absolute_chain_coefficient <= 0
    ):
        blockers.append("maximum_absolute_chain_coefficient_invalid")
        maximum = 0
    else:
        maximum = maximum_absolute_chain_coefficient

    vertex_errors, vertices = normalize_vertices(vertex_records)
    edge_errors, edges = normalize_edges(oriented_edge_records)
    triangle_errors, triangles = normalize_triangles(oriented_triangle_records)
    blockers.extend(vertex_errors + edge_errors + triangle_errors)
    if blockers:
        return _blocked(blockers)

    vertex_ids = [item["vertex_id"] for item in vertices]
    edge_ids = [item["edge_id"] for item in edges]
    triangle_ids = [item["triangle_id"] for item in triangles]
    vertex_set = set(vertex_ids)
    for edge in edges:
        if any(vertex not in vertex_set for vertex in edge["vertex_ids"]):
            blockers.append(f"edge_vertex_missing_{edge['edge_id']}")
    for triangle in triangles:
        if any(vertex not in vertex_set for vertex in triangle["vertex_ids"]):
            blockers.append(f"triangle_vertex_missing_{triangle['triangle_id']}")

    one_errors, one_chains = normalize_one_chains(one_chain_records, edge_ids, maximum)
    two_errors, two_chains = normalize_two_chains(two_chain_records, triangle_ids, maximum)
    exact_errors, exact_witnesses = normalize_witnesses(exactness_witnesses, "exactness")
    nontrivial_errors, nontrivial_witnesses = normalize_witnesses(
        nontriviality_witnesses, "nontriviality"
    )
    blockers.extend(one_errors + two_errors + exact_errors + nontrivial_errors)
    if blockers:
        return _blocked(blockers)

    expected_digest = compute_chain_complex_input_digest(
        vertex_records=vertex_records,
        oriented_edge_records=oriented_edge_records,
        oriented_triangle_records=oriented_triangle_records,
        one_chain_records=one_chain_records,
        two_chain_records=two_chain_records,
        exactness_witnesses=exactness_witnesses,
        nontriviality_witnesses=nontriviality_witnesses,
    )
    if chain_complex_input_digest != expected_digest:
        blockers.append("chain_complex_input_digest_mismatch")

    boundary_errors, boundary_one, boundary_two = boundary_matrices(vertices, edges, triangles)
    blockers.extend(boundary_errors)
    boundary_squared = matrix_multiply(boundary_one, boundary_two)
    if any(value != 0 for row in boundary_squared for value in row):
        blockers.append("boundary_squared_nonzero")

    rank_boundary_one = rational_rank(boundary_one)
    rank_boundary_two = rational_rank(boundary_two)
    vertex_count = len(vertices)
    edge_count = len(edges)
    triangle_count = len(triangles)
    betti_zero = vertex_count - rank_boundary_one
    betti_one = edge_count - rank_boundary_one - rank_boundary_two
    betti_two = triangle_count - rank_boundary_two
    if min(betti_zero, betti_one, betti_two) < 0:
        blockers.append("finite_betti_number_negative")
    euler_characteristic = vertex_count - edge_count + triangle_count
    betti_euler_characteristic = betti_zero - betti_one + betti_two
    if euler_characteristic != betti_euler_characteristic:
        blockers.append("finite_euler_poincare_identity_mismatch")

    one_chain_map = {chain["chain_id"]: chain for chain in one_chains}
    two_chain_map = {chain["chain_id"]: chain for chain in two_chains}
    one_chain_vectors: dict[str, list[int]] = {}
    one_chain_boundary_records: list[dict] = []
    for chain in one_chains:
        vector = [chain["edge_coefficients"][edge_id] for edge_id in edge_ids]
        boundary = matrix_vector(boundary_one, vector)
        is_cycle = all(value == 0 for value in boundary)
        if not is_cycle:
            blockers.append(f"declared_one_chain_not_cycle_{chain['chain_id']}")
        one_chain_vectors[chain["chain_id"]] = vector
        one_chain_boundary_records.append(
            {
                **chain,
                "edge_coefficient_vector": vector,
                "vertex_boundary_vector": boundary,
                "is_one_cycle": is_cycle,
            }
        )

    two_chain_vectors: dict[str, list[int]] = {}
    two_chain_boundary_records: list[dict] = []
    for chain in two_chains:
        vector = [chain["triangle_coefficients"][triangle_id] for triangle_id in triangle_ids]
        boundary = matrix_vector(boundary_two, vector)
        two_chain_vectors[chain["chain_id"]] = vector
        two_chain_boundary_records.append(
            {
                **chain,
                "triangle_coefficient_vector": vector,
                "edge_boundary_vector": boundary,
            }
        )

    exactness_records: list[dict] = []
    exact_cycle_ids: set[str] = set()
    for witness in exact_witnesses:
        one_chain = one_chain_map.get(witness["one_chain_id"])
        two_chain = two_chain_map.get(witness["two_chain_id"])
        if one_chain is None:
            blockers.append(f"exactness_one_chain_missing_{witness['witness_id']}")
        if two_chain is None:
            blockers.append(f"exactness_two_chain_missing_{witness['witness_id']}")
        matches = False
        if one_chain is not None and two_chain is not None:
            if one_chain["chain_role"] != "exact_cycle":
                blockers.append(f"exactness_role_mismatch_{witness['witness_id']}")
            matches = one_chain_vectors[one_chain["chain_id"]] == matrix_vector(
                boundary_two, two_chain_vectors[two_chain["chain_id"]]
            )
            if not matches:
                blockers.append(f"exactness_boundary_mismatch_{witness['witness_id']}")
            else:
                exact_cycle_ids.add(one_chain["chain_id"])
        exactness_records.append({**witness, "boundary_matches_one_cycle": matches})

    expected_exact_ids = {
        chain["chain_id"] for chain in one_chains if chain["chain_role"] == "exact_cycle"
    }
    if exact_cycle_ids != expected_exact_ids:
        blockers.append("not_all_exact_cycles_have_fillings")

    nontriviality_records: list[dict] = []
    nontrivial_cycle_ids: set[str] = set()
    for witness in nontrivial_witnesses:
        chain = one_chain_map.get(witness["one_chain_id"])
        if chain is None:
            blockers.append(f"nontriviality_one_chain_missing_{witness['witness_id']}")
            rank_augmented = rank_boundary_two
        else:
            if chain["chain_role"] != "nontrivial_cycle":
                blockers.append(f"nontriviality_role_mismatch_{witness['witness_id']}")
            vector = one_chain_vectors[chain["chain_id"]]
            rank_augmented = rational_rank(augment_with_column(boundary_two, vector))
            if rank_augmented <= rank_boundary_two:
                blockers.append(f"cycle_lies_in_rational_boundary_image_{witness['witness_id']}")
            else:
                nontrivial_cycle_ids.add(chain["chain_id"])
        nontriviality_records.append(
            {
                **witness,
                "boundary_two_rank": rank_boundary_two,
                "augmented_boundary_two_rank": rank_augmented,
                "not_in_rational_boundary_image": rank_augmented > rank_boundary_two,
            }
        )

    expected_nontrivial_ids = {
        chain["chain_id"] for chain in one_chains if chain["chain_role"] == "nontrivial_cycle"
    }
    if nontrivial_cycle_ids != expected_nontrivial_ids:
        blockers.append("not_all_nontrivial_cycles_have_rank_witnesses")
    if expected_nontrivial_ids and betti_one <= 0:
        blockers.append("nontrivial_cycle_declared_but_betti_one_zero")

    if blockers:
        return _blocked(blockers)

    certificate = {
        "kernel": "PlanOS Finite Simplicial Chain Complex and Homology Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.15",
        "source_nerve_certificate_digest": source_nerve_certificate_digest,
        "source_finite_cover_certificate_digest": source_finite_cover_certificate_digest,
        "chain_complex_input_digest": chain_complex_input_digest,
        "maximum_absolute_chain_coefficient": maximum,
        "vertex_records": vertices,
        "oriented_edge_records": edges,
        "oriented_triangle_records": triangles,
        "one_chain_records": one_chain_boundary_records,
        "two_chain_records": two_chain_boundary_records,
        "exactness_witnesses": exactness_records,
        "nontriviality_witnesses": nontriviality_records,
        "boundary_one_matrix": boundary_one,
        "boundary_two_matrix": boundary_two,
        "boundary_one_boundary_two_matrix": boundary_squared,
        "rank_boundary_one_over_q": rank_boundary_one,
        "rank_boundary_two_over_q": rank_boundary_two,
        "betti_zero_over_q": betti_zero,
        "betti_one_over_q": betti_one,
        "betti_two_over_q": betti_two,
        "finite_euler_characteristic": euler_characteristic,
        "betti_euler_characteristic": betti_euler_characteristic,
        "finite_simplicial_basis_retained": True,
        "boundary_one_recomputed": True,
        "boundary_two_recomputed": True,
        "boundary_squared_zero": True,
        "declared_one_chains_are_cycles": True,
        "exact_cycle_fillings_verified": True,
        "rational_nonboundary_witnesses_verified": True,
        "finite_betti_numbers_recomputed": True,
        "finite_euler_poincare_identity_verified": True,
        "bounded_first_homology_obstruction_retained": betti_one > 0,
        "integer_chain_coefficients_bounded": True,
        "finite_chain_complex_only": True,
        "rational_homology_only": True,
        "integral_torsion_not_computed": True,
        "persistent_homology_not_computed": True,
        "global_homology_not_claimed": True,
        "classical_cech_homology_equivalence_not_claimed": True,
        "global_topological_invariant_not_claimed": True,
        "candidate_identity_retained": True,
        "source_nerve_certificate_not_mutated": True,
        "source_finite_cover_certificate_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "chain_complex_grants_no_authority": True,
        "homology_witness_grants_no_authority": True,
        "topological_obstruction_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["finite_simplicial_chain_homology_certificate_digest"] = canonical_digest(
        certificate
    )
    return FiniteSimplicialChainHomologyCertificateResult(STATUS_READY, [], certificate)
