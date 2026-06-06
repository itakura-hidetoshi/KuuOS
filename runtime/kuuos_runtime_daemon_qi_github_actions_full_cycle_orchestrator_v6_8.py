#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_loop_run_executor_v6_2 import build_qi_github_actions_loop_run_executor
from runtime.kuuos_runtime_daemon_qi_github_actions_external_cycle_runner_v6_7 import build_qi_github_actions_external_cycle_runner


@dataclass(frozen=True)
class QiGitHubActionsFullCycleOrchestratorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    phases_run: int
    stop_reason: str
    final_phase: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]
    phase_records: list[dict[str, Any]]

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


def _exists(root: pathlib.Path, name: str) -> bool:
    return (root / name).is_file() and (root / name).stat().st_size > 2


def _loop_context(root: pathlib.Path, max_loop_steps: int) -> dict[str, Any]:
    return {
        "qi_github_actions_loop_run_executor_enabled": True,
        "apply_github_actions_loop_run_executor": True,
        "runtime_root": str(root),
        "max_loop_steps": max_loop_steps,
    }


def _loop_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_LOOP_RUN_EXECUTOR_LICENSE_READY",
        "coordinator_run_allowed": True,
        "step_executor_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _external_context(root: pathlib.Path, dispatch_target: str | None = None) -> dict[str, Any]:
    value = {
        "qi_github_actions_external_cycle_runner_enabled": True,
        "apply_github_actions_external_cycle_runner": True,
        "runtime_root": str(root),
    }
    if dispatch_target:
        value["dispatch_target"] = dispatch_target
    return value


def _external_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_EXTERNAL_CYCLE_RUNNER_LICENSE_READY",
        "resolver_run_allowed": True,
        "dispatcher_run_allowed": True,
        "collector_run_allowed": True,
        "adapter_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _record(index: int, phase: str, result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "index": index,
        "phase": phase,
        "status": str(result.get("status", "unknown")),
        "stop_reason": str(result.get("stop_reason", "unknown")),
        "digest": _sha(dict(result)),
        "blockers": list(result.get("blockers", [])) if isinstance(result.get("blockers", []), list) else [],
        "epoch": int(time.time()),
    }


def _has_external_result(root: pathlib.Path) -> bool:
    names = [
        "qi_github_actions_external_call_raw_result_packet.json",
        "qi_github_actions_dispatch_commit_workflow_runs_result.json",
        "qi_github_actions_dispatch_workflow_run_jobs_result.json",
        "qi_github_actions_dispatch_workflow_job_steps_result.json",
        "qi_github_actions_dispatch_workflow_job_logs_result.json",
        "qi_github_actions_dispatch_workflow_run_artifacts_result.json",
        "qi_github_actions_dispatch_rerun_failed_workflow_run_jobs_result.json",
        "qi_github_actions_dispatch_rerun_workflow_job_result.json",
        "qi_github_actions_dispatch_merge_pull_request_result.json",
    ]
    return any(_exists(root, name) for name in names)


def _has_external_wait(root: pathlib.Path) -> bool:
    names = [
        "qi_github_actions_status_reobserve_request.json",
        "qi_github_actions_connector_execution_request.json",
        "qi_github_actions_observation_connector_request.json",
        "qi_github_actions_external_call_packet.json",
    ]
    return any(_exists(root, name) for name in names)


