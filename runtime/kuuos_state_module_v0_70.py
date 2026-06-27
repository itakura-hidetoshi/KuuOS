#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)

VERSION = "kuuos_state_module_v0_70"
REQUIRED_CHANNELS = ("observe", "verify", "memory", "ethics")


def _normalized_coordinates(values: Iterable[int], rank: int, *, label: str) -> tuple[int, ...]:
    coordinates = tuple(sorted(int(value) for value in values))
    if len(set(coordinates)) != len(coordinates):
        raise ValueError(f"{label}_coordinates_not_unique")
    if any(value < 0 or value >= rank for value in coordinates):
        raise ValueError(f"{label}_coordinate_out_of_range")
    return coordinates


@dataclass(frozen=True)
class Projector:
    label: str
    coordinates: tuple[int, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"label": self.label, "coordinates": list(self.coordinates)}


@dataclass(frozen=True)
class SubmoduleSpec:
    label: str
    coordinates: tuple[int, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"label": self.label, "coordinates": list(self.coordinates)}


@dataclass(frozen=True)
class KuuStateModule:
    algebra_digest: str
    module_rank: int
    semantic_projectors: tuple[Projector, ...]
    authority_filtration: tuple[SubmoduleSpec, ...]
    protected_projector: Projector
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.algebra_digest:
            raise ValueError("state_module_algebra_digest_missing")
        if self.module_rank <= 0:
            raise ValueError("state_module_rank_invalid")

        protected = Projector(
            self.protected_projector.label,
            _normalized_coordinates(
                self.protected_projector.coordinates,
                self.module_rank,
                label="protected",
            ),
        )
        if protected.label != "protected":
            raise ValueError("protected_projector_label_invalid")

        projectors: list[Projector] = []
        seen_labels: set[str] = set()
        occupied = set(protected.coordinates)
        for raw in self.semantic_projectors:
            if raw.label in seen_labels:
                raise ValueError("semantic_projector_label_duplicate")
            coordinates = _normalized_coordinates(
                raw.coordinates,
                self.module_rank,
                label=f"semantic_{raw.label}",
            )
            if occupied.intersection(coordinates):
                raise ValueError("semantic_projectors_overlap")
            occupied.update(coordinates)
            seen_labels.add(raw.label)
            projectors.append(Projector(raw.label, coordinates))
        if tuple(sorted(seen_labels)) != tuple(sorted(REQUIRED_CHANNELS)):
            raise ValueError("semantic_projector_channels_incomplete")
        if occupied != set(range(self.module_rank)):
            raise ValueError("module_direct_sum_not_total")

        filtration: list[SubmoduleSpec] = []
        previous: set[int] = set()
        for raw in self.authority_filtration:
            coordinates = set(_normalized_coordinates(
                raw.coordinates,
                self.module_rank,
                label=f"filtration_{raw.label}",
            ))
            if not previous.issubset(coordinates):
                raise ValueError("authority_filtration_not_nested")
            previous = coordinates
            filtration.append(SubmoduleSpec(raw.label, tuple(sorted(coordinates))))
        if not filtration or set(filtration[-1].coordinates) != set(range(self.module_rank)):
            raise ValueError("authority_filtration_not_exhaustive")
        if not set(protected.coordinates).issubset(set(filtration[0].coordinates)):
            raise ValueError("protected_not_in_lowest_authority_level")

        object.__setattr__(self, "protected_projector", protected)
        object.__setattr__(self, "semantic_projectors", tuple(projectors))
        object.__setattr__(self, "authority_filtration", tuple(filtration))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["semantic_projectors"] = [item.to_dict() for item in self.semantic_projectors]
        payload["authority_filtration"] = [item.to_dict() for item in self.authority_filtration]
        payload["protected_projector"] = self.protected_projector.to_dict()
        return payload

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())

    def all_projectors(self) -> tuple[Projector, ...]:
        return (self.protected_projector,) + self.semantic_projectors

    def is_admissible_gauge(self, gauge: SignedPermutation) -> bool:
        if gauge.dimension != self.module_rank:
            return False
        if not gauge.fixes(self.protected_projector.coordinates):
            return False
        for projector in self.semantic_projectors:
            image = {gauge.permutation[index] for index in projector.coordinates}
            if image != set(projector.coordinates):
                return False
        for level in self.authority_filtration:
            image = {gauge.permutation[index] for index in level.coordinates}
            if image != set(level.coordinates):
                return False
        return True
