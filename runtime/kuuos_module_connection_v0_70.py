#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Sequence

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)

VERSION = "kuuos_module_connection_v0_70"
Matrix = tuple[tuple[float, ...], ...]


def matrix(values: Iterable[Iterable[float]], rank: int) -> Matrix:
    result = tuple(tuple(float(value) for value in row) for row in values)
    if len(result) != rank or any(len(row) != rank for row in result):
        raise ValueError("endomorphism_matrix_dimension_mismatch")
    return result


def zero_matrix(rank: int) -> Matrix:
    return tuple(tuple(0.0 for _ in range(rank)) for _ in range(rank))


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(a + b for a, b in zip(left_row, right_row, strict=True))
        for left_row, right_row in zip(left, right, strict=True)
    )


def matrix_sub(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(a - b for a, b in zip(left_row, right_row, strict=True))
        for left_row, right_row in zip(left, right, strict=True)
    )


def matrix_mul(left: Matrix, right: Matrix) -> Matrix:
    rank = len(left)
    return tuple(
        tuple(
            sum(left[i][k] * right[k][j] for k in range(rank))
            for j in range(rank)
        )
        for i in range(rank)
    )


def matrix_transpose(value: Matrix) -> Matrix:
    rank = len(value)
    return tuple(tuple(value[j][i] for j in range(rank)) for i in range(rank))


def matrix_norm_sq(value: Matrix) -> float:
    return sum(entry * entry for row in value for entry in row)


def signed_permutation_matrix(gauge: SignedPermutation) -> Matrix:
    rank = gauge.dimension
    return tuple(
        tuple(
            float(gauge.signs[i]) if j == gauge.permutation[i] else 0.0
            for j in range(rank)
        )
        for i in range(rank)
    )


def conjugate(value: Matrix, gauge: SignedPermutation) -> Matrix:
    gauge_matrix = signed_permutation_matrix(gauge)
    return matrix_mul(matrix_mul(gauge_matrix, value), matrix_transpose(gauge_matrix))


@dataclass(frozen=True)
class EndomorphismValuedOneForm:
    direction_labels: tuple[str, ...]
    components: tuple[Matrix, ...]
    module_rank: int

    def __post_init__(self) -> None:
        if self.module_rank <= 0:
            raise ValueError("one_form_module_rank_invalid")
        if not self.direction_labels:
            raise ValueError("one_form_direction_basis_empty")
        if len(set(self.direction_labels)) != len(self.direction_labels):
            raise ValueError("one_form_direction_basis_not_unique")
        if len(self.components) != len(self.direction_labels):
            raise ValueError("one_form_component_count_mismatch")
        normalized = tuple(matrix(component, self.module_rank) for component in self.components)
        object.__setattr__(self, "components", normalized)

    def to_dict(self) -> dict[str, Any]:
        return {
            "direction_labels": list(self.direction_labels),
            "components": [[list(row) for row in component] for component in self.components],
            "module_rank": self.module_rank,
        }

    def add(self, other: "EndomorphismValuedOneForm") -> "EndomorphismValuedOneForm":
        self.require_same_space(other)
        return EndomorphismValuedOneForm(
            self.direction_labels,
            tuple(matrix_add(left, right) for left, right in zip(self.components, other.components, strict=True)),
            self.module_rank,
        )

    def subtract(self, other: "EndomorphismValuedOneForm") -> "EndomorphismValuedOneForm":
        self.require_same_space(other)
        return EndomorphismValuedOneForm(
            self.direction_labels,
            tuple(matrix_sub(left, right) for left, right in zip(self.components, other.components, strict=True)),
            self.module_rank,
        )

    def gauge_transform(self, gauge: SignedPermutation) -> "EndomorphismValuedOneForm":
        if gauge.dimension != self.module_rank:
            raise ValueError("one_form_gauge_dimension_mismatch")
        return EndomorphismValuedOneForm(
            self.direction_labels,
            tuple(conjugate(component, gauge) for component in self.components),
            self.module_rank,
        )

    def require_same_space(self, other: "EndomorphismValuedOneForm") -> None:
        if self.module_rank != other.module_rank:
            raise ValueError("one_form_module_rank_mismatch")
        if self.direction_labels != other.direction_labels:
            raise ValueError("one_form_direction_basis_mismatch")


@dataclass(frozen=True)
class ModuleConnection:
    connection_form: EndomorphismValuedOneForm
    source_module_digest: str
    gauge_group_digest: str
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.source_module_digest:
            raise ValueError("connection_source_module_digest_missing")
        if not self.gauge_group_digest:
            raise ValueError("connection_gauge_group_digest_missing")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["connection_form"] = self.connection_form.to_dict()
        return payload

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())

    def gauge_transform(self, gauge: SignedPermutation) -> "ModuleConnection":
        return ModuleConnection(
            self.connection_form.gauge_transform(gauge),
            self.source_module_digest,
            self.gauge_group_digest,
        )


def curvature_components(connection: ModuleConnection) -> tuple[Matrix, ...]:
    components = connection.connection_form.components
    values: list[Matrix] = []
    for left_index in range(len(components)):
        for right_index in range(left_index + 1, len(components)):
            left = matrix_mul(components[left_index], components[right_index])
            right = matrix_mul(components[right_index], components[left_index])
            values.append(matrix_sub(left, right))
    return tuple(values)


def curvature_observable(connection: ModuleConnection) -> float:
    return round(sum(matrix_norm_sq(value) for value in curvature_components(connection)), 12)