def build_qi_github_actions_full_cycle_orchestrator(*, runtime_context: Mapping[str, Any], full_cycle_orchestrator_license: Mapping[str, Any]) -> QiGitHubActionsFullCycleOrchestratorResult:
    ctx = _m(runtime_context)
    lic = _m(full_cycle_orchestrator_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_full_cycle_orchestrator_receipt.json"
    audit_path = root / "qi_github_actions_full_cycle_orchestrator_audit.jsonl"

    if ctx.get("qi_github_actions_full_cycle_orchestrator_enabled") is not True:
        blockers.append("qi_github_actions_full_cycle_orchestrator_enabled_not_true")
    if ctx.get("apply_github_actions_full_cycle_orchestrator") is not True:
        blockers.append("apply_github_actions_full_cycle_orchestrator_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_FULL_CYCLE_ORCHESTRATOR_LICENSE_READY":
        blockers.append("github_actions_full_cycle_orchestrator_license_not_ready")
    for name in ["loop_run_allowed", "external_cycle_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    max_phases = _i(ctx.get("max_full_cycle_phases", 4), 4)
    max_loop_steps = _i(ctx.get("max_loop_steps_per_phase", 5), 5)
    if max_phases < 1:
        blockers.append("max_full_cycle_phases_invalid")
        max_phases = 0
    if max_phases > 20:
        warnings.append("max_full_cycle_phases_capped_to_20")
        max_phases = 20
    if max_loop_steps < 1:
        blockers.append("max_loop_steps_per_phase_invalid")
        max_loop_steps = 0

    phase_records: list[dict[str, Any]] = []
    stop_reason = "not_run"
    final_phase = "unknown"
    if not blockers:
        stop_reason = "max_phases_reached"
        for index in range(1, max_phases + 1):
            if _has_external_result(root):
                final_phase = "external_cycle"
                ext = build_qi_github_actions_external_cycle_runner(
                    runtime_context=_external_context(root, str(ctx.get("dispatch_target", "")) or None),
                    external_cycle_runner_license=_external_license(),
                ).to_dict()
                phase_records.append(_record(index, final_phase, ext))
                if ext.get("status") != "QI_GITHUB_ACTIONS_EXTERNAL_CYCLE_RUNNER_READY":
                    blockers.append("external_cycle_not_ready")
                    stop_reason = "external_cycle_blocked"
                    break
                if ext.get("stop_reason") == "adapted_result_ready":
                    stop_reason = "external_result_adapted"
                    continue
                stop_reason = str(ext.get("stop_reason", "external_cycle_stopped"))
                break

            loop = build_qi_github_actions_loop_run_executor(
                runtime_context=_loop_context(root, max_loop_steps),
                loop_run_executor_license=_loop_license(),
            ).to_dict()
            final_phase = "loop_run"
            phase_records.append(_record(index, final_phase, loop))
            if loop.get("status") != "QI_GITHUB_ACTIONS_LOOP_RUN_EXECUTOR_READY":
                blockers.append("loop_run_not_ready")
                stop_reason = "loop_run_blocked"
                break
            loop_stop = str(loop.get("stop_reason", "unknown"))
            if loop_stop in {"waiting_for_connector_operation", "waiting_for_external_observation"} or _has_external_wait(root):
                final_phase = "external_cycle"
                ext = build_qi_github_actions_external_cycle_runner(
                    runtime_context=_external_context(root, str(ctx.get("dispatch_target", "")) or None),
                    external_cycle_runner_license=_external_license(),
                ).to_dict()
                phase_records.append(_record(index, final_phase, ext))
                if ext.get("status") != "QI_GITHUB_ACTIONS_EXTERNAL_CYCLE_RUNNER_READY":
                    blockers.append("external_cycle_not_ready")
                    stop_reason = "external_cycle_blocked"
                    break
                stop_reason = str(ext.get("stop_reason", "unknown"))
                if stop_reason == "await_dispatch_result":
                    break
                if stop_reason == "adapted_result_ready":
                    continue
                break
            stop_reason = loop_stop
            break

    status = "QI_GITHUB_ACTIONS_FULL_CYCLE_ORCHESTRATOR_READY" if not blockers else "QI_GITHUB_ACTIONS_FULL_CYCLE_ORCHESTRATOR_BLOCKED"
    packet_id = "qi-github-actions-full-cycle-" + _sha({"records": phase_records, "stop": stop_reason, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_full_cycle_orchestrator_v6_8",
        "status": status,
        "packet_id": packet_id,
        "phases_run": len(phase_records),
        "stop_reason": stop_reason,
        "final_phase": final_phase,
        "phase_records": phase_records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsFullCycleOrchestratorResult(
        "kuuos_runtime_daemon_qi_github_actions_full_cycle_orchestrator_v6_8",
        status,
        packet_id,
        str(root),
        len(phase_records),
        stop_reason,
        final_phase,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
        phase_records,
    )
