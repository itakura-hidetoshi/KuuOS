"""Read-only HTTP transport/negative-auth probe for KuuOS protected Vercel previews.

Run only against the known project preview hostname. Vercel's temporary
deployment share link is taken from an environment variable; never put its
secret in command-line arguments, GitHub, output, or a saved receipt.
The probe never authenticates an end-user, never subscribes, never sends a
valid GitHub signature and never claims Dots event delivery or Lean proof.
"""
from __future__ import annotations

import argparse
import http.cookiejar
import json
import os
import re
import sys
from typing import Any
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit
from urllib.request import (
    HTTPRedirectHandler, HTTPCookieProcessor, Request, build_opener,
)

_HOST = re.compile(
    r"kuuos-chat-work-[a-z0-9]+-itakurahidetoshi-9224\.vercel\.app"
)
_SCHEMA = "kuuos_mcp_preview_transport_probe_v1"


def validate_origin(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("preview_origin_required")
    parsed = urlsplit(value)
    if (
        parsed.scheme != "https" or parsed.username is not None
        or parsed.password is not None or parsed.port is not None
        or parsed.path not in ("", "/") or parsed.query or parsed.fragment
        or not _HOST.fullmatch(parsed.hostname or "")
    ):
        raise ValueError("preview_origin_not_allowlisted")
    return "https://" + parsed.hostname


def validate_share(origin: str, value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("protected_share_link_required")
    address = urlsplit(value)
    expected = urlsplit(origin)
    if (
        address.scheme != "https" or address.netloc != expected.netloc
        or address.path not in ("", "/") or address.fragment
        or address.username is not None or address.password is not None
    ):
        raise ValueError("share_origin_mismatch")
    q = parse_qs(address.query, keep_blank_values=True)
    if set(q) != {"_vercel_share"} or len(q["_vercel_share"]) != 1 or not q["_vercel_share"][0]:
        raise ValueError("share_query_invalid")
    return value


class SameOriginRedirect(HTTPRedirectHandler):
    def __init__(self, origin: str):
        super().__init__()
        self.origin = urlsplit(origin)

    def redirect_request(self, req: Request, fp: Any, code: int, msg: str,
                         headers: Any, newurl: str) -> Request | None:
        target = urlsplit(newurl)
        if target.scheme != self.origin.scheme or target.netloc != self.origin.netloc:
            raise RuntimeError("cross_origin_redirect_blocked")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _request(opener: Any, url: str, method: str = "GET",
             data: bytes | None = None, headers: dict[str, str] | None = None) -> tuple[int, Any, bytes]:
    req = Request(url, data=data, method=method, headers=headers or {})
    try:
        with opener.open(req, timeout=12) as resp:
            return resp.status, resp.headers, resp.read(8192)
    except HTTPError as exc:
        return exc.code, exc.headers, exc.read(8192)


def probe(origin: str, share_url: str) -> dict[str, Any]:
    origin = validate_origin(origin)
    share_url = validate_share(origin, share_url)
    jar = http.cookiejar.CookieJar()
    opener = build_opener(HTTPCookieProcessor(jar), SameOriginRedirect(origin))
    # The share link only bypasses Vercel's deployment layer, not MCP OAuth.
    # The application has no route at '/', so HTTP 404 is expected here.
    _request(opener, share_url)

    status, _, raw = _request(opener, origin + "/healthz")
    if status != 200:
        raise RuntimeError("protected_health_http_not_200")
    try:
        health = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise RuntimeError("health_json_invalid") from exc
    if not isinstance(health, dict) or not (
        health.get("ok") is True
        and health.get("backend") == "PostgresStateStore"
        and health.get("mode") == "read-only"
        and health.get("oauth_enabled") is True
        and health.get("mcp_events_adapter_loaded") is True
        and health.get("github_event_ingress_loaded") is True
        and health.get("write_ready") is False
        and health.get("vercel_deployment_environment") == "preview"
    ):
        raise RuntimeError("health_runtime_gate_failed")

    status, _, raw = _request(
        opener, origin + "/.well-known/oauth-protected-resource/api/mcp",
    )
    if status != 200:
        raise RuntimeError("protected_resource_metadata_not_200")
    resource = json.loads(raw)
    if resource.get("resource") != origin + "/api/mcp":
        raise RuntimeError("oauth_resource_origin_drift")
    status, _, raw = _request(opener, origin + "/.well-known/oauth-authorization-server")
    if status != 200:
        raise RuntimeError("authorization_metadata_not_200")
    authorization = json.loads(raw)
    if authorization.get("issuer", "").rstrip("/") != origin:
        raise RuntimeError("oauth_issuer_origin_drift")
    if "S256" not in authorization.get("code_challenge_methods_supported", []):
        raise RuntimeError("oauth_pkce_s256_missing")

    initialization = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": "2025-11-25", "capabilities": {},
            "clientInfo": {"name": "kuuos-http-transport-audit", "version": "1"},
        },
    }, separators=(",", ":")).encode("utf-8")
    status, mcp_headers, _ = _request(
        opener, origin + "/api/mcp", "POST", initialization, {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": "2025-11-25",
        },
    )
    if status != 401 or not mcp_headers.get("WWW-Authenticate", "").lower().startswith("bearer"):
        raise RuntimeError("unauthenticated_mcp_post_not_rejected_by_oauth")

    status, _, payload = _request(opener, origin + "/api/github", "POST", b"{}", {
        "Content-Type": "application/json",
        "X-GitHub-Event": "workflow_run",
        "X-Hub-Signature-256": "sha256=" + "0" * 64,
        "X-GitHub-Delivery": "kuuos-negative-audit-no-authority",
    })
    if status != 401:
        raise RuntimeError("invalid_github_signature_not_rejected")
    try:
        error = json.loads(payload)
    except (ValueError, UnicodeError) as exc:
        raise RuntimeError("github_rejection_json_invalid") from exc
    if error.get("error") != "unauthorized_event":
        raise RuntimeError("github_rejection_category_invalid")

    return {
        "schema": _SCHEMA,
        "origin": origin,
        "observed_http": {
            "health": 200,
            "oauth_protected_resource": 200,
            "oauth_authorization_server": 200,
            "unauthenticated_mcp_initialize": 401,
            "invalid_github_signature": 401,
        },
        "real_mcp_oauth_client_authenticated": False,
        "subscription_created": False,
        "real_github_event_received": False,
        "dot_callback_received": False,
        "independent_github_mcp_reobservation": False,
        "status": "BLOCKED_MCP_EVENT_SUBSCRIPTION",
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Safe KuuOS Preview transport probe")
    p.add_argument("--origin", required=True, help="Allowlisted HTTPS Vercel Preview origin")
    args = p.parse_args()
    try:
        receipt = probe(args.origin, os.environ.get("KUUOS_MCP_PREVIEW_SHARE_URL", ""))
    except (ValueError, RuntimeError, OSError, HTTPError):
        # Never emit network error messages: they may contain share URLs.
        print(json.dumps({"schema": _SCHEMA, "verified": False,
                          "status": "HOLD_TRANSPORT_UNCERTIFIED"}))
        return 1
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
