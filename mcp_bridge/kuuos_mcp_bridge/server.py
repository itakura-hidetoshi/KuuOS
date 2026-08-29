from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse

from .state_store import JsonStateStore, PostgresStateStore, StateConflictError, StateStore


def _env_bool(name: str, *, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_csv(name: str) -> list[str]:
    raw = os.environ.get(name, "")
    return [item.strip() for item in raw.split(",") if item.strip()]


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def build_store() -> StateStore:
    database_url = os.environ.get("KUUOS_MCP_DATABASE_URL") or os.environ.get("DATABASE_URL")
    if database_url:
        return PostgresStateStore(
            database_url,
            state_key=os.environ.get("KUUOS_MCP_STATE_KEY", "project"),
        )
    state_path = Path(os.environ.get("KUUOS_MCP_STATE_PATH", "./var/kuuos-mcp-state.json"))
    return JsonStateStore(state_path)


def build_transport_security() -> TransportSecuritySettings:
    allowed_hosts = _env_csv("KUUOS_MCP_ALLOWED_HOSTS")
    allowed_origins = _env_csv("KUUOS_MCP_ALLOWED_ORIGINS")

    for variable in ("VERCEL_URL", "VERCEL_BRANCH_URL", "VERCEL_PROJECT_PRODUCTION_URL"):
        hostname = os.environ.get(variable)
        if hostname:
            allowed_hosts.append(hostname)
            allowed_origins.append(f"https://{hostname}")

    if not allowed_hosts:
        allowed_hosts.extend(["127.0.0.1:*", "localhost:*", "[::1]:*"])
        allowed_origins.extend(
            ["http://127.0.0.1:*", "http://localhost:*", "http://[::1]:*"]
        )

    return TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=_dedupe(allowed_hosts),
        allowed_origins=_dedupe(allowed_origins),
    )


WRITE_ENABLED = _env_bool("KUUOS_MCP_WRITE_ENABLED", default=False)
store = build_store()
mcp = MCPServer(
    "KuuOS Chat-Work State Bridge",
    instructions=(
        "Use this server as the canonical continuation-state bridge shared by "
        "Chat and Work. Read before writing. Every write must pass the version "
        "returned by the preceding read as expected_version. On conflict, read "
        "again and reconcile rather than overwriting blindly."
    ),
)


@mcp.tool()
def get_project_state() -> dict[str, Any]:
    """Read the canonical shared project state, including its CAS version."""
    return store.read()


def update_project_state(
    expected_version: int,
    actor: str,
    patch_json: str,
) -> dict[str, Any]:
    """CAS-update canonical state from a JSON object patch."""
    patch = json.loads(patch_json)
    if not isinstance(patch, dict):
        raise ValueError("patch_json must decode to a JSON object")
    try:
        return store.update(patch, expected_version=expected_version, actor=actor)
    except StateConflictError as exc:
        return {
            "ok": False,
            "conflict": True,
            "message": str(exc),
            "current": store.read(),
        }


def record_continuation(
    expected_version: int,
    actor: str,
    canonical_sha: str | None = None,
    mathematical_frontier: str | None = None,
    next_actions_json: str | None = None,
    active_pr_json: str | None = None,
    ci_json: str | None = None,
) -> dict[str, Any]:
    """Write common repository/PR/CI/frontier hand-off fields with CAS."""
    patch: dict[str, Any] = {}
    if canonical_sha is not None:
        patch["canonical_sha"] = canonical_sha
    if mathematical_frontier is not None:
        patch["mathematical_frontier"] = mathematical_frontier
    if next_actions_json is not None:
        next_actions = json.loads(next_actions_json)
        if not isinstance(next_actions, list) or not all(
            isinstance(item, str) for item in next_actions
        ):
            raise ValueError("next_actions_json must decode to a list of strings")
        patch["next_actions"] = next_actions
    if active_pr_json is not None:
        patch["active_pr"] = json.loads(active_pr_json)
    if ci_json is not None:
        patch["ci"] = json.loads(ci_json)
    try:
        return store.update(patch, expected_version=expected_version, actor=actor)
    except StateConflictError as exc:
        return {
            "ok": False,
            "conflict": True,
            "message": str(exc),
            "current": store.read(),
        }


if WRITE_ENABLED:
    mcp.tool()(update_project_state)
    mcp.tool()(record_continuation)


@mcp.tool()
def list_next_actions() -> dict[str, Any]:
    """Return the current state version and ordered next actions."""
    state = store.read()
    return {"version": state["version"], "next_actions": state.get("next_actions", [])}


@mcp.resource("kuuos://state/project", mime_type="application/json")
def canonical_project_state() -> str:
    """Canonical Chat/Work continuation state as JSON."""
    return json.dumps(store.read(), ensure_ascii=False, indent=2, sort_keys=True)


@mcp.custom_route("/healthz", methods=["GET"], include_in_schema=False)
async def healthz(_: Request) -> JSONResponse:
    state = store.read()
    return JSONResponse(
        {
            "ok": True,
            "mode": "read-write" if WRITE_ENABLED else "read-only",
            "backend": type(store).__name__,
            "version": state["version"],
        }
    )


application = mcp.streamable_http_app(
    streamable_http_path="/mcp",
    json_response=True,
    stateless_http=True,
    transport_security=build_transport_security(),
)


def main() -> None:
    mcp.run(
        transport="streamable-http",
        host=os.environ.get("KUUOS_MCP_HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "8000")),
        streamable_http_path="/mcp",
        json_response=True,
        stateless_http=True,
        transport_security=build_transport_security(),
    )


if __name__ == "__main__":
    main()
