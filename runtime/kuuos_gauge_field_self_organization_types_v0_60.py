#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
from typing import Any, Mapping, Protocol, Sequence, runtime_checkable

VERSION = "kuuos_gauge_field_self_organization_v0_60"


def canonical_digest(value: Any) -> str:
    if hasattr(value, "to_dict"):
        value = value.to_dict()
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _vector(values: Sequence[float], dimension: int) -> tuple[float, ...]:
    result = tuple(float(value) for value in values)
    if len(result) != dimension:
        raise ValueError(f"dimension_mismatch:{len(result)}!={dimension}")
    return result


@dataclass(frozen=True)
class SignedPermutation:
    """Finite orthogonal gauge element represented by a signed permutation.

    The convention is ``output[i] = signs[i] * input[permutation[i]]``.
    Signed permutations give an exact finite gauge group while keeping the
    runtime implementation dependency-free and replay deterministic.
    """

    permutation: tuple[int, ...]
    signs: tuple[int, ...]

    def __post_init__(self) -> None:
        dimension = len(self.permutation)
        if dimension == 0:
            raise ValueError("gauge_dimension_must_be_positive")
        if tuple(sorted(self.permutation)) != tuple(range(dimension)):
            raise ValueError("permutation_invalid")
        if len(self.signs) != dimension or any(sign not in {-1, 1} for sign in self.signs):
            raise ValueError("signs_invalid")

    @property
    def dimension(self) -> int:
        return len(self.permutation)

    @classmethod
    def identity(cls, dimension: int) -> "SignedPermutation":
        if dimension <= 0:
            raise ValueError("gauge_dimension_must_be_positive")
        return cls(tuple(range(dimension)), (1,) * dimension)

    def apply(self, values: Sequence[float]) -> tuple[float, ...]:
        vector = _vector(values, self.dimension)
        return tuple(float(self.signs[i]) * vector[self.permutation[i]] for i in range(self.dimension))

    def compose(self, other: "SignedPermutation") -> "SignedPermutation":
        """Return ``self ∘ other``."""
        if self.dimension != other.dimension:
            raise ValueError("gauge_dimension_mismatch")
        permutation = tuple(other.permutation[self.permutation[i]] for i in range(self.dimension))
        signs = tuple(self.signs[i] * other.signs[self.permutation[i]] for i in range(self.dimension))
        return SignedPermutation(permutation, signs)

    def inverse(self) -> "SignedPermutation":
        permutation = [0] * self.dimension
        signs = [1] * self.dimension
        for output_index, input_index in enumerate(self.permutation):
            permutation[input_index] = output_index
            signs[input_index] = self.signs[output_index]
        return SignedPermutation(tuple(permutation), tuple(signs))

    def fixes(self, coordinates: Sequence[int]) -> bool:
        return all(
            0 <= coordinate < self.dimension
            and self.permutation[coordinate] == coordinate
            and self.signs[coordinate] == 1
            for coordinate in coordinates
        )

    def normalized_trace(self) -> float:
        trace = sum(
            self.signs[index]
            for index in range(self.dimension)
            if self.permutation[index] == index
        )
        return float(trace) / float(self.dimension)

    def identity_defect(self) -> float:
        changed = sum(
            1
            for index in range(self.dimension)
            if self.permutation[index] != index or self.signs[index] != 1
        )
        return float(changed) / float(self.dimension)

    def to_dict(self) -> dict[str, Any]:
        return {
            "permutation": list(self.permutation),
            "signs": list(self.signs),
        }


@dataclass(frozen=True)
class ConstitutionalGaugeGroup:
    """Admissible finite gauge group fixing constitutional coordinates."""

    dimension: int
    protected_coordinates: tuple[int, ...]
    protected_labels: tuple[str, ...] = (
        "authority",
        "audit",
        "provenance",
        "rollback",
    )

    def __post_init__(self) -> None:
        if self.dimension <= 0:
            raise ValueError("gauge_dimension_must_be_positive")
        if len(set(self.protected_coordinates)) != len(self.protected_coordinates):
            raise ValueError("protected_coordinates_not_unique")
        if any(index < 0 or index >= self.dimension for index in self.protected_coordinates):
            raise ValueError("protected_coordinate_out_of_range")
        if len(self.protected_labels) != len(self.protected_coordinates):
            raise ValueError("protected_labels_dimension_mismatch")

    @classmethod
    def standard(cls, adaptive_dimension: int = 4) -> "ConstitutionalGaugeGroup":
        if adaptive_dimension < 1:
            raise ValueError("adaptive_dimension_must_be_positive")
        return cls(4 + adaptive_dimension, (0, 1, 2, 3))

    def identity(self) -> SignedPermutation:
        return SignedPermutation.identity(self.dimension)

    def is_admissible(self, element: SignedPermutation) -> bool:
        return element.dimension == self.dimension and element.fixes(self.protected_coordinates)

    def require_admissible(self, element: SignedPermutation) -> SignedPermutation:
        if not self.is_admissible(element):
            raise ValueError("constitutional_gauge_element_forbidden")
        return element

    def protected_projection(self, values: Sequence[float]) -> tuple[float, ...]:
        vector = _vector(values, self.dimension)
        return tuple(vector[index] for index in self.protected_coordinates)

    def to_dict(self) -> dict[str, Any]:
        return {
            "dimension": self.dimension,
            "protected_coordinates": list(self.protected_coordinates),
            "protected_labels": list(self.protected_labels),
        }


@runtime_checkable
class GaugeField(Protocol):
    field_id: str
    chart_id: str
    values: tuple[float, ...]
    owner: str
    authority_class: str

    def gauge_transform(self, element: SignedPermutation) -> "GaugeField": ...


@dataclass(frozen=True)
class AssociatedField:
    """A local section of an associated finite-dimensional bundle."""

    field_id: str
    chart_id: str
    values: tuple[float, ...]
    owner: str
    authority_class: str
    lineage_digest: str = ""

    def __post_init__(self) -> None:
        if not self.field_id:
            raise ValueError("field_id_missing")
        if not self.chart_id:
            raise ValueError("chart_id_missing")
        if not self.values:
            raise ValueError("field_values_missing")
        if not self.owner:
            raise ValueError("field_owner_missing")
        if not self.authority_class:
            raise ValueError("field_authority_class_missing")

    @property
    def dimension(self) -> int:
        return len(self.values)

    def norm_sq(self) -> float:
        return sum(value * value for value in self.values)

    def gauge_transform(self, element: SignedPermutation) -> "AssociatedField":
        if element.dimension != self.dimension:
            raise ValueError("gauge_dimension_mismatch")
        transformed = element.apply(self.values)
        return replace(
            self,
            values=transformed,
            lineage_digest=canonical_digest(
                {
                    "source": self.to_dict(),
                    "gauge_element": element.to_dict(),
                }
            ),
        )

    def with_values(self, values: Sequence[float], *, lineage: Mapping[str, Any]) -> "AssociatedField":
        return replace(
            self,
            values=_vector(values, self.dimension),
            lineage_digest=canonical_digest(lineage),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self) | {"values": list(self.values)}
