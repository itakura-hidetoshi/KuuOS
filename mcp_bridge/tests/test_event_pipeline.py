from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone

import pytest

from kuuos_mcp_bridge.event_delivery import PostResult
from kuuos_mcp_bridge.event_outbox import MemoryOutboxStore
from kuuos_mcp_bridge.event_subscriptions import MemorySubscriptionStore, SubscriptionManager
from kuuos_mcp_bridge.event_pipeline import stage_signed_event, deliver_one
from kuuos_mcp_bridge.github_event_contract import CI_EVENT, MGAP_REPO

NOW = datetime(2026, 11, 20, 14, tzinfo=timezone.utc)
SECRET = "a" * 40


def signed_event():
    payload = {
        "action": "completed", "repository": {"full_name": MGAP_REPO},
        "workflow_run": {"id": 42, "run_attempt": 1, "name": "PR Lean Fast Check",
                         "event": "pull_request", "head_sha": "b" * 40,
                         "status": "completed", "conclusion": "failure"},
    }
    body = json.dumps(payload, sort_keys=True).encode()
    return {
        "event_type": "workflow_run", "raw_body": body,
        "github_signature": "sha256=" + hmac.new(
            SECRET.encode(), body, hashlib.sha256
        ).hexdigest(),
        "github_secret": SECRET,
        "delivery_id": "a20f3142-0b52-4ea4-a93b-3412cf17f010",
    }


def setup():
    rights = {"active": True}
    subs = MemorySubscriptionStore()
    mgr = SubscriptionManager(
        subs, authorize=lambda p, n, a: rights["active"],
        verify_callback=lambda u, s, i: True, now=lambda: NOW,
    )
    mgr.subscribe("owner-1", {
        "name": CI_EVENT,
        "arguments": {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"},
        "delivery": {"mode": "webhook", "url": "https://receiver.example.com/events",
                     "secret": "whsec_" + base64.b64encode(b"a" * 32).decode()},
    })
    return mgr, MemoryOutboxStore(), rights


class Poster:
    def __init__(self, status=200):
        self.status, self.calls = status, []
    def post(self, url, body, headers):
        self.calls.append((url, body, headers))
        return PostResult(self.status, b"ok")


def test_duplicate_signed_source_event_enqueues_only_once():
    mgr, outbox, _ = setup()
    one = stage_signed_event(mgr, outbox, **signed_event(), now=NOW)
    two = stage_signed_event(mgr, outbox, **signed_event(), now=NOW)
    assert one["outbox_ids"] == two["outbox_ids"]
    assert len(outbox.records) == 1
    assert one["signal_is_success_evidence"] is False


def test_revoked_access_is_checked_before_delivery():
    mgr, outbox, rights = setup()
    stage_signed_event(mgr, outbox, **signed_event(), now=NOW)
    rights["active"] = False
    poster = Poster()
    result = deliver_one(mgr, outbox, poster=poster, now=NOW)
    assert result["state"] == "recipient_revoked"
    assert poster.calls == []


def test_delivered_event_never_proves_ci_or_merge_authority():
    mgr, outbox, _ = setup()
    stage_signed_event(mgr, outbox, **signed_event(), now=NOW)
    poster = Poster()
    result = deliver_one(mgr, outbox, poster=poster, now=NOW)
    assert result["state"] == "delivered"
    assert result["signal_is_success_evidence"] is False
    assert result["fresh_mcp_reobservation_required"] is True
    assert len(poster.calls) == 1


def test_5xx_is_retried_on_later_event_trigger():
    mgr, outbox, _ = setup()
    stage_signed_event(mgr, outbox, **signed_event(), now=NOW)
    assert deliver_one(mgr, outbox, poster=Poster(503), now=NOW)["state"] == "pending"
    assert deliver_one(mgr, outbox, poster=Poster(), now=NOW)["state"] == "no_due_events"
    assert deliver_one(mgr, outbox, poster=Poster(), now=NOW + timedelta(seconds=2))["state"] == "delivered"


def test_410_permanently_stops_delivery():
    mgr, outbox, _ = setup()
    stage_signed_event(mgr, outbox, **signed_event(), now=NOW)
    assert deliver_one(mgr, outbox, poster=Poster(410), now=NOW)["state"] == "permanent_failure"
    assert deliver_one(mgr, outbox, poster=Poster(), now=NOW + timedelta(days=1))["state"] == "no_due_events"


def test_tampered_signature_has_no_outbox_side_effects():
    mgr, outbox, _ = setup()
    bad = signed_event()
    bad["raw_body"] += b" "
    with pytest.raises(Exception):
        stage_signed_event(mgr, outbox, **bad, now=NOW)
    assert outbox.records == {}


def test_specific_new_event_delivered_without_claiming_older_backlog():
    mgr, outbox, _ = setup()
    first = stage_signed_event(mgr, outbox, **signed_event(), now=NOW)
    older_id = first["outbox_ids"][0]
    newest = signed_event()
    raw = json.loads(newest["raw_body"])
    raw["workflow_run"]["id"] = 43
    newest["raw_body"] = json.dumps(raw, sort_keys=True).encode()
    newest["github_signature"] = "sha256=" + hmac.new(
        SECRET.encode(), newest["raw_body"], hashlib.sha256
    ).hexdigest()
    second = stage_signed_event(mgr, outbox, **newest, now=NOW)
    fresh_id = second["outbox_ids"][0]
    assert older_id != fresh_id
    p = Poster()
    result = deliver_one(mgr, outbox, poster=p, now=NOW, outbox_id=fresh_id)
    assert result["state"] == "delivered"
    assert json.loads(p.calls[0][1])["data"]["run_id"] == 43
    assert outbox.records[older_id].state == "pending"
    assert deliver_one(mgr, outbox, poster=p, now=NOW, outbox_id=fresh_id)["state"] == "no_due_events"
    assert len(p.calls) == 1
