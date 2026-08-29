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
from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions
from pydantic import AnyHttpUrl

from .embedded_oauth import EmbeddedPostgresOAuthProvider


def normalize_scopes(value: Any) -> list[str]:
    if isinstance(value, str):
        return [scope for scope in value.split() if scope]
    if isinstance(value, list) and all(isinstance(scope, str) for scope in value):
        return [scope for scope in value if scope]
    return []


def token_scopes(payload: dict[str, Any]) -> list[str]:
    """Normalize OAuth scope claims used by common authorization servers."""
    scopes = normalize_scopes(payload.get("scope"))
    if scopes:
        return scopes
    return normalize_scopes(payload.get("scp"))


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


def token_client_id(payload: dict[str, Any]) -> str:
    client_id = payload.get("client_id")
    if isinstance(client_id, str) and client_id:
        return client_id
    authorized_party = payload.get("azp")
    if isinstance(authorized_party, str) and authorized_party:
        return authorized_party
    return "oauth-client"


def token_subject(payload: dict[str, Any]) -> str | None:
    subject = payload.get("sub")
    return subject if isinstance(subject, str) else None


def token_expiry(payload: dict[str, Any]) -> int | None:
    expires_at = payload.get("exp")
    return expires_at if isinstance(expires_at, int) else None


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

        return AccessToken(
            token=token,
            client_id=token_client_id(payload),
            scopes=token_scopes(payload),
            expires_at=token_expiry(payload),
            resource=self.expected_audience,
            subject=token_subject(payload),
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
                "User-Agent": "KuuOS-MCP-State-Bridge/0.5",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            payload = json.load(response)
        if not isinstance(payload, dict):
            raise ValueError("OAuth introspection response must be a JSON object")
        return payload


class JWKSTokenVerifier(TokenVerifier):
    """Fail-closed OIDC JWT verifier backed by an HTTPS JWKS endpoint."""

    def __init__(
        self,
        jwks_url: str,
        *,
        issuer: str,
        expected_audience: str | None,
        timeout_seconds: float = 8.0,
    ):
        if not jwks_url.startswith("https://"):
            raise ValueError("OAuth JWKS URL must use HTTPS")
        if not issuer.startswith("https://"):
            raise ValueError("OAuth issuer must use HTTPS")
        self.jwks_url = jwks_url
        self.issuer = issuer.rstrip("/")
        self.expected_audience = expected_audience
        self.timeout_seconds = timeout_seconds

    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            payload = await asyncio.to_thread(self._decode, token)
        except Exception:
            return None
        if not audience_allows(payload, self.expected_audience):
            return None
        return AccessToken(
            token=token,
            client_id=token_client_id(payload),
            scopes=token_scopes(payload),
            expires_at=token_expiry(payload),
            resource=self.expected_audience,
            subject=token_subject(payload),
            claims=payload,
        )

    def _decode(self, token: str) -> dict[str, Any]:
        try:
            import jwt
        except ImportError as exc:  # pragma: no cover - deployment packaging guard
            raise RuntimeError(
                "JWKS OAuth mode requires `pip install 'PyJWT[crypto]>=2.10,<3'`"
            ) from exc

        jwks_client = jwt.PyJWKClient(
            self.jwks_url,
            timeout=self.timeout_seconds,
        )
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        algorithm = getattr(signing_key, "algorithm_name", None)
        if not isinstance(algorithm, str) or not algorithm:
            raise ValueError("JWKS signing key did not declare an algorithm")
        if algorithm.lower() == "none":
            raise ValueError("unsigned JWT access tokens are not accepted")

        options = {"verify_aud": self.expected_audience is not None}
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=[algorithm],
            audience=self.expected_audience,
            issuer=self.issuer,
            options=options,
        )
        if not isinstance(payload, dict):
            raise ValueError("OAuth JWT payload must be a JSON object")
        return payload


