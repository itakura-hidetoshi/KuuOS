from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any, Mapping

from .identity import digest_json


GENESIS_DIGEST = "0" * 64


class LedgerIntegrityError(ValueError):
    pass


class StaleLedgerHeadError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class LedgerEvent:
    sequence: int
    event_id: str
    kind: str
    payload: dict[str, Any]
    predecessor_digest: str
    event_digest: str

    @classmethod
    def build(
        cls,
        *,
        sequence: int,
        event_id: str,
        kind: str,
        payload: Mapping[str, Any],
        predecessor_digest: str,
    ) -> "LedgerEvent":
        body = {
            "sequence": sequence,
            "event_id": event_id,
            "kind": kind,
            "payload": dict(payload),
            "predecessor_digest": predecessor_digest,
        }
        return cls(event_digest=digest_json(body), **body)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "LedgerEvent":
        try:
            event = cls(
                sequence=int(value["sequence"]),
                event_id=str(value["event_id"]),
                kind=str(value["kind"]),
                payload=dict(value["payload"]),
                predecessor_digest=str(value["predecessor_digest"]),
                event_digest=str(value["event_digest"]),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise LedgerIntegrityError("ledger_event_shape_invalid") from error
        expected = cls.build(
            sequence=event.sequence,
            event_id=event.event_id,
            kind=event.kind,
            payload=event.payload,
            predecessor_digest=event.predecessor_digest,
        )
        if expected.event_digest != event.event_digest:
            raise LedgerIntegrityError("ledger_event_digest_mismatch")
        return event

    def to_mapping(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "event_id": self.event_id,
            "kind": self.kind,
            "payload": self.payload,
            "predecessor_digest": self.predecessor_digest,
            "event_digest": self.event_digest,
        }


@dataclass(frozen=True, slots=True)
class AppendResult:
    event: LedgerEvent
    replayed: bool


class AppendOnlyLedger:
    """Small JSONL event ledger with hash chaining and replay protection.

    The ledger is deliberately non-authoritative outside its own event history.
    It records evidence and state transitions but grants no execution authority.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def read(self) -> list[LedgerEvent]:
        if not self.path.exists():
            return []
        events: list[LedgerEvent] = []
        predecessor = GENESIS_DIGEST
        seen_ids: set[str] = set()
        with self.path.open("r", encoding="utf-8") as handle:
            for line_number, raw in enumerate(handle, start=1):
                if not raw.strip():
                    continue
                try:
                    value = json.loads(raw)
                except json.JSONDecodeError as error:
                    raise LedgerIntegrityError(
                        f"ledger_json_invalid_at_line:{line_number}"
                    ) from error
                if not isinstance(value, Mapping):
                    raise LedgerIntegrityError(
                        f"ledger_event_not_mapping_at_line:{line_number}"
                    )
                event = LedgerEvent.from_mapping(value)
                if event.sequence != len(events) + 1:
                    raise LedgerIntegrityError(
                        f"ledger_sequence_invalid_at_line:{line_number}"
                    )
                if event.predecessor_digest != predecessor:
                    raise LedgerIntegrityError(
                        f"ledger_predecessor_invalid_at_line:{line_number}"
                    )
                if event.event_id in seen_ids:
                    raise LedgerIntegrityError(
                        f"ledger_duplicate_event_id_at_line:{line_number}"
                    )
                events.append(event)
                seen_ids.add(event.event_id)
                predecessor = event.event_digest
        return events

    @property
    def head_digest(self) -> str:
        events = self.read()
        return events[-1].event_digest if events else GENESIS_DIGEST

    def append(
        self,
        *,
        event_id: str,
        kind: str,
        payload: Mapping[str, Any],
        expected_head_digest: str | None = None,
    ) -> AppendResult:
        if not event_id.strip():
            raise ValueError("event_id_missing")
        if not kind.strip():
            raise ValueError("event_kind_missing")
        events = self.read()
        head = events[-1].event_digest if events else GENESIS_DIGEST
        for existing in events:
            if existing.event_id != event_id:
                continue
            candidate = LedgerEvent.build(
                sequence=existing.sequence,
                event_id=event_id,
                kind=kind,
                payload=payload,
                predecessor_digest=existing.predecessor_digest,
            )
            if candidate.event_digest != existing.event_digest:
                raise LedgerIntegrityError("event_id_reused_with_different_content")
            return AppendResult(event=existing, replayed=True)
        if expected_head_digest is not None and expected_head_digest != head:
            raise StaleLedgerHeadError("stale_ledger_head")
        event = LedgerEvent.build(
            sequence=len(events) + 1,
            event_id=event_id,
            kind=kind,
            payload=payload,
            predecessor_digest=head,
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        encoded = json.dumps(
            event.to_mapping(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(encoded + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return AppendResult(event=event, replayed=False)
