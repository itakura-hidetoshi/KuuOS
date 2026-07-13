#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any, Mapping, Sequence

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
TOL = 1e-9


@dataclass
class FiniteNormalBallCoverHopfRinowWitnessCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


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


def _vector(value: Any, coordinates: Sequence[str], prefix: str) -> tuple[list[str], dict[str, float]]:
    if not isinstance(value, dict) or set(value) != set(coordinates):
        return [f"{prefix}_schema_invalid"], {}
    if any(not finite(value[c]) for c in coordinates):
        return [f"{prefix}_nonfinite"], {}
    return [], {c: float(value[c]) for c in coordinates}


def _distance(left: Mapping[str, float], right: Mapping[str, float], coordinates: Sequence[str]) -> float:
    return math.sqrt(sum((left[c] - right[c]) ** 2 for c in coordinates))


def _text(value: Any, blocker: str, blockers: list[str]) -> str:
    if not isinstance(value, str) or not value:
        blockers.append(blocker)
        return ""
    return value


def _unique(value: str, seen: set[str], blocker: str, blockers: list[str]) -> None:
    if value in seen:
        blockers.append(blocker)
    seen.add(value)


def _normalize_balls(value: Any, coordinates: Sequence[str]) -> tuple[list[str], list[dict]]:
    if not isinstance(value, list) or not value:
        return ["normal_ball_records_empty"], []
    blockers: list[str] = []
    fields = {
        "ball_id", "center", "radius", "source_injectivity_radius_lower_bound",
        "chart_id", "source_normal_ball_digest",
    }
    ids: set[str] = set()
    digests: set[str] = set()
    out: list[dict] = []
    for index, record in enumerate(value):
        if not isinstance(record, dict) or set(record) != fields:
            blockers.append(f"normal_ball_schema_invalid_{index}")
            continue
        ball_id = _text(record["ball_id"], f"normal_ball_id_invalid_{index}", blockers)
        chart_id = _text(record["chart_id"], f"normal_ball_chart_id_invalid_{index}", blockers)
        digest = _text(record["source_normal_ball_digest"], f"source_normal_ball_digest_missing_{index}", blockers)
        if ball_id:
            _unique(ball_id, ids, "duplicate_normal_ball_id", blockers)
        if digest:
            _unique(digest, digests, "duplicate_source_normal_ball_digest", blockers)
        center_errors, center = _vector(record["center"], coordinates, f"normal_ball_center_{ball_id or index}")
        blockers.extend(center_errors)
        radius = record["radius"]
        injectivity = record["source_injectivity_radius_lower_bound"]
        if not finite(radius) or float(radius) <= 0.0:
            blockers.append(f"normal_ball_radius_invalid_{ball_id or index}")
        if not finite(injectivity) or float(injectivity) <= 0.0:
            blockers.append(f"normal_ball_injectivity_bound_invalid_{ball_id or index}")
        if finite(radius) and finite(injectivity) and float(radius) >= float(injectivity) - TOL:
            blockers.append(f"normal_ball_not_inside_injectivity_bound_{ball_id or index}")
        if ball_id and chart_id and digest and not center_errors and finite(radius) and finite(injectivity):
            out.append({
                "ball_id": ball_id,
                "center": center,
                "radius": float(radius),
                "source_injectivity_radius_lower_bound": float(injectivity),
                "chart_id": chart_id,
                "source_normal_ball_digest": digest,
            })
    return blockers, sorted(out, key=lambda item: item["ball_id"])


