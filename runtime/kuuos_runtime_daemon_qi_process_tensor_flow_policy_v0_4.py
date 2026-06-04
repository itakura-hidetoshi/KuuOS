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
class QiProcessTensorFlowPolicyResult:
    policy_version: str
    policy_status: str
    policy_packet_id: str
    runtime_root: str
    input_queue_path: str
    ready_queue_path: str
    deferred_queue_path: str
    policy_state_path: str
    policy_log_path: str
    admitted_count: int
    deferred_count: int
    replay_count: int
    pressure: float
    coherence: float
    memory_depth: int
    non_markov_unresolved: bool
    recovery_witness_present: bool
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]
    local_state_written: bool
    local_log_appended: bool
    authority: str = "qi_process_tensor_flow_policy_v0_4"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _bool(value: Any, default: bool = False) -> bool:
    return value if isinstance(value, bool) else default


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


def _sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


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


def _append_many(path: pathlib.Path, rows: list[Mapping[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(dict(row), ensure_ascii=False, sort_keys=True) + "\n")


def _seen_keys(path: pathlib.Path) -> set[str]:
    return {str(row.get("policy_key")) for row in _read_jsonl(path) if row.get("policy_key")}


def _item_key(row: Mapping[str, Any]) -> str:
    return str(row.get("idempotency_key") or row.get("item_id") or _sha(dict(row)))


def _score(row: Mapping[str, Any], *, pressure: float, coherence: float, memory_depth: int, preferred: set[str]) -> float:
    item_kind = str(row.get("item_kind", row.get("action", "local_item")))
    base = _float(row.get("priority"), 0.0)
    if item_kind in preferred:
        base += 1.0
    base += max(0.0, min(1.0, pressure))
    base += 0.5 * max(0.0, min(1.0, coherence))
    base += min(memory_depth, 10) * 0.01
    return round(base, 6)


def build_qi_process_tensor_flow_policy(
    *,
    runtime_context: Mapping[str, Any],
    process_tensor_packet: Mapping[str, Any],
    policy_license_packet: Mapping[str, Any],
) -> QiProcessTensorFlowPolicyResult:
    ctx = _mapping(runtime_context)
    pt = _mapping(process_tensor_packet)
    lic = _mapping(policy_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    input_queue_path = root / "queue.jsonl"
    ready_queue_path = root / "queue.ready.jsonl"
    deferred_queue_path = root / "queue.deferred.jsonl"
    policy_state_path = root / "pt_policy_state.json"
    policy_log_path = root / "pt_policy_log.jsonl"

    if ctx.get("qi_process_tensor_flow_policy_enabled") is not True:
        blockers.append("qi_process_tensor_flow_policy_enabled_not_true")
    if ctx.get("apply_process_tensor_policy") is not True:
        blockers.append("apply_process_tensor_policy_not_true")
    if lic.get("license_status") != "QI_PROCESS_TENSOR_FLOW_POLICY_LICENSE_READY":
        blockers.append("policy_license_not_ready")
    if lic.get("queue_read_allowed") is not True:
        blockers.append("queue_read_not_allowed")
    if lic.get("ready_queue_append_allowed") is not True:
        blockers.append("ready_queue_append_not_allowed")
    if lic.get("deferred_queue_append_allowed") is not True:
        blockers.append("deferred_queue_append_not_allowed")
    if lic.get("policy_state_write_allowed") is not True:
        blockers.append("policy_state_write_not_allowed")
    if lic.get("policy_log_append_allowed") is not True:
        blockers.append("policy_log_append_not_allowed")

    pt_ok = _bool(pt.get("process_tensor_ok"), False)
    non_markov_unresolved = _bool(pt.get("non_markov_unresolved"), False)
    recovery_missing = _bool(pt.get("recovery_witness_missing"), False)
    recovery_present = _bool(pt.get("recovery_witness_present"), not recovery_missing)
    pressure = _float(pt.get("execution_pressure", pt.get("pressure")), 0.0)
    coherence = _float(pt.get("coherence_score", pt.get("coherence")), 0.0)
    memory_depth = _int(pt.get("memory_depth", pt.get("history_depth")), 0)
    preferred = {str(item) for item in _list(pt.get("preferred_actions"))}
    blocked = {str(item) for item in _list(pt.get("blocked_actions"))}

    if not pt_ok:
        blockers.append("process_tensor_not_ok")
    if non_markov_unresolved:
        warnings.append("non_markov_unresolved_defers_items")
    if recovery_missing or not recovery_present:
        warnings.append("recovery_witness_missing_defers_items")

    max_rows = _int(ctx.get("max_rows"), 100)
    if max_rows < 1:
        blockers.append("max_rows_invalid")
        max_rows = 1
    max_admit = _int(ctx.get("max_admit"), max_rows)
    if max_admit < 0:
        blockers.append("max_admit_invalid")
        max_admit = 0

    rows = _read_jsonl(input_queue_path)[:max_rows]
    seen = _seen_keys(policy_log_path)
    replay_count = 0
    candidates: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []

    ready = not blockers
    if ready:
        for row in rows:
            key = _item_key(row)
            policy_key = _sha({"item_key": key, "row": row, "pt_digest": _sha(dict(pt))})
            if policy_key in seen:
                replay_count += 1
                continue
            item_kind = str(row.get("item_kind", row.get("action", "local_item")))
            reason = "admit"
            if item_kind in blocked:
                reason = "blocked_by_process_tensor"
            elif non_markov_unresolved:
                reason = "defer_non_markov_unresolved"
            elif recovery_missing or not recovery_present:
                reason = "defer_recovery_witness_missing"
            enriched = dict(row)
            enriched.update({
                "policy_key": policy_key,
                "source_key": key,
                "process_tensor_digest": _sha(dict(pt)),
                "policy_reason": reason,
                "policy_score": _score(row, pressure=pressure, coherence=coherence, memory_depth=memory_depth, preferred=preferred),
                "pressure": pressure,
                "coherence": coherence,
                "memory_depth": memory_depth,
                "policy_applied_at_epoch": int(time.time()),
            })
            if reason == "admit":
                candidates.append(enriched)
            else:
                deferred.append(enriched)
        candidates.sort(key=lambda item: (-_float(item.get("policy_score"), 0.0), str(item.get("source_key"))))
        admitted = candidates[:max_admit]
        deferred.extend(candidates[max_admit:])
        for item in candidates[max_admit:]:
            item["policy_reason"] = "defer_capacity"
        _append_many(ready_queue_path, admitted)
        _append_many(deferred_queue_path, deferred)
        for item in admitted + deferred:
            record = {
                "policy_key": item["policy_key"],
                "source_key": item["source_key"],
                "policy_reason": item["policy_reason"],
                "policy_score": item["policy_score"],
                "process_tensor_digest": item["process_tensor_digest"],
                "record_digest": _sha(item),
            }
            _append_jsonl(policy_log_path, record)
            records.append(record)
        state = _read_json(policy_state_path)
        state.update({
            "last_policy_epoch": int(time.time()),
            "pressure": pressure,
            "coherence": coherence,
            "memory_depth": memory_depth,
            "admitted_total": int(state.get("admitted_total", 0)) + len(admitted),
            "deferred_total": int(state.get("deferred_total", 0)) + len(deferred),
            "replay_total": int(state.get("replay_total", 0)) + replay_count,
            "last_policy_records": records[-20:],
        })
        if records or replay_count:
            _write_json(policy_state_path, state)
    elif rows:
        warnings.append("queue_rows_present_but_policy_blocked")

    core = {
        "runtime_root": str(root),
        "admitted": len([r for r in records if r.get("policy_reason") == "admit"]),
        "deferred": len([r for r in records if r.get("policy_reason") != "admit"]),
        "replay": replay_count,
        "pt": _sha(dict(pt)),
    }
    packet_id = "qi-pt-flow-" + _sha(core)[:16]
    if blockers:
        status = "QI_PROCESS_TENSOR_FLOW_POLICY_BLOCKED"
    elif not rows:
        status = "QI_PROCESS_TENSOR_FLOW_POLICY_IDLE"
    elif not records and replay_count:
        status = "QI_PROCESS_TENSOR_FLOW_POLICY_REPLAYED"
    else:
        status = "QI_PROCESS_TENSOR_FLOW_POLICY_APPLIED"

    admitted_count = len([r for r in records if r.get("policy_reason") == "admit"])
    deferred_count = len([r for r in records if r.get("policy_reason") != "admit"])
    return QiProcessTensorFlowPolicyResult(
        policy_version="kuuos_runtime_daemon_qi_process_tensor_flow_policy_v0_4",
        policy_status=status,
        policy_packet_id=packet_id,
        runtime_root=str(root),
        input_queue_path=str(input_queue_path),
        ready_queue_path=str(ready_queue_path),
        deferred_queue_path=str(deferred_queue_path),
        policy_state_path=str(policy_state_path),
        policy_log_path=str(policy_log_path),
        admitted_count=admitted_count,
        deferred_count=deferred_count,
        replay_count=replay_count,
        pressure=pressure,
        coherence=coherence,
        memory_depth=memory_depth,
        non_markov_unresolved=non_markov_unresolved,
        recovery_witness_present=recovery_present,
        records=records,
        blockers=blockers,
        warnings=warnings,
        local_state_written=ready and bool(records or replay_count),
        local_log_appended=ready and bool(records),
    )
