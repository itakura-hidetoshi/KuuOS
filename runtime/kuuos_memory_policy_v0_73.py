#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

VERSION = "kuuos_memory_evaluation_v0_73"


@dataclass(frozen=True)
class MemoryEvaluationPolicy:
    require_nonincrease: bool = True
    require_strict_decrease: bool = False
    tolerance: float = 1.0e-9

    def __post_init__(self) -> None:
        if self.tolerance < 0.0:
            raise ValueError("memory_evaluation_tolerance_invalid")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
