"""Real MCP SDK Streamable HTTP and GitHub route integration checks.

Unlike direct handler tests, these travel through the ASGI application.
No external HTTP or GitHub API calls are performed.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone

from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from starlette.testclient import TestClient

from kuuos_mcp_bridge.event_subscriptions import (
    MemorySubscriptionStore,
    SubscriptionManager,
)
from kuuos_mcp_bridge.event_outbox import MemoryOutboxStore
from kuuos_mcp_bridge.github_event_contract import CI_EVENT, MGAP_REPO
from kuuos_mcp_bridge.github_event_route import install_github_event_route
from kuuos_mcp_bridge.mcp_event_methods import install_mcp_event_methods

SECRET = "test-signature-secret-" + "s" * 32
CLOCK = datetime(2026, 11, 20, 13, 0, tzinfo=timezone.utc)


def _fixture():
    server = MCPServer("KuuOS typed events ASGI integration fixture")
    subscriptions = MemorySubscriptionStore()
    manager = SubscriptionManager(
        subscriptions,
        authorize=lambda principal, name, args: (
            principal == "fixture-owner" and args.get("repository") == MGAP_REPO
        ),
        verify_callback=lambda url, key, identity: True,
        now=lambda: CLOCK,
    )
    manager.subscribe("fixture-owner", {
        "name": CI_EVENT,
        "arguments": {
            "repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"
        },
        "delivery": {
            "mode": "webhook",
            "url": "https://receiver.example.org/callback",
            "secret": "whsec_" + base64.b64encode(b"z" * 32).decode("ascii"),
        },
    })
    outbox = MemoryOutboxStore()
    install_mcp_event_methods(
        server, manager, principal_provider=lambda ctx: "fixture-owner"
    )
    install_github_event_route(
        server, manager, outbox, ingress_secret=SECRET, deliver_inline=False
    )
    app = server.streamable_http_app(
        streamable_http_path="/mcp",
        json_response=True,
        stateless_http=True,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=False
        ),
    )
    return app, outbox


def _envelope() -> bytes:
    return json.dumps({
        "action": "completed",
        "repository": {"full_name": MGAP_REPO},
        "workflow_run": {
            "id": 44738980579,
            "run_attempt": 1,
            "name": "PR Lean Fast Check",
            "event": "pull_request",
            "status": "completed",
            "conclusion": "failure",
            "head_sha": "a" * 40,
        },
    }, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _headers(payload: bytes, *, valid: bool):
    signature = "sha256=" + hmac.new(
        SECRET.encode("utf-8"), payload, hashlib.sha256
    ).hexdigest()
    if not valid:
        signature = "sha256=" + "0" * 64
    return {
        "content-type": "application/json",
        "x-github-event": "workflow_run",
        "x-hub-signature-256": signature,
        "x-github-delivery": "9e93ae0e-034e-4a17-9333-e1004d094046",
    }


def test_signed_github_event_through_actual_asgi_custom_route():
    app, outbox = _fixture()
    with TestClient(app) as client:
        raw = _envelope()
        response = client.post("/github/events", content=raw, headers=_headers(raw, valid=True))
        assert response.status_code == 202, response.text
        data = response.json()
        assert data["accepted"] is True
        assert data["enqueued"] == 1
        assert data["event_is_success_evidence"] is False
        assert data["fresh_mcp_reobservation_required"] is True
        assert len(outbox.records) == 1


def test_bad_signature_through_actual_asgi_has_no_delivery_effect():
    app, outbox = _fixture()
    with TestClient(app) as client:
        raw = _envelope()
        response = client.post("/github/events", content=raw, headers=_headers(raw, valid=False))
        assert response.status_code == 401, response.text
        assert outbox.records == {}


def test_initialize_advertises_events_through_actual_mcp_http_transport():
    app, _ = _fixture()
    with TestClient(app) as client:
        reply = client.post(
            "/mcp",
            headers={
                "accept": "application/json, text/event-stream",
                "content-type": "application/json",
                "mcp-protocol-version": "2025-11-25",
            },
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-11-25",
                    "capabilities": {},
                    "clientInfo": {"name": "kuuos-asgi-test", "version": "0.1"},
                },
            },
        )
        assert reply.status_code == 200, reply.text
        packet = reply.json()
        assert packet["result"]["capabilities"]["events"] == {}
        assert "tools" in packet["result"]["capabilities"]
