from __future__ import annotations

from typing import Any, Mapping


def revise_future_input(job: Mapping[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    return dict(job)


def reduce_future_scope(job: Mapping[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    return dict(job)
