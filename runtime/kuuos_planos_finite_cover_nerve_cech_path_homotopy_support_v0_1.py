from __future__ import annotations

from hashlib import sha256
import json
import math
from typing import Any, Mapping, Sequence

TOL = 1e-9


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def finite(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def vector(value: Any, coordinates: Sequence[str], prefix: str):
    if not isinstance(value, dict) or set(value) != set(coordinates):
        return [f"{prefix}_schema_invalid"], {}
    if any(not finite(value[c]) for c in coordinates):
        return [f"{prefix}_nonfinite"], {}
    return [], {c: float(value[c]) for c in coordinates}


def distance(left: Mapping[str, float], right: Mapping[str, float], coordinates):
    return math.sqrt(sum((left[c] - right[c]) ** 2 for c in coordinates))


def canonical_edge(left: str, right: str) -> tuple[str, str]:
    return (left, right) if left < right else (right, left)


def triangle_boundary(vertices: Sequence[str]) -> set[tuple[str, str]]:
    first, second, third = sorted(vertices)
    return {
        canonical_edge(first, second),
        canonical_edge(first, third),
        canonical_edge(second, third),
    }


def _unique_string(value: Any, seen: set[str], duplicate_blocker: str):
    if not isinstance(value, str) or not value:
        return False, "invalid"
    if value in seen:
        return False, duplicate_blocker
    seen.add(value)
    return True, ""


def normalize_balls(values: Any, coordinates: Sequence[str]):
    if not isinstance(values, list) or len(values) < 2:
        return ["normal_ball_records_insufficient"], []
    fields = {
        "ball_id",
        "center",
        "radius",
        "source_injectivity_radius_lower_bound",
        "chart_id",
        "source_normal_ball_digest",
    }
    blockers, out = [], []
    seen_ids, seen_digests = set(), set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"normal_ball_schema_invalid_{index}")
            continue
        ball_id = item["ball_id"]
        ok, reason = _unique_string(ball_id, seen_ids, "duplicate_normal_ball_id")
        if not ok:
            blockers.append(
                reason if reason != "invalid" else f"normal_ball_id_invalid_{index}"
            )
            continue
        chart_id = item["chart_id"]
        if not isinstance(chart_id, str) or not chart_id:
            blockers.append(f"normal_ball_chart_id_invalid_{ball_id}")
        digest = item["source_normal_ball_digest"]
        ok, reason = _unique_string(
            digest, seen_digests, "duplicate_source_normal_ball_digest"
        )
        if not ok:
            blockers.append(
                reason
                if reason != "invalid"
                else f"source_normal_ball_digest_missing_{ball_id}"
            )
        errors, center = vector(item["center"], coordinates, f"normal_ball_center_{ball_id}")
        blockers.extend(errors)
        radius = item["radius"]
        injectivity = item["source_injectivity_radius_lower_bound"]
        if not finite(radius) or float(radius) <= 0:
            blockers.append(f"normal_ball_radius_invalid_{ball_id}")
        if not finite(injectivity) or float(injectivity) <= 0:
            blockers.append(f"injectivity_lower_bound_invalid_{ball_id}")
        if finite(radius) and finite(injectivity) and float(radius) >= float(injectivity) - TOL:
            blockers.append(f"normal_ball_not_inside_injectivity_bound_{ball_id}")
        if errors or not finite(radius) or not finite(injectivity):
            continue
        out.append(
            {
                "ball_id": ball_id,
                "center": center,
                "radius": float(radius),
                "source_injectivity_radius_lower_bound": float(injectivity),
                "chart_id": chart_id,
                "source_normal_ball_digest": digest,
            }
        )
    return blockers, sorted(out, key=lambda item: item["ball_id"])


def normalize_samples(values: Any, coordinates: Sequence[str]):
    if not isinstance(values, list) or not values:
        return ["covered_samples_empty"], []
    fields = {"sample_id", "point", "assigned_ball_id", "source_sample_digest"}
    blockers, out = [], []
    seen_ids, seen_digests = set(), set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"covered_sample_schema_invalid_{index}")
            continue
        sample_id = item["sample_id"]
        ok, reason = _unique_string(sample_id, seen_ids, "duplicate_covered_sample_id")
        if not ok:
            blockers.append(
                reason if reason != "invalid" else f"covered_sample_id_invalid_{index}"
            )
            continue
        assigned = item["assigned_ball_id"]
        if not isinstance(assigned, str) or not assigned:
            blockers.append(f"assigned_ball_id_invalid_{sample_id}")
        digest = item["source_sample_digest"]
        ok, reason = _unique_string(digest, seen_digests, "duplicate_source_sample_digest")
        if not ok:
            blockers.append(
                reason if reason != "invalid" else f"source_sample_digest_missing_{sample_id}"
            )
        errors, point = vector(item["point"], coordinates, f"covered_sample_point_{sample_id}")
        blockers.extend(errors)
        if not errors:
            out.append(
                {
                    "sample_id": sample_id,
                    "point": point,
                    "assigned_ball_id": assigned,
                    "source_sample_digest": digest,
                }
            )
    return blockers, sorted(out, key=lambda item: item["sample_id"])


