from __future__ import annotations

import json

import pytest

from kuuos_mcp_bridge import attestation
from kuuos_mcp_bridge.attestation import (
    DeploymentAttestationError,
    DeploymentExpectation,
    build_health_url,
    fetch_health_payload,
    validate_health_payload,
)


SHA = "d7ea7c026ec448ff1949ff532c8a3b8fecb6e3bc"


def health_payload(**overrides):
    payload = {
        "ok": True,
        "mode": "read-only",
        "backend": "PostgresStateStore",
        "version": 22,
        "oauth_enabled": True,
        "oauth_mode": "embedded",
        "write_ready": False,
        "canonical_sha": SHA,
    }
    payload.update(overrides)
    return payload


def expectation(**overrides):
    values = {
        "canonical_sha": SHA,
        "backend": "PostgresStateStore",
        "oauth_mode": "embedded",
        "oauth_enabled": True,
        "write_ready": False,
        "mode": "read-only",
    }
    values.update(overrides)
    return DeploymentExpectation(**values)


def test_validate_health_payload_accepts_safe_read_only_embedded_postgres():
    observed = validate_health_payload(health_payload(), expectation())
    assert observed["canonical_sha"] == SHA
    assert observed["write_ready"] is False


def test_validate_health_payload_rejects_missing_contract_field():
    payload = health_payload()
    del payload["oauth_mode"]
    with pytest.raises(DeploymentAttestationError, match="missing required fields"):
        validate_health_payload(payload, expectation())


def test_validate_health_payload_rejects_stale_canonical_sha():
    with pytest.raises(DeploymentAttestationError, match="canonical SHA mismatch"):
        validate_health_payload(
            health_payload(canonical_sha="stale"), expectation()
        )


def test_validate_health_payload_rejects_embedded_oauth_without_postgres():
    with pytest.raises(DeploymentAttestationError, match="PostgresStateStore"):
        validate_health_payload(
            health_payload(backend="JsonStateStore"),
            expectation(backend=None),
        )


def test_validate_health_payload_rejects_write_ready_without_read_write_mode():
    with pytest.raises(DeploymentAttestationError, match="write_ready=true"):
        validate_health_payload(
            health_payload(write_ready=True),
            expectation(write_ready=None),
        )


def test_validate_health_payload_rejects_oauth_flag_mode_inconsistency():
    with pytest.raises(DeploymentAttestationError, match="internally inconsistent"):
        validate_health_payload(
            health_payload(oauth_enabled=False),
            expectation(oauth_enabled=None),
        )


def test_build_health_url_requires_https_except_explicit_localhost():
    assert (
        build_health_url("https://example.test/mcp")
        == "https://example.test/mcp/healthz"
    )
    with pytest.raises(DeploymentAttestationError, match="requires HTTPS"):
        build_health_url("http://example.test")
    assert (
        build_health_url(
            "http://127.0.0.1:8000", allow_http_localhost=True
        )
        == "http://127.0.0.1:8000/healthz"
    )


class FakeHeaders(dict):
    def get(self, key, default=None):
        return super().get(key.lower(), default)


class FakeResponse:
    status = 200

    def __init__(self, *, final_url: str, payload: dict):
        self._final_url = final_url
        self._raw = json.dumps(payload).encode("utf-8")
        self.headers = FakeHeaders({"content-type": "application/json"})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def geturl(self):
        return self._final_url

    def read(self, _limit):
        return self._raw


def test_fetch_health_payload_rejects_cross_origin_redirect(monkeypatch):
    def fake_urlopen(_request, timeout):
        assert timeout == 3.0
        return FakeResponse(
            final_url="https://evil.example/healthz",
            payload=health_payload(),
        )

    monkeypatch.setattr(attestation, "urlopen", fake_urlopen)
    with pytest.raises(DeploymentAttestationError, match="different origin"):
        fetch_health_payload("https://staging.example", timeout=3.0)


def test_fetch_health_payload_accepts_same_origin_json(monkeypatch):
    def fake_urlopen(_request, timeout):
        assert timeout == 5.0
        return FakeResponse(
            final_url="https://staging.example/healthz",
            payload=health_payload(),
        )

    monkeypatch.setattr(attestation, "urlopen", fake_urlopen)
    health_url, payload = fetch_health_payload(
        "https://staging.example", timeout=5.0
    )
    assert health_url == "https://staging.example/healthz"
    assert payload["canonical_sha"] == SHA
