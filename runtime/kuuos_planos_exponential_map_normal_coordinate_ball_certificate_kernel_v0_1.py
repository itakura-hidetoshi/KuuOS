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
class ExponentialMapNormalCoordinateBallCertificateResult:
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


def _vector(
    value: Any,
    coordinates: Sequence[str],
    blocker_prefix: str,
) -> tuple[list[str], dict[str, float]]:
    if not isinstance(value, dict) or set(value) != set(coordinates):
        return [f"{blocker_prefix}_schema_invalid"], {}
    if any(not finite(value[c]) for c in coordinates):
        return [f"{blocker_prefix}_nonfinite"], {}
    return [], {c: float(value[c]) for c in coordinates}


def _matrix(
    value: Any,
    coordinates: Sequence[str],
    blocker_prefix: str,
) -> tuple[list[str], dict[str, dict[str, float]]]:
    if not isinstance(value, dict) or set(value) != set(coordinates):
        return [f"{blocker_prefix}_row_schema_invalid"], {}
    out: dict[str, dict[str, float]] = {}
    blockers: list[str] = []
    for i in coordinates:
        row = value[i]
        if not isinstance(row, dict) or set(row) != set(coordinates):
            blockers.append(f"{blocker_prefix}_column_schema_invalid_{i}")
            continue
        if any(not finite(row[j]) for j in coordinates):
            blockers.append(f"{blocker_prefix}_nonfinite_{i}")
            continue
        out[i] = {j: float(row[j]) for j in coordinates}
    return blockers, out


def _connection(
    value: Any,
    coordinates: Sequence[str],
) -> tuple[list[str], dict[str, dict[str, dict[str, float]]]]:
    if not isinstance(value, dict) or set(value) != set(coordinates):
        return ["christoffel_output_schema_invalid"], {}
    blockers: list[str] = []
    out: dict[str, dict[str, dict[str, float]]] = {}
    for i in coordinates:
        if not isinstance(value[i], dict) or set(value[i]) != set(coordinates):
            blockers.append(f"christoffel_first_input_schema_invalid_{i}")
            continue
        out[i] = {}
        for j in coordinates:
            row = value[i][j]
            if not isinstance(row, dict) or set(row) != set(coordinates):
                blockers.append(f"christoffel_second_input_schema_invalid_{i}_{j}")
                continue
            if any(not finite(row[k]) for k in coordinates):
                blockers.append(f"christoffel_nonfinite_{i}_{j}")
                continue
            out[i][j] = {k: float(row[k]) for k in coordinates}
    return blockers, out


def _cholesky_positive_definite(
    matrix: Mapping[str, Mapping[str, float]],
    coordinates: Sequence[str],
) -> bool:
    n = len(coordinates)
    lower = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            total = sum(lower[i][k] * lower[j][k] for k in range(j))
            value = float(matrix[coordinates[i]][coordinates[j]]) - total
            if i == j:
                if value <= TOL:
                    return False
                lower[i][j] = math.sqrt(value)
            else:
                if abs(lower[j][j]) <= TOL:
                    return False
                lower[i][j] = value / lower[j][j]
    return True


def _metric_norm_squared(
    vector: Mapping[str, float],
    metric: Mapping[str, Mapping[str, float]],
    coordinates: Sequence[str],
) -> float:
    return sum(
        vector[i] * metric[i][j] * vector[j]
        for i in coordinates
        for j in coordinates
    )


def _connection_contraction(
    christoffel: Mapping[str, Mapping[str, Mapping[str, float]]],
    tangent: Mapping[str, float],
    coordinates: Sequence[str],
) -> dict[str, float]:
    return {
        i: sum(
            christoffel[i][j][k] * tangent[j] * tangent[k]
            for j in coordinates
            for k in coordinates
        )
        for i in coordinates
    }


def _second_order_radial_point(
    base_point: Mapping[str, float],
    tangent: Mapping[str, float],
    christoffel: Mapping[str, Mapping[str, Mapping[str, float]]],
    coordinates: Sequence[str],
    parameter: float,
) -> dict[str, float]:
    contraction = _connection_contraction(christoffel, tangent, coordinates)
    return {
        i: base_point[i]
        + parameter * tangent[i]
        - 0.5 * parameter * parameter * contraction[i]
        for i in coordinates
    }


def _max_residual(
    left: Mapping[str, float],
    right: Mapping[str, float],
    coordinates: Sequence[str],
) -> float:
    return max(abs(left[i] - right[i]) for i in coordinates)


def _euclidean_distance(
    left: Mapping[str, float],
    right: Mapping[str, float],
    coordinates: Sequence[str],
) -> float:
    return math.sqrt(sum((left[i] - right[i]) ** 2 for i in coordinates))


