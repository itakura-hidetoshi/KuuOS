#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_nonmarkov_memory_kernel_v0_72 import MemoryKernelDeformation

VERSION = "kuuos_finite_kernel_search_v0_73"
READY = "KERNEL_SEARCH_READY"
SOURCE_RETAINED = "KERNEL_SOURCE_RETAINED"
BLOCKED = "KERNEL_SEARCH_BLOCKED"


@dataclass(frozen=True)
class KernelCatalogEntry:
    candidate_id: str
    deformation: MemoryKernelDeformation

    def __post_init__(self) -> None:
        if not self.candidate_id:
            raise ValueError("kernel_candidate_id_missing")

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "deformation": self.deformation.to_dict(),
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class KernelSearchConfig:
    require_energy_nonincrease: bool = True
    require_strict_energy_decrease: bool = False
    tolerance: float = 1.0e-9

    def __post_init__(self) -> None:
        if self.tolerance < 0.0:
            raise ValueError("kernel_search_tolerance_invalid")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
