#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_finite_cover_nerve_cech_path_homotopy_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_finite_cover_nerve_cech_path_homotopy_certificate,
    compute_nerve_input_digest,
)


def coordinates() -> list[str]:
    return ["x", "y"]


def balls() -> list[dict]:
    return [
        {
            "ball_id": "A",
            "center": {"x": 0.0, "y": 0.0},
            "radius": 0.8,
            "source_injectivity_radius_lower_bound": 1.5,
            "chart_id": "chart-A",
            "source_normal_ball_digest": "normal-ball-A",
        },
        {
            "ball_id": "B",
            "center": {"x": 0.8, "y": 0.0},
            "radius": 0.8,
            "source_injectivity_radius_lower_bound": 1.4,
            "chart_id": "chart-B",
            "source_normal_ball_digest": "normal-ball-B",
        },
        {
            "ball_id": "C",
            "center": {"x": 0.4, "y": 0.6},
            "radius": 0.8,
            "source_injectivity_radius_lower_bound": 1.3,
            "chart_id": "chart-C",
            "source_normal_ball_digest": "normal-ball-C",
        },
    ]


def samples() -> list[dict]:
    return [
        {
            "sample_id": "sample-A",
            "point": {"x": 0.1, "y": 0.0},
            "assigned_ball_id": "A",
            "source_sample_digest": "sample-digest-A",
        },
        {
            "sample_id": "sample-B",
            "point": {"x": 0.7, "y": 0.0},
            "assigned_ball_id": "B",
            "source_sample_digest": "sample-digest-B",
        },
        {
            "sample_id": "sample-C",
            "point": {"x": 0.4, "y": 0.5},
            "assigned_ball_id": "C",
            "source_sample_digest": "sample-digest-C",
        },
    ]


def edges() -> list[dict]:
    return [
        {
            "edge_id": "edge-AB",
            "left_ball_id": "A",
            "right_ball_id": "B",
            "overlap_witness": {"x": 0.4, "y": 0.0},
            "source_overlap_digest": "overlap-AB",
        },
        {
            "edge_id": "edge-AC",
            "left_ball_id": "A",
            "right_ball_id": "C",
            "overlap_witness": {"x": 0.2, "y": 0.3},
            "source_overlap_digest": "overlap-AC",
        },
        {
            "edge_id": "edge-BC",
            "left_ball_id": "B",
            "right_ball_id": "C",
            "overlap_witness": {"x": 0.6, "y": 0.3},
            "source_overlap_digest": "overlap-BC",
        },
    ]


def triangles() -> list[dict]:
    return [
        {
            "triangle_id": "triangle-ABC",
            "vertex_ball_ids": ["A", "B", "C"],
            "triple_overlap_witness": {"x": 0.4, "y": 0.2},
            "source_triple_overlap_digest": "triple-overlap-ABC",
        }
    ]


def paths() -> list[dict]:
    return [
        {
            "path_id": "path-long",
            "vertex_sequence": ["A", "B", "C"],
            "source_path_digest": "path-long-digest",
        },
        {
            "path_id": "path-short",
            "vertex_sequence": ["A", "C"],
            "source_path_digest": "path-short-digest",
        },
    ]


def moves() -> list[dict]:
    return [
        {
            "move_id": "contract-ABC",
            "move_kind": "triangle_contraction",
            "source_path_id": "path-long",
            "target_path_id": "path-short",
            "triangle_id": "triangle-ABC",
            "source_move_digest": "move-contract-ABC",
        }
    ]


