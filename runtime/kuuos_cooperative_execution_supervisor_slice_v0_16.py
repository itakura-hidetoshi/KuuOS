from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_cooperative_execution_supervisor_handoff_v0_16 import (
    build_background_continuation,
    build_completion_handoff,
    build_progress_checkpoint,
)
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import next_step, reseal_job, validate_job
from runtime.kuuos_cooperative_execution_supervisor_receipts_v0_16 import build_foreground_yield
from runtime.kuuos_cooperative_execution_supervisor_registry_v0_16 import Executor
from runtime.kuuos_cooperative_execution_supervisor_slice_result_v0_16 import finish_slice, pause_slice
from runtime.kuuos_cooperative_execution_supervisor_step_execute_v0_16 import execute_ready_step
from runtime.kuuos_cooperative_execution_supervisor_step_precheck_v0_16 import precheck_step


def run_supervisor_slice(*, job: Mapping[str, Any], slice_id: str, mode: str, policy: Mapping[str, Any], registry: Mapping[str, Executor]) -> dict[str, Any]:
    validate_job(job)
    if mode not in {"foreground", "background"}:
        raise ValueError("execution_mode_invalid")
    key = str(slice_id).strip()
    if not key:
        raise ValueError("slice_id_missing")
    if str(job.get("supervisor_state", "")) in {"completed", "cancelled"}:
        raise ValueError("terminal_job_cannot_run")

    source_digest = str(job.get("job_state_digest", ""))
    work = deepcopy(dict(job))
    work["execution_mode"] = mode
    work["supervisor_state"] = "foreground_running" if mode == "foreground" else "background_leased"
    maximum_steps = max(1, int(policy.get("max_steps_per_slice", 1) or 1))
    raw_maximum_cost = policy.get("max_cost_per_slice")
    maximum_cost = max(
        0.0,
        float(work.get("remaining_budget_units", 0.0) if raw_maximum_cost is None else raw_maximum_cost),
    )
    completed_in_slice: list[str] = []
    new_receipts: list[dict[str, Any]] = []
    spent_cost = 0.0

    while len(completed_in_slice) < maximum_steps:
        ready = precheck_step(
            job=work,
            policy=policy,
            spent_cost=spent_cost,
            maximum_cost=maximum_cost,
        )
        kind = str(ready.get("kind", "pause"))
        if kind == "complete":
            break
        if kind == "yield":
            break
        if kind == "pause":
            return pause_slice(
                work=work,
                slice_id=key,
                source_digest=source_digest,
                mode=mode,
                policy=dict(ready.get("policy", policy)),
                step=ready.get("step") if isinstance(ready.get("step"), Mapping) else None,
                result=ready.get("result") if isinstance(ready.get("result"), Mapping) else None,
                completed_in_slice=completed_in_slice,
                new_receipts=new_receipts,
                spent_cost=spent_cost,
                phase=str(ready.get("phase", "precheck")),
            )

        outcome = execute_ready_step(
            job=work,
            ready=ready,
            registry=registry,
            mode=mode,
            spent_cost=spent_cost,
            maximum_cost=maximum_cost,
        )
        outcome_kind = str(outcome.get("kind", "pause"))
        if outcome_kind in {"pause", "success_then_pause"}:
            if outcome_kind == "success_then_pause":
                receipt = outcome.get("receipt")
                if isinstance(receipt, Mapping):
                    new_receipts.append(dict(receipt))
                step_id = str(outcome.get("step_id", ""))
                if step_id:
                    completed_in_slice.append(step_id)
                spent_cost += max(0.0, float(outcome.get("cost", 0.0) or 0.0))
            return pause_slice(
                work=outcome.get("job", work) if isinstance(outcome.get("job", work), Mapping) else work,
                slice_id=key,
                source_digest=source_digest,
                mode=mode,
                policy=dict(outcome.get("policy", policy)),
                step=outcome.get("step") if isinstance(outcome.get("step"), Mapping) else None,
                result=outcome.get("result") if isinstance(outcome.get("result"), Mapping) else None,
                completed_in_slice=completed_in_slice,
                new_receipts=new_receipts,
                spent_cost=spent_cost,
                phase=str(outcome.get("phase", "step_result")),
            )
        if outcome_kind != "success":
            raise ValueError("step_outcome_invalid")
        work = deepcopy(dict(outcome["job"]))
        receipt = outcome.get("receipt")
        if isinstance(receipt, Mapping):
            new_receipts.append(dict(receipt))
        step_id = str(outcome.get("step_id", ""))
        if step_id:
            completed_in_slice.append(step_id)
        spent_cost += max(0.0, float(outcome.get("cost", 0.0) or 0.0))

    remaining_step = next_step(work)
    if remaining_step is None:
        work["supervisor_state"] = "completed"
        work = reseal_job(work)
        handoff = build_completion_handoff(
            job=work,
            attempt_id=f"{key}:completed",
            policy=policy,
            mode=mode,
        )
        work["latest_checkpoint_digest"] = str(handoff.get("checkpoint_digest", ""))
        work["latest_feedback_digest"] = str(handoff.get("feedback_digest", ""))
        work["active_continuation_ticket"] = {}
        work = reseal_job(work)
        return finish_slice(
            slice_id=key,
            source_digest=source_digest,
            mode=mode,
            job=work,
            completed_in_slice=completed_in_slice,
            new_receipts=new_receipts,
            spent_cost=spent_cost,
            handoff=handoff,
        )

    if mode == "foreground":
        work["supervisor_state"] = "foreground_yielded"
        work["active_continuation_ticket"] = {}
        work = reseal_job(work)
        checkpoint = build_progress_checkpoint(
            job=work,
            attempt_id=f"{key}:yield",
            phase="foreground_slice_complete",
            next_step=remaining_step,
            policy=policy,
            mode=mode,
        )
        work["latest_checkpoint_digest"] = str(checkpoint.get("checkpoint_digest", ""))
        work = reseal_job(work)
        yield_receipt = build_foreground_yield(
            job=work,
            source_job_state_digest=source_digest,
            completed_in_slice=completed_in_slice,
            next_step=remaining_step,
            checkpoint_digest=str(checkpoint.get("checkpoint_digest", "")),
            background_supported=bool(policy.get("background_worker_available", False)),
        )
        return finish_slice(
            slice_id=key,
            source_digest=source_digest,
            mode=mode,
            job=work,
            completed_in_slice=completed_in_slice,
            new_receipts=new_receipts,
            spent_cost=spent_cost,
            yield_receipt=yield_receipt,
        )

    work["supervisor_state"] = "background_queued"
    work = reseal_job(work)
    continuation = build_background_continuation(
        job=work,
        attempt_id=f"{key}:background-yield",
        next_step=remaining_step,
        policy=policy,
    )
    work["latest_checkpoint_digest"] = str(continuation["checkpoint"].get("checkpoint_digest", ""))
    work["latest_feedback_digest"] = str(continuation["feedback"].get("feedback_digest", ""))
    work["active_continuation_ticket"] = dict(continuation.get("background_ticket", {}))
    work = reseal_job(work)
    handoff = {
        "execution_state": "background_queued",
        "reason_code": "cooperative_slice_complete",
        "checkpoint": continuation["checkpoint"],
        "feedback": continuation["feedback"],
        "background_ticket": continuation["background_ticket"],
        "checkpoint_digest": continuation["checkpoint"].get("checkpoint_digest", ""),
        "feedback_digest": continuation["feedback"].get("feedback_digest", ""),
        "background_ticket_digest": continuation["background_ticket"].get("background_ticket_digest", ""),
        "foreground_prompt_released": True,
    }
    return finish_slice(
        slice_id=key,
        source_digest=source_digest,
        mode=mode,
        job=work,
        completed_in_slice=completed_in_slice,
        new_receipts=new_receipts,
        spent_cost=spent_cost,
        handoff=handoff,
    )
