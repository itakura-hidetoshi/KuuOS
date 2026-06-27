#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any, Sequence

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    AssociatedField,
    ConstitutionalGaugeGroup,
    SignedPermutation,
)

VERSION = "kuuos_os_associated_gauge_fields_v0_61"
OS_ROLES = ("observe", "verify", "memory")


@dataclass(frozen=True)
class GaugeChannelLayout:
    """Fixed decomposition of the adaptive fiber into invariant channels."""

    protected: tuple[int, ...] = (0, 1, 2, 3)
    epistemic: tuple[int, ...] = (4, 5, 6)
    verification: tuple[int, ...] = (7, 8)
    memory: tuple[int, ...] = (9, 10, 11)

    def __post_init__(self) -> None:
        blocks = (self.protected, self.epistemic, self.verification, self.memory)
        flattened = tuple(index for block in blocks for index in block)
        if not all(block for block in blocks):
            raise ValueError("gauge_channel_empty")
        if len(flattened) != len(set(flattened)):
            raise ValueError("gauge_channel_overlap")
        if tuple(sorted(flattened)) != tuple(range(len(flattened))):
            raise ValueError("gauge_channel_partition_invalid")

    @property
    def dimension(self) -> int:
        return sum(len(block) for block in (
            self.protected,
            self.epistemic,
            self.verification,
            self.memory,
        ))

    def channel(self, name: str) -> tuple[int, ...]:
        if name not in {"protected", "epistemic", "verification", "memory"}:
            raise KeyError(f"gauge_channel_unknown:{name}")
        return tuple(getattr(self, name))

    def to_dict(self) -> dict[str, Any]:
        return {
            "protected": list(self.protected),
            "epistemic": list(self.epistemic),
            "verification": list(self.verification),
            "memory": list(self.memory),
            "dimension": self.dimension,
        }


@dataclass(frozen=True)
class ChannelPreservingGaugeGroup:
    """Constitutional gauge group preserving each semantic channel as a set."""

    layout: GaugeChannelLayout = GaugeChannelLayout()
    protected_labels: tuple[str, ...] = (
        "authority",
        "audit",
        "provenance",
        "rollback",
    )

    def __post_init__(self) -> None:
        if len(self.protected_labels) != len(self.layout.protected):
            raise ValueError("protected_labels_dimension_mismatch")

    @property
    def dimension(self) -> int:
        return self.layout.dimension

    @property
    def protected_coordinates(self) -> tuple[int, ...]:
        return self.layout.protected

    @property
    def base_group(self) -> ConstitutionalGaugeGroup:
        return ConstitutionalGaugeGroup(
            self.dimension,
            self.protected_coordinates,
            self.protected_labels,
        )

    def identity(self) -> SignedPermutation:
        return SignedPermutation.identity(self.dimension)

    def is_admissible(self, element: SignedPermutation) -> bool:
        if not self.base_group.is_admissible(element):
            return False
        for name in ("epistemic", "verification", "memory"):
            block = set(self.layout.channel(name))
            if {element.permutation[index] for index in block} != block:
                return False
        return True

    def require_admissible(self, element: SignedPermutation) -> SignedPermutation:
        if not self.is_admissible(element):
            raise ValueError("os_channel_gauge_element_forbidden")
        return element

    def protected_projection(self, values: Sequence[float]) -> tuple[float, ...]:
        return self.base_group.protected_projection(values)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "channel_preserving_constitutional_gauge_group",
            "layout": self.layout.to_dict(),
            "protected_labels": list(self.protected_labels),
        }


def _unit(value: float, name: str) -> float:
    number = float(value)
    if number < 0.0 or number > 1.0:
        raise ValueError(f"{name}_unit_interval_required")
    return number


def os_field_values(
    *,
    evidence_support: float,
    uncertainty: float,
    contradiction: float,
    criterion_coverage: float,
    verification_debt: float,
    history_depth: float,
    residue_load: float,
    predictive_uncertainty: float,
) -> tuple[float, ...]:
    return (
        1.0,
        1.0,
        1.0,
        1.0,
        _unit(evidence_support, "evidence_support"),
        _unit(uncertainty, "uncertainty"),
        _unit(contradiction, "contradiction"),
        _unit(criterion_coverage, "criterion_coverage"),
        _unit(verification_debt, "verification_debt"),
        _unit(history_depth, "history_depth"),
        _unit(residue_load, "residue_load"),
        _unit(predictive_uncertainty, "predictive_uncertainty"),
    )


@dataclass(frozen=True)
class OSAssociatedGaugeField:
    role: str
    source_version: str
    source_digest: str
    boundary_digest: str
    field: AssociatedField

    def __post_init__(self) -> None:
        if self.role not in OS_ROLES:
            raise ValueError("os_gauge_field_role_invalid")
        if not self.source_version:
            raise ValueError("os_gauge_field_source_version_missing")
        if not self.source_digest:
            raise ValueError("os_gauge_field_source_digest_missing")
        if not self.boundary_digest:
            raise ValueError("os_gauge_field_boundary_digest_missing")
        if self.field.dimension != GaugeChannelLayout().dimension:
            raise ValueError("os_gauge_field_dimension_invalid")

    @property
    def chart_id(self) -> str:
        return self.field.chart_id

    @property
    def values(self) -> tuple[float, ...]:
        return self.field.values

    def gauge_transform(self, element: SignedPermutation) -> "OSAssociatedGaugeField":
        return replace(self, field=self.field.gauge_transform(element))

    def channel_values(
        self,
        name: str,
        layout: GaugeChannelLayout = GaugeChannelLayout(),
    ) -> tuple[float, ...]:
        return tuple(self.values[index] for index in layout.channel(name))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["field"] = self.field.to_dict()
        return payload
