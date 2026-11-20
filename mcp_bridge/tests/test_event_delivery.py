from __future__ import annotations

import base64
import hashlib
import hmac
import json
import socket
from datetime import datetime, timezone

import pytest

from kuuos_mcp_bridge.event_delivery import (
    MAX_BODY_BYTES,
    DeliveryReceipt,
    EventDeliveryError,
    PinnedHTTPSPoster,
    PostResult,
    deliver_event,
    resolve_public_addresses,
    verify_callback_challenge,
)
from kuuos_mcp_bridge.event_subscriptions import Subscription, _identity
from kuuos_mcp_bridge.github_event_contract import (
    CI_EVENT,
    MGAP_REPO,
    PR_EVENT,
    compile_ci_completed,
    compile_pr_head_updated,
)


URL = "https://receiver.example.com/mcp-events"
KEY_BYTES = b"k" * 32
SECRET = "whsec_" + base64.b64encode(KEY_BYTES).decode("ascii")
NOW = datetime(2026, 11, 20, 12, tzinfo=timezone.utc)


def ci_event():
    return compile_ci_completed({
        "action": "completed",
        "repository": {"full_name": MGAP_REPO},
        "workflow_run": {
            "id": 42, "run_attempt": 1, "name": "PR Lean Fast Check",
            "event": "pull_request", "status": "completed",
            "conclusion": "success", "head_sha": "a" * 40,
        },
    })


def pr_event():
    return compile_pr_head_updated({
        "action": "synchronize", "repository": {"full_name": MGAP_REPO},
        "pull_request": {
            "number": 6883,
            "head": {"sha": "a" * 40, "repo": {"full_name": MGAP_REPO}},
            "base": {"ref": "formal/real-hilbert-uniform-coercive-strong-limit"},
        },
    })


def subscription(name=CI_EVENT, arguments=None):
    if arguments is None:
        arguments = {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"}
    subid = _identity("owner-1", name, arguments, URL)
    return Subscription(subid, "owner-1", name, arguments, URL, SECRET, NOW, NOW)


class Recorder:
    def __init__(self, statuses=None):
        self.statuses = list(statuses or [200])
        self.calls = []

    def post(self, url, body, headers):
        self.calls.append((url, body, headers))
        status = self.statuses.pop(0)
        if isinstance(status, Exception):
            raise status
        return PostResult(status, b"{}")


def public_answers(addresses):
    return [
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, 443))
        for address in addresses
    ]


def test_resolver_all_public_addresses_accepted():
    got = resolve_public_addresses(
        "callback.example.com",
        resolver=lambda *args, **kwargs: public_answers(["8.8.8.8", "1.1.1.1"]),
    )
    assert got == [(socket.AF_INET, "8.8.8.8"), (socket.AF_INET, "1.1.1.1")]


@pytest.mark.parametrize("host", [
    "localhost", "foo.localhost", "foo.local", "worker.internal",
    "local.invalid", "node.test", "something.onion",
])
def test_resolver_blocks_reserved_hostnames_without_dns_calls(host):
    def forbidden_resolver(*args, **kwargs):
        pytest.fail("reserved host must never be resolved")
    with pytest.raises(EventDeliveryError, match="dns_hostname_reserved"):
        resolve_public_addresses(host, resolver=forbidden_resolver)


@pytest.mark.parametrize("ip", [
    "127.0.0.1", "10.0.0.1", "172.16.0.1", "169.254.0.1",
    "192.168.1.1", "100.64.0.1", "0.0.0.0",
    "203.0.113.1", "192.0.2.1",
])
def test_resolver_blocks_non_global_addresses(ip):
    with pytest.raises(EventDeliveryError, match="dns_address_not_public"):
        resolve_public_addresses(
            "callback.example.com",
            resolver=lambda *args, **kwargs: public_answers([ip]),
        )


def test_resolver_blocks_mixed_public_private_addresses():
    with pytest.raises(EventDeliveryError, match="dns_address_not_public"):
        resolve_public_addresses(
            "callback.example.com",
            resolver=lambda *args, **kwargs: public_answers(["8.8.8.8", "127.0.0.1"]),
        )


def test_resolver_blocks_empty_and_oversized_dns_answers():
    with pytest.raises(EventDeliveryError, match="dns_address_count_invalid"):
        resolve_public_addresses("callback.example.com", resolver=lambda *a, **k: [])
    with pytest.raises(EventDeliveryError, match="dns_address_count_invalid"):
        resolve_public_addresses(
            "callback.example.com",
            resolver=lambda *a, **k: public_answers(["8.8.8.8"] * 17),
        )


def test_poster_preflight_rejects_http_without_dns_or_network():
    with pytest.raises(EventDeliveryError, match="callback_preflight_failed"):
        PinnedHTTPSPoster().post("http://callback.example.com", b"{}", {})


def test_challenge_success_uses_signed_headers_and_exact_body():
    class Echo:
        def __init__(self):
            self.called = []
        def post(self, url, body, headers):
            self.called.append((url, body, headers))
            return PostResult(200, json.dumps({
                "challenge": json.loads(body)["challenge"]
            }).encode("utf-8"))
    p = Echo()
    ok = verify_callback_challenge(
        URL, SECRET, "sub_123", poster=p,
        now_seconds=lambda: 1788000000, challenge_factory=lambda: "x" * 32,
    )
    assert ok is True
    url, body, headers = p.called[0]
    assert url == URL
    assert headers["webhook-id"].startswith("msg_verification_")
    assert headers["X-MCP-Subscription-Id"] == "sub_123"
    assert headers["webhook-timestamp"] == "1788000000"
    assert json.loads(body)["type"] == "verification"
    to_sign = headers["webhook-id"].encode() + b".1788000000." + body
    expected = "v1," + base64.b64encode(
        hmac.new(KEY_BYTES, to_sign, hashlib.sha256).digest()
    ).decode("ascii")
    assert headers["webhook-signature"] == expected