def normalize_edges(values: Any, coordinates: Sequence[str]):
    if not isinstance(values, list) or not values:
        return ["nerve_edges_empty"], []
    fields = {
        "edge_id",
        "left_ball_id",
        "right_ball_id",
        "overlap_witness",
        "source_overlap_digest",
    }
    blockers, out = [], []
    seen_ids, seen_pairs, seen_digests = set(), set(), set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"nerve_edge_schema_invalid_{index}")
            continue
        edge_id = item["edge_id"]
        ok, reason = _unique_string(edge_id, seen_ids, "duplicate_nerve_edge_id")
        if not ok:
            blockers.append(reason if reason != "invalid" else f"nerve_edge_id_invalid_{index}")
            continue
        left, right = item["left_ball_id"], item["right_ball_id"]
        if not all(isinstance(v, str) and v for v in (left, right)):
            blockers.append(f"nerve_edge_vertex_invalid_{edge_id}")
            continue
        if left == right:
            blockers.append(f"nerve_edge_loop_{edge_id}")
        pair = canonical_edge(left, right)
        if pair in seen_pairs:
            blockers.append("duplicate_nerve_edge_pair")
        seen_pairs.add(pair)
        digest = item["source_overlap_digest"]
        ok, reason = _unique_string(digest, seen_digests, "duplicate_source_overlap_digest")
        if not ok:
            blockers.append(reason if reason != "invalid" else f"source_overlap_digest_missing_{edge_id}")
        errors, witness = vector(item["overlap_witness"], coordinates, f"overlap_witness_{edge_id}")
        blockers.extend(errors)
        if not errors:
            out.append(
                {
                    "edge_id": edge_id,
                    "left_ball_id": pair[0],
                    "right_ball_id": pair[1],
                    "overlap_witness": witness,
                    "source_overlap_digest": digest,
                }
            )
    return blockers, sorted(out, key=lambda item: (item["left_ball_id"], item["right_ball_id"]))


def normalize_triangles(values: Any, coordinates: Sequence[str]):
    if not isinstance(values, list) or not values:
        return ["cech_triangles_empty"], []
    fields = {
        "triangle_id",
        "vertex_ball_ids",
        "triple_overlap_witness",
        "source_triple_overlap_digest",
    }
    blockers, out = [], []
    seen_ids, seen_vertices, seen_digests = set(), set(), set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"cech_triangle_schema_invalid_{index}")
            continue
        triangle_id = item["triangle_id"]
        ok, reason = _unique_string(triangle_id, seen_ids, "duplicate_cech_triangle_id")
        if not ok:
            blockers.append(reason if reason != "invalid" else f"cech_triangle_id_invalid_{index}")
            continue
        vertices = item["vertex_ball_ids"]
        if (
            not isinstance(vertices, list)
            or len(vertices) != 3
            or any(not isinstance(v, str) or not v for v in vertices)
            or len(set(vertices)) != 3
        ):
            blockers.append(f"cech_triangle_vertices_invalid_{triangle_id}")
            continue
        canonical = tuple(sorted(vertices))
        if canonical in seen_vertices:
            blockers.append("duplicate_cech_triangle_vertices")
        seen_vertices.add(canonical)
        digest = item["source_triple_overlap_digest"]
        ok, reason = _unique_string(
            digest, seen_digests, "duplicate_source_triple_overlap_digest"
        )
        if not ok:
            blockers.append(
                reason if reason != "invalid" else f"source_triple_overlap_digest_missing_{triangle_id}"
            )
        errors, witness = vector(
            item["triple_overlap_witness"], coordinates, f"triple_overlap_witness_{triangle_id}"
        )
        blockers.extend(errors)
        if not errors:
            out.append(
                {
                    "triangle_id": triangle_id,
                    "vertex_ball_ids": list(canonical),
                    "triple_overlap_witness": witness,
                    "source_triple_overlap_digest": digest,
                }
            )
    return blockers, sorted(out, key=lambda item: tuple(item["vertex_ball_ids"]))


