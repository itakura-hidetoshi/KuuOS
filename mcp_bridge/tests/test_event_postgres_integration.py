"""Actual PostgreSQL integration, run only with a disposable CI service database.

No application/user database is used. This test does not prove live Dots event
delivery: it certifies only the SQL/transaction/encryption behavior observed
inside the GitHub Actions PostgreSQL service container.
"""
from __future__ import annotations

import base64
import os
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor

import pytest
import psycopg

from kuuos_mcp_bridge.event_outbox import PostgresOutboxStore
from kuuos_mcp_bridge.event_subscriptions import (
    PostgresSubscriptionStore, SubscriptionManager, ROTATION_WINDOW_SECONDS,
)
from kuuos_mcp_bridge.github_event_contract import (
    CI_EVENT, MGAP_REPO, EventContractError, compile_ci_completed,
)

DSN = os.environ.get("KUUOS_MCP_TEST_POSTGRES_DSN")
pytestmark = pytest.mark.skipif(
    not DSN, reason="requires isolated GitHub Actions PostgreSQL service DSN"
)
NOW = datetime(2026, 11, 20, 14, tzinfo=timezone.utc)
KEY = base64.b64encode(b"k" * 32).decode()
ONE = "whsec_" + base64.b64encode(b"a" * 32).decode()
TWO = "whsec_" + base64.b64encode(b"b" * 32).decode()


@pytest.fixture(scope="module")
def stores():
    # Hard boundary: the test never runs on an unknown or non-CI database.
    if not DSN:
        pytest.skip("no disposable postgres service configured")
    conninfo = psycopg.conninfo.conninfo_to_dict(DSN)
    if conninfo.get("dbname") != "kuuos_events_ci" or conninfo.get("user") != "kuuos_ci":
        pytest.fail("isolated CI PostgreSQL database identity mismatch")
    return PostgresSubscriptionStore(DSN, KEY), PostgresOutboxStore(DSN)


def _manager(store, *, owner="owner-fixture"):
    return SubscriptionManager(
        store, authorize=lambda p, n, a: p == owner,
        verify_callback=lambda url, secret, identity: True,
        now=lambda: NOW,
    )


