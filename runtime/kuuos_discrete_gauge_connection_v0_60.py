#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    AssociatedField,
    ConstitutionalGaugeGroup,
    SignedPermutation,
)

ChartPair = tuple[str, str]
Plaquette = tuple[str, str, str, str]


def distance_sq(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("field_dimension_mismatch")
    return sum((float(a) - float(b)) ** 2 for a, b in zip(left, right, strict=True))


@dataclass(frozen=True)
class KuuConnection:
    group: ConstitutionalGaugeGroup
    transports: Mapping[ChartPair, SignedPermutation]

    def __post_init__(self) -> None:
        normalized: dict[ChartPair, SignedPermutation] = {}
        for raw_pair, element in self.transports.items():
            source, target = str(raw_pair[0]), str(raw_pair[1])
            if not source or not target or source == target:
                raise ValueError("chart_pair_invalid")
            self.group.require_admissible(element)
            reverse = normalized.get((target, source))
            if reverse is not None and reverse != element.inverse():
                raise ValueError("reverse_transport_inconsistent")
            normalized[(source, target)] = element
        object.__setattr__(self, "transports", normalized)

    def transport_element(self, source: str, target: str) -> SignedPermutation:
        if source == target:
            return self.group.identity()
        direct = self.transports.get((source, target))
        if direct is not None:
            return direct
        reverse = self.transports.get((target, source))
        if reverse is not None:
            return reverse.inverse()
        raise KeyError(f"transport_missing:{source}->{target}")

    def transport(self, source: str, target: str, values: Sequence[float]) -> tuple[float, ...]:
        return self.transport_element(source, target).apply(values)

    def oriented_pairs(self) -> tuple[ChartPair, ...]:
        pairs = {
            (source, target) if source < target else (target, source)
            for source, target in self.transports
        }
        return tuple(sorted(pairs))

    def path_transport(self, path: Sequence[str]) -> SignedPermutation:
        if not path:
            raise ValueError("path_empty")
        total = self.group.identity()
        for source, target in zip(path, path[1:], strict=False):
            total = self.transport_element(source, target).compose(total)
        return total

    def plaquette_holonomy(self, plaquette: Plaquette) -> SignedPermutation:
        x0, x1, x2, x3 = plaquette
        return self.path_transport((x0, x1, x2, x3, x0))

    def wilson_observable(self, plaquette: Plaquette) -> float:
        return self.plaquette_holonomy(plaquette).normalized_trace()

    def curvature_defect(self, plaquette: Plaquette) -> float:
        return self.plaquette_holonomy(plaquette).identity_defect()

    def gauge_transform(self, local_gauges: Mapping[str, SignedPermutation]) -> "KuuConnection":
        identity = self.group.identity()
        transformed: dict[ChartPair, SignedPermutation] = {}
        for source, target in self.transports:
            source_gauge = self.group.require_admissible(local_gauges.get(source, identity))
            target_gauge = self.group.require_admissible(local_gauges.get(target, identity))
            transformed[(source, target)] = target_gauge.compose(
                self.transports[(source, target)]
            ).compose(source_gauge.inverse())
        return KuuConnection(self.group, transformed)

    def to_dict(self) -> dict[str, Any]:
        return {
            "group": self.group.to_dict(),
            "transports": [
                {"source": source, "target": target, "element": element.to_dict()}
                for (source, target), element in sorted(self.transports.items())
            ],
        }


@dataclass(frozen=True)
class GaugeAction:
    curvature_energy: float
    matter_energy: float
    total: float
    plaquette_count: int
    transport_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def gauge_action(
    connection: KuuConnection,
    fields: Mapping[str, AssociatedField],
    plaquettes: Sequence[Plaquette] = (),
) -> GaugeAction:
    curvature = sum(connection.curvature_defect(p) ** 2 for p in plaquettes)
    matter = 0.0
    count = 0
    for source, target in connection.oriented_pairs():
        if source in fields and target in fields:
            matter += distance_sq(connection.transport(source, target, fields[source].values), fields[target].values)
            count += 1
    return GaugeAction(round(curvature, 12), round(matter, 12), round(curvature + matter, 12), len(plaquettes), count)
