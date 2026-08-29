from __future__ import annotations

import asyncio
import base64
import json
import os
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl


def normalize_scopes(value: Any) -> list[str]:
    if isinstance(value, str):
        return [scope for scope in value.split() if scope]
    if isinstance(value, list) and all(isinstance(scope, str) for scope in value):
        return [scope for scope in value if scope]
    return []


def audience_allows(payload: dict[str, Any], expected_audience: str | None) -> bool:
    if expected_audience is None:
        return True
    audience = payload.get("aud")
    resource = payload.get("resource")
    candidates: list[str] = []
    if isinstance(audience, str):
        candidates.append(audience)
    elif isinstance(audience, list):
        candidates.extend(item for item in audience if isinstance(item, str))
    if isinstance(resource, str):
        candidates.append(resource)
    elif isinstance(resource, list):
        candidates.extend(item for item in resource if isinstance(item, str))
    return expected_audience in candidates


class IntrospectionTokenVerifier(TokenVerifier):
    """RFC 7662 verifier for an external OAuth/OIDC authorization server."""

    def __init__(
        self,
        introspection_url: str,
        *,
        client_id: str,
        client_secret: str,
        expected_audience: str | None,
        timeout_seconds: float = 8.0,
    ):
        if not introspection_url.startswith("https://"):
            raise ValueError("OAuth introspection URL must use HTTPS")
        self.introspection_url = introspection_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.expected_audience = expected_audience
        self.timeout_seconds = timeout_seconds

    async def verify_token(self, token: str) -> AccessToken | None:
        payload = await asyncio.to_thread(self._introspect, token)
        if payload.get("active") is not True:
            return None
        if not audience_allows(payload, self.expected_audience):
            return None

        scopes = normalize_scopes(payload.get("scope"))
        client_id = payload.get("client_id")
        if not isinstance(client_id, str) or not client_id:
            client_id = "oauth-client"

        expires_at = payload.get("exp")
        if not isinstance(expires_at, int):
            expires_at = None

        subject = payload.get("sub")
        if not isinstance(subject, str):
            subject = None

        return AccessToken(
            token=token,
            client_id=client_id,
            scopes=scopes,
            expires_at=expires_at,
            resource=self.expected_audience,
            subject=subject,
            claims=payload,
        )

    def _introspect(self, token: str) -> dict[str, Any]:
        body = urllib.parse.urlencode(
            {"token": token, "token_type_hint": "access_token"}
        ).encode("utf-8")
        credentials = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode("utf-8")
        ).decode("ascii")
        request = urllib.request.Request(
            self.introspection_url,
            data=body,
            headers={
                "Accept": "application/json",
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "KuuOS-MCP-State-Bridge/0.3",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            payload = json.load(response)
        if not isinstance(payload, dict):
            raise ValueError("OAuth introspection response must be a JSON object")
        return payload


@dataclass(frozen=True)
class OAuthConfig:
    token_verifier: TokenVerifier
    auth_settings: AuthSettings
    read_scope: str
    write_scope: str


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is required when KUUOS_MCP_OAUTH_ENABLED=true")
    return value


def build_oauth_config() -> OAuthConfig | None:
    enabled = os.environ.get("KUUOS_MCP_OAUTH_ENABLED", "").strip().lower()
    if enabled not in {"1", "true", "yes", "on"}:
        return None

    issuer = _required_env("KUUOS_MCP_OAUTH_ISSUER")
    resource_url = _required_env("KUUOS_MCP_OAUTH_RESOURCE_URL")
    introspection_url = _required_env("KUUOS_MCP_OAUTH_INTROSPECTION_URL")
    client_id = _required_env("KUUOS_MCP_OAUTH_INTROSPECTION_CLIENT_ID")
    client_secret = _required_env("KUUOS_MCP_OAUTH_INTROSPECTION_CLIENT_SECRET")
    read_scope = os.environ.get("KUUOS_MCP_OAUTH_READ_SCOPE", "kuuos:read").strip()
    write_scope = os.environ.get("KUUOS_MCP_OAUTH_WRITE_SCOPE", "kuuos:write").strip()
    audience = os.environ.get("KUUOS_MCP_OAUTH_AUDIENCE", resource_url).strip()

    if not issuer.startswith("https://"):
        raise RuntimeError("KUUOS_MCP_OAUTH_ISSUER must use HTTPS")
    if not resource_url.startswith("https://"):
        raise RuntimeError("KUUOS_MCP_OAUTH_RESOURCE_URL must use HTTPS")
    if not read_scope or not write_scope:
        raise RuntimeError("OAuth read/write scopes must be non-empty")

    verifier = IntrospectionTokenVerifier(
        introspection_url,
        client_id=client_id,
        client_secret=client_secret,
        expected_audience=audience or None,
    )
    return OAuthConfig(
        token_verifier=verifier,
        auth_settings=AuthSettings(
            issuer_url=AnyHttpUrl(issuer),
            resource_server_url=AnyHttpUrl(resource_url),
            required_scopes=[read_scope],
        ),
        read_scope=read_scope,
        write_scope=write_scope,
    )
