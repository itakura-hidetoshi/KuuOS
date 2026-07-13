from __future__ import annotations

from dataclasses import dataclass

from runtime.kuuos_planos_finite_filtration_persistent_homology_certificate_support_v0_1 import (
    canonical_digest,
    compute_persistent_homology_input_digest,
    compute_stage_smith_data,
    normalize_barcode_claims,
    normalize_edges,
    normalize_filtration_stages,
    normalize_persistent_betti_claims,
    normalize_stage_claims,
    normalize_triangles,
    normalize_vertices,
    persistent_barcode_f2,
    persistent_betti_from_barcode,
    validate_face_closure_and_filtration,
)

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"


@dataclass
class FiniteFiltrationPersistentHomologyCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def build_finite_filtration_persistent_homology_certificate(
    *,
    source_integer_homology_certificate_digest: str,
    source_nerve_certificate_digest: str,
    persistent_homology_input_digest: str,
    filtered_vertex_records: list[dict],
    filtered_edge_records: list[dict],
    filtered_triangle_records: list[dict],
    filtration_stages: list[int],
    claimed_stage_smith_data: list[dict],
    claimed_barcode_intervals: list[dict],
    claimed_persistent_betti: list[dict],
    maximum_filtration_value: int,
    maximum_simplex_count: int,
) -> FiniteFiltrationPersistentHomologyCertificateResult:
    blockers: list[str] = []
    for name, value in {
        "source_integer_homology_certificate_digest": source_integer_homology_certificate_digest,
        "source_nerve_certificate_digest": source_nerve_certificate_digest,
        "persistent_homology_input_digest": persistent_homology_input_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    if not isinstance(maximum_filtration_value, int) or isinstance(maximum_filtration_value, bool) or maximum_filtration_value < 0:
        blockers.append("maximum_filtration_value_invalid")
        maximum_filtration_value = 0
    if not isinstance(maximum_simplex_count, int) or isinstance(maximum_simplex_count, bool) or maximum_simplex_count <= 0:
        blockers.append("maximum_simplex_count_invalid")
        maximum_simplex_count = 0

    vertex_errors, vertices = normalize_vertices(filtered_vertex_records, maximum_filtration_value)
    edge_errors, edges = normalize_edges(filtered_edge_records, maximum_filtration_value)
    triangle_errors, triangles = normalize_triangles(filtered_triangle_records, maximum_filtration_value)
    stage_errors, stages = normalize_filtration_stages(filtration_stages, maximum_filtration_value)
    stage_claim_errors, stage_claims = normalize_stage_claims(claimed_stage_smith_data)
    barcode_errors, barcode_claims = normalize_barcode_claims(claimed_barcode_intervals)
    betti_errors, betti_claims = normalize_persistent_betti_claims(claimed_persistent_betti)
    blockers.extend(vertex_errors + edge_errors + triangle_errors + stage_errors)
    blockers.extend(stage_claim_errors + barcode_errors + betti_errors)

    simplex_ids = [f"vertex-{item['vertex_id']}" for item in vertices]
    simplex_ids += [item["edge_id"] for item in edges]
    simplex_ids += [item["triangle_id"] for item in triangles]
    if len(simplex_ids) != len(set(simplex_ids)):
        blockers.append("global_filtered_simplex_id_collision")
    if len(simplex_ids) > maximum_simplex_count:
        blockers.append("maximum_simplex_count_exceeded")

    blockers.extend(validate_face_closure_and_filtration(vertices, edges, triangles))
    computed_stages = sorted({item["filtration"] for item in [*vertices, *edges, *triangles]})
    if stages and stages != computed_stages:
        blockers.append("filtration_stages_do_not_match_simplex_values")
    if stages and [item["stage"] for item in stage_claims] != stages:
        blockers.append("stage_smith_claim_stages_mismatch")
    if stages and [item["stage"] for item in betti_claims] != stages:
        blockers.append("persistent_betti_claim_stages_mismatch")

    if blockers:
        return FiniteFiltrationPersistentHomologyCertificateResult(STATUS_BLOCKED, sorted(set(blockers)), None)

    expected_digest = compute_persistent_homology_input_digest(
        filtered_vertex_records=vertices,
        filtered_edge_records=edges,
        filtered_triangle_records=triangles,
        filtration_stages=stages,
        claimed_stage_smith_data=stage_claims,
        claimed_barcode_intervals=barcode_claims,
        claimed_persistent_betti=betti_claims,
    )
    if persistent_homology_input_digest != expected_digest:
        blockers.append("persistent_homology_input_digest_mismatch")

    try:
        computed_stage_data = compute_stage_smith_data(vertices, edges, triangles, stages)
        ordered_simplices, reduced_columns, computed_barcode = persistent_barcode_f2(vertices, edges, triangles)
        computed_betti = persistent_betti_from_barcode(computed_barcode, stages)
    except (KeyError, ValueError, ZeroDivisionError) as exc:
        blockers.append(f"persistent_homology_computation_failed_{type(exc).__name__}_{exc}")
        computed_stage_data, ordered_simplices, reduced_columns, computed_barcode, computed_betti = [], [], [], [], []

    if computed_stage_data != stage_claims:
        blockers.append("stage_smith_data_mismatch")
    if computed_barcode != barcode_claims:
        blockers.append("barcode_interval_claim_mismatch")
    if computed_betti != betti_claims:
        blockers.append("persistent_betti_claim_mismatch")
    if computed_stage_data and computed_stage_data[-1]["h1_free_rank"] != computed_betti[-1]["beta1"]:
        blockers.append("final_integer_and_f2_h1_rank_mismatch")

    if blockers:
        return FiniteFiltrationPersistentHomologyCertificateResult(STATUS_BLOCKED, sorted(set(blockers)), None)

    finite_intervals = [item for item in computed_barcode if item["death"] is not None]
    infinite_intervals = [item for item in computed_barcode if item["death"] is None]
    certificate = {
        "kernel": "PlanOS Finite Filtration Persistent Homology Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.17",
        "coefficient_fields": {"stagewise_integer_homology": "Z", "barcode_reduction": "F2"},
        "source_integer_homology_certificate_digest": source_integer_homology_certificate_digest,
        "source_nerve_certificate_digest": source_nerve_certificate_digest,
        "persistent_homology_input_digest": persistent_homology_input_digest,
        "filtration_stages": stages,
        "filtered_vertex_records": vertices,
        "filtered_edge_records": edges,
        "filtered_triangle_records": triangles,
        "ordered_simplices": ordered_simplices,
        "stage_smith_data": computed_stage_data,
        "barcode_intervals": computed_barcode,
        "persistent_betti": computed_betti,
        "finite_interval_count": len(finite_intervals),
        "infinite_interval_count": len(infinite_intervals),
        "maximum_filtration_value": maximum_filtration_value,
        "maximum_simplex_count": maximum_simplex_count,
        "reduced_boundary_column_pivots": [max(column) if column else None for column in reduced_columns],
        "face_closure_verified": True,
        "filtration_monotonicity_verified": True,
        "stagewise_integer_smith_data_recomputed": True,
        "f2_boundary_matrix_reduced": True,
        "birth_death_pairing_recomputed": True,
        "barcode_intervals_verified": True,
        "persistent_betti_verified": True,
        "finite_filtration_only": True,
        "dimensions_above_two_not_computed": True,
        "integer_persistence_module_not_computed": True,
        "zigzag_persistence_not_computed": True,
        "stability_theorem_not_claimed": True,
        "planning_space_persistent_homology_not_claimed": True,
        "global_topological_invariant_not_claimed": True,
        "barcode_does_not_rank_candidates": True,
        "candidate_identity_retained": True,
        "source_integer_homology_certificate_not_mutated": True,
        "source_nerve_certificate_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "persistent_homology_grants_no_authority": True,
        "barcode_interval_grants_no_authority": True,
        "persistent_betti_grants_no_authority": True,
        "topological_obstruction_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["persistent_homology_certificate_digest"] = canonical_digest(certificate)
    return FiniteFiltrationPersistentHomologyCertificateResult(STATUS_READY, [], certificate)
