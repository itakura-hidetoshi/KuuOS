#!/usr/bin/env python3
from __future__ import annotations

import math
from typing import Any

from runtime.kuuos_planos_atlas_common_v0_1 import (
    GEOMETRY_TOL,
    TOL,
    _determinant,
    _is_identity,
    _matrix_product,
    close,
)
from runtime.kuuos_planos_atlas_geometry_v0_1 import (
    _connection_transform,
    _inverse_metric_transform,
    _maximum_matrix_residual,
    _maximum_tensor3_residual,
    _maximum_tensor4_residual,
    _metric_transform,
    _ricci_transform,
    _riemann_transform,
    _transform_vector,
)


def evaluate_atlas_transitions(
    *,
    normalized_charts: list[dict],
    normalized_transitions: list[dict],
    minimum_absolute_jacobian_determinant: float,
    maximum_absolute_jacobian_component: float,
    maximum_absolute_inverse_jacobian_component: float,
    maximum_absolute_transition_hessian_component: float,
    minimum_overlap_margin: float,
    maximum_metric_transform_residual: float,
    maximum_connection_transform_residual: float,
    maximum_curvature_transform_residual: float,
    maximum_scalar_invariance_residual: float,
    maximum_sectional_invariance_residual: float,
    maximum_holonomy_equivariance_residual: float,
) -> tuple[list[str], list[dict], dict[str, float], dict[tuple[str, str], dict]]:
    blockers: list[str] = []
    chart_by_id = {chart["chart_id"]: chart for chart in normalized_charts}
    transition_by_pair = {
        (transition["source_chart_id"], transition["target_chart_id"]): transition
        for transition in normalized_transitions
    }
    records: list[dict] = []
    observed = {
        "minimum_absolute_jacobian_determinant": math.inf,
        "maximum_absolute_jacobian_component": 0.0,
        "maximum_absolute_inverse_jacobian_component": 0.0,
        "maximum_absolute_transition_hessian_component": 0.0,
        "minimum_overlap_margin": math.inf,
        "maximum_metric_transform_residual": 0.0,
        "maximum_inverse_metric_transform_residual": 0.0,
        "maximum_connection_transform_residual": 0.0,
        "maximum_riemann_transform_residual": 0.0,
        "maximum_ricci_transform_residual": 0.0,
        "maximum_scalar_invariance_residual": 0.0,
        "maximum_sectional_invariance_residual": 0.0,
        "maximum_holonomy_equivariance_residual": 0.0,
    }
    nontrivial_transition_present = False

    for transition in normalized_transitions:
        source = chart_by_id[transition["source_chart_id"]]
        target = chart_by_id[transition["target_chart_id"]]
        source_coordinates = source["coordinates"]
        target_coordinates = target["coordinates"]
        jacobian = transition["jacobian"]
        inverse_jacobian = transition["inverse_jacobian"]
        inverse_hessian = transition["inverse_hessian"]
        transition_name = f"{source['chart_id']}_{target['chart_id']}"

        determinant = _determinant(jacobian, target_coordinates, source_coordinates)
        observed["minimum_absolute_jacobian_determinant"] = min(
            observed["minimum_absolute_jacobian_determinant"], abs(determinant)
        )
        if abs(determinant) < minimum_absolute_jacobian_determinant - TOL:
            blockers.append(f"singular_or_near_singular_transition_{transition_name}")

        jacobian_max = max(
            abs(jacobian[a][i])
            for a in target_coordinates
            for i in source_coordinates
        )
        inverse_max = max(
            abs(inverse_jacobian[i][a])
            for i in source_coordinates
            for a in target_coordinates
        )
        hessian_max = max(
            abs(inverse_hessian[i][a][b])
            for i in source_coordinates
            for a in target_coordinates
            for b in target_coordinates
        )
        observed["maximum_absolute_jacobian_component"] = max(
            observed["maximum_absolute_jacobian_component"], jacobian_max
        )
        observed["maximum_absolute_inverse_jacobian_component"] = max(
            observed["maximum_absolute_inverse_jacobian_component"], inverse_max
        )
        observed["maximum_absolute_transition_hessian_component"] = max(
            observed["maximum_absolute_transition_hessian_component"], hessian_max
        )
        observed["minimum_overlap_margin"] = min(
            observed["minimum_overlap_margin"], transition["overlap_margin"]
        )
        if transition["overlap_margin"] < minimum_overlap_margin - TOL:
            blockers.append(f"overlap_margin_below_minimum_{transition_name}")
        if jacobian_max > maximum_absolute_jacobian_component + TOL:
            blockers.append("jacobian_component_bound_exceeded")
        if inverse_max > maximum_absolute_inverse_jacobian_component + TOL:
            blockers.append("inverse_jacobian_component_bound_exceeded")
        if hessian_max > maximum_absolute_transition_hessian_component + TOL:
            blockers.append("transition_hessian_component_bound_exceeded")

        jacobian_inverse = _matrix_product(
            jacobian,
            inverse_jacobian,
            target_coordinates,
            source_coordinates,
            target_coordinates,
        )
        inverse_jacobian_product = _matrix_product(
            inverse_jacobian,
            jacobian,
            source_coordinates,
            target_coordinates,
            source_coordinates,
        )
        if not (
            _is_identity(jacobian_inverse, target_coordinates)
            and _is_identity(inverse_jacobian_product, source_coordinates)
        ):
            blockers.append(f"transition_inverse_identity_mismatch_{transition_name}")
        if any(
            not close(
                inverse_hessian[i][a][b],
                inverse_hessian[i][b][a],
                GEOMETRY_TOL,
            )
            for i in source_coordinates
            for a in target_coordinates
            for b in target_coordinates
        ):
            blockers.append(f"transition_hessian_not_symmetric_{transition_name}")

        expected_metric = _metric_transform(
            inverse_jacobian,
            source["metric_matrix"],
            source_coordinates,
            target_coordinates,
        )
        metric_residual = _maximum_matrix_residual(
            expected_metric,
            target["metric_matrix"],
            target_coordinates,
            target_coordinates,
        )
        observed["maximum_metric_transform_residual"] = max(
            observed["maximum_metric_transform_residual"], metric_residual
        )
        if metric_residual > maximum_metric_transform_residual + TOL:
            blockers.append(f"metric_transform_residual_exceeded_{transition_name}")

        expected_inverse_metric = _inverse_metric_transform(
            jacobian,
            source["inverse_metric_matrix"],
            source_coordinates,
            target_coordinates,
        )
        inverse_metric_residual = _maximum_matrix_residual(
            expected_inverse_metric,
            target["inverse_metric_matrix"],
            target_coordinates,
            target_coordinates,
        )
        observed["maximum_inverse_metric_transform_residual"] = max(
            observed["maximum_inverse_metric_transform_residual"],
            inverse_metric_residual,
        )
        if inverse_metric_residual > maximum_metric_transform_residual + TOL:
            blockers.append(
                f"inverse_metric_transform_residual_exceeded_{transition_name}"
            )

        expected_connection = _connection_transform(
            jacobian,
            inverse_jacobian,
            inverse_hessian,
            source["christoffel_symbols"],
            source_coordinates,
            target_coordinates,
        )
        connection_residual = _maximum_tensor3_residual(
            expected_connection, target["christoffel_symbols"], target_coordinates
        )
        observed["maximum_connection_transform_residual"] = max(
            observed["maximum_connection_transform_residual"], connection_residual
        )
        if connection_residual > maximum_connection_transform_residual + TOL:
            blockers.append(f"connection_transform_residual_exceeded_{transition_name}")

        expected_riemann = _riemann_transform(
            jacobian,
            inverse_jacobian,
            source["riemann_tensor"],
            source_coordinates,
            target_coordinates,
        )
        riemann_residual = _maximum_tensor4_residual(
            expected_riemann, target["riemann_tensor"], target_coordinates
        )
        observed["maximum_riemann_transform_residual"] = max(
            observed["maximum_riemann_transform_residual"], riemann_residual
        )
        if riemann_residual > maximum_curvature_transform_residual + TOL:
            blockers.append(f"riemann_transform_residual_exceeded_{transition_name}")

        expected_ricci = _ricci_transform(
            inverse_jacobian,
            source["ricci_tensor"],
            source_coordinates,
            target_coordinates,
        )
        ricci_residual = _maximum_matrix_residual(
            expected_ricci,
            target["ricci_tensor"],
            target_coordinates,
            target_coordinates,
        )
        observed["maximum_ricci_transform_residual"] = max(
            observed["maximum_ricci_transform_residual"], ricci_residual
        )
        if ricci_residual > maximum_curvature_transform_residual + TOL:
            blockers.append(f"ricci_transform_residual_exceeded_{transition_name}")

        scalar_residual = abs(source["scalar_curvature"] - target["scalar_curvature"])
        observed["maximum_scalar_invariance_residual"] = max(
            observed["maximum_scalar_invariance_residual"], scalar_residual
        )
        if scalar_residual > maximum_scalar_invariance_residual + TOL:
            blockers.append(
                f"scalar_curvature_invariance_residual_exceeded_{transition_name}"
            )

        source_records = {
            record["candidate_id"]: record for record in source["candidate_records"]
        }
        target_records = {
            record["candidate_id"]: record for record in target["candidate_records"]
        }
        if set(source_records) != set(target_records):
            blockers.append(f"candidate_record_identity_mismatch_{transition_name}")
        candidate_transition_records: list[dict] = []
        for candidate_id in sorted(set(source_records) & set(target_records)):
            source_record = source_records[candidate_id]
            target_record = target_records[candidate_id]
            expected_plane_u = _transform_vector(
                jacobian,
                source_record["plane_u"],
                source_coordinates,
                target_coordinates,
            )
            expected_plane_v = _transform_vector(
                jacobian,
                source_record["plane_v"],
                source_coordinates,
                target_coordinates,
            )
            expected_holonomy_vector = _transform_vector(
                jacobian,
                source_record["holonomy_vector"],
                source_coordinates,
                target_coordinates,
            )
            expected_holonomy_increment = _transform_vector(
                jacobian,
                source_record["holonomy_increment"],
                source_coordinates,
                target_coordinates,
            )
            plane_residual = max(
                max(
                    abs(expected_plane_u[a] - target_record["plane_u"][a])
                    for a in target_coordinates
                ),
                max(
                    abs(expected_plane_v[a] - target_record["plane_v"][a])
                    for a in target_coordinates
                ),
                max(
                    abs(
                        expected_holonomy_vector[a]
                        - target_record["holonomy_vector"][a]
                    )
                    for a in target_coordinates
                ),
            )
            if plane_residual > maximum_holonomy_equivariance_residual + TOL:
                blockers.append(
                    "candidate_vector_transform_residual_exceeded_"
                    f"{candidate_id}_{transition_name}"
                )
            sectional_residual = abs(
                source_record["sectional_curvature"]
                - target_record["sectional_curvature"]
            )
            observed["maximum_sectional_invariance_residual"] = max(
                observed["maximum_sectional_invariance_residual"],
                sectional_residual,
            )
            if sectional_residual > maximum_sectional_invariance_residual + TOL:
                blockers.append(
                    "sectional_curvature_invariance_residual_exceeded_"
                    f"{candidate_id}_{transition_name}"
                )
            holonomy_residual = max(
                abs(
                    expected_holonomy_increment[a]
                    - target_record["holonomy_increment"][a]
                )
                for a in target_coordinates
            )
            observed["maximum_holonomy_equivariance_residual"] = max(
                observed["maximum_holonomy_equivariance_residual"],
                holonomy_residual,
            )
            if holonomy_residual > maximum_holonomy_equivariance_residual + TOL:
                blockers.append(
                    f"holonomy_equivariance_residual_exceeded_{candidate_id}_{transition_name}"
                )
            if (
                source_record["source_candidate_digest"]
                != target_record["source_candidate_digest"]
            ):
                blockers.append(
                    f"source_candidate_digest_mismatch_{candidate_id}_{transition_name}"
                )
            candidate_transition_records.append(
                {
                    "candidate_id": candidate_id,
                    "maximum_candidate_vector_residual": plane_residual,
                    "sectional_curvature_residual": sectional_residual,
                    "holonomy_equivariance_residual": holonomy_residual,
                }
            )

        identity_like = (
            source_coordinates == target_coordinates
            and all(
                close(jacobian[a][i], 1.0 if a == i else 0.0)
                for a in target_coordinates
                for i in source_coordinates
            )
        )
        nontrivial_transition_present = nontrivial_transition_present or not identity_like
        records.append(
            {
                "source_chart_id": source["chart_id"],
                "target_chart_id": target["chart_id"],
                "jacobian_determinant": determinant,
                "metric_transform_residual": metric_residual,
                "inverse_metric_transform_residual": inverse_metric_residual,
                "connection_transform_residual": connection_residual,
                "riemann_transform_residual": riemann_residual,
                "ricci_transform_residual": ricci_residual,
                "scalar_curvature_invariance_residual": scalar_residual,
                "candidate_transition_records": candidate_transition_records,
                "overlap_margin": transition["overlap_margin"],
            }
        )

    if not nontrivial_transition_present:
        blockers.append("nontrivial_chart_transition_missing")
    return blockers, records, observed, transition_by_pair
