"""The MCP Events profile requires callback failures on the JSON-RPC error path."""
from __future__ import annotations

import asyncio
import base64

import pytest
from mcp import MCPError
from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from starlette.testclient import TestClient

from kuuos_mcp_bridge.event_subscriptions import MemorySubscriptionStore, SubscriptionManager
from kuuos_mcp_bridge.github_event_contract import CI_EVENT, MGAP_REPO
from kuuos_mcp_bridge.mcp_event_methods import (
    EventsSubscribeParams, install_mcp_event_methods,
)

SECRET = "whsec_" + base64.b64encode(b"x" * 32).decode("ascii")


def _server():
    store = MemorySubscriptionStore()
    manager = SubscriptionManager(
        store, authorize=lambda p, name, args: True,
        verify_callback=lambda url, key, subid: False,
    )
    mcp = MCPServer("KuuOS negative callback verification")
    install_mcp_event_methods(
        mcp, manager, principal_provider=lambda ctx: "test-owner",
    )
    return mcp, store


def _request():
    return {
        "name": CI_EVENT,
        "arguments": {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"},
        "delivery": {
            "mode": "webhook",
            "url": "https://callback.example.com/probe",
            "secret": SECRET,
        },
    }


def test_failed_callback_raises_typed_protocol_error():
    server, store = _server()
    entry = server._lowlevel_server.get_request_handler("events/subscribe")
    assert entry is not None
    with pytest.raises(MCPError) as caught:
        asyncio.run(entry.handler(None, EventsSubscribeParams.model_validate(_request())))
    assert caught.value.error.code == -32015
    assert caught.value.error.data == {"reason": "challenge_failed"}
    assert store.records == {}


def test_failed_callback_is_jsonrpc_minus_32015_not_success_result():
    server, store = _server()
    app = server.streamable_http_app(
        streamable_http_path="/mcp", json_response=True, stateless_http=True,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=False
        ),
    )
    with TestClient(app) as client:
        response = client.post("/mcp", headers={
            "accept": "application/json, text/event-stream",
            "content-type": "application/json",
            "mcp-protocol-version": "2025-11-25",
        }, json={
            "jsonrpc": "2.0", "id": 51,
            "method": "events/subscribe", "params": _request(),
        })
        assert response.status_code == 200, response.text
        data = response.json()
        assert "result" not in data
        assert data["error"]["code"] == -32015
        assert data["error"]["message"] == "CallbackEndpointError"
        assert data["error"]["data"] == {"reason": "challenge_failed"}
        assert store.records == {}
