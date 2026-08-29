from __future__ import annotations

import asyncio
import hashlib
import html
import secrets
import time
import urllib.parse
from typing import Any

from mcp.server.auth.provider import (
    AccessToken,
    AuthorizationCode,
    AuthorizationParams,
    AuthorizeError,
    OAuthAuthorizationServerProvider,
    RefreshToken,
    TokenError,
    construct_redirect_uri,
)
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response


class EmbeddedPostgresOAuthProvider(
    OAuthAuthorizationServerProvider[AuthorizationCode, RefreshToken, AccessToken]
):
    """Single-owner OAuth 2.1 fallback with PostgreSQL-backed durable state.

    This provider is deliberately opt-in. It is intended for deployments where an
    external authorization server is unavailable but PostgreSQL and encrypted
    deployment secrets are available. OAuth clients and pending authorization state
    are shared through PostgreSQL so replicated HTTP workers do not rely on
    process-local memory. Authorization codes, access tokens, and refresh tokens are
    indexed only by SHA-256 credential digests; raw credentials are never persisted.
    """

    _TABLE = "kuuos_mcp_oauth"

    def __init__(
        self,
        database_url: str,
        *,
        issuer: str,
        resource_url: str,
        owner_secret: str,
        owner_subject: str = "kuuos-owner",
        access_ttl_seconds: int = 3600,
        refresh_ttl_seconds: int = 30 * 24 * 3600,
    ):
        if not database_url:
            raise ValueError("embedded OAuth requires a PostgreSQL database URL")
        if not issuer.startswith("https://"):
            raise ValueError("embedded OAuth issuer must use HTTPS")
        if not resource_url.startswith("https://"):
            raise ValueError("embedded OAuth resource URL must use HTTPS")
        if len(owner_secret) < 24:
            raise ValueError("embedded OAuth owner secret must be at least 24 characters")
        self.database_url = database_url
        self.issuer = issuer.rstrip("/")
        self.resource_url = resource_url
        self.owner_secret = owner_secret
        self.owner_subject = owner_subject
        self.access_ttl_seconds = access_ttl_seconds
        self.refresh_ttl_seconds = refresh_ttl_seconds
        self._ensure_schema()

    def _connect(self):
        try:
            import psycopg
        except ImportError as exc:  # pragma: no cover - deployment packaging guard
            raise RuntimeError(
                "embedded OAuth requires `pip install 'kuuos-mcp-bridge[postgres]'`"
            ) from exc
        return psycopg.connect(self.database_url)

    @staticmethod
    def _jsonb(value: dict[str, Any]):
        try:
            from psycopg.types.json import Jsonb
        except ImportError as exc:  # pragma: no cover - deployment packaging guard
            raise RuntimeError(
                "embedded OAuth requires `pip install 'kuuos-mcp-bridge[postgres]'`"
            ) from exc
        return Jsonb(value)

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self._TABLE} (
                    kind TEXT NOT NULL,
                    item_key TEXT NOT NULL,
                    payload JSONB NOT NULL,
                    expires_at DOUBLE PRECISION,
                    PRIMARY KEY (kind, item_key)
                )
                """
            )
            conn.execute(
                f"CREATE INDEX IF NOT EXISTS {self._TABLE}_expiry_idx "
                f"ON {self._TABLE} (expires_at)"
            )

    @staticmethod
    def _token_key(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def _dump_without_secret(model: Any, field: str) -> dict[str, Any]:
        payload = dict(model.model_dump(mode="json"))
        payload.pop(field, None)
        return payload

    @staticmethod
    def _restore_secret(
        payload: dict[str, Any], field: str, value: str
    ) -> dict[str, Any]:
        restored = dict(payload)
        restored[field] = value
        return restored

    def _require_authorization_resource(self, resource: str | None) -> str:
        if resource != self.resource_url:
            raise AuthorizeError(
                error="invalid_target",
                error_description="OAuth resource must exactly match the configured MCP resource",
            )
        return self.resource_url

    def _require_token_resource(self, resource: str | None) -> str:
        if resource != self.resource_url:
            raise TokenError(
                error="invalid_target",
                error_description="OAuth resource must exactly match the configured MCP resource",
            )
        return self.resource_url

    def _put(
        self,
        kind: str,
        item_key: str,
        payload: dict[str, Any],
        *,
        expires_at: float | None = None,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                f"""
                INSERT INTO {self._TABLE} (kind, item_key, payload, expires_at)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (kind, item_key)
                DO UPDATE SET payload = EXCLUDED.payload, expires_at = EXCLUDED.expires_at
                """,
                (kind, item_key, self._jsonb(payload), expires_at),
            )

    def _get(self, kind: str, item_key: str) -> dict[str, Any] | None:
        now = time.time()
        with self._connect() as conn:
            row = conn.execute(
                f"SELECT payload, expires_at FROM {self._TABLE} "
                "WHERE kind = %s AND item_key = %s",
                (kind, item_key),
            ).fetchone()
            if row is None:
                return None
            payload, expires_at = row
            if expires_at is not None and expires_at <= now:
                conn.execute(
                    f"DELETE FROM {self._TABLE} WHERE kind = %s AND item_key = %s",
                    (kind, item_key),
                )
                return None
            return dict(payload)

    def _pop(self, kind: str, item_key: str) -> dict[str, Any] | None:
        now = time.time()
        with self._connect() as conn:
            row = conn.execute(
                f"DELETE FROM {self._TABLE} WHERE kind = %s AND item_key = %s "
                "RETURNING payload, expires_at",
                (kind, item_key),
            ).fetchone()
        if row is None:
            return None
        payload, expires_at = row
        if expires_at is not None and expires_at <= now:
            return None
        return dict(payload)

    def _delete_pair(self, pair_id: str) -> None:
        with self._connect() as conn:
            conn.execute(
                f"DELETE FROM {self._TABLE} "
                "WHERE kind IN ('access', 'refresh') AND payload ->> 'pair_id' = %s",
                (pair_id,),
            )

    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        payload = await asyncio.to_thread(self._get, "client", client_id)
        if payload is None:
            return None
        return OAuthClientInformationFull.model_validate(payload)

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        if not client_info.client_id:
            raise ValueError("OAuth client_id is required")
        await asyncio.to_thread(
            self._put,
            "client",
            client_info.client_id,
            client_info.model_dump(mode="json"),
        )

    async def authorize(
        self,
        client: OAuthClientInformationFull,
        params: AuthorizationParams,
    ) -> str:
        if not client.client_id:
            raise ValueError("OAuth client_id is required")
        resource = self._require_authorization_resource(params.resource)
        login_state = secrets.token_urlsafe(32)
        expires_at = time.time() + 300
        requested_scopes = list(params.scopes or [])
        pending = {
            "oauth_state": params.state,
            "redirect_uri": str(params.redirect_uri),
            "redirect_uri_provided_explicitly": params.redirect_uri_provided_explicitly,
            "code_challenge": params.code_challenge,
            "client_id": client.client_id,
            "resource": resource,
            "scopes": requested_scopes,
        }
        await asyncio.to_thread(
            self._put,
            "pending",
            login_state,
            pending,
            expires_at=expires_at,
        )
        return f"{self.issuer}/login?state={urllib.parse.quote(login_state, safe='')}"

    async def login_page(self, request: Request) -> Response:
        state = request.query_params.get("state", "")
        if not state or await asyncio.to_thread(self._get, "pending", state) is None:
            raise HTTPException(400, "Invalid or expired authorization state")
        escaped_state = html.escape(state, quote=True)
        return HTMLResponse(
            "<!doctype html><html><head><meta charset='utf-8'>"
            "<title>KuuOS MCP authorization</title></head><body>"
            "<h2>KuuOS MCP authorization</h2>"
            "<p>Enter the deployment owner secret to authorize this MCP client.</p>"
            f"<form method='post' action='{html.escape(self.issuer, quote=True)}/login/callback'>"
            f"<input type='hidden' name='state' value='{escaped_state}'>"
            "<label>Owner secret <input type='password' name='secret' required autocomplete='current-password'></label>"
            "<button type='submit'>Authorize</button></form></body></html>"
        )

    async def _store_authorization_code(self, auth_code: AuthorizationCode) -> None:
        await asyncio.to_thread(
            self._put,
            "code",
            self._token_key(auth_code.code),
            self._dump_without_secret(auth_code, "code"),
            expires_at=auth_code.expires_at,
        )

    async def login_callback(self, request: Request) -> Response:
        raw = (await request.body()).decode("utf-8")
        fields = urllib.parse.parse_qs(raw, keep_blank_values=True)
        state = (fields.get("state") or [""])[0]
        submitted = (fields.get("secret") or [""])[0]
        if not state or not submitted:
            raise HTTPException(400, "Missing authorization credentials")

        pending = await asyncio.to_thread(self._pop, "pending", state)
        if pending is None:
            raise HTTPException(400, "Invalid or expired authorization state")
        if not secrets.compare_digest(submitted, self.owner_secret):
            raise HTTPException(401, "Invalid authorization credentials")

        resource = pending.get("resource")
        if not isinstance(resource, str):
            raise HTTPException(400, "Invalid authorization resource")
        try:
            resource = self._require_token_resource(resource)
        except TokenError as exc:
            raise HTTPException(400, "Invalid authorization resource") from exc

        code = f"kuuos_code_{secrets.token_urlsafe(32)}"
        scopes = [scope for scope in pending.get("scopes", []) if isinstance(scope, str)]
        auth_code = AuthorizationCode(
            code=code,
            scopes=scopes,
            expires_at=time.time() + 300,
            client_id=str(pending["client_id"]),
            code_challenge=str(pending["code_challenge"]),
            redirect_uri=str(pending["redirect_uri"]),
            redirect_uri_provided_explicitly=bool(
                pending["redirect_uri_provided_explicitly"]
            ),
            resource=resource,
            subject=self.owner_subject,
        )
        await self._store_authorization_code(auth_code)
        return RedirectResponse(
            construct_redirect_uri(
                str(auth_code.redirect_uri),
                code=code,
                state=pending.get("oauth_state"),
            ),
            status_code=302,
        )

    async def load_authorization_code(
        self,
        client: OAuthClientInformationFull,
        authorization_code: str,
    ) -> AuthorizationCode | None:
        payload = await asyncio.to_thread(
            self._get, "code", self._token_key(authorization_code)
        )
        if payload is None:
            return None
        code = AuthorizationCode.model_validate(
            self._restore_secret(payload, "code", authorization_code)
        )
        if code.client_id != client.client_id or code.resource != self.resource_url:
            return None
        return code

    async def exchange_authorization_code(
        self,
        client: OAuthClientInformationFull,
        authorization_code: AuthorizationCode,
    ) -> OAuthToken:
        payload = await asyncio.to_thread(
            self._pop, "code", self._token_key(authorization_code.code)
        )
        if payload is None:
            raise TokenError(
                error="invalid_grant",
                error_description="authorization code is invalid or expired",
            )
        stored = AuthorizationCode.model_validate(
            self._restore_secret(payload, "code", authorization_code.code)
        )
        if stored.client_id != client.client_id:
            raise TokenError(
                error="invalid_grant",
                error_description="authorization code client mismatch",
            )
        resource = self._require_token_resource(stored.resource)
        return await self._issue_pair(
            client_id=stored.client_id,
            scopes=stored.scopes,
            resource=resource,
            subject=stored.subject,
        )

    async def _issue_pair(
        self,
        *,
        client_id: str,
        scopes: list[str],
        resource: str | None,
        subject: str | None,
    ) -> OAuthToken:
        resource = self._require_token_resource(resource)
        now = int(time.time())
        pair_id = secrets.token_urlsafe(24)
        access_value = f"kuuos_at_{secrets.token_urlsafe(32)}"
        refresh_value = f"kuuos_rt_{secrets.token_urlsafe(32)}"
        access = AccessToken(
            token=access_value,
            client_id=client_id,
            scopes=scopes,
            expires_at=now + self.access_ttl_seconds,
            resource=resource,
            subject=subject,
            claims={"iss": self.issuer},
        )
        refresh = RefreshToken(
            token=refresh_value,
            client_id=client_id,
            scopes=scopes,
            expires_at=now + self.refresh_ttl_seconds,
            subject=subject,
        )
        await asyncio.to_thread(
            self._put,
            "access",
            self._token_key(access_value),
            {
                "pair_id": pair_id,
                "token": self._dump_without_secret(access, "token"),
            },
            expires_at=access.expires_at,
        )
        await asyncio.to_thread(
            self._put,
            "refresh",
            self._token_key(refresh_value),
            {
                "pair_id": pair_id,
                "resource": resource,
                "token": self._dump_without_secret(refresh, "token"),
            },
            expires_at=refresh.expires_at,
        )
        return OAuthToken(
            access_token=access_value,
            token_type="Bearer",
            expires_in=self.access_ttl_seconds,
            refresh_token=refresh_value,
            scope=" ".join(scopes),
        )

    async def load_access_token(self, token: str) -> AccessToken | None:
        wrapper = await asyncio.to_thread(self._get, "access", self._token_key(token))
        if wrapper is None:
            return None
        payload = wrapper.get("token")
        if not isinstance(payload, dict):
            return None
        access = AccessToken.model_validate(
            self._restore_secret(payload, "token", token)
        )
        if access.resource != self.resource_url:
            return None
        if access.expires_at is not None and access.expires_at <= time.time():
            return None
        return access

    async def load_refresh_token(
        self,
        client: OAuthClientInformationFull,
        refresh_token: str,
    ) -> RefreshToken | None:
        wrapper = await asyncio.to_thread(
            self._get, "refresh", self._token_key(refresh_token)
        )
        if wrapper is None or wrapper.get("resource") != self.resource_url:
            return None
        payload = wrapper.get("token")
        if not isinstance(payload, dict):
            return None
        refresh = RefreshToken.model_validate(
            self._restore_secret(payload, "token", refresh_token)
        )
        if refresh.client_id != client.client_id:
            return None
        return refresh

    async def exchange_refresh_token(
        self,
        client: OAuthClientInformationFull,
        refresh_token: RefreshToken,
        scopes: list[str],
    ) -> OAuthToken:
        wrapper = await asyncio.to_thread(
            self._pop, "refresh", self._token_key(refresh_token.token)
        )
        if wrapper is None:
            raise TokenError(
                error="invalid_grant",
                error_description="refresh token is invalid or expired",
            )
        resource = wrapper.get("resource")
        if not isinstance(resource, str):
            raise TokenError(
                error="invalid_target",
                error_description="refresh token resource is missing",
            )
        resource = self._require_token_resource(resource)
        payload = wrapper.get("token")
        if not isinstance(payload, dict):
            raise TokenError(
                error="invalid_grant",
                error_description="refresh token metadata is invalid",
            )
        stored = RefreshToken.model_validate(
            self._restore_secret(payload, "token", refresh_token.token)
        )
        if stored.client_id != client.client_id:
            raise TokenError(
                error="invalid_grant",
                error_description="refresh token client mismatch",
            )
        requested = scopes or stored.scopes
        if not set(requested).issubset(stored.scopes):
            raise TokenError(
                error="invalid_scope",
                error_description="refresh requested an ungranted scope",
            )
        pair_id = wrapper.get("pair_id")
        if isinstance(pair_id, str):
            await asyncio.to_thread(self._delete_pair, pair_id)
        return await self._issue_pair(
            client_id=stored.client_id,
            scopes=requested,
            resource=resource,
            subject=stored.subject,
        )

    async def revoke_token(self, token: AccessToken | RefreshToken) -> None:
        kind = "access" if isinstance(token, AccessToken) else "refresh"
        wrapper = await asyncio.to_thread(self._get, kind, self._token_key(token.token))
        if wrapper is None:
            return
        pair_id = wrapper.get("pair_id")
        if isinstance(pair_id, str):
            await asyncio.to_thread(self._delete_pair, pair_id)