def _normalize_charts(
    charts: Any,
    coordinates: Sequence[str],
) -> tuple[list[str], list[dict]]:
    blockers: list[str] = []
    if not isinstance(charts, list) or not charts:
        return ["chart_records_empty"], []
    fields = {
        "chart_id",
        "center",
        "safe_radius",
        "coordinate_lower_bounds",
        "coordinate_upper_bounds",
        "source_chart_digest",
    }
    seen_ids: set[str] = set()
    seen_digests: set[str] = set()
    out: list[dict] = []
    for index, chart in enumerate(charts):
        if not isinstance(chart, dict) or set(chart) != fields:
            blockers.append(f"chart_schema_invalid_{index}")
            continue
        chart_id = chart["chart_id"]
        digest = chart["source_chart_digest"]
        if not isinstance(chart_id, str) or not chart_id:
            blockers.append(f"chart_id_invalid_{index}")
            continue
        if chart_id in seen_ids:
            blockers.append("duplicate_chart_id")
        seen_ids.add(chart_id)
        if not isinstance(digest, str) or not digest:
            blockers.append(f"source_chart_digest_missing_{index}")
        elif digest in seen_digests:
            blockers.append("duplicate_source_chart_digest")
        else:
            seen_digests.add(digest)
        if not finite(chart["safe_radius"]) or float(chart["safe_radius"]) <= 0.0:
            blockers.append(f"chart_safe_radius_invalid_{chart_id}")
            continue
        center_errors, center = _vector(
            chart["center"], coordinates, f"chart_center_{chart_id}"
        )
        lower_errors, lower = _vector(
            chart["coordinate_lower_bounds"],
            coordinates,
            f"chart_lower_{chart_id}",
        )
        upper_errors, upper = _vector(
            chart["coordinate_upper_bounds"],
            coordinates,
            f"chart_upper_{chart_id}",
        )
        blockers.extend(center_errors + lower_errors + upper_errors)
        if center_errors or lower_errors or upper_errors:
            continue
        if any(lower[c] >= upper[c] for c in coordinates):
            blockers.append(f"chart_bounds_order_invalid_{chart_id}")
        if any(not (lower[c] <= center[c] <= upper[c]) for c in coordinates):
            blockers.append(f"chart_center_outside_bounds_{chart_id}")
        out.append(
            {
                "chart_id": chart_id,
                "center": center,
                "safe_radius": float(chart["safe_radius"]),
                "coordinate_lower_bounds": lower,
                "coordinate_upper_bounds": upper,
                "source_chart_digest": digest,
            }
        )
    out.sort(key=lambda item: item["chart_id"])
    return blockers, out


def _normalize_candidates(
    candidates: Any,
    coordinates: Sequence[str],
) -> tuple[list[str], list[dict]]:
    blockers: list[str] = []
    if not isinstance(candidates, list) or not candidates:
        return ["radial_geodesic_candidates_empty"], []
    fields = {
        "candidate_id",
        "tangent_vector",
        "expected_endpoint",
        "expected_midpoint",
        "assigned_chart_id",
        "source_candidate_digest",
    }
    seen_ids: set[str] = set()
    seen_digests: set[str] = set()
    out: list[dict] = []
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict) or set(candidate) != fields:
            blockers.append(f"candidate_schema_invalid_{index}")
            continue
        cid = candidate["candidate_id"]
        digest = candidate["source_candidate_digest"]
        chart_id = candidate["assigned_chart_id"]
        if not isinstance(cid, str) or not cid:
            blockers.append(f"candidate_id_invalid_{index}")
            continue
        if cid in seen_ids:
            blockers.append("duplicate_candidate_id")
        seen_ids.add(cid)
        if not isinstance(digest, str) or not digest:
            blockers.append(f"source_candidate_digest_missing_{index}")
        elif digest in seen_digests:
            blockers.append("duplicate_source_candidate_digest")
        else:
            seen_digests.add(digest)
        if not isinstance(chart_id, str) or not chart_id:
            blockers.append(f"assigned_chart_id_invalid_{cid}")
            continue
        tangent_errors, tangent = _vector(
            candidate["tangent_vector"], coordinates, f"candidate_tangent_{cid}"
        )
        endpoint_errors, endpoint = _vector(
            candidate["expected_endpoint"], coordinates, f"candidate_endpoint_{cid}"
        )
        midpoint_errors, midpoint = _vector(
            candidate["expected_midpoint"], coordinates, f"candidate_midpoint_{cid}"
        )
        blockers.extend(tangent_errors + endpoint_errors + midpoint_errors)
        if tangent_errors or endpoint_errors or midpoint_errors:
            continue
        out.append(
            {
                "candidate_id": cid,
                "tangent_vector": tangent,
                "expected_endpoint": endpoint,
                "expected_midpoint": midpoint,
                "assigned_chart_id": chart_id,
                "source_candidate_digest": digest,
            }
        )
    out.sort(key=lambda item: item["candidate_id"])
    return blockers, out


