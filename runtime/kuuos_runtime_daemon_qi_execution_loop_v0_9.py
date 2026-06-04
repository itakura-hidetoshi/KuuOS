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
class QiExecutionLoopResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    state_path: str
    loop_log_path: str
    summary_path: str
    feedback_path: str
    cycles_requested: int
    cycles_completed: int
    items_applied: int
    graph_nodes_done: int
    qi_gain: float
    qi_drag: float
    recovery_gain: float
    memory_gain: float
    state_digest_before: str
    state_digest_after: str
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


def _gains(pt: Mapping[str, Any]) -> tuple[float, float, float, float]:
    p = max(0.0, min(1.0, _float(pt.get("execution_pressure", pt.get("pressure")), 0.0)))
    c = max(0.0, min(1.0, _float(pt.get("coherence_score", pt.get("coherence")), 0.0)))
    m = max(0, _int(pt.get("memory_depth", pt.get("history_depth")), 0))
    r = pt.get("recovery_witness_present") is True and pt.get("recovery_witness_missing") is not True
    return round(1.0 + p * c, 6), round(1.0 - c, 6), round(0.25 if r else -0.5, 6), round(min(m, 20) * 0.05, 6)


def _key(row: Mapping[str, Any]) -> str:
    return str(row.get("policy_key") or row.get("item_id") or row.get("idempotency_key") or _sha(dict(row)))


def _seen(path: pathlib.Path, field: str) -> set[str]:
    return {str(row.get(field)) for row in _read_jsonl(path) if row.get(field)}


def _sort_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda row: (-_float(row.get("policy_score"), 0.0), _key(row)))


def _apply_item(state: dict[str, Any], row: Mapping[str, Any], *, gain: float, drag: float, rgain: float, mgain: float) -> dict[str, Any]:
    kind = str(row.get("item_kind", row.get("kind", "state_patch")))
    out: dict[str, Any] = {"kind": kind, "source_key": _key(row)}
    if kind == "metric":
        value = round(_float(row.get("value"), 1.0) * gain - drag, 6)
        state["loop_metric_total"] = round(_float(state.get("loop_metric_total"), 0.0) + value, 6)
        out["value"] = value
    elif kind == "counter":
        name = str(row.get("name", "loop"))
        amount = max(1, int(round(_float(row.get("amount"), 1.0) * gain + mgain)))
        counters = state.setdefault("counters", {})
        counters[name] = int(counters.get(name, 0)) + amount
        out["counter"] = name
        out["amount"] = amount
    elif kind == "recover":
        delta = round(0.5 + rgain + mgain, 6)
        state["qi_recovery"] = round(_float(state.get("qi_recovery"), 0.0) + delta, 6)
        out["delta_recovery"] = delta
    else:
        energy = round(_float(row.get("energy_delta"), 0.1) * gain - drag, 6)
        stability = round(_float(row.get("stability_delta"), 0.1) + rgain + mgain, 6)
        state["qi_energy"] = round(_float(state.get("qi_energy"), 0.0) + energy, 6)
        state["qi_stability"] = round(_float(state.get("qi_stability"), 0.0) + stability, 6)
        out["delta_energy"] = energy
        out["delta_stability"] = stability
    state["loop_item_total"] = int(state.get("loop_item_total", 0)) + 1
    return out


