from __future__ import annotations

from typing import Any

from kuuos_mcp_bridge.server import application as _application


async def app(scope: dict[str, Any], receive: Any, send: Any) -> None:
    """Expose the canonical `/mcp` ASGI app through Vercel's `/api/mcp` route."""
    if scope.get("type") == "http":
        scope = dict(scope)
        scope["path"] = "/mcp"
        scope["raw_path"] = b"/mcp"
    await _application(scope, receive, send)


application = app
