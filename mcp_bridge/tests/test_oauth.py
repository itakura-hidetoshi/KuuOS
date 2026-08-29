from __future__ import annotations

from kuuos_mcp_bridge.oauth import audience_allows, normalize_scopes


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


def test_audience_allows_exact_audience_or_resource() -> None:
    expected = "https://kuuos-chat-work-mcp.vercel.app/api/mcp"
    assert audience_allows({"aud": expected}, expected)
    assert audience_allows({"aud": ["other", expected]}, expected)
    assert audience_allows({"resource": expected}, expected)
    assert not audience_allows({"aud": "other"}, expected)


def test_audience_check_can_be_explicitly_disabled() -> None:
    assert audience_allows({}, None)
