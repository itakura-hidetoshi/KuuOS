#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


@dataclass(frozen=True)
class QiLocalFlowResult:
    flow_version: str
    flow_status: str
    flow_packet_id: str
    runtime_root: str
    queue_path: str
    applied_path: str
    state_path: str
    applied_count: int
    replay_count: int
    state_digest_before: str
    state_digest_after: str
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]
    local_state_written: bool
    local_log_appended: bool
    authority: str = "qi_local_flow_v0_3"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def build_qi_local_flow(*, runtime_context: Mapping[str, Any], flow_license_packet: Mapping[str, Any]) -> QiLocalFlowResult:
    ctx = _mapping(runtime_context)
    lic = _mapping(flow_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    runtime_root = _root(ctx.get("runtime_root"), blockers)
    queue_path = runtime_root / "queue.jsonl"
    applied_path = runtime_root / "applied.jsonl"
    state_path = runtime_root / "state.json"

    if ctx.get("qi_local_flow_enabled") is not True:
        blockers.append("qi_local_flow_enabled_not_true")
    if ctx.get("apply_local_flow") is not True:
        blockers.append("apply_local_flow_not_true")
    if lic.get("license_status") != "QI_LOCAL_FLOW_LICENSE_READY":
        blockers.append("flow_license_not_ready")
    if lic.get("queue_read_allowed") is not True:
        blockers.append("queue_read_not_allowed")
    if lic.get("state_write_allowed") is not True:
        blockers.append("state_write_not_allowed")
    if lic.get("applied_log_append_allowed") is not True:
        blockers.append("applied_log_append_not_allowed")

    max_rows = ctx.get("max_rows", 100)
    if isinstance(max_rows, bool):
        max_rows = 100
    try:
        max_rows = int(max_rows)
    except (TypeError, ValueError):
        max_rows = 100
    if max_rows < 1:
        blockers.append("max_rows_invalid")

    state_before = _read_json(state_path)
    state_before_digest = _sha(state_before)
    queue_rows = _read_jsonl(queue_path)[:max_rows]
    applied_rows = _read_jsonl(applied_path)
    seen = {str(row.get("flow_key")) for row in applied_rows if row.get("flow_key")}

    ready = not blockers
    records: list[dict[str, Any]] = []
    replay_count = 0
    state_after = dict(state_before)
    state_after.setdefault("applied_total", 0)
    state_after.setdefault("last_items", [])

    if ready:
        for row in queue_rows:
            source_key = str(row.get("idempotency_key") or row.get("item_id") or _sha(row))
            flow_key = _sha({"source_key": source_key, "row": row})
            if flow_key in seen:
                replay_count += 1
                continue
            record = {
                "flow_key": flow_key,
                "source_key": source_key,
                "item_digest": _sha(row),
                "item_kind": row.get("item_kind", row.get("action", "local_item")),
                "status": "applied_local",
                "applied_at_epoch": int(time.time()),
            }
            record["record_digest"] = _sha(record)
            _append_jsonl(applied_path, record)
            records.append(record)
            seen.add(flow_key)
            state_after["applied_total"] = int(state_after.get("applied_total", 0)) + 1
            state_after["last_items"] = (list(state_after.get("last_items", [])) + [record["source_key"]])[-20:]
        if records:
            state_after["last_flow_packet_epoch"] = int(time.time())
            _write_json(state_path, state_after)
    elif queue_rows:
        warnings.append("queue_rows_present_but_flow_blocked")

    state_after_digest = _sha(_read_json(state_path) if ready and records else state_after)
    core = {
        "runtime_root": str(runtime_root),
        "queue_path": str(queue_path),
        "applied_count": len(records),
        "replay_count": replay_count,
        "state_after_digest": state_after_digest,
    }
    packet_id = "qi-local-flow-" + _sha(core)[:16]
    if blockers:
        status = "QI_LOCAL_FLOW_BLOCKED"
    elif not queue_rows:
        status = "QI_LOCAL_FLOW_IDLE"
    elif not records and replay_count:
        status = "QI_LOCAL_FLOW_REPLAYED"
    else:
        status = "QI_LOCAL_FLOW_APPLIED"

    return QiLocalFlowResult(
        flow_version="kuuos_runtime_daemon_qi_local_flow_v0_3",
        flow_status=status,
        flow_packet_id=packet_id,
        runtime_root=str(runtime_root),
        queue_path=str(queue_path),
        applied_path=str(applied_path),
        state_path=str(state_path),
        applied_count=len(records),
        replay_count=replay_count,
        state_digest_before=state_before_digest,
        state_digest_after=state_after_digest,
        records=records,
        blockers=blockers,
        warnings=warnings,
        local_state_written=bool(records),
        local_log_appended=bool(records),
    )
