"""Feature-gated GitHub event HTTP ingress on the existing KuuOS MCP bridge.

This module registers no endpoint until called explicitly by server startup
with OAuth, encrypted PostgreSQL subscriptions, an outbox and an ingress secret.
An accepted GitHub signal is NOT proof of CI success or authorization to merge.
"""
from __future__ import annotations

import asyncio
import os
from datetime import datetime, timezone
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

from .event_delivery import PinnedHTTPSPoster
from .event_outbox import OutboxStore
from .event_pipeline import deliver_one, stage_signed_event
from .event_subscriptions import SubscriptionManager
from .github_event_ingress import GitHubIngressError, MAX_GITHUB_EVENT_BODY


async def _bounded_body(request: Request) -> bytes:
    declared = request.headers.get("content-length")
    if declared is not None:
        try:
            value = int(declared)
        except ValueError:
            raise GitHubIngressError("content_length_invalid") from None
        if value < 0 or value > MAX_GITHUB_EVENT_BODY:
            raise GitHubIngressError("body_too_large")
    chunks: list[bytes] = []
    size = 0
    async for chunk in request.stream():
        size += len(chunk)
        if size > MAX_GITHUB_EVENT_BODY:
            raise GitHubIngressError("body_too_large")
        chunks.append(chunk)
    return b"".join(chunks)


async def receive_signed_github_event(
    request: Request,
    *,
    manager: SubscriptionManager,
    outbox: OutboxStore,
    ingress_secret: str,
    deliver_inline: bool = False,
    poster: Any | None = None,
    now: datetime | None = None,
) -> JSONResponse:
    """Signatures must be validated before subscription/outbox lookup.

    The optional inline path is one bounded delivery attempt. Its failure
    leaves a durable pending record and does not create a timer or cron.
    """
    if not isinstance(ingress_secret, str) or len(ingress_secret.encode("utf-8")) < 32:
        return JSONResponse({"error": "ingress_not_configured"}, status_code=503)
    if request.method != "POST":
        return JSONResponse({"error": "method_not_allowed"}, status_code=405)
    try:
        raw = await _bounded_body(request)
    except GitHubIngressError:
        return JSONResponse({"error": "bad_request"}, status_code=413)
    event_type = request.headers.get("x-github-event", "")
    signature = request.headers.get("x-hub-signature-256", "")
    delivery_id = request.headers.get("x-github-delivery", "")
    moment = now if now is not None else datetime.now(timezone.utc)
    try:
        staged = await asyncio.to_thread(
            stage_signed_event, manager, outbox,
            event_type=event_type, raw_body=raw,
            github_signature=signature, github_secret=ingress_secret,
            delivery_id=delivery_id, now=moment,
        )
    except GitHubIngressError:
        # No caller-controlled error text, callback URLs or signing material.
        return JSONResponse({"error": "unauthorized_event"}, status_code=401)
    except Exception:
        # An unavailable database or ACL service must fail closed.
        return JSONResponse({"error": "ingress_unavailable"}, status_code=503)
    delivered: dict[str, Any] | None = None
    if deliver_inline and staged["outbox_ids"]:
        sender = poster if poster is not None else PinnedHTTPSPoster()
        try:
            delivered = await asyncio.to_thread(
                deliver_one, manager, outbox, poster=sender, now=moment,
            )
        except Exception:
            # Do not convert unknown egress failure into claim of delivery.
            delivered = {"state": "delivery_unverified"}
    return JSONResponse({
        "accepted": True,
        "enqueued": len(staged["outbox_ids"]),
        "event_id": staged["event_id"],
        "delivery_state": delivered["state"] if delivered else "not_attempted",
        "event_is_success_evidence": False,
        "fresh_mcp_reobservation_required": True,
        "merge_authority_granted": False,
    }, status_code=202)


def install_github_event_route(
    mcp: Any,
    manager: SubscriptionManager,
    outbox: OutboxStore,
    *,
    ingress_secret: str,
    deliver_inline: bool = False,
) -> None:
    if not isinstance(ingress_secret, str) or len(ingress_secret.encode()) < 32:
        raise RuntimeError("GitHub event ingress requires a configured signing secret")

    @mcp.custom_route("/github/events", methods=["POST"], include_in_schema=False)
    async def github_event(request: Request) -> JSONResponse:
        return await receive_signed_github_event(
            request, manager=manager, outbox=outbox,
            ingress_secret=ingress_secret, deliver_inline=deliver_inline,
        )
