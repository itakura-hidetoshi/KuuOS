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
class QiMultiWorkResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    source_path: str
    state_path: str
    work_log_path: str
    applied_count: int
    replay_count: int
    qi_gain: float
    qi_drag: float
    recovery_gain: float
    memory_gain: float
    work_counts: dict[str, int]
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


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


def _append_text(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _key(row: Mapping[str, Any]) -> str:
    return str(row.get("policy_key") or row.get("item_id") or row.get("idempotency_key") or _sha(dict(row)))


def _seen(path: pathlib.Path) -> set[str]:
    return {str(row.get("work_key")) for row in _read_jsonl(path) if row.get("work_key")}


def _ordered(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda row: (-_float(row.get("policy_score"), 0.0), _key(row)))


def _gains(pt: Mapping[str, Any]) -> tuple[float, float, float, float]:
    p = max(0.0, min(1.0, _float(pt.get("execution_pressure", pt.get("pressure")), 0.0)))
    c = max(0.0, min(1.0, _float(pt.get("coherence_score", pt.get("coherence")), 0.0)))
    m = max(0, _int(pt.get("memory_depth", pt.get("history_depth")), 0))
    r = pt.get("recovery_witness_present") is True and pt.get("recovery_witness_missing") is not True
    return round(1.0 + p * c, 6), round(1.0 - c, 6), round(0.25 if r else -0.5, 6), round(min(m, 20) * 0.05, 6)


def _record_path(root: pathlib.Path, key: str) -> pathlib.Path:
    return root / "records" / f"{key[:16]}.json"


def _snapshot_path(root: pathlib.Path, digest: str) -> pathlib.Path:
    return root / "snapshots" / f"state_{digest[:16]}.json"


def _do_work(root: pathlib.Path, state: dict[str, Any], row: Mapping[str, Any], *, qi_gain: float, qi_drag: float, recovery_gain: float, memory_gain: float) -> dict[str, Any]:
    kind = str(row.get("item_kind", row.get("work_kind", "state_patch")))
    source_key = _key(row)
    output: dict[str, Any] = {"kind": kind, "source_key": source_key}
    if kind == "metric":
        base = _float(row.get("value"), 1.0)
        metric = {"source_key": source_key, "name": row.get("name", "qi_metric"), "value": round(base * qi_gain - qi_drag, 6), "qi_gain": qi_gain, "epoch": int(time.time())}
        _append_jsonl(root / "metrics.jsonl", metric)
        output["metric_value"] = metric["value"]
    elif kind == "note":
        text = str(row.get("text", source_key))
        line = f"- {int(time.time())} | {source_key} | gain={qi_gain} | {text}\n"
        _append_text(root / "notes.md", line)
        output["note_appended"] = True
    elif kind == "record":
        payload = {"source_key": source_key, "row": dict(row), "qi_gain": qi_gain, "memory_gain": memory_gain, "epoch": int(time.time())}
        path = _record_path(root, source_key)
        _write_json(path, payload)
        output["record_path"] = str(path)
    elif kind == "state_patch":
        energy = _float(row.get("energy_delta"), 0.0) * qi_gain - qi_drag
        stable = _float(row.get("stability_delta"), 0.0) + memory_gain + recovery_gain
        state["qi_energy"] = round(_float(state.get("qi_energy"), 0.0) + energy, 6)
        state["qi_stability"] = round(_float(state.get("qi_stability"), 0.0) + stable, 6)
        output["energy_delta"] = round(energy, 6)
        output["stability_delta"] = round(stable, 6)
    elif kind == "counter":
        name = str(row.get("name", "counter"))
        amount = max(1, int(round(_float(row.get("amount"), 1.0) * qi_gain + memory_gain)))
        counters = state.setdefault("counters", {})
        counters[name] = int(counters.get(name, 0)) + amount
        output["counter"] = name
        output["amount"] = amount
    elif kind == "snapshot":
        digest = _sha(state)
        path = _snapshot_path(root, digest)
        _write_json(path, {"source_key": source_key, "state_digest": digest, "state": state, "epoch": int(time.time())})
        output["snapshot_path"] = str(path)
    elif kind == "pull_deferred":
        deferred_path = root / "queue.deferred.jsonl"
        ready_path = root / "queue.ready.jsonl"
        rows = _read_jsonl(deferred_path)
        n = max(0, int(round(qi_gain + memory_gain + max(0.0, recovery_gain))))
        pulled = []
        for item in rows[:n]:
            new_item = dict(item)
            new_item["policy_reason"] = "pulled_by_qi_multi_work"
            new_item["policy_score"] = round(_float(new_item.get("policy_score"), 0.0) + qi_gain + recovery_gain, 6)
            new_item["pull_source_key"] = source_key
            _append_jsonl(ready_path, new_item)
            pulled.append(new_item)
        output["pulled_count"] = len(pulled)
    else:
        state["last_unknown_work"] = kind
        output["unknown_recorded"] = True
    state["multi_work_total"] = int(state.get("multi_work_total", 0)) + 1
    state["last_multi_work_kind"] = kind
    state["last_multi_work_epoch"] = int(time.time())
    return output


def build_qi_multi_work(*, runtime_context: Mapping[str, Any], process_tensor_packet: Mapping[str, Any], work_license_packet: Mapping[str, Any]) -> QiMultiWorkResult:
    ctx = _mapping(runtime_context)
    pt = _mapping(process_tensor_packet)
    lic = _mapping(work_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    source_path = root / "queue.ready.jsonl"
    state_path = root / "state.json"
    work_log_path = root / "multi_work_log.jsonl"
    if ctx.get("qi_multi_work_enabled") is not True:
        blockers.append("qi_multi_work_enabled_not_true")
    if ctx.get("apply_multi_work") is not True:
        blockers.append("apply_multi_work_not_true")
    if lic.get("license_status") != "QI_MULTI_WORK_LICENSE_READY":
        blockers.append("work_license_not_ready")
    for name in ["source_read_allowed", "state_write_allowed", "work_log_append_allowed", "metric_append_allowed", "note_append_allowed", "record_write_allowed", "queue_append_allowed", "snapshot_write_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    if pt.get("process_tensor_ok") is not True:
        blockers.append("process_tensor_not_ok")
    if pt.get("non_markov_unresolved") is True:
        blockers.append("non_markov_unresolved")
    max_apply = max(1, _int(ctx.get("max_apply"), 100))
    qi_gain, qi_drag, recovery_gain, memory_gain = _gains(pt)
    rows = _ordered(_read_jsonl(source_path))[:max_apply]
    seen = _seen(work_log_path)
    state = _read_json(state_path)
    records: list[dict[str, Any]] = []
    replay = 0
    counts: dict[str, int] = {}
    ready = not blockers
    if ready:
        for row in rows:
            key = _key(row)
            work_key = _sha({"key": key, "row": row, "pt": _sha(dict(pt))})
            if work_key in seen:
                replay += 1
                continue
            output = _do_work(root, state, row, qi_gain=qi_gain, qi_drag=qi_drag, recovery_gain=recovery_gain, memory_gain=memory_gain)
            kind = str(output.get("kind", "unknown"))
            counts[kind] = counts.get(kind, 0) + 1
            rec = {"work_key": work_key, "source_key": key, "kind": kind, "qi_gain": qi_gain, "qi_drag": qi_drag, "recovery_gain": recovery_gain, "memory_gain": memory_gain, "output": output, "state_digest": _sha(state), "epoch": int(time.time())}
            rec["record_digest"] = _sha(rec)
            _append_jsonl(work_log_path, rec)
            records.append(rec)
            seen.add(work_key)
        if records or replay:
            state["last_multi_work_qi_gain"] = qi_gain
            state["last_multi_work_qi_drag"] = qi_drag
            state["last_multi_work_recovery_gain"] = recovery_gain
            state["last_multi_work_memory_gain"] = memory_gain
            _write_json(state_path, state)
    elif rows:
        warnings.append("rows_present_but_work_blocked")
    core = {"root": str(root), "applied": len(records), "replay": replay, "counts": counts}
    packet_id = "qi-multi-work-" + _sha(core)[:16]
    if blockers:
        status = "QI_MULTI_WORK_BLOCKED"
    elif not rows:
        status = "QI_MULTI_WORK_IDLE"
    elif not records and replay:
        status = "QI_MULTI_WORK_REPLAYED"
    else:
        status = "QI_MULTI_WORK_APPLIED"
    return QiMultiWorkResult("kuuos_runtime_daemon_qi_multi_work_v0_7", status, packet_id, str(root), str(source_path), str(state_path), str(work_log_path), len(records), replay, qi_gain, qi_drag, recovery_gain, memory_gain, counts, records, blockers, warnings)
