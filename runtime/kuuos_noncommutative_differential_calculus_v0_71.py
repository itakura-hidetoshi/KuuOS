#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_module_connection_v0_70 import (
    Matrix,
    matrix,
    matrix_add,
    matrix_mul,
    matrix_norm_sq,
    matrix_sub,
)

VERSION = "kuuos_noncommutative_differential_calculus_v0_71"
TOLERANCE = 1.0e-12


def matrix_close(left: Matrix, right: Matrix, tolerance: float = TOLERANCE) -> bool:
    if len(left) != len(right):
        return False
    return all(
        abs(a - b) <= tolerance
        for left_row, right_row in zip(left, right, strict=True)
        for a, b in zip(left_row, right_row, strict=True)
    )


def commutator(left: Matrix, right: Matrix) -> Matrix:
    return matrix_sub(matrix_mul(left, right), matrix_mul(right, left))


@dataclass(frozen=True)
class InnerDifferentialCalculus:
    """Finite matrix-algebra differential calculus.

    The context algebra is the noncommutative matrix algebra M_n(R).  Each
    differential direction is the inner derivation delta_i(a) = [H_i, a].
    Direction generators are required to commute so that the represented
    first-order differential directions commute while the algebra itself may
    remain noncommutative.
    """

    algebra_id: str
    dimension: int
    direction_labels: tuple[str, ...]
    derivation_generators: tuple[Matrix, ...]
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.algebra_id:
            raise ValueError("calculus_algebra_id_missing")
        if self.dimension <= 0:
            raise ValueError("calculus_dimension_invalid")
        if not self.direction_labels:
            raise ValueError("calculus_direction_basis_empty")
        if len(set(self.direction_labels)) != len(self.direction_labels):
            raise ValueError("calculus_direction_basis_not_unique")
        if len(self.direction_labels) != len(self.derivation_generators):
            raise ValueError("calculus_generator_count_mismatch")
        normalized = tuple(
            matrix(generator, self.dimension)
            for generator in self.derivation_generators
        )
        for left_index in range(len(normalized)):
            for right_index in range(left_index + 1, len(normalized)):
                if matrix_norm_sq(commutator(
                    normalized[left_index],
                    normalized[right_index],
                )) > TOLERANCE:
                    raise ValueError("calculus_derivations_do_not_commute")
        object.__setattr__(self, "derivation_generators", normalized)

    def to_dict(self) -> dict[str, Any]:
        return {
            "algebra_id": self.algebra_id,
            "dimension": self.dimension,
            "direction_labels": list(self.direction_labels),
            "derivation_generators": [
                [list(row) for row in generator]
                for generator in self.derivation_generators
            ],
            "version": self.version,
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())

    def require_element(self, value: Matrix) -> Matrix:
        return matrix(value, self.dimension)

    def derivative(self, direction_index: int, value: Matrix) -> Matrix:
        element = self.require_element(value)
        try:
            generator = self.derivation_generators[direction_index]
        except IndexError as error:
            raise ValueError("calculus_direction_out_of_range") from error
        return commutator(generator, element)

    def leibniz_residual(
        self,
        direction_index: int,
        left: Matrix,
        right: Matrix,
    ) -> Matrix:
        left = self.require_element(left)
        right = self.require_element(right)
        product = matrix_mul(left, right)
        return matrix_sub(
            self.derivative(direction_index, product),
            matrix_add(
                matrix_mul(self.derivative(direction_index, left), right),
                matrix_mul(left, self.derivative(direction_index, right)),
            ),
        )

    def satisfies_leibniz(
        self,
        direction_index: int,
        left: Matrix,
        right: Matrix,
    ) -> bool:
        return matrix_norm_sq(self.leibniz_residual(direction_index, left, right)) <= TOLERANCE

    def directions_commute_on(self, value: Matrix) -> bool:
        element = self.require_element(value)
        for left_index in range(len(self.direction_labels)):
            for right_index in range(left_index + 1, len(self.direction_labels)):
                left_then_right = self.derivative(
                    right_index,
                    self.derivative(left_index, element),
                )
                right_then_left = self.derivative(
                    left_index,
                    self.derivative(right_index, element),
                )
                if not matrix_close(left_then_right, right_then_left):
                    return False
        return True

    def is_noncommutative_witness(self, left: Matrix, right: Matrix) -> bool:
        left = self.require_element(left)
        right = self.require_element(right)
        return not matrix_close(matrix_mul(left, right), matrix_mul(right, left))
