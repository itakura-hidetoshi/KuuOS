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
class SecondOrderMetricJetCurvatureCertificateResult:
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


def _canonical_coordinates(metric: Mapping[str, Any]) -> list[str]:
    return sorted(str(name) for name in metric)


def _normalize_vector(vector: Mapping[str, Any], coordinates: Sequence[str]) -> dict:
    return {coordinate: float(vector[coordinate]) for coordinate in coordinates}


def _normalize_matrix(matrix: Mapping[str, Any], coordinates: Sequence[str]) -> dict:
    return {
        row: {column: float(matrix[row][column]) for column in coordinates}
        for row in coordinates
    }


def _normalize_first_derivatives(
    derivatives: Mapping[str, Any], coordinates: Sequence[str]
) -> dict:
    return {
        derivative: _normalize_matrix(derivatives[derivative], coordinates)
        for derivative in coordinates
    }


def _normalize_second_derivatives(
    derivatives: Mapping[str, Any], coordinates: Sequence[str]
) -> dict:
    return {
        first: {
            second: _normalize_matrix(derivatives[first][second], coordinates)
            for second in coordinates
        }
        for first in coordinates
    }


def _normalize_planes(
    planes: Sequence[Mapping[str, Any]], coordinates: Sequence[str]
) -> list[dict]:
    return sorted(
        (
            {
                "candidate_id": str(plane["candidate_id"]),
                "plane_u": _normalize_vector(plane["plane_u"], coordinates),
                "plane_v": _normalize_vector(plane["plane_v"], coordinates),
                "holonomy_vector": _normalize_vector(
                    plane["holonomy_vector"], coordinates
                ),
                "source_candidate_digest": str(plane["source_candidate_digest"]),
            }
            for plane in planes
        ),
        key=lambda plane: plane["candidate_id"],
    )


def compute_plan_coordinate_schema_digest(metric_matrix: Mapping[str, Any]) -> str:
    return canonical_digest(_canonical_coordinates(metric_matrix))


def compute_metric_jet_digest(
    *,
    metric_matrix: Mapping[str, Any],
    inverse_metric_matrix: Mapping[str, Any],
    metric_first_derivatives: Mapping[str, Any],
) -> str:
    coordinates = _canonical_coordinates(metric_matrix)
    return canonical_digest(
        {
            "metric_matrix": _normalize_matrix(metric_matrix, coordinates),
            "inverse_metric_matrix": _normalize_matrix(
                inverse_metric_matrix, coordinates
            ),
            "metric_first_derivatives": _normalize_first_derivatives(
                metric_first_derivatives, coordinates
            ),
        }
    )


def compute_second_order_metric_jet_digest(
    *,
    source_metric_jet_digest: str,
    metric_second_derivatives: Mapping[str, Any],
    coordinates: Sequence[str],
) -> str:
    return canonical_digest(
        {
            "source_metric_jet_digest": source_metric_jet_digest,
            "metric_second_derivatives": _normalize_second_derivatives(
                metric_second_derivatives, coordinates
            ),
        }
    )


def compute_candidate_plane_bundle_digest(
    candidate_planes: Sequence[Mapping[str, Any]], coordinates: Sequence[str]
) -> str:
    return canonical_digest(_normalize_planes(candidate_planes, coordinates))


def _validate_square_matrix(
    name: str, value: Any, coordinates: Sequence[str]
) -> tuple[list[str], dict]:
    blockers: list[str] = []
    coordinate_set = set(coordinates)
    if not isinstance(value, dict) or set(value) != coordinate_set:
        return [f"{name}_row_schema_invalid"], {}
    normalized: dict[str, dict[str, float]] = {}
    for row in coordinates:
        row_value = value.get(row)
        if not isinstance(row_value, dict) or set(row_value) != coordinate_set:
            blockers.append(f"{name}_column_schema_invalid_{row}")
            continue
        if any(not finite(row_value[column]) for column in coordinates):
            blockers.append(f"{name}_nonfinite_{row}")
            continue
        normalized[row] = {
            column: float(row_value[column]) for column in coordinates
        }
    return blockers, normalized


