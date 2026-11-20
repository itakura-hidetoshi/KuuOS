"""Staging source-to-events integration with no claim of CI terminal truth."""
from __future__ import annotations

import base64
import json
from dataclasses import replace
from datetime import datetime, timezone

import pytest

from kuuos_mcp_bridge.event_delivery import PostResult
from kuuos_mcp_bridge.event_outbox import MemoryOutboxStore
from kuuos_mcp_bridge.event_pipeline import deliver_one
from kuuos_mcp_bridge.event_subscriptions import (
    MemorySubscriptionStore, SubscriptionManager,
)
from kuuos_mcp_bridge.github_event_contract import (
    CI_GATES_EVENT, CI_GATES_WORKFLOW, KUUOS_REPO, MGAP_REPO,
)
from kuuos_mcp_bridge.github_oidc_source import (
    CI_WORKFLOW_REF, FEATURE_REF, GitHubOIDCSourceError, VerifiedSource,
    compile_verified_oidc_ci_gates, stage_verified_oidc_ci_gates,
)

KEY = "whsec_" + base64.b64encode(b"o" * 32).decode("ascii")
DEST = "https://synthetic-mcp-receiver.example.org/ci-gates"


def source(run_id=44833605981, *, kind="ci_jobs_observed", sha="a"*40):
    return VerifiedSource(
        identity="oidc_" + "f"*64, repository=KUUOS_REPO,
        workflow_ref=CI_WORKFLOW_REF, ref=FEATURE_REF,
        head_sha=sha, run_id=run_id, run_attempt=1,
        jti_hash="d"*64, kind=kind,
    )


def setup_manager(*, authorized=True, workflow=CI_GATES_WORKFLOW):
    store = MemorySubscriptionStore()
    mgr = SubscriptionManager(
        store,
        authorize=lambda principal, name, args: (
            principal == "synthetic-owner"
            and name == CI_GATES_EVENT
            and args.get("repository") == KUUOS_REPO
            and authorized
        ),
        verify_callback=lambda url, key, sub: True,
        now=lambda: datetime.now(timezone.utc),
    )
    receipt = mgr.subscribe("synthetic-owner", {
        "name": CI_GATES_EVENT,
        "arguments": {"repository": KUUOS_REPO, "workflow_name": workflow},
        "delivery": {"mode": "webhook", "url": DEST, "secret": KEY},
    })
    assert receipt["id"].startswith("sub_")
    return mgr, MemoryOutboxStore()


class Poster:
    def __init__(self):
        self.calls = []

    def post(self, url, body, headers):
        self.calls.append((url, body, headers))
        return PostResult(200, b"{}")


def test_genuine_oidc_gate_packet_is_non_authoritative_and_stable():
    packet = compile_verified_oidc_ci_gates(source())
    duplicate = compile_verified_oidc_ci_gates(source())
    assert packet["eventId"] == duplicate["eventId"]
    assert packet["name"] == CI_GATES_EVENT
    assert packet["data"]["github_oidc_signature_verified"] is True
    assert packet["data"]["ci_terminal_conclusion_verified"] is False
    assert packet["data"]["signal_is_success_evidence"] is False
    assert packet["data"]["fresh_mcp_reobservation_required"] is True
    assert packet["data"]["merge_authority_granted"] is False
    assert "conclusion" not in packet["data"]
    assert compile_verified_oidc_ci_gates(source(44833605982))["eventId"] != packet["eventId"]


def test_unverified_push_or_impersonated_workflow_cannot_create_ci_gate():
    with pytest.raises(GitHubOIDCSourceError, match="source_not_allowed"):
        compile_verified_oidc_ci_gates(source(kind="push_observed"))
    with pytest.raises(GitHubOIDCSourceError, match="source_not_allowed"):
        compile_verified_oidc_ci_gates(replace(source(), workflow_ref="fake/ref"))
    with pytest.raises(GitHubOIDCSourceError, match="source_not_allowed"):
        compile_verified_oidc_ci_gates(replace(source(), repository=MGAP_REPO))


def test_real_pipeline_stage_delivery_replay_never_promotes_ci():
    manager, outbox = setup_manager()
    packet, ids = stage_verified_oidc_ci_gates(source(), manager, outbox)
    assert len(ids) == 1
    packet2, ids2 = stage_verified_oidc_ci_gates(source(), manager, outbox)
    assert packet2["eventId"] == packet["eventId"] and ids2 == ids
    assert len(outbox.records) == 1
    poster = Poster()
    delivered = deliver_one(manager, outbox, poster=poster, outbox_id=ids[0])
    assert delivered["state"] == "delivered"
    assert delivered["signal_is_success_evidence"] is False
    assert len(poster.calls) == 1
    data = json.loads(poster.calls[0][1])["data"]
    assert data["ci_terminal_conclusion_verified"] is False
    assert data["fresh_mcp_reobservation_required"] is True
    assert deliver_one(manager, outbox, poster=poster, outbox_id=ids[0])["state"] == "no_due_events"
    assert len(poster.calls) == 1


def test_revoked_rights_before_delivery_do_not_send():
    rights = {"allowed": True}
    store = MemorySubscriptionStore()
    manager = SubscriptionManager(
        store,
        authorize=lambda p, n, a: rights["allowed"],
        verify_callback=lambda *a: True,
    )
    manager.subscribe("owner", {
        "name": CI_GATES_EVENT,
        "arguments": {"repository": KUUOS_REPO, "workflow_name": CI_GATES_WORKFLOW},
        "delivery": {"mode": "webhook", "url": DEST, "secret": KEY},
    })
    outbox = MemoryOutboxStore()
    _, ids = stage_verified_oidc_ci_gates(source(), manager, outbox)
    assert len(ids) == 1
    rights["allowed"] = False
    poster = Poster()
    result = deliver_one(manager, outbox, poster=poster, outbox_id=ids[0])
    assert result["state"] == "recipient_revoked"
    assert not poster.calls


def test_no_matching_subscription_emits_no_outbox_writes():
    store = MemorySubscriptionStore()
    manager = SubscriptionManager(store, authorize=lambda *args: False,
                                  verify_callback=lambda *args: False)
    outbox = MemoryOutboxStore()
    packet, ids = stage_verified_oidc_ci_gates(source(), manager, outbox)
    assert packet["name"] == CI_GATES_EVENT
    assert ids == [] and outbox.records == {}
