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
class SecondVariationMorseIndexCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
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


def _coordinates(metric: Mapping[str, Any]) -> list[str]:
    return sorted(str(key) for key in metric)


def _validate_matrix(
    name: str,
    value: Any,
    coordinates: Sequence[str],
) -> tuple[list[str], dict[str, dict[str, float]]]:
    if not isinstance(value, dict) or set(value) != set(coordinates):
        return [f"{name}_row_schema_invalid"], {}
    normalized: dict[str, dict[str, float]] = {}
    blockers: list[str] = []
    for row_name in coordinates:
        row = value.get(row_name)
        if not isinstance(row, dict) or set(row) != set(coordinates):
            blockers.append(f"{name}_column_schema_invalid_{row_name}")
            continue
        if any(not finite(row[column]) for column in coordinates):
            blockers.append(f"{name}_nonfinite_{row_name}")
            continue
        normalized[row_name] = {
            column: float(row[column]) for column in coordinates
        }
    return blockers, normalized


def _validate_vector(
    name: str,
    value: Any,
    coordinates: Sequence[str],
) -> tuple[list[str], dict[str, float]]:
    if not isinstance(value, dict) or set(value) != set(coordinates):
        return [f"{name}_schema_invalid"], {}
    if any(not finite(value[coordinate]) for coordinate in coordinates):
        return [f"{name}_nonfinite"], {}
    return [], {
        coordinate: float(value[coordinate]) for coordinate in coordinates
    }


def _validate_tensor4(
    name: str,
    value: Any,
    coordinates: Sequence[str],
) -> tuple[list[str], dict]:
    try:
        normalized = {
            i: {
                j: {
                    k: {
                        l: float(value[i][j][k][l])
                        for l in coordinates
                    }
                    for k in coordinates
                }
                for j in coordinates
            }
            for i in coordinates
        }
    except (KeyError, TypeError, ValueError):
        return [f"{name}_schema_invalid"], {}
    if any(
        not finite(normalized[i][j][k][l])
        for i in coordinates
        for j in coordinates
        for k in coordinates
        for l in coordinates
    ):
        return [f"{name}_nonfinite"], {}
    return [], normalized


def _metric_pair(
    metric: dict,
    left: dict,
    right: dict,
    coordinates: Sequence[str],
) -> float:
    return sum(
        left[i] * metric[i][j] * right[j]
        for i in coordinates
        for j in coordinates
    )


def _curvature_action(
    curvature: dict,
    tangent: dict,
    variation: dict,
    coordinates: Sequence[str],
) -> dict[str, float]:
    return {
        i: sum(
            curvature[i][j][k][l]
            * tangent[j]
            * variation[k]
            * tangent[l]
            for j in coordinates
            for k in coordinates
            for l in coordinates
        )
        for i in coordinates
    }


