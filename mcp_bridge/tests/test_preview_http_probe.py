"""Offline checks for safe, secret-free external Preview HTTP auditing."""
from __future__ import annotations

import json
from urllib.request import Request

import pytest

import preview_http_probe as probe


HOST = "kuuos-chat-work-ksyrxn8mm-itakurahidetoshi-9224.vercel.app"
ORIGIN = "https://" + HOST
SHARE = ORIGIN + "/?_vercel_share=synthetic-testing-only"


def test_expected_preview_origin_admitted():
    assert probe.validate_origin(ORIGIN) == ORIGIN
    assert probe.validate_origin(ORIGIN + "/") == ORIGIN


@pytest.mark.parametrize("candidate", [
    "", "http://" + HOST, "https://kuuos-chat-work-mcp.vercel.app",
    "https://other.vercel.app", ORIGIN + "/api/mcp",
    ORIGIN + "?share=secret", ORIGIN + ":443",
    ORIGIN + ".evil.example", ORIGIN + "#fragment",
    "https://login:pass@" + HOST,
])
def test_other_origins_refused(candidate):
    with pytest.raises(ValueError):
        probe.validate_origin(candidate)


def test_same_origin_share_link_without_leaking_token():
    assert probe.validate_share(ORIGIN, SHARE) == SHARE


@pytest.mark.parametrize("candidate", [
    ORIGIN + "/",
    ORIGIN + "/?_vercel_share=",
    ORIGIN + "/?_vercel_share=one&_vercel_share=two",
    ORIGIN + "/?_vercel_share=one&debug=1",
    ORIGIN + "/?_vercel_share=one#fragment",
    ORIGIN + "/api/mcp?_vercel_share=one",
    "https://other.vercel.app/?_vercel_share=one",
])
def test_share_url_scoping_fail_closed(candidate):
    with pytest.raises(ValueError):
        probe.validate_share(ORIGIN, candidate)


def test_cross_origin_redirect_blocked():
    redirect = probe.SameOriginRedirect(ORIGIN)
    req = Request(ORIGIN + "/healthz")
    with pytest.raises(RuntimeError, match="cross_origin_redirect_blocked"):
        redirect.redirect_request(
            req, None, 302, "Found", {}, "https://attacker.example/"
        )


class Response:
    def __init__(self, status, body, headers=None):
        self.status = status
        self.body = body
        self.headers = headers or {}
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self, n=8192):
        return self.body[:n]


class FakeOpener:
    def __init__(self, mcp_status=401, github_status=401):
        self.calls = []
        self.mcp_status = mcp_status
        self.github_status = github_status

    def open(self, req, timeout=None):
        self.calls.append((req.full_url, req.get_method(), req.data))
        if "_vercel_share" in req.full_url:
            return Response(404, b"Not Found")
        if req.full_url.endswith("/healthz"):
            return Response(200, json.dumps({
                "ok": True, "backend": "PostgresStateStore",
                "mode": "read-only", "oauth_enabled": True,
                "mcp_events_adapter_loaded": True,
                "github_event_ingress_loaded": True, "write_ready": False,
                "vercel_deployment_environment": "preview",
            }).encode())
        if req.full_url.endswith("/.well-known/oauth-protected-resource/api/mcp"):
            return Response(200, json.dumps({
                "resource": ORIGIN + "/api/mcp",
            }).encode())
        if req.full_url.endswith("/.well-known/oauth-authorization-server"):
            return Response(200, json.dumps({
                "issuer": ORIGIN + "/",
                "code_challenge_methods_supported": ["S256"],
            }).encode())
        if req.full_url.endswith("/api/mcp"):
            return Response(self.mcp_status, b"{}", {
                "WWW-Authenticate": "Bearer error=invalid_token"
            })
        if req.full_url.endswith("/api/github"):
            return Response(self.github_status, b'{"error":"unauthorized_event"}')
        raise AssertionError("unexpected network request")


def test_probe_reports_negative_transport_only(monkeypatch):
    opener = FakeOpener()
    monkeypatch.setattr(probe, "build_opener", lambda *args: opener)
    out = probe.probe(ORIGIN, SHARE)
    assert out["observed_http"]["unauthenticated_mcp_initialize"] == 401
    assert out["observed_http"]["invalid_github_signature"] == 401
    assert out["subscription_created"] is False
    assert out["real_github_event_received"] is False
    assert out["dot_callback_received"] is False
    assert out["independent_github_mcp_reobservation"] is False
    assert out["status"] == "BLOCKED_MCP_EVENT_SUBSCRIPTION"
    assert "_vercel_share" not in json.dumps(out)
    assert [x[1] for x in opener.calls[-2:]] == ["POST", "POST"]


def test_probe_rejects_unprotected_mcp(monkeypatch):
    opener = FakeOpener(mcp_status=200)
    monkeypatch.setattr(probe, "build_opener", lambda *args: opener)
    with pytest.raises(RuntimeError, match="unauthenticated_mcp_post_not_rejected"):
        probe.probe(ORIGIN, SHARE)


def test_probe_rejects_accepted_bad_github_signature(monkeypatch):
    opener = FakeOpener(github_status=202)
    monkeypatch.setattr(probe, "build_opener", lambda *args: opener)
    with pytest.raises(RuntimeError, match="invalid_github_signature_not_rejected"):
        probe.probe(ORIGIN, SHARE)
