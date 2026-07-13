#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping, Sequence

from runtime.kuuos_planos_atlas_common_v0_1 import TOL

def _transform_vector(
    jacobian: Mapping[str, Mapping[str, float]],
    vector: Mapping[str, float],
    source_coordinates: Sequence[str],
    target_coordinates: Sequence[str],
) -> dict:
    return {
        target: sum(jacobian[target][source] * vector[source] for source in source_coordinates)
        for target in target_coordinates
    }


def _metric_transform(
    inverse_jacobian: Mapping[str, Mapping[str, float]],
    source_metric: Mapping[str, Mapping[str, float]],
    source_coordinates: Sequence[str],
    target_coordinates: Sequence[str],
) -> dict:
    return {
        a: {
            b: sum(
                inverse_jacobian[i][a]
                * source_metric[i][j]
                * inverse_jacobian[j][b]
                for i in source_coordinates
                for j in source_coordinates
            )
            for b in target_coordinates
        }
        for a in target_coordinates
    }


def _inverse_metric_transform(
    jacobian: Mapping[str, Mapping[str, float]],
    source_inverse_metric: Mapping[str, Mapping[str, float]],
    source_coordinates: Sequence[str],
    target_coordinates: Sequence[str],
) -> dict:
    return {
        a: {
            b: sum(
                jacobian[a][i]
                * source_inverse_metric[i][j]
                * jacobian[b][j]
                for i in source_coordinates
                for j in source_coordinates
            )
            for b in target_coordinates
        }
        for a in target_coordinates
    }


def _connection_transform(
    jacobian: Mapping[str, Mapping[str, float]],
    inverse_jacobian: Mapping[str, Mapping[str, float]],
    inverse_hessian: Mapping[str, Mapping[str, Mapping[str, float]]],
    source_connection: Mapping[str, Mapping[str, Mapping[str, float]]],
    source_coordinates: Sequence[str],
    target_coordinates: Sequence[str],
) -> dict:
    return {
        a: {
            b: {
                c: sum(
                    jacobian[a][i]
                    * inverse_jacobian[j][b]
                    * inverse_jacobian[k][c]
                    * source_connection[i][j][k]
                    for i in source_coordinates
                    for j in source_coordinates
                    for k in source_coordinates
                )
                + sum(
                    jacobian[a][i] * inverse_hessian[i][b][c]
                    for i in source_coordinates
                )
                for c in target_coordinates
            }
            for b in target_coordinates
        }
        for a in target_coordinates
    }


def _riemann_transform(
    jacobian: Mapping[str, Mapping[str, float]],
    inverse_jacobian: Mapping[str, Mapping[str, float]],
    source_riemann: Mapping[str, Any],
    source_coordinates: Sequence[str],
    target_coordinates: Sequence[str],
) -> dict:
    return {
        a: {
            b: {
                c: {
                    d: sum(
                        jacobian[a][i]
                        * inverse_jacobian[j][b]
                        * inverse_jacobian[k][c]
                        * inverse_jacobian[l][d]
                        * source_riemann[i][j][k][l]
                        for i in source_coordinates
                        for j in source_coordinates
                        for k in source_coordinates
                        for l in source_coordinates
                    )
                    for d in target_coordinates
                }
                for c in target_coordinates
            }
            for b in target_coordinates
        }
        for a in target_coordinates
    }


def _ricci_transform(
    inverse_jacobian: Mapping[str, Mapping[str, float]],
    source_ricci: Mapping[str, Mapping[str, float]],
    source_coordinates: Sequence[str],
    target_coordinates: Sequence[str],
) -> dict:
    return {
        b: {
            d: sum(
                inverse_jacobian[j][b]
                * inverse_jacobian[l][d]
                * source_ricci[j][l]
                for j in source_coordinates
                for l in source_coordinates
            )
            for d in target_coordinates
        }
        for b in target_coordinates
    }


def _maximum_matrix_residual(left: dict, right: dict, rows: Sequence[str], columns: Sequence[str]) -> float:
    return max(
        (abs(left[row][column] - right[row][column]) for row in rows for column in columns),
        default=0.0,
    )


def _maximum_tensor3_residual(left: dict, right: dict, coordinates: Sequence[str]) -> float:
    return max(
        (
            abs(left[a][b][c] - right[a][b][c])
            for a in coordinates
            for b in coordinates
            for c in coordinates
        ),
        default=0.0,
    )


def _maximum_tensor4_residual(left: dict, right: dict, coordinates: Sequence[str]) -> float:
    return max(
        (
            abs(left[a][b][c][d] - right[a][b][c][d])
            for a in coordinates
            for b in coordinates
            for c in coordinates
            for d in coordinates
        ),
        default=0.0,
    )


