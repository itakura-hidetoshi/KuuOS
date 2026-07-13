#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_planos_atlas_common_v0_1 import (
    TOL,
    _matrix_product,
)
from runtime.kuuos_planos_atlas_geometry_v0_1 import _maximum_matrix_residual


def evaluate_atlas_cocycles(
    *,
    normalized_charts: list[dict],
    transition_by_pair: dict[tuple[str, str], dict],
    maximum_cocycle_residual: float,
) -> tuple[list[str], list[dict], float]:
    blockers: list[str] = []
    records: list[dict] = []
    maximum_observed = 0.0
    chart_by_id = {chart["chart_id"]: chart for chart in normalized_charts}
    chart_ids = sorted(chart_by_id)
    for source_id in chart_ids:
        for middle_id in chart_ids:
            for target_id in chart_ids:
                if len({source_id, middle_id, target_id}) < 3:
                    continue
                source_middle = transition_by_pair.get((source_id, middle_id))
                middle_target = transition_by_pair.get((middle_id, target_id))
                source_target = transition_by_pair.get((source_id, target_id))
                if not (source_middle and middle_target and source_target):
                    continue
                source_coordinates = chart_by_id[source_id]["coordinates"]
                middle_coordinates = chart_by_id[middle_id]["coordinates"]
                target_coordinates = chart_by_id[target_id]["coordinates"]
                composed_jacobian = _matrix_product(
                    middle_target["jacobian"],
                    source_middle["jacobian"],
                    target_coordinates,
                    middle_coordinates,
                    source_coordinates,
                )
                jacobian_residual = _maximum_matrix_residual(
                    composed_jacobian,
                    source_target["jacobian"],
                    target_coordinates,
                    source_coordinates,
                )
                composed_inverse = _matrix_product(
                    source_middle["inverse_jacobian"],
                    middle_target["inverse_jacobian"],
                    source_coordinates,
                    middle_coordinates,
                    target_coordinates,
                )
                inverse_residual = _maximum_matrix_residual(
                    composed_inverse,
                    source_target["inverse_jacobian"],
                    source_coordinates,
                    target_coordinates,
                )
                residual = max(jacobian_residual, inverse_residual)
                maximum_observed = max(maximum_observed, residual)
                if residual > maximum_cocycle_residual + TOL:
                    blockers.append(
                        f"atlas_cocycle_residual_exceeded_{source_id}_{middle_id}_{target_id}"
                    )
                records.append(
                    {
                        "source_chart_id": source_id,
                        "middle_chart_id": middle_id,
                        "target_chart_id": target_id,
                        "jacobian_cocycle_residual": jacobian_residual,
                        "inverse_jacobian_cocycle_residual": inverse_residual,
                    }
                )
    if not records:
        blockers.append("atlas_cocycle_witness_missing")
    return blockers, records, maximum_observed
