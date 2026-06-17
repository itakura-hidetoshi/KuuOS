from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_resumable_execution_handoff_checkpoint_v0_15 import build_checkpoint
from runtime.kuuos_resumable_execution_handoff_feedback_v0_15 import build_feedback
from runtime.kuuos_resumable_execution_handoff_model_v0_15 import classify_execution
from runtime.kuuos_resumable_execution_handoff_ticket_v0_15 import build_background_ticket
from runtime.kuuos_resumable_execution_handoff_types_v0_15 import (
    DECISION_VERSION,
    NON_RUNNING_STATES,
    PAUSED_OR_BLOCKED_STATES,
    attempt_digest,
    decision_digest,
)


def build_execution_handoff(
    *,
    observation: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    job_id = str(observation.get("job_id", "")).strip()
    attempt_id = str(observation.get("attempt_id", "")).strip()
    if not job_id:
        raise ValueError("job_id_missing")
    if not attempt_id:
        raise ValueError("attempt_id_missing")

    checkpoint = build_checkpoint(observation)
    classification = classify_execution(observation, plan)
    feedback = build_feedback(
        observation=observation,
        classification=classification,
        checkpoint=checkpoint,
    )
    ticket = build_background_ticket(
        observation=observation,
        classification=classification,
        checkpoint=checkpoint,
    )
    state = str(classification.get("execution_state", "running"))

    if state in NON_RUNNING_STATES and not feedback:
        raise ValueError("non_running_state_without_feedback")
    if state in PAUSED_OR_BLOCKED_STATES and not bool(
        classification.get("foreground_prompt_released", False)
    ):
        raise ValueError("paused_state_without_foreground_release")

    packet = {
        "version": DECISION_VERSION,
        "job_id": job_id,
        "attempt_id": attempt_id,
        "source_parent_digest": str(observation.get("source_parent_digest", "")),
        "attempt_digest": attempt_digest(observation),
        "execution_state": state,
        "reason_code": classification.get("reason_code", ""),
        "reason_summary": classification.get("reason_summary", ""),
        "resume_condition": classification.get("resume_condition", ""),
        "retry_after_ms": classification.get("retry_after_ms", 0),
        "background_disposition": classification.get(
            "background_disposition", "not_queued"
        ),
        "foreground_prompt_released": classification.get(
            "foreground_prompt_released", False
        ),
        "resumable": classification.get("resumable", False),
        "requires_user_guidance": classification.get(
            "requires_user_guidance", False
        ),
        "checkpoint": checkpoint,
        "feedback": feedback,
        "background_ticket": ticket or {},
        "checkpoint_digest": checkpoint.get("checkpoint_digest", ""),
        "feedback_digest": feedback.get("feedback_digest", ""),
        "background_ticket_digest": (
            ticket.get("background_ticket_digest", "") if ticket else ""
        ),
        "feedback_receipt_present": True,
        "no_silent_stop": True,
        "lower_authority_preserved": True,
        "handoff_decision_digest": "",
    }
    packet["handoff_decision_digest"] = decision_digest(packet)
    return packet