def normalize_paths(values: Any):
    if not isinstance(values, list) or len(values) < 2:
        return ["nerve_paths_insufficient"], []
    fields = {"path_id", "vertex_sequence", "source_path_digest"}
    blockers, out = [], []
    seen_ids, seen_digests = set(), set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"nerve_path_schema_invalid_{index}")
            continue
        path_id = item["path_id"]
        ok, reason = _unique_string(path_id, seen_ids, "duplicate_nerve_path_id")
        if not ok:
            blockers.append(reason if reason != "invalid" else f"nerve_path_id_invalid_{index}")
            continue
        vertices = item["vertex_sequence"]
        if not isinstance(vertices, list) or len(vertices) < 2 or any(not isinstance(v, str) or not v for v in vertices):
            blockers.append(f"nerve_path_vertices_invalid_{path_id}")
            continue
        if any(left == right for left, right in zip(vertices, vertices[1:])):
            blockers.append(f"nerve_path_stationary_edge_{path_id}")
        digest = item["source_path_digest"]
        ok, reason = _unique_string(digest, seen_digests, "duplicate_source_path_digest")
        if not ok:
            blockers.append(reason if reason != "invalid" else f"source_path_digest_missing_{path_id}")
        out.append({"path_id": path_id, "vertex_sequence": list(vertices), "source_path_digest": digest})
    return blockers, sorted(out, key=lambda item: item["path_id"])


def normalize_moves(values: Any):
    if not isinstance(values, list) or not values:
        return ["path_homotopy_moves_empty"], []
    fields = {
        "move_id",
        "move_kind",
        "source_path_id",
        "target_path_id",
        "triangle_id",
        "source_move_digest",
    }
    blockers, out = [], []
    seen_ids, seen_digests = set(), set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"path_homotopy_move_schema_invalid_{index}")
            continue
        move_id = item["move_id"]
        ok, reason = _unique_string(move_id, seen_ids, "duplicate_path_homotopy_move_id")
        if not ok:
            blockers.append(reason if reason != "invalid" else f"path_homotopy_move_id_invalid_{index}")
            continue
        kind = item["move_kind"]
        if kind not in {"triangle_contraction", "triangle_expansion"}:
            blockers.append(f"path_homotopy_move_kind_invalid_{move_id}")
        for name in ("source_path_id", "target_path_id", "triangle_id"):
            if not isinstance(item[name], str) or not item[name]:
                blockers.append(f"{name}_invalid_{move_id}")
        digest = item["source_move_digest"]
        ok, reason = _unique_string(digest, seen_digests, "duplicate_source_move_digest")
        if not ok:
            blockers.append(reason if reason != "invalid" else f"source_move_digest_missing_{move_id}")
        out.append(dict(item))
    return blockers, sorted(out, key=lambda item: item["move_id"])


def compute_input_digest(
    *,
    coordinate_schema,
    normal_ball_records,
    covered_samples,
    nerve_edges,
    cech_triangles,
    nerve_paths,
    path_homotopy_moves,
):
    return canonical_digest(
        {
            "coordinate_schema": list(coordinate_schema),
            "normal_ball_records": sorted(normal_ball_records, key=lambda x: str(x["ball_id"])),
            "covered_samples": sorted(covered_samples, key=lambda x: str(x["sample_id"])),
            "nerve_edges": sorted(
                nerve_edges,
                key=lambda x: canonical_edge(str(x["left_ball_id"]), str(x["right_ball_id"])),
            ),
            "cech_triangles": sorted(
                cech_triangles,
                key=lambda x: tuple(sorted(str(v) for v in x["vertex_ball_ids"])),
            ),
            "nerve_paths": sorted(nerve_paths, key=lambda x: str(x["path_id"])),
            "path_homotopy_moves": sorted(path_homotopy_moves, key=lambda x: str(x["move_id"])),
        }
    )


def path_valid(vertices: Sequence[str], edges: set[tuple[str, str]]) -> bool:
    return all(canonical_edge(left, right) in edges for left, right in zip(vertices, vertices[1:]))


def apply_triangle_move(source, target, triangle_vertices, kind) -> bool:
    if source[0] != target[0] or source[-1] != target[-1]:
        return False
    if kind == "triangle_expansion":
        return apply_triangle_move(target, source, triangle_vertices, "triangle_contraction")
    if kind != "triangle_contraction" or len(source) != len(target) + 1:
        return False
    triangle = set(triangle_vertices)
    for index in range(len(source) - 2):
        first, middle, last = source[index : index + 3]
        if len({first, middle, last}) == 3 and {first, middle, last} == triangle:
            candidate = list(source[: index + 1]) + list(source[index + 2 :])
            if candidate == list(target):
                return True
    return False


def connected_vertices(vertices: set[str], edges: set[tuple[str, str]], root: str):
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        if left in adjacency and right in adjacency:
            adjacency[left].add(right)
            adjacency[right].add(left)
    seen, frontier = {root}, [root]
    while frontier:
        current = frontier.pop()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                frontier.append(neighbor)
    return seen
