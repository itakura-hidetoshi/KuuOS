from __future__ import annotations

from typing import Any, Mapping


def precheck_step(*, job: Mapping[str, Any], policy: Mapping[str, Any], spent_cost: float, maximum_cost: float) -> dict[str, Any]:
    return {"kind": "ready"}
