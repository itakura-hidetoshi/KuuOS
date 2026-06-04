#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_epoch_runner_v1_2 import build_qi_epoch_runner


@dataclass(frozen=True)
class QiObjectiveRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    objectives_path: str
    epoch_tasks_path: str
    work_graph_path: str
    objective_plan_path: str
    objective_final_path: str
    objectives_loaded: int
    tasks_created: int
    graph_nodes_created: int
    epoch_status: str
    epochs_completed: int
    tasks_injected: int
    progress_score: float
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _f(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _i(value: Any, default: int = 0) -> int:
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
        if not line.strip():
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


def _objectives(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("objectives", [])
    return [dict(item) for item in raw if isinstance(item, Mapping)] if isinstance(raw, list) else []


def _existing_task_keys(path: pathlib.Path) -> set[str]:
    return {str(row.get("task_id")) for row in _read_jsonl(path) if row.get("task_id")}


def _existing_node_ids(graph: Mapping[str, Any]) -> set[str]:
    raw = graph.get("nodes", [])
    if not isinstance(raw, list):
        return set()
    return {str(node.get("id")) for node in raw if isinstance(node, Mapping) and node.get("id")}


def _pt_factor(pt: Mapping[str, Any]) -> float:
    pressure = max(0.0, min(1.0, _f(pt.get("execution_pressure", pt.get("pressure")), 0.0)))
    coherence = max(0.0, min(1.0, _f(pt.get("coherence_score", pt.get("coherence")), 0.0)))
    memory = max(0, _i(pt.get("memory_depth", pt.get("history_depth")), 0))
    return round(1.0 + pressure * 0.5 + coherence * 0.5 + min(memory, 10) * 0.03, 6)


def _task_for(obj: Mapping[str, Any], index: int, factor: float) -> dict[str, Any]:
    oid = str(obj.get("id") or f"objective_{index}")
    kind = str(obj.get("task_kind", obj.get("item_kind", "metric")))
    base_value = _f(obj.get("value"), _f(obj.get("target"), 1.0))
    score = round(_f(obj.get("priority"), 1.0) * factor, 6)
    task = {
        "task_id": f"obj:{oid}:task",
        "objective_id": oid,
        "due_epoch": _i(obj.get("due_epoch"), index),
        "period": _i(obj.get("period"), 0),
        "item_kind": kind,
        "policy_score": score,
        "value": base_value,
    }
    if "name" in obj:
        task["name"] = obj["name"]
    if kind == "counter":
        task.setdefault("name", oid)
        task["amount"] = max(1, _i(obj.get("amount"), 1))
    if kind == "state_patch":
        task["energy_delta"] = _f(obj.get("energy_delta"), base_value)
        task["stability_delta"] = _f(obj.get("stability_delta"), 0.1)
    if kind == "recover":
        task["value"] = base_value
    return task


def _nodes_for(obj: Mapping[str, Any], index: int, factor: float) -> list[dict[str, Any]]:
    oid = str(obj.get("id") or f"objective_{index}")
    make_report = obj.get("make_report", True) is not False
    make_checkpoint = obj.get("make_checkpoint", True) is not False
    nodes: list[dict[str, Any]] = []
    roll_id = f"obj_{oid}_rollup"
    nodes.append({"id": roll_id, "kind": "metric_rollup", "score": round(10.0 * factor - index, 6)})
    if make_report:
        report_id = f"obj_{oid}_report"
        nodes.append({"id": report_id, "kind": "report", "depends_on": [roll_id], "title": str(obj.get("title", oid)), "score": round(8.0 * factor - index, 6)})
    else:
        report_id = roll_id
    if make_checkpoint:
        nodes.append({"id": f"obj_{oid}_checkpoint", "kind": "checkpoint", "depends_on": [report_id], "score": round(6.0 * factor - index, 6)})
    return nodes


def _epoch_license(lic: Mapping[str, Any]) -> dict[str, Any]:
    nested = lic.get("epoch_license_packet")
    if isinstance(nested, Mapping):
        return dict(nested)
    value = {
        "license_status": "QI_EPOCH_RUNNER_LICENSE_READY",
        "task_read_allowed": True,
        "task_inject_allowed": True,
        "epoch_chain_append_allowed": True,
        "epoch_final_write_allowed": True,
        "pt_carry_allowed": True,
        "context_carry_allowed": True,
        "chain_append_allowed": True,
        "final_write_allowed": True,
        "queue_read_allowed": True,
        "state_write_allowed": True,
        "loop_log_append_allowed": True,
        "summary_write_allowed": True,
        "feedback_append_allowed": True,
        "artifact_write_allowed": True,
        "state_read_allowed": True,
        "summary_read_allowed": True,
        "feedback_read_allowed": True,
        "next_pt_write_allowed": True,
        "next_context_write_allowed": True,
        "adapt_log_append_allowed": True,
    }
    for key in list(value):
        if key in lic:
            value[key] = lic[key]
    return value


def build_qi_objective_runner(*, runtime_context: Mapping[str, Any], pt_packet: Mapping[str, Any], objective_license_packet: Mapping[str, Any]) -> QiObjectiveRunnerResult:
    ctx = dict(_m(runtime_context))
    pt = dict(_m(pt_packet))
    lic = _m(objective_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    objectives_path = root / "objectives.json"
    epoch_tasks_path = root / "epoch_tasks.jsonl"
    work_graph_path = root / "work_graph.json"
    objective_plan_path = root / "objective_plan.json"
    objective_final_path = root / "objective_final.json"
    plan_log_path = root / "objective_plan_log.jsonl"
    if ctx.get("qi_objective_runner_enabled") is not True:
        blockers.append("qi_objective_runner_enabled_not_true")
    if ctx.get("apply_objective_runner") is not True:
        blockers.append("apply_objective_runner_not_true")
    if lic.get("license_status") != "QI_OBJECTIVE_RUNNER_LICENSE_READY":
        blockers.append("objective_runner_license_not_ready")
    for name in ["objective_read_allowed", "task_write_allowed", "graph_write_allowed", "plan_write_allowed", "final_write_allowed", "epoch_run_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    if pt.get("process_tensor_ok") is not True:
        blockers.append("process_tensor_not_ok")
    if pt.get("non_markov_unresolved") is True:
        blockers.append("non_markov_unresolved")
    objective_payload = _read_json(objectives_path)
    objectives = _objectives(objective_payload)
    if not objectives and not blockers:
        warnings.append("objectives_empty")
    tasks_created = 0
    nodes_created = 0
    records: list[dict[str, Any]] = []
    factor = _pt_factor(pt)
    ready = not blockers
    if ready:
        task_keys = _existing_task_keys(epoch_tasks_path)
        graph = _read_json(work_graph_path)
        raw_nodes = graph.get("nodes", [])
        nodes = [dict(node) for node in raw_nodes if isinstance(node, Mapping)] if isinstance(raw_nodes, list) else []
        node_ids = _existing_node_ids({"nodes": nodes})
        for index, obj in enumerate(objectives):
            task = _task_for(obj, index, factor)
            if task["task_id"] not in task_keys:
                _append_jsonl(epoch_tasks_path, task)
                task_keys.add(task["task_id"])
                tasks_created += 1
            for node in _nodes_for(obj, index, factor):
                node_id = str(node.get("id"))
                if node_id not in node_ids:
                    nodes.append(node)
                    node_ids.add(node_id)
                    nodes_created += 1
            rec = {"objective_id": str(obj.get("id") or f"objective_{index}"), "task_id": task["task_id"], "pt_factor": factor, "objective_digest": _sha(obj), "epoch_time": int(time.time())}
            rec["record_digest"] = _sha(rec)
            records.append(rec)
        _write_json(work_graph_path, {"nodes": nodes, "generated_by": "qi_objective_runner_v1_3", "epoch_time": int(time.time())})
        plan = {"objectives": len(objectives), "tasks_created": tasks_created, "graph_nodes_created": nodes_created, "pt_factor": factor, "records": records, "plan_digest": _sha(records), "epoch_time": int(time.time())}
        _write_json(objective_plan_path, plan)
        _append_jsonl(plan_log_path, {"plan_digest": plan["plan_digest"], "tasks_created": tasks_created, "graph_nodes_created": nodes_created, "epoch_time": int(time.time())})
    epoch_status = "NOT_RUN"
    epochs_completed = 0
    tasks_injected = 0
    progress_score = 0.0
    if ready and lic.get("epoch_run_allowed") is True:
        epoch_ctx = dict(ctx)
        epoch_ctx.update({"qi_epoch_runner_enabled": True, "apply_epoch_runner": True, "runtime_root": str(root)})
        epoch_result = build_qi_epoch_runner(runtime_context=epoch_ctx, pt_packet=pt, epoch_license_packet=_epoch_license(lic))
        epoch_payload = epoch_result.to_dict()
        epoch_status = str(epoch_payload.get("status"))
        epochs_completed = _i(epoch_payload.get("epochs_completed"), 0)
        tasks_injected = _i(epoch_payload.get("tasks_injected"), 0)
        if epoch_status == "QI_EPOCH_RUNNER_BLOCKED":
            blockers.append("epoch_runner_blocked")
        progress_score = round(tasks_injected + epochs_completed + nodes_created * 0.25, 6)
    elif ready:
        warnings.append("epoch_run_skipped")
    status = "QI_OBJECTIVE_RUNNER_BLOCKED" if blockers else ("QI_OBJECTIVE_RUNNER_IDLE" if not objectives else "QI_OBJECTIVE_RUNNER_APPLIED")
    packet_id = "qi-objective-runner-" + _sha({"root": str(root), "records": records, "status": status, "epoch_status": epoch_status})[:16]
    final = {"version": "kuuos_runtime_daemon_qi_objective_runner_v1_3", "status": status, "packet_id": packet_id, "objectives_loaded": len(objectives), "tasks_created": tasks_created, "graph_nodes_created": nodes_created, "epoch_status": epoch_status, "epochs_completed": epochs_completed, "tasks_injected": tasks_injected, "progress_score": progress_score, "objective_plan_path": str(objective_plan_path), "epoch_final_path": str(root / "epoch_final.json"), "blockers": blockers, "warnings": warnings, "epoch_time": int(time.time())}
    if lic.get("final_write_allowed") is True:
        _write_json(objective_final_path, final)
    return QiObjectiveRunnerResult("kuuos_runtime_daemon_qi_objective_runner_v1_3", status, packet_id, str(root), str(objectives_path), str(epoch_tasks_path), str(work_graph_path), str(objective_plan_path), str(objective_final_path), len(objectives), tasks_created, nodes_created, epoch_status, epochs_completed, tasks_injected, progress_score, records, blockers, warnings)
