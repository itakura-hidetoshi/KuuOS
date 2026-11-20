"""Durable at-least-once outbox for authenticated KuuOS MCP wake-up delivery.

This is a candidate implementation. It never starts a worker, schedules a
timer or posts a webhook on import. It requires independent authenticated
GitHub ingress, current subscription authorization and callback verification.
An outbox receipt is not a Lean/CI success receipt or Git mutation authority.
"""
from __future__ import annotations

import hashlib
import json
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping, Protocol

from .event_delivery import _packet
from .event_subscriptions import Subscription
from .github_event_contract import EventContractError, matches_filters

MAX_CLAIM_ATTEMPTS = 6
DEFAULT_LEASE_SECONDS = 30
MAX_PACKET_BYTES = 262_144


@dataclass(frozen=True)
class OutboxRecord:
    id: str
    subscription_id: str
    event_id: str
    name: str
    packet: dict[str, Any]
    state: str
    attempts: int
    available_at: datetime
    lease_token: str | None = None
    lease_until: datetime | None = None
    last_http_status: int | None = None

    def public_receipt(self) -> dict[str, Any]:
        return {
            "id": self.id, "subscription_id": self.subscription_id,
            "event_id": self.event_id, "state": self.state,
            "attempts": self.attempts,
            "last_http_status": self.last_http_status,
            "signal_is_success_evidence": False,
            "merge_authority_granted": False,
            "write_authority_granted": False,
        }


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _stamp(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.utcoffset() is None:
        raise ValueError("outbox_timestamp_timezone_required")
    return value.astimezone(timezone.utc)


def _fingerprint(subscription_id: str, event_id: str) -> str:
    if not isinstance(subscription_id, str) or not subscription_id.startswith("sub_"):
        raise EventContractError("outbox_subscription_invalid")
    if not isinstance(event_id, str) or not event_id.startswith("evt_"):
        raise EventContractError("outbox_event_id_invalid")
    raw = json.dumps(
        [subscription_id, event_id], separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    return "out_" + hashlib.sha256(raw).hexdigest()


def _new_record(
    subscription: Subscription, event: Mapping[str, Any], now: datetime,
) -> OutboxRecord:
    now = _stamp(now)
    if subscription.expires_at <= now:
        raise EventContractError("outbox_subscription_expired")
    if subscription.name != event.get("name"):
        raise EventContractError("outbox_event_name_mismatch")
    if not matches_filters(event, subscription.arguments):
        raise EventContractError("outbox_subscription_filter_mismatch")
    raw = _packet(event)
    if len(raw) > MAX_PACKET_BYTES:
        raise EventContractError("outbox_event_too_large")
    envelope = json.loads(raw)
    event_id = envelope["eventId"]
    return OutboxRecord(
        id=_fingerprint(subscription.id, event_id),
        subscription_id=subscription.id, event_id=event_id,
        name=subscription.name, packet=envelope, state="pending",
        attempts=0, available_at=now,
    )


def _valid_lease(lease: int) -> int:
    if type(lease) is not int or not 10 <= lease <= 120:
        raise ValueError("outbox_lease_seconds_invalid")
    return lease


def _next_transition(
    record: OutboxRecord, lease_token: str, status: int | None,
    now: datetime,
) -> OutboxRecord:
    from dataclasses import replace
    if record.state != "leased" or not lease_token or record.lease_token != lease_token:
        raise EventContractError("outbox_lease_mismatch")
    now = _stamp(now)
    if status is not None and (type(status) is not int or not 100 <= status <= 599):
        raise EventContractError("outbox_http_status_invalid")
    if status is not None and 200 <= status < 300:
        disposition = "delivered"
    elif status is not None and 400 <= status < 500:
        disposition = "permanent_failure"
    elif record.attempts >= MAX_CLAIM_ATTEMPTS:
        disposition = "retry_exhausted"
    else:
        disposition = "pending"
    delay = min(2 ** max(0, record.attempts - 1), 60)
    return replace(
        record, state=disposition, lease_token=None, lease_until=None,
        available_at=now + timedelta(seconds=delay),
        last_http_status=status,
    )


class OutboxStore(Protocol):
    def enqueue(self, subscription: Subscription, event: Mapping[str, Any],
                now: datetime) -> OutboxRecord: ...
    def claim(self, now: datetime, lease_seconds: int) -> OutboxRecord | None: ...
    def claim_specific(self, outbox_id: str, now: datetime,
                       lease_seconds: int = DEFAULT_LEASE_SECONDS) -> OutboxRecord | None: ...
    def settle(self, outbox_id: str, lease_token: str, status: int | None,
               now: datetime) -> OutboxRecord: ...
    def cancel(self, outbox_id: str, lease_token: str) -> OutboxRecord: ...


class MemoryOutboxStore:
    """Pure single-process regression fixture, never used for production."""

    def __init__(self) -> None:
        self.records: dict[str, OutboxRecord] = {}

    def enqueue(self, subscription: Subscription, event: Mapping[str, Any],
                now: datetime) -> OutboxRecord:
        record = _new_record(subscription, event, now)
        if record.id not in self.records:
            self.records[record.id] = record
        return self.records[record.id]

    def claim(self, now: datetime, lease_seconds: int = DEFAULT_LEASE_SECONDS) -> OutboxRecord | None:
        from dataclasses import replace
        now = _stamp(now)
        lease_seconds = _valid_lease(lease_seconds)
        for key in sorted(self.records):
            item = self.records[key]
            due = (
                (item.state == "pending" and item.available_at <= now)
                or (item.state == "leased" and item.lease_until is not None
                    and item.lease_until <= now)
            )
            if not due:
                continue
            if item.attempts >= MAX_CLAIM_ATTEMPTS:
                self.records[key] = replace(
                    item, state="retry_exhausted", lease_token=None, lease_until=None
                )
                continue
            updated = replace(
                item, state="leased", attempts=item.attempts + 1,
                lease_token=secrets.token_hex(24),
                lease_until=now + timedelta(seconds=lease_seconds),
            )
            self.records[key] = updated
            return updated
        return None


    def claim_specific(
        self, outbox_id: str, now: datetime,
        lease_seconds: int = DEFAULT_LEASE_SECONDS,
    ) -> OutboxRecord | None:
        """Target the exact new event, not a hash-ordered unrelated backlog."""
        from dataclasses import replace
        now = _stamp(now)
        lease_seconds = _valid_lease(lease_seconds)
        item = self.records.get(outbox_id)
        if item is None:
            return None
        due = (
            (item.state == "pending" and item.available_at <= now)
            or (item.state == "leased" and item.lease_until is not None
                and item.lease_until <= now)
        )
        if not due:
            return None
        if item.attempts >= MAX_CLAIM_ATTEMPTS:
            self.records[outbox_id] = replace(
                item, state="retry_exhausted", lease_token=None,
                lease_until=None,
            )
            return None
        updated = replace(
            item, state="leased", attempts=item.attempts + 1,
            lease_token=secrets.token_hex(24),
            lease_until=now + timedelta(seconds=lease_seconds),
        )
        self.records[outbox_id] = updated
        return updated

    def settle(self, outbox_id: str, lease_token: str, status: int | None,
               now: datetime) -> OutboxRecord:
        record = self.records[outbox_id]
        next_record = _next_transition(record, lease_token, status, now)
        self.records[outbox_id] = next_record
        return next_record

    def cancel(self, outbox_id: str, lease_token: str) -> OutboxRecord:
        from dataclasses import replace
        record = self.records[outbox_id]
        if record.state != "leased" or record.lease_token != lease_token:
            raise EventContractError("outbox_lease_mismatch")
        updated = replace(
            record, state="cancelled", lease_token=None, lease_until=None,
        )
        self.records[outbox_id] = updated
        return updated


class PostgresOutboxStore:
    """Transactional PostgreSQL outbox with skip-locked worker leasing.

    Requires caller-owned PostgreSQL credentials. This class does not create
    a new database, configure credentials or start a background worker.
    """

    _TABLE = "kuuos_mcp_event_outbox_v1"

    def __init__(self, database_url: str):
        if not isinstance(database_url, str) or not database_url:
            raise ValueError("outbox_postgres_dsn_required")
        try:
            import psycopg
            from psycopg.types.json import Jsonb
        except ImportError as exc:
            raise RuntimeError("psycopg package required for outbox") from exc
        self._psycopg = psycopg
        self._Jsonb = Jsonb
        self._url = database_url
        self._ensure_schema()

    def _connect(self):
        return self._psycopg.connect(self._url)

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._TABLE} (
                    id TEXT PRIMARY KEY,
                    subscription_id TEXT NOT NULL,
                    event_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    packet JSONB NOT NULL,
                    state TEXT NOT NULL,
                    attempts INTEGER NOT NULL CHECK (attempts >= 0),
                    available_at TIMESTAMPTZ NOT NULL,
                    lease_token TEXT,
                    lease_until TIMESTAMPTZ,
                    last_http_status INTEGER,
                    UNIQUE(subscription_id, event_id),
                    CHECK (state IN ('pending', 'leased', 'delivered',
                        'permanent_failure', 'retry_exhausted', 'cancelled'))
                )
            """)
            conn.execute(f"""
                CREATE INDEX IF NOT EXISTS kuuos_mcp_outbox_due_v1
                ON {self._TABLE} (state, available_at, lease_until)
            """)

    @staticmethod
    def _restore(row: Any) -> OutboxRecord:
        if row is None:
            raise EventContractError("outbox_record_missing")
        (identity, subscription_id, event_id, name, packet, state,
         attempts, available_at, lease_token, lease_until, last_status) = row
        if _fingerprint(subscription_id, event_id) != identity:
            raise EventContractError("outbox_identity_mismatch")
        return OutboxRecord(
            id=identity, subscription_id=subscription_id, event_id=event_id,
            name=name, packet=dict(packet), state=state, attempts=attempts,
            available_at=available_at, lease_token=lease_token,
            lease_until=lease_until, last_http_status=last_status,
        )

    _SELECT = (
        "id, subscription_id, event_id, name, packet, state, attempts, "
        "available_at, lease_token, lease_until, last_http_status"
    )
    # UPDATE...FROM candidate has a second 'id' column. RETURNING must
    # refer to the target alias explicitly; the unqualified SELECT list
    # above is valid only when no candidate table is in scope.
    _RETURNING = (
        "work.id, work.subscription_id, work.event_id, work.name, "
        "work.packet, work.state, work.attempts, work.available_at, "
        "work.lease_token, work.lease_until, work.last_http_status"
    )

    def enqueue(self, subscription: Subscription, event: Mapping[str, Any],
                now: datetime) -> OutboxRecord:
        record = _new_record(subscription, event, now)
        with self._connect() as conn:
            conn.execute(
                f"INSERT INTO {self._TABLE} (id, subscription_id, event_id, name, "
                f"packet, state, attempts, available_at) VALUES "
                f"(%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING",
                (record.id, record.subscription_id, record.event_id,
                 record.name, self._Jsonb(record.packet), record.state,
                 record.attempts, record.available_at),
            )
            row = conn.execute(
                f"SELECT {self._SELECT} FROM {self._TABLE} WHERE id = %s",
                (record.id,),
            ).fetchone()
        return self._restore(row)

    def claim(self, now: datetime, lease_seconds: int = DEFAULT_LEASE_SECONDS) -> OutboxRecord | None:
        now = _stamp(now)
        lease_seconds = _valid_lease(lease_seconds)
        token = secrets.token_hex(24)
        lease_until = now + timedelta(seconds=lease_seconds)
        with self._connect() as conn:
            # Exhausted expired leases cannot block newer deliveries.
            conn.execute(
                f"UPDATE {self._TABLE} SET state = 'retry_exhausted', "
                f"lease_token = NULL, lease_until = NULL "
                f"WHERE state = 'leased' AND lease_until <= %s "
                f"AND attempts >= %s",
                (now, MAX_CLAIM_ATTEMPTS),
            )
            row = conn.execute(
                f"WITH candidate AS ("
                f"SELECT id FROM {self._TABLE} WHERE "
                f"((state='pending' AND available_at <= %s) OR "
                f"(state='leased' AND lease_until <= %s)) "
                f"AND attempts < %s ORDER BY available_at, id "
                f"FOR UPDATE SKIP LOCKED LIMIT 1) "
                f"UPDATE {self._TABLE} AS work "
                f"SET state='leased', attempts=work.attempts+1, "
                f"lease_token=%s, lease_until=%s "
                f"FROM candidate WHERE work.id=candidate.id "
                f"RETURNING {self._RETURNING}",
                (now, now, MAX_CLAIM_ATTEMPTS, token, lease_until),
            ).fetchone()
        return self._restore(row) if row is not None else None


    def claim_specific(
        self, outbox_id: str, now: datetime,
        lease_seconds: int = DEFAULT_LEASE_SECONDS,
    ) -> OutboxRecord | None:
        """CAS claim one known pending event; concurrent workers use SKIP LOCKED.

        The caller may not claim an unrelated event when an explicitly
        requested event is already delivered, leased, or not yet due.
        """
        if not isinstance(outbox_id, str) or not outbox_id.startswith("out_"):
            raise EventContractError("outbox_identity_invalid")
        now = _stamp(now)
        lease_seconds = _valid_lease(lease_seconds)
        token = secrets.token_hex(24)
        lease_until = now + timedelta(seconds=lease_seconds)
        with self._connect() as conn:
            conn.execute(
                f"UPDATE {self._TABLE} SET state='retry_exhausted', "
                f"lease_token=NULL, lease_until=NULL "
                f"WHERE id=%s AND state='leased' AND lease_until <= %s "
                f"AND attempts >= %s",
                (outbox_id, now, MAX_CLAIM_ATTEMPTS),
            )
            row = conn.execute(
                f"WITH candidate AS ("
                f"SELECT id FROM {self._TABLE} "
                f"WHERE id=%s AND attempts < %s AND "
                f"((state='pending' AND available_at <= %s) OR "
                f"(state='leased' AND lease_until <= %s)) "
                f"FOR UPDATE SKIP LOCKED LIMIT 1) "
                f"UPDATE {self._TABLE} AS work "
                f"SET state='leased', attempts=work.attempts+1, "
                f"lease_token=%s, lease_until=%s "
                f"FROM candidate WHERE work.id=candidate.id "
                f"RETURNING {self._RETURNING}",
                (outbox_id, MAX_CLAIM_ATTEMPTS, now, now, token, lease_until),
            ).fetchone()
        return self._restore(row) if row is not None else None

    def settle(self, outbox_id: str, lease_token: str, status: int | None,
               now: datetime) -> OutboxRecord:
        now = _stamp(now)
        with self._connect() as conn:
            row = conn.execute(
                f"SELECT {self._SELECT} FROM {self._TABLE} "
                f"WHERE id=%s FOR UPDATE",
                (outbox_id,),
            ).fetchone()
            if row is None:
                raise EventContractError("outbox_record_missing")
            updated = _next_transition(self._restore(row), lease_token, status, now)
            result = conn.execute(
                f"UPDATE {self._TABLE} SET state=%s, lease_token=NULL, "
                f"lease_until=NULL, available_at=%s, last_http_status=%s "
                f"WHERE id=%s AND state='leased' AND lease_token=%s",
                (updated.state, updated.available_at, updated.last_http_status,
                 outbox_id, lease_token),
            )
            if result.rowcount != 1:
                raise EventContractError("outbox_lease_lost")
        return updated

    def cancel(self, outbox_id: str, lease_token: str) -> OutboxRecord:
        from dataclasses import replace
        with self._connect() as conn:
            row = conn.execute(
                f"SELECT {self._SELECT} FROM {self._TABLE} "
                f"WHERE id=%s FOR UPDATE",
                (outbox_id,),
            ).fetchone()
            if row is None:
                raise EventContractError("outbox_record_missing")
            current = self._restore(row)
            if current.state != "leased" or current.lease_token != lease_token:
                raise EventContractError("outbox_lease_mismatch")
            result = conn.execute(
                f"UPDATE {self._TABLE} SET state='cancelled', "
                f"lease_token=NULL, lease_until=NULL "
                f"WHERE id=%s AND state='leased' AND lease_token=%s",
                (outbox_id, lease_token),
            )
            if result.rowcount != 1:
                raise EventContractError("outbox_lease_lost")
        return replace(current, state="cancelled", lease_token=None, lease_until=None)
