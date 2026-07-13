#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_planos_atlas_common_v0_1 import (
    GEOMETRY_TOL,
    _is_identity,
    _is_positive_definite,
    _matrix_product,
    _normalize_vector,
    _validate_matrix,
    _validate_named_vector,
    _validate_tensor3,
    _validate_tensor4,
    close,
    finite,
)

def _validate_charts(value: Any) -> tuple[list[str], list[dict]]:
    if not isinstance(value, list) or len(value) < 3:
        return ["atlas_requires_at_least_three_charts"], []
    blockers: list[str] = []
    normalized: list[dict] = []
    seen_ids: set[str] = set()
    expected_fields = {
        "chart_id",
        "coordinates",
        "source_curvature_certificate_digest",
        "metric_matrix",
        "inverse_metric_matrix",
        "christoffel_symbols",
        "riemann_tensor",
        "ricci_tensor",
        "scalar_curvature",
        "candidate_records",
        "boundary_margin",
        "regularity_radius",
    }
    expected_dimension: int | None = None
    for index, chart in enumerate(value):
        if not isinstance(chart, dict) or set(chart) != expected_fields:
            blockers.append(f"chart_schema_invalid_{index}")
            continue
        chart_id = chart["chart_id"]
        coordinates = chart["coordinates"]
        source_digest = chart["source_curvature_certificate_digest"]
        if not isinstance(chart_id, str) or not chart_id.strip():
            blockers.append(f"chart_id_invalid_{index}")
            continue
        chart_id = chart_id.strip()
        if chart_id in seen_ids:
            blockers.append("duplicate_chart_id")
        seen_ids.add(chart_id)
        if not isinstance(coordinates, list) or len(coordinates) < 2:
            blockers.append(f"chart_coordinates_invalid_{chart_id}")
            continue
        coordinates = [str(coordinate) for coordinate in coordinates]
        if any(not coordinate for coordinate in coordinates) or len(set(coordinates)) != len(coordinates):
            blockers.append(f"chart_coordinates_invalid_{chart_id}")
            continue
        if expected_dimension is None:
            expected_dimension = len(coordinates)
        elif len(coordinates) != expected_dimension:
            blockers.append("chart_dimension_mismatch")
        if not isinstance(source_digest, str) or not source_digest:
            blockers.append(f"source_curvature_certificate_digest_missing_{chart_id}")
        metric_errors, metric = _validate_matrix(
            f"metric_{chart_id}", chart["metric_matrix"], coordinates, coordinates
        )
        inverse_errors, inverse = _validate_matrix(
            f"inverse_metric_{chart_id}", chart["inverse_metric_matrix"], coordinates, coordinates
        )
        connection_errors, connection = _validate_tensor3(
            f"christoffel_{chart_id}",
            chart["christoffel_symbols"],
            coordinates,
            coordinates,
            coordinates,
        )
        riemann_errors, riemann = _validate_tensor4(
            f"riemann_{chart_id}",
            chart["riemann_tensor"],
            coordinates,
            coordinates,
            coordinates,
            coordinates,
        )
        ricci_errors, ricci = _validate_matrix(
            f"ricci_{chart_id}", chart["ricci_tensor"], coordinates, coordinates
        )
        blockers.extend(metric_errors + inverse_errors + connection_errors + riemann_errors + ricci_errors)
        if not finite(chart["scalar_curvature"]):
            blockers.append(f"scalar_curvature_nonfinite_{chart_id}")
        if not finite(chart["boundary_margin"]) or float(chart["boundary_margin"]) <= 0.0:
            blockers.append(f"boundary_margin_invalid_{chart_id}")
        if not finite(chart["regularity_radius"]) or float(chart["regularity_radius"]) <= 0.0:
            blockers.append(f"regularity_radius_invalid_{chart_id}")
        candidate_records = chart["candidate_records"]
        if not isinstance(candidate_records, list) or not candidate_records:
            blockers.append(f"candidate_records_empty_{chart_id}")
            candidate_records = []
        normalized_records: list[dict] = []
        seen_candidates: set[str] = set()
        for record_index, record in enumerate(candidate_records):
            required = {
                "candidate_id",
                "plane_u",
                "plane_v",
                "holonomy_vector",
                "sectional_curvature",
                "holonomy_increment",
                "source_candidate_digest",
            }
            if not isinstance(record, dict) or set(record) != required:
                blockers.append(f"candidate_record_schema_invalid_{chart_id}_{record_index}")
                continue
            candidate_id = record["candidate_id"]
            if not isinstance(candidate_id, str) or not candidate_id.strip():
                blockers.append(f"candidate_id_invalid_{chart_id}_{record_index}")
                continue
            candidate_id = candidate_id.strip()
            if candidate_id in seen_candidates:
                blockers.append(f"duplicate_candidate_id_{chart_id}")
            seen_candidates.add(candidate_id)
            vector_values: dict[str, dict] = {}
            vector_invalid = False
            for field in ("plane_u", "plane_v", "holonomy_vector", "holonomy_increment"):
                errors, vector = _validate_named_vector(
                    f"candidate_{field}_{chart_id}_{candidate_id}", record[field], coordinates
                )
                blockers.extend(errors)
                if errors:
                    vector_invalid = True
                else:
                    vector_values[field] = vector
            if not finite(record["sectional_curvature"]):
                blockers.append(f"sectional_curvature_nonfinite_{chart_id}_{candidate_id}")
                vector_invalid = True
            source_candidate_digest = record["source_candidate_digest"]
            if not isinstance(source_candidate_digest, str) or not source_candidate_digest:
                blockers.append(f"source_candidate_digest_missing_{chart_id}_{candidate_id}")
                vector_invalid = True
            if not vector_invalid:
                normalized_records.append(
                    {
                        "candidate_id": candidate_id,
                        **vector_values,
                        "sectional_curvature": float(record["sectional_curvature"]),
                        "source_candidate_digest": source_candidate_digest,
                    }
                )
        if not metric_errors and not all(close(metric[i][j], metric[j][i]) for i in coordinates for j in coordinates):
            blockers.append(f"metric_not_symmetric_{chart_id}")
        if not metric_errors and not _is_positive_definite(metric, coordinates):
            blockers.append(f"metric_not_positive_definite_{chart_id}")
        if not metric_errors and not inverse_errors:
            left = _matrix_product(inverse, metric, coordinates, coordinates, coordinates)
            right = _matrix_product(metric, inverse, coordinates, coordinates, coordinates)
            if not (_is_identity(left, coordinates) and _is_identity(right, coordinates)):
                blockers.append(f"inverse_metric_identity_mismatch_{chart_id}")
        if not ricci_errors and not all(close(ricci[i][j], ricci[j][i], GEOMETRY_TOL) for i in coordinates for j in coordinates):
            blockers.append(f"ricci_not_symmetric_{chart_id}")
        if not inverse_errors and not ricci_errors and finite(chart["scalar_curvature"]):
            computed_scalar = sum(
                inverse[i][j] * ricci[i][j]
                for i in coordinates
                for j in coordinates
            )
            if not close(computed_scalar, float(chart["scalar_curvature"]), GEOMETRY_TOL):
                blockers.append(f"scalar_contraction_mismatch_{chart_id}")
        normalized.append(
            {
                "chart_id": chart_id,
                "coordinates": coordinates,
                "source_curvature_certificate_digest": source_digest,
                "metric_matrix": metric,
                "inverse_metric_matrix": inverse,
                "christoffel_symbols": connection,
                "riemann_tensor": riemann,
                "ricci_tensor": ricci,
                "scalar_curvature": float(chart["scalar_curvature"]) if finite(chart["scalar_curvature"]) else 0.0,
                "candidate_records": sorted(normalized_records, key=lambda record: record["candidate_id"]),
                "boundary_margin": float(chart["boundary_margin"]) if finite(chart["boundary_margin"]) else 0.0,
                "regularity_radius": float(chart["regularity_radius"]) if finite(chart["regularity_radius"]) else 0.0,
            }
        )
    normalized.sort(key=lambda chart: chart["chart_id"])
    return blockers, normalized


