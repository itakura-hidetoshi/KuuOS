from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, integer, mapping
from runtime.kuuos_resumable_execution_handoff_types_v0_15 import (
    BUNDLE_VERSION,
    bundle_digest,
    decision_digest,
)


def empty_handoff_bundle(agent_id: str) -> dict[str, Any]:
    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": str(agent_id),
        "generation": 0,
        "jobs": [],
        "feedback_history": [],
        "checkpoint_history": [],
        "background_queue": [],
        "handoff_ledger": [],
        "processed_attempt_digests": [],
        "handoff_bundle_digest": "",
    }
    packet["handoff_bundle_digest"] = bundle_digest(packet)
    return packet


def commit_execution_handoff(
    *,
    previous: Mapping[str, Any],
    decision: Mapping[str, Any],
    max_history: int = 256,
) -> tuple[dict[str, Any], bool]:
    expected = str(decision.get("handoff_decision_digest", ""))
    if not expected or expected != decision_digest(decision):
        raise ValueError("handoff_decision_digest_invalid")
    attempt = str(decision.get("attempt_digest", ""))
    if not attempt:
        raise ValueError("attempt_digest_missing")

    processed = {str(item) for item in as_list(previous.get("processed_attempt_digests"))}
    if attempt in processed:
        return dict(previous), True

    limit = max(1, int(max_history))
    job_id = str(decision.get("job_id", ""))
    jobs = [
        dict(mapping(item))
        for item in as_list(previous.get("jobs"))
        if str(mapping(item).get("job_id", "")) != job_id
    ]
    jobs.append(
        {
            "job_id": job_id,
            "attempt_id": decision.get("attempt_id", ""),
            "execution_state": decision.get("execution_state", ""),
            "reason_code": decision.get("reason_code", ""),
            "resume_condition": decision.get("resume_condition", ""),
            "checkpoint_digest": decision.get("checkpoint_digest", ""),
            "feedback_digest": decision.get("feedback_digest", ""),
            "foreground_prompt_released": decision.get(
                "foreground_prompt_released", False
            ),
            "requires_user_guidance": decision.get(
                "requires_user_guidance", False
            ),
            "handoff_decision_digest": expected,
        }
    )
    jobs.sort(key=lambda item: str(item.get("job_id", "")))

    feedback_history = as_list(previous.get("feedback_history")) + [
        dict(mapping(decision.get("feedback")))
    ]
    checkpoint_history = as_list(previous.get("checkpoint_history")) + [
        dict(mapping(decision.get("checkpoint")))
    ]

    queue = [dict(mapping(item)) for item in as_list(previous.get("background_queue"))]
    ticket = dict(mapping(decision.get("background_ticket")))
    ticket_id = str(ticket.get("ticket_id", ""))
    if ticket_id and all(str(item.get("ticket_id", "")) != ticket_id for item in queue):
        queue.append(ticket)

    ledger = as_list(previous.get("handoff_ledger")) + [
        {
            "job_id": job_id,
            "attempt_id": decision.get("attempt_id", ""),
            "attempt_digest": attempt,
            "execution_state": decision.get("execution_state", ""),
            "reason_code": decision.get("reason_code", ""),
            "checkpoint_digest": decision.get("checkpoint_digest", ""),
            "feedback_digest": decision.get("feedback_digest", ""),
            "background_ticket_digest": decision.get(
                "background_ticket_digest", ""
            ),
            "handoff_decision_digest": expected,
        }
    ]

    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": previous.get("agent_id", ""),
        "generation": integer(previous.get("generation"), 0) + 1,
        "jobs": jobs[-limit:],
        "feedback_history": feedback_history[-limit:],
        "checkpoint_history": checkpoint_history[-limit:],
        "background_queue": queue[-limit:],
        "handoff_ledger": ledger[-limit:],
        "processed_attempt_digests": sorted(processed | {attempt}),
        "handoff_bundle_digest": "",
    }
    packet["handoff_bundle_digest"] = bundle_digest(packet)
    return packet, False
