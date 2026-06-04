#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_closed_run_v1_1 import build_qi_closed_run


@dataclass(frozen=True)
class QiEpochRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    epochs_requested: int
    epochs_completed: int
    tasks_loaded: int
    tasks_injected: int
    closed_runs_applied: int
    closed_runs_idle: int
    next_pt_path: str
    next_context_path: str
    epoch_chain_path: str
    epoch_final_path: str
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


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


def _task_key(task: Mapping[str, Any]) -> str:
    return str(task.get("task_id") or task.get("policy_key") or task.get("item_id") or _sha(dict(task)))


def _seen_injections(path: pathlib.Path) -> set[str]:
    return {str(row.get("injection_key")) for row in _read_jsonl(path) if row.get("injection_key")}


def _due_tasks(tasks: list[dict[str, Any]], epoch: int) -> list[dict[str, Any]]:
    due: list[dict[str, Any]] = []
    for task in tasks:
        due_epoch = _i(task.get("due_epoch"), 0)
        period = _i(task.get("period"), 0)
        if epoch < due_epoch:
            continue
        if period > 0 and (epoch - due_epoch) % period != 0:
            continue
        due.append(task)
    return sorted(due, key=lambda item: (-float(item.get("policy_score", 0.0) or 0.0), _task_key(item)))


def _inject_tasks(root: pathlib.Path, tasks: list[dict[str, Any]], epoch: int, injection_log_path: pathlib.Path) -> int:
    ready_path = root / "queue.ready.jsonl"
    seen = _seen_injections(injection_log_path)
    injected = 0
    for task in tasks:
        key = _task_key(task)
        injection_key = _sha({"epoch": epoch, "task_key": key, "task": task})
        if injection_key in seen:
            continue
        row = dict(task)
        row.update({
            "policy_key": f"epoch:{epoch}:{key}",
            "epoch": epoch,
            "epoch_task_key": key,
            "injection_key": injection_key,
        })
        row.setdefault("item_kind", row.get("kind", "metric"))
        row.setdefault("policy_score", 1.0)
        _append_jsonl(ready_path, row)
        _append_jsonl(injection_log_path, {"injection_key": injection_key, "epoch": epoch, "task_key": key, "row_digest": _sha(row), "epoch_time": int(time.time())})
        seen.add(injection_key)
        injected += 1
    return injected


