#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

VERSION = "indra_qi_bounded_generational_cycle_v0_12"
READY = "INDRA_QI_BOUNDED_GENERATIONAL_CYCLE_V0_12_READY"
BLOCKED = "INDRA_QI_BOUNDED_GENERATIONAL_CYCLE_V0_12_BLOCKED"


@dataclass(frozen=True)
class IndraQiBoundedCycleV0_12Result:
    version: str
    status: str
    packet_id: str
    runner_id: str
    generation_index: int
    completed_generations: int
    runner_status: str
    stop_reason: str
    transaction_committed: bool
    transaction_rolled_back: bool
    runner_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