def build(**overrides):
    coords = overrides.pop("coordinate_schema", coordinates())
    ball_records = overrides.pop("normal_ball_records", balls())
    covered_samples = overrides.pop("covered_samples", samples())
    nerve_edges = overrides.pop("nerve_edges", edges())
    cech_triangles = overrides.pop("cech_triangles", triangles())
    nerve_paths = overrides.pop("nerve_paths", paths())
    path_moves = overrides.pop("path_homotopy_moves", moves())
    digest = overrides.pop(
        "nerve_input_digest",
        compute_nerve_input_digest(
            coordinate_schema=coords,
            normal_ball_records=ball_records,
            covered_samples=covered_samples,
            nerve_edges=nerve_edges,
            cech_triangles=cech_triangles,
            nerve_paths=nerve_paths,
            path_homotopy_moves=path_moves,
        ),
    )
    args = {
        "source_finite_cover_certificate_digest": "planos-v1-13-finite-cover-certificate",
        "source_atlas_certificate_digest": "planos-v1-08-atlas-certificate",
        "nerve_input_digest": digest,
        "coordinate_schema": coords,
        "normal_ball_records": ball_records,
        "covered_samples": covered_samples,
        "nerve_edges": nerve_edges,
        "cech_triangles": cech_triangles,
        "nerve_paths": nerve_paths,
        "path_homotopy_moves": path_moves,
        "reference_root_ball_id": "A",
        "minimum_overlap_margin": 0.3,
        "minimum_triple_overlap_margin": 0.3,
    }
    args.update(overrides)
    return build_finite_cover_nerve_cech_path_homotopy_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    cert = result.certificate
    assert cert["reachable_ball_ids_from_reference_root"] == ["A", "B", "C"]
    assert cert["computed_minimum_overlap_margin"] > 0.3
    assert cert["computed_minimum_triple_overlap_margin"] > 0.3
    assert cert["nerve_paths"][0]["nerve_path_valid"] is True
    assert cert["path_homotopy_moves"][0]["elementary_triangle_move_valid"] is True
    for name in (
        "finite_cover_vertices_retained",
        "nerve_edges_recomputed_from_overlap_witnesses",
        "cech_two_simplices_recomputed_from_triple_overlap_witnesses",
        "triangle_boundaries_present_in_nerve",
        "finite_nerve_connected_from_reference_root",
        "retained_samples_covered_by_assigned_vertices",
        "nerve_paths_edge_valid",
        "elementary_triangle_path_homotopy_verified",
        "path_homotopy_endpoints_preserved",
        "local_to_global_finite_topological_coherence",
        "finite_complex_only",
        "classical_nerve_theorem_not_claimed",
        "cover_homotopy_equivalence_not_claimed",
        "fundamental_group_not_computed",
        "global_path_homotopy_classification_not_claimed",
        "global_topological_invariant_not_claimed",
        "candidate_identity_retained",
        "source_finite_cover_certificate_not_mutated",
        "source_atlas_certificate_not_mutated",
        "persistent_world_state_unchanged",
        "history_read_only",
        "nerve_complex_grants_no_authority",
        "cech_overlap_grants_no_authority",
        "path_homotopy_grants_no_authority",
        "topological_coherence_grants_no_authority",
        "future_only",
    ):
        assert cert[name] is True
    assert cert["decision_selection_performed"] is False
    assert cert["active_now"] is False
    assert cert["execution_permission"] is False

    blocked = [
        build(source_finite_cover_certificate_digest=""),
        build(source_atlas_certificate_digest=""),
        build(nerve_input_digest="stale"),
        build(coordinate_schema=["x", "x"]),
        build(normal_ball_records=[]),
        build(covered_samples=[]),
        build(nerve_edges=[]),
        build(cech_triangles=[]),
        build(nerve_paths=[]),
        build(path_homotopy_moves=[]),
        build(reference_root_ball_id="missing"),
        build(minimum_overlap_margin=-1.0),
    ]

    duplicate_ball = balls()
    duplicate_ball[1]["ball_id"] = duplicate_ball[0]["ball_id"]
    blocked.append(build(normal_ball_records=duplicate_ball))

    invalid_radius = balls()
    invalid_radius[0]["radius"] = 1.5
    blocked.append(build(normal_ball_records=invalid_radius))

    uncovered = samples()
    uncovered[0]["point"] = {"x": 2.0, "y": 2.0}
    blocked.append(build(covered_samples=uncovered))

    missing_ball_sample = samples()
    missing_ball_sample[0]["assigned_ball_id"] = "missing"
    blocked.append(build(covered_samples=missing_ball_sample))

    weak_edge = edges()
    weak_edge[0]["overlap_witness"] = {"x": -0.7, "y": 0.0}
    blocked.append(build(nerve_edges=weak_edge))

    duplicate_edge = edges()
    duplicate_edge[1]["left_ball_id"] = "B"
    duplicate_edge[1]["right_ball_id"] = "A"
    blocked.append(build(nerve_edges=duplicate_edge))

    missing_boundary = edges()[:2]
    blocked.append(build(nerve_edges=missing_boundary))

    weak_triangle = triangles()
    weak_triangle[0]["triple_overlap_witness"] = {"x": -0.7, "y": 0.0}
    blocked.append(build(cech_triangles=weak_triangle))

    invalid_path = paths()
    invalid_path[0]["vertex_sequence"] = ["A", "B", "missing"]
    blocked.append(build(nerve_paths=invalid_path))

    disconnected_edges = [deepcopy(edges()[0])]
    blocked.append(build(nerve_edges=disconnected_edges))

    changed_endpoint = paths()
    changed_endpoint[1]["vertex_sequence"] = ["B", "C"]
    blocked.append(build(nerve_paths=changed_endpoint))

    invalid_move = moves()
    invalid_move[0]["move_kind"] = "unknown"
    blocked.append(build(path_homotopy_moves=invalid_move))

    wrong_triangle = moves()
    wrong_triangle[0]["triangle_id"] = "missing"
    blocked.append(build(path_homotopy_moves=wrong_triangle))

    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    tampered = deepcopy(edges())
    stale_digest = compute_nerve_input_digest(
        coordinate_schema=coordinates(),
        normal_ball_records=balls(),
        covered_samples=samples(),
        nerve_edges=tampered,
        cech_triangles=triangles(),
        nerve_paths=paths(),
        path_homotopy_moves=moves(),
    )
    tampered[0]["overlap_witness"]["x"] += 0.01
    item = build(nerve_edges=tampered, nerve_input_digest=stale_digest)
    assert item.status != STATUS_READY and item.certificate is None

    print(
        "PASS: PlanOS Finite Cover Nerve, Cech Overlap, and Path Homotopy Certificate Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
