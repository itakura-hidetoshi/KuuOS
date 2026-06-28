#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class MemoryAssessment:
    member_id: str
    member_digest: str
    deformation_digest: str
    connection_digest: str
    source_score: float
    evaluated_score: float
    nonincreasing: bool
    strict_decrease: bool
    changed_term_count: int
    gauge_score_invariant: bool
    accepted: bool
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["issues"] = list(self.issues)
        return payload
