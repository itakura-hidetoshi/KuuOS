"""Opt-in MCP Events method adapter for the existing KuuOS MCPServer.

This does not start an event source, grant OAuth, create a subscription store,
or deploy anything. The caller must supply a previously authenticated, stable
principal and a fail-closed subscription manager with current repository ACLs.

MCP Python SDK v2 has no first-class Events capability. The capability shim is
kept here, explicitly version-bound and isolated behind manual installation.
"""
from __future__ import annotations

import asyncio
from copy import deepcopy
from typing import Any, Callable

from mcp import MCPError
from mcp.server import MCPServer
from mcp.server.context import CallNext, HandlerResult
from mcp.types import RequestParams
from pydantic import ConfigDict, Field

from .event_subscriptions import SubscriptionManager
from .github_event_contract import (
    CI_EVENT, PR_EVENT, MGAP_REPO, KUUOS_REPO, EventContractError, event_catalog,
)


class EventsListParams(RequestParams):
    model_config = ConfigDict(extra="forbid")
    cursor: str | None = None


class EventsSubscribeParams(RequestParams):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    name: str
    arguments: dict[str, Any]
    delivery: dict[str, Any]
    cursor: str | None = None
    ttl_ms: int | None = Field(default=None, alias="ttlMs")


class EventsUnsubscribeParams(RequestParams):
    model_config = ConfigDict(extra="forbid")
    name: str
    arguments: dict[str, Any]
    delivery: dict[str, Any]


def _catalog_for_principal(
    principal: str, manager: SubscriptionManager,
) -> dict[str, Any]:
    """Do not advertise repository options the caller cannot use."""
    catalog = event_catalog()
    admitted: list[dict[str, Any]] = []
    for item in catalog["events"]:
        permitted = [
            repo for repo in (KUUOS_REPO, MGAP_REPO)
            if manager.authorize(principal, item["name"], {"repository": repo})
        ]
        if permitted:
            entry = deepcopy(item)
            entry["inputSchema"]["properties"]["repository"]["enum"] = permitted
            admitted.append(entry)
    return {"events": admitted}


async def _advertise_events_capability(ctx: Any, call_next: CallNext) -> HandlerResult:
    """Insert the extension only into the already computed handshake response.

    Unknown keys in the installed SDK's ServerCapabilities model are dropped.
    SDK v2 middleware returns serialized handler results: copy its capabilities
    into an ordinary dict to expose events while preserving all existing
    tools, resources, prompts and server metadata.
    """
    result = await call_next(ctx)
    if ctx.method not in ("initialize", "server/discover"):
        return result
    if hasattr(result, "model_dump"):
        serialized = result.model_dump(by_alias=True, exclude_none=True)
    elif isinstance(result, dict):
        serialized = dict(result)
    else:
        raise RuntimeError("mcp_events_handshake_shape_not_supported")
    caps = serialized.get("capabilities")
    if not isinstance(caps, dict):
        raise RuntimeError("mcp_events_capabilities_not_mapping")
    caps = dict(caps)
    caps["events"] = {}
    serialized["capabilities"] = caps
    return serialized


def oauth_principal(_: Any) -> str:
    """Stable owner identity from the *verified* MCP OAuth access token.

    Never fall back to a GitHub username, HTTP header or unverified bearer.
    """
    from mcp.server.auth.middleware.auth_context import get_access_token

    token = get_access_token()
    if token is None:
        raise EventContractError("mcp_events_oauth_required")
    subject = getattr(token, "subject", None)
    if subject is None:
        claims = getattr(token, "claims", None)
        if isinstance(claims, dict):
            subject = claims.get("sub")
    if not isinstance(subject, str) or not subject:
        raise EventContractError("mcp_events_oauth_subject_required")
    return subject


def install_mcp_event_methods(
    mcp: MCPServer,
    manager: SubscriptionManager,
    *,
    principal_provider: Callable[[Any], str] = oauth_principal,
) -> None:
    """Register three JSON-RPC methods on the existing authenticated endpoint.

    The default principal provider accepts only the verified MCP OAuth token.
    Do not call in production without a configured PostgreSQL store, current
    repo authorization, a DNS-pinned callback verifier and valid encryption.
    """
    lowlevel = getattr(mcp, "_lowlevel_server", None)
    if lowlevel is None or not callable(getattr(lowlevel, "add_request_handler", None)):
        raise RuntimeError("mcp_events_sdk_request_handler_missing")
    for name in ("events/list", "events/subscribe", "events/unsubscribe"):
        if lowlevel.get_request_handler(name) is not None:
            raise RuntimeError("mcp_events_already_registered")

    async def list_events(ctx: Any, params: EventsListParams) -> dict[str, Any]:
        if params.cursor is not None:
            raise EventContractError("events_list_cursor_not_supported")
        principal = principal_provider(ctx)
        return _catalog_for_principal(principal, manager)

    async def subscribe(ctx: Any, params: EventsSubscribeParams) -> dict[str, Any]:
        principal = principal_provider(ctx)
        payload: dict[str, Any] = {
            "name": params.name,
            "arguments": params.arguments,
            "delivery": params.delivery,
            "cursor": params.cursor,
        }
        if "ttl_ms" in params.model_fields_set:
            payload["ttlMs"] = params.ttl_ms
        try:
            return await asyncio.to_thread(manager.subscribe, principal, payload)
        except EventContractError as exc:
            if str(exc) == "callback_verification_failed":
                # The MCP Events profile requires a protocol error (-32015),
                # not a successful result or a generic SDK exception.
                raise MCPError(
                    code=-32015,
                    message="CallbackEndpointError",
                    data={"reason": "challenge_failed"},
                ) from None
            raise

    async def unsubscribe(ctx: Any, params: EventsUnsubscribeParams) -> dict[str, Any]:
        principal = principal_provider(ctx)
        return await asyncio.to_thread(
            manager.unsubscribe, principal, {
                "name": params.name, "arguments": params.arguments,
                "delivery": params.delivery,
            }
        )

    lowlevel.add_request_handler("events/list", EventsListParams, list_events)
    lowlevel.add_request_handler("events/subscribe", EventsSubscribeParams, subscribe)
    lowlevel.add_request_handler("events/unsubscribe", EventsUnsubscribeParams, unsubscribe)
    mcp.middleware.append(_advertise_events_capability)
