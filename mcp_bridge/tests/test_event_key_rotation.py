"""Bounded dual-key Standard Webhooks migration, with no external network."""
from __future__ import annotations

import base64
import hashlib
import hmac
from datetime import datetime, timedelta, timezone

import pytest
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from kuuos_mcp_bridge.event_delivery import PostResult, deliver_event
from kuuos_mcp_bridge.event_subscriptions import (
    ROTATION_WINDOW_SECONDS, MemorySubscriptionStore,
    PostgresSubscriptionStore, SubscriptionManager,
)
from kuuos_mcp_bridge.github_event_contract import (
    CI_EVENT, MGAP_REPO, EventContractError, compile_ci_completed,
)

NOW = datetime(2026, 11, 20, 12, 0, tzinfo=timezone.utc)
OLD_BYTES, NEW_BYTES, NEXT_BYTES = b"a" * 32, b"b" * 32, b"c" * 32


def _secret(value: bytes) -> str:
    return "whsec_" + base64.b64encode(value).decode("ascii")


def _request(key: bytes) -> dict:
    return {
        "name": CI_EVENT,
        "arguments": {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"},
        "delivery": {
            "mode": "webhook", "url": "https://receiver.example.org/callback",
            "secret": _secret(key),
        },
    }


def _event():
    return compile_ci_completed({
        "action": "completed", "repository": {"full_name": MGAP_REPO},
        "workflow_run": {
            "id": 42, "run_attempt": 1, "head_sha": "a" * 40,
            "name": "PR Lean Fast Check", "event": "pull_request",
            "status": "completed", "conclusion": "failure",
        },
    })


def _system():
    calls = []
    store = MemorySubscriptionStore()
    clock = [NOW]
    manager = SubscriptionManager(
        store,
        authorize=lambda p, n, a: True,
        verify_callback=lambda u, key, i: calls.append(key) or True,
        now=lambda: clock[0],
    )
    return manager, store, clock, calls


class RecordingPoster:
    def __init__(self):
        self.calls = []
    def post(self, url, body, headers):
        self.calls.append((url, body, headers))
        return PostResult(200, b"{}")


def _expected_signature(event_id: str, timestamp: int, payload: bytes, key: bytes) -> str:
    signed = event_id.encode() + b"." + str(timestamp).encode() + b"." + payload
    return "v1," + base64.b64encode(hmac.new(key, signed, hashlib.sha256).digest()).decode()


def test_rotation_is_idempotent_and_carries_short_previous_key_window():
    manager, store, clock, calls = _system()
    one = manager.subscribe("owner", _request(OLD_BYTES))
    two = manager.subscribe("owner", _request(NEW_BYTES))
    item = store.get(one["id"])
    assert one["id"] == two["id"]
    assert item.secret == _secret(NEW_BYTES)
    assert item.previous_secret == _secret(OLD_BYTES)
    assert item.previous_secret_until == NOW + timedelta(seconds=ROTATION_WINDOW_SECONDS)
    assert len(calls) == 2
    assert _secret(OLD_BYTES) not in repr(item)
    assert _secret(NEW_BYTES) not in repr(item)
    assert item.public_receipt()["cursor"] is None


def test_webhook_contains_both_hmac_signatures_only_during_rotation():
    manager, store, clock, _ = _system()
    identity = manager.subscribe("owner", _request(OLD_BYTES))["id"]
    manager.subscribe("owner", _request(NEW_BYTES))
    item = store.get(identity)
    event = _event()
    during = RecordingPoster()
    stamp = int((NOW + timedelta(minutes=2)).timestamp())
    deliver_event(item, event, poster=during, now_seconds=lambda: stamp)
    url, body, headers = during.calls[0]
    signatures = headers["webhook-signature"].split(" ")
    assert len(signatures) == 2
    assert signatures[0] == _expected_signature(event["eventId"], stamp, body, NEW_BYTES)
    assert signatures[1] == _expected_signature(event["eventId"], stamp, body, OLD_BYTES)
    assert headers["webhook-id"] == event["eventId"]
    assert headers["X-MCP-Subscription-Id"] == identity

    after = RecordingPoster()
    past = int((NOW + timedelta(minutes=12)).timestamp())
    deliver_event(item, event, poster=after, now_seconds=lambda: past)
    assert after.calls[0][2]["webhook-signature"] == _expected_signature(
        event["eventId"], past, after.calls[0][1], NEW_BYTES
    )


def test_refresh_same_key_preserves_window_and_expiration_clears_it():
    manager, store, clock, calls = _system()
    identity = manager.subscribe("owner", _request(OLD_BYTES))["id"]
    manager.subscribe("owner", _request(NEW_BYTES))
    clock[0] = NOW + timedelta(minutes=5)
    manager.subscribe("owner", _request(NEW_BYTES))
    assert store.get(identity).previous_secret == _secret(OLD_BYTES)
    assert store.get(identity).previous_secret_until == NOW + timedelta(minutes=10)
    clock[0] = NOW + timedelta(minutes=11)
    manager.subscribe("owner", _request(NEW_BYTES))
    assert store.get(identity).previous_secret is None
    assert store.get(identity).previous_secret_until is None
    assert len(calls) == 2


def test_reject_overlapping_rotation_without_persisting_third_secret():
    manager, store, clock, calls = _system()
    identity = manager.subscribe("owner", _request(OLD_BYTES))["id"]
    manager.subscribe("owner", _request(NEW_BYTES))
    with pytest.raises(EventContractError, match="overlapping_key_rotation_not_supported"):
        manager.subscribe("owner", _request(NEXT_BYTES))
    assert store.get(identity).secret == _secret(NEW_BYTES)
    assert store.get(identity).previous_secret == _secret(OLD_BYTES)


def test_expired_original_subscription_is_not_carried_as_previous_key():
    manager, store, clock, _ = _system()
    identity = manager.subscribe("owner", _request(OLD_BYTES) | {"ttlMs": 3600000})["id"]
    clock[0] = NOW + timedelta(hours=2)
    manager.subscribe("owner", _request(NEW_BYTES))
    assert store.get(identity).previous_secret is None


def test_aes_gcm_previous_key_separate_aad_and_tamper_rejection():
    manager, store, _, _ = _system()
    identity = manager.subscribe("owner", _request(OLD_BYTES))["id"]
    manager.subscribe("owner", _request(NEW_BYTES))
    item = store.get(identity)
    pg = object.__new__(PostgresSubscriptionStore)
    pg._aes = AESGCM(b"z" * 32)
    main_blob = pg._seal(item)
    old_blob = pg._seal_previous(item)
    assert old_blob is not None and OLD_BYTES not in old_blob
    assert pg._unseal(identity, main_blob) == _secret(NEW_BYTES)
    assert pg._unseal_previous(identity, old_blob) == _secret(OLD_BYTES)
    with pytest.raises(EventContractError, match="encrypted_previous_secret_invalid"):
        pg._unseal_previous("sub_" + "0" * 64, old_blob)
    with pytest.raises(EventContractError, match="encrypted_previous_secret_invalid"):
        pg._unseal_previous(identity, old_blob[:-1] + bytes([old_blob[-1] ^ 1]))
    with pytest.raises(EventContractError, match="encrypted_secret_invalid"):
        pg._unseal(identity, old_blob)
    restored = pg._restore((
        item.id, item.principal, item.name, item.arguments, item.callback_url,
        main_blob, item.expires_at, item.verified_at, old_blob,
        item.previous_secret_until,
    ))
    assert restored == item


def test_additive_postgres_schema_migration_columns():
    statements = []
    class FakeConn:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def execute(self, statement, *args):
            statements.append(statement)
    pg = object.__new__(PostgresSubscriptionStore)
    pg._connect = lambda: FakeConn()
    pg._ensure_schema()
    assert any("ADD COLUMN IF NOT EXISTS previous_secret_blob" in q for q in statements)
    assert any("ADD COLUMN IF NOT EXISTS previous_secret_until" in q for q in statements)
    assert any("CREATE TABLE IF NOT EXISTS" in q for q in statements)
