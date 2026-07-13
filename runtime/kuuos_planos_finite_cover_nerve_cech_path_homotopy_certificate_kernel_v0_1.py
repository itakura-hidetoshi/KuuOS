#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import math

from runtime.kuuos_planos_finite_cover_nerve_cech_path_homotopy_support_v0_1 import (
    TOL,
    apply_triangle_move,
    canonical_digest,
    canonical_edge,
    compute_input_digest,
    connected_vertices,
    distance,
    finite,
    normalize_balls,
    normalize_edges,
    normalize_moves,
    normalize_paths,
    normalize_samples,
    normalize_triangles,
    path_valid,
    triangle_boundary,
)

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"


@dataclass
class FiniteCoverNerveCechPathHomotopyCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def compute_nerve_input_digest(**kwargs) -> str:
    return compute_input_digest(**kwargs)


def _blocked(blockers):
    return FiniteCoverNerveCechPathHomotopyCertificateResult(
        STATUS_BLOCKED, sorted(set(blockers)), None
    )


def build_finite_cover_nerve_cech_path_homotopy_certificate(
    *,
    source_finite_cover_certificate_digest: str,
    source_atlas_certificate_digest: str,
    nerve_input_digest: str,
    coordinate_schema: list[str],
    normal_ball_records: list[dict],
    covered_samples: list[dict],
    nerve_edges: list[dict],
    cech_triangles: list[dict],
    nerve_paths: list[dict],
    path_homotopy_moves: list[dict],
    reference_root_ball_id: str,
    minimum_overlap_margin: float,
    minimum_triple_overlap_margin: float,
) -> FiniteCoverNerveCechPathHomotopyCertificateResult:
    blockers = []
    for name, value in {
        "source_finite_cover_certificate_digest": source_finite_cover_certificate_digest,
        "source_atlas_certificate_digest": source_atlas_certificate_digest,
        "nerve_input_digest": nerve_input_digest,
        "reference_root_ball_id": reference_root_ball_id,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    if (
        not isinstance(coordinate_schema, list)
        or not coordinate_schema
        or any(not isinstance(c, str) or not c for c in coordinate_schema)
        or len(set(coordinate_schema)) != len(coordinate_schema)
    ):
        blockers.append("coordinate_schema_invalid")
        coordinates = []
    else:
        coordinates = list(coordinate_schema)
    for name, value in {
        "minimum_overlap_margin": minimum_overlap_margin,
        "minimum_triple_overlap_margin": minimum_triple_overlap_margin,
    }.items():
        if not finite(value) or float(value) < 0:
            blockers.append(f"{name}_invalid")

    ball_errors, balls = normalize_balls(normal_ball_records, coordinates)
    sample_errors, samples = normalize_samples(covered_samples, coordinates)
    edge_errors, edges = normalize_edges(nerve_edges, coordinates)
    triangle_errors, triangles = normalize_triangles(cech_triangles, coordinates)
    path_errors, paths = normalize_paths(nerve_paths)
    move_errors, moves = normalize_moves(path_homotopy_moves)
    blockers.extend(
        ball_errors
        + sample_errors
        + edge_errors
        + triangle_errors
        + path_errors
        + move_errors
    )
    if blockers:
        return _blocked(blockers)

    expected_digest = compute_nerve_input_digest(
        coordinate_schema=coordinates,
        normal_ball_records=normal_ball_records,
        covered_samples=covered_samples,
        nerve_edges=nerve_edges,
        cech_triangles=cech_triangles,
        nerve_paths=nerve_paths,
        path_homotopy_moves=path_homotopy_moves,
    )
    if nerve_input_digest != expected_digest:
        blockers.append("nerve_input_digest_mismatch")

    ball_map = {ball["ball_id"]: ball for ball in balls}
    ball_ids = set(ball_map)
    if reference_root_ball_id not in ball_ids:
        blockers.append("reference_root_ball_missing")

    sample_records = []
    for sample in samples:
        ball = ball_map.get(sample["assigned_ball_id"])
        if ball is None:
            blockers.append(f"assigned_sample_ball_missing_{sample['sample_id']}")
            continue
        sample_distance = distance(sample["point"], ball["center"], coordinates)
        clearance = ball["radius"] - sample_distance
        if clearance <= TOL:
            blockers.append(f"sample_not_strictly_covered_{sample['sample_id']}")
        sample_records.append(
            {
                **sample,
                "distance_to_assigned_ball_center": sample_distance,
                "assigned_ball_clearance": clearance,
                "strictly_covered_by_assigned_ball": clearance > TOL,
            }
        )

    edge_pairs, edge_records = set(), []
    minimum_computed_overlap_margin = math.inf
    for edge in edges:
        left = ball_map.get(edge["left_ball_id"])
        right = ball_map.get(edge["right_ball_id"])
        if left is None or right is None:
            blockers.append(f"nerve_edge_ball_missing_{edge['edge_id']}")
            continue
        pair = canonical_edge(left["ball_id"], right["ball_id"])
        edge_pairs.add(pair)
        left_clearance = left["radius"] - distance(
            edge["overlap_witness"], left["center"], coordinates
        )
        right_clearance = right["radius"] - distance(
            edge["overlap_witness"], right["center"], coordinates
        )
        margin = min(left_clearance, right_clearance)
        minimum_computed_overlap_margin = min(minimum_computed_overlap_margin, margin)
        if margin < float(minimum_overlap_margin) - TOL:
            blockers.append(f"overlap_margin_below_bound_{edge['edge_id']}")
        edge_records.append(
            {
                **edge,
                "left_ball_clearance": left_clearance,
                "right_ball_clearance": right_clearance,
                "computed_overlap_margin": margin,
                "edge_witness_lies_in_both_balls": margin > TOL,
            }
        )
    if math.isinf(minimum_computed_overlap_margin):
        minimum_computed_overlap_margin = 0.0

    triangle_map, triangle_records = {}, []
    minimum_computed_triple_overlap_margin = math.inf
    for triangle in triangles:
        triangle_map[triangle["triangle_id"]] = triangle
        vertices = triangle["vertex_ball_ids"]
        if any(vertex not in ball_ids for vertex in vertices):
            blockers.append(f"cech_triangle_ball_missing_{triangle['triangle_id']}")
            continue
        boundary = triangle_boundary(vertices)
        if not boundary.issubset(edge_pairs):
            blockers.append(f"cech_triangle_boundary_edge_missing_{triangle['triangle_id']}")
        clearances = {
            vertex: ball_map[vertex]["radius"]
            - distance(
                triangle["triple_overlap_witness"],
                ball_map[vertex]["center"],
                coordinates,
            )
            for vertex in vertices
        }
        margin = min(clearances.values())
        minimum_computed_triple_overlap_margin = min(
            minimum_computed_triple_overlap_margin, margin
        )
        if margin < float(minimum_triple_overlap_margin) - TOL:
            blockers.append(f"triple_overlap_margin_below_bound_{triangle['triangle_id']}")
        triangle_records.append(
            {
                **triangle,
                "boundary_edges": [list(pair) for pair in sorted(boundary)],
                "vertex_clearances": clearances,
                "computed_triple_overlap_margin": margin,
                "triple_witness_lies_in_all_balls": margin > TOL,
            }
        )
    if math.isinf(minimum_computed_triple_overlap_margin):
        minimum_computed_triple_overlap_margin = 0.0

    if reference_root_ball_id in ball_ids:
        reachable = connected_vertices(ball_ids, edge_pairs, reference_root_ball_id)
        if reachable != ball_ids:
            blockers.append("finite_nerve_not_connected_from_reference_root")
    else:
        reachable = set()

    path_map = {path["path_id"]: path for path in paths}
    path_records = []
    for path in paths:
        vertices = path["vertex_sequence"]
        if any(vertex not in ball_ids for vertex in vertices):
            blockers.append(f"nerve_path_ball_missing_{path['path_id']}")
        valid = path_valid(vertices, edge_pairs)
        if not valid:
            blockers.append(f"nerve_path_edge_missing_{path['path_id']}")
        path_records.append(
            {
                **path,
                "path_edge_pairs": [
                    list(canonical_edge(left, right))
                    for left, right in zip(vertices, vertices[1:])
                ],
                "nerve_path_valid": valid,
            }
        )

    move_records = []
    for move in moves:
        source = path_map.get(move["source_path_id"])
        target = path_map.get(move["target_path_id"])
        triangle = triangle_map.get(move["triangle_id"])
        if source is None:
            blockers.append(f"homotopy_source_path_missing_{move['move_id']}")
        if target is None:
            blockers.append(f"homotopy_target_path_missing_{move['move_id']}")
        if triangle is None:
            blockers.append(f"homotopy_triangle_missing_{move['move_id']}")
        valid = False
        endpoints_preserved = False
        if source is not None and target is not None and triangle is not None:
            source_vertices = source["vertex_sequence"]
            target_vertices = target["vertex_sequence"]
            endpoints_preserved = (
                source_vertices[0] == target_vertices[0]
                and source_vertices[-1] == target_vertices[-1]
            )
            valid = apply_triangle_move(
                source_vertices,
                target_vertices,
                triangle["vertex_ball_ids"],
                move["move_kind"],
            )
            if not endpoints_preserved:
                blockers.append(f"homotopy_endpoints_changed_{move['move_id']}")
            if not valid:
                blockers.append(f"triangle_homotopy_move_invalid_{move['move_id']}")
        move_records.append(
            {
                **move,
                "endpoints_preserved": endpoints_preserved,
                "elementary_triangle_move_valid": valid,
            }
        )

    if blockers:
        return _blocked(blockers)

    certificate = {
        "kernel": "PlanOS Finite Cover Nerve, Cech Overlap, and Path Homotopy Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.14",
        "source_finite_cover_certificate_digest": source_finite_cover_certificate_digest,
        "source_atlas_certificate_digest": source_atlas_certificate_digest,
        "nerve_input_digest": nerve_input_digest,
        "coordinate_schema": coordinates,
        "normal_ball_records": balls,
        "covered_samples": sample_records,
        "nerve_edges": edge_records,
        "cech_triangles": triangle_records,
        "nerve_paths": path_records,
        "path_homotopy_moves": move_records,
        "reference_root_ball_id": reference_root_ball_id,
        "minimum_overlap_margin": float(minimum_overlap_margin),
        "minimum_triple_overlap_margin": float(minimum_triple_overlap_margin),
        "computed_minimum_overlap_margin": minimum_computed_overlap_margin,
        "computed_minimum_triple_overlap_margin": minimum_computed_triple_overlap_margin,
        "reachable_ball_ids_from_reference_root": sorted(reachable),
        "finite_cover_vertices_retained": True,
        "nerve_edges_recomputed_from_overlap_witnesses": True,
        "cech_two_simplices_recomputed_from_triple_overlap_witnesses": True,
        "triangle_boundaries_present_in_nerve": True,
        "finite_nerve_connected_from_reference_root": True,
        "retained_samples_covered_by_assigned_vertices": True,
        "nerve_paths_edge_valid": True,
        "elementary_triangle_path_homotopy_verified": True,
        "path_homotopy_endpoints_preserved": True,
        "local_to_global_finite_topological_coherence": True,
        "finite_complex_only": True,
        "classical_nerve_theorem_not_claimed": True,
        "cover_homotopy_equivalence_not_claimed": True,
        "fundamental_group_not_computed": True,
        "global_path_homotopy_classification_not_claimed": True,
        "global_topological_invariant_not_claimed": True,
        "candidate_identity_retained": True,
        "source_finite_cover_certificate_not_mutated": True,
        "source_atlas_certificate_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "nerve_complex_grants_no_authority": True,
        "cech_overlap_grants_no_authority": True,
        "path_homotopy_grants_no_authority": True,
        "topological_coherence_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["finite_cover_nerve_certificate_digest"] = canonical_digest(certificate)
    return FiniteCoverNerveCechPathHomotopyCertificateResult(
        STATUS_READY, [], certificate
    )
