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
GEOMETRY_TOL = 1e-7


@dataclass
class MultiChartAtlasCurvatureCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    return sha256(payload).hexdigest()


def finite(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def close(left: float, right: float, tolerance: float = TOL) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance)


def _normalize_vector(vector: Mapping[str, Any], coordinates: Sequence[str]) -> dict:
    return {coordinate: float(vector[coordinate]) for coordinate in coordinates}


def _normalize_matrix(
    matrix: Mapping[str, Any], row_coordinates: Sequence[str], column_coordinates: Sequence[str]
) -> dict:
    return {
        row: {column: float(matrix[row][column]) for column in column_coordinates}
        for row in row_coordinates
    }


def _normalize_tensor3(
    tensor: Mapping[str, Any],
    first_coordinates: Sequence[str],
    second_coordinates: Sequence[str],
    third_coordinates: Sequence[str],
) -> dict:
    return {
        first: {
            second: {
                third: float(tensor[first][second][third])
                for third in third_coordinates
            }
            for second in second_coordinates
        }
        for first in first_coordinates
    }


def _normalize_tensor4(
    tensor: Mapping[str, Any],
    first_coordinates: Sequence[str],
    second_coordinates: Sequence[str],
    third_coordinates: Sequence[str],
    fourth_coordinates: Sequence[str],
) -> dict:
    return {
        first: {
            second: {
                third: {
                    fourth: float(tensor[first][second][third][fourth])
                    for fourth in fourth_coordinates
                }
                for third in third_coordinates
            }
            for second in second_coordinates
        }
        for first in first_coordinates
    }


def _normalize_candidate_records(
    records: Sequence[Mapping[str, Any]], coordinates: Sequence[str]
) -> list[dict]:
    return sorted(
        (
            {
                "candidate_id": str(record["candidate_id"]),
                "plane_u": _normalize_vector(record["plane_u"], coordinates),
                "plane_v": _normalize_vector(record["plane_v"], coordinates),
                "holonomy_vector": _normalize_vector(
                    record["holonomy_vector"], coordinates
                ),
                "sectional_curvature": float(record["sectional_curvature"]),
                "holonomy_increment": _normalize_vector(
                    record["holonomy_increment"], coordinates
                ),
                "source_candidate_digest": str(record["source_candidate_digest"]),
            }
            for record in records
        ),
        key=lambda record: record["candidate_id"],
    )


def _normalize_chart(chart: Mapping[str, Any]) -> dict:
    coordinates = [str(value) for value in chart["coordinates"]]
    return {
        "chart_id": str(chart["chart_id"]),
        "coordinates": coordinates,
        "source_curvature_certificate_digest": str(
            chart["source_curvature_certificate_digest"]
        ),
        "metric_matrix": _normalize_matrix(
            chart["metric_matrix"], coordinates, coordinates
        ),
        "inverse_metric_matrix": _normalize_matrix(
            chart["inverse_metric_matrix"], coordinates, coordinates
        ),
        "christoffel_symbols": _normalize_tensor3(
            chart["christoffel_symbols"], coordinates, coordinates, coordinates
        ),
        "riemann_tensor": _normalize_tensor4(
            chart["riemann_tensor"],
            coordinates,
            coordinates,
            coordinates,
            coordinates,
        ),
        "ricci_tensor": _normalize_matrix(
            chart["ricci_tensor"], coordinates, coordinates
        ),
        "scalar_curvature": float(chart["scalar_curvature"]),
        "candidate_records": _normalize_candidate_records(
            chart["candidate_records"], coordinates
        ),
        "boundary_margin": float(chart["boundary_margin"]),
        "regularity_radius": float(chart["regularity_radius"]),
    }