def _cholesky_positive_definite(
    matrix: dict,
    coordinates: Sequence[str],
) -> bool:
    size = len(coordinates)
    lower = [[0.0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(i + 1):
            value = matrix[coordinates[i]][coordinates[j]]
            value -= sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if value <= TOL:
                    return False
                lower[i][j] = math.sqrt(value)
            else:
                if abs(lower[j][j]) <= TOL:
                    return False
                lower[i][j] = value / lower[j][j]
    return True


def _jacobi_eigendecomposition(
    matrix: list[list[float]],
    *,
    tolerance: float,
) -> tuple[list[float], list[list[float]], float]:
    size = len(matrix)
    working = [row[:] for row in matrix]
    eigenvectors = [
        [1.0 if i == j else 0.0 for j in range(size)]
        for i in range(size)
    ]
    if size <= 1:
        return ([working[0][0]] if size else []), eigenvectors, 0.0

    maximum_iterations = max(32, 100 * size * size)
    for _ in range(maximum_iterations):
        p = 0
        q = 1
        maximum = abs(working[p][q])
        for i in range(size):
            for j in range(i + 1, size):
                candidate = abs(working[i][j])
                if candidate > maximum:
                    maximum = candidate
                    p, q = i, j
        if maximum <= tolerance:
            break

        app = working[p][p]
        aqq = working[q][q]
        apq = working[p][q]
        angle = 0.5 * math.atan2(2.0 * apq, aqq - app)
        cosine = math.cos(angle)
        sine = math.sin(angle)

        for k in range(size):
            if k in (p, q):
                continue
            akp = working[k][p]
            akq = working[k][q]
            working[k][p] = cosine * akp - sine * akq
            working[p][k] = working[k][p]
            working[k][q] = sine * akp + cosine * akq
            working[q][k] = working[k][q]

        working[p][p] = (
            cosine * cosine * app
            - 2.0 * sine * cosine * apq
            + sine * sine * aqq
        )
        working[q][q] = (
            sine * sine * app
            + 2.0 * sine * cosine * apq
            + cosine * cosine * aqq
        )
        working[p][q] = 0.0
        working[q][p] = 0.0

        for k in range(size):
            vkp = eigenvectors[k][p]
            vkq = eigenvectors[k][q]
            eigenvectors[k][p] = cosine * vkp - sine * vkq
            eigenvectors[k][q] = sine * vkp + cosine * vkq

    residual = max(
        (
            abs(working[i][j])
            for i in range(size)
            for j in range(size)
            if i != j
        ),
        default=0.0,
    )
    eigenvalues = [working[i][i] for i in range(size)]
    order = sorted(range(size), key=lambda index: eigenvalues[index])
    sorted_values = [eigenvalues[index] for index in order]
    sorted_vectors = [
        [eigenvectors[row][index] for index in order]
        for row in range(size)
    ]
    return sorted_values, sorted_vectors, residual


def _normalize_sign(vector: list[float]) -> list[float]:
    for value in vector:
        if abs(value) > TOL:
            return [-entry for entry in vector] if value < 0 else vector
    return vector


def compute_second_variation_input_digest(
    *,
    metric: dict,
    curvature: dict,
    variation_basis: list[dict],
    quadrature_samples: list[dict],
) -> str:
    return canonical_digest(
        {
            "metric": metric,
            "curvature": curvature,
            "variation_basis": variation_basis,
            "quadrature_samples": quadrature_samples,
        }
    )


def build_second_variation_morse_index_certificate(
    *,
    source_jacobi_certificate_digest: str,
    second_variation_input_digest: str,
    metric_matrix: dict,
    riemann_tensor: dict,
    variation_basis: list[dict],
    quadrature_samples: list[dict],
    endpoint_vanishing_tolerance: float,
    minimum_tangent_norm: float,
    eigenvalue_zero_tolerance: float,
    maximum_absolute_index_entry: float,
    maximum_absolute_eigenvalue: float,
    maximum_index_symmetry_residual: float,
    maximum_spectral_invariant_residual: float,
) -> SecondVariationMorseIndexCertificateResult:
    blockers: list[str] = []

    if (
        not isinstance(source_jacobi_certificate_digest, str)
        or not source_jacobi_certificate_digest
    ):
        blockers.append("source_jacobi_certificate_digest_missing")
    if (
        not isinstance(second_variation_input_digest, str)
        or not second_variation_input_digest
    ):
        blockers.append("second_variation_input_digest_missing")

    bounds = {
        "endpoint_vanishing_tolerance": endpoint_vanishing_tolerance,
        "minimum_tangent_norm": minimum_tangent_norm,
        "eigenvalue_zero_tolerance": eigenvalue_zero_tolerance,
        "maximum_absolute_index_entry": maximum_absolute_index_entry,
        "maximum_absolute_eigenvalue": maximum_absolute_eigenvalue,
        "maximum_index_symmetry_residual": maximum_index_symmetry_residual,
        "maximum_spectral_invariant_residual": (
            maximum_spectral_invariant_residual
        ),
    }
    for name, value in bounds.items():
        if not finite(value) or float(value) <= 0.0:
            blockers.append(f"{name}_invalid")

    if not isinstance(metric_matrix, dict) or not metric_matrix:
        blockers.append("metric_matrix_empty")
        coordinates: list[str] = []
    else:
        coordinates = _coordinates(metric_matrix)

    errors, metric = _validate_matrix(
        "metric_matrix", metric_matrix, coordinates
    )
    blockers.extend(errors)
    errors, curvature = _validate_tensor4(
        "riemann_tensor", riemann_tensor, coordinates
    )
    blockers.extend(errors)

    normalized_basis: list[dict] = []
    basis_ids: list[str] = []
    if not isinstance(variation_basis, list) or not variation_basis:
        blockers.append("variation_basis_empty")
    else:
        seen_basis_ids: set[str] = set()
        seen_source_digests: set[str] = set()
        fields = {
            "basis_id",
            "source_candidate_id",
            "source_variation_digest",
            "initial_endpoint_vector",
            "final_endpoint_vector",
        }
        for index, basis in enumerate(variation_basis):
            if not isinstance(basis, dict) or set(basis) != fields:
                blockers.append(f"variation_basis_schema_invalid_{index}")
                continue
            basis_id = basis["basis_id"]
            candidate_id = basis["source_candidate_id"]
            source_digest = basis["source_variation_digest"]
            if not isinstance(basis_id, str) or not basis_id:
                blockers.append(f"variation_basis_id_invalid_{index}")
                continue
            if basis_id in seen_basis_ids:
                blockers.append("duplicate_variation_basis_id")
            seen_basis_ids.add(basis_id)
            if not isinstance(candidate_id, str) or not candidate_id:
                blockers.append(f"source_candidate_id_invalid_{index}")
            if not isinstance(source_digest, str) or not source_digest:
                blockers.append(f"source_variation_digest_missing_{index}")
            elif source_digest in seen_source_digests:
                blockers.append("duplicate_source_variation_digest")
            seen_source_digests.add(source_digest)
            initial_errors, initial = _validate_vector(
                f"initial_endpoint_vector_{index}",
                basis["initial_endpoint_vector"],
                coordinates,
            )
            final_errors, final = _validate_vector(
                f"final_endpoint_vector_{index}",
                basis["final_endpoint_vector"],
                coordinates,
            )
            blockers.extend(initial_errors)
            blockers.extend(final_errors)
            if not initial_errors and not final_errors:
                normalized_basis.append(
                    {
                        "basis_id": basis_id,
                        "source_candidate_id": candidate_id,
                        "source_variation_digest": source_digest,
                        "initial_endpoint_vector": initial,
                        "final_endpoint_vector": final,
                    }
                )
        normalized_basis.sort(key=lambda item: item["basis_id"])
        basis_ids = [item["basis_id"] for item in normalized_basis]

    normalized_samples: list[dict] = []
    if not isinstance(quadrature_samples, list) or not quadrature_samples:
        blockers.append("quadrature_samples_empty")
    else:
        seen_sample_ids: set[str] = set()
        sample_fields = {
            "sample_id",
            "quadrature_weight",
            "tangent",
            "basis_data",
        }
        basis_data_fields = {"variation_field", "covariant_derivative"}
        for sample_index, sample in enumerate(quadrature_samples):
            if not isinstance(sample, dict) or set(sample) != sample_fields:
                blockers.append(
                    f"quadrature_sample_schema_invalid_{sample_index}"
                )
                continue
            sample_id = sample["sample_id"]
            weight = sample["quadrature_weight"]
            if not isinstance(sample_id, str) or not sample_id:
                blockers.append(
                    f"quadrature_sample_id_invalid_{sample_index}"
                )
                continue
            if sample_id in seen_sample_ids:
                blockers.append("duplicate_quadrature_sample_id")
            seen_sample_ids.add(sample_id)
            if not finite(weight) or float(weight) <= 0.0:
                blockers.append(
                    f"quadrature_weight_invalid_{sample_index}"
                )
                continue
            tangent_errors, tangent = _validate_vector(
                f"quadrature_tangent_{sample_index}",
                sample["tangent"],
                coordinates,
            )
            blockers.extend(tangent_errors)
            basis_data = sample["basis_data"]
            if not isinstance(basis_data, dict) or set(basis_data) != set(
                basis_ids
            ):
                blockers.append(
                    f"quadrature_basis_data_schema_invalid_{sample_index}"
                )
                continue
            normalized_data: dict[str, dict] = {}
            data_invalid = bool(tangent_errors)
            for basis_id in basis_ids:
                entry = basis_data[basis_id]
                if not isinstance(entry, dict) or set(entry) != basis_data_fields:
                    blockers.append(
                        f"quadrature_basis_entry_invalid_"
                        f"{sample_index}_{basis_id}"
                    )
                    data_invalid = True
                    continue
                field_errors, variation = _validate_vector(
                    f"quadrature_variation_{sample_index}_{basis_id}",
                    entry["variation_field"],
                    coordinates,
                )
                derivative_errors, derivative = _validate_vector(
                    f"quadrature_derivative_{sample_index}_{basis_id}",
                    entry["covariant_derivative"],
                    coordinates,
                )
                blockers.extend(field_errors)
                blockers.extend(derivative_errors)
                data_invalid = (
                    data_invalid
                    or bool(field_errors)
                    or bool(derivative_errors)
                )
                normalized_data[basis_id] = {
                    "variation_field": variation,
                    "covariant_derivative": derivative,
                }
            if not data_invalid:
                normalized_samples.append(
                    {
                        "sample_id": sample_id,
                        "quadrature_weight": float(weight),
                        "tangent": tangent,
                        "basis_data": normalized_data,
                    }
                )
        normalized_samples.sort(key=lambda item: item["sample_id"])

    if blockers:
        return SecondVariationMorseIndexCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    if any(
        not close(metric[i][j], metric[j][i])
        for i in coordinates
        for j in coordinates
    ):
        blockers.append("metric_not_symmetric")
    if not _cholesky_positive_definite(metric, coordinates):
        blockers.append("metric_not_positive_definite")

    endpoint_tolerance_squared = endpoint_vanishing_tolerance ** 2
    for basis in normalized_basis:
        initial_norm = _metric_pair(
            metric,
            basis["initial_endpoint_vector"],
            basis["initial_endpoint_vector"],
            coordinates,
        )
        final_norm = _metric_pair(
            metric,
            basis["final_endpoint_vector"],
            basis["final_endpoint_vector"],
            coordinates,
        )
        basis["initial_endpoint_norm_squared"] = initial_norm
        basis["final_endpoint_norm_squared"] = final_norm
        if initial_norm > endpoint_tolerance_squared + TOL:
            blockers.append(
                f"initial_endpoint_not_vanishing_{basis['basis_id']}"
            )
        if final_norm > endpoint_tolerance_squared + TOL:
            blockers.append(
                f"final_endpoint_not_vanishing_{basis['basis_id']}"
            )

    minimum_tangent_norm_squared = minimum_tangent_norm ** 2
    for sample in normalized_samples:
        tangent_norm = _metric_pair(
            metric, sample["tangent"], sample["tangent"], coordinates
        )
        sample["tangent_norm_squared"] = tangent_norm
        if tangent_norm < minimum_tangent_norm_squared - TOL:
            blockers.append(
                f"quadrature_tangent_too_small_{sample['sample_id']}"
            )

    expected_digest = compute_second_variation_input_digest(
        metric=metric,
        curvature=curvature,
        variation_basis=[
            {
                key: value
                for key, value in basis.items()
                if key
                not in {
                    "initial_endpoint_norm_squared",
                    "final_endpoint_norm_squared",
                }
            }
            for basis in normalized_basis
        ],
        quadrature_samples=[
            {
                key: value
                for key, value in sample.items()
                if key != "tangent_norm_squared"
            }
            for sample in normalized_samples
        ],
    )
    if second_variation_input_digest != expected_digest:
        blockers.append("second_variation_input_digest_mismatch")

    size = len(basis_ids)
    index_matrix = [
        [0.0 for _ in range(size)] for _ in range(size)
    ]
    sample_records: list[dict] = []
    for sample in normalized_samples:
        weight = sample["quadrature_weight"]
        tangent = sample["tangent"]
        curvature_actions: dict[str, dict[str, float]] = {}
        for basis_id in basis_ids:
            curvature_actions[basis_id] = _curvature_action(
                curvature,
                tangent,
                sample["basis_data"][basis_id]["variation_field"],
                coordinates,
            )
        integrand_matrix: dict[str, dict[str, float]] = {
            left: {} for left in basis_ids
        }
        for left_index, left_id in enumerate(basis_ids):
            left_data = sample["basis_data"][left_id]
            for right_index, right_id in enumerate(basis_ids):
                right_data = sample["basis_data"][right_id]
                derivative_pair = _metric_pair(
                    metric,
                    left_data["covariant_derivative"],
                    right_data["covariant_derivative"],
                    coordinates,
                )
                curvature_pair = _metric_pair(
                    metric,
                    curvature_actions[left_id],
                    right_data["variation_field"],
                    coordinates,
                )
                integrand = derivative_pair - curvature_pair
                integrand_matrix[left_id][right_id] = integrand
                index_matrix[left_index][right_index] += weight * integrand
        sample_records.append(
            {
                "sample_id": sample["sample_id"],
                "quadrature_weight": weight,
                "tangent": tangent,
                "tangent_norm_squared": sample["tangent_norm_squared"],
                "curvature_action_by_basis": curvature_actions,
                "index_integrand_matrix": integrand_matrix,
            }
        )

    maximum_entry = max(
        (abs(value) for row in index_matrix for value in row),
        default=0.0,
    )
    symmetry_residual = max(
        (
            abs(index_matrix[i][j] - index_matrix[j][i])
            for i in range(size)
            for j in range(size)
        ),
        default=0.0,
    )
    if maximum_entry > maximum_absolute_index_entry + TOL:
        blockers.append("index_entry_bound_exceeded")
    if symmetry_residual > maximum_index_symmetry_residual + TOL:
        blockers.append("index_form_symmetry_residual_exceeded")

    eigenvalues, eigenvectors, eigensolver_residual = (
        _jacobi_eigendecomposition(
            index_matrix,
            tolerance=min(
                eigenvalue_zero_tolerance * 0.01,
                maximum_index_symmetry_residual * 0.01,
                1e-12,
            ),
        )
    )
    maximum_eigenvalue = max(
        (abs(value) for value in eigenvalues), default=0.0
    )
    if maximum_eigenvalue > maximum_absolute_eigenvalue + TOL:
        blockers.append("eigenvalue_bound_exceeded")

    trace = sum(index_matrix[i][i] for i in range(size))
    spectral_trace = sum(eigenvalues)
    frobenius_squared = sum(
        value * value for row in index_matrix for value in row
    )
    spectral_square_sum = sum(value * value for value in eigenvalues)
    trace_residual = abs(trace - spectral_trace)
    square_sum_residual = abs(frobenius_squared - spectral_square_sum)
    spectral_invariant_residual = max(
        trace_residual, square_sum_residual, eigensolver_residual
    )
    if (
        spectral_invariant_residual
        > maximum_spectral_invariant_residual + TOL
    ):
        blockers.append("spectral_invariant_residual_exceeded")

    if blockers:
        return SecondVariationMorseIndexCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    negative_count = sum(
        value < -eigenvalue_zero_tolerance for value in eigenvalues
    )
    nullity = sum(
        abs(value) <= eigenvalue_zero_tolerance for value in eigenvalues
    )
    positive_count = size - negative_count - nullity

    spectral_records: list[dict] = []
    for column, eigenvalue in enumerate(eigenvalues):
        coefficients = _normalize_sign(
            [eigenvectors[row][column] for row in range(size)]
        )
        if eigenvalue < -eigenvalue_zero_tolerance:
            disposition = "negative"
        elif eigenvalue > eigenvalue_zero_tolerance:
            disposition = "positive"
        else:
            disposition = "null"
        spectral_records.append(
            {
                "eigenvalue": eigenvalue,
                "disposition": disposition,
                "basis_coefficients": {
                    basis_ids[index]: coefficients[index]
                    for index in range(size)
                },
            }
        )

    index_matrix_mapping = {
        basis_ids[i]: {
            basis_ids[j]: index_matrix[i][j]
            for j in range(size)
        }
        for i in range(size)
    }

    certificate = {
        "kernel": "PlanOS Second Variation and Morse Index Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.10",
        "source_jacobi_certificate_digest": (
            source_jacobi_certificate_digest
        ),
        "second_variation_input_digest": second_variation_input_digest,
        "metric_matrix": metric,
        "riemann_tensor": curvature,
        "variation_basis_records": normalized_basis,
        "quadrature_sample_records": sample_records,
        "index_form_matrix": index_matrix_mapping,
        "index_form_eigenvalue_records": spectral_records,
        "finite_basis_morse_index": negative_count,
        "finite_basis_nullity": nullity,
        "finite_basis_positive_dimension": positive_count,
        "computed_maximum_absolute_index_entry": maximum_entry,
        "computed_maximum_absolute_eigenvalue": maximum_eigenvalue,
        "computed_index_symmetry_residual": symmetry_residual,
        "computed_spectral_trace_residual": trace_residual,
        "computed_spectral_square_sum_residual": square_sum_residual,
        "computed_eigensolver_offdiagonal_residual": (
            eigensolver_residual
        ),
        "endpoint_fixed_variations_verified": True,
        "index_form_symmetric": True,
        "second_variation_retained": True,
        "finite_basis_morse_index_computed": True,
        "conjugate_multiplicity_candidate": nullity,
        "conjugate_multiplicity_candidate_local_only": True,
        "morse_index_finite_window_only": True,
        "negative_direction_witnesses_retained": negative_count > 0,
        "null_direction_witnesses_retained": nullity > 0,
        "candidate_identity_retained": True,
        "source_jacobi_certificate_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "curvature_grants_no_authority": True,
        "second_variation_grants_no_authority": True,
        "morse_index_grants_no_authority": True,
        "conjugate_multiplicity_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["second_variation_certificate_digest"] = (
        canonical_digest(certificate)
    )
    return SecondVariationMorseIndexCertificateResult(
        STATUS_READY, [], certificate
    )
