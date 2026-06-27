#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_context_algebra_v0_70"


@dataclass(frozen=True)
class ContextAlgebra:
    """Finite presentation of the context algebra and its differential basis.

    The runtime model stores only the canonical algebra identity and the basis
    of one-form directions.  It does not introduce graph vertices or edges.
    """

    algebra_id: str
    differential_directions: tuple[str, ...]
    noncommutative: bool = False
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.algebra_id:
            raise ValueError("context_algebra_id_missing")
        if not self.differential_directions:
            raise ValueError("context_differential_basis_empty")
        if len(set(self.differential_directions)) != len(self.differential_directions):
            raise ValueError("context_differential_basis_not_unique")
        if any(not direction for direction in self.differential_directions):
            raise ValueError("context_differential_direction_missing")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["differential_directions"] = list(self.differential_directions)
        return payload

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())
