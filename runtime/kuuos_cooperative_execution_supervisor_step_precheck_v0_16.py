from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, mapping
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import next_step


def precheck_step(*, job: Mapping[str, Any], policy: Mapping[str, Any], spent_cost: float, maximum_cost: float) -> dict[str, Any]:
    step = next_step(job)
    if step is None:
        return {"kind": "complete", "step": None, "policy": dict(policy)}
    estimate = max(0.0, float(step.get("estimated_cost_units", 0.0) or 0.0))
    if estimate > maximum_cost and spent_cost <= 0.0:
        return {
            "kind": "pause",
            "step": step,
            "phase": "slice_cost_bound",
            "result": {
                "outcome": "deterministic_bug",
                "error_kind": "invariant_violation",
                "summary": "The next step estimate exceeds the configured maximum cost per slice.",
            },
            "policy": dict(policy),
        }
    if spent_cost + estimate > maximum_cost:
        return {"kind": "yield", "step": step, "policy": dict(policy)}
    remaining = max(0.0, float(job.get("remaining_budget_units", 0.0) or 0.0))
    if estimate > remaining:
        return {"kind": "pause", "step": step, "phase": "budget_precheck", "result": None, "policy": dict(policy)}
    required_permission = str(step.get("required_permission", ""))
    permissions = {str(item) for item in as_list(job.get("granted_permissions"))}
    if required_permission and required_permission not in permissions:
        return {
            "kind": "pause",
            "step": step,
            "phase": "permission_precheck",
            "result": {"outcome": "permission_denied", "summary": f"Required permission is not granted: {required_permission}"},
            "policy": dict(policy),
        }
    return {"kind": "ready", "step": step, "estimate": estimate, "attempt": 1, "policy": dict(policy)}
