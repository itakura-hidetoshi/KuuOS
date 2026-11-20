from __future__ import annotations

from typing import Any

from kuuos_mcp_bridge.server import application as _application


async def app(scope: dict[str, Any], receive: Any, send: Any) -> None:
    """Route /api/github to the opt-in, signed KuuOS MCP event ingress.

    If the feature is not enabled in the existing MCP server, the path is
    absent. The bridge never accepts unsigned events in a fallback mode.
    """
    if scope.get("type") == "http" and scope.get("path") in {
        "/api/github", "/api/github/", "/github/events",
    }:
        scope = dict(scope)
        scope["path"] = "/github/events"
        scope["raw_path"] = b"/github/events"
    await _application(scope, receive, send)


application = app
