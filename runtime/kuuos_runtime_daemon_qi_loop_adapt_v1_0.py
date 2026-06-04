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
class QiLoopAdaptResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    feedback_count: int
    records_seen: int
    items_seen: int
    graph_seen: int
    pressure_before: float
    pressure_after: float
    coherence_before: float
    coherence_after: float
    memory_before: int
    memory_after: int
    next_cycles: int
    next_budget: int
    next_pt_path: str
    next_context_path: str
    log_path: str
    record: dict[str, Any]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(v: Any) -> Mapping[str, Any]:
    return v if isinstance(v, Mapping) else {}


def _sha(v: Any) -> str:
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _f(v: Any, default: float = 0.0) -> float:
    if isinstance(v, bool):
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _i(v: Any, default: int = 0) -> int:
    if isinstance(v, bool):
        return default
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _clamp(v: float) -> float:
    return round(max(0.0, min(1.0, v)), 6)


def _root(v: Any, blockers: list[str]) -> pathlib.Path:
    if not v:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(v)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        v = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return v if isinstance(v, dict) else {}


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
        if not line.strip():
            continue
        try:
            v = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(v, dict):
            rows.append(v)
    return rows


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as h:
        h.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _stats(summary: Mapping[str, Any], feedback: list[dict[str, Any]], state: Mapping[str, Any]) -> tuple[int, int, int, float]:
    records = _i(summary.get("records"), 0) or sum(_i(row.get("cycle_records"), 0) for row in feedback)
    items = _i(summary.get("items_applied"), 0) or _i(state.get("loop_item_total"), 0)
    graph = _i(summary.get("graph_nodes_done"), 0) or _i(state.get("loop_graph_total"), 0)
    cycles = max(1, len(feedback))
    return records, items, graph, records / cycles


def build_qi_loop_adapt(*, runtime_context: Mapping[str, Any], pt_packet: Mapping[str, Any], adapt_license_packet: Mapping[str, Any]) -> QiLoopAdaptResult:
    ctx = _m(runtime_context)
    pt = _m(pt_packet)
    lic = _m(adapt_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    state_path = root / "state.json"
    summary_path = root / "run_summary.json"
    feedback_path = root / "loop_feedback.jsonl"
    next_pt_path = root / "pt_next.json"
    next_context_path = root / "next_loop_context.json"
    log_path = root / "adapt_log.jsonl"
    if ctx.get("qi_loop_adapt_enabled") is not True:
        blockers.append("qi_loop_adapt_enabled_not_true")
    if ctx.get("apply_loop_adapt") is not True:
        blockers.append("apply_loop_adapt_not_true")
    if lic.get("license_status") != "QI_LOOP_ADAPT_LICENSE_READY":
        blockers.append("loop_adapt_license_not_ready")
    for name in ["state_read_allowed", "summary_read_allowed", "feedback_read_allowed", "next_pt_write_allowed", "next_context_write_allowed", "adapt_log_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    state = _read_json(state_path)
    summary = _read_json(summary_path)
    feedback = _read_jsonl(feedback_path)
    if not summary and not blockers:
        warnings.append("summary_empty")
    if not feedback and not blockers:
        warnings.append("feedback_empty")
    records, items, graph, density = _stats(summary, feedback, state)
    p0 = _f(pt.get("execution_pressure", pt.get("pressure")), 0.0)
    c0 = _f(pt.get("coherence_score", pt.get("coherence")), 0.0)
    m0 = _i(pt.get("memory_depth", pt.get("history_depth")), 0)
    target = max(1.0, _f(pt.get("target_cycle_density"), 3.0))
    ratio = min(2.0, density / target)
    p1 = _clamp(p0 + 0.08 * (1.0 - ratio) + (0.02 if graph == 0 else -0.02))
    c1 = _clamp(c0 + 0.04 * min(1.0, _f(state.get("qi_stability"), 0.0)) + 0.02 * min(1.0, records / target))
    m1 = max(0, m0 + (1 if records else 0) + (1 if items and graph else 0))
    recover = bool(pt.get("recovery_witness_present", True)) or _f(state.get("qi_recovery"), 0.0) > 0 or graph > 0
    base_cycles = max(1, _i(ctx.get("cycles"), _i(summary.get("cycles_requested"), 1)))
    next_cycles = max(1, min(_i(ctx.get("max_cycles"), 8), base_cycles + (1 if records else 0)))
    base_budget = max(1, _i(ctx.get("base_cycle_budget"), 3))
    next_budget = max(1, min(_i(ctx.get("max_base_cycle_budget"), 12), base_budget + (1 if c1 >= c0 else 0)))
    next_pt = dict(pt)
    next_pt.update({
        "process_tensor_ok": True,
        "execution_pressure": p1,
        "coherence_score": c1,
        "memory_depth": m1,
        "recovery_witness_present": recover,
        "recovery_witness_missing": not recover,
        "non_markov_unresolved": False,
        "previous_feedback_digest": _sha(feedback),
        "previous_summary_digest": _sha(summary),
        "adaptation_version": "qi_loop_adapt_v1_0",
        "adapted_at_epoch": int(time.time()),
    })
    next_context = dict(ctx)
    next_context.update({
        "qi_execution_loop_enabled": True,
        "apply_execution_loop": True,
        "runtime_root": str(root),
        "cycles": next_cycles,
        "base_cycle_budget": next_budget,
        "adapted_from": "qi_loop_adapt_v1_0",
        "adapted_at_epoch": int(time.time()),
    })
    record = {
        "adapt_key": _sha({"pt": dict(pt), "summary": summary, "feedback": feedback}),
        "records_seen": records,
        "items_seen": items,
        "graph_seen": graph,
        "density": round(density, 6),
        "pressure_before": p0,
        "pressure_after": p1,
        "coherence_before": c0,
        "coherence_after": c1,
        "memory_before": m0,
        "memory_after": m1,
        "next_cycles": next_cycles,
        "next_budget": next_budget,
        "next_pt_digest": _sha(next_pt),
        "next_context_digest": _sha(next_context),
        "epoch": int(time.time()),
    }
    record["record_digest"] = _sha(record)
    ready = not blockers
    if ready:
        _write_json(next_pt_path, next_pt)
        _write_json(next_context_path, next_context)
        _append_jsonl(log_path, record)
    else:
        warnings.append("adapt_blocked_before_write")
    status = "QI_LOOP_ADAPT_BLOCKED" if blockers else ("QI_LOOP_ADAPT_IDLE" if not summary and not feedback else "QI_LOOP_ADAPT_APPLIED")
    packet_id = "qi-loop-adapt-" + _sha({"root": str(root), "record": record, "blockers": blockers})[:16]
    return QiLoopAdaptResult(
        "kuuos_runtime_daemon_qi_loop_adapt_v1_0",
        status,
        packet_id,
        str(root),
        len(feedback),
        records,
        items,
        graph,
        p0,
        p1,
        c0,
        c1,
        m0,
        m1,
        next_cycles,
        next_budget,
        str(next_pt_path),
        str(next_context_path),
        str(log_path),
        record if ready else {},
        blockers,
        warnings,
    )