def _normalize_transition(
    transition: Mapping[str, Any], chart_by_id: Mapping[str, Mapping[str, Any]]
) -> dict:
    source_id = str(transition["source_chart_id"])
    target_id = str(transition["target_chart_id"])
    source_coordinates = chart_by_id[source_id]["coordinates"]
    target_coordinates = chart_by_id[target_id]["coordinates"]
    return {
        "source_chart_id": source_id,
        "target_chart_id": target_id,
        "jacobian": _normalize_matrix(
            transition["jacobian"], target_coordinates, source_coordinates
        ),
        "inverse_jacobian": _normalize_matrix(
            transition["inverse_jacobian"], source_coordinates, target_coordinates
        ),
        "inverse_hessian": _normalize_tensor3(
            transition["inverse_hessian"],
            source_coordinates,
            target_coordinates,
            target_coordinates,
        ),
        "overlap_margin": float(transition["overlap_margin"]),
        "source_transition_digest": str(transition["source_transition_digest"]),
    }


def compute_chart_bundle_digest(charts: Sequence[Mapping[str, Any]]) -> str:
    normalized = sorted((_normalize_chart(chart) for chart in charts), key=lambda c: c["chart_id"])
    return canonical_digest(normalized)


def compute_transition_bundle_digest(
    charts: Sequence[Mapping[str, Any]], transitions: Sequence[Mapping[str, Any]]
) -> str:
    normalized_charts = [_normalize_chart(chart) for chart in charts]
    chart_by_id = {chart["chart_id"]: chart for chart in normalized_charts}
    normalized = sorted(
        (_normalize_transition(transition, chart_by_id) for transition in transitions),
        key=lambda transition: (
            transition["source_chart_id"],
            transition["target_chart_id"],
        ),
    )
    return canonical_digest(normalized)


def compute_atlas_digest(
    *,
    source_curvature_bundle_digest: str,
    chart_bundle_digest: str,
    transition_bundle_digest: str,
) -> str:
    return canonical_digest(
        {
            "source_curvature_bundle_digest": source_curvature_bundle_digest,
            "chart_bundle_digest": chart_bundle_digest,
            "transition_bundle_digest": transition_bundle_digest,
        }
    )


def _validate_named_vector(name: str, value: Any, coordinates: Sequence[str]) -> tuple[list[str], dict]:
    if not isinstance(value, dict) or set(value) != set(coordinates):
        return [f"{name}_schema_invalid"], {}
    if any(not finite(value[coordinate]) for coordinate in coordinates):
        return [f"{name}_nonfinite"], {}
    return [], _normalize_vector(value, coordinates)


def _validate_matrix(
    name: str, value: Any, rows: Sequence[str], columns: Sequence[str]
) -> tuple[list[str], dict]:
    blockers: list[str] = []
    if not isinstance(value, dict) or set(value) != set(rows):
        return [f"{name}_row_schema_invalid"], {}
    normalized: dict[str, dict[str, float]] = {}
    for row in rows:
        row_value = value.get(row)
        if not isinstance(row_value, dict) or set(row_value) != set(columns):
            blockers.append(f"{name}_column_schema_invalid_{row}")
            continue
        if any(not finite(row_value[column]) for column in columns):
            blockers.append(f"{name}_nonfinite_{row}")
            continue
        normalized[row] = {column: float(row_value[column]) for column in columns}
    return blockers, normalized


def _validate_tensor3(
    name: str,
    value: Any,
    first: Sequence[str],
    second: Sequence[str],
    third: Sequence[str],
) -> tuple[list[str], dict]:
    if not isinstance(value, dict) or set(value) != set(first):
        return [f"{name}_first_schema_invalid"], {}
    blockers: list[str] = []
    normalized: dict = {}
    for a in first:
        if not isinstance(value[a], dict) or set(value[a]) != set(second):
            blockers.append(f"{name}_second_schema_invalid_{a}")
            continue
        normalized[a] = {}
        for b in second:
            if not isinstance(value[a][b], dict) or set(value[a][b]) != set(third):
                blockers.append(f"{name}_third_schema_invalid_{a}_{b}")
                continue
            if any(not finite(value[a][b][c]) for c in third):
                blockers.append(f"{name}_nonfinite_{a}_{b}")
                continue
            normalized[a][b] = {c: float(value[a][b][c]) for c in third}
    return blockers, normalized


