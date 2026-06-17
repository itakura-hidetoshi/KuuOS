from __future__ import annotations

from typing import Any, Mapping


def execute_ready_step(*, job: Mapping[str, Any], ready: Mapping[str, Any], registry: Mapping[str, Any], mode: str, spent_cost: float, maximum_cost: float) -> dict[str, Any]:
    return {"kind": "pause", "job": dict(job)}
