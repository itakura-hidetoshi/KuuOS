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
class QiPTReadyFlowResult:
    ready_flow_version: str
    ready_flow_status: str
    ready_flow_packet_id: str
    runtime_root: str
    ready_queue_path: str
    applied_path: str
    state_path: str
    feedback_path: str
    applied_count: int
    replay_count: int
    state_digest_before: str
    state_digest_after: str
    feedback_count: int
    records: list[dict[str, Any]]
    feedback_records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]
    local_state_written: bool
    local_log_appended: bool
    feedback_appended: bool
    authority: str = "qi_pt_ready_flow_v0_5"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


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


def _seen(path: pathlib.Path) -> set[str]:
    rows = _read_jsonl(path)
    keys: set[str] = set()
    for row in rows:
        key = row.get("ready_flow_key") or row.get("source_key")
        if key:
            keys.add(str(key))
    return keys


def _source_key(row: Mapping[str, Any]) -> str:
    return str(row.get("policy_key") or row.get("idempotency_key") or row.get("item_id") or _sha(dict(row)))


def _ordered(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda row: (-_float(row.get("policy_score"), 0.0), str(_source_key(row))))


def build_qi_pt_ready_flow(
    *,
    runtime_context: Mapping[str, Any],
    ready_flow_license_packet: Mapping[str, Any],
) -> QiPTReadyFlowResult:
    ctx = _mapping(runtime_context)
    lic = _mapping(ready_flow_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    ready_queue_path = root / "queue.ready.jsonl"
    applied_path = root / "applied.jsonl"
    state_path = root / "state.json"
    feedback_path = root / "pt_feedback.jsonl"

    if ctx.get("qi_pt_ready_flow_enabled") is not True:
        blockers.append("qi_pt_ready_flow_enabled_not_true")
    if ctx.get("apply_ready_flow") is not True:
        blockers.append("apply_ready_flow_not_true")
    if lic.get("license_status") != "QI_PT_READY_FLOW_LICENSE_READY":
        blockers.append("ready_flow_license_not_ready")
    if lic.get("ready_queue_read_allowed") is not True:
        blockers.append("ready_queue_read_not_allowed")
    if lic.get("state_write_allowed") is not True:
        blockers.append("state_write_not_allowed")
    if lic.get("applied_log_append_allowed") is not True:
        blockers.append("applied_log_append_not_allowed")
    if lic.get("feedback_append_allowed") is not True:
        blockers.append("feedback_append_not_allowed")

    max_apply = _int(ctx.get("max_apply"), 100)
    if max_apply < 1:
        blockers.append("max_apply_invalid")
        max_apply = 1

    rows = _ordered(_read_jsonl(ready_queue_path))[:max_apply]
    applied_seen = _seen(applied_path)
    feedback_seen = _seen(feedback_path)
    state_before = _read_json(state_path)
    state_digest_before = _sha(state_before)
    state_after = dict(state_before)
    state_after.setdefault("applied_total", 0)
    state_after.setdefault("pt_ready_applied_total", 0)
    state_after.setdefault("last_items", [])

    ready = not blockers
    records: list[dict[str, Any]] = []
    feedback_records: list[dict[str, Any]] = []
    replay_count = 0

    if ready:
        for row in rows:
            source_key = _source_key(row)
            ready_flow_key = _sha({"source_key": source_key, "row_digest": _sha(row)})
            if ready_flow_key in applied_seen or ready_flow_key in feedback_seen:
                replay_count += 1
                continue
            record = {
                "ready_flow_key": ready_flow_key,
                "source_key": source_key,
                "item_digest": _sha(row),
                "item_kind": row.get("item_kind", row.get("action", "local_item")),
                "policy_score": _float(row.get("policy_score"), 0.0),
                "policy_reason": row.get("policy_reason", "admit"),
                "status": "pt_ready_applied",
                "applied_at_epoch": int(time.time()),
            }
            record["record_digest"] = _sha(record)
            feedback = {
                "ready_flow_key": ready_flow_key,
                "source_key": source_key,
                "policy_key": row.get("policy_key"),
                "policy_score": _float(row.get("policy_score"), 0.0),
                "outcome_status": "applied",
                "outcome_digest": record["record_digest"],
                "feedback_at_epoch": int(time.time()),
            }
            feedback["feedback_digest"] = _sha(feedback)
            _append_jsonl(applied_path, record)
            _append_jsonl(feedback_path, feedback)
            records.append(record)
            feedback_records.append(feedback)
            applied_seen.add(ready_flow_key)
            feedback_seen.add(ready_flow_key)
            state_after["applied_total"] = int(state_after.get("applied_total", 0)) + 1
            state_after["pt_ready_applied_total"] = int(state_after.get("pt_ready_applied_total", 0)) + 1
            state_after["last_items"] = (list(state_after.get("last_items", [])) + [source_key])[-20:]
        if records or replay_count:
            state_after["last_pt_ready_flow_epoch"] = int(time.time())
            state_after["last_pt_ready_feedback_count"] = len(feedback_records)
            _write_json(state_path, state_after)
    elif rows:
        warnings.append("ready_rows_present_but_flow_blocked")

    state_digest_after = _sha(_read_json(state_path) if ready and (records or replay_count) else state_after)
    core = {
        "runtime_root": str(root),
        "applied": len(records),
        "replay": replay_count,
        "state_after_digest": state_digest_after,
    }
    packet_id = "qi-pt-ready-flow-" + _sha(core)[:16]
    if blockers:
        status = "QI_PT_READY_FLOW_BLOCKED"
    elif not rows:
        status = "QI_PT_READY_FLOW_IDLE"
    elif not records and replay_count:
        status = "QI_PT_READY_FLOW_REPLAYED"
    else:
        status = "QI_PT_READY_FLOW_APPLIED"

    return QiPTReadyFlowResult(
        ready_flow_version="kuuos_runtime_daemon_qi_pt_ready_flow_v0_5",
        ready_flow_status=status,
        ready_flow_packet_id=packet_id,
        runtime_root=str(root),
        ready_queue_path=str(ready_queue_path),
        applied_path=str(applied_path),
        state_path=str(state_path),
        feedback_path=str(feedback_path),
        applied_count=len(records),
        replay_count=replay_count,
        state_digest_before=state_digest_before,
        state_digest_after=state_digest_after,
        feedback_count=len(feedback_records),
        records=records,
        feedback_records=feedback_records,
        blockers=blockers,
        warnings=warnings,
        local_state_written=ready and bool(records or replay_count),
        local_log_appended=ready and bool(records),
        feedback_appended=ready and bool(feedback_records),
    )