def _closed_license(lic: Mapping[str, Any]) -> dict[str, Any]:
    nested = lic.get("closed_run_license_packet")
    if isinstance(nested, Mapping):
        return dict(nested)
    value = {
        "license_status": "QI_CLOSED_RUN_LICENSE_READY",
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


def build_qi_epoch_runner(*, runtime_context: Mapping[str, Any], pt_packet: Mapping[str, Any], epoch_license_packet: Mapping[str, Any]) -> QiEpochRunnerResult:
    ctx = dict(_m(runtime_context))
    pt = dict(_m(pt_packet))
    lic = _m(epoch_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    epoch_chain_path = root / "epoch_chain.jsonl"
    epoch_final_path = root / "epoch_final.json"
    injection_log_path = root / "epoch_injections.jsonl"
    tasks_path = root / "epoch_tasks.jsonl"
    if ctx.get("qi_epoch_runner_enabled") is not True:
        blockers.append("qi_epoch_runner_enabled_not_true")
    if ctx.get("apply_epoch_runner") is not True:
        blockers.append("apply_epoch_runner_not_true")
    if lic.get("license_status") != "QI_EPOCH_RUNNER_LICENSE_READY":
        blockers.append("epoch_runner_license_not_ready")
    for name in ["task_read_allowed", "task_inject_allowed", "epoch_chain_append_allowed", "epoch_final_write_allowed", "pt_carry_allowed", "context_carry_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    epochs = max(1, min(_i(ctx.get("max_epochs"), 4), _i(ctx.get("epochs"), 1)))
    start_epoch = _i(ctx.get("start_epoch"), 0)
    tasks = _read_jsonl(tasks_path)
    records: list[dict[str, Any]] = []
    total_injected = 0
    applied = 0
    idle = 0
    completed = 0
    current_pt = dict(pt)
    current_ctx = dict(ctx)
    current_ctx.update({"qi_closed_run_enabled": True, "apply_closed_run": True, "runtime_root": str(root)})
    if not blockers:
        for offset in range(epochs):
            epoch = start_epoch + offset
            due = _due_tasks(tasks, epoch)
            injected = _inject_tasks(root, due, epoch, injection_log_path)
            total_injected += injected
            current_ctx["epoch"] = epoch
            result = build_qi_closed_run(
                runtime_context=current_ctx,
                pt_packet=current_pt,
                closed_license_packet=_closed_license(lic),
            )
            payload = result.to_dict()
            status = str(payload.get("status"))
            if status == "QI_CLOSED_RUN_APPLIED":
                applied += 1
            elif status == "QI_CLOSED_RUN_IDLE":
                idle += 1
            elif status == "QI_CLOSED_RUN_BLOCKED":
                blockers.append(f"closed_run_blocked_epoch_{epoch}")
            rec = {
                "epoch": epoch,
                "status": status,
                "packet_id": payload.get("packet_id"),
                "tasks_due": len(due),
                "tasks_injected": injected,
                "items_applied": payload.get("items_applied", 0),
                "graph_nodes_done": payload.get("graph_nodes_done", 0),
                "next_cycles": payload.get("next_cycles", 0),
                "next_budget": payload.get("next_budget", 0),
                "payload_digest": _sha(payload),
                "epoch_time": int(time.time()),
            }
            rec["record_digest"] = _sha(rec)
            _append_jsonl(epoch_chain_path, rec)
            records.append(rec)
            completed += 1
            next_pt = _read_json(root / "pt_next.json")
            next_ctx = _read_json(root / "next_loop_context.json")
            if next_pt:
                current_pt = next_pt
            if next_ctx:
                current_ctx.update(next_ctx)
                current_ctx.update({"qi_closed_run_enabled": True, "apply_closed_run": True, "runtime_root": str(root)})
            if status == "QI_CLOSED_RUN_BLOCKED":
                break
    else:
        warnings.append("epoch_runner_blocked_before_run")
    status = "QI_EPOCH_RUNNER_BLOCKED" if blockers else ("QI_EPOCH_RUNNER_IDLE" if completed == 0 or (applied == 0 and total_injected == 0) else "QI_EPOCH_RUNNER_APPLIED")
    packet_id = "qi-epoch-runner-" + _sha({"root": str(root), "records": records, "blockers": blockers})[:16]
    final = {
        "version": "kuuos_runtime_daemon_qi_epoch_runner_v1_2",
        "status": status,
        "packet_id": packet_id,
        "epochs_requested": epochs,
        "epochs_completed": completed,
        "tasks_loaded": len(tasks),
        "tasks_injected": total_injected,
        "closed_runs_applied": applied,
        "closed_runs_idle": idle,
        "next_pt_path": str(root / "pt_next.json"),
        "next_context_path": str(root / "next_loop_context.json"),
        "epoch_chain_path": str(epoch_chain_path),
        "blockers": blockers,
        "warnings": warnings,
        "epoch_time": int(time.time()),
    }
    if lic.get("epoch_final_write_allowed") is True:
        _write_json(epoch_final_path, final)
    return QiEpochRunnerResult(
        "kuuos_runtime_daemon_qi_epoch_runner_v1_2",
        status,
        packet_id,
        str(root),
        epochs,
        completed,
        len(tasks),
        total_injected,
        applied,
        idle,
        str(root / "pt_next.json"),
        str(root / "next_loop_context.json"),
        str(epoch_chain_path),
        str(epoch_final_path),
        records,
        blockers,
        warnings,
    )
