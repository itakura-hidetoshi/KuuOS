from __future__ import annotations

import base64
from datetime import datetime, timedelta, timezone

import pytest

from kuuos_mcp_bridge.event_subscriptions import (
    DEFAULT_TTL_MS,
    MemorySubscriptionStore,
    PostgresSubscriptionStore,
    SubscriptionManager,
)
from kuuos_mcp_bridge.github_event_contract import (
    CI_EVENT,
    MGAP_REPO,
    PR_EVENT,
    EventContractError,
    compile_ci_completed,
    compile_pr_head_updated,
)


NOW = datetime(2026, 11, 20, 12, 0, tzinfo=timezone.utc)
SECRET = "whsec_" + base64.b64encode(b"a" * 32).decode("ascii")
ROTATED = "whsec_" + base64.b64encode(b"b" * 32).decode("ascii")
URL = "https://receiver.example.com/events/callback_1"


def pr_request(**overrides):
    value = {
        "name": PR_EVENT,
        "arguments": {"repository": MGAP_REPO, "pr_number": 6883},
        "delivery": {"mode": "webhook", "url": URL, "secret": SECRET},
        "cursor": None,
    }
    value.update(overrides)
    return value


def ci_request(**overrides):
    value = {
        "name": CI_EVENT,
        "arguments": {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"},
        "delivery": {"mode": "webhook", "url": URL, "secret": SECRET},
    }
    value.update(overrides)
    return value


def pr_event(pr=6883, repo=MGAP_REPO):
    return compile_pr_head_updated({
        "action": "synchronize",
        "repository": {"full_name": repo},
        "number": pr,
        "pull_request": {
            "number": pr,
            "head": {"sha": "a" * 40, "repo": {"full_name": repo}},
            "base": {"ref": "formal/real-hilbert-uniform-coercive-strong-limit"},
        },
    })


def ci_event():
    return compile_ci_completed({
        "action": "completed",
        "repository": {"full_name": MGAP_REPO},
        "workflow_run": {
            "id": 14, "run_attempt": 1,
            "name": "PR Lean Fast Check", "event": "pull_request",
            "status": "completed", "conclusion": "failure", "head_sha": "a" * 40,
        },
    })


def system(*, authorized=lambda principal, name, arguments: True,
           verified=lambda url, key, identity: True):
    store = MemorySubscriptionStore()
    return SubscriptionManager(
        store, authorize=authorized, verify_callback=verified, now=lambda: NOW
    ), store


def test_create_subscription_and_public_receipt_do_not_expose_secret():
    service, store = system()
    result = service.subscribe("owner-1", pr_request())
    assert result["id"].startswith("sub_")
    assert result["cursor"] is None and result["truncated"] is False
    assert SECRET not in repr(result)
    assert len(store.records) == 1
    assert service.recipients(pr_event())[0].principal == "owner-1"


def test_repeated_request_is_idempotent_and_reuses_verified_callback():
    attempts = []
    service, store = system(verified=lambda url, key, identity: attempts.append(identity) or True)
    first = service.subscribe("owner-1", pr_request())
    second = service.subscribe("owner-1", pr_request())
    assert first == second
    assert len(store.records) == 1
    assert len(attempts) == 1


def test_filter_order_does_not_change_identity():
    service, _ = system()
    first = service.subscribe("owner-1", pr_request())
    reversed_args = {"pr_number": 6883, "repository": MGAP_REPO}
    second = service.subscribe("owner-1", pr_request(arguments=reversed_args))
    assert first["id"] == second["id"]


def test_different_owner_cannot_unsubscribe_or_match_other_subscription():
    service, store = system()
    one = service.subscribe("owner-1", pr_request())
    two = service.subscribe("owner-2", pr_request())
    assert one["id"] != two["id"]
    service.unsubscribe("owner-2", {
        "name": PR_EVENT, "arguments": pr_request()["arguments"],
        "delivery": {"mode": "webhook", "url": URL},
    })
    assert store.get(one["id"]) is not None
    assert store.get(two["id"]) is None


def test_verification_failure_must_not_persist():
    service, store = system(verified=lambda url, key, identity: False)
    with pytest.raises(EventContractError, match="callback_verification_failed"):
        service.subscribe("owner-1", pr_request())
    assert not store.records


def test_rotated_secret_requires_new_verified_challenge():
    calls = []
    service, store = system(verified=lambda url, key, identity: calls.append(key) or True)
    identity = service.subscribe("owner-1", pr_request())["id"]
    service.subscribe("owner-1", pr_request(delivery={
        "mode": "webhook", "url": URL, "secret": ROTATED
    }))
    assert len(calls) == 2
    assert store.get(identity).secret == ROTATED


def test_failed_rotation_preserves_existing_secret():
    calls = []
    service, store = system(verified=lambda url, key, identity: calls.append(key) or key == SECRET)
    identity = service.subscribe("owner-1", pr_request())["id"]
    with pytest.raises(EventContractError, match="callback_verification_failed"):
        service.subscribe("owner-1", pr_request(delivery={
            "mode": "webhook", "url": URL, "secret": ROTATED
        }))
    assert store.get(identity).secret == SECRET


@pytest.mark.parametrize("bad", ["", None, " owner", "owner\nx", "x" * 300])
def test_authentication_principal_required(bad):
    service, _ = system()
    with pytest.raises(EventContractError, match="authenticated_principal"):
        service.subscribe(bad, pr_request())


def test_authorization_denied_before_callback():
    challenge_called = []
    service, store = system(
        authorized=lambda p, n, a: False,
        verified=lambda u, k, i: challenge_called.append(i) or True,
    )
    with pytest.raises(EventContractError, match="event_scope_not_authorized"):
        service.subscribe("owner-1", pr_request())
    assert not store.records and not challenge_called


@pytest.mark.parametrize("invalid", [None, 0, -1, True, DEFAULT_TTL_MS * 100])
def test_ttl_policy_rejects_invalid_requested_duration(invalid):
    service, _ = system()
    with pytest.raises(EventContractError):
        service.subscribe("owner-1", pr_request(ttlMs=invalid))


def test_custom_valid_ttl_and_expiry_excluded():
    service, store = system()
    receipt = service.subscribe("owner-1", pr_request(ttlMs=3600000))
    assert receipt["refreshBefore"] == "2026-11-20T13:00:00Z"
    service.now = lambda: NOW + timedelta(hours=2)
    assert service.recipients(pr_event()) == []


def test_late_access_revocation_stops_fanout_without_mutation():
    access = {"valid": True}
    service, store = system(authorized=lambda p, n, a: access["valid"])
    service.subscribe("owner-1", pr_request())
    assert len(service.recipients(pr_event())) == 1
    access["valid"] = False
    assert service.recipients(pr_event()) == []
    assert len(store.records) == 1


def test_matching_pr_filter_excludes_others_and_ci():
    service, _ = system()
    service.subscribe("owner-1", pr_request())
    assert len(service.recipients(pr_event())) == 1
    assert service.recipients(pr_event(pr=6884)) == []
    assert service.recipients(ci_event()) == []


def test_ci_filter_excludes_other_events():
    service, _ = system()
    service.subscribe("owner-1", ci_request())
    assert len(service.recipients(ci_event())) == 1
    assert service.recipients(pr_event()) == []


def test_cursor_non_null_not_supported():
    service, store = system()
    with pytest.raises(EventContractError, match="replay_cursor_not_supported"):
        service.subscribe("owner-1", pr_request(cursor="old"))
    assert store.records == {}


def test_unsubscribe_is_idempotent_and_owner_bound():
    service, store = system()
    id1 = service.subscribe("owner-1", pr_request())["id"]
    params = {
        "name": PR_EVENT, "arguments": {"repository": MGAP_REPO, "pr_number": 6883},
        "delivery": {"mode": "webhook", "url": URL},
    }
    assert service.unsubscribe("owner-1", params) == {}
    assert service.unsubscribe("owner-1", params) == {}
    assert store.get(id1) is None


def test_subscription_request_fails_on_invalid_delivery_fields():
    service, _ = system()
    with pytest.raises(EventContractError, match="delivery_fields_invalid"):
        service.subscribe("owner-1", pr_request(delivery={
            "mode": "webhook", "url": URL, "secret": SECRET, "unexpected": True
        }))


def test_postgres_master_key_validation_without_database_access():
    for key in ("", "bad", base64.b64encode(b"c" * 16).decode("ascii")):
        with pytest.raises(EventContractError):
            PostgresSubscriptionStore("postgresql://unused", key)


def test_postgres_aes_gcm_ciphertext_and_aad_tamper():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from kuuos_mcp_bridge.event_subscriptions import Subscription, _identity
    arguments = {"repository": MGAP_REPO, "pr_number": 6883}
    identity = _identity("owner-1", PR_EVENT, arguments, URL)
    sub = Subscription(identity, "owner-1", PR_EVENT, arguments, URL, SECRET, NOW, NOW)
    store = object.__new__(PostgresSubscriptionStore)
    store._aes = AESGCM(b"d" * 32)
    cipher = store._seal(sub)
    assert SECRET.encode("utf-8") not in cipher
    assert store._unseal(identity, cipher) == SECRET
    with pytest.raises(EventContractError, match="encrypted_secret_invalid"):
        store._unseal("sub_" + "0" * 64, cipher)
    with pytest.raises(EventContractError, match="encrypted_secret_invalid"):
        store._unseal(identity, cipher[:-1] + bytes([cipher[-1] ^ 1]))
