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
class QiWorkGraphResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    graph_path: str
    state_path: str
    graph_log_path: str
    done_count: int
    hold_count: int
    replay_count: int
    budget: int
    qi_gain: float
    qi_drag: float
    recovery_gain: float
    memory_gain: float
    node_counts: dict[str, int]
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


def _write_text(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


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


def _seen(path: pathlib.Path) -> set[str]:
    return {str(row.get("graph_key")) for row in _read_jsonl(path) if row.get("graph_key")}


def _nodes(graph: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = graph.get("nodes", [])
    return [dict(item) for item in raw if isinstance(item, Mapping)] if isinstance(raw, list) else []


def _ready_nodes(nodes: list[dict[str, Any]], done: set[str]) -> list[dict[str, Any]]:
    ready: list[dict[str, Any]] = []
    for node in nodes:
        node_id = str(node.get("id", ""))
        if not node_id or node_id in done:
            continue
        deps = node.get("depends_on", [])
        if not isinstance(deps, list):
            deps = []
        if all(str(dep) in done for dep in deps):
            ready.append(node)
    return sorted(ready, key=lambda n: (-_float(n.get("score"), 0.0), str(n.get("id", ""))))


def _metric_rollup(root: pathlib.Path) -> dict[str, Any]:
    rows = _read_jsonl(root / "metrics.jsonl")
    total = 0.0
    count = 0
    by_name: dict[str, float] = {}
    for row in rows:
        value = _float(row.get("value"), 0.0)
        name = str(row.get("name", "metric"))
        total += value
        count += 1
        by_name[name] = round(by_name.get(name, 0.0) + value, 6)
    return {"count": count, "total": round(total, 6), "by_name": by_name}


def _run_node(root: pathlib.Path, state: dict[str, Any], node: Mapping[str, Any], *, qi_gain: float, qi_drag: float, recovery_gain: float, memory_gain: float) -> dict[str, Any]:
    node_id = str(node.get("id"))
    kind = str(node.get("kind", "state_patch"))
    out: dict[str, Any] = {"node_id": node_id, "kind": kind}
    if kind == "metric_rollup":
        rollup = _metric_rollup(root)
        path = root / "rollups" / f"{node_id}.json"
        _write_json(path, {"node_id": node_id, "rollup": rollup, "qi_gain": qi_gain, "epoch": int(time.time())})
        out["rollup_path"] = str(path)
        out["metric_count"] = rollup["count"]
    elif kind == "report":
        title = str(node.get("title", node_id))
        rollup = _metric_rollup(root)
        text = [f"# {title}\n", f"- qi_gain: {qi_gain}\n", f"- qi_drag: {qi_drag}\n", f"- recovery_gain: {recovery_gain}\n", f"- memory_gain: {memory_gain}\n", f"- metric_count: {rollup['count']}\n", f"- metric_total: {rollup['total']}\n"]
        path = root / "reports" / f"{node_id}.md"
        _write_text(path, "".join(text))
        out["report_path"] = str(path)
    elif kind == "checkpoint":
        digest = _sha(state)
        path = root / "checkpoints" / f"{node_id}_{digest[:16]}.json"
        _write_json(path, {"node_id": node_id, "state_digest": digest, "state": state, "epoch": int(time.time())})
        out["checkpoint_path"] = str(path)
    elif kind == "index":
        items = []
        for sub in ["reports", "rollups", "checkpoints", "records", "snapshots"]:
            folder = root / sub
            if folder.exists():
                items.extend(str(path.relative_to(root)) for path in sorted(folder.glob("**/*")) if path.is_file())
        path = root / "index.json"
        _write_json(path, {"node_id": node_id, "items": items, "count": len(items), "epoch": int(time.time())})
        out["index_path"] = str(path)
        out["index_count"] = len(items)
    elif kind == "state_patch":
        e = _float(node.get("energy_delta"), 0.0) * qi_gain - qi_drag
        s = _float(node.get("stability_delta"), 0.0) + recovery_gain + memory_gain
        state["qi_energy"] = round(_float(state.get("qi_energy"), 0.0) + e, 6)
        state["qi_stability"] = round(_float(state.get("qi_stability"), 0.0) + s, 6)
        out["energy_delta"] = round(e, 6)
        out["stability_delta"] = round(s, 6)
    elif kind == "append_note":
        path = root / "graph_notes.md"
        _append_text(path, f"- {int(time.time())} | {node_id} | gain={qi_gain} | {node.get('text', '')}\n")
        out["note_path"] = str(path)
    elif kind == "ready_seed":
        path = root / "queue.ready.jsonl"
        item = {"policy_key": f"graph:{node_id}", "item_kind": node.get("item_kind", "metric"), "policy_score": round(_float(node.get("score"), 0.0) + qi_gain + recovery_gain, 6), "graph_node_id": node_id}
        _append_jsonl(path, item)
        out["seeded_ready"] = True
    else:
        state["last_graph_unknown"] = kind
        out["unknown_recorded"] = True
    state["work_graph_total"] = int(state.get("work_graph_total", 0)) + 1
    state["last_work_graph_node"] = node_id
    state["last_work_graph_kind"] = kind
    state["last_work_graph_epoch"] = int(time.time())
    return out


def build_qi_work_graph(*, runtime_context: Mapping[str, Any], process_tensor_packet: Mapping[str, Any], graph_license_packet: Mapping[str, Any]) -> QiWorkGraphResult:
    ctx = _mapping(runtime_context)
    pt = _mapping(process_tensor_packet)
    lic = _mapping(graph_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    graph_path = root / "work_graph.json"
    state_path = root / "state.json"
    graph_log_path = root / "work_graph_log.jsonl"
    if ctx.get("qi_work_graph_enabled") is not True:
        blockers.append("qi_work_graph_enabled_not_true")
    if ctx.get("apply_work_graph") is not True:
        blockers.append("apply_work_graph_not_true")
    if lic.get("license_status") != "QI_WORK_GRAPH_LICENSE_READY":
        blockers.append("graph_license_not_ready")
    for name in ["graph_read_allowed", "state_write_allowed", "graph_log_append_allowed", "artifact_write_allowed", "queue_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    if pt.get("process_tensor_ok") is not True:
        blockers.append("process_tensor_not_ok")
    if pt.get("non_markov_unresolved") is True:
        blockers.append("non_markov_unresolved")
    qi_gain, qi_drag, recovery_gain, memory_gain = _gains(pt)
    base_budget = max(1, _int(ctx.get("base_budget"), 3))
    budget = max(1, min(_int(ctx.get("max_budget"), 20), int(round(base_budget * qi_gain + memory_gain + max(0.0, recovery_gain)))))
    graph = _read_json(graph_path)
    nodes = _nodes(graph)
    if not nodes and not blockers:
        warnings.append("work_graph_empty")
    seen = _seen(graph_log_path)
    done = {str(row.get("node_id")) for row in _read_jsonl(graph_log_path) if row.get("status") == "done" and row.get("node_id")}
    state = _read_json(state_path)
    records: list[dict[str, Any]] = []
    replay = 0
    hold = 0
    counts: dict[str, int] = {}
    ready = not blockers
    if ready:
        while len(records) < budget:
            ready_nodes = _ready_nodes(nodes, done)
            if not ready_nodes:
                break
            node = ready_nodes[0]
            node_id = str(node.get("id"))
            graph_key = _sha({"node_id": node_id, "node": node, "pt": _sha(dict(pt))})
            if graph_key in seen:
                replay += 1
                done.add(node_id)
                continue
            output = _run_node(root, state, node, qi_gain=qi_gain, qi_drag=qi_drag, recovery_gain=recovery_gain, memory_gain=memory_gain)
            kind = str(output.get("kind", node.get("kind", "unknown")))
            counts[kind] = counts.get(kind, 0) + 1
            rec = {"graph_key": graph_key, "node_id": node_id, "kind": kind, "status": "done", "output": output, "state_digest": _sha(state), "qi_gain": qi_gain, "qi_drag": qi_drag, "recovery_gain": recovery_gain, "memory_gain": memory_gain, "epoch": int(time.time())}
            rec["record_digest"] = _sha(rec)
            _append_jsonl(graph_log_path, rec)
            records.append(rec)
            seen.add(graph_key)
            done.add(node_id)
        hold = len([n for n in nodes if str(n.get("id", "")) not in done])
        if records or replay:
            state["last_work_graph_budget"] = budget
            state["last_work_graph_done_count"] = len(done)
            state["last_work_graph_hold_count"] = hold
            state["last_work_graph_qi_gain"] = qi_gain
            _write_json(state_path, state)
    elif nodes:
        warnings.append("nodes_present_but_graph_blocked")
    packet_id = "qi-work-graph-" + _sha({"root": str(root), "done": len(records), "replay": replay, "budget": budget})[:16]
    if blockers:
        status = "QI_WORK_GRAPH_BLOCKED"
    elif not nodes:
        status = "QI_WORK_GRAPH_IDLE"
    elif not records and replay:
        status = "QI_WORK_GRAPH_REPLAYED"
    else:
        status = "QI_WORK_GRAPH_APPLIED"
    return QiWorkGraphResult("kuuos_runtime_daemon_qi_work_graph_v0_8", status, packet_id, str(root), str(graph_path), str(state_path), str(graph_log_path), len(records), hold, replay, budget, qi_gain, qi_drag, recovery_gain, memory_gain, counts, records, blockers, warnings)
