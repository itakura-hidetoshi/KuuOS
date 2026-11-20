"""Health receipt exposes only configured event routes, not Dot delivery proof."""
from __future__ import annotations

import asyncio
import json

from kuuos_mcp_bridge import server


class FixtureStore:
    def read(self):
        return {"version": 7, "canonical_sha": "a" * 40}


def _receipt(monkeypatch, *, events: bool, ingress: bool):
    monkeypatch.setattr(server, "store", FixtureStore())
    monkeypatch.setattr(server, "oauth", None)
    monkeypatch.setattr(server, "WRITE_ENABLED", False)
    monkeypatch.setattr(
        server, "event_subscription_manager",
        object() if events else None,
    )
    monkeypatch.setattr(server, "event_outbox", object() if ingress else None)
    response = asyncio.run(server.healthz(None))
    assert response.status_code == 200
    return json.loads(response.body)


def test_disabled_event_routes_are_explicit_and_do_not_claim_delivery(monkeypatch):
    receipt = _receipt(monkeypatch, events=False, ingress=False)
    assert receipt["ok"] is True
    assert receipt["mode"] == "read-only"
    assert receipt["mcp_events_adapter_loaded"] is False
    assert receipt["github_event_ingress_loaded"] is False
    assert "dots_callback_verified" not in receipt
    assert "github_signature_verified" not in receipt


def test_loaded_event_routes_are_observable_but_not_delivery_receipts(monkeypatch):
    receipt = _receipt(monkeypatch, events=True, ingress=True)
    assert receipt["mcp_events_adapter_loaded"] is True
    assert receipt["github_event_ingress_loaded"] is True
    assert receipt["oauth_enabled"] is False
    assert receipt["write_ready"] is False
    assert "dots_callback_verified" not in receipt
    assert "subscription_receipt" not in receipt
