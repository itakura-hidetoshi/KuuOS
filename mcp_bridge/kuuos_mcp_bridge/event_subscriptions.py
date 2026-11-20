"""Account-bound, fail-closed MCP Events subscription state.

Only the protocol-side contract is implemented here. Production wiring MUST
provide authenticated principal identity, current repository authorization,
a DNS-pinned and TLS-verified callback challenge, and durable encrypted storage.
No outbound network calls or subscriptions are activated by importing this file.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Mapping, Protocol

from .github_event_contract import (
    EventContractError,
    decode_signing_secret,
    matches_filters,
    validate_delivery_url,
    validate_filters,
)

DEFAULT_TTL_MS = 7 * 24 * 60 * 60 * 1000
MAX_TTL_MS = 30 * 24 * 60 * 60 * 1000
MIN_TTL_MS = 60 * 60 * 1000
ROTATION_WINDOW_SECONDS = 600  # A bounded 10-minute two-signature transition.


@dataclass(frozen=True)
class Subscription:
    id: str
    principal: str
    name: str
    arguments: dict[str, Any]
    callback_url: str
    secret: str = field(repr=False)
    expires_at: datetime
    verified_at: datetime
    previous_secret: str | None = field(default=None, repr=False)
    previous_secret_until: datetime | None = None

    def public_receipt(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "refreshBefore": self.expires_at.isoformat().replace("+00:00", "Z"),
            "cursor": None,
            "truncated": False,
        }


class SubscriptionStore(Protocol):
    def get(self, subscription_id: str) -> Subscription | None: ...
    def upsert(self, subscription: Subscription) -> None: ...
    def delete(self, subscription_id: str, principal: str) -> None: ...
    def active(self, name: str, now: datetime) -> list[Subscription]: ...


class MemorySubscriptionStore:
    """Explicitly test-only. Never use as a multi-worker production store."""

    def __init__(self) -> None:
        self.records: dict[str, Subscription] = {}

    def get(self, subscription_id: str) -> Subscription | None:
        return self.records.get(subscription_id)

    def upsert(self, subscription: Subscription) -> None:
        self.records[subscription.id] = subscription

    def delete(self, subscription_id: str, principal: str) -> None:
        item = self.records.get(subscription_id)
        if item is not None and item.principal == principal:
            del self.records[subscription_id]

    def active(self, name: str, now: datetime) -> list[Subscription]:
        return [
            item for item in self.records.values()
            if item.name == name and item.expires_at > now
        ]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _principal(value: Any) -> str:
    if not isinstance(value, str) or not value or len(value) > 256:
        raise EventContractError("authenticated_principal_required")
    if value.strip() != value or any(ord(ch) < 32 for ch in value):
        raise EventContractError("authenticated_principal_invalid")
    return value


def _delivery(params: Mapping[str, Any], *, require_secret: bool) -> tuple[str, str | None]:
    delivery = params.get("delivery")
    if not isinstance(delivery, Mapping) or delivery.get("mode") != "webhook":
        raise EventContractError("webhook_delivery_required")
    expected = {"mode", "url", "secret"} if require_secret else {"mode", "url"}
    if set(delivery) != expected:
        raise EventContractError("delivery_fields_invalid")
    url = validate_delivery_url(delivery.get("url"))
    secret = delivery.get("secret")
    if require_secret:
        decode_signing_secret(secret)
    return url, secret


def _identity(principal: str, name: str, arguments: Mapping[str, Any], url: str) -> str:
    identity = {
        "principal": principal,
        "name": name,
        "arguments": dict(arguments),
        "callback_url": url,
    }
    raw = json.dumps(identity, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=False, allow_nan=False).encode("utf-8")
    return "sub_" + hashlib.sha256(raw).hexdigest()


def _ttl_ms(raw: Any) -> int:
    if raw is None:
        # Null means unbounded per protocol. This provider explicitly refuses
        # perpetual subscriptions; no implicit infinite access is granted.
        raise EventContractError("unbounded_subscription_not_supported")
    if type(raw) is not int or not MIN_TTL_MS <= raw <= MAX_TTL_MS:
        raise EventContractError("subscription_ttl_out_of_policy")
    return raw


class SubscriptionManager:
    """Protocol handler core; caller authenticates requests before invoking."""

    def __init__(
        self,
        store: SubscriptionStore,
        *,
        authorize: Callable[[str, str, Mapping[str, Any]], bool],
        verify_callback: Callable[[str, str, str], bool],
        now: Callable[[], datetime] = _utc_now,
    ):
        self.store = store
        self.authorize = authorize
        self.verify_callback = verify_callback
        self.now = now

    def _authorized(self, principal: str, name: str, arguments: Mapping[str, Any]) -> None:
        if not self.authorize(principal, name, arguments):
            raise EventContractError("event_scope_not_authorized")

    def subscribe(self, principal: str, params: Mapping[str, Any]) -> dict[str, Any]:
        subject = _principal(principal)
        if not isinstance(params, Mapping):
            raise EventContractError("subscription_request_not_mapping")
        if set(params) - {"name", "arguments", "delivery", "cursor", "ttlMs"}:
            raise EventContractError("subscription_fields_invalid")
        if params.get("cursor") is not None:
            raise EventContractError("replay_cursor_not_supported")
        name = params.get("name")
        arguments = validate_filters(name, params.get("arguments"))
        self._authorized(subject, name, arguments)
        url, key = _delivery(params, require_secret=True)
        assert isinstance(key, str)
        millis = _ttl_ms(params.get("ttlMs", DEFAULT_TTL_MS))
        now = self.now()
        if now.tzinfo is None:
            raise EventContractError("clock_must_be_timezone_aware")
        expires_at = now + timedelta(milliseconds=millis)
        subscription_id = _identity(subject, name, arguments, url)
        existing = self.store.get(subscription_id)
        already_verified = (
            existing is not None
            and existing.principal == subject
            and existing.expires_at > now
            and hmac.compare_digest(existing.secret, key)
        )
        # A prior verified callback may be refreshed with the same key.
        # New/rotated keys require a new signed challenge before persistence.
        if not already_verified and not self.verify_callback(url, key, subscription_id):
            raise EventContractError("callback_verification_failed")
        rotated = (
            existing is not None
            and existing.expires_at > now
            and not hmac.compare_digest(existing.secret, key)
        )
        # A second rapid key change could invalidate a still-live prior
        # ChatGPT signing key. Require the current transition to expire first.
        if (
            rotated and existing is not None
            and existing.previous_secret is not None
            and existing.previous_secret_until is not None
            and existing.previous_secret_until > now
        ):
            raise EventContractError("overlapping_key_rotation_not_supported")
        if rotated and existing is not None:
            previous_secret = existing.secret
            previous_until = min(
                existing.expires_at, now + timedelta(seconds=ROTATION_WINDOW_SECONDS)
            )
        elif (
            already_verified and existing is not None
            and existing.previous_secret is not None
            and existing.previous_secret_until is not None
            and existing.previous_secret_until > now
        ):
            previous_secret = existing.previous_secret
            previous_until = existing.previous_secret_until
        else:
            previous_secret = None
            previous_until = None
        record = Subscription(
            id=subscription_id,
            principal=subject,
            name=name,
            arguments=dict(arguments),
            callback_url=url,
            secret=key,
            expires_at=expires_at,
            verified_at=existing.verified_at if already_verified else now,
            previous_secret=previous_secret,
            previous_secret_until=previous_until,
        )
        self.store.upsert(record)
        return record.public_receipt()

    def unsubscribe(self, principal: str, params: Mapping[str, Any]) -> dict[str, Any]:
        subject = _principal(principal)
        if not isinstance(params, Mapping) or set(params) != {"name", "arguments", "delivery"}:
            raise EventContractError("unsubscribe_fields_invalid")
        name = params.get("name")
        arguments = validate_filters(name, params.get("arguments"))
        self._authorized(subject, name, arguments)
        url, _ = _delivery(params, require_secret=False)
        self.store.delete(_identity(subject, name, arguments, url), subject)
        return {}

    def recipients(self, event: Mapping[str, Any]) -> list[Subscription]:
        if not isinstance(event, Mapping):
            return []
        name = event.get("name")
        if not isinstance(name, str):
            return []
        now = self.now()
        accepted: list[Subscription] = []
        for item in self.store.active(name, now):
            if matches_filters(event, item.arguments) and self.authorize(
                item.principal, item.name, item.arguments
            ):
                accepted.append(item)
        return accepted


class PostgresSubscriptionStore:
    """Durable encrypted subscriptions; no secret leaves this store via logs.

    Requires an explicitly supplied 32-byte AES-GCM master key. Instantiation
    initializes a dedicated table; do not enable this on live production before
    reviewing migration and operator authorization.
    """

    _TABLE = "kuuos_mcp_event_subscriptions_v1"

    def __init__(self, database_url: str, encryption_key_b64: str):
        if not isinstance(database_url, str) or not database_url:
            raise EventContractError("postgres_database_url_required")
        try:
            key = base64.b64decode(encryption_key_b64, validate=True)
        except (ValueError, TypeError) as exc:
            raise EventContractError("master_key_encoding_invalid") from exc
        if len(key) != 32:
            raise EventContractError("master_key_must_be_32_bytes")
        try:
            import psycopg
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        except ImportError as exc:
            raise RuntimeError("Postgres/cryptography dependencies not installed") from exc
        self._psycopg = psycopg
        self._aes = AESGCM(key)
        self._url = database_url
        self._ensure_schema()

    def _connect(self):
        return self._psycopg.connect(self._url)

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._TABLE} (
                    id TEXT PRIMARY KEY,
                    principal TEXT NOT NULL,
                    name TEXT NOT NULL,
                    arguments JSONB NOT NULL,
                    callback_url TEXT NOT NULL,
                    secret_blob BYTEA NOT NULL,
                    expires_at TIMESTAMPTZ NOT NULL,
                    verified_at TIMESTAMPTZ NOT NULL,
                    previous_secret_blob BYTEA,
                    previous_secret_until TIMESTAMPTZ
                )
            """)
            # Additive only: an existing subscription table from v0.1 may
            # predate the dual-signature fields.
            conn.execute(
                f"ALTER TABLE {self._TABLE} ADD COLUMN IF NOT EXISTS "
                f"previous_secret_blob BYTEA"
            )
            conn.execute(
                f"ALTER TABLE {self._TABLE} ADD COLUMN IF NOT EXISTS "
                f"previous_secret_until TIMESTAMPTZ"
            )
            conn.execute(f"""
                CREATE INDEX IF NOT EXISTS kuuos_mcp_events_active_v1
                ON {self._TABLE} (name, expires_at)
            """)

    def _seal(self, item: Subscription) -> bytes:
        nonce = secrets.token_bytes(12)
        data = item.secret.encode("utf-8")
        return nonce + self._aes.encrypt(nonce, data, item.id.encode("ascii"))

    def _seal_previous(self, item: Subscription) -> bytes | None:
        if item.previous_secret is None:
            if item.previous_secret_until is not None:
                raise EventContractError("rotation_expiry_without_previous_key")
            return None
        if item.previous_secret_until is None:
            raise EventContractError("previous_key_expiry_missing")
        nonce = secrets.token_bytes(12)
        associated = (item.id + ":previous").encode("ascii")
        return nonce + self._aes.encrypt(
            nonce, item.previous_secret.encode("utf-8"), associated
        )

    def _unseal_previous(self, identity: str, blob: bytes) -> str:
        if len(blob) < 29:
            raise EventContractError("encrypted_previous_secret_invalid")
        try:
            associated = (identity + ":previous").encode("ascii")
            return self._aes.decrypt(
                blob[:12], blob[12:], associated
            ).decode("utf-8")
        except Exception as exc:
            raise EventContractError("encrypted_previous_secret_invalid") from exc

    def _unseal(self, identity: str, blob: bytes) -> str:
        if len(blob) < 29:
            raise EventContractError("encrypted_secret_invalid")
        try:
            secret = self._aes.decrypt(blob[:12], blob[12:], identity.encode("ascii"))
            return secret.decode("utf-8")
        except Exception as exc:
            raise EventContractError("encrypted_secret_invalid") from exc

    def _restore(self, row: tuple[Any, ...]) -> Subscription:
        (identity, principal, name, arguments, url, secret_blob, expires,
         verified, previous_blob, previous_until) = row
        if (previous_blob is None) != (previous_until is None):
            raise EventContractError("previous_key_storage_inconsistent")
        result = Subscription(
            id=identity, principal=principal, name=name, arguments=dict(arguments),
            callback_url=url, secret=self._unseal(identity, bytes(secret_blob)),
            expires_at=expires, verified_at=verified,
            previous_secret=self._unseal_previous(identity, bytes(previous_blob))
                if previous_blob is not None else None,
            previous_secret_until=previous_until,
        )
        if result.id != _identity(result.principal, result.name, result.arguments, result.callback_url):
            raise EventContractError("subscription_identity_mismatch")
        return result

    def get(self, subscription_id: str) -> Subscription | None:
        with self._connect() as conn:
            row = conn.execute(
                f"SELECT id, principal, name, arguments, callback_url, secret_blob, "
                f"expires_at, verified_at, previous_secret_blob, previous_secret_until " 
                f"FROM {self._TABLE} WHERE id = %s",
                (subscription_id,),
            ).fetchone()
        return self._restore(row) if row is not None else None

    def upsert(self, subscription: Subscription) -> None:
        if subscription.id != _identity(
            subscription.principal, subscription.name, subscription.arguments, subscription.callback_url
        ):
            raise EventContractError("subscription_identity_mismatch")
        blob = self._seal(subscription)
        previous_blob = self._seal_previous(subscription)
        with self._connect() as conn:
            from psycopg.types.json import Jsonb
            conn.execute(
                f"INSERT INTO {self._TABLE} (id, principal, name, arguments, "
                f"callback_url, secret_blob, expires_at, verified_at, "
                f"previous_secret_blob, previous_secret_until) "
                f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                f"ON CONFLICT (id) DO UPDATE SET "
                f"secret_blob=EXCLUDED.secret_blob, expires_at=EXCLUDED.expires_at, "
                f"verified_at=EXCLUDED.verified_at, "
                f"previous_secret_blob=EXCLUDED.previous_secret_blob, "
                f"previous_secret_until=EXCLUDED.previous_secret_until",
                (
                    subscription.id, subscription.principal, subscription.name,
                    Jsonb(subscription.arguments), subscription.callback_url,
                    blob, subscription.expires_at, subscription.verified_at,
                    previous_blob, subscription.previous_secret_until,
                ),
            )

    def delete(self, subscription_id: str, principal: str) -> None:
        with self._connect() as conn:
            conn.execute(
                f"DELETE FROM {self._TABLE} WHERE id = %s AND principal = %s",
                (subscription_id, principal),
            )

    def active(self, name: str, now: datetime) -> list[Subscription]:
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT id, principal, name, arguments, callback_url, secret_blob, "
                f"expires_at, verified_at, previous_secret_blob, previous_secret_until "
                f"FROM {self._TABLE} "
                f"WHERE name = %s AND expires_at > %s ORDER BY id LIMIT 512",
                (name, now),
            ).fetchall()
        return [self._restore(row) for row in rows]