def _validate_tensor4(
    name: str,
    value: Any,
    first: Sequence[str],
    second: Sequence[str],
    third: Sequence[str],
    fourth: Sequence[str],
) -> tuple[list[str], dict]:
    if not isinstance(value, dict) or set(value) != set(first):
        return [f"{name}_first_schema_invalid"], {}
    blockers: list[str] = []
    normalized: dict = {}
    for a in first:
        if not isinstance(value[a], dict) or set(value[a]) != set(second):
            blockers.append(f"{name}_second_schema_invalid_{a}")
            continue
        normalized[a] = {}
        for b in second:
            if not isinstance(value[a][b], dict) or set(value[a][b]) != set(third):
                blockers.append(f"{name}_third_schema_invalid_{a}_{b}")
                continue
            normalized[a][b] = {}
            for c in third:
                if not isinstance(value[a][b][c], dict) or set(value[a][b][c]) != set(fourth):
                    blockers.append(f"{name}_fourth_schema_invalid_{a}_{b}_{c}")
                    continue
                if any(not finite(value[a][b][c][d]) for d in fourth):
                    blockers.append(f"{name}_nonfinite_{a}_{b}_{c}")
                    continue
                normalized[a][b][c] = {
                    d: float(value[a][b][c][d]) for d in fourth
                }
    return blockers, normalized


def _matrix_product(
    left: Mapping[str, Mapping[str, float]],
    right: Mapping[str, Mapping[str, float]],
    rows: Sequence[str],
    middle: Sequence[str],
    columns: Sequence[str],
) -> dict:
    return {
        row: {
            column: sum(left[row][k] * right[k][column] for k in middle)
            for column in columns
        }
        for row in rows
    }


def _is_identity(matrix: Mapping[str, Mapping[str, float]], coordinates: Sequence[str]) -> bool:
    return all(
        close(matrix[i][j], 1.0 if i == j else 0.0)
        for i in coordinates
        for j in coordinates
    )


def _determinant(
    matrix: Mapping[str, Mapping[str, float]],
    row_coordinates: Sequence[str],
    column_coordinates: Sequence[str],
) -> float:
    work = [
        [float(matrix[row][column]) for column in column_coordinates]
        for row in row_coordinates
    ]
    determinant = 1.0
    for pivot_index in range(len(row_coordinates)):
        pivot_row = max(
            range(pivot_index, len(row_coordinates)),
            key=lambda row: abs(work[row][pivot_index]),
        )
        pivot = work[pivot_row][pivot_index]
        if abs(pivot) <= TOL:
            return 0.0
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
            determinant *= -1.0
        pivot = work[pivot_index][pivot_index]
        determinant *= pivot
        for row in range(pivot_index + 1, len(row_coordinates)):
            factor = work[row][pivot_index] / pivot
            for column in range(pivot_index + 1, len(column_coordinates)):
                work[row][column] -= factor * work[pivot_index][column]
    return determinant


def _is_positive_definite(matrix: Mapping[str, Mapping[str, float]], coordinates: Sequence[str]) -> bool:
    lower = [[0.0 for _ in coordinates] for _ in coordinates]
    for i in range(len(coordinates)):
        for j in range(i + 1):
            subtotal = sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                pivot = matrix[coordinates[i]][coordinates[i]] - subtotal
                if pivot <= TOL:
                    return False
                lower[i][j] = math.sqrt(pivot)
            else:
                divisor = lower[j][j]
                if abs(divisor) <= TOL:
                    return False
                lower[i][j] = (
                    matrix[coordinates[i]][coordinates[j]] - subtotal
                ) / divisor
    return True


