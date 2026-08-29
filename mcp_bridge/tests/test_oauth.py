from __future__ import annotations

import pytest

import kuuos_mcp_bridge.oauth as oauth_module
from kuuos_mcp_bridge.oauth import (
    JWKSTokenVerifier,
    audience_allows,
    build_oauth_config,
    normalize_scopes,
    token_client_id,
    token_scopes,
)


def test_normalize_scopes_accepts_space_separated_string() -> None:
    assert normalize_scopes("kuuos:read kuuos:write") == [
        "kuuos:read",
        "kuuos:write",
    ]


def test_normalize_scopes_accepts_string_list() -> None:
    assert normalize_scopes(["kuuos:read", "kuuos:write"]) == [
        "kuuos:read",
        "kuuos:write",
    ]


def test_token_scopes_supports_standard_and_oidc_style_claims() -> None:
    assert token_scopes({"scope": "kuuos:read kuuos:write"}) == [
        "kuuos:read",
        "kuuos:write",
    ]
    assert token_scopes({"scp": ["kuuos:read", "kuuos:write"]}) == [
        "kuuos:read",
        "kuuos:write",
    ]


def test_token_client_id_prefers_client_id_then_authorized_party() -> None:
    assert token_client_id({"client_id": "client-a", "azp": "client-b"}) == "client-a"
    assert token_client_id({"azp": "client-b"}) == "client-b"
    assert token_client_id({}) == "oauth-client"


def test_audience_allows_exact_audience_or_resource() -> None:
    expected = "https://kuuos-chat-work-mcp.vercel.app/api/mcp"
    assert audience_allows({"aud": expected}, expected)
    assert audience_allows({"aud": ["other", expected]}, expected)
    assert audience_allows({"resource": expected}, expected)
    assert not audience_allows({"aud": "other"}, expected)


def test_audience_check_can_be_explicitly_disabled() -> None:
    assert audience_allows({}, None)


def test_jwks_verifier_requires_https() -> None:
    with pytest.raises(ValueError, match="JWKS URL must use HTTPS"):
        JWKSTokenVerifier(
            "http://issuer.example/jwks.json",
            issuer="https://issuer.example",
            expected_audience="https://resource.example/mcp",
        )


def test_build_oauth_config_supports_explicit_jwks_mode(monkeypatch) -> None:
    monkeypatch.setenv("KUUOS_MCP_OAUTH_ENABLED", "true")
    monkeypatch.setenv("KUUOS_MCP_OAUTH_ISSUER", "https://issuer.example")
    monkeypatch.setenv(
        "KUUOS_MCP_OAUTH_RESOURCE_URL", "https://resource.example/api/mcp"
    )
    monkeypatch.setenv("KUUOS_MCP_OAUTH_TOKEN_MODE", "jwks")
    monkeypatch.setenv(
        "KUUOS_MCP_OAUTH_JWKS_URL", "https://issuer.example/.well-known/jwks.json"
    )

    config = build_oauth_config()

    assert config is not None
    assert isinstance(config.token_verifier, JWKSTokenVerifier)
    assert config.embedded_provider is None
    assert config.token_mode == "jwks"
    assert config.read_scope == "kuuos:read"
    assert config.write_scope == "kuuos:write"


def test_build_oauth_config_embedded_requires_postgres(monkeypatch) -> None:
    monkeypatch.setenv("KUUOS_MCP_OAUTH_ENABLED", "true")
    monkeypatch.setenv("KUUOS_MCP_OAUTH_ISSUER", "https://issuer.example")
    monkeypatch.setenv(
        "KUUOS_MCP_OAUTH_RESOURCE_URL", "https://resource.example/mcp"
    )
    monkeypatch.setenv("KUUOS_MCP_OAUTH_TOKEN_MODE", "embedded")
    monkeypatch.setenv("KUUOS_MCP_EMBEDDED_AUTH_SECRET", "x" * 32)
    monkeypatch.delenv("KUUOS_MCP_DATABASE_URL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="requires KUUOS_MCP_DATABASE_URL or DATABASE_URL"):
        build_oauth_config()


def test_build_oauth_config_embedded_requires_strong_secret(monkeypatch) -> None:
    monkeypatch.setenv("KUUOS_MCP_OAUTH_ENABLED", "true")
    monkeypatch.setenv("KUUOS_MCP_OAUTH_ISSUER", "https://issuer.example")
    monkeypatch.setenv(
        "KUUOS_MCP_OAUTH_RESOURCE_URL", "https://resource.example/mcp"
    )
    monkeypatch.setenv("KUUOS_MCP_OAUTH_TOKEN_MODE", "embedded")
    monkeypatch.setenv("DATABASE_URL", "postgresql://example.invalid/db")
    monkeypatch.setenv("KUUOS_MCP_EMBEDDED_AUTH_SECRET", "too-short")

    with pytest.raises(RuntimeError, match="at least 24 characters"):
        build_oauth_config()


def test_build_oauth_config_embedded_wires_provider_without_external_verifier(
    monkeypatch,
) -> None:
    captured: dict[str, object] = {}

    class FakeEmbeddedProvider:
        def __init__(self, database_url: str, **kwargs) -> None:
            captured["database_url"] = database_url
            captured.update(kwargs)

    monkeypatch.setattr(oauth_module, "EmbeddedPostgresOAuthProvider", FakeEmbeddedProvider)
    monkeypatch.setenv("KUUOS_MCP_OAUTH_ENABLED", "true")
    monkeypatch.setenv("KUUOS_MCP_OAUTH_ISSUER", "https://issuer.example")
    monkeypatch.setenv(
        "KUUOS_MCP_OAUTH_RESOURCE_URL", "https://resource.example/mcp"
    )
    monkeypatch.setenv("KUUOS_MCP_OAUTH_TOKEN_MODE", "embedded")
    monkeypatch.setenv("DATABASE_URL", "postgresql://db.example/kuuos")
    monkeypatch.setenv("KUUOS_MCP_EMBEDDED_AUTH_SECRET", "s" * 32)
    monkeypatch.setenv("KUUOS_MCP_WRITE_ENABLED", "true")

    config = build_oauth_config()

    assert config is not None
    assert config.token_verifier is None
    assert config.embedded_provider is not None
    assert config.token_mode == "embedded"
    assert captured["database_url"] == "postgresql://db.example/kuuos"
    assert captured["issuer"] == "https://issuer.example"
    assert captured["resource_url"] == "https://resource.example/mcp"
    assert config.auth_settings.client_registration_options is not None
    assert config.auth_settings.client_registration_options.enabled
    assert config.auth_settings.client_registration_options.default_scopes == [
        "kuuos:read",
        "kuuos:write",
    ]


def test_build_oauth_config_rejects_unknown_token_mode(monkeypatch) -> None:
    monkeypatch.setenv("KUUOS_MCP_OAUTH_ENABLED", "true")
    monkeypatch.setenv("KUUOS_MCP_OAUTH_ISSUER", "https://issuer.example")
    monkeypatch.setenv(
        "KUUOS_MCP_OAUTH_RESOURCE_URL", "https://resource.example/api/mcp"
    )
    monkeypatch.setenv("KUUOS_MCP_OAUTH_TOKEN_MODE", "opaque-magic")

    with pytest.raises(RuntimeError, match="TOKEN_MODE"):
        build_oauth_config()
