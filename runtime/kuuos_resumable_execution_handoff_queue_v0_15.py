from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, integer, mapping
from runtime.kuuos_resumable_execution_handoff_ticket_v0_15 import (
    claim_background_ticket,
    finish_background_ticket,
    heartbeat_background_ticket,
)
from runtime.kuuos_resumable_execution_handoff_types_v0_15 import (
    bundle_digest,
    ticket_digest,
)


def _replace_ticket(
    bundle: Mapping[str, Any],
    updated_ticket: Mapping[str, Any],
    event: str,
) -> dict[str, Any]:
    ticket_id = str(updated_ticket.get("ticket_id", ""))
    digest = str(updated_ticket.get("background_ticket_digest", ""))
    if not ticket_id:
        raise ValueError("background_ticket_id_missing")
    if not digest or digest != ticket_digest(updated_ticket):
        raise ValueError("background_ticket_digest_invalid")

    queue = [dict(mapping(item)) for item in as_list(bundle.get("background_queue"))]
    found = False
    for index, item in enumerate(queue):
        if str(item.get("ticket_id", "")) == ticket_id:
            queue[index] = dict(updated_ticket)
            found = True
            break
    if not found:
        raise ValueError("background_ticket_not_found")

    packet = dict(bundle)
    packet["generation"] = integer(bundle.get("generation"), 0) + 1
    packet["background_queue"] = queue
    packet["handoff_ledger"] = as_list(bundle.get("handoff_ledger")) + [
        {
            "phase": "background_ticket_update",
            "event": event,
            "ticket_id": ticket_id,
            "queue_status": updated_ticket.get("queue_status", ""),
            "lease_owner": updated_ticket.get("lease_owner", ""),
            "lease_expires_at_ms": updated_ticket.get("lease_expires_at_ms", 0),
            "background_ticket_digest": digest,
        }
    ]
    packet["handoff_bundle_digest"] = ""
    packet["handoff_bundle_digest"] = bundle_digest(packet)
    return packet


def claim_next_background_ticket(
    bundle: Mapping[str, Any],
    *,
    worker_id: str,
    now_ms: int,
    lease_duration_ms: int,
) -> tuple[dict[str, Any], dict[str, Any], bool]:
    queue = sorted(
        [dict(mapping(item)) for item in as_list(bundle.get("background_queue"))],
        key=lambda item: str(item.get("ticket_id", "")),
    )
    for ticket in queue:
        claimed, changed = claim_background_ticket(
            ticket,
            worker_id=worker_id,
            now_ms=now_ms,
            lease_duration_ms=lease_duration_ms,
        )
        if changed:
            return _replace_ticket(bundle, claimed, "claimed"), claimed, True
    return dict(bundle), {}, False


def heartbeat_ticket_in_bundle(
    bundle: Mapping[str, Any],
    *,
    ticket_id: str,
    worker_id: str,
    now_ms: int,
    lease_duration_ms: int,
) -> tuple[dict[str, Any], bool]:
    for raw in as_list(bundle.get("background_queue")):
        ticket = dict(mapping(raw))
        if str(ticket.get("ticket_id", "")) != str(ticket_id):
            continue
        updated, changed = heartbeat_background_ticket(
            ticket,
            worker_id=worker_id,
            now_ms=now_ms,
            lease_duration_ms=lease_duration_ms,
        )
        if not changed:
            return dict(bundle), False
        return _replace_ticket(bundle, updated, "heartbeat"), True
    return dict(bundle), False


def finish_ticket_in_bundle(
    bundle: Mapping[str, Any],
    *,
    ticket_id: str,
    worker_id: str,
    final_status: str,
    summary: str,
) -> tuple[dict[str, Any], bool]:
    for raw in as_list(bundle.get("background_queue")):
        ticket = dict(mapping(raw))
        if str(ticket.get("ticket_id", "")) != str(ticket_id):
            continue
        updated, changed = finish_background_ticket(
            ticket,
            worker_id=worker_id,
            final_status=final_status,
            summary=summary,
        )
        if not changed:
            return dict(bundle), False
        return _replace_ticket(bundle, updated, "finished"), True
    return dict(bundle), False
