"""Explicit feature-gated bootstrap of MCP Events on the existing KuuOS server.

Fail closed if any required authentication, durable backend, principal
allowlist, encryption key or repository authorization configuration is absent.
Nothing is subscribed or delivered merely because the module exists.
"""
from __future__ import annotations

import os
from typing import Any

from .event_delivery import verify_callback_challenge
from .event_subscriptions import PostgresSubscriptionStore, SubscriptionManager
from .github_event_contract import REPOSITORIES
from .mcp_event_methods import install_mcp_event_methods
from .state_store import PostgresStateStore


def _csv(name: str) -> tuple[str, ...]:
    raw = os.environ.get(name, "")
    values = [v.strip() for v in raw.split(",") if v.strip()]
    if len(values) != len(set(values)) or "*" in values:
        raise RuntimeError(f"{name} invalid or wildcard")
    return tuple(values)


def configure_mcp_events(mcp: Any, oauth: Any, store: Any) -> SubscriptionManager:
    """Called only under KUUOS_MCP_EVENTS_ENABLED=true.

    This config enables authenticated subscription methods, *not* GitHub
    ingress, event publication or Dots delivery. Those remain distinct,
    independently tested boundaries.
    """
    if oauth is None:
        raise RuntimeError("MCP Events require OAuth")
    if not isinstance(store, PostgresStateStore):
        raise RuntimeError("MCP Events require PostgreSQL state backend")

    owners = _csv("KUUOS_MCP_EVENTS_ALLOWED_SUBJECTS")
    if not owners:
        raise RuntimeError("MCP Events require allowed OAuth subject list")
    repositories = _csv("KUUOS_MCP_EVENTS_ALLOWED_REPOS")
    if not repositories or not set(repositories).issubset(REPOSITORIES):
        raise RuntimeError("MCP Events repository allowlist missing or invalid")

    key = os.environ.get("KUUOS_MCP_EVENTS_ENCRYPTION_KEY", "")
    if not key:
        raise RuntimeError("MCP Events encryption key missing")
    database_url = getattr(store, "database_url", "")
    if not isinstance(database_url, str) or not database_url:
        raise RuntimeError("MCP Events require configured PostgreSQL DSN")

    def authorize(principal: str, name: str, arguments: Any) -> bool:
        return (
            principal in owners
            and isinstance(arguments, dict)
            and arguments.get("repository") in repositories
        )

    subscriptions = PostgresSubscriptionStore(database_url, key)
    manager = SubscriptionManager(
        subscriptions,
        authorize=authorize,
        verify_callback=verify_callback_challenge,
    )
    install_mcp_event_methods(mcp, manager)
    return manager
