"""Verified GitHub wake-ups into durable events; no implicit background work.

The source packet is only a wake-up. CI truth requires a subsequent exact
GitHub MCP run/job/step re-observation by the receiving Dot.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .event_delivery import EventDeliveryError, deliver_event
from .event_outbox import OutboxStore
from .event_subscriptions import SubscriptionManager
from .github_event_ingress import compile_signed_github_wakeup


def _now() -> datetime:
    return datetime.now(timezone.utc)


def stage_signed_event(
    manager: SubscriptionManager, outbox: OutboxStore,
    *, event_type: str, raw_body: bytes, github_signature: str,
    github_secret: str, delivery_id: str, now: datetime | None = None,
) -> dict[str, Any]:
    verified = compile_signed_github_wakeup(
        event_type, raw_body, github_signature, github_secret, delivery_id,
    )
    moment = now if now is not None else _now()
    matching = manager.recipients(verified.packet)
    identifiers = [
        outbox.enqueue(item, verified.packet, moment).id
        for item in matching
    ]
    return {
        "event_id": verified.event_id, "outbox_ids": identifiers,
        "eligible_recipients": len(matching),
        "github_signature_verified": True,
        "signal_is_success_evidence": False,
        "fresh_mcp_reobservation_required": True,
        "merge_authority_granted": False,
        "write_authority_granted": False,
    }


def deliver_one(
    manager: SubscriptionManager, outbox: OutboxStore,
    *, poster: Any, now: datetime | None = None,
    outbox_id: str | None = None,
) -> dict[str, Any]:
    """Claim a specific newly received event when provided.

    Without an exact ID, this retains the prior bounded recovery behavior.
    No arbitrary backlog event can consume a new event's inline wake-up.
    """
    moment = now if now is not None else _now()
    lease = (outbox.claim_specific(outbox_id, moment, 30)
             if outbox_id is not None else outbox.claim(moment, 30))
    if lease is None:
        return {"state": "no_due_events", "signal_is_success_evidence": False}
    token = lease.lease_token
    assert isinstance(token, str)
    try:
        # A recipient can revoke OAuth/repository access between enqueue and
        # delivery. Refuse the send unless fresh authorization still passes.
        matching = manager.recipients(lease.packet)
    except Exception:
        next_row = outbox.settle(lease.id, token, None, moment)
        return {"state": "authorization_recheck_failed",
                "outbox": next_row.public_receipt()}
    current = next((sub for sub in matching if sub.id == lease.subscription_id), None)
    if current is None:
        revoked = outbox.cancel(lease.id, token)
        return {"state": "recipient_revoked", "outbox": revoked.public_receipt()}
    try:
        report = deliver_event(
            current, lease.packet, poster=poster,
            max_attempts=1, sleep=lambda _: None,
        )
        status = report.last_status
    except (EventDeliveryError, OSError):
        status = None
    row = outbox.settle(lease.id, token, status, moment)
    return {
        "state": row.state,
        "outbox": row.public_receipt(),
        "signal_is_success_evidence": False,
        "fresh_mcp_reobservation_required": True,
    }