def compute_local_model_input_digest(
    *,
    coordinate_schema: Sequence[str],
    base_point: Mapping[str, float],
    metric_matrix: Mapping[str, Mapping[str, float]],
    christoffel_symbols: Mapping[str, Mapping[str, Mapping[str, float]]],
    chart_records: Sequence[Mapping[str, Any]],
    radial_geodesic_candidates: Sequence[Mapping[str, Any]],
) -> str:
    coordinates = list(coordinate_schema)
    normalized_base = {c: float(base_point[c]) for c in coordinates}
    normalized_metric = {
        i: {j: float(metric_matrix[i][j]) for j in coordinates}
        for i in coordinates
    }
    normalized_connection = {
        i: {
            j: {k: float(christoffel_symbols[i][j][k]) for k in coordinates}
            for j in coordinates
        }
        for i in coordinates
    }
    normalized_charts = sorted(
        (
            {
                "chart_id": str(chart["chart_id"]),
                "center": {c: float(chart["center"][c]) for c in coordinates},
                "safe_radius": float(chart["safe_radius"]),
                "coordinate_lower_bounds": {
                    c: float(chart["coordinate_lower_bounds"][c])
                    for c in coordinates
                },
                "coordinate_upper_bounds": {
                    c: float(chart["coordinate_upper_bounds"][c])
                    for c in coordinates
                },
                "source_chart_digest": str(chart["source_chart_digest"]),
            }
            for chart in chart_records
        ),
        key=lambda chart: chart["chart_id"],
    )
    normalized_candidates = sorted(
        (
            {
                "candidate_id": str(candidate["candidate_id"]),
                "tangent_vector": {
                    c: float(candidate["tangent_vector"][c]) for c in coordinates
                },
                "expected_endpoint": {
                    c: float(candidate["expected_endpoint"][c]) for c in coordinates
                },
                "expected_midpoint": {
                    c: float(candidate["expected_midpoint"][c]) for c in coordinates
                },
                "assigned_chart_id": str(candidate["assigned_chart_id"]),
                "source_candidate_digest": str(candidate["source_candidate_digest"]),
            }
            for candidate in radial_geodesic_candidates
        ),
        key=lambda candidate: candidate["candidate_id"],
    )
    return canonical_digest(
        {
            "coordinate_schema": coordinates,
            "base_point": normalized_base,
            "metric_matrix": normalized_metric,
            "christoffel_symbols": normalized_connection,
            "chart_records": normalized_charts,
            "radial_geodesic_candidates": normalized_candidates,
        }
    )