def test_challenge_rejects_wrong_response_and_http_errors():
    class Bad:
        def __init__(self, code, content):
            self.code = code
            self.content = content
        def post(self, *args):
            return PostResult(self.code, self.content)
    assert verify_callback_challenge(
        URL, SECRET, "sub_x", poster=Bad(200, b'{"challenge":"wrong"}')
    ) is False
    assert verify_callback_challenge(
        URL, SECRET, "sub_x", poster=Bad(301, b'{"challenge":"x"}')
    ) is False
    assert verify_callback_challenge(
        URL, SECRET, "sub_x", poster=Bad(200, b'not-json')
    ) is False


def test_challenge_rejects_bounded_response_and_short_entropy():
    class Over:
        def post(self, *args):
            return PostResult(200, b"x" * 5000)
    assert verify_callback_challenge(
        URL, SECRET, "sub_1", poster=Over()
    ) is False
    with pytest.raises(EventDeliveryError, match="challenge_entropy_insufficient"):
        verify_callback_challenge(
            URL, SECRET, "sub_1", poster=Over(), challenge_factory=lambda: "x"
        )


def test_successful_delivery_preserves_non_authority_and_signature():
    poster = Recorder()
    event = ci_event()
    receipt = deliver_event(subscription(), event, poster=poster, now_seconds=lambda: 1788000000)
    assert receipt.public()["outcome"] == "accepted"
    assert receipt.public()["event_is_success_evidence"] is False
    assert receipt.public()["merge_authority_granted"] is False
    assert SECRET not in repr(receipt.public())
    url, body, headers = poster.calls[0]
    assert json.loads(body)["data"]["signal_is_success_evidence"] is False
    assert headers["webhook-id"] == event["eventId"]
    assert headers["X-MCP-Subscription-Id"] == subscription().id
    msg = (headers["webhook-id"] + ".1788000000.").encode() + body
    expected = hmac.new(KEY_BYTES, msg, hashlib.sha256).digest()
    assert headers["webhook-signature"] == "v1," + base64.b64encode(expected).decode()


def test_delivery_5xx_retries_and_body_event_id_remain_stable():
    poster = Recorder([503, 202])
    delays = []
    result = deliver_event(
        subscription(), ci_event(), poster=poster, sleep=delays.append,
        now_seconds=iter([1788000000, 1788000001]).__next__,
    )
    assert result.outcome == "accepted" and result.attempts == 2
    assert len(delays) == 1
    assert poster.calls[0][1] == poster.calls[1][1]
    assert poster.calls[0][2]["webhook-id"] == poster.calls[1][2]["webhook-id"]
    assert poster.calls[0][2]["webhook-timestamp"] != poster.calls[1][2]["webhook-timestamp"]
    assert poster.calls[0][2]["webhook-signature"] != poster.calls[1][2]["webhook-signature"]


@pytest.mark.parametrize("code", [400, 401, 403, 410, 413])
def test_delivery_4xx_never_retried(code):
    poster = Recorder([code, 200])
    result = deliver_event(subscription(), ci_event(), poster=poster)
    assert result.outcome == "permanent_failure"
    assert result.attempts == 1
    assert len(poster.calls) == 1


def test_delivery_retry_budget_exhaustion():
    poster = Recorder([503, 503, 503])
    result = deliver_event(
        subscription(), ci_event(), poster=poster, sleep=lambda t: None
    )
    assert result.outcome == "retry_exhausted"
    assert result.attempts == 3


def test_unrelated_event_never_sent():
    poster = Recorder()
    with pytest.raises(EventDeliveryError, match="event_subscription_mismatch"):
        deliver_event(subscription(), pr_event(), poster=poster)
    assert poster.calls == []


def test_oversize_packet_never_sent():
    poster = Recorder()
    packet = ci_event()
    packet["data"]["padding"] = "x" * MAX_BODY_BYTES
    with pytest.raises(EventDeliveryError, match="event_body_over_limit"):
        deliver_event(subscription(), packet, poster=poster)
    assert poster.calls == []


def test_claim_of_success_or_authority_never_sent():
    for field, val in [
        ("signal_is_success_evidence", True),
        ("fresh_mcp_reobservation_required", False),
        ("merge_authority_granted", True),
        ("write_authority_granted", True),
    ]:
        packet = ci_event()
        packet["data"][field] = val
        with pytest.raises(EventDeliveryError):
            deliver_event(subscription(), packet, poster=Recorder())


def test_unknown_fields_and_cursor_not_sent():
    packet = ci_event()
    packet["extra"] = "untrusted"
    with pytest.raises(EventDeliveryError, match="event_shape_invalid"):
        deliver_event(subscription(), packet, poster=Recorder())
    packet = ci_event()
    packet["cursor"] = "replay"
    with pytest.raises(EventDeliveryError, match="event_replay_not_supported"):
        deliver_event(subscription(), packet, poster=Recorder())
