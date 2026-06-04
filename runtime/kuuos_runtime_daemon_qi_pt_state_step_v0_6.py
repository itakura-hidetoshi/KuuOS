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
class QiPTStateStepResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    source_path: str
    state_path: str
    step_log_path: str
    fb_path: str
    applied_count: int
    replay_count: int
    qi_gain: float
    qi_drag: float
    recovery_gain: float
    memory_gain: float
    state_before_digest: str
    state_after_digest: str
    step_records: list[dict[str, Any]]
    fb_records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]
    state_written: bool
    log_appended: bool
    fb_appended: bool

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


def _key(row: Mapping[str, Any]) -> str:
    return str(row.get("policy_key") or row.get("item_id") or row.get("idempotency_key") or _sha(dict(row)))


def _seen(path: pathlib.Path) -> set[str]:
    return {str(row.get("step_key")) for row in _read_jsonl(path) if row.get("step_key")}


def _ordered(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda row: (-_float(row.get("policy_score"), 0.0), _key(row)))


def _gains(pt: Mapping[str, Any]) -> tuple[float, float, float, float]:
    p = max(0.0, min(1.0, _float(pt.get("execution_pressure", pt.get("pressure")), 0.0)))
    c = max(0.0, min(1.0, _float(pt.get("coherence_score", pt.get("coherence")), 0.0)))
    m = max(0, _int(pt.get("memory_depth", pt.get("history_depth")), 0))
    r = pt.get("recovery_witness_present") is True and pt.get("recovery_witness_missing") is not True
    return round(1.0 + p * c, 6), round(1.0 - c, 6), round(0.25 if r else -0.5, 6), round(min(m, 20) * 0.05, 6)


def _apply(state: dict[str, Any], row: Mapping[str, Any], g: float, d: float, r: float, m: float) -> dict[str, Any]:
    kind = str(row.get("item_kind", row.get("action", "item")))
    dt = 1
    de = round(0.1 * g - 0.05 * d, 6)
    ds = round(0.05 * g + 0.05 * m - 0.05 * d, 6)
    dr = 0.0
    if kind == "advance_tick":
        dt = max(1, int(round(g + m)))
        de = round(g - d, 6)
    elif kind == "recover":
        dr = round(0.5 + r + m, 6)
        ds = round(0.1 + r, 6)
    elif kind == "hold":
        dt = 0
        ds = round(0.2 + r, 6)
    elif kind == "freeze":
        dt = 0
        ds = round(0.5, 6)
        state["frozen"] = True
    elif kind == "observe":
        ds = round(0.1 + m, 6)
    state["tick"] = int(state.get("tick", 0)) + dt
    state["qi_energy"] = round(_float(state.get("qi_energy"), 0.0) + de, 6)
    state["qi_stability"] = round(_float(state.get("qi_stability"), 0.0) + ds, 6)
    state["qi_recovery"] = round(_float(state.get("qi_recovery"), 0.0) + dr, 6)
    state["last_kind"] = kind
    state["step_total"] = int(state.get("step_total", 0)) + 1
    return {"kind": kind, "delta_tick": dt, "delta_energy": de, "delta_stability": ds, "delta_recovery": dr}


def build_qi_pt_state_step(*, runtime_context: Mapping[str, Any], process_tensor_packet: Mapping[str, Any], step_license_packet: Mapping[str, Any]) -> QiPTStateStepResult:
    ctx = _mapping(runtime_context)
    pt = _mapping(process_tensor_packet)
    lic = _mapping(step_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    source_path = root / "queue.ready.jsonl"
    state_path = root / "state.json"
    step_log_path = root / "pt_step_log.jsonl"
    fb_path = root / "pt_feedback.jsonl"
    if ctx.get("qi_pt_state_step_enabled") is not True:
        blockers.append("qi_pt_state_step_enabled_not_true")
    if ctx.get("apply_pt_state_step") is not True:
        blockers.append("apply_pt_state_step_not_true")
    if lic.get("license_status") != "QI_PT_STATE_STEP_LICENSE_READY":
        blockers.append("step_license_not_ready")
    for name in ["source_read_allowed", "state_write_allowed", "step_log_append_allowed", "feedback_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    if pt.get("process_tensor_ok") is not True:
        blockers.append("process_tensor_not_ok")
    if pt.get("non_markov_unresolved") is True:
        blockers.append("non_markov_unresolved")
    max_apply = max(1, _int(ctx.get("max_apply"), 100))
    gain, drag, rgain, mgain = _gains(pt)
    rows = _ordered(_read_jsonl(source_path))[:max_apply]
    seen = _seen(step_log_path)
    before = _read_json(state_path)
    state = dict(before)
    before_digest = _sha(before)
    steps: list[dict[str, Any]] = []
    fbs: list[dict[str, Any]] = []
    replay = 0
    ready = not blockers
    if ready:
        for row in rows:
            key = _key(row)
            step_key = _sha({"key": key, "pt": _sha(dict(pt)), "row": row})
            if step_key in seen:
                replay += 1
                continue
            delta = _apply(state, row, gain, drag, rgain, mgain)
            rec = {"step_key": step_key, "source_key": key, "qi_gain": gain, "qi_drag": drag, "recovery_gain": rgain, "memory_gain": mgain, **delta, "state_digest": _sha(state), "epoch": int(time.time())}
            rec["record_digest"] = _sha(rec)
            fb = {"step_key": step_key, "source_key": key, "outcome": "pt_state_step_applied", "state_digest": rec["state_digest"], "record_digest": rec["record_digest"], "epoch": int(time.time())}
            fb["feedback_digest"] = _sha(fb)
            _append_jsonl(step_log_path, rec)
            _append_jsonl(fb_path, fb)
            steps.append(rec)
            fbs.append(fb)
            seen.add(step_key)
        if steps or replay:
            state["last_qi_gain"] = gain
            state["last_qi_drag"] = drag
            state["last_recovery_gain"] = rgain
            state["last_memory_gain"] = mgain
            state["last_step_epoch"] = int(time.time())
            _write_json(state_path, state)
    elif rows:
        warnings.append("rows_present_but_step_blocked")
    after = _read_json(state_path) if ready and (steps or replay) else state
    after_digest = _sha(after)
    core = {"root": str(root), "applied": len(steps), "replay": replay, "after": after_digest}
    packet_id = "qi-pt-state-step-" + _sha(core)[:16]
    if blockers:
        status = "QI_PT_STATE_STEP_BLOCKED"
    elif not rows:
        status = "QI_PT_STATE_STEP_IDLE"
    elif not steps and replay:
        status = "QI_PT_STATE_STEP_REPLAYED"
    else:
        status = "QI_PT_STATE_STEP_APPLIED"
    return QiPTStateStepResult("kuuos_runtime_daemon_qi_pt_state_step_v0_6", status, packet_id, str(root), str(source_path), str(state_path), str(step_log_path), str(fb_path), len(steps), replay, gain, drag, rgain, mgain, before_digest, after_digest, steps, fbs, blockers, warnings, ready and bool(steps or replay), ready and bool(steps), ready and bool(fbs))
