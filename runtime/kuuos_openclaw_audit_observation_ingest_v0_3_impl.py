#!/usr/bin/env python3
"""OpenClaw audit.activity.list -> KuuOS ObserveOS/MemoryOS intake v0.3.

This adapter ingests OpenClaw's metadata-only, best-effort audit activity ledger
as append-only KuuOS observation *candidates*.  It never promotes an audit row
to an ObserveOS commit, verification result, WORLD truth, PlanOS completion, or
rollback proof.

The OpenClaw Gateway remains the source of the audit metadata.  KuuOS stores a
strict allowlisted projection plus a source-event digest and keeps an explicit
per-query pagination checkpoint so bounded polls can resume without treating a
partial page window as complete history.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

VERSION = "kuuos_openclaw_audit_observation_ingest_v0_3"
SOURCE = "openclaw.gateway.audit.activity"
DEFAULT_DATA_DIR = "~/.kuuos/openclaw"

EVENT_TYPES = {"agent_run", "tool_action", "inbound_message", "outbound_message"}
QUERY_KINDS = {"agent_run", "tool_action", "message"}
STATUSES = {"started", "succeeded", "failed", "cancelled", "timed_out", "blocked", "unknown"}
DIRECTIONS = {"inbound", "outbound"}

BASE_FIELDS = (
    "eventType",
    "schemaVersion",
    "eventId",
    "sequence",
    "sourceSequence",
    "occurredAt",
    "kind",
    "action",
    "status",
    "redaction",
)
SAFE_OPTIONAL_FIELDS = (
    "agentId",
    "runId",
    "toolCallId",
    "toolName",
    "errorCode",
    "direction",
    "channel",
    "conversationKind",
    "outcome",
    "deliveryKind",
    "failureStage",
    "durationMs",
    "resultCount",
    "reasonCode",
)


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def require_int(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise RuntimeError(f"OpenClaw audit event field {name!r} must be an integer")
    return value


def require_nonempty_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise RuntimeError(f"OpenClaw audit event field {name!r} must be a non-empty string")
    return value


def validate_event(event: Any) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise RuntimeError("OpenClaw audit.activity.list returned a non-object event")

    schema_version = require_int(event.get("schemaVersion"), "schemaVersion")
    if schema_version != 1:
        raise RuntimeError(f"unsupported OpenClaw audit schemaVersion: {schema_version!r}")

    event_type = require_nonempty_string(event.get("eventType"), "eventType")
    if event_type not in EVENT_TYPES:
        raise RuntimeError(f"unsupported OpenClaw audit eventType: {event_type!r}")

    event_id = require_nonempty_string(event.get("eventId"), "eventId")
    sequence = require_int(event.get("sequence"), "sequence")
    if sequence < 0:
        raise RuntimeError("OpenClaw audit event sequence must be non-negative")

    require_int(event.get("sourceSequence"), "sourceSequence")
    require_int(event.get("occurredAt"), "occurredAt")
    require_nonempty_string(event.get("kind"), "kind")
    require_nonempty_string(event.get("action"), "action")
    status = require_nonempty_string(event.get("status"), "status")
    if status not in STATUSES:
        raise RuntimeError(f"unsupported OpenClaw audit status: {status!r}")

    redaction = require_nonempty_string(event.get("redaction"), "redaction")
    if redaction != "metadata_only":
        raise RuntimeError(
            "OpenClaw audit event is not explicitly metadata_only; refusing to persist an unknown payload shape"
        )
    if "actor" not in event:
        raise RuntimeError("OpenClaw audit event is missing required actor metadata")

    if event_type == "agent_run":
        require_nonempty_string(event.get("agentId"), "agentId")
        require_nonempty_string(event.get("runId"), "runId")
    elif event_type == "tool_action":
        require_nonempty_string(event.get("agentId"), "agentId")
        require_nonempty_string(event.get("runId"), "runId")
    elif event_type == "inbound_message" and event.get("direction") not in (None, "inbound"):
        raise RuntimeError("inbound_message event has a contradictory direction")
    elif event_type == "outbound_message" and event.get("direction") not in (None, "outbound"):
        raise RuntimeError("outbound_message event has a contradictory direction")

    _ = event_id
    return event


def project_event(event: dict[str, Any]) -> dict[str, Any]:
    """Project only documented metadata fields and hash privacy-sensitive identity context."""
    validate_event(event)
    projected: dict[str, Any] = {}
    for key in BASE_FIELDS + SAFE_OPTIONAL_FIELDS:
        if key in event:
            projected[key] = event[key]

    projected["actorDigest"] = digest(event["actor"])

    if "sessionKey" in event and event["sessionKey"] is not None:
        projected["sessionKeyDigest"] = digest(event["sessionKey"])
    if "sessionId" in event and event["sessionId"] is not None:
        projected["sessionIdDigest"] = digest(event["sessionId"])

    projected["sourceEventDigest"] = digest(event)
    return projected


class ObservationLedger:
    def __init__(self, data_dir: Path) -> None:
        data_dir.mkdir(parents=True, exist_ok=True)
        self.path = data_dir / "audit-observation-candidates.jsonl"

    def seen_event_ids(self) -> set[str]:
        seen: set[str] = set()
        if not self.path.exists():
            return seen
        with self.path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as error:
                    raise RuntimeError(
                        f"corrupt KuuOS audit observation ledger at line {line_number}: {error}"
                    ) from error
                event = record.get("event") if isinstance(record, dict) else None
                event_id = event.get("eventId") if isinstance(event, dict) else None
                if not isinstance(event_id, str) or not event_id:
                    raise RuntimeError(
                        f"invalid KuuOS audit observation ledger record at line {line_number}"
                    )
                seen.add(event_id)
        return seen

    def append_candidate(self, event: dict[str, Any], query_digest: str) -> dict[str, Any]:
        projected = project_event(event)
        now_ns = time.time_ns()
        record: dict[str, Any] = {
            "version": VERSION,
            "recordType": "openclaw_audit_observation_candidate",
            "source": SOURCE,
            "ingestedAtUnixNs": now_ns,
            "queryDigest": query_digest,
            "event": projected,
            "semantics": {
                "metadataOnly": True,
                "bestEffortSource": True,
                "observeOwnerReviewRequired": True,
                "observeCommitPerformed": False,
                "verificationRequired": True,
                "verificationCreated": False,
                "worldCommitAuthority": False,
                "truthPromotionAuthority": False,
                "planCompletionAuthority": False,
                "automaticPlanCompletion": False,
                "rollbackProofAuthority": False,
                "automaticRollback": False,
                "absenceProvesNonOccurrence": False,
                "memoryOverwriteAuthority": False,
            },
        }
        record["recordDigest"] = digest(record)
        record["recordId"] = f"kuuos-oc-audit-{now_ns}-{record['recordDigest'][:16]}"
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return record


class CheckpointStore:
    def __init__(self, data_dir: Path) -> None:
        data_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir = data_dir
        self.path = data_dir / "audit-ingest-checkpoints.json"

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"version": VERSION, "queries": {}}
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise RuntimeError(f"corrupt KuuOS audit checkpoint file: {error}") from error
        if not isinstance(value, dict) or not isinstance(value.get("queries"), dict):
            raise RuntimeError("invalid KuuOS audit checkpoint file")
        if value.get("version") != VERSION:
            raise RuntimeError(
                f"unsupported KuuOS audit checkpoint version: {value.get('version')!r}"
            )
        return value

    def save(self, value: dict[str, Any]) -> None:
        value = dict(value)
        value["version"] = VERSION
        tmp = self.path.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, self.path)
        try:
            directory_fd = os.open(self.data_dir, os.O_RDONLY)
        except OSError:
            return
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)


def gateway_call(args: argparse.Namespace, params: dict[str, Any]) -> dict[str, Any]:
    command = [
        args.openclaw_bin,
        "gateway",
        "call",
        "audit.activity.list",
        "--params",
        json.dumps(params, ensure_ascii=False, separators=(",", ":")),
        "--timeout",
        str(args.rpc_timeout_ms),
        "--json",
        "--no-color",
    ]
    if args.port is not None:
        command.extend(["--port", str(args.port)])

    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=max(5.0, args.rpc_timeout_ms / 1000 + 10.0),
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(f"OpenClaw Gateway RPC audit.activity.list failed: {detail}")
    raw = completed.stdout.strip()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"OpenClaw Gateway RPC audit.activity.list returned non-JSON output: {raw[:500]}"
        ) from error
    if not isinstance(value, dict):
        raise RuntimeError("OpenClaw Gateway RPC audit.activity.list returned a non-object payload")
    events = value.get("events")
    if not isinstance(events, list):
        raise RuntimeError("OpenClaw audit.activity.list response is missing an events array")
    next_cursor = value.get("nextCursor")
    if next_cursor is not None and not isinstance(next_cursor, str):
        raise RuntimeError("OpenClaw audit.activity.list nextCursor is not a string")
    return value


def build_filters(args: argparse.Namespace) -> dict[str, Any]:
    filters: dict[str, Any] = {}
    mapping = (
        ("agent_id", "agentId"),
        ("session_key", "sessionKey"),
        ("run_id", "runId"),
        ("kind", "kind"),
        ("status", "status"),
        ("direction", "direction"),
        ("channel", "channel"),
        ("after_ms", "after"),
        ("before_ms", "before"),
    )
    for attribute, key in mapping:
        value = getattr(args, attribute, None)
        if value is not None:
            filters[key] = value

    if args.direction is not None and args.kind not in (None, "message"):
        raise RuntimeError("--direction requires --kind message or no --kind filter")
    if args.channel is not None and args.kind not in (None, "message"):
        raise RuntimeError("--channel requires --kind message or no --kind filter")
    if args.after_ms is not None and args.before_ms is not None and args.after_ms > args.before_ms:
        raise RuntimeError("--after-ms must be <= --before-ms")
    return filters


def query_digest(filters: dict[str, Any]) -> str:
    return digest({"method": "audit.activity.list", "filters": filters})


def _entry_for(state: dict[str, Any], qdigest: str) -> dict[str, Any]:
    queries = state.setdefault("queries", {})
    entry = queries.setdefault(
        qdigest,
        {
            "maxSequence": 0,
            "resumeCursor": None,
            "catchupHighWaterSequence": None,
            "lastCompletedAtUnixNs": None,
        },
    )
    if not isinstance(entry, dict):
        raise RuntimeError("invalid per-query KuuOS audit checkpoint")
    max_sequence = entry.get("maxSequence", 0)
    if not isinstance(max_sequence, int) or isinstance(max_sequence, bool) or max_sequence < 0:
        raise RuntimeError("invalid maxSequence in KuuOS audit checkpoint")
    cursor = entry.get("resumeCursor")
    if cursor is not None and not isinstance(cursor, str):
        raise RuntimeError("invalid resumeCursor in KuuOS audit checkpoint")
    high_water = entry.get("catchupHighWaterSequence")
    if high_water is not None and (
        not isinstance(high_water, int) or isinstance(high_water, bool) or high_water < max_sequence
    ):
        raise RuntimeError("invalid catchupHighWaterSequence in KuuOS audit checkpoint")
    return entry


def sync(args: argparse.Namespace, ledger: ObservationLedger, checkpoints: CheckpointStore) -> dict[str, Any]:
    filters = build_filters(args)
    qdigest = query_digest(filters)
    state = checkpoints.load()
    entry = _entry_for(state, qdigest)

    if args.restart_catchup:
        entry["resumeCursor"] = None
        entry["catchupHighWaterSequence"] = None

    old_max = int(entry.get("maxSequence", 0))
    cursor = entry.get("resumeCursor")
    high_water = entry.get("catchupHighWaterSequence")
    seen = ledger.seen_event_ids()

    inserted = 0
    duplicates = 0
    fetched = 0
    pages = 0
    reached_checkpoint = False
    exhausted = False
    previous_page_min: int | None = None
    last_cursor: str | None = cursor

    while pages < args.max_pages:
        params = dict(filters)
        params["limit"] = args.limit
        if cursor is not None:
            params["cursor"] = cursor

        result = gateway_call(args, params)
        pages += 1
        raw_events = result["events"]
        events = [validate_event(event) for event in raw_events]
        fetched += len(events)

        sequences = [int(event["sequence"]) for event in events]
        if sequences != sorted(sequences, reverse=True):
            raise RuntimeError(
                "OpenClaw audit page is not newest-first by monotonic sequence; refusing checkpoint advancement"
            )
        if previous_page_min is not None and sequences and sequences[0] > previous_page_min:
            raise RuntimeError(
                "OpenClaw audit pagination sequence order regressed across pages; refusing checkpoint advancement"
            )
        if sequences:
            previous_page_min = sequences[-1]
            page_high = sequences[0]
            if high_water is None:
                high_water = page_high
            else:
                high_water = max(int(high_water), page_high)

        for event in events:
            sequence = int(event["sequence"])
            if sequence <= old_max:
                reached_checkpoint = True
                continue
            event_id = str(event["eventId"])
            if event_id in seen:
                duplicates += 1
                continue
            ledger.append_candidate(event, qdigest)
            seen.add(event_id)
            inserted += 1

        next_cursor = result.get("nextCursor")
        if reached_checkpoint or next_cursor is None:
            exhausted = next_cursor is None
            cursor = None
            last_cursor = None
            break

        cursor = next_cursor
        last_cursor = cursor

    completed_window = reached_checkpoint or exhausted
    if completed_window:
        if high_water is not None:
            entry["maxSequence"] = max(old_max, int(high_water))
        entry["resumeCursor"] = None
        entry["catchupHighWaterSequence"] = None
        entry["lastCompletedAtUnixNs"] = time.time_ns()
    else:
        entry["resumeCursor"] = last_cursor
        entry["catchupHighWaterSequence"] = high_water

    checkpoints.save(state)
    return {
        "version": VERSION,
        "source": SOURCE,
        "queryDigest": qdigest,
        "fetched": fetched,
        "inserted": inserted,
        "duplicates": duplicates,
        "pages": pages,
        "oldMaxSequence": old_max,
        "newMaxSequence": entry.get("maxSequence", old_max),
        "completedWindow": completed_window,
        "reachedPreviousCheckpoint": reached_checkpoint,
        "sourceExhausted": exhausted,
        "resumeRequired": not completed_window,
        "resumeCursorStored": bool(entry.get("resumeCursor")),
        "semantics": {
            "metadataOnly": True,
            "bestEffortSource": True,
            "absenceProvesNonOccurrence": False,
            "observeCommitPerformed": False,
            "verificationRequired": True,
            "verificationCreated": False,
            "worldCommitAuthority": False,
            "truthPromotionAuthority": False,
            "automaticPlanCompletion": False,
            "automaticRollback": False,
        },
    }


def status(args: argparse.Namespace, ledger: ObservationLedger, checkpoints: CheckpointStore) -> dict[str, Any]:
    state = checkpoints.load()
    seen = ledger.seen_event_ids()
    queries = state.get("queries", {})
    pending = 0
    for entry in queries.values():
        if isinstance(entry, dict) and entry.get("resumeCursor"):
            pending += 1
    return {
        "version": VERSION,
        "source": SOURCE,
        "ledgerPath": str(ledger.path),
        "checkpointPath": str(checkpoints.path),
        "candidateCount": len(seen),
        "queryCheckpointCount": len(queries),
        "pendingCatchups": pending,
        "worldCommitAuthority": False,
        "truthPromotionAuthority": False,
        "automaticPlanCompletion": False,
        "automaticRollback": False,
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Ingest OpenClaw metadata-only audit activity as KuuOS observation candidates."
    )
    root.add_argument("--openclaw-bin", default=os.environ.get("OPENCLAW_BIN", "openclaw"))
    root.add_argument("--port", type=int, default=None, help="Local Gateway port; omit to use OpenClaw config.")
    root.add_argument("--data-dir", default=os.environ.get("KUUOS_OPENCLAW_DATA_DIR", DEFAULT_DATA_DIR))
    root.add_argument("--rpc-timeout-ms", type=int, default=30000)

    sub = root.add_subparsers(dest="command", required=True)

    sync_parser = sub.add_parser("sync", help="Pull bounded audit pages into the append-only candidate ledger.")
    sync_parser.add_argument("--agent-id")
    sync_parser.add_argument("--session-key")
    sync_parser.add_argument("--run-id")
    sync_parser.add_argument("--kind", choices=sorted(QUERY_KINDS))
    sync_parser.add_argument("--status", choices=sorted(STATUSES))
    sync_parser.add_argument("--direction", choices=sorted(DIRECTIONS))
    sync_parser.add_argument("--channel")
    sync_parser.add_argument("--after-ms", type=int)
    sync_parser.add_argument("--before-ms", type=int)
    sync_parser.add_argument("--limit", type=int, default=500)
    sync_parser.add_argument("--max-pages", type=int, default=20)
    sync_parser.add_argument(
        "--restart-catchup",
        action="store_true",
        help="Discard only the stored pagination cursor for this exact filter set and restart from newest.",
    )

    sub.add_parser("status", help="Show local intake ledger/checkpoint status without contacting OpenClaw.")
    return root


def validate_args(args: argparse.Namespace) -> None:
    if args.rpc_timeout_ms <= 0:
        raise RuntimeError("--rpc-timeout-ms must be positive")
    if args.command == "sync":
        if not 1 <= args.limit <= 500:
            raise RuntimeError("--limit must be between 1 and 500")
        if not 1 <= args.max_pages <= 200:
            raise RuntimeError("--max-pages must be between 1 and 200")


def main() -> int:
    args = parser().parse_args()
    data_dir = Path(args.data_dir).expanduser()
    ledger = ObservationLedger(data_dir)
    checkpoints = CheckpointStore(data_dir)
    try:
        validate_args(args)
        if args.command == "sync":
            result = sync(args, ledger, checkpoints)
        elif args.command == "status":
            result = status(args, ledger, checkpoints)
        else:
            raise RuntimeError(f"unknown command {args.command!r}")
    except (RuntimeError, subprocess.TimeoutExpired, OSError) as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
