from __future__ import annotations

from typing import Any

from kuuos_mcp_bridge.server import application as _application


async def app(scope: dict[str, Any], receive: Any, send: Any) -> None:
    """Expose MCP on `/api/mcp` while preserving auxiliary ASGI routes."""
    if scope.get("type") == "http":
        path = scope.get("path")
        if path in {"/api/mcp", "/api/mcp/", "/mcp/"}:
            scope = dict(scope)
            scope["path"] = "/mcp"
            scope["raw_path"] = b"/mcp"
    await _application(scope, receive, send)


application = app
