from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone

from starlette.requests import Request
from kuuos_mcp_bridge.event_delivery import PostResult
from kuuos_mcp_bridge.event_outbox import MemoryOutboxStore
from kuuos_mcp_bridge.event_subscriptions import MemorySubscriptionStore, SubscriptionManager
from kuuos_mcp_bridge.github_event_contract import CI_EVENT, MGAP_REPO
from kuuos_mcp_bridge.github_event_route import receive_signed_github_event

NOW = datetime(2026, 11, 20, 15, tzinfo=timezone.utc)
KEY = "a" * 40


def make_request(*, body=None, signature=True, method="POST", extra_headers=()):
    event = {
        "action": "completed",
        "repository": {"full_name": MGAP_REPO},
        "workflow_run": {
            "name": "PR Lean Fast Check", "id": 44737078837, "run_attempt": 1,
            "status": "completed", "conclusion": "failure",
            "head_sha": "b" * 40, "event": "pull_request",
        },
    }
    b = body if body is not None else json.dumps(event, sort_keys=True).encode()
    sig = "sha256=" + hmac.new(KEY.encode(), b, hashlib.sha256).hexdigest()
    if not signature:
        sig = "sha256=" + "0" * 64
    headers = [
        (b"x-github-event", b"workflow_run"),
        (b"x-hub-signature-256", sig.encode()),
        (b"x-github-delivery", b"a20f3142-0b52-4ea4-a93b-3412cf17f010"),
    ] + [(k.lower().encode(), str(v).encode()) for k, v in extra_headers]

    async def receive():
        return {"type": "http.request", "body": b, "more_body": False}
    return Request({
        "type": "http", "http_version": "1.1", "scheme": "https",
        "method": method, "path": "/github/events",
        "headers": headers,
    }, receive=receive)


def subscription_manager(*, authorized=True):
    store = MemorySubscriptionStore()
    manager = SubscriptionManager(
        store,
        authorize=lambda p, n, a: authorized,
        verify_callback=lambda u, k, i: True,
        now=lambda: NOW,
    )
    if authorized:
        manager.subscribe("owner-1", {
            "name": CI_EVENT,
            "arguments": {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"},
            "delivery": {"mode": "webhook", "url": "https://receiver.example.com/events",
                         "secret": "whsec_" + base64.b64encode(b"a" * 32).decode()},
        })
    return manager


class RecordingPoster:
    def __init__(self):
        self.calls = []
    def post(self, url, body, headers):
        self.calls.append((url, body, headers))
        return PostResult(200, b"ok")


def call(request, manager, outbox, **kwargs):
    return asyncio.run(receive_signed_github_event(
        request, manager=manager, outbox=outbox,
        ingress_secret=KEY, now=NOW, **kwargs,
    ))


def test_valid_signed_event_enqueued_once_without_claiming_ci_success():
    manager, outbox = subscription_manager(), MemoryOutboxStore()
    a = call(make_request(), manager, outbox)
    assert a.status_code == 202
    data = json.loads(a.body)
    assert data["accepted"] is True and data["enqueued"] == 1
    assert data["fresh_mcp_reobservation_required"] is True
    assert data["merge_authority_granted"] is False
    b = call(make_request(), manager, outbox)
    assert json.loads(b.body)["event_id"] == data["event_id"]
    assert len(outbox.records) == 1


def test_signed_event_inline_one_bounded_delivery():
    manager, outbox = subscription_manager(), MemoryOutboxStore()
    poster = RecordingPoster()
    response = call(make_request(), manager, outbox, deliver_inline=True, poster=poster)
    assert response.status_code == 202
    assert json.loads(response.body)["delivery_state"] == "delivered"
    assert len(poster.calls) == 1


def test_bad_signature_never_writes_outbox():
    manager, outbox = subscription_manager(), MemoryOutboxStore()
    reply = call(make_request(signature=False), manager, outbox)
    assert reply.status_code == 401
    assert len(outbox.records) == 0


def test_large_declared_request_fails_before_reading_body():
    manager, outbox = subscription_manager(), MemoryOutboxStore()
    reply = call(make_request(extra_headers=[("content-length", "999999")]), manager, outbox)
    assert reply.status_code == 413 and not outbox.records


def test_unknown_subscriber_not_invented():
    manager, outbox = subscription_manager(authorized=False), MemoryOutboxStore()
    reply = call(make_request(), manager, outbox)
    assert reply.status_code == 202
    assert json.loads(reply.body)["enqueued"] == 0
    assert not outbox.records


def test_invalid_source_event_is_not_trusted_even_if_signed():
    manager, outbox = subscription_manager(), MemoryOutboxStore()
    malformed = b'{"action":"completed","repository":{"full_name":"untrusted/other"}}'
    reply = call(make_request(body=malformed), manager, outbox)
    assert reply.status_code == 401
    assert not outbox.records


def test_no_configured_secret_rejects_even_correct_signature():
    manager, outbox = subscription_manager(), MemoryOutboxStore()
    reply = asyncio.run(receive_signed_github_event(
        make_request(), manager=manager, outbox=outbox,
        ingress_secret="", now=NOW,
    ))
    assert reply.status_code == 503
    assert not outbox.records
