from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from mcp.server import MCPServer
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse

from .github_issue_store import DEFAULT_GITHUB_ISSUE_API_URL, GitHubIssueStateStore
from .oauth import OAuthConfig, build_oauth_config
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

    issue_api_url = os.environ.get("KUUOS_MCP_GITHUB_ISSUE_API_URL")
    if issue_api_url or os.environ.get("VERCEL"):
        return GitHubIssueStateStore(issue_api_url or DEFAULT_GITHUB_ISSUE_API_URL)

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
oauth: OAuthConfig | None = build_oauth_config()

if WRITE_ENABLED:
    if not isinstance(store, PostgresStateStore):
        raise RuntimeError(
            "KUUOS_MCP_WRITE_ENABLED=true requires the PostgreSQL backend"
        )
    if oauth is None:
        raise RuntimeError(
            "KUUOS_MCP_WRITE_ENABLED=true requires KUUOS_MCP_OAUTH_ENABLED=true "
            "with a configured OAuth token verifier or embedded provider"
        )


mcp_kwargs: dict[str, Any] = {}
if oauth is not None:
    mcp_kwargs["auth"] = oauth.auth_settings
    if oauth.embedded_provider is not None:
        mcp_kwargs["auth_server_provider"] = oauth.embedded_provider
    elif oauth.token_verifier is not None:
        mcp_kwargs["token_verifier"] = oauth.token_verifier
    else:  # pragma: no cover - OAuthConfig invariant
        raise RuntimeError("OAuth configuration has no verifier or provider")

mcp = MCPServer(
    "KuuOS Chat-Work State Bridge",
    instructions=(
        "Use this server as the canonical continuation-state bridge shared by "
        "Chat and Work. Read before writing. Every write must pass the version "
        "returned by the preceding read as expected_version. On conflict, read "
        "again and reconcile rather than overwriting blindly."
    ),
    **mcp_kwargs,
)


if oauth is not None and oauth.embedded_provider is not None:
    _embedded_provider = oauth.embedded_provider

    @mcp.custom_route("/login", methods=["GET"], include_in_schema=False)
    async def embedded_login(request: Request):
        return await _embedded_provider.login_page(request)

    @mcp.custom_route("/login/callback", methods=["POST"], include_in_schema=False)
    async def embedded_login_callback(request: Request):
        return await _embedded_provider.login_callback(request)


def _require_write_scope() -> None:
    if oauth is None:
        raise PermissionError("OAuth is required for writes")
    token = get_access_token()
    if token is None or oauth.write_scope not in token.scopes:
        raise PermissionError(f"OAuth scope {oauth.write_scope!r} is required for writes")


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
    _require_write_scope()
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
    _require_write_scope()
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
            "oauth_enabled": oauth is not None,
            "oauth_mode": oauth.token_mode if oauth is not None else None,
            "write_ready": WRITE_ENABLED
            and isinstance(store, PostgresStateStore)
            and oauth is not None,
            # Non-secret server-side feature inventory only. These fields do
            # not attest a Dots subscription, callback, or GitHub CI evidence.
            "mcp_events_adapter_loaded": event_subscription_manager is not None,
            "github_event_ingress_loaded": event_outbox is not None,
            "github_oidc_source_loaded": _env_bool("KUUOS_MCP_GITHUB_OIDC_ENABLED"),
            "github_oidc_delivery_loaded": oidc_delivery_loaded,
            # No URL or secret is returned; system variables are optional.
            "vercel_system_url_present": bool(os.environ.get("VERCEL_URL")),
            "vercel_deployment_environment": os.environ.get("VERCEL_ENV")
            if os.environ.get("VERCEL_ENV") in {"preview", "production", "development"}
            else None,
            "canonical_sha": os.environ.get("KUUOS_MCP_CANONICAL_SHA")
            or state.get("canonical_sha"),
        }
    )


# Event methods are opt-in. Production stays unchanged without all of:
# OAuth, PostgreSQL, subject/repository allowlists, and an encryption key.
# An enabled subscription API is not an event source or Dots delivery receipt.
event_subscription_manager = None
if _env_bool("KUUOS_MCP_EVENTS_ENABLED"):
    from .event_bootstrap import configure_mcp_events

    event_subscription_manager = configure_mcp_events(mcp, oauth, store)


# Trusted GitHub ingress is separately opt-in, requires an authenticated
# MCP Events subscription manager and a durable PostgreSQL outbox.
# The inline post switch is off unless explicitly enabled after review.
event_outbox = None
if _env_bool("KUUOS_MCP_GITHUB_INGRESS_ENABLED"):
    if event_subscription_manager is None or not isinstance(store, PostgresStateStore):
        raise RuntimeError("GitHub event ingress requires configured MCP Events and PostgreSQL")
    ingress_secret = os.environ.get("KUUOS_MCP_GITHUB_INGRESS_SECRET", "")
    if len(ingress_secret.encode("utf-8")) < 32:
        raise RuntimeError("GitHub event ingress requires a protected signing secret")
    from .event_outbox import PostgresOutboxStore
    from .github_event_route import install_github_event_route

    event_outbox = PostgresOutboxStore(store.database_url)
    install_github_event_route(
        mcp, event_subscription_manager, event_outbox,
        ingress_secret=ingress_secret,
        deliver_inline=_env_bool("KUUOS_MCP_GITHUB_INGRESS_INLINE_DELIVERY"),
    )


# GitHub Actions OIDC is a separate source identity attestation gate.
# A real signed push receipt is NOT a completed CI result or Dots delivery.
github_oidc_source_loaded = False
oidc_delivery_loaded = False
if _env_bool("KUUOS_MCP_GITHUB_OIDC_DELIVERY_ENABLED") and not _env_bool("KUUOS_MCP_GITHUB_OIDC_ENABLED"):
    raise RuntimeError("OIDC delivery cannot be enabled without verified OIDC receiver")
if _env_bool("KUUOS_MCP_GITHUB_OIDC_ENABLED"):
    from .github_oidc_source import install_oidc_source_route

    oidc_delivery_loaded = _env_bool("KUUOS_MCP_GITHUB_OIDC_DELIVERY_ENABLED")
    if oidc_delivery_loaded:
        if event_subscription_manager is None:
            raise RuntimeError("OIDC delivery requires authenticated MCP Events")
        from .event_outbox import PostgresOutboxStore

        oidc_outbox = PostgresOutboxStore(store.database_url)
    else:
        oidc_outbox = None
    install_oidc_source_route(
        mcp, store, manager=event_subscription_manager if oidc_delivery_loaded else None,
        outbox=oidc_outbox, deliver_inline=oidc_delivery_loaded,
    )
    github_oidc_source_loaded = True


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