def _validate_first_derivatives(
    value: Any, coordinates: Sequence[str]
) -> tuple[list[str], dict]:
    if not isinstance(value, dict) or set(value) != set(coordinates):
        return ["metric_first_derivative_schema_invalid"], {}
    blockers: list[str] = []
    normalized: dict[str, dict] = {}
    for derivative in coordinates:
        errors, matrix = _validate_square_matrix(
            f"metric_first_derivative_{derivative}",
            value[derivative],
            coordinates,
        )
        blockers.extend(errors)
        if not errors:
            normalized[derivative] = matrix
    return blockers, normalized


def _validate_second_derivatives(
    value: Any, coordinates: Sequence[str]
) -> tuple[list[str], dict]:
    coordinate_set = set(coordinates)
    if not isinstance(value, dict) or set(value) != coordinate_set:
        return ["metric_second_derivative_first_schema_invalid"], {}
    blockers: list[str] = []
    normalized: dict[str, dict] = {}
    for first in coordinates:
        row = value[first]
        if not isinstance(row, dict) or set(row) != coordinate_set:
            blockers.append(f"metric_second_derivative_second_schema_invalid_{first}")
            continue
        normalized[first] = {}
        for second in coordinates:
            errors, matrix = _validate_square_matrix(
                f"metric_second_derivative_{first}_{second}",
                row[second],
                coordinates,
            )
            blockers.extend(errors)
            if not errors:
                normalized[first][second] = matrix
    return blockers, normalized


def _validate_planes(
    value: Any, coordinates: Sequence[str]
) -> tuple[list[str], list[dict]]:
    if not isinstance(value, list) or not value:
        return ["candidate_plane_field_empty"], []
    blockers: list[str] = []
    coordinate_set = set(coordinates)
    expected_fields = {
        "candidate_id",
        "plane_u",
        "plane_v",
        "holonomy_vector",
        "source_candidate_digest",
    }
    seen_ids: set[str] = set()
    seen_source_digests: set[str] = set()
    normalized: list[dict] = []
    for index, plane in enumerate(value):
        if not isinstance(plane, dict) or set(plane) != expected_fields:
            blockers.append(f"candidate_plane_schema_invalid_{index}")
            continue
        candidate_id = plane["candidate_id"]
        source_digest = plane["source_candidate_digest"]
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            blockers.append(f"candidate_id_invalid_{index}")
            continue
        candidate_id = candidate_id.strip()
        if candidate_id in seen_ids:
            blockers.append("duplicate_candidate_id")
        seen_ids.add(candidate_id)
        if not isinstance(source_digest, str) or not source_digest:
            blockers.append(f"source_candidate_digest_missing_{index}")
        elif source_digest in seen_source_digests:
            blockers.append("duplicate_source_candidate_digest")
        else:
            seen_source_digests.add(source_digest)
        vector_invalid = False
        for field in ("plane_u", "plane_v", "holonomy_vector"):
            vector = plane[field]
            if not isinstance(vector, dict) or set(vector) != coordinate_set:
                blockers.append(f"candidate_{field}_schema_invalid_{index}")
                vector_invalid = True
                continue
            if any(not finite(vector[coordinate]) for coordinate in coordinates):
                blockers.append(f"candidate_{field}_nonfinite_{index}")
                vector_invalid = True
        if vector_invalid:
            continue
        normalized.append(
            {
                "candidate_id": candidate_id,
                "plane_u": _normalize_vector(plane["plane_u"], coordinates),
                "plane_v": _normalize_vector(plane["plane_v"], coordinates),
                "holonomy_vector": _normalize_vector(
                    plane["holonomy_vector"], coordinates
                ),
                "source_candidate_digest": source_digest,
            }
        )
    normalized.sort(key=lambda plane: plane["candidate_id"])
    return blockers, normalized


def _matrix_product(left: dict, right: dict, coordinates: Sequence[str]) -> dict:
    return {
        i: {
            j: sum(left[i][k] * right[k][j] for k in coordinates)
            for j in coordinates
        }
        for i in coordinates
    }


def _is_identity(matrix: dict, coordinates: Sequence[str]) -> bool:
    return all(
        close(matrix[i][j], 1.0 if i == j else 0.0)
        for i in coordinates
        for j in coordinates
    )


