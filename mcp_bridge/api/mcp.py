from __future__ import annotations

from typing import Any

from kuuos_mcp_bridge.server import application as _application


async def app(scope: dict[str, Any], receive: Any, send: Any) -> None:
    """Normalize MCP and signed GitHub ingress through one Vercel ASGI entrypoint.

    Alias mapping does not authorize a GitHub event: the server still
    validates its raw-body HMAC and enforces the feature-gated route.
    """
    if scope.get("type") == "http":
        path = scope.get("path")
        if path in {"/api/mcp", "/api/mcp/", "/mcp/"}:
            scope = dict(scope)
            scope["path"] = "/mcp"
            scope["raw_path"] = b"/mcp"
        elif path in {"/api/github", "/api/github/"}:
            scope = dict(scope)
            scope["path"] = "/github/events"
            scope["raw_path"] = b"/github/events"
        elif path in {"/api/github-oidc", "/api/github-oidc/"}:
            scope = dict(scope)
            scope["path"] = "/github/oidc"
            scope["raw_path"] = b"/github/oidc"
    await _application(scope, receive, send)


application = app
