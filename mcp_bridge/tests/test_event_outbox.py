from __future__ import annotations

import base64
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from kuuos_mcp_bridge.event_outbox import (
    MAX_CLAIM_ATTEMPTS, MemoryOutboxStore, PostgresOutboxStore,
    _fingerprint, _new_record,
)
from kuuos_mcp_bridge.event_subscriptions import Subscription, _identity
from kuuos_mcp_bridge.github_event_contract import (
    CI_EVENT, MGAP_REPO, EventContractError, compile_ci_completed,
)


NOW = datetime(2026, 11, 20, 13, tzinfo=timezone.utc)
URL = "https://receiver.example.com/dots"
KEY = "whsec_" + base64.b64encode(b"a" * 32).decode()


def fixture_event(run_id=44737078837, conclusion="success"):
    return compile_ci_completed({
        "action": "completed", "repository": {"full_name": MGAP_REPO},
        "workflow_run": {
            "id": run_id, "run_attempt": 1, "name": "PR Lean Fast Check",
            "status": "completed", "conclusion": conclusion,
            "event": "pull_request", "head_sha": "a" * 40,
        },
    })


def fixture_sub():
    args = {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"}
    subid = _identity("owner-1", CI_EVENT, args, URL)
    return Subscription(
        id=subid, principal="owner-1", name=CI_EVENT,
        arguments=args, callback_url=URL, secret=KEY,
        expires_at=NOW + timedelta(days=1), verified_at=NOW,
    )


def test_enqueued_event_is_non_authoritative_and_unique():
    store = MemoryOutboxStore()
    one = store.enqueue(fixture_sub(), fixture_event(), NOW)
    two = store.enqueue(fixture_sub(), fixture_event(), NOW)
    assert one == two
    assert len(store.records) == 1
    assert one.public_receipt()["merge_authority_granted"] is False
    assert one.public_receipt()["signal_is_success_evidence"] is False
    assert KEY not in repr(one.public_receipt())


def test_claim_requires_due_time_and_leases_exactly_one():
    store = MemoryOutboxStore()
    x = store.enqueue(fixture_sub(), fixture_event(), NOW)
    assert store.claim(NOW - timedelta(seconds=1)) is None
    claim = store.claim(NOW)
    assert claim.id == x.id
    assert claim.attempts == 1 and claim.state == "leased"
    assert claim.lease_token is not None and claim.lease_until == NOW + timedelta(seconds=30)
    assert store.claim(NOW) is None


def test_success_moves_to_permanent_delivered_and_no_replay():
    store = MemoryOutboxStore()
    sub, event = fixture_sub(), fixture_event()
    store.enqueue(sub, event, NOW)
    lease = store.claim(NOW)
    done = store.settle(lease.id, lease.lease_token, 202, NOW)
    assert done.state == "delivered"
    assert store.claim(NOW + timedelta(days=1)) is None
    assert store.enqueue(sub, event, NOW).state == "delivered"


def test_transient_failure_is_retryable_after_backoff():
    store = MemoryOutboxStore()
    store.enqueue(fixture_sub(), fixture_event(), NOW)
    first = store.claim(NOW)
    retry = store.settle(first.id, first.lease_token, 503, NOW)
    assert retry.state == "pending"
    assert retry.available_at > NOW
    assert store.claim(NOW) is None
    second = store.claim(retry.available_at)
    assert second.attempts == 2
    assert second.lease_token != first.lease_token


def test_permanent_failure_never_replayed():
    store = MemoryOutboxStore()
    store.enqueue(fixture_sub(), fixture_event(), NOW)
    first = store.claim(NOW)
    status = store.settle(first.id, first.lease_token, 410, NOW)
    assert status.state == "permanent_failure"
    assert store.claim(NOW + timedelta(days=100)) is None


def test_expired_lease_reclaimed_without_losing_event():
    store = MemoryOutboxStore()
    store.enqueue(fixture_sub(), fixture_event(), NOW)
    old = store.claim(NOW)
    fresh = store.claim(NOW + timedelta(seconds=31))
    assert fresh.id == old.id
    assert fresh.lease_token != old.lease_token
    with pytest.raises(EventContractError, match="outbox_lease_mismatch"):
        store.settle(old.id, old.lease_token, 200, NOW + timedelta(seconds=32))
    assert store.settle(fresh.id, fresh.lease_token, 200, NOW + timedelta(seconds=32)).state == "delivered"


def test_timed_out_budget_never_leaves_lease_reusable():
    store = MemoryOutboxStore()
    store.enqueue(fixture_sub(), fixture_event(), NOW)
    for attempt in range(MAX_CLAIM_ATTEMPTS):
        moment = NOW + timedelta(minutes=attempt)
        claim = store.claim(moment)
        assert claim is not None
        if attempt != MAX_CLAIM_ATTEMPTS - 1:
            store.settle(claim.id, claim.lease_token, 503, moment)
    assert store.claim(NOW + timedelta(hours=1)) is None
    assert next(iter(store.records.values())).state == "retry_exhausted"


def test_cancellation_requires_exact_lease():
    store = MemoryOutboxStore()
    store.enqueue(fixture_sub(), fixture_event(), NOW)
    first = store.claim(NOW)
    with pytest.raises(EventContractError, match="outbox_lease_mismatch"):
        store.cancel(first.id, "wrong")
    assert store.cancel(first.id, first.lease_token).state == "cancelled"
    assert store.claim(NOW + timedelta(days=1)) is None


def test_subscription_filter_and_expiry_fail_before_insert():
    store = MemoryOutboxStore()
    sub = fixture_sub()
    with pytest.raises(EventContractError, match="outbox_subscription_expired"):
        store.enqueue(replace(sub, expires_at=NOW), fixture_event(), NOW)
    bad = replace(sub, arguments={"repository": "other/repository"})
    with pytest.raises(EventContractError, match="outbox_subscription_filter_mismatch"):
        store.enqueue(bad, fixture_event(), NOW)
    assert not store.records


def test_packet_rejects_injected_ci_success_or_merge_authority():
    store = MemoryOutboxStore()
    for field, value in [("merge_authority_granted", True), ("signal_is_success_evidence", True)]:
        e = fixture_event()
        e["data"][field] = value
        with pytest.raises(Exception):
            store.enqueue(fixture_sub(), e, NOW)
    assert not store.records


def test_unique_outbox_id_scoped_by_subscription():
    first = fixture_sub()
    second = replace(first, id="sub_" + "a" * 64)
    event = fixture_event()
    assert _fingerprint(first.id, event["eventId"]) != _fingerprint(second.id, event["eventId"])
    assert _fingerprint(first.id, event["eventId"]) == _fingerprint(first.id, event["eventId"])


def test_sql_candidate_is_transactional_and_has_no_secrets():
    import inspect
    source = inspect.getsource(PostgresOutboxStore)
    assert "FOR UPDATE SKIP LOCKED" in source
    assert "UNIQUE(subscription_id, event_id)" in source
    assert "lease_token" in source
    assert "secret_blob" not in source
    assert "GITHUB_TOKEN" not in source


def test_postgres_constructor_rejects_missing_dsn():
    with pytest.raises(ValueError, match="outbox_postgres_dsn_required"):
        PostgresOutboxStore("")


def test_specific_claim_skips_unrelated_pending_backlog():
    store = MemoryOutboxStore()
    sub = fixture_sub()
    old = store.enqueue(sub, fixture_event(987501), NOW)
    fresh = store.enqueue(sub, fixture_event(987502), NOW)
    claimed = store.claim_specific(fresh.id, NOW)
    assert claimed is not None and claimed.id == fresh.id
    assert store.records[old.id].state == "pending"
    assert store.claim_specific(fresh.id, NOW) is None
    stored = store.settle(fresh.id, claimed.lease_token, 200, NOW)
    assert stored.state == "delivered"
    assert store.claim_specific(fresh.id, NOW + timedelta(hours=1)) is None
    assert store.claim_specific("out_" + "0" * 64, NOW) is None


def test_specific_claim_reclaims_expired_lease_and_rejects_old_token():
    store = MemoryOutboxStore()
    row = store.enqueue(fixture_sub(), fixture_event(987503), NOW)
    first = store.claim_specific(row.id, NOW)
    assert first is not None
    assert store.claim_specific(row.id, NOW + timedelta(seconds=29)) is None
    second = store.claim_specific(row.id, NOW + timedelta(seconds=31))
    assert second is not None and second.lease_token != first.lease_token
    with pytest.raises(EventContractError, match="outbox_lease_mismatch"):
        store.settle(row.id, first.lease_token, 200, NOW + timedelta(seconds=32))
