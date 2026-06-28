#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)
from runtime.kuuos_module_connection_v0_70 import (
    Matrix,
    ModuleConnection,
    matrix_mul,
    matrix_sub,
    matrix_transpose,
    signed_permutation_matrix,
)
from runtime.kuuos_noncommutative_differential_calculus_v0_71 import (
    InnerDifferentialCalculus,
    commutator,
)
from runtime.kuuos_state_module_v0_70 import KuuStateModule

VERSION = "kuuos_leibniz_module_connection_v0_71"
TOLERANCE = 1.0e-10
RectMatrix = tuple[tuple[float, ...], ...]


def rect_matrix(values: Iterable[Iterable[float]], rows: int, columns: int) -> RectMatrix:
    result = tuple(tuple(float(value) for value in row) for row in values)
    if len(result) != rows or any(len(row) != columns for row in result):
        raise ValueError("module_section_dimension_mismatch")
    return result


def rect_add(left: RectMatrix, right: RectMatrix) -> RectMatrix:
    return tuple(
        tuple(a + b for a, b in zip(left_row, right_row, strict=True))
        for left_row, right_row in zip(left, right, strict=True)
    )


def rect_sub(left: RectMatrix, right: RectMatrix) -> RectMatrix:
    return tuple(
        tuple(a - b for a, b in zip(left_row, right_row, strict=True))
        for left_row, right_row in zip(left, right, strict=True)
    )


def rect_norm_sq(value: RectMatrix) -> float:
    return sum(entry * entry for row in value for entry in row)


def rect_close(left: RectMatrix, right: RectMatrix, tolerance: float = TOLERANCE) -> bool:
    if len(left) != len(right):
        return False
    return all(
        abs(a - b) <= tolerance
        for left_row, right_row in zip(left, right, strict=True)
        for a, b in zip(left_row, right_row, strict=True)
    )


def left_action(algebra_element: Matrix, section: RectMatrix) -> RectMatrix:
    rows = len(algebra_element)
    columns = len(section[0])
    return tuple(
        tuple(
            sum(algebra_element[i][k] * section[k][j] for k in range(rows))
            for j in range(columns)
        )
        for i in range(rows)
    )


def right_action(section: RectMatrix, fiber_endomorphism: Matrix) -> RectMatrix:
    rows = len(section)
    rank = len(fiber_endomorphism)
    return tuple(
        tuple(
            sum(section[i][k] * fiber_endomorphism[k][j] for k in range(rank))
            for j in range(rank)
        )
        for i in range(rows)
    )


@dataclass(frozen=True)
class FreeLeftModuleSection:
    values: RectMatrix
    context_dimension: int
    module_rank: int

    def __post_init__(self) -> None:
        normalized = rect_matrix(self.values, self.context_dimension, self.module_rank)
        object.__setattr__(self, "values", normalized)

    def to_dict(self) -> dict[str, Any]:
        return {
            "values": [list(row) for row in self.values],
            "context_dimension": self.context_dimension,
            "module_rank": self.module_rank,
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class LeibnizModuleConnection:
    calculus_digest: str
    module_connection: ModuleConnection
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.calculus_digest:
            raise ValueError("leibniz_connection_calculus_digest_missing")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["module_connection"] = self.module_connection.to_dict()
        return payload

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())

    def require_compatible(
        self,
        calculus: InnerDifferentialCalculus,
        module: KuuStateModule,
    ) -> None:
        if calculus.digest != self.calculus_digest:
            raise ValueError("leibniz_connection_calculus_binding_mismatch")
        if self.module_connection.source_module_digest != module.digest:
            raise ValueError("leibniz_connection_module_binding_mismatch")
        if self.module_connection.connection_form.direction_labels != calculus.direction_labels:
            raise ValueError("leibniz_connection_direction_basis_mismatch")
        if self.module_connection.connection_form.module_rank != module.module_rank:
            raise ValueError("leibniz_connection_module_rank_mismatch")

    def apply(
        self,
        calculus: InnerDifferentialCalculus,
        direction_index: int,
        section: FreeLeftModuleSection,
    ) -> FreeLeftModuleSection:
        if calculus.digest != self.calculus_digest:
            raise ValueError("leibniz_connection_calculus_binding_mismatch")
        if section.context_dimension != calculus.dimension:
            raise ValueError("leibniz_connection_context_dimension_mismatch")
        if section.module_rank != self.module_connection.connection_form.module_rank:
            raise ValueError("leibniz_connection_section_rank_mismatch")
        try:
            generator = calculus.derivation_generators[direction_index]
            potential = self.module_connection.connection_form.components[direction_index]
        except IndexError as error:
            raise ValueError("leibniz_connection_direction_out_of_range") from error
        values = rect_add(
            left_action(generator, section.values),
            right_action(section.values, potential),
        )
        return FreeLeftModuleSection(values, section.context_dimension, section.module_rank)

    def gauge_transform(self, gauge: SignedPermutation) -> "LeibnizModuleConnection":
        return LeibnizModuleConnection(
            self.calculus_digest,
            self.module_connection.gauge_transform(gauge),
        )


