from __future__ import annotations

import asyncio
import base64
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from mcp.server import MCPServer
from pydantic import ValidationError

from kuuos_mcp_bridge.event_subscriptions import (
    MemorySubscriptionStore, SubscriptionManager,
)
from kuuos_mcp_bridge.github_event_contract import (
    CI_EVENT, PR_EVENT, CI_GATES_EVENT, KUUOS_REPO, MGAP_REPO, EventContractError,
)
from kuuos_mcp_bridge.mcp_event_methods import (
    EventsListParams, EventsSubscribeParams, EventsUnsubscribeParams,
    _advertise_events_capability, _catalog_for_principal,
    install_mcp_event_methods,
)


NOW = datetime(2026, 11, 20, 13, tzinfo=timezone.utc)
KEY = "whsec_" + base64.b64encode(b"a" * 32).decode("ascii")
DEST = "https://receiver.example.com/cb"


def fixtures(authorized=lambda p, n, a: True, verified=lambda url, key, sid: True):
    store = MemorySubscriptionStore()
    manager = SubscriptionManager(
        store, authorize=authorized, verify_callback=verified,
        now=lambda: NOW
    )
    server = MCPServer("KuuOS MCP Events isolated test")
    install_mcp_event_methods(server, manager, principal_provider=lambda ctx: "owner-1")
    return server, manager, store


def handler(server, method):
    entry = server._lowlevel_server.get_request_handler(method)
    assert entry is not None
    return entry.handler


def params():
    return {
        "name": PR_EVENT,
        "arguments": {"repository": MGAP_REPO, "pr_number": 6883},
        "delivery": {"mode": "webhook", "url": DEST, "secret": KEY},
    }


def test_all_three_methods_registered_and_only_once():
    server, manager, _ = fixtures()
    for method in ("events/list", "events/subscribe", "events/unsubscribe"):
        assert server._lowlevel_server.get_request_handler(method) is not None
    with pytest.raises(RuntimeError, match="mcp_events_already_registered"):
        install_mcp_event_methods(
            server, manager, principal_provider=lambda ctx: "owner-1"
        )


def test_catalog_scopes_repository_to_authorized_owner_only():
    admitted = lambda p, n, a: a.get("repository") == KUUOS_REPO
    server, manager, _ = fixtures(authorized=admitted)
    data = asyncio.run(handler(server, "events/list")(None, EventsListParams()))
    assert len(data["events"]) == 3
    for item in data["events"]:
        assert item["inputSchema"]["properties"]["repository"]["enum"] == [KUUOS_REPO]


def test_no_authority_means_no_events():
    server, manager, _ = fixtures(authorized=lambda p, n, a: False)
    packet = _catalog_for_principal("owner-1", manager)
    assert packet == {"events": []}
    listed = asyncio.run(handler(server, "events/list")(None, EventsListParams()))
    assert listed["events"] == []


def test_list_cursor_rejected():
    server, _, _ = fixtures()
    with pytest.raises(EventContractError, match="events_list_cursor_not_supported"):
        asyncio.run(handler(server, "events/list")(None, EventsListParams(cursor="old")))


def test_subscribe_unsubscribe_lifecycle_via_registered_handlers():
    server, manager, store = fixtures()
    subscribe = handler(server, "events/subscribe")
    unsubscribe = handler(server, "events/unsubscribe")
    payload = params()
    first = asyncio.run(subscribe(None, EventsSubscribeParams.model_validate(payload)))
    second = asyncio.run(subscribe(None, EventsSubscribeParams.model_validate(payload)))
    assert first == second
    assert len(store.records) == 1
    unsub_payload = {
        "name": PR_EVENT,
        "arguments": payload["arguments"],
        "delivery": {"mode": "webhook", "url": DEST},
    }
    done = asyncio.run(unsubscribe(None, EventsUnsubscribeParams.model_validate(unsub_payload)))
    assert done == {}
    assert store.records == {}


def test_ttl_is_passed_with_alias_and_omitted_defaults():
    server, _, _ = fixtures()
    subscribe = handler(server, "events/subscribe")
    payload = params()
    payload["ttlMs"] = 3600000
    model = EventsSubscribeParams.model_validate(payload)
    assert model.ttl_ms == 3600000
    assert "ttl_ms" in model.model_fields_set
    result = asyncio.run(subscribe(None, model))
    assert result["refreshBefore"] == "2026-11-20T14:00:00Z"
    default = EventsSubscribeParams.model_validate(params())
    assert "ttl_ms" not in default.model_fields_set


def test_explicit_null_ttl_fails_closed():
    server, _, _ = fixtures()
    payload = params()
    payload["ttlMs"] = None
    with pytest.raises(EventContractError, match="unbounded_subscription_not_supported"):
        asyncio.run(
            handler(server, "events/subscribe")(
                None, EventsSubscribeParams.model_validate(payload)
            )
        )


def test_invalid_params_extra_fields_blocked_before_handler():
    with pytest.raises(ValidationError):
        EventsSubscribeParams.model_validate({**params(), "untrusted": True})
    with pytest.raises(ValidationError):
        EventsListParams.model_validate({"bad": 1})


def test_capabilities_keep_existing_and_advertise_only_handshake():
    async def downstream(ctx):
        return {"resultType": "complete", "capabilities": {"tools": {}, "resources": {}}}
    result = asyncio.run(
        _advertise_events_capability(
            SimpleNamespace(method="server/discover"), downstream
        )
    )
    assert result["capabilities"]["events"] == {}
    assert result["capabilities"]["tools"] == {}
    assert result["capabilities"]["resources"] == {}
    normal = asyncio.run(
        _advertise_events_capability(
            SimpleNamespace(method="tools/list"), downstream
        )
    )
    assert "events" not in normal["capabilities"]


def test_capability_does_not_claim_success_or_authority():
    server, manager, _ = fixtures()
    assert len(server.middleware) >= 1
    listed = _catalog_for_principal("owner-1", manager)
    assert [e["name"] for e in listed["events"]] == [CI_EVENT, CI_GATES_EVENT, PR_EVENT]
    assert all("Subscribe" not in e["description"] for e in listed["events"])


def test_capability_refuses_non_mapping_handshake():
    async def bad(ctx):
        return "not-a-supported-handshake"
    with pytest.raises(RuntimeError, match="mcp_events_handshake_shape_not_supported"):
        asyncio.run(_advertise_events_capability(
            SimpleNamespace(method="initialize"), bad
        ))


def test_oidc_ci_gates_not_advertised_for_mgap_only_principal():
    server, manager, _ = fixtures(
        authorized=lambda p, n, a: a.get("repository") == MGAP_REPO
    )
    catalog = asyncio.run(handler(server, "events/list")(None, EventsListParams()))
    assert [e["name"] for e in catalog["events"]] == [CI_EVENT, PR_EVENT]
    assert all(
        e["inputSchema"]["properties"]["repository"]["enum"] == [MGAP_REPO]
        for e in catalog["events"]
    )
