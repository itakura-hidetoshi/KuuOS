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
class StateDependentMetricJetLeviCivitaCertificateResult:
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


def _normalize_derivatives(
    derivatives: Mapping[str, Any], coordinates: Sequence[str]
) -> dict:
    return {
        derivative: _normalize_matrix(derivatives[derivative], coordinates)
        for derivative in coordinates
    }


def _normalize_candidates(
    candidates: Sequence[Mapping[str, Any]], coordinates: Sequence[str]
) -> list[dict]:
    return sorted(
        (
            {
                "candidate_id": str(candidate["candidate_id"]),
                "tangent_vector": _normalize_vector(
                    candidate["tangent_vector"], coordinates
                ),
                "transport_displacement": _normalize_vector(
                    candidate["transport_displacement"], coordinates
                ),
                "source_candidate_digest": str(
                    candidate["source_candidate_digest"]
                ),
            }
            for candidate in candidates
        ),
        key=lambda candidate: candidate["candidate_id"],
    )


def compute_plan_coordinate_schema_digest(
    metric_matrix: Mapping[str, Any],
) -> str:
    return canonical_digest(_canonical_coordinates(metric_matrix))


def compute_state_context_digest(
    *,
    plan_state_point: Mapping[str, Any],
    qi_state_digest: str,
    history_state_digest: str,
    world_state_digest: str,
) -> str:
    coordinates = sorted(plan_state_point)
    return canonical_digest(
        {
            "plan_state_point": {
                coordinate: float(plan_state_point[coordinate])
                for coordinate in coordinates
            },
            "qi_state_digest": qi_state_digest,
            "history_state_digest": history_state_digest,
            "world_state_digest": world_state_digest,
        }
    )


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
            "metric_first_derivatives": _normalize_derivatives(
                metric_first_derivatives, coordinates
            ),
        }
    )


def compute_candidate_tangent_bundle_digest(
    candidate_tangents: Sequence[Mapping[str, Any]], coordinates: Sequence[str]
) -> str:
    return canonical_digest(_normalize_candidates(candidate_tangents, coordinates))


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


def _validate_plan_state_point(
    value: Any, coordinates: Sequence[str]
) -> tuple[list[str], dict]:
    coordinate_set = set(coordinates)
    if not isinstance(value, dict) or set(value) != coordinate_set:
        return ["plan_state_point_schema_invalid"], {}
    if any(not finite(value[coordinate]) for coordinate in coordinates):
        return ["plan_state_point_nonfinite"], {}
    return [], _normalize_vector(value, coordinates)


def _validate_derivatives(
    value: Any, coordinates: Sequence[str]
) -> tuple[list[str], dict]:
    blockers: list[str] = []
    coordinate_set = set(coordinates)
    if not isinstance(value, dict) or set(value) != coordinate_set:
        return ["metric_first_derivative_schema_invalid"], {}
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


def _validate_candidates(
    value: Any, coordinates: Sequence[str]
) -> tuple[list[str], list[dict]]:
    blockers: list[str] = []
    if not isinstance(value, list) or not value:
        return ["candidate_tangent_field_empty"], []
    coordinate_set = set(coordinates)
    seen_ids: set[str] = set()
    seen_source_digests: set[str] = set()
    normalized: list[dict] = []
    expected_fields = {
        "candidate_id",
        "tangent_vector",
        "transport_displacement",
        "source_candidate_digest",
    }
    for index, candidate in enumerate(value):
        if not isinstance(candidate, dict) or set(candidate) != expected_fields:
            blockers.append(f"candidate_tangent_schema_invalid_{index}")
            continue
        candidate_id = candidate["candidate_id"]
        source_digest = candidate["source_candidate_digest"]
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
        tangent = candidate["tangent_vector"]
        displacement = candidate["transport_displacement"]
        index_invalid = False
        for field_name, vector in (
            ("tangent_vector", tangent),
            ("transport_displacement", displacement),
        ):
            if not isinstance(vector, dict) or set(vector) != coordinate_set:
                blockers.append(f"candidate_{field_name}_schema_invalid_{index}")
                index_invalid = True
                continue
            if any(not finite(vector[coordinate]) for coordinate in coordinates):
                blockers.append(f"candidate_{field_name}_nonfinite_{index}")
                index_invalid = True
        if index_invalid:
            continue
        normalized.append(
            {
                "candidate_id": candidate_id,
                "tangent_vector": _normalize_vector(tangent, coordinates),
                "transport_displacement": _normalize_vector(
                    displacement, coordinates
                ),
                "source_candidate_digest": source_digest,
            }
        )
    normalized.sort(key=lambda candidate: candidate["candidate_id"])
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