def section_left_action(
    algebra_element: Matrix,
    section: FreeLeftModuleSection,
) -> FreeLeftModuleSection:
    return FreeLeftModuleSection(
        left_action(algebra_element, section.values),
        section.context_dimension,
        section.module_rank,
    )


def section_gauge_transform(
    section: FreeLeftModuleSection,
    gauge: SignedPermutation,
) -> FreeLeftModuleSection:
    if gauge.dimension != section.module_rank:
        raise ValueError("module_section_gauge_dimension_mismatch")
    inverse_matrix = matrix_transpose(signed_permutation_matrix(gauge))
    return FreeLeftModuleSection(
        right_action(section.values, inverse_matrix),
        section.context_dimension,
        section.module_rank,
    )


def leibniz_residual(
    connection: LeibnizModuleConnection,
    calculus: InnerDifferentialCalculus,
    direction_index: int,
    algebra_element: Matrix,
    section: FreeLeftModuleSection,
) -> RectMatrix:
    acted_section = section_left_action(algebra_element, section)
    left = connection.apply(calculus, direction_index, acted_section)
    derivative_term = section_left_action(
        calculus.derivative(direction_index, algebra_element),
        section,
    )
    transported = section_left_action(
        algebra_element,
        connection.apply(calculus, direction_index, section),
    )
    return rect_sub(left.values, rect_add(derivative_term.values, transported.values))


def satisfies_leibniz(
    connection: LeibnizModuleConnection,
    calculus: InnerDifferentialCalculus,
    direction_index: int,
    algebra_element: Matrix,
    section: FreeLeftModuleSection,
) -> bool:
    return rect_norm_sq(leibniz_residual(
        connection,
        calculus,
        direction_index,
        algebra_element,
        section,
    )) <= TOLERANCE


def connection_difference_action(
    source: LeibnizModuleConnection,
    candidate: LeibnizModuleConnection,
    calculus: InnerDifferentialCalculus,
    direction_index: int,
    section: FreeLeftModuleSection,
) -> FreeLeftModuleSection:
    source_value = source.apply(calculus, direction_index, section)
    candidate_value = candidate.apply(calculus, direction_index, section)
    return FreeLeftModuleSection(
        rect_sub(candidate_value.values, source_value.values),
        section.context_dimension,
        section.module_rank,
    )


def difference_is_left_module_linear(
    source: LeibnizModuleConnection,
    candidate: LeibnizModuleConnection,
    calculus: InnerDifferentialCalculus,
    direction_index: int,
    algebra_element: Matrix,
    section: FreeLeftModuleSection,
) -> bool:
    acted = section_left_action(algebra_element, section)
    left = connection_difference_action(
        source,
        candidate,
        calculus,
        direction_index,
        acted,
    )
    right = section_left_action(
        algebra_element,
        connection_difference_action(
            source,
            candidate,
            calculus,
            direction_index,
            section,
        ),
    )
    return rect_close(left.values, right.values)


def curvature_action(
    connection: LeibnizModuleConnection,
    calculus: InnerDifferentialCalculus,
    left_direction: int,
    right_direction: int,
    section: FreeLeftModuleSection,
) -> FreeLeftModuleSection:
    right_after_left = connection.apply(
        calculus,
        right_direction,
        connection.apply(calculus, left_direction, section),
    )
    left_after_right = connection.apply(
        calculus,
        left_direction,
        connection.apply(calculus, right_direction, section),
    )
    return FreeLeftModuleSection(
        rect_sub(right_after_left.values, left_after_right.values),
        section.context_dimension,
        section.module_rank,
    )


def curvature_representation_exact(
    connection: LeibnizModuleConnection,
    calculus: InnerDifferentialCalculus,
    left_direction: int,
    right_direction: int,
    section: FreeLeftModuleSection,
) -> bool:
    actual = curvature_action(
        connection,
        calculus,
        left_direction,
        right_direction,
        section,
    )
    components = connection.module_connection.connection_form.components
    fiber_curvature = commutator(
        components[left_direction],
        components[right_direction],
    )
    expected = FreeLeftModuleSection(
        right_action(section.values, fiber_curvature),
        section.context_dimension,
        section.module_rank,
    )
    return rect_close(actual.values, expected.values)


def gauge_covariant_on(
    connection: LeibnizModuleConnection,
    calculus: InnerDifferentialCalculus,
    direction_index: int,
    section: FreeLeftModuleSection,
    gauge: SignedPermutation,
) -> bool:
    transformed_connection = connection.gauge_transform(gauge)
    transformed_section = section_gauge_transform(section, gauge)
    left = transformed_connection.apply(calculus, direction_index, transformed_section)
    right = section_gauge_transform(
        connection.apply(calculus, direction_index, section),
        gauge,
    )
    return rect_close(left.values, right.values)