def _nodes(graph: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = graph.get("nodes", [])
    return [dict(item) for item in raw if isinstance(item, Mapping)] if isinstance(raw, list) else []


def _graph_done(log_path: pathlib.Path) -> set[str]:
    return {str(row.get("node_id")) for row in _read_jsonl(log_path) if row.get("node_id") and row.get("status") == "done"}


def _ready_nodes(nodes: list[dict[str, Any]], done: set[str]) -> list[dict[str, Any]]:
    ready: list[dict[str, Any]] = []
    for node in nodes:
        node_id = str(node.get("id", ""))
        deps = node.get("depends_on", [])
        if not isinstance(deps, list):
            deps = []
        if node_id and node_id not in done and all(str(dep) in done for dep in deps):
            ready.append(node)
    return sorted(ready, key=lambda node: (-_float(node.get("score"), 0.0), str(node.get("id", ""))))


def _run_node(root: pathlib.Path, state: dict[str, Any], node: Mapping[str, Any], *, gain: float, drag: float, rgain: float, mgain: float) -> dict[str, Any]:
    node_id = str(node.get("id"))
    kind = str(node.get("kind", "state_patch"))
    out: dict[str, Any] = {"node_id": node_id, "kind": kind}
    if kind == "report":
        path = root / "loop_reports" / f"{node_id}.md"
        text = f"# {node_id}\n- gain: {gain}\n- drag: {drag}\n- loop_item_total: {state.get('loop_item_total', 0)}\n"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        out["report_path"] = str(path)
    elif kind == "checkpoint":
        digest = _sha(state)
        path = root / "loop_checkpoints" / f"{node_id}_{digest[:16]}.json"
        _write_json(path, {"node_id": node_id, "state_digest": digest, "state": state, "epoch": int(time.time())})
        out["checkpoint_path"] = str(path)
    elif kind == "note":
        path = root / "loop_notes.md"
        _append_text(path, f"- {int(time.time())} | {node_id} | gain={gain}\n")
        out["note_path"] = str(path)
    else:
        state["qi_energy"] = round(_float(state.get("qi_energy"), 0.0) + _float(node.get("energy_delta"), 0.1) * gain - drag, 6)
        state["qi_stability"] = round(_float(state.get("qi_stability"), 0.0) + _float(node.get("stability_delta"), 0.1) + rgain + mgain, 6)
        out["state_patched"] = True
    state["loop_graph_total"] = int(state.get("loop_graph_total", 0)) + 1
    return out


def build_qi_execution_loop(*, runtime_context: Mapping[str, Any], process_tensor_packet: Mapping[str, Any], loop_license_packet: Mapping[str, Any]) -> QiExecutionLoopResult:
    ctx = _mapping(runtime_context)
    pt = _mapping(process_tensor_packet)
    lic = _mapping(loop_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    state_path = root / "state.json"
    loop_log_path = root / "loop.jsonl"
    summary_path = root / "run_summary.json"
    feedback_path = root / "loop_feedback.jsonl"
    graph_log_path = root / "loop_graph_log.jsonl"
    if ctx.get("qi_execution_loop_enabled") is not True:
        blockers.append("qi_execution_loop_enabled_not_true")
    if ctx.get("apply_execution_loop") is not True:
        blockers.append("apply_execution_loop_not_true")
    if lic.get("license_status") != "QI_EXECUTION_LOOP_LICENSE_READY":
        blockers.append("loop_license_not_ready")
    for name in ["queue_read_allowed", "state_write_allowed", "loop_log_append_allowed", "summary_write_allowed", "feedback_append_allowed", "artifact_write_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    if pt.get("process_tensor_ok") is not True:
        blockers.append("process_tensor_not_ok")
    if pt.get("non_markov_unresolved") is True:
        blockers.append("non_markov_unresolved")
    gain, drag, rgain, mgain = _gains(pt)
    cycles = max(1, _int(ctx.get("cycles"), 1))
    cycle_budget = max(1, int(round(max(1, _int(ctx.get("base_cycle_budget"), 3)) * gain + mgain + max(0.0, rgain))))
    rows = _sort_rows(_read_jsonl(root / "queue.ready.jsonl"))
    row_seen = _seen(loop_log_path, "item_key")
    graph = _read_json(root / "work_graph.json")
    graph_nodes = _nodes(graph)
    graph_done = _graph_done(graph_log_path)
    before = _read_json(state_path)
    state = dict(before)
    before_digest = _sha(before)
    records: list[dict[str, Any]] = []
    applied_items = 0
    graph_done_count = 0
    ready = not blockers
    cursor = 0
    if ready:
        for cycle in range(cycles):
            cycle_records: list[dict[str, Any]] = []
            used = 0
            while used < cycle_budget and cursor < len(rows):
                row = rows[cursor]
                cursor += 1
                item_key = _sha({"key": _key(row), "row": row, "pt": _sha(dict(pt))})
                if item_key in row_seen:
                    continue
                output = _apply_item(state, row, gain=gain, drag=drag, rgain=rgain, mgain=mgain)
                rec = {"record_kind": "item", "cycle": cycle, "item_key": item_key, "source_key": _key(row), "output": output, "state_digest": _sha(state), "epoch": int(time.time())}
                rec["record_digest"] = _sha(rec)
                _append_jsonl(loop_log_path, rec)
                records.append(rec)
                cycle_records.append(rec)
                row_seen.add(item_key)
                applied_items += 1
                used += 1
            while used < cycle_budget:
                ready_nodes = _ready_nodes(graph_nodes, graph_done)
                if not ready_nodes:
                    break
                node = ready_nodes[0]
                node_id = str(node.get("id"))
                graph_key = _sha({"node_id": node_id, "node": node, "pt": _sha(dict(pt))})
                output = _run_node(root, state, node, gain=gain, drag=drag, rgain=rgain, mgain=mgain)
                rec = {"record_kind": "graph", "cycle": cycle, "graph_key": graph_key, "node_id": node_id, "status": "done", "output": output, "state_digest": _sha(state), "epoch": int(time.time())}
                rec["record_digest"] = _sha(rec)
                _append_jsonl(graph_log_path, rec)
                _append_jsonl(loop_log_path, rec)
                records.append(rec)
                cycle_records.append(rec)
                graph_done.add(node_id)
                graph_done_count += 1
                used += 1
            fb = {"cycle": cycle, "cycle_records": len(cycle_records), "state_digest": _sha(state), "qi_gain": gain, "qi_drag": drag, "recovery_gain": rgain, "memory_gain": mgain, "epoch": int(time.time())}
            fb["feedback_digest"] = _sha(fb)
            _append_jsonl(feedback_path, fb)
            if not cycle_records:
                break
        state["last_loop_epoch"] = int(time.time())
        state["last_loop_cycles_requested"] = cycles
        state["last_loop_records"] = len(records)
        state["last_loop_qi_gain"] = gain
        _write_json(state_path, state)
        summary = {"status": "complete", "cycles_requested": cycles, "records": len(records), "items_applied": applied_items, "graph_nodes_done": graph_done_count, "state_digest": _sha(state), "qi_gain": gain, "qi_drag": drag, "recovery_gain": rgain, "memory_gain": mgain}
        _write_json(summary_path, summary)
    else:
        warnings.append("loop_blocked_before_state_change")
    after = _read_json(state_path) if ready else state
    after_digest = _sha(after)
    packet_id = "qi-execution-loop-" + _sha({"root": str(root), "records": len(records), "after": after_digest})[:16]
    if blockers:
        status = "QI_EXECUTION_LOOP_BLOCKED"
    elif not records:
        status = "QI_EXECUTION_LOOP_IDLE"
    else:
        status = "QI_EXECUTION_LOOP_APPLIED"
    return QiExecutionLoopResult("kuuos_runtime_daemon_qi_execution_loop_v0_9", status, packet_id, str(root), str(state_path), str(loop_log_path), str(summary_path), str(feedback_path), cycles, min(cycles, max(1, len(_read_jsonl(feedback_path)))), applied_items, graph_done_count, gain, drag, rgain, mgain, before_digest, after_digest, records, blockers, warnings)