def _params(secret=ONE):
    return {
        "name": CI_EVENT,
        "arguments": {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"},
        "delivery": {
            "mode": "webhook",
            "url": "https://receiver.example.org/ci-postgres",
            "secret": secret,
        },
    }


def _event(run_id=980001):
    return compile_ci_completed({
        "action": "completed",
        "repository": {"full_name": MGAP_REPO},
        "workflow_run": {
            "id": run_id, "run_attempt": 1,
            "name": "PR Lean Fast Check", "event": "pull_request",
            "status": "completed", "conclusion": "failure",
            "head_sha": "a" * 40,
        },
    })


def test_real_postgres_subscribe_rotation_and_encrypted_secret_storage(stores):
    subs, _ = stores
    manager = _manager(subs)
    first = manager.subscribe("owner-fixture", _params())
    assert first["id"].startswith("sub_")
    assert subs.get(first["id"]).secret == ONE
    manager.subscribe("owner-fixture", _params(TWO))
    current = subs.get(first["id"])
    assert current.secret == TWO
    assert current.previous_secret == ONE
    assert current.previous_secret_until == NOW + timedelta(seconds=ROTATION_WINDOW_SECONDS)
    assert current.id == first["id"]
    assert ONE not in repr(current) and TWO not in repr(current)
    with psycopg.connect(DSN) as conn:
        row = conn.execute(
            "SELECT secret_blob, previous_secret_blob FROM "
            "kuuos_mcp_event_subscriptions_v1 WHERE id = %s", (first["id"],),
        ).fetchone()
    assert row is not None
    assert ONE.encode() not in bytes(row[0]) and TWO.encode() not in bytes(row[0])
    assert ONE.encode() not in bytes(row[1]) and TWO.encode() not in bytes(row[1])


def test_real_postgres_outbox_claim_settle_and_idempotent_replay(stores):
    subs, outbox = stores
    sub = subs.active(CI_EVENT, NOW)[0]
    event = _event(980001)
    first = outbox.enqueue(sub, event, NOW)
    same = outbox.enqueue(sub, event, NOW)
    assert first.id == same.id
    assert first.state == same.state == "pending"
    claimed = outbox.claim(NOW)
    assert claimed is not None
    assert claimed.id == first.id
    assert claimed.state == "leased" and claimed.attempts == 1
    assert claimed.lease_token
    assert outbox.claim(NOW) is None
    completed = outbox.settle(claimed.id, claimed.lease_token, 202, NOW)
    assert completed.state == "delivered"
    assert outbox.claim(NOW + timedelta(hours=1)) is None
    assert outbox.enqueue(sub, event, NOW).state == "delivered"


def test_real_postgres_reclaim_expired_lease_rejects_stale_completion(stores):
    from kuuos_mcp_bridge.github_event_contract import EventContractError
    subs, outbox = stores
    sub = subs.active(CI_EVENT, NOW)[0]
    row = outbox.enqueue(sub, _event(980002), NOW)
    first = outbox.claim(NOW)
    assert first is not None and first.id == row.id
    second = outbox.claim(NOW + timedelta(seconds=31))
    assert second is not None and second.id == row.id
    assert second.lease_token != first.lease_token
    with pytest.raises(EventContractError, match="outbox_lease_mismatch"):
        outbox.settle(first.id, first.lease_token, 200, NOW + timedelta(seconds=32))
    done = outbox.settle(second.id, second.lease_token, 200, NOW + timedelta(seconds=32))
    assert done.state == "delivered"


def test_real_postgres_two_workers_claim_only_one_pending_event(stores):
    subs, outbox = stores
    sub = subs.active(CI_EVENT, NOW)[0]
    row = outbox.enqueue(sub, _event(980003), NOW)
    another = PostgresOutboxStore(DSN)
    with ThreadPoolExecutor(max_workers=2) as pool:
        a = pool.submit(outbox.claim, NOW)
        b = pool.submit(another.claim, NOW)
        results = [a.result(), b.result()]
    claimed = [item for item in results if item is not None]
    assert len(claimed) == 1, results
    assert claimed[0].id == row.id
    outbox.settle(claimed[0].id, claimed[0].lease_token, 200, NOW)


def test_real_postgres_revoked_subscription_unsubscribe_is_owner_bound(stores):
    subs, _ = stores
    # Use an isolated subscriber: previous tests intentionally rotated
    # owner-fixture's key and must not silently reset that live rotation.
    owner = "owner-revocation-fixture"
    manager = _manager(subs, owner=owner)
    receipt = manager.subscribe(owner, _params())
    args = {
        "name": CI_EVENT,
        "arguments": {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"},
        "delivery": {"mode": "webhook", "url": "https://receiver.example.org/ci-postgres"},
    }
    with pytest.raises(EventContractError, match="event_scope_not_authorized"):
        manager.unsubscribe("different-owner", args)
    assert subs.get(receipt["id"]) is not None
    manager.unsubscribe(owner, args)
    assert subs.get(receipt["id"]) is None


def test_real_postgres_migrates_legacy_subscription_without_losing_old_secret(stores):
    """Test additive migrations against an actual pre-rotation table schema."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from psycopg.types.json import Jsonb
    from kuuos_mcp_bridge.event_subscriptions import _identity

    # Use a separate synthetic table so neither the existing test subscription
    # nor any user state is touched. The service database is itself ephemeral.
    class LegacyStore(PostgresSubscriptionStore):
        _TABLE = "kuuos_mcp_event_subscriptions_legacy_ci"

    owner = "owner-legacy-fixture"
    arguments = {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"}
    callback = "https://receiver.example.org/ci-postgres"
    sub_id = _identity(owner, CI_EVENT, arguments, callback)
    key = base64.b64decode(KEY, validate=True)
    nonce = b"l" * 12  # Synthetic test-only nonce, not a production pattern.
    old_ciphertext = nonce + AESGCM(key).encrypt(
        nonce, ONE.encode("utf-8"), sub_id.encode("ascii")
    )
    with psycopg.connect(DSN) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS kuuos_mcp_event_subscriptions_legacy_ci (
                id TEXT PRIMARY KEY,
                principal TEXT NOT NULL,
                name TEXT NOT NULL,
                arguments JSONB NOT NULL,
                callback_url TEXT NOT NULL,
                secret_blob BYTEA NOT NULL,
                expires_at TIMESTAMPTZ NOT NULL,
                verified_at TIMESTAMPTZ NOT NULL
            )
        """)
        conn.execute("""
            INSERT INTO kuuos_mcp_event_subscriptions_legacy_ci
              (id, principal, name, arguments, callback_url, secret_blob, expires_at, verified_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (id) DO NOTHING
        """, (
            sub_id, owner, CI_EVENT, Jsonb(arguments), callback, old_ciphertext,
            NOW + timedelta(days=1), NOW,
        ))

    upgraded = LegacyStore(DSN, KEY)
    restored = upgraded.get(sub_id)
    assert restored is not None
    assert restored.secret == ONE
    assert restored.previous_secret is None
    assert restored.previous_secret_until is None

    manager = _manager(upgraded, owner=owner)
    assert manager.subscribe(owner, _params(ONE))["id"] == sub_id
    assert manager.subscribe(owner, _params(TWO))["id"] == sub_id
    active = upgraded.get(sub_id)
    assert active.secret == TWO
    assert active.previous_secret == ONE
    with psycopg.connect(DSN) as conn:
        row = conn.execute("""
            SELECT secret_blob, previous_secret_blob, previous_secret_until
            FROM kuuos_mcp_event_subscriptions_legacy_ci WHERE id = %s
        """, (sub_id,)).fetchone()
    assert row is not None and row[1] is not None and row[2] is not None
    assert ONE.encode() not in bytes(row[1])


def test_real_postgres_specific_claim_prioritizes_fresh_event_and_prevents_replay(stores):
    subs, outbox = stores
    sub = subs.active(CI_EVENT, NOW)[0]
    old = outbox.enqueue(sub, _event(980101), NOW)
    fresh = outbox.enqueue(sub, _event(980102), NOW)
    claim = outbox.claim_specific(fresh.id, NOW)
    assert claim is not None and claim.id == fresh.id
    assert outbox.claim_specific(fresh.id, NOW) is None
    assert outbox.claim_specific(old.id, NOW) is not None
    done = outbox.settle(claim.id, claim.lease_token, 202, NOW)
    assert done.state == "delivered"
    assert outbox.claim_specific(fresh.id, NOW + timedelta(minutes=2)) is None


def test_real_postgres_specific_claim_competing_workers_only_one_wins(stores):
    subs, outbox = stores
    sub = subs.active(CI_EVENT, NOW)[0]
    row = outbox.enqueue(sub, _event(980103), NOW)
    second = PostgresOutboxStore(DSN)
    with ThreadPoolExecutor(max_workers=2) as pool:
        a = pool.submit(outbox.claim_specific, row.id, NOW)
        b = pool.submit(second.claim_specific, row.id, NOW)
        result = [a.result(), b.result()]
    claimed = [c for c in result if c is not None]
    assert len(claimed) == 1
    assert claimed[0].id == row.id
    outbox.settle(row.id, claimed[0].lease_token, 200, NOW)
