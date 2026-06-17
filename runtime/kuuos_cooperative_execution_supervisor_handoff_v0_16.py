from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_resumable_execution_handoff_checkpoint_v0_15 import build_checkpoint
from runtime.kuuos_resumable_execution_handoff_v0_15 import build_execution_handoff


def supervisor_observation(*, job: Mapping[str, Any], attempt_id: str, phase: str, next_step: Mapping[str, Any] | None, policy: Mapping[str, Any], mode: str, result: Mapping[str, Any] | None = None) -> dict[str, Any]:
    receipts = job.get("step_receipts", []) if isinstance(job.get("step_receipts", []), list) else []
    completed = job.get("completed_step_ids", []) if isinstance(job.get("completed_step_ids", []), list) else []
    steps = job.get("steps", []) if isinstance(job.get("steps", []), list) else []
    attempts = job.get("step_attempts", {}) if isinstance(job.get("step_attempts", {}), Mapping) else {}
    step_id = str((next_step or {}).get("step_id", ""))
    last_summary = str(receipts[-1].get("summary", "")) if receipts else ""
    packet = {
        "job_id": str(job.get("job_id", "")),
        "attempt_id": str(attempt_id),
        "source_parent_digest": str(job.get("source_parent_digest", "")),
        "phase": str(phase),
        "completed_work_units": len(completed),
        "total_work_units": len(steps),
        "last_successful_operation": last_summary,
        "checkpoint_payload": {
            "job_state_digest": str(job.get("job_state_digest", "")),
            "manifest_digest": str(job.get("manifest_digest", "")),
            "current_step_index": int(job.get("current_step_index", 0) or 0),
            "completed_step_ids": [str(item) for item in completed],
            "next_step_id": step_id,
        },
        "remaining_cost_units": max(0.0, float(job.get("remaining_budget_units", 0.0) or 0.0)),
        "estimated_next_cost_units": max(0.0, float((next_step or {}).get("estimated_cost_units", 0.0) or 0.0)),
        "wait_elapsed_ms": 0,
        "external_dependency_ready": True,
        "background_capable": bool(policy.get("background_worker_available", False)),
        "background_requested": mode == "background",
        "retry_count": int(attempts.get(step_id, 0) or 0),
        "error_kind": "",
        "blocker_summary": "",
        "user_input_required": False,
        "completed": False,
        "cancelled": False,
    }
    if result is None:
        return packet
    outcome = str(result.get("outcome", ""))
    packet["blocker_summary"] = str(result.get("summary", ""))
    if outcome == "transient_error":
        kind = str(result.get("error_kind", "transient_error"))
        packet["error_kind"] = kind if kind in {"timeout", "rate_limit", "transient_error"} else "transient_error"
    elif outcome == "deterministic_bug":
        kind = str(result.get("error_kind", "deterministic_bug"))
        packet["error_kind"] = kind if kind in {"deterministic_bug", "invariant_violation", "validation_bug", "serialization_bug"} else "deterministic_bug"
    elif outcome == "waiting_external":
        packet["external_dependency_ready"] = False
        packet["wait_elapsed_ms"] = max(1, int(policy.get("foreground_wait_threshold_ms", 10000) or 10000))
    elif outcome == "permission_denied":
        packet["error_kind"] = "permission_denied"
    elif outcome == "needs_user_input":
        packet["user_input_required"] = True
    elif outcome == "cancelled":
        packet["cancelled"] = True
    return packet


def build_progress_checkpoint(*, job: Mapping[str, Any], attempt_id: str, phase: str, next_step: Mapping[str, Any] | None, policy: Mapping[str, Any], mode: str) -> dict[str, Any]:
    return build_checkpoint(
        supervisor_observation(
            job=job,
            attempt_id=attempt_id,
            phase=phase,
            next_step=next_step,
            policy=policy,
            mode=mode,
        )
    )


def build_pause_handoff(*, job: Mapping[str, Any], attempt_id: str, phase: str, next_step: Mapping[str, Any] | None, policy: Mapping[str, Any], mode: str, result: Mapping[str, Any] | None = None) -> dict[str, Any]:
    observation = supervisor_observation(
        job=job,
        attempt_id=attempt_id,
        phase=phase,
        next_step=next_step,
        policy=policy,
        mode=mode,
        result=result,
    )
    return build_execution_handoff(observation=observation, plan=policy)
