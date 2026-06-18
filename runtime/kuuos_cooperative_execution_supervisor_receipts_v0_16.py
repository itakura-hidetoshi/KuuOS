from __future__ import annotations

from typing import Any, Mapping, Sequence

from runtime.kuuos_context_gauge_atlas_types_v0_13 import sha
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import (
    STEP_RECEIPT_VERSION,
    YIELD_VERSION,
    step_receipt_digest,
    yield_digest,
)


def build_step_receipt(*, job: Mapping[str, Any], step: Mapping[str, Any], attempt: int, execution_key: str, result: Mapping[str, Any]) -> dict[str, Any]:
    packet = {
        "version": STEP_RECEIPT_VERSION,
        "job_id": str(job.get("job_id", "")),
        "manifest_digest": str(job.get("manifest_digest", "")),
        "step_id": str(step.get("step_id", "")),
        "operation_id": str(step.get("operation_id", "")),
        "operation_input_digest": str(step.get("operation_input_digest", "")),
        "attempt": int(attempt),
        "execution_key": str(execution_key),
        "outcome": str(result.get("outcome", "")),
        "summary": str(result.get("summary", "")),
        "cost_units": max(0.0, float(result.get("cost_units", 0.0) or 0.0)),
        "output_digest": sha(result.get("output", {})),
        "checkpoint_payload_digest": sha(result.get("checkpoint_payload", {})),
        "step_receipt_digest": "",
    }
    packet["step_receipt_digest"] = step_receipt_digest(packet)
    return packet


def build_foreground_yield(*, job: Mapping[str, Any], source_job_state_digest: str, completed_in_slice: Sequence[str], next_step: Mapping[str, Any] | None, checkpoint_digest: str, background_supported: bool) -> dict[str, Any]:
    steps = job.get("steps", []) if isinstance(job.get("steps", []), list) else []
    completed_steps = job.get("completed_step_ids", []) if isinstance(job.get("completed_step_ids", []), list) else []
    total = len(steps)
    completed = len(completed_steps)
    progress = round(completed / total, 6) if total > 0 else 1.0
    actions = ["continue_foreground", "reduce_scope", "revise_input", "cancel_job"]
    if background_supported:
        actions.insert(1, "queue_background")
    packet = {
        "version": YIELD_VERSION,
        "job_id": str(job.get("job_id", "")),
        "source_job_state_digest": str(source_job_state_digest),
        "result_job_state_digest": str(job.get("job_state_digest", "")),
        "supervisor_state": "foreground_yielded",
        "completed_in_slice": [str(item) for item in completed_in_slice],
        "completed_work_units": completed,
        "total_work_units": total,
        "progress_fraction": progress,
        "next_step_id": str((next_step or {}).get("step_id", "")),
        "checkpoint_digest": str(checkpoint_digest),
        "foreground_prompt_released": True,
        "background_supported": bool(background_supported),
        "user_actions": actions,
        "yield_digest": "",
    }
    packet["yield_digest"] = yield_digest(packet)
    return packet
