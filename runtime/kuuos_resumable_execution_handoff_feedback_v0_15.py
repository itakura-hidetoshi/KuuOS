from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_resumable_execution_handoff_types_v0_15 import (
    FEEDBACK_VERSION,
    feedback_digest,
)


ACTIONS_BY_STATE = {
    "running": ["continue_foreground", "queue_background", "cancel_job"],
    "background_queued": ["continue_foreground", "change_priority", "cancel_job"],
    "waiting_external": ["retry_now", "queue_background", "cancel_job"],
    "budget_paused": ["increase_budget", "reduce_scope", "queue_background", "cancel_job"],
    "retry_backoff": ["retry_now", "retry_later", "queue_background", "cancel_job"],
    "blocked_bug": ["inspect_bug", "apply_patch", "revise_input", "reduce_scope", "cancel_job"],
    "permission_blocked": ["grant_permission", "reduce_scope", "cancel_job"],
    "needs_user_input": ["provide_input", "revise_input", "cancel_job"],
    "retry_exhausted": ["revise_input", "change_retry_policy", "reduce_scope", "cancel_job"],
    "completed": ["inspect_result", "start_new_job"],
    "cancelled": ["start_new_job"],
}


def build_feedback(
    *,
    observation: Mapping[str, Any],
    classification: Mapping[str, Any],
    checkpoint: Mapping[str, Any],
) -> dict[str, Any]:
    state = str(classification.get("execution_state", "running"))
    packet = {
        "version": FEEDBACK_VERSION,
        "job_id": str(observation.get("job_id", "")),
        "attempt_id": str(observation.get("attempt_id", "")),
        "execution_state": state,
        "reason_code": str(classification.get("reason_code", "")),
        "reason_summary": str(classification.get("reason_summary", "")),
        "phase": str(checkpoint.get("phase", "")),
        "completed_work_units": checkpoint.get("completed_work_units", 0),
        "total_work_units": checkpoint.get("total_work_units", 0),
        "progress_fraction": checkpoint.get("progress_fraction", 0.0),
        "checkpoint_digest": str(checkpoint.get("checkpoint_digest", "")),
        "last_successful_operation": str(
            checkpoint.get("last_successful_operation", "")
        ),
        "blocker_summary": str(observation.get("blocker_summary", "")),
        "resumable": bool(classification.get("resumable", False)),
        "foreground_prompt_released": bool(
            classification.get("foreground_prompt_released", False)
        ),
        "background_disposition": str(
            classification.get("background_disposition", "not_queued")
        ),
        "resume_condition": str(classification.get("resume_condition", "")),
        "retry_after_ms": int(classification.get("retry_after_ms", 0)),
        "retry_count": int(observation.get("retry_count", 0) or 0),
        "requires_user_guidance": bool(
            classification.get("requires_user_guidance", False)
        ),
        "user_actions": list(ACTIONS_BY_STATE.get(state, ["cancel_job"])),
        "no_silent_stop": True,
        "feedback_digest": "",
    }
    packet["feedback_digest"] = feedback_digest(packet)
    return packet
