"""SSRF-hardened Standard Webhooks delivery for typed KuuOS MCP wake-ups.

This module has no automatic network or background activity. The caller must
first authenticate the ingress, verify the subscription owner's current access,
and select a persisted eligible subscription. CI event packets never grant Git
write or merge authority; delivery is a signal for independent MCP re-checking.
"""
from __future__ import annotations

import http.client
import ipaddress
import json
import secrets
import socket
import ssl
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Mapping
from urllib.parse import urlsplit

from .event_subscriptions import Subscription
from .github_event_contract import (
    EventContractError, matches_filters, standard_webhook_signature,
    validate_delivery_url,
)

MAX_BODY_BYTES = 262_144
MAX_RESPONSE_BYTES = 4_096
MAX_ADDRESSES = 16
DEFAULT_TIMEOUT_SECONDS = 8.0
MAX_DELIVERY_ATTEMPTS = 3
TERMINAL_CODES = frozenset({410, 413})


class EventDeliveryError(RuntimeError):
    """Non-sensitive category; never place callback URLs or keys in messages."""


@dataclass(frozen=True)
class PostResult:
    status: int
    body: bytes


@dataclass(frozen=True)
class DeliveryReceipt:
    event_id: str
    subscription_id: str
    outcome: str
    attempts: int
    last_status: int | None

    def public(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "subscription_id": self.subscription_id,
            "outcome": self.outcome,
            "attempts": self.attempts,
            "last_http_status": self.last_status,
            "event_is_success_evidence": False,
            "merge_authority_granted": False,
        }


def _global_ip(value: str) -> bool:
    try:
        parsed = ipaddress.ip_address(value)
        return parsed.is_global
    except ValueError:
        return False


def resolve_public_addresses(
    hostname: str,
    *,
    resolver: Callable[..., list[Any]] = socket.getaddrinfo,
) -> list[tuple[int, str]]:
    """Reject a DNS answer if ANY address is not globally routable.

    Every returned address is revalidated before a connection. The socket
    connects to this numerical address, never re-resolves the hostname.
    """
    if not isinstance(hostname, str) or not hostname:
        raise EventDeliveryError("dns_host_invalid")
    normalized = hostname.lower().rstrip(".")
    if any(normalized == suffix or normalized.endswith("." + suffix) for suffix in
           ("localhost", "local", "internal", "invalid", "test", "onion")):
        raise EventDeliveryError("dns_hostname_reserved")
    try:
        encoded = hostname.encode("idna").decode("ascii")
        results = resolver(encoded, 443, type=socket.SOCK_STREAM)
    except (OSError, ValueError, UnicodeError) as exc:
        raise EventDeliveryError("dns_resolution_failed") from exc
    if not results or len(results) > MAX_ADDRESSES:
        raise EventDeliveryError("dns_address_count_invalid")
    addresses: list[tuple[int, str]] = []
    for item in results:
        if not isinstance(item, (list, tuple)) or len(item) < 5:
            raise EventDeliveryError("dns_record_invalid")
        family, _, _, _, sockaddr = item
        if family not in (socket.AF_INET, socket.AF_INET6):
            raise EventDeliveryError("dns_family_not_allowed")
        if not isinstance(sockaddr, (list, tuple)) or not sockaddr:
            raise EventDeliveryError("dns_record_invalid")
        address = sockaddr[0]
        if not isinstance(address, str) or not _global_ip(address):
            raise EventDeliveryError("dns_address_not_public")
        if (family, address) not in addresses:
            addresses.append((family, address))
    return addresses