def _normalize_samples(value: Any, coordinates: Sequence[str]) -> tuple[list[str], list[dict]]:
    if not isinstance(value, list) or not value:
        return ["cover_sample_points_empty"], []
    blockers: list[str] = []
    fields = {"sample_id", "point", "assigned_ball_id", "source_sample_digest"}
    ids: set[str] = set()
    digests: set[str] = set()
    out: list[dict] = []
    for index, record in enumerate(value):
        if not isinstance(record, dict) or set(record) != fields:
            blockers.append(f"cover_sample_schema_invalid_{index}")
            continue
        sample_id = _text(record["sample_id"], f"cover_sample_id_invalid_{index}", blockers)
        ball_id = _text(record["assigned_ball_id"], f"assigned_ball_id_invalid_{index}", blockers)
        digest = _text(record["source_sample_digest"], f"source_sample_digest_missing_{index}", blockers)
        if sample_id:
            _unique(sample_id, ids, "duplicate_cover_sample_id", blockers)
        if digest:
            _unique(digest, digests, "duplicate_source_sample_digest", blockers)
        point_errors, point = _vector(record["point"], coordinates, f"cover_sample_point_{sample_id or index}")
        blockers.extend(point_errors)
        if sample_id and ball_id and digest and not point_errors:
            out.append({
                "sample_id": sample_id,
                "point": point,
                "assigned_ball_id": ball_id,
                "source_sample_digest": digest,
            })
    return blockers, sorted(out, key=lambda item: item["sample_id"])


def _normalize_overlaps(value: Any, coordinates: Sequence[str]) -> tuple[list[str], list[dict]]:
    if not isinstance(value, list):
        return ["overlap_records_invalid"], []
    blockers: list[str] = []
    fields = {"overlap_id", "left_ball_id", "right_ball_id", "witness_point", "source_overlap_digest"}
    ids: set[str] = set()
    digests: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    out: list[dict] = []
    for index, record in enumerate(value):
        if not isinstance(record, dict) or set(record) != fields:
            blockers.append(f"overlap_schema_invalid_{index}")
            continue
        overlap_id = _text(record["overlap_id"], f"overlap_id_invalid_{index}", blockers)
        left = _text(record["left_ball_id"], f"left_ball_id_invalid_{index}", blockers)
        right = _text(record["right_ball_id"], f"right_ball_id_invalid_{index}", blockers)
        digest = _text(record["source_overlap_digest"], f"source_overlap_digest_missing_{index}", blockers)
        if overlap_id:
            _unique(overlap_id, ids, "duplicate_overlap_id", blockers)
        if digest:
            _unique(digest, digests, "duplicate_source_overlap_digest", blockers)
        if left and right:
            if left == right:
                blockers.append(f"overlap_self_pair_{overlap_id or index}")
            pair = tuple(sorted((left, right)))
            if pair in pairs:
                blockers.append("duplicate_overlap_ball_pair")
            pairs.add(pair)
        point_errors, point = _vector(record["witness_point"], coordinates, f"overlap_witness_{overlap_id or index}")
        blockers.extend(point_errors)
        if overlap_id and left and right and digest and not point_errors:
            out.append({
                "overlap_id": overlap_id,
                "left_ball_id": left,
                "right_ball_id": right,
                "witness_point": point,
                "source_overlap_digest": digest,
            })
    return blockers, sorted(out, key=lambda item: item["overlap_id"])


