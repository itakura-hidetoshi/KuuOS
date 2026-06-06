#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_loop_coordinator_v6_0 import build_qi_github_actions_loop_coordinator
from runtime.kuuos_runtime_daemon_qi_github_actions_loop_step_executor_v6_1 import build_qi_github_actions_loop_step_executor


TERMINAL_STEP_CLASSES = {
    "waiting_for_connector_operation",
    "waiting_for_external_observation",
    "local_stage_blocked",
}

LOCAL_STAGES = {
    "plan_from_status",
    "operation_result_ingest",
    "status_reobserve",
    "observation_result_ingest",
}

WAIT_STAGES = {
    "await_connector_operation",
    "await_status_observation",
}


@dataclass(frozen=True)
class QiGitHubActionsLoopRunExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    steps_run: int
    stop_reason: str
    final_stage: str
    final_step_result_class: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]
    step_records: list[dict[str, Any]]

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


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _coordinator_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_loop_coordinator_enabled": True,
        "apply_github_actions_loop_coordinator": True,
        "runtime_root": str(root),
    }


def _coordinator_license(stage: str | None = None) -> dict[str, Any]:
    value = {
        "license_status": "QI_GITHUB_ACTIONS_LOOP_COORDINATOR_LICENSE_READY",
        "loop_state_read_allowed": True,
        "loop_command_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    for name in LOCAL_STAGES | WAIT_STAGES:
        value[f"allow_{name}_stage"] = True
    if stage:
        value[f"allow_{stage}_stage"] = True
    return value


def _step_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_loop_step_executor_enabled": True,
        "apply_github_actions_loop_step_executor": True,
        "runtime_root": str(root),
    }


def _step_license() -> dict[str, Any]:
    value = {
        "license_status": "QI_GITHUB_ACTIONS_LOOP_STEP_EXECUTOR_LICENSE_READY",
        "loop_command_read_allowed": True,
        "local_step_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    for name in LOCAL_STAGES | WAIT_STAGES:
        value[f"allow_{name}_stage"] = True
    return value


def _record(index: int, coord: Mapping[str, Any], step: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "index": index,
        "coordinator_status": str(coord.get("status", "unknown")),
        "step_status": str(step.get("status", "unknown")),
        "selected_stage": str(coord.get("selected_stage", step.get("selected_stage", "unknown"))),
        "next_command": str(coord.get("next_command", step.get("next_command", "unknown"))),
        "step_result_class": str(step.get("step_result_class", "unknown")),
        "local_step_performed": step.get("local_step_performed") is True,
        "coordinator_digest": _sha(dict(coord)),
        "step_digest": _sha(dict(step)),
        "epoch": int(time.time()),
    }


def build_qi_github_actions_loop_run_executor(*, runtime_context: Mapping[str, Any], loop_run_executor_license: Mapping[str, Any]) -> QiGitHubActionsLoopRunExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(loop_run_executor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_loop_run_executor_receipt.json"
    audit_path = root / "qi_github_actions_loop_run_executor_audit.jsonl"

    if ctx.get("qi_github_actions_loop_run_executor_enabled") is not True:
        blockers.append("qi_github_actions_loop_run_executor_enabled_not_true")
    if ctx.get("apply_github_actions_loop_run_executor") is not True:
        blockers.append("apply_github_actions_loop_run_executor_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_LOOP_RUN_EXECUTOR_LICENSE_READY":
        blockers.append("github_actions_loop_run_executor_license_not_ready")
    for name in ["coordinator_run_allowed", "step_executor_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    max_steps = _i(ctx.get("max_loop_steps", 5), 5)
    if max_steps < 1:
        blockers.append("max_loop_steps_invalid")
        max_steps = 0
    if max_steps > 20:
        warnings.append("max_loop_steps_capped_to_20")
        max_steps = 20

    records: list[dict[str, Any]] = []
    stop_reason = "not_run"
    final_stage = "unknown"
    final_step_class = "unknown"
    if not blockers:
        stop_reason = "max_steps_reached"
        for index in range(1, max_steps + 1):
            coord = build_qi_github_actions_loop_coordinator(
                runtime_context=_coordinator_context(root),
                loop_coordinator_license=_coordinator_license(),
            ).to_dict()
            if coord.get("status") != "QI_GITHUB_ACTIONS_LOOP_COORDINATOR_READY":
                blockers.append("coordinator_not_ready")
                stop_reason = "coordinator_blocked"
                final_stage = str(coord.get("selected_stage", "unknown"))
                final_step_class = "coordinator_blocked"
                break
            step = build_qi_github_actions_loop_step_executor(
                runtime_context=_step_context(root),
                loop_step_executor_license=_step_license(),
            ).to_dict()
            records.append(_record(index, coord, step))
            final_stage = str(step.get("selected_stage", coord.get("selected_stage", "unknown")))
            final_step_class = str(step.get("step_result_class", "unknown"))
            if step.get("status") != "QI_GITHUB_ACTIONS_LOOP_STEP_EXECUTOR_READY":
                blockers.append("step_executor_not_ready")
                stop_reason = "step_blocked"
                break
            if final_step_class in TERMINAL_STEP_CLASSES:
                stop_reason = final_step_class
                break
            if final_step_class != "local_stage_completed":
                stop_reason = "unknown_step_result_class"
                blockers.append("unknown_step_result_class")
                break

    status = "QI_GITHUB_ACTIONS_LOOP_RUN_EXECUTOR_READY" if not blockers else "QI_GITHUB_ACTIONS_LOOP_RUN_EXECUTOR_BLOCKED"
    packet_id = "qi-github-actions-loop-run-" + _sha({"records": records, "stop": stop_reason, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_loop_run_executor_v6_2",
        "status": status,
        "packet_id": packet_id,
        "steps_run": len(records),
        "stop_reason": stop_reason,
        "final_stage": final_stage,
        "final_step_result_class": final_step_class,
        "step_records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsLoopRunExecutorResult(
        "kuuos_runtime_daemon_qi_github_actions_loop_run_executor_v6_2",
        status,
        packet_id,
        str(root),
        len(records),
        stop_reason,
        final_stage,
        final_step_class,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
        records,
    )