@dataclass(frozen=True)
class OAuthConfig:
    token_verifier: TokenVerifier | None
    embedded_provider: EmbeddedPostgresOAuthProvider | None
    auth_settings: AuthSettings
    read_scope: str
    write_scope: str
    token_mode: str


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
    token_mode = os.environ.get(
        "KUUOS_MCP_OAUTH_TOKEN_MODE", "introspection"
    ).strip().lower()
    read_scope = os.environ.get("KUUOS_MCP_OAUTH_READ_SCOPE", "kuuos:read").strip()
    write_scope = os.environ.get("KUUOS_MCP_OAUTH_WRITE_SCOPE", "kuuos:write").strip()
    audience = os.environ.get("KUUOS_MCP_OAUTH_AUDIENCE", resource_url).strip()

    if not issuer.startswith("https://"):
        raise RuntimeError("KUUOS_MCP_OAUTH_ISSUER must use HTTPS")
    if not resource_url.startswith("https://"):
        raise RuntimeError("KUUOS_MCP_OAUTH_RESOURCE_URL must use HTTPS")
    if not read_scope or not write_scope:
        raise RuntimeError("OAuth read/write scopes must be non-empty")

    verifier: TokenVerifier | None = None
    embedded_provider: EmbeddedPostgresOAuthProvider | None = None
    client_registration_options: ClientRegistrationOptions | None = None
    revocation_options: RevocationOptions | None = None

    if token_mode == "introspection":
        verifier = IntrospectionTokenVerifier(
            _required_env("KUUOS_MCP_OAUTH_INTROSPECTION_URL"),
            client_id=_required_env("KUUOS_MCP_OAUTH_INTROSPECTION_CLIENT_ID"),
            client_secret=_required_env(
                "KUUOS_MCP_OAUTH_INTROSPECTION_CLIENT_SECRET"
            ),
            expected_audience=audience or None,
        )
    elif token_mode == "jwks":
        verifier = JWKSTokenVerifier(
            _required_env("KUUOS_MCP_OAUTH_JWKS_URL"),
            issuer=issuer,
            expected_audience=audience or None,
        )
    elif token_mode == "embedded":
        database_url = (
            os.environ.get("KUUOS_MCP_DATABASE_URL")
            or os.environ.get("DATABASE_URL")
            or ""
        ).strip()
        if not database_url:
            raise RuntimeError("embedded OAuth mode requires KUUOS_MCP_DATABASE_URL or DATABASE_URL")
        owner_secret = _required_env("KUUOS_MCP_EMBEDDED_AUTH_SECRET")
        if len(owner_secret) < 24:
            raise RuntimeError("KUUOS_MCP_EMBEDDED_AUTH_SECRET must be at least 24 characters")
        embedded_provider = EmbeddedPostgresOAuthProvider(
            database_url,
            issuer=issuer,
            resource_url=resource_url,
            owner_secret=owner_secret,
            owner_subject=os.environ.get(
                "KUUOS_MCP_EMBEDDED_AUTH_SUBJECT", "kuuos-owner"
            ).strip()
            or "kuuos-owner",
        )
        default_scopes = [read_scope]
        if os.environ.get("KUUOS_MCP_WRITE_ENABLED", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            default_scopes.append(write_scope)
        client_registration_options = ClientRegistrationOptions(
            enabled=True,
            valid_scopes=[read_scope, write_scope],
            default_scopes=default_scopes,
        )
        revocation_options = RevocationOptions(enabled=True)
    else:
        raise RuntimeError(
            "KUUOS_MCP_OAUTH_TOKEN_MODE must be 'introspection', 'jwks', or 'embedded'"
        )

    return OAuthConfig(
        token_verifier=verifier,
        embedded_provider=embedded_provider,
        auth_settings=AuthSettings(
            issuer_url=AnyHttpUrl(issuer),
            resource_server_url=AnyHttpUrl(resource_url),
            required_scopes=[read_scope],
            client_registration_options=client_registration_options,
            revocation_options=revocation_options,
        ),
        read_scope=read_scope,
        write_scope=write_scope,
        token_mode=token_mode,
    )
