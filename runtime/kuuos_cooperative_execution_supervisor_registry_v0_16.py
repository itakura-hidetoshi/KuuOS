from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

Executor = Callable[[Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any]]


def resolve_executor(registry: Mapping[str, Executor], operation_id: str) -> Executor | None:
    executor = registry.get(str(operation_id))
    return executor if callable(executor) else None


def execute_allowlisted(*, registry: Mapping[str, Executor], operation_id: str, operation_input: Mapping[str, Any], execution_context: Mapping[str, Any]) -> dict[str, Any]:
    executor = resolve_executor(registry, operation_id)
    if executor is None:
        return {"outcome": "deterministic_bug", "summary": "Allowlisted operation is unavailable.", "error_kind": "deterministic_bug", "output": {}, "cost_units": 0.0, "checkpoint_payload": {}}
    raw = executor(dict(operation_input), dict(execution_context))
    result = dict(raw) if isinstance(raw, Mapping) else {}
    outcome = str(result.get("outcome", "success"))
    output = result.get("output", {})
    checkpoint = result.get("checkpoint_payload", {})
    return {
        "outcome": outcome,
        "summary": str(result.get("summary", "")),
        "error_kind": str(result.get("error_kind", "")),
        "output": dict(output) if isinstance(output, Mapping) else {"value": output},
        "cost_units": max(0.0, float(result.get("cost_units", 0.0) or 0.0)),
        "checkpoint_payload": dict(checkpoint) if isinstance(checkpoint, Mapping) else {},
        "external_dependency_ready": bool(result.get("external_dependency_ready", outcome != "waiting_external")),
        "user_input_required": bool(result.get("user_input_required", outcome == "needs_user_input")),
        "cancelled": bool(result.get("cancelled", outcome == "cancelled")),
    }