def _normalize_segments(value: Any, coordinates: Sequence[str]) -> tuple[list[str], list[dict]]:
    if not isinstance(value, list) or not value:
        return ["geodesic_extension_segments_empty"], []
    blockers: list[str] = []
    fields = {
        "segment_id", "start_parameter", "end_parameter", "length",
        "start_point", "end_point", "start_tangent", "end_tangent",
        "normal_ball_id", "source_segment_digest",
    }
    ids: set[str] = set()
    digests: set[str] = set()
    out: list[dict] = []
    for index, record in enumerate(value):
        if not isinstance(record, dict) or set(record) != fields:
            blockers.append(f"extension_segment_schema_invalid_{index}")
            continue
        segment_id = _text(record["segment_id"], f"extension_segment_id_invalid_{index}", blockers)
        ball_id = _text(record["normal_ball_id"], f"extension_segment_ball_id_invalid_{index}", blockers)
        digest = _text(record["source_segment_digest"], f"source_segment_digest_missing_{index}", blockers)
        if segment_id:
            _unique(segment_id, ids, "duplicate_extension_segment_id", blockers)
        if digest:
            _unique(digest, digests, "duplicate_source_segment_digest", blockers)
        scalars: dict[str, float] = {}
        scalars_ok = True
        for name in ("start_parameter", "end_parameter", "length"):
            if not finite(record[name]):
                blockers.append(f"extension_segment_{name}_invalid_{segment_id or index}")
                scalars_ok = False
            else:
                scalars[name] = float(record[name])
        vectors: dict[str, dict[str, float]] = {}
        vectors_ok = True
        for name in ("start_point", "end_point", "start_tangent", "end_tangent"):
            errors, vector = _vector(record[name], coordinates, f"extension_segment_{name}_{segment_id or index}")
            blockers.extend(errors)
            vectors_ok = vectors_ok and not errors
            vectors[name] = vector
        if segment_id and ball_id and digest and scalars_ok and vectors_ok:
            out.append({
                "segment_id": segment_id,
                **scalars,
                **vectors,
                "normal_ball_id": ball_id,
                "source_segment_digest": digest,
            })
    return blockers, sorted(out, key=lambda item: (item["start_parameter"], item["segment_id"]))


def compute_finite_cover_input_digest(
    *,
    coordinate_schema: Sequence[str],
    normal_ball_records: Sequence[Mapping[str, Any]],
    cover_sample_points: Sequence[Mapping[str, Any]],
    overlap_records: Sequence[Mapping[str, Any]],
    geodesic_extension_segments: Sequence[Mapping[str, Any]],
) -> str:
    coordinates = list(coordinate_schema)
    def vec(value: Mapping[str, Any]) -> dict[str, float]:
        return {c: float(value[c]) for c in coordinates}
    balls = sorted(({
        "ball_id": str(x["ball_id"]), "center": vec(x["center"]),
        "radius": float(x["radius"]),
        "source_injectivity_radius_lower_bound": float(x["source_injectivity_radius_lower_bound"]),
        "chart_id": str(x["chart_id"]),
        "source_normal_ball_digest": str(x["source_normal_ball_digest"]),
    } for x in normal_ball_records), key=lambda x: x["ball_id"])
    samples = sorted(({
        "sample_id": str(x["sample_id"]), "point": vec(x["point"]),
        "assigned_ball_id": str(x["assigned_ball_id"]),
        "source_sample_digest": str(x["source_sample_digest"]),
    } for x in cover_sample_points), key=lambda x: x["sample_id"])
    overlaps = sorted(({
        "overlap_id": str(x["overlap_id"]),
        "left_ball_id": str(x["left_ball_id"]),
        "right_ball_id": str(x["right_ball_id"]),
        "witness_point": vec(x["witness_point"]),
        "source_overlap_digest": str(x["source_overlap_digest"]),
    } for x in overlap_records), key=lambda x: x["overlap_id"])
    segments = sorted(({
        "segment_id": str(x["segment_id"]),
        "start_parameter": float(x["start_parameter"]),
        "end_parameter": float(x["end_parameter"]),
        "length": float(x["length"]),
        "start_point": vec(x["start_point"]),
        "end_point": vec(x["end_point"]),
        "start_tangent": vec(x["start_tangent"]),
        "end_tangent": vec(x["end_tangent"]),
        "normal_ball_id": str(x["normal_ball_id"]),
        "source_segment_digest": str(x["source_segment_digest"]),
    } for x in geodesic_extension_segments), key=lambda x: (x["start_parameter"], x["segment_id"]))
    return canonical_digest({
        "coordinate_schema": coordinates,
        "normal_ball_records": balls,
        "cover_sample_points": samples,
        "overlap_records": overlaps,
        "geodesic_extension_segments": segments,
    })