def _validate_transitions(value: Any, chart_by_id: Mapping[str, dict]) -> tuple[list[str], list[dict]]:
    if not isinstance(value, list) or not value:
        return ["atlas_transition_field_empty"], []
    blockers: list[str] = []
    normalized: list[dict] = []
    seen_pairs: set[tuple[str, str]] = set()
    expected_fields = {
        "source_chart_id",
        "target_chart_id",
        "jacobian",
        "inverse_jacobian",
        "inverse_hessian",
        "overlap_margin",
        "source_transition_digest",
    }
    for index, transition in enumerate(value):
        if not isinstance(transition, dict) or set(transition) != expected_fields:
            blockers.append(f"transition_schema_invalid_{index}")
            continue
        source_id = transition["source_chart_id"]
        target_id = transition["target_chart_id"]
        if source_id not in chart_by_id or target_id not in chart_by_id:
            blockers.append(f"transition_chart_reference_invalid_{index}")
            continue
        if source_id == target_id:
            blockers.append(f"transition_self_map_forbidden_{source_id}")
        pair = (source_id, target_id)
        if pair in seen_pairs:
            blockers.append("duplicate_transition_pair")
        seen_pairs.add(pair)
        source_coordinates = chart_by_id[source_id]["coordinates"]
        target_coordinates = chart_by_id[target_id]["coordinates"]
        jacobian_errors, jacobian = _validate_matrix(
            f"jacobian_{source_id}_{target_id}",
            transition["jacobian"],
            target_coordinates,
            source_coordinates,
        )
        inverse_errors, inverse_jacobian = _validate_matrix(
            f"inverse_jacobian_{source_id}_{target_id}",
            transition["inverse_jacobian"],
            source_coordinates,
            target_coordinates,
        )
        hessian_errors, inverse_hessian = _validate_tensor3(
            f"inverse_hessian_{source_id}_{target_id}",
            transition["inverse_hessian"],
            source_coordinates,
            target_coordinates,
            target_coordinates,
        )
        blockers.extend(jacobian_errors + inverse_errors + hessian_errors)
        if not finite(transition["overlap_margin"]) or float(transition["overlap_margin"]) <= 0.0:
            blockers.append(f"overlap_margin_invalid_{source_id}_{target_id}")
        source_transition_digest = transition["source_transition_digest"]
        if not isinstance(source_transition_digest, str) or not source_transition_digest:
            blockers.append(f"source_transition_digest_missing_{source_id}_{target_id}")
        normalized.append(
            {
                "source_chart_id": source_id,
                "target_chart_id": target_id,
                "jacobian": jacobian,
                "inverse_jacobian": inverse_jacobian,
                "inverse_hessian": inverse_hessian,
                "overlap_margin": float(transition["overlap_margin"]) if finite(transition["overlap_margin"]) else 0.0,
                "source_transition_digest": source_transition_digest,
            }
        )
    normalized.sort(key=lambda transition: (transition["source_chart_id"], transition["target_chart_id"]))
    return blockers, normalized


