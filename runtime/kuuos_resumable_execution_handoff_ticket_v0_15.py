from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import sha
from runtime.kuuos_resumable_execution_handoff_types_v0_15 import (
    TICKET_VERSION,
    ticket_digest,
)


def _sealed(packet: dict[str, Any]) -> dict[str, Any]:
    packet["background_ticket_digest"] = ticket_digest(packet)
    return packet


def build_background_ticket(
    *,
    observation: Mapping[str, Any],
    classification: Mapping[str, Any],
    checkpoint: Mapping[str, Any],
) -> dict[str, Any] | None:
    if str(classification.get("execution_state", "")) != "background_queued":
        return None
    packet = {
        "version": TICKET_VERSION,
        "ticket_id": "handoff-ticket-" + sha(
            {
                "job": observation.get("job_id", ""),
                "attempt": observation.get("attempt_id", ""),
                "checkpoint": checkpoint.get("checkpoint_digest", ""),
                "reason": classification.get("reason_code", ""),
            }
        )[:20],
        "job_id": str(observation.get("job_id", "")),
        "attempt_id": str(observation.get("attempt_id", "")),
        "checkpoint_digest": str(checkpoint.get("checkpoint_digest", "")),
        "reason_code": str(classification.get("reason_code", "")),
        "resume_condition": str(classification.get("resume_condition", "")),
        "retry_after_ms": int(classification.get("retry_after_ms", 0)),
        "queue_status": "queued",
        "lease_owner": "",
        "lease_started_at_ms": 0,
        "lease_expires_at_ms": 0,
        "heartbeat_at_ms": 0,
        "completion_summary": "",
        "background_ticket_digest": "",
    }
    return _sealed(packet)


def claim_background_ticket(
    ticket: Mapping[str, Any],
    *,
    worker_id: str,
    now_ms: int,
    lease_duration_ms: int,
) -> tuple[dict[str, Any], bool]:
    packet = dict(ticket)
    status = str(packet.get("queue_status", ""))
    now = max(0, int(now_ms))
    duration = max(1, int(lease_duration_ms))
    expired = status == "leased" and int(packet.get("lease_expires_at_ms", 0)) <= now
    if status != "queued" and not expired:
        return packet, False
    packet.update(
        {
            "queue_status": "leased",
            "lease_owner": str(worker_id),
            "lease_started_at_ms": now,
            "lease_expires_at_ms": now + duration,
            "heartbeat_at_ms": now,
            "background_ticket_digest": "",
        }
    )
    return _sealed(packet), True


def heartbeat_background_ticket(
    ticket: Mapping[str, Any],
    *,
    worker_id: str,
    now_ms: int,
    lease_duration_ms: int,
) -> tuple[dict[str, Any], bool]:
    packet = dict(ticket)
    now = max(0, int(now_ms))
    if str(packet.get("queue_status", "")) != "leased":
        return packet, False
    if str(packet.get("lease_owner", "")) != str(worker_id):
        return packet, False
    if int(packet.get("lease_expires_at_ms", 0)) < now:
        return packet, False
    duration = max(1, int(lease_duration_ms))
    packet.update(
        {
            "heartbeat_at_ms": now,
            "lease_expires_at_ms": now + duration,
            "background_ticket_digest": "",
        }
    )
    return _sealed(packet), True


def finish_background_ticket(
    ticket: Mapping[str, Any],
    *,
    worker_id: str,
    final_status: str,
    summary: str,
) -> tuple[dict[str, Any], bool]:
    packet = dict(ticket)
    if str(packet.get("queue_status", "")) != "leased":
        return packet, False
    if str(packet.get("lease_owner", "")) != str(worker_id):
        return packet, False
    if final_status not in {"completed", "failed", "cancelled"}:
        return packet, False
    packet.update(
        {
            "queue_status": final_status,
            "completion_summary": str(summary),
            "background_ticket_digest": "",
        }
    )
    return _sealed(packet), True