class PinnedHTTPSPoster:
    """TLS hostname verified while TCP connects to a vetted public literal IP.

    It bypasses ambient HTTP proxies; redirects are never followed. A fresh
    DNS resolution and global-IP check occurs on every post/retry.
    """

    def __init__(self, *, timeout: float = DEFAULT_TIMEOUT_SECONDS):
        if not 0 < timeout <= 15:
            raise ValueError("invalid_callback_timeout")
        self.timeout = timeout

    def post(self, url: str, body: bytes, headers: Mapping[str, str]) -> PostResult:
        try:
            validate_delivery_url(url)
            parsed = urlsplit(url)
            hostname = parsed.hostname
            if hostname is None:
                raise EventDeliveryError("callback_hostname_invalid")
            if not isinstance(body, bytes) or len(body) > MAX_BODY_BYTES:
                raise EventDeliveryError("callback_body_over_limit")
            addresses = resolve_public_addresses(hostname)
            target = parsed.path or "/"
            if parsed.query:
                target += "?" + parsed.query
            context = ssl.create_default_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_2
        except (ValueError, EventContractError) as exc:
            raise EventDeliveryError("callback_preflight_failed") from exc

        # A rejected DNS answer is fatal: do not fall back to unpinned DNS.
        last_error: Exception | None = None
        for family, ip in addresses:
            sock = None
            connection = None
            try:
                sock = socket.socket(family, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                dest = (ip, 443) if family == socket.AF_INET else (ip, 443, 0, 0)
                sock.connect(dest)
                verified = context.wrap_socket(sock, server_hostname=hostname)
                sock = None  # Ownership transferred to the verified TLS socket.
                connection = http.client.HTTPConnection(hostname, port=443, timeout=self.timeout)
                connection.sock = verified
                safe_headers = {str(k): str(v) for k, v in headers.items()}
                safe_headers["Host"] = hostname
                connection.request("POST", target, body=body, headers=safe_headers)
                response = connection.getresponse()
                payload = response.read(MAX_RESPONSE_BYTES + 1)
                if len(payload) > MAX_RESPONSE_BYTES:
                    raise EventDeliveryError("callback_response_too_large")
                # 3xx is returned as a non-success outcome, never followed.
                return PostResult(response.status, payload)
            except (OSError, ssl.SSLError, http.client.HTTPException) as exc:
                last_error = exc
            finally:
                if connection is not None:
                    connection.close()
                if sock is not None:
                    sock.close()
        raise EventDeliveryError("callback_connection_failed") from last_error


def _webhook_headers(
    event_id: str, timestamp: int, body: bytes, secret: str, subscription_id: str,
    *, previous_secret: str | None = None,
    previous_secret_until: datetime | None = None,
) -> dict[str, str]:
    if len(body) > MAX_BODY_BYTES:
        raise EventDeliveryError("callback_body_over_limit")
    signature = standard_webhook_signature(event_id, timestamp, body, secret)
    if previous_secret is not None and previous_secret_until is not None:
        if previous_secret_until.tzinfo is None:
            raise EventDeliveryError("previous_key_expiry_without_timezone")
        if datetime.fromtimestamp(timestamp, timezone.utc) < previous_secret_until:
            signature += " " + standard_webhook_signature(
                event_id, timestamp, body, previous_secret
            )
    return {
        "Content-Type": "application/json",
        "webhook-id": event_id,
        "webhook-timestamp": str(timestamp),
        "webhook-signature": signature,
        "X-MCP-Subscription-Id": subscription_id,
    }


def verify_callback_challenge(
    url: str,
    secret: str,
    subscription_id: str,
    *,
    poster: Any | None = None,
    now_seconds: Callable[[], int] = lambda: int(time.time()),
    challenge_factory: Callable[[], str] = lambda: secrets.token_urlsafe(32),
) -> bool:
    """Signed one-use challenge; fails closed and never persists subscriptions."""
    client = poster if poster is not None else PinnedHTTPSPoster()
    challenge = challenge_factory()
    if not isinstance(challenge, str) or len(challenge) < 24:
        raise EventDeliveryError("challenge_entropy_insufficient")
    control = {"type": "verification", "challenge": challenge}
    body = json.dumps(control, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    event_id = "msg_verification_" + secrets.token_hex(16)
    headers = _webhook_headers(event_id, now_seconds(), body, secret, subscription_id)
    try:
        response = client.post(url, body, headers)
        if not 200 <= response.status < 300:
            return False
        if len(response.body) > MAX_RESPONSE_BYTES:
            return False
        decoded = json.loads(response.body)
        returned = decoded.get("challenge") if isinstance(decoded, dict) else None
        return isinstance(returned, str) and secrets.compare_digest(
            challenge.encode("utf-8"), returned.encode("utf-8")
        )
    except (OSError, EventDeliveryError, ValueError, UnicodeError, json.JSONDecodeError):
        return False


def _packet(event: Mapping[str, Any]) -> bytes:
    if not isinstance(event, Mapping):
        raise EventDeliveryError("event_not_mapping")
    if set(event) != {"eventId", "name", "timestamp", "data", "cursor"}:
        raise EventDeliveryError("event_shape_invalid")
    data = event.get("data")
    if not isinstance(data, Mapping):
        raise EventDeliveryError("event_data_invalid")
    if data.get("fresh_mcp_reobservation_required") is not True or data.get("signal_is_success_evidence") is not False:
        raise EventDeliveryError("event_truth_boundary_invalid")
    if data.get("merge_authority_granted") is not False or data.get("write_authority_granted") is not False:
        raise EventDeliveryError("event_authority_boundary_invalid")
    if event.get("cursor") is not None:
        raise EventDeliveryError("event_replay_not_supported")
    event_id = event.get("eventId")
    if not isinstance(event_id, str) or not event_id.startswith("evt_"):
        raise EventDeliveryError("event_id_invalid")
    encoded = json.dumps(event, separators=(",", ":"), ensure_ascii=False,
                         allow_nan=False).encode("utf-8")
    if len(encoded) > MAX_BODY_BYTES:
        raise EventDeliveryError("event_body_over_limit")
    return encoded


def deliver_event(
    subscription: Subscription,
    event: Mapping[str, Any],
    *,
    poster: Any | None = None,
    now_seconds: Callable[[], int] = lambda: int(time.time()),
    sleep: Callable[[float], None] = time.sleep,
    max_attempts: int = MAX_DELIVERY_ATTEMPTS,
) -> DeliveryReceipt:
    """Bounded synchronous delivery attempt; a durable outbox is still needed."""
    if not 1 <= max_attempts <= MAX_DELIVERY_ATTEMPTS:
        raise EventDeliveryError("retry_budget_invalid")
    if subscription.name != event.get("name") or not matches_filters(event, subscription.arguments):
        raise EventDeliveryError("event_subscription_mismatch")
    data = _record(event.get("data"))
    if not data:
        raise EventDeliveryError("event_data_invalid")
    body = _packet(event)
    client = poster if poster is not None else PinnedHTTPSPoster()
    event_id = str(event["eventId"])
    last_status: int | None = None
    for attempt in range(1, max_attempts + 1):
        timestamp = now_seconds()
        headers = _webhook_headers(
            event_id, timestamp, body, subscription.secret, subscription.id,
            previous_secret=subscription.previous_secret,
            previous_secret_until=subscription.previous_secret_until,
        )
        try:
            result = client.post(subscription.callback_url, body, headers)
        except (OSError, EventDeliveryError, http.client.HTTPException):
            result = None
        if result is not None:
            last_status = result.status
            if 200 <= result.status < 300:
                return DeliveryReceipt(event_id, subscription.id, "accepted", attempt, last_status)
            if result.status in TERMINAL_CODES or 400 <= result.status < 500:
                return DeliveryReceipt(event_id, subscription.id, "permanent_failure", attempt, last_status)
        if attempt < max_attempts:
            sleep(min(2 ** (attempt - 1) / 4, 2))
    return DeliveryReceipt(event_id, subscription.id, "retry_exhausted", max_attempts, last_status)


def _record(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}
