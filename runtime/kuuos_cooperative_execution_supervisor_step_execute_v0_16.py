from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, mapping
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import next_step, reseal_job
from runtime.kuuos_cooperative_execution_supervisor_receipts_v0_16 import build_step_receipt
from runtime.kuuos_cooperative_execution_supervisor_registry_v0_16 import Executor, execute_allowlisted
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import execution_key


def execute_ready_step(*, job: Mapping[str, Any], ready: Mapping[str, Any], registry: Mapping[str, Executor], mode: str, spent_cost: float, maximum_cost: float) -> dict[str, Any]:
    work = deepcopy(dict(job))
    step = dict(mapping(ready.get("step")))
    step_id = str(step.get("step_id", ""))
    attempt = max(1, int(ready.get("attempt", 1) or 1))
    attempts = dict(mapping(work.get("step_attempts")))
    attempts[step_id] = attempt
    work["step_attempts"] = attempts
    key_digest = execution_key(
        job_id=str(work.get("job_id", "")),
        manifest=str(work.get("manifest_digest", "")),
        step_id=step_id,
        attempt=attempt,
    )
    try:
        result = execute_allowlisted(
            registry=registry,
            operation_id=str(step.get("operation_id", "")),
            operation_input=mapping(step.get("operation_input")),
            execution_context={
                "job_id": work.get("job_id", ""),
                "step_id": step_id,
                "attempt": attempt,
                "execution_key": key_digest,
                "execution_mode": mode,
                "source_job_state_digest": job.get("job_state_digest", ""),
            },
        )
    except Exception as error:
        result = {
            "outcome": "deterministic_bug",
            "error_kind": "deterministic_bug",
            "summary": f"Trusted executor raised {type(error).__name__}.",
            "output": {},
            "cost_units": 0.0,
            "checkpoint_payload": {},
        }
    if str(result.get("outcome", "")) != "success":
        return {
            "kind": "pause",
            "job": work,
            "step": step,
            "phase": "step_result",
            "result": result,
            "policy": dict(ready.get("policy", {})),
        }
    estimate = max(0.0, float(ready.get("estimate", 0.0) or 0.0))
    actual_cost = max(0.0, float(result.get("cost_units", estimate) or 0.0))
    receipt = build_step_receipt(
        job=work,
        step=step,
        attempt=attempt,
        execution_key=key_digest,
        result=result,
    )
    receipts = [dict(mapping(item)) for item in as_list(work.get("step_receipts"))]
    receipts.append(receipt)
    work["step_receipts"] = receipts
    completed = [str(item) for item in as_list(work.get("completed_step_ids"))]
    completed.append(step_id)
    work["completed_step_ids"] = completed
    work["current_step_index"] = int(work.get("current_step_index", 0) or 0) + 1
    remaining = max(0.0, float(work.get("remaining_budget_units", 0.0) or 0.0))
    work["remaining_budget_units"] = max(0.0, remaining - actual_cost)
    work = reseal_job(work)
    if actual_cost > estimate and spent_cost + actual_cost > maximum_cost:
        return {
            "kind": "success_then_pause",
            "job": work,
            "step": next_step(work),
            "phase": "reported_cost_overrun",
            "result": {
                "outcome": "deterministic_bug",
                "error_kind": "invariant_violation",
                "summary": "A completed step reported cost beyond the bounded slice allowance.",
            },
            "policy": dict(ready.get("policy", {})),
            "receipt": receipt,
            "cost": actual_cost,
            "step_id": step_id,
        }
    return {
        "kind": "success",
        "job": work,
        "receipt": receipt,
        "cost": actual_cost,
        "step_id": step_id,
    }