def _is_positive_definite(matrix: dict, coordinates: Sequence[str]) -> bool:
    lower: dict[str, dict[str, float]] = {
        i: {j: 0.0 for j in coordinates} for i in coordinates
    }
    for i_index, i in enumerate(coordinates):
        for j_index, j in enumerate(coordinates[: i_index + 1]):
            subtotal = sum(
                lower[i][coordinates[k]] * lower[j][coordinates[k]]
                for k in range(j_index)
            )
            if i == j:
                pivot = matrix[i][i] - subtotal
                if pivot <= TOL:
                    return False
                lower[i][j] = math.sqrt(pivot)
            else:
                divisor = lower[j][j]
                if abs(divisor) <= TOL:
                    return False
                lower[i][j] = (matrix[i][j] - subtotal) / divisor
    return True


def _inner(metric: dict, left: dict, right: dict, coordinates: Sequence[str]) -> float:
    return sum(
        left[i] * metric[i][j] * right[j]
        for i in coordinates
        for j in coordinates
    )


def build_second_order_metric_jet_curvature_certificate(
    *,
    source_levi_civita_certificate_digest: str,
    plan_coordinate_schema_digest: str,
    state_context_digest: str,
    source_metric_jet_digest: str,
    metric_matrix: dict,
    inverse_metric_matrix: dict,
    metric_first_derivatives: dict,
    second_order_metric_jet_digest: str,
    metric_second_derivatives: dict,
    candidate_plane_bundle_digest: str,
    candidate_planes: list[dict],
    maximum_absolute_second_metric_derivative: float,
    maximum_absolute_connection_derivative: float,
    maximum_absolute_riemann: float,
    maximum_absolute_ricci: float,
    maximum_absolute_scalar_curvature: float,
    maximum_absolute_sectional_curvature: float,
    minimum_plane_gram_determinant: float,
    maximum_loop_edge_component: float,
    maximum_absolute_holonomy_increment: float,
) -> SecondOrderMetricJetCurvatureCertificateResult:
    blockers: list[str] = []

    text_inputs = {
        "source_levi_civita_certificate_digest": source_levi_civita_certificate_digest,
        "plan_coordinate_schema_digest": plan_coordinate_schema_digest,
        "state_context_digest": state_context_digest,
        "source_metric_jet_digest": source_metric_jet_digest,
        "second_order_metric_jet_digest": second_order_metric_jet_digest,
        "candidate_plane_bundle_digest": candidate_plane_bundle_digest,
    }
    for name, value in text_inputs.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    numeric_bounds = {
        "maximum_absolute_second_metric_derivative": maximum_absolute_second_metric_derivative,
        "maximum_absolute_connection_derivative": maximum_absolute_connection_derivative,
        "maximum_absolute_riemann": maximum_absolute_riemann,
        "maximum_absolute_ricci": maximum_absolute_ricci,
        "maximum_absolute_scalar_curvature": maximum_absolute_scalar_curvature,
        "maximum_absolute_sectional_curvature": maximum_absolute_sectional_curvature,
        "minimum_plane_gram_determinant": minimum_plane_gram_determinant,
        "maximum_loop_edge_component": maximum_loop_edge_component,
        "maximum_absolute_holonomy_increment": maximum_absolute_holonomy_increment,
    }
    for name, value in numeric_bounds.items():
        if not finite(value) or float(value) <= 0.0:
            blockers.append(f"{name}_invalid")

    if not isinstance(metric_matrix, dict) or not metric_matrix:
        blockers.append("metric_matrix_empty")
        coordinates: list[str] = []
    else:
        coordinates = _canonical_coordinates(metric_matrix)
        if any(not coordinate for coordinate in coordinates):
            blockers.append("metric_coordinate_invalid")
        if len(coordinates) < 2:
            blockers.append("curvature_chart_dimension_too_small")

    metric_errors, metric = _validate_square_matrix(
        "metric_matrix", metric_matrix, coordinates
    )
    blockers.extend(metric_errors)
    inverse_errors, inverse = _validate_square_matrix(
        "inverse_metric_matrix", inverse_metric_matrix, coordinates
    )
    blockers.extend(inverse_errors)
    first_errors, first = _validate_first_derivatives(
        metric_first_derivatives, coordinates
    )
    blockers.extend(first_errors)
    second_errors, second = _validate_second_derivatives(
        metric_second_derivatives, coordinates
    )
    blockers.extend(second_errors)
    plane_errors, planes = _validate_planes(candidate_planes, coordinates)
    blockers.extend(plane_errors)

    if blockers:
        return SecondOrderMetricJetCurvatureCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    if plan_coordinate_schema_digest != canonical_digest(coordinates):
        blockers.append("plan_coordinate_schema_digest_mismatch")
    expected_source_metric_jet_digest = compute_metric_jet_digest(
        metric_matrix=metric,
        inverse_metric_matrix=inverse,
        metric_first_derivatives=first,
    )
    if source_metric_jet_digest != expected_source_metric_jet_digest:
        blockers.append("source_metric_jet_digest_mismatch")
    expected_second_digest = compute_second_order_metric_jet_digest(
        source_metric_jet_digest=source_metric_jet_digest,
        metric_second_derivatives=second,
        coordinates=coordinates,
    )
    if second_order_metric_jet_digest != expected_second_digest:
        blockers.append("second_order_metric_jet_digest_mismatch")
    expected_plane_digest = compute_candidate_plane_bundle_digest(planes, coordinates)
    if candidate_plane_bundle_digest != expected_plane_digest:
        blockers.append("candidate_plane_bundle_digest_mismatch")

    metric_symmetric = all(
        close(metric[i][j], metric[j][i])
        for i in coordinates
        for j in coordinates
    )
    if not metric_symmetric:
        blockers.append("metric_not_symmetric")
    if not _is_positive_definite(metric, coordinates):
        blockers.append("metric_not_positive_definite")
    inverse_left = _matrix_product(inverse, metric, coordinates)
    inverse_right = _matrix_product(metric, inverse, coordinates)
    inverse_exact = _is_identity(inverse_left, coordinates) and _is_identity(
        inverse_right, coordinates
    )
    if not inverse_exact:
        blockers.append("inverse_metric_identity_mismatch")

    first_symmetric = all(
        close(first[a][i][j], first[a][j][i])
        for a in coordinates
        for i in coordinates
        for j in coordinates
    )
    if not first_symmetric:
        blockers.append("metric_first_derivative_not_symmetric")
    second_metric_symmetric = all(
        close(second[a][b][i][j], second[a][b][j][i])
        for a in coordinates
        for b in coordinates
        for i in coordinates
        for j in coordinates
    )
    if not second_metric_symmetric:
        blockers.append("metric_second_derivative_metric_indices_not_symmetric")
    mixed_partial_symmetric = all(
        close(second[a][b][i][j], second[b][a][i][j])
        for a in coordinates
        for b in coordinates
        for i in coordinates
        for j in coordinates
    )
    if not mixed_partial_symmetric:
        blockers.append("metric_second_derivative_mixed_partials_not_symmetric")

    second_values = [
        abs(second[a][b][i][j])
        for a in coordinates
        for b in coordinates
        for i in coordinates
        for j in coordinates
    ]
    computed_max_second = max(second_values, default=0.0)
    if computed_max_second <= TOL:
        blockers.append("second_order_metric_jet_missing")
    if computed_max_second > float(maximum_absolute_second_metric_derivative) + TOL:
        blockers.append("second_metric_derivative_bound_exceeded")

    lower_christoffel = {
        i: {
            j: {
                k: 0.5
                * (first[j][i][k] + first[k][i][j] - first[i][j][k])
                for k in coordinates
            }
            for j in coordinates
        }
        for i in coordinates
    }
    christoffel = {
        upper: {
            j: {
                k: sum(
                    inverse[upper][lower] * lower_christoffel[lower][j][k]
                    for lower in coordinates
                )
                for k in coordinates
            }
            for j in coordinates
        }
        for upper in coordinates
    }

    inverse_derivatives = {
        a: {
            i: {
                l: -sum(
                    inverse[i][p] * first[a][p][q] * inverse[q][l]
                    for p in coordinates
                    for q in coordinates
                )
                for l in coordinates
            }
            for i in coordinates
        }
        for a in coordinates
    }
    inverse_derivative_left_residual = {
        a: {
            i: {
                j: sum(
                    inverse_derivatives[a][i][k] * metric[k][j]
                    + inverse[i][k] * first[a][k][j]
                    for k in coordinates
                )
                for j in coordinates
            }
            for i in coordinates
        }
        for a in coordinates
    }
    inverse_derivative_right_residual = {
        a: {
            i: {
                j: sum(
                    first[a][i][k] * inverse[k][j]
                    + metric[i][k] * inverse_derivatives[a][k][j]
                    for k in coordinates
                )
                for j in coordinates
            }
            for i in coordinates
        }
        for a in coordinates
    }
    max_inverse_derivative_residual = max(
        (
            abs(inverse_derivative_left_residual[a][i][j])
            for a in coordinates
            for i in coordinates
            for j in coordinates
        ),
        default=0.0,
    )
    max_inverse_derivative_residual = max(
        max_inverse_derivative_residual,
        max(
            (
                abs(inverse_derivative_right_residual[a][i][j])
                for a in coordinates
                for i in coordinates
                for j in coordinates
            ),
            default=0.0,
        ),
    )
    if max_inverse_derivative_residual > GEOMETRY_TOL:
        blockers.append("inverse_metric_derivative_identity_mismatch")

    lower_christoffel_derivatives = {
        a: {
            i: {
                j: {
                    k: 0.5
                    * (
                        second[a][j][i][k]
                        + second[a][k][i][j]
                        - second[a][i][j][k]
                    )
                    for k in coordinates
                }
                for j in coordinates
            }
            for i in coordinates
        }
        for a in coordinates
    }
    christoffel_derivatives = {
        a: {
            upper: {
                j: {
                    k: sum(
                        inverse_derivatives[a][upper][lower]
                        * lower_christoffel[lower][j][k]
                        + inverse[upper][lower]
                        * lower_christoffel_derivatives[a][lower][j][k]
                        for lower in coordinates
                    )
                    for k in coordinates
                }
                for j in coordinates
            }
            for upper in coordinates
        }
        for a in coordinates
    }
    connection_derivative_values = [
        abs(christoffel_derivatives[a][upper][j][k])
        for a in coordinates
        for upper in coordinates
        for j in coordinates
        for k in coordinates
    ]
    computed_max_connection_derivative = max(
        connection_derivative_values, default=0.0
    )
    if computed_max_connection_derivative > float(maximum_absolute_connection_derivative) + TOL:
        blockers.append("connection_derivative_bound_exceeded")

    riemann = {
        upper: {
            lower: {
                k: {
                    l: christoffel_derivatives[k][upper][l][lower]
                    - christoffel_derivatives[l][upper][k][lower]
                    + sum(
                        christoffel[upper][k][middle]
                        * christoffel[middle][l][lower]
                        - christoffel[upper][l][middle]
                        * christoffel[middle][k][lower]
                        for middle in coordinates
                    )
                    for l in coordinates
                }
                for k in coordinates
            }
            for lower in coordinates
        }
        for upper in coordinates
    }
    lower_riemann = {
        i: {
            j: {
                k: {
                    l: sum(
                        metric[i][upper] * riemann[upper][j][k][l]
                        for upper in coordinates
                    )
                    for l in coordinates
                }
                for k in coordinates
            }
            for j in coordinates
        }
        for i in coordinates
    }

    last_pair_antisymmetric = all(
        close(
            riemann[upper][j][k][l],
            -riemann[upper][j][l][k],
            GEOMETRY_TOL,
        )
        for upper in coordinates
        for j in coordinates
        for k in coordinates
        for l in coordinates
    )
    if not last_pair_antisymmetric:
        blockers.append("riemann_last_pair_antisymmetry_violation")

    first_bianchi = all(
        close(
            riemann[upper][j][k][l]
            + riemann[upper][k][l][j]
            + riemann[upper][l][j][k],
            0.0,
            GEOMETRY_TOL,
        )
        for upper in coordinates
        for j in coordinates
        for k in coordinates
        for l in coordinates
    )
    if not first_bianchi:
        blockers.append("riemann_first_bianchi_violation")

    lower_pair_symmetries = all(
        close(
            lower_riemann[i][j][k][l],
            -lower_riemann[j][i][k][l],
            GEOMETRY_TOL,
        )
        and close(
            lower_riemann[i][j][k][l],
            -lower_riemann[i][j][l][k],
            GEOMETRY_TOL,
        )
        and close(
            lower_riemann[i][j][k][l],
            lower_riemann[k][l][i][j],
            GEOMETRY_TOL,
        )
        for i in coordinates
        for j in coordinates
        for k in coordinates
        for l in coordinates
    )
    if not lower_pair_symmetries:
        blockers.append("lower_riemann_pair_symmetry_violation")

    riemann_values = [
        abs(riemann[upper][j][k][l])
        for upper in coordinates
        for j in coordinates
        for k in coordinates
        for l in coordinates
    ]
    computed_max_riemann = max(riemann_values, default=0.0)
    if computed_max_riemann <= TOL:
        blockers.append("nontrivial_riemann_curvature_missing")
    if computed_max_riemann > float(maximum_absolute_riemann) + TOL:
        blockers.append("riemann_bound_exceeded")

    ricci = {
        j: {
            l: sum(riemann[upper][j][upper][l] for upper in coordinates)
            for l in coordinates
        }
        for j in coordinates
    }
    ricci_symmetric = all(
        close(ricci[i][j], ricci[j][i], GEOMETRY_TOL)
        for i in coordinates
        for j in coordinates
    )
    if not ricci_symmetric:
        blockers.append("ricci_symmetry_violation")
    ricci_values = [abs(ricci[i][j]) for i in coordinates for j in coordinates]
    computed_max_ricci = max(ricci_values, default=0.0)
    if computed_max_ricci > float(maximum_absolute_ricci) + TOL:
        blockers.append("ricci_bound_exceeded")

    scalar_curvature = sum(
        inverse[i][j] * ricci[i][j] for i in coordinates for j in coordinates
    )
    if abs(scalar_curvature) > float(maximum_absolute_scalar_curvature) + TOL:
        blockers.append("scalar_curvature_bound_exceeded")

    plane_records: list[dict] = []
    maximum_observed_sectional = 0.0
    maximum_observed_holonomy = 0.0
    for plane in planes:
        candidate_id = plane["candidate_id"]
        u = plane["plane_u"]
        v = plane["plane_v"]
        w = plane["holonomy_vector"]
        maximum_edge = max(
            max(abs(value) for value in u.values()),
            max(abs(value) for value in v.values()),
        )
        if maximum_edge > float(maximum_loop_edge_component) + TOL:
            blockers.append(f"loop_edge_bound_exceeded_{candidate_id}")
            continue
        uu = _inner(metric, u, u, coordinates)
        vv = _inner(metric, v, v, coordinates)
        uv = _inner(metric, u, v, coordinates)
        gram_determinant = uu * vv - uv * uv
        if gram_determinant < float(minimum_plane_gram_determinant) - TOL:
            blockers.append(f"plane_gram_determinant_too_small_{candidate_id}")
            continue
        sectional_numerator = sum(
            lower_riemann[i][j][k][l] * u[i] * v[j] * v[k] * u[l]
            for i in coordinates
            for j in coordinates
            for k in coordinates
            for l in coordinates
        )
        sectional_curvature = sectional_numerator / gram_determinant
        maximum_observed_sectional = max(
            maximum_observed_sectional, abs(sectional_curvature)
        )
        if abs(sectional_curvature) > float(maximum_absolute_sectional_curvature) + TOL:
            blockers.append(f"sectional_curvature_bound_exceeded_{candidate_id}")
        holonomy_increment = {
            upper: sum(
                riemann[upper][j][k][l] * w[j] * u[k] * v[l]
                for j in coordinates
                for k in coordinates
                for l in coordinates
            )
            for upper in coordinates
        }
        candidate_max_holonomy = max(
            abs(value) for value in holonomy_increment.values()
        )
        maximum_observed_holonomy = max(
            maximum_observed_holonomy, candidate_max_holonomy
        )
        if candidate_max_holonomy > float(maximum_absolute_holonomy_increment) + TOL:
            blockers.append(f"holonomy_increment_bound_exceeded_{candidate_id}")
        plane_records.append(
            {
                "candidate_id": candidate_id,
                "source_candidate_digest": plane["source_candidate_digest"],
                "plane_u": u,
                "plane_v": v,
                "holonomy_vector": w,
                "plane_gram_determinant": gram_determinant,
                "sectional_curvature_numerator": sectional_numerator,
                "sectional_curvature": sectional_curvature,
                "infinitesimal_holonomy_increment": holonomy_increment,
            }
        )

    if blockers:
        return SecondOrderMetricJetCurvatureCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    certificate = {
        "kernel": "PlanOS Second-Order Metric Jet Curvature Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.07",
        "source_levi_civita_certificate_digest": source_levi_civita_certificate_digest,
        "plan_coordinate_schema_digest": plan_coordinate_schema_digest,
        "state_context_digest": state_context_digest,
        "source_metric_jet_digest": source_metric_jet_digest,
        "second_order_metric_jet_digest": second_order_metric_jet_digest,
        "metric_matrix": metric,
        "inverse_metric_matrix": inverse,
        "metric_first_derivatives": first,
        "metric_second_derivatives": second,
        "candidate_plane_bundle_digest": candidate_plane_bundle_digest,
        "candidate_planes": planes,
        "maximum_absolute_second_metric_derivative": float(
            maximum_absolute_second_metric_derivative
        ),
        "maximum_absolute_connection_derivative": float(
            maximum_absolute_connection_derivative
        ),
        "maximum_absolute_riemann": float(maximum_absolute_riemann),
        "maximum_absolute_ricci": float(maximum_absolute_ricci),
        "maximum_absolute_scalar_curvature": float(maximum_absolute_scalar_curvature),
        "maximum_absolute_sectional_curvature": float(
            maximum_absolute_sectional_curvature
        ),
        "minimum_plane_gram_determinant": float(minimum_plane_gram_determinant),
        "maximum_loop_edge_component": float(maximum_loop_edge_component),
        "maximum_absolute_holonomy_increment": float(
            maximum_absolute_holonomy_increment
        ),
        "computed_maximum_absolute_second_metric_derivative": computed_max_second,
        "computed_maximum_absolute_connection_derivative": (
            computed_max_connection_derivative
        ),
        "computed_maximum_absolute_riemann": computed_max_riemann,
        "computed_maximum_absolute_ricci": computed_max_ricci,
        "computed_scalar_curvature": scalar_curvature,
        "maximum_inverse_metric_derivative_residual": max_inverse_derivative_residual,
        "maximum_observed_absolute_sectional_curvature": maximum_observed_sectional,
        "maximum_observed_absolute_holonomy_increment": maximum_observed_holonomy,
        "inverse_metric_derivatives": inverse_derivatives,
        "lower_christoffel_symbols": lower_christoffel,
        "christoffel_symbols": christoffel,
        "lower_christoffel_derivatives": lower_christoffel_derivatives,
        "christoffel_derivatives": christoffel_derivatives,
        "riemann_curvature": riemann,
        "lower_riemann_curvature": lower_riemann,
        "ricci_curvature": ricci,
        "plane_curvature_records": plane_records,
        "second_order_metric_jet_present": True,
        "metric_symmetric": metric_symmetric,
        "metric_positive_definite": True,
        "inverse_metric_exact": inverse_exact,
        "metric_first_derivative_symmetric": first_symmetric,
        "metric_second_derivative_metric_indices_symmetric": second_metric_symmetric,
        "mixed_partial_derivatives_symmetric": mixed_partial_symmetric,
        "inverse_metric_derivative_identity_preserved": True,
        "connection_derivative_recomputed": True,
        "riemann_curvature_recomputed": True,
        "riemann_last_pair_antisymmetric": last_pair_antisymmetric,
        "riemann_first_bianchi": first_bianchi,
        "lower_riemann_pair_symmetries": lower_pair_symmetries,
        "ricci_curvature_recomputed": True,
        "ricci_symmetric": ricci_symmetric,
        "scalar_curvature_recomputed": True,
        "sectional_curvature_retained": True,
        "infinitesimal_holonomy_retained": True,
        "curvature_bounded": True,
        "holonomy_bounded": True,
        "source_levi_civita_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "candidate_plane_field_retained": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "world_projection_grants_no_authority": True,
        "connection_grants_no_authority": True,
        "curvature_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["curvature_certificate_digest"] = canonical_digest(certificate)
    return SecondOrderMetricJetCurvatureCertificateResult(
        STATUS_READY, [], certificate
    )