def _quadratic_form(matrix: dict, vector: dict, coordinates: Sequence[str]) -> float:
    return sum(
        vector[i] * matrix[i][j] * vector[j]
        for i in coordinates
        for j in coordinates
    )


def _predicted_metric(
    metric: dict,
    derivatives: dict,
    displacement: dict,
    coordinates: Sequence[str],
) -> dict:
    return {
        i: {
            j: metric[i][j]
            + sum(
                derivatives[k][i][j] * displacement[k]
                for k in coordinates
            )
            for j in coordinates
        }
        for i in coordinates
    }


def build_state_dependent_metric_jet_levi_civita_certificate(
    *,
    source_native_coupled_metric_certificate_digest: str,
    plan_coordinate_schema_digest: str,
    qi_state_digest: str,
    history_state_digest: str,
    world_state_digest: str,
    state_context_digest: str,
    plan_state_point: dict,
    metric_jet_digest: str,
    metric_matrix: dict,
    inverse_metric_matrix: dict,
    metric_first_derivatives: dict,
    candidate_tangent_bundle_digest: str,
    candidate_tangents: list[dict],
    maximum_absolute_metric_derivative: float,
    maximum_absolute_christoffel: float,
    maximum_transport_displacement: float,
    maximum_first_order_norm_defect: float,
) -> StateDependentMetricJetLeviCivitaCertificateResult:
    blockers: list[str] = []

    text_inputs = {
        "source_native_coupled_metric_certificate_digest": (
            source_native_coupled_metric_certificate_digest
        ),
        "plan_coordinate_schema_digest": plan_coordinate_schema_digest,
        "qi_state_digest": qi_state_digest,
        "history_state_digest": history_state_digest,
        "world_state_digest": world_state_digest,
        "state_context_digest": state_context_digest,
        "metric_jet_digest": metric_jet_digest,
        "candidate_tangent_bundle_digest": candidate_tangent_bundle_digest,
    }
    for name, value in text_inputs.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    numeric_bounds = {
        "maximum_absolute_metric_derivative": maximum_absolute_metric_derivative,
        "maximum_absolute_christoffel": maximum_absolute_christoffel,
        "maximum_transport_displacement": maximum_transport_displacement,
        "maximum_first_order_norm_defect": maximum_first_order_norm_defect,
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
        if len(coordinates) != len(set(coordinates)):
            blockers.append("duplicate_metric_coordinate")

    metric_errors, metric = _validate_square_matrix(
        "metric_matrix", metric_matrix, coordinates
    )
    blockers.extend(metric_errors)
    inverse_errors, inverse = _validate_square_matrix(
        "inverse_metric_matrix", inverse_metric_matrix, coordinates
    )
    blockers.extend(inverse_errors)
    derivative_errors, derivatives = _validate_derivatives(
        metric_first_derivatives, coordinates
    )
    blockers.extend(derivative_errors)
    point_errors, normalized_point = _validate_plan_state_point(
        plan_state_point, coordinates
    )
    blockers.extend(point_errors)
    candidate_errors, candidates = _validate_candidates(
        candidate_tangents, coordinates
    )
    blockers.extend(candidate_errors)

    if blockers:
        return StateDependentMetricJetLeviCivitaCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    if plan_coordinate_schema_digest != canonical_digest(coordinates):
        blockers.append("plan_coordinate_schema_digest_mismatch")
    expected_state_context_digest = compute_state_context_digest(
        plan_state_point=normalized_point,
        qi_state_digest=qi_state_digest,
        history_state_digest=history_state_digest,
        world_state_digest=world_state_digest,
    )
    if state_context_digest != expected_state_context_digest:
        blockers.append("state_context_digest_mismatch")
    expected_metric_jet_digest = compute_metric_jet_digest(
        metric_matrix=metric,
        inverse_metric_matrix=inverse,
        metric_first_derivatives=derivatives,
    )
    if metric_jet_digest != expected_metric_jet_digest:
        blockers.append("metric_jet_digest_mismatch")
    expected_candidate_digest = compute_candidate_tangent_bundle_digest(
        candidates, coordinates
    )
    if candidate_tangent_bundle_digest != expected_candidate_digest:
        blockers.append("candidate_tangent_bundle_digest_mismatch")

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

    derivative_symmetric = all(
        close(derivatives[k][i][j], derivatives[k][j][i])
        for k in coordinates
        for i in coordinates
        for j in coordinates
    )
    if not derivative_symmetric:
        blockers.append("metric_derivative_not_symmetric")

    derivative_values = [
        abs(derivatives[k][i][j])
        for k in coordinates
        for i in coordinates
        for j in coordinates
    ]
    computed_max_derivative = max(derivative_values, default=0.0)
    if computed_max_derivative <= TOL:
        blockers.append("state_dependent_metric_jet_missing")
    if computed_max_derivative > float(maximum_absolute_metric_derivative) + TOL:
        blockers.append("metric_derivative_bound_exceeded")

    lower_christoffel = {
        i: {
            j: {
                k: 0.5
                * (
                    derivatives[j][i][k]
                    + derivatives[k][i][j]
                    - derivatives[i][j][k]
                )
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

    torsion_free = all(
        close(christoffel[upper][j][k], christoffel[upper][k][j])
        for upper in coordinates
        for j in coordinates
        for k in coordinates
    )
    if not torsion_free:
        blockers.append("christoffel_torsion_detected")

    metric_compatibility_residual = {
        k: {
            i: {
                j: derivatives[k][i][j]
                - sum(
                    christoffel[lower][k][i] * metric[lower][j]
                    for lower in coordinates
                )
                - sum(
                    christoffel[lower][k][j] * metric[i][lower]
                    for lower in coordinates
                )
                for j in coordinates
            }
            for i in coordinates
        }
        for k in coordinates
    }
    maximum_metric_compatibility_residual = max(
        (
            abs(metric_compatibility_residual[k][i][j])
            for k in coordinates
            for i in coordinates
            for j in coordinates
        ),
        default=0.0,
    )
    metric_compatible = maximum_metric_compatibility_residual <= 1e-7
    if not metric_compatible:
        blockers.append("metric_compatibility_residual_exceeded")

    christoffel_values = [
        abs(christoffel[upper][j][k])
        for upper in coordinates
        for j in coordinates
        for k in coordinates
    ]
    computed_max_christoffel = max(christoffel_values, default=0.0)
    if computed_max_christoffel <= TOL:
        blockers.append("nontrivial_levi_civita_connection_missing")
    if computed_max_christoffel > float(maximum_absolute_christoffel) + TOL:
        blockers.append("christoffel_bound_exceeded")

    candidate_transport_records: list[dict] = []
    maximum_observed_norm_defect = 0.0
    for candidate in candidates:
        candidate_id = candidate["candidate_id"]
        tangent = candidate["tangent_vector"]
        displacement = candidate["transport_displacement"]
        displacement_max = max(abs(value) for value in displacement.values())
        if displacement_max > float(maximum_transport_displacement) + TOL:
            blockers.append(f"transport_displacement_bound_exceeded_{candidate_id}")
            continue
        transported = {
            upper: tangent[upper]
            - sum(
                christoffel[upper][j][k] * displacement[j] * tangent[k]
                for j in coordinates
                for k in coordinates
            )
            for upper in coordinates
        }
        acceleration = {
            upper: -sum(
                christoffel[upper][j][k] * tangent[j] * tangent[k]
                for j in coordinates
                for k in coordinates
            )
            for upper in coordinates
        }
        predicted = _predicted_metric(
            metric, derivatives, displacement, coordinates
        )
        if not all(
            close(predicted[i][j], predicted[j][i])
            for i in coordinates
            for j in coordinates
        ):
            blockers.append(f"predicted_metric_symmetry_violation_{candidate_id}")
        base_norm_squared = _quadratic_form(metric, tangent, coordinates)
        transported_norm_squared = _quadratic_form(
            predicted, transported, coordinates
        )
        norm_defect = abs(transported_norm_squared - base_norm_squared)
        maximum_observed_norm_defect = max(
            maximum_observed_norm_defect, norm_defect
        )
        if norm_defect > float(maximum_first_order_norm_defect) + 1e-15:
            blockers.append(f"parallel_transport_norm_defect_exceeded_{candidate_id}")
        candidate_transport_records.append(
            {
                "candidate_id": candidate_id,
                "source_candidate_digest": candidate["source_candidate_digest"],
                "tangent_vector": tangent,
                "transport_displacement": displacement,
                "transported_tangent_vector": transported,
                "geodesic_acceleration": acceleration,
                "predicted_metric_at_displaced_state": predicted,
                "base_metric_norm_squared": base_norm_squared,
                "transported_metric_norm_squared": transported_norm_squared,
                "first_order_norm_defect": norm_defect,
            }
        )

    if blockers:
        return StateDependentMetricJetLeviCivitaCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    certificate = {
        "kernel": (
            "PlanOS State-Dependent Metric Jet and Levi-Civita Certificate Kernel"
        ),
        "kernel_version": "v0.1",
        "planos_version": "v1.06",
        "source_native_coupled_metric_certificate_digest": (
            source_native_coupled_metric_certificate_digest
        ),
        "plan_coordinate_schema_digest": plan_coordinate_schema_digest,
        "qi_state_digest": qi_state_digest,
        "history_state_digest": history_state_digest,
        "world_state_digest": world_state_digest,
        "state_context_digest": state_context_digest,
        "plan_state_point": normalized_point,
        "metric_jet_digest": metric_jet_digest,
        "metric_matrix": metric,
        "inverse_metric_matrix": inverse,
        "metric_first_derivatives": derivatives,
        "candidate_tangent_bundle_digest": candidate_tangent_bundle_digest,
        "candidate_tangents": candidates,
        "maximum_absolute_metric_derivative": float(
            maximum_absolute_metric_derivative
        ),
        "maximum_absolute_christoffel": float(maximum_absolute_christoffel),
        "maximum_transport_displacement": float(
            maximum_transport_displacement
        ),
        "maximum_first_order_norm_defect": float(
            maximum_first_order_norm_defect
        ),
        "computed_maximum_absolute_metric_derivative": computed_max_derivative,
        "computed_maximum_absolute_christoffel": computed_max_christoffel,
        "maximum_metric_compatibility_residual": (
            maximum_metric_compatibility_residual
        ),
        "maximum_observed_first_order_norm_defect": (
            maximum_observed_norm_defect
        ),
        "lower_christoffel_symbols": lower_christoffel,
        "christoffel_symbols": christoffel,
        "metric_compatibility_residual": metric_compatibility_residual,
        "candidate_transport_records": candidate_transport_records,
        "state_dependent_metric_jet_present": True,
        "metric_symmetric": metric_symmetric,
        "metric_positive_definite": True,
        "inverse_metric_exact": inverse_exact,
        "metric_derivative_symmetric": derivative_symmetric,
        "levi_civita_connection_recomputed": True,
        "torsion_free": torsion_free,
        "metric_compatible": metric_compatible,
        "connection_bounded": True,
        "parallel_transport_bounded": True,
        "first_order_metric_norm_preserved": True,
        "geodesic_acceleration_retained": True,
        "source_metric_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "candidate_tangent_field_retained": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "world_projection_grants_no_authority": True,
        "connection_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["levi_civita_certificate_digest"] = canonical_digest(certificate)
    return StateDependentMetricJetLeviCivitaCertificateResult(
        STATUS_READY, [], certificate
    )