def build_finite_normal_ball_cover_hopf_rinow_witness_certificate(
    *,
    source_exponential_map_certificate_digest: str,
    source_atlas_certificate_digest: str,
    finite_cover_input_digest: str,
    coordinate_schema: list[str],
    normal_ball_records: list[dict],
    cover_sample_points: list[dict],
    overlap_records: list[dict],
    geodesic_extension_segments: list[dict],
    finite_window_start: float,
    finite_window_end: float,
    maximum_segment_length_fraction: float,
    minimum_overlap_margin: float,
    maximum_junction_position_residual: float,
    maximum_junction_tangent_jump: float,
) -> FiniteNormalBallCoverHopfRinowWitnessCertificateResult:
    blockers: list[str] = []
    for name, value in {
        "source_exponential_map_certificate_digest": source_exponential_map_certificate_digest,
        "source_atlas_certificate_digest": source_atlas_certificate_digest,
        "finite_cover_input_digest": finite_cover_input_digest,
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
        coordinates: list[str] = []
    else:
        coordinates = list(coordinate_schema)
    scalars = {
        "finite_window_start": finite_window_start,
        "finite_window_end": finite_window_end,
        "maximum_segment_length_fraction": maximum_segment_length_fraction,
        "minimum_overlap_margin": minimum_overlap_margin,
        "maximum_junction_position_residual": maximum_junction_position_residual,
        "maximum_junction_tangent_jump": maximum_junction_tangent_jump,
    }
    for name, value in scalars.items():
        if not finite(value):
            blockers.append(f"{name}_invalid")
    if finite(finite_window_start) and finite(finite_window_end) and float(finite_window_start) >= float(finite_window_end) - TOL:
        blockers.append("finite_window_not_positive")
    if finite(maximum_segment_length_fraction) and not (0.0 < float(maximum_segment_length_fraction) < 1.0):
        blockers.append("maximum_segment_length_fraction_out_of_range")
    for name in ("minimum_overlap_margin", "maximum_junction_position_residual", "maximum_junction_tangent_jump"):
        if finite(scalars[name]) and float(scalars[name]) < 0.0:
            blockers.append(f"{name}_negative")

    ball_errors, balls = _normalize_balls(normal_ball_records, coordinates)
    sample_errors, samples = _normalize_samples(cover_sample_points, coordinates)
    overlap_errors, overlaps = _normalize_overlaps(overlap_records, coordinates)
    segment_errors, segments = _normalize_segments(geodesic_extension_segments, coordinates)
    blockers.extend(ball_errors + sample_errors + overlap_errors + segment_errors)
    if blockers:
        return FiniteNormalBallCoverHopfRinowWitnessCertificateResult(STATUS_BLOCKED, sorted(set(blockers)), None)

    expected_digest = compute_finite_cover_input_digest(
        coordinate_schema=coordinates,
        normal_ball_records=balls,
        cover_sample_points=samples,
        overlap_records=overlaps,
        geodesic_extension_segments=segments,
    )
    if finite_cover_input_digest != expected_digest:
        blockers.append("finite_cover_input_digest_mismatch")

    ball_map = {x["ball_id"]: x for x in balls}
    overlap_map: dict[tuple[str, str], dict] = {}
    overlap_out: list[dict] = []
    min_clearance = math.inf
    for overlap in overlaps:
        left = ball_map.get(overlap["left_ball_id"])
        right = ball_map.get(overlap["right_ball_id"])
        if left is None or right is None:
            blockers.append(f"overlap_ball_missing_{overlap['overlap_id']}")
            continue
        witness = overlap["witness_point"]
        left_clearance = left["radius"] - _distance(left["center"], witness, coordinates)
        right_clearance = right["radius"] - _distance(right["center"], witness, coordinates)
        clearance = min(left_clearance, right_clearance)
        min_clearance = min(min_clearance, clearance)
        if clearance < float(minimum_overlap_margin) - TOL:
            blockers.append(f"overlap_margin_insufficient_{overlap['overlap_id']}")
        overlap_map[tuple(sorted((left["ball_id"], right["ball_id"])))] = overlap
        overlap_out.append({
            **overlap,
            "left_ball_clearance": left_clearance,
            "right_ball_clearance": right_clearance,
            "computed_overlap_clearance": clearance,
        })
    if math.isinf(min_clearance):
        min_clearance = 0.0

    sample_out: list[dict] = []
    max_sample_fraction = 0.0
    for sample in samples:
        ball = ball_map.get(sample["assigned_ball_id"])
        if ball is None:
            blockers.append(f"assigned_normal_ball_missing_{sample['sample_id']}")
            continue
        distance = _distance(sample["point"], ball["center"], coordinates)
        fraction = distance / ball["radius"]
        max_sample_fraction = max(max_sample_fraction, fraction)
        if distance >= ball["radius"] - TOL:
            blockers.append(f"cover_sample_outside_assigned_ball_{sample['sample_id']}")
        sample_out.append({
            **sample,
            "distance_from_assigned_ball_center": distance,
            "assigned_ball_radial_fraction": fraction,
            "covered_by_assigned_normal_ball": distance < ball["radius"],
        })

    segment_out: list[dict] = []
    total_length = 0.0
    max_segment_fraction = 0.0
    max_position_residual = 0.0
    max_tangent_jump = 0.0
    for index, segment in enumerate(segments):
        sid = segment["segment_id"]
        start, end, length = segment["start_parameter"], segment["end_parameter"], segment["length"]
        if start >= end - TOL:
            blockers.append(f"extension_segment_parameter_order_invalid_{sid}")
        expected_length = end - start
        if abs(length - expected_length) > TOL:
            blockers.append(f"extension_segment_length_mismatch_{sid}")
        if length <= 0.0:
            blockers.append(f"extension_segment_length_nonpositive_{sid}")
        ball = ball_map.get(segment["normal_ball_id"])
        if ball is None:
            blockers.append(f"extension_segment_ball_missing_{sid}")
            continue
        start_distance = _distance(segment["start_point"], ball["center"], coordinates)
        end_distance = _distance(segment["end_point"], ball["center"], coordinates)
        if start_distance >= ball["radius"] - TOL:
            blockers.append(f"extension_segment_start_outside_ball_{sid}")
        if end_distance >= ball["radius"] - TOL:
            blockers.append(f"extension_segment_end_outside_ball_{sid}")
        allowed = float(maximum_segment_length_fraction) * ball["radius"]
        if length > allowed + TOL:
            blockers.append(f"extension_segment_too_long_for_ball_{sid}")
        fraction = length / ball["radius"]
        max_segment_fraction = max(max_segment_fraction, fraction)
        total_length += length
        segment_out.append({
            **segment,
            "computed_length": expected_length,
            "start_distance_from_ball_center": start_distance,
            "end_distance_from_ball_center": end_distance,
            "maximum_allowed_segment_length": allowed,
            "segment_radius_fraction": fraction,
            "locally_extendible_inside_normal_ball": (
                length <= allowed + TOL
                and start_distance < ball["radius"]
                and end_distance < ball["radius"]
            ),
        })
        if index == 0:
            if abs(start - float(finite_window_start)) > TOL:
                blockers.append("extension_chain_start_mismatch")
            continue
        previous = segments[index - 1]
        if abs(previous["end_parameter"] - start) > TOL:
            blockers.append(f"extension_chain_parameter_gap_{sid}")
        position_residual = _distance(previous["end_point"], segment["start_point"], coordinates)
        tangent_jump = _distance(previous["end_tangent"], segment["start_tangent"], coordinates)
        max_position_residual = max(max_position_residual, position_residual)
        max_tangent_jump = max(max_tangent_jump, tangent_jump)
        if position_residual > float(maximum_junction_position_residual) + TOL:
            blockers.append(f"extension_chain_position_residual_{sid}")
        if tangent_jump > float(maximum_junction_tangent_jump) + TOL:
            blockers.append(f"extension_chain_tangent_jump_{sid}")
        left_ball, right_ball = previous["normal_ball_id"], segment["normal_ball_id"]
        if left_ball != right_ball:
            overlap = overlap_map.get(tuple(sorted((left_ball, right_ball))))
            if overlap is None:
                blockers.append(f"extension_chain_ball_overlap_missing_{sid}")
            elif _distance(overlap["witness_point"], segment["start_point"], coordinates) > float(maximum_junction_position_residual) + TOL:
                blockers.append(f"extension_chain_overlap_witness_mismatch_{sid}")

    if segments and abs(segments[-1]["end_parameter"] - float(finite_window_end)) > TOL:
        blockers.append("extension_chain_end_mismatch")
    window_length = float(finite_window_end) - float(finite_window_start)
    if abs(total_length - window_length) > TOL:
        blockers.append("extension_total_length_mismatch")
    if blockers:
        return FiniteNormalBallCoverHopfRinowWitnessCertificateResult(STATUS_BLOCKED, sorted(set(blockers)), None)

    envelope = {
        c: {
            "lower": min(ball["center"][c] - ball["radius"] for ball in balls),
            "upper": max(ball["center"][c] + ball["radius"] for ball in balls),
        }
        for c in coordinates
    }
    diameter = math.sqrt(sum((envelope[c]["upper"] - envelope[c]["lower"]) ** 2 for c in coordinates))
    certificate = {
        "kernel": "PlanOS Finite Normal-Ball Cover and Bounded Hopf-Rinow Witness Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.13",
        "source_exponential_map_certificate_digest": source_exponential_map_certificate_digest,
        "source_atlas_certificate_digest": source_atlas_certificate_digest,
        "finite_cover_input_digest": finite_cover_input_digest,
        "coordinate_schema": coordinates,
        "normal_ball_records": balls,
        "cover_sample_points": sample_out,
        "overlap_records": overlap_out,
        "geodesic_extension_segments": segment_out,
        "finite_window_start": float(finite_window_start),
        "finite_window_end": float(finite_window_end),
        "finite_window_length": window_length,
        "maximum_segment_length_fraction": float(maximum_segment_length_fraction),
        "minimum_overlap_margin": float(minimum_overlap_margin),
        "maximum_junction_position_residual": float(maximum_junction_position_residual),
        "maximum_junction_tangent_jump": float(maximum_junction_tangent_jump),
        "computed_total_extension_length": total_length,
        "computed_minimum_overlap_clearance": min_clearance,
        "computed_maximum_sample_radial_fraction": max_sample_fraction,
        "computed_maximum_segment_radius_fraction": max_segment_fraction,
        "computed_maximum_junction_position_residual": max_position_residual,
        "computed_maximum_junction_tangent_jump": max_tangent_jump,
        "finite_cover_coordinate_envelope": envelope,
        "finite_cover_coordinate_diameter_bound": diameter,
        "finite_normal_ball_cover_certified": True,
        "all_retained_samples_covered": True,
        "normal_ball_overlap_chain_certified": True,
        "local_geodesic_extension_chain_certified": True,
        "finite_window_fully_extended": True,
        "finite_cover_coordinate_bound_certified": True,
        "bounded_hopf_rinow_finite_window_witness": True,
        "classical_hopf_rinow_equivalence_not_claimed": True,
        "global_geodesic_completeness_not_claimed": True,
        "global_metric_completeness_not_claimed": True,
        "global_compactness_not_claimed": True,
        "global_minimizing_geodesic_not_claimed": True,
        "local_finite_witness_only": True,
        "source_exponential_map_certificate_not_mutated": True,
        "source_atlas_certificate_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "candidate_identity_retained": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "finite_cover_grants_no_authority": True,
        "geodesic_extension_grants_no_authority": True,
        "hopf_rinow_witness_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["finite_normal_ball_cover_certificate_digest"] = canonical_digest(certificate)
    return FiniteNormalBallCoverHopfRinowWitnessCertificateResult(STATUS_READY, [], certificate)
