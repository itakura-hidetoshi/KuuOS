from __future__ import annotations

from typing import Any, Mapping


def run_supervisor_slice(*, job: Mapping[str, Any], slice_id: str, mode: str, policy: Mapping[str, Any], registry: Mapping[str, Any]) -> dict[str, Any]:
    return {"slice_id": slice_id}
