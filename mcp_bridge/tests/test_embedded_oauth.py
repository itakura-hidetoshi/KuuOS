from __future__ import annotations

import asyncio
import hashlib
import json
from types import SimpleNamespace

import pytest
from mcp.server.auth.provider import (
    AuthorizationCode,
    AuthorizationParams,
    AuthorizeError,
    TokenError,
)

from kuuos_mcp_bridge.embedded_oauth import EmbeddedPostgresOAuthProvider


ISSUER = "https://mcp.example.com"
RESOURCE = "https://mcp.example.com/mcp"


def _provider() -> EmbeddedPostgresOAuthProvider:
    provider = object.__new__(EmbeddedPostgresOAuthProvider)
    provider.issuer = ISSUER
    provider.resource_url = RESOURCE
    provider.owner_subject = "kuuos-owner"
    provider.access_ttl_seconds = 3600
    provider.refresh_ttl_seconds = 30 * 24 * 3600
    return provider


def _authorization_params(resource: str | None) -> AuthorizationParams:
    return AuthorizationParams(
        state="oauth-state",
        scopes=["kuuos:read"],
        code_challenge="challenge",
        redirect_uri="https://client.example/callback",
        redirect_uri_provided_explicitly=True,
        resource=resource,
    )


def test_embedded_authorize_requires_exact_rfc8707_resource() -> None:
    provider = _provider()
    client = SimpleNamespace(client_id="client-a")

    with pytest.raises(AuthorizeError) as missing:
        asyncio.run(provider.authorize(client, _authorization_params(None)))
    assert missing.value.error == "invalid_target"

    with pytest.raises(AuthorizeError) as mismatch:
        asyncio.run(
            provider.authorize(
                client,
                _authorization_params("https://other.example/mcp"),
            )
        )
    assert mismatch.value.error == "invalid_target"


def test_embedded_authorize_persists_only_canonical_resource() -> None:
    provider = _provider()
    stored: list[tuple[str, str, dict[str, object], float | None]] = []

    def put(
        kind: str,
        item_key: str,
        payload: dict[str, object],
        *,
        expires_at: float | None = None,
    ) -> None:
        stored.append((kind, item_key, payload, expires_at))

    provider._put = put
    client = SimpleNamespace(client_id="client-a")

    redirect = asyncio.run(provider.authorize(client, _authorization_params(RESOURCE)))

    assert redirect.startswith(f"{ISSUER}/login?state=")
    assert len(stored) == 1
    kind, _, payload, expires_at = stored[0]
    assert kind == "pending"
    assert payload["resource"] == RESOURCE
    assert expires_at is not None


def test_authorization_code_is_hash_indexed_and_restored_from_presented_secret() -> None:
    provider = _provider()
    stored: dict[tuple[str, str], dict[str, object]] = {}

    def put(
        kind: str,
        item_key: str,
        payload: dict[str, object],
        *,
        expires_at: float | None = None,
    ) -> None:
        del expires_at
        stored[(kind, item_key)] = payload

    provider._put = put
    raw_code = "kuuos_code_super-secret-code"
    code = AuthorizationCode(
        code=raw_code,
        scopes=["kuuos:read"],
        expires_at=4_000_000_000,
        client_id="client-a",
        code_challenge="challenge",
        redirect_uri="https://client.example/callback",
        redirect_uri_provided_explicitly=True,
        resource=RESOURCE,
        subject="kuuos-owner",
    )

    asyncio.run(provider._store_authorization_code(code))

    key = hashlib.sha256(raw_code.encode("utf-8")).hexdigest()
    payload = stored[("code", key)]
    assert raw_code not in json.dumps(payload, sort_keys=True)
    assert "code" not in payload

    def get(kind: str, item_key: str):
        return stored.get((kind, item_key))

    provider._get = get
    loaded = asyncio.run(
        provider.load_authorization_code(SimpleNamespace(client_id="client-a"), raw_code)
    )
    assert loaded is not None
    assert loaded.code == raw_code
    assert loaded.resource == RESOURCE


def test_access_and_refresh_credentials_are_hash_only_at_rest() -> None:
    provider = _provider()
    stored: dict[tuple[str, str], dict[str, object]] = {}

    def put(
        kind: str,
        item_key: str,
        payload: dict[str, object],
        *,
        expires_at: float | None = None,
    ) -> None:
        del expires_at
        stored[(kind, item_key)] = payload

    provider._put = put
    issued = asyncio.run(
        provider._issue_pair(
            client_id="client-a",
            scopes=["kuuos:read", "kuuos:write"],
            resource=RESOURCE,
            subject="kuuos-owner",
        )
    )

    assert issued.refresh_token is not None
    access_key = hashlib.sha256(issued.access_token.encode("utf-8")).hexdigest()
    refresh_key = hashlib.sha256(issued.refresh_token.encode("utf-8")).hexdigest()
    access_payload = stored[("access", access_key)]
    refresh_payload = stored[("refresh", refresh_key)]

    serialized = json.dumps(
        {"access": access_payload, "refresh": refresh_payload},
        sort_keys=True,
    )
    assert issued.access_token not in serialized
    assert issued.refresh_token not in serialized
    assert "token" not in access_payload["token"]
    assert "token" not in refresh_payload["token"]
    assert refresh_payload["resource"] == RESOURCE

    def get(kind: str, item_key: str):
        return stored.get((kind, item_key))

    provider._get = get
    access = asyncio.run(provider.load_access_token(issued.access_token))
    refresh = asyncio.run(
        provider.load_refresh_token(
            SimpleNamespace(client_id="client-a"),
            issued.refresh_token,
        )
    )

    assert access is not None
    assert access.token == issued.access_token
    assert access.resource == RESOURCE
    assert refresh is not None
    assert refresh.token == issued.refresh_token