def build_exponential_map_normal_coordinate_ball_certificate(
    *,
    source_injectivity_radius_certificate_digest: str,
    source_atlas_certificate_digest: str,
    local_model_input_digest: str,
    coordinate_schema: list[str],
    base_point: dict,
    metric_matrix: dict,
    christoffel_symbols: dict,
    chart_records: list[dict],
    radial_geodesic_candidates: list[dict],
    source_injectivity_radius_lower_bound: float,
    normal_coordinate_ball_radius: float,
    maximum_exponential_map_residual: float,
    maximum_midpoint_residual: float,
    minimum_distinct_endpoint_separation: float,
) -> ExponentialMapNormalCoordinateBallCertificateResult:
    blockers: list[str] = []
    for name, value in {
        "source_injectivity_radius_certificate_digest": (
            source_injectivity_radius_certificate_digest
        ),
        "source_atlas_certificate_digest": source_atlas_certificate_digest,
        "local_model_input_digest": local_model_input_digest,
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
    for name, value in {
        "source_injectivity_radius_lower_bound": source_injectivity_radius_lower_bound,
        "normal_coordinate_ball_radius": normal_coordinate_ball_radius,
        "maximum_exponential_map_residual": maximum_exponential_map_residual,
        "maximum_midpoint_residual": maximum_midpoint_residual,
        "minimum_distinct_endpoint_separation": minimum_distinct_endpoint_separation,
    }.items():
        if not finite(value):
            blockers.append(f"{name}_invalid")
    if finite(source_injectivity_radius_lower_bound) and float(
        source_injectivity_radius_lower_bound
    ) <= 0.0:
        blockers.append("source_injectivity_radius_lower_bound_nonpositive")
    if finite(normal_coordinate_ball_radius) and float(
        normal_coordinate_ball_radius
    ) <= 0.0:
        blockers.append("normal_coordinate_ball_radius_nonpositive")
    if (
        finite(source_injectivity_radius_lower_bound)
        and finite(normal_coordinate_ball_radius)
        and float(normal_coordinate_ball_radius)
        >= float(source_injectivity_radius_lower_bound) - TOL
    ):
        blockers.append("normal_ball_not_strictly_inside_injectivity_bound")
    for name, value in {
        "maximum_exponential_map_residual": maximum_exponential_map_residual,
        "maximum_midpoint_residual": maximum_midpoint_residual,
        "minimum_distinct_endpoint_separation": minimum_distinct_endpoint_separation,
    }.items():
        if finite(value) and float(value) < 0.0:
            blockers.append(f"{name}_negative")

    base_errors, normalized_base = _vector(base_point, coordinates, "base_point")
    metric_errors, normalized_metric = _matrix(
        metric_matrix, coordinates, "metric"
    )
    connection_errors, normalized_connection = _connection(
        christoffel_symbols, coordinates
    )
    chart_errors, normalized_charts = _normalize_charts(chart_records, coordinates)
    candidate_errors, normalized_candidates = _normalize_candidates(
        radial_geodesic_candidates, coordinates
    )
    blockers.extend(
        base_errors
        + metric_errors
        + connection_errors
        + chart_errors
        + candidate_errors
    )
    if blockers:
        return ExponentialMapNormalCoordinateBallCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    if any(
        abs(normalized_metric[i][j] - normalized_metric[j][i]) > TOL
        for i in coordinates
        for j in coordinates
    ):
        blockers.append("metric_not_symmetric")
    elif not _cholesky_positive_definite(normalized_metric, coordinates):
        blockers.append("metric_not_positive_definite")

    expected_digest = compute_local_model_input_digest(
        coordinate_schema=coordinates,
        base_point=normalized_base,
        metric_matrix=normalized_metric,
        christoffel_symbols=normalized_connection,
        chart_records=normalized_charts,
        radial_geodesic_candidates=normalized_candidates,
    )
    if local_model_input_digest != expected_digest:
        blockers.append("local_model_input_digest_mismatch")

    chart_map = {chart["chart_id"]: chart for chart in normalized_charts}
    candidate_records: list[dict] = []
    predicted_endpoints: list[tuple[str, dict[str, float]]] = []
    maximum_endpoint_residual = 0.0
    maximum_computed_midpoint_residual = 0.0
    maximum_tangent_norm = 0.0

    for candidate in normalized_candidates:
        cid = candidate["candidate_id"]
        tangent = candidate["tangent_vector"]
        norm_squared = _metric_norm_squared(
            tangent, normalized_metric, coordinates
        )
        if norm_squared <= TOL:
            blockers.append(f"candidate_tangent_zero_or_null_{cid}")
            tangent_norm = 0.0
        else:
            tangent_norm = math.sqrt(norm_squared)
        maximum_tangent_norm = max(maximum_tangent_norm, tangent_norm)
        if tangent_norm >= float(normal_coordinate_ball_radius) - TOL:
            blockers.append(f"candidate_outside_normal_ball_{cid}")

        predicted_endpoint = _second_order_radial_point(
            normalized_base,
            tangent,
            normalized_connection,
            coordinates,
            1.0,
        )
        predicted_midpoint = _second_order_radial_point(
            normalized_base,
            tangent,
            normalized_connection,
            coordinates,
            0.5,
        )
        endpoint_residual = _max_residual(
            predicted_endpoint, candidate["expected_endpoint"], coordinates
        )
        midpoint_residual = _max_residual(
            predicted_midpoint, candidate["expected_midpoint"], coordinates
        )
        maximum_endpoint_residual = max(
            maximum_endpoint_residual, endpoint_residual
        )
        maximum_computed_midpoint_residual = max(
            maximum_computed_midpoint_residual, midpoint_residual
        )
        if endpoint_residual > float(maximum_exponential_map_residual) + TOL:
            blockers.append(f"exponential_map_residual_exceeded_{cid}")
        if midpoint_residual > float(maximum_midpoint_residual) + TOL:
            blockers.append(f"midpoint_residual_exceeded_{cid}")

        chart_id = candidate["assigned_chart_id"]
        chart = chart_map.get(chart_id)
        if chart is None:
            blockers.append(f"assigned_chart_missing_{cid}")
            chart_safe = False
        else:
            chart_safe = True
            for point_name, point in (
                ("endpoint", predicted_endpoint),
                ("midpoint", predicted_midpoint),
            ):
                if any(
                    point[c] < chart["coordinate_lower_bounds"][c] - TOL
                    or point[c] > chart["coordinate_upper_bounds"][c] + TOL
                    for c in coordinates
                ):
                    blockers.append(f"{point_name}_outside_chart_bounds_{cid}")
                    chart_safe = False
                if (
                    _euclidean_distance(point, chart["center"], coordinates)
                    > chart["safe_radius"] + TOL
                ):
                    blockers.append(
                        f"{point_name}_outside_chart_safe_radius_{cid}"
                    )
                    chart_safe = False

        predicted_endpoints.append((cid, predicted_endpoint))
        candidate_records.append(
            {
                **candidate,
                "metric_tangent_norm_squared": norm_squared,
                "metric_tangent_norm": tangent_norm,
                "predicted_endpoint": predicted_endpoint,
                "predicted_midpoint": predicted_midpoint,
                "endpoint_residual": endpoint_residual,
                "midpoint_residual": midpoint_residual,
                "radial_geodesic_unique_from_basepoint_witness": (
                    tangent_norm < float(normal_coordinate_ball_radius)
                    and float(normal_coordinate_ball_radius)
                    < float(source_injectivity_radius_lower_bound)
                ),
                "assigned_chart_safe": chart_safe,
            }
        )

    minimum_computed_endpoint_separation = math.inf
    for left_index, (left_id, left_endpoint) in enumerate(predicted_endpoints):
        for right_id, right_endpoint in predicted_endpoints[left_index + 1 :]:
            separation = _euclidean_distance(
                left_endpoint, right_endpoint, coordinates
            )
            minimum_computed_endpoint_separation = min(
                minimum_computed_endpoint_separation, separation
            )
            if separation < float(minimum_distinct_endpoint_separation) - TOL:
                blockers.append(
                    "finite_sample_exponential_map_not_injective_"
                    f"{left_id}_{right_id}"
                )
    if math.isinf(minimum_computed_endpoint_separation):
        minimum_computed_endpoint_separation = 0.0

    if blockers:
        return ExponentialMapNormalCoordinateBallCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    certificate = {
        "kernel": "PlanOS Exponential Map and Normal Coordinate Ball Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.12",
        "source_injectivity_radius_certificate_digest": (
            source_injectivity_radius_certificate_digest
        ),
        "source_atlas_certificate_digest": source_atlas_certificate_digest,
        "local_model_input_digest": local_model_input_digest,
        "coordinate_schema": coordinates,
        "base_point": normalized_base,
        "metric_matrix": normalized_metric,
        "christoffel_symbols": normalized_connection,
        "chart_records": normalized_charts,
        "radial_geodesic_candidates": candidate_records,
        "source_injectivity_radius_lower_bound": float(
            source_injectivity_radius_lower_bound
        ),
        "normal_coordinate_ball_radius": float(normal_coordinate_ball_radius),
        "maximum_exponential_map_residual": float(
            maximum_exponential_map_residual
        ),
        "maximum_midpoint_residual": float(maximum_midpoint_residual),
        "minimum_distinct_endpoint_separation": float(
            minimum_distinct_endpoint_separation
        ),
        "computed_maximum_endpoint_residual": maximum_endpoint_residual,
        "computed_maximum_midpoint_residual": (
            maximum_computed_midpoint_residual
        ),
        "computed_maximum_tangent_norm": maximum_tangent_norm,
        "computed_minimum_endpoint_separation": (
            minimum_computed_endpoint_separation
        ),
        "finite_second_order_exponential_model_recomputed": True,
        "normal_ball_strictly_inside_injectivity_bound": True,
        "radial_geodesic_unique_from_basepoint": True,
        "finite_sample_exponential_map_injective": True,
        "normal_coordinate_candidates_retained": True,
        "chart_safe_geodesic_ball_covering": True,
        "chart_boundaries_respected": True,
        "atlas_transition_authority_not_extended": True,
        "local_model_only": True,
        "global_exponential_map_not_claimed": True,
        "strong_convexity_not_claimed": True,
        "pairwise_endpoint_geodesic_uniqueness_not_claimed": True,
        "candidate_identity_retained": True,
        "source_injectivity_certificate_not_mutated": True,
        "source_atlas_certificate_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "exponential_map_grants_no_authority": True,
        "normal_ball_grants_no_authority": True,
        "chart_cover_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["exponential_map_certificate_digest"] = canonical_digest(certificate)
    return ExponentialMapNormalCoordinateBallCertificateResult(
        STATUS_READY, [], certificate
    )
