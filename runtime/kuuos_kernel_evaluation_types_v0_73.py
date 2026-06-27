#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class KernelCandidateEvaluation:
    candidate_id: str
    catalog_entry_digest: str
    deformation_digest: str
    candidate_kernel_digest: str
    candidate_connection_digest: str
    source_energy: float
    candidate_energy: float
    energy_nonincreasing: bool
    strict_energy_decrease: bool
    changed_term_count: int
    gauge_score_invariant: bool
    admissible: bool
    blockers: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return payload