def test_pair_issuance_rejects_noncanonical_resource_before_persistence() -> None:
    provider = _provider()
    provider._put = lambda *args, **kwargs: pytest.fail("credential must not persist")

    with pytest.raises(TokenError) as exc:
        asyncio.run(
            provider._issue_pair(
                client_id="client-a",
                scopes=["kuuos:read"],
                resource="https://other.example/mcp",
                subject="kuuos-owner",
            )
        )
    assert exc.value.error == "invalid_target"


def test_pinned_mcp_public_client_revocation_requires_client_secret_form_field():
    """Source-backed v2.3.0 protocol parser quirk; NOT authentication authority.

    The public client has no client secret. The installed MCP SDK parser
    treats nullable client_secret without a default as a required form field.
    Sending an empty string is a client-side compatibility workaround;
    it is not a credential and must not weaken server client authentication.
    """
    from importlib.metadata import version

    from mcp.server.auth.handlers.revoke import RevocationRequest
    from pydantic import ValidationError

    assert version("mcp") == "2.3.0"
    client = {
        "token": "synthetic-token-not-valid-on-any-server",
        "client_id": "synthetic-public-client",
        "token_type_hint": "access_token",
    }
    with pytest.raises(ValidationError) as missing:
        RevocationRequest.model_validate(client)
    assert any(
        error["loc"] == ("client_secret",)
        for error in missing.value.errors()
    )

    parsed = RevocationRequest.model_validate({
        **client, "client_secret": "",
    })
    assert parsed.client_id == client["client_id"]
    assert parsed.client_secret == ""


def test_embedded_provider_revokes_access_and_refresh_pair_together() -> None:
    """Provider revocation closes a pair under a synthetic in-memory fixture."""
    from mcp.server.auth.provider import AccessToken

    provider = _provider()
    deleted: list[str] = []
    record = {"pair_id": "synthetic-pair-never-in-a-database"}

    def synthetic_get(kind: str, item_key: str):
        if kind == "access" and item_key == provider._token_key(
            "synthetic-never-issued-access"
        ):
            return record
        return None

    provider._get = synthetic_get
    provider._delete_pair = deleted.append
    credential = AccessToken(
        token="synthetic-never-issued-access",
        client_id="synthetic-public-client",
        scopes=["kuuos:read"],
        expires_at=4_000_000_000,
        resource=RESOURCE,
        subject="kuuos-owner",
    )
    asyncio.run(provider.revoke_token(credential))
    assert deleted == ["synthetic-pair-never-in-a-database"]

def test_old_owner_credentials_fail_closed_after_subject_rotation() -> None:
    """Retained synthetic grants cannot authorize a replacement owner."""
    provider = _provider()
    records: dict[tuple[str, str], dict[str, object]] = {}

    def put(kind: str, key: str, payload: dict[str, object], *,
            expires_at: float | None = None) -> None:
        del expires_at
        records[(kind, key)] = payload

    provider._put = put
    provider._get = lambda kind, key: records.get((kind, key))
    provider._pop = lambda kind, key: records.pop((kind, key), None)
    pair = asyncio.run(provider._issue_pair(
        client_id="client-a", scopes=["kuuos:read"],
        resource=RESOURCE, subject="kuuos-owner",
    ))
    assert pair.refresh_token is not None
    client = SimpleNamespace(client_id="client-a")
    refresh = asyncio.run(provider.load_refresh_token(client, pair.refresh_token))
    assert refresh is not None
    assert asyncio.run(provider.load_access_token(pair.access_token)) is not None

    # Operator changes the owner subject when replacing the synthetic
    # staging owner secret; no destructive database mutation is needed.
    provider.owner_subject = "kuuos-human-owner-v1"
    assert asyncio.run(provider.load_access_token(pair.access_token)) is None
    assert asyncio.run(provider.load_refresh_token(client, pair.refresh_token)) is None
    with pytest.raises(TokenError) as invalid_refresh:
        asyncio.run(provider.exchange_refresh_token(client, refresh, ["kuuos:read"]))
    assert invalid_refresh.value.error == "invalid_grant"
    with pytest.raises(TokenError) as invalid_code:
        asyncio.run(provider._issue_pair(
            client_id="client-a", scopes=["kuuos:read"],
            resource=RESOURCE, subject="kuuos-owner",
        ))
    assert invalid_code.value.error == "invalid_grant"

