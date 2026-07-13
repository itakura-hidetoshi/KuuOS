#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime.kuuos_planos_smith_normal_form_integer_homology_certificate_support_v0_1 import (
    boundary_matrices,
    canonical_digest,
    compute_smith_input_digest,
    cycle_presentation_matrix,
    divisibility_chain,
    matrix_multiply,
    matrix_vector,
    normalize_edges,
    normalize_triangles,
    normalize_vertices,
    rational_rank,
    smith_normal_form_diagonal,
    spanning_forest_cycle_basis,
)

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"


@dataclass
class SmithNormalFormIntegerHomologyCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def compute_integer_homology_input_digest(**kwargs) -> str:
    return compute_smith_input_digest(**kwargs)


def _blocked(blockers: list[str]):
    return SmithNormalFormIntegerHomologyCertificateResult(
        STATUS_BLOCKED, sorted(set(blockers)), None
    )


def _valid_nonnegative_integer(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _valid_positive_integer_list(value) -> bool:
    return (
        isinstance(value, list)
        and all(
            isinstance(item, int) and not isinstance(item, bool) and item > 0
            for item in value
        )
    )


def build_smith_normal_form_integer_homology_certificate(
    *,
    source_chain_homology_certificate_digest: str,
    source_nerve_certificate_digest: str,
    smith_input_digest: str,
    vertex_records: list[dict],
    oriented_edge_records: list[dict],
    oriented_triangle_records: list[dict],
    claimed_smith_diagonal: list[int],
    expected_h0_free_rank: int,
    expected_h1_free_rank: int,
    expected_h2_free_rank: int,
    expected_torsion_invariant_factors: list[int],
    maximum_basis_size: int,
) -> SmithNormalFormIntegerHomologyCertificateResult:
    blockers: list[str] = []
    for name, value in {
        "source_chain_homology_certificate_digest": source_chain_homology_certificate_digest,
        "source_nerve_certificate_digest": source_nerve_certificate_digest,
        "smith_input_digest": smith_input_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    if (
        not isinstance(maximum_basis_size, int)
        or isinstance(maximum_basis_size, bool)
        or maximum_basis_size <= 0
    ):
        blockers.append("maximum_basis_size_invalid")
    for name, value in {
        "expected_h0_free_rank": expected_h0_free_rank,
        "expected_h1_free_rank": expected_h1_free_rank,
        "expected_h2_free_rank": expected_h2_free_rank,
    }.items():
        if not _valid_nonnegative_integer(value):
            blockers.append(f"{name}_invalid")
    if not _valid_positive_integer_list(claimed_smith_diagonal):
        blockers.append("claimed_smith_diagonal_invalid")
    elif not divisibility_chain(claimed_smith_diagonal):
        blockers.append("claimed_smith_diagonal_not_divisibility_chain")
    if not isinstance(expected_torsion_invariant_factors, list) or any(
        not isinstance(value, int) or isinstance(value, bool) or value <= 1
        for value in expected_torsion_invariant_factors
    ):
        blockers.append("expected_torsion_invariant_factors_invalid")
    elif not divisibility_chain(expected_torsion_invariant_factors):
        blockers.append("expected_torsion_invariant_factors_not_divisibility_chain")

    vertex_errors, vertices = normalize_vertices(vertex_records)
    edge_errors, edges = normalize_edges(oriented_edge_records)
    triangle_errors, triangles = normalize_triangles(oriented_triangle_records)
    blockers.extend(vertex_errors + edge_errors + triangle_errors)
    if blockers:
        return _blocked(blockers)

    if max(len(vertices), len(edges), len(triangles)) > maximum_basis_size:
        blockers.append("finite_basis_size_bound_exceeded")

    expected_digest = compute_integer_homology_input_digest(
        vertex_records=vertex_records,
        oriented_edge_records=oriented_edge_records,
        oriented_triangle_records=oriented_triangle_records,
        claimed_smith_diagonal=claimed_smith_diagonal,
        expected_h0_free_rank=expected_h0_free_rank,
        expected_h1_free_rank=expected_h1_free_rank,
        expected_h2_free_rank=expected_h2_free_rank,
        expected_torsion_invariant_factors=expected_torsion_invariant_factors,
    )
    if smith_input_digest != expected_digest:
        blockers.append("smith_input_digest_mismatch")

    matrix_errors, boundary_one, boundary_two = boundary_matrices(
        vertices, edges, triangles
    )
    blockers.extend(matrix_errors)
    boundary_composition = matrix_multiply(boundary_one, boundary_two)
    if any(value != 0 for row in boundary_composition for value in row):
        blockers.append("boundary_composition_nonzero")
    if blockers:
        return _blocked(blockers)

    try:
        cycle_basis_data = spanning_forest_cycle_basis(vertices, edges)
    except ValueError as exc:
        blockers.append(str(exc))
        cycle_basis_data = {
            "tree_edge_ids": [],
            "chord_edge_ids": [],
            "connected_component_count": 0,
            "cycle_basis": [],
        }

    for basis in cycle_basis_data["cycle_basis"]:
        if any(
            value != 0
            for value in matrix_vector(boundary_one, basis["vector"])
        ):
            blockers.append(
                f"fundamental_cycle_boundary_nonzero_{basis['basis_id']}"
            )

    presentation_matrix, reconstructed_columns = cycle_presentation_matrix(
        edges, triangles, boundary_two, cycle_basis_data
    )
    for column, reconstructed in enumerate(reconstructed_columns):
        original = [row[column] for row in boundary_two]
        if reconstructed != original:
            blockers.append(
                f"cycle_basis_reconstruction_mismatch_{triangles[column]['triangle_id']}"
            )

    smith_diagonal, diagonalized_presentation_matrix = smith_normal_form_diagonal(
        presentation_matrix
    )
    if not divisibility_chain(smith_diagonal):
        blockers.append("computed_smith_diagonal_not_divisibility_chain")
    smith_rank = len(smith_diagonal)
    rational_presentation_rank = rational_rank(presentation_matrix)
    if smith_rank != rational_presentation_rank:
        blockers.append("smith_rank_rational_rank_mismatch")
    if smith_diagonal != claimed_smith_diagonal:
        blockers.append("claimed_smith_diagonal_mismatch")

    component_count = cycle_basis_data["connected_component_count"]
    cycle_rank = len(cycle_basis_data["cycle_basis"])
    h0_free_rank = component_count
    h1_free_rank = cycle_rank - smith_rank
    h2_free_rank = len(triangles) - rational_rank(boundary_two)
    torsion_invariant_factors = [value for value in smith_diagonal if value > 1]

    if h0_free_rank != expected_h0_free_rank:
        blockers.append("expected_h0_free_rank_mismatch")
    if h1_free_rank != expected_h1_free_rank:
        blockers.append("expected_h1_free_rank_mismatch")
    if h2_free_rank != expected_h2_free_rank:
        blockers.append("expected_h2_free_rank_mismatch")
    if torsion_invariant_factors != expected_torsion_invariant_factors:
        blockers.append("expected_torsion_invariant_factors_mismatch")
    if blockers:
        return _blocked(blockers)

    edge_ids = [edge["edge_id"] for edge in edges]
    triangle_ids = [triangle["triangle_id"] for triangle in triangles]
    certificate = {
        "kernel": "PlanOS Smith Normal Form and Integer Homology Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.16",
        "source_chain_homology_certificate_digest": source_chain_homology_certificate_digest,
        "source_nerve_certificate_digest": source_nerve_certificate_digest,
        "smith_input_digest": smith_input_digest,
        "vertex_records": vertices,
        "oriented_edge_records": edges,
        "oriented_triangle_records": triangles,
        "vertex_basis_ids": [vertex["vertex_id"] for vertex in vertices],
        "edge_basis_ids": edge_ids,
        "triangle_basis_ids": triangle_ids,
        "boundary_one_matrix": boundary_one,
        "boundary_two_matrix": boundary_two,
        "boundary_composition_matrix": boundary_composition,
        "spanning_forest_tree_edge_ids": cycle_basis_data["tree_edge_ids"],
        "fundamental_cycle_chord_edge_ids": cycle_basis_data["chord_edge_ids"],
        "fundamental_cycle_basis": [
            {
                "basis_id": basis["basis_id"],
                "chord_edge_id": basis["chord_edge_id"],
                "edge_coefficients": basis["edge_coefficients"],
            }
            for basis in cycle_basis_data["cycle_basis"]
        ],
        "integer_h1_presentation_matrix": presentation_matrix,
        "diagonalized_integer_h1_presentation_matrix": diagonalized_presentation_matrix,
        "smith_diagonal": smith_diagonal,
        "smith_rank": smith_rank,
        "connected_component_count": component_count,
        "cycle_lattice_rank": cycle_rank,
        "h0_free_rank": h0_free_rank,
        "h1_free_rank": h1_free_rank,
        "h2_free_rank": h2_free_rank,
        "torsion_invariant_factors": torsion_invariant_factors,
        "integer_h1_decomposition": {
            "free_rank": h1_free_rank,
            "torsion_invariant_factors": torsion_invariant_factors,
        },
        "maximum_basis_size": maximum_basis_size,
        "boundary_squared_zero_verified": True,
        "fundamental_cycle_basis_verified": True,
        "triangle_boundaries_reconstructed_in_cycle_basis": True,
        "smith_diagonal_recomputed_by_unimodular_operations": True,
        "smith_divisibility_chain_verified": True,
        "integer_homology_decomposition_verified": True,
        "torsion_invariant_factors_retained": True,
        "finite_integral_chain_complex_only": True,
        "unimodular_transform_matrices_not_retained": True,
        "higher_dimensional_homology_not_computed": True,
        "persistent_homology_not_computed": True,
        "global_integer_homology_not_claimed": True,
        "classical_cech_homology_equivalence_not_claimed": True,
        "global_topological_invariant_not_claimed": True,
        "candidate_identity_retained": True,
        "source_chain_homology_certificate_not_mutated": True,
        "source_nerve_certificate_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "smith_normal_form_grants_no_authority": True,
        "integer_homology_grants_no_authority": True,
        "torsion_invariant_grants_no_authority": True,
        "topological_obstruction_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["smith_integer_homology_certificate_digest"] = canonical_digest(
        certificate
    )
    return SmithNormalFormIntegerHomologyCertificateResult(
        STATUS_READY, [], certificate
    )
