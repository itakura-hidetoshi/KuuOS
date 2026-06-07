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
from runtime.kuuos_runtime_daemon_qi_github_actions_external_bridge_executor_v6_7 import build_qi_github_actions_external_bridge_executor


EXTERNAL_TERMINALS = {
    "await_dispatch_result",
    "await_external_call",
}

INTERNAL_WAIT_STOP_REASONS = {
    "waiting_for_connector_operation",
    "waiting_for_external_observation",
}


@dataclass(frozen=True)
class QiGitHubActionsIntegratedBridgeRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    cycles_run: int
    stop_reason: str
    final_internal_stage: str
    final_external_stage: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]
    cycle_records: list[dict[str, Any]]

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


def _external_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_external_bridge_executor_enabled": True,
        "apply_github_actions_external_bridge_executor": True,
        "runtime_root": str(root),
    }


def _external_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_EXTERNAL_BRIDGE_EXECUTOR_LICENSE_READY",
        "external_bridge_state_read_allowed": True,
        "local_external_stage_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "allow_external_wait_resolve_stage": True,
        "allow_external_call_dispatch_stage": True,
        "allow_dispatch_result_collect_stage": True,
        "allow_external_result_adapt_stage": True,
        "allow_await_dispatch_result_stage": True,
        "allow_await_external_call_stage": True,
    }


def _record(index: int, internal: Mapping[str, Any], external: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "index": index,
        "internal_status": str(internal.get("status", "unknown")),
        "internal_stop_reason": str(internal.get("stop_reason", "unknown")),
        "internal_final_stage": str(internal.get("final_stage", "unknown")),
        "external_status": str(external.get("status", "not_run")) if external else "not_run",
        "external_selected_stage": str(external.get("selected_stage", "not_run")) if external else "not_run",
        "external_stage_result_class": str(external.get("stage_result_class", "not_run")) if external else "not_run",
        "internal_digest": _sha(dict(internal)),
        "external_digest": _sha(dict(external)) if external else "",
        "epoch": int(time.time()),
    }


def build_qi_github_actions_integrated_bridge_runner(*, runtime_context: Mapping[str, Any], integrated_bridge_runner_license: Mapping[str, Any]) -> QiGitHubActionsIntegratedBridgeRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(integrated_bridge_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_integrated_bridge_runner_receipt.json"
    audit_path = root / "qi_github_actions_integrated_bridge_runner_audit.jsonl"

    if ctx.get("qi_github_actions_integrated_bridge_runner_enabled") is not True:
        blockers.append("qi_github_actions_integrated_bridge_runner_enabled_not_true")
    if ctx.get("apply_github_actions_integrated_bridge_runner") is not True:
        blockers.append("apply_github_actions_integrated_bridge_runner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_LICENSE_READY":
        blockers.append("github_actions_integrated_bridge_runner_license_not_ready")
    for name in ["internal_loop_run_allowed", "external_bridge_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    max_cycles = _i(ctx.get("max_bridge_cycles", 5), 5)
    if max_cycles < 1:
        blockers.append("max_bridge_cycles_invalid")
        max_cycles = 0
    if max_cycles > 20:
        warnings.append("max_bridge_cycles_capped_to_20")
        max_cycles = 20
    max_loop_steps = _i(ctx.get("max_loop_steps_per_cycle", 5), 5)
    if max_loop_steps < 1:
        blockers.append("max_loop_steps_per_cycle_invalid")
        max_loop_steps = 1

    records: list[dict[str, Any]] = []
    stop_reason = "not_run"
    final_internal_stage = "unknown"
    final_external_stage = "unknown"
    if not blockers:
        stop_reason = "max_bridge_cycles_reached"
        for index in range(1, max_cycles + 1):
            internal = build_qi_github_actions_loop_run_executor(
                runtime_context=_loop_context(root, max_loop_steps),
                loop_run_executor_license=_loop_license(),
            ).to_dict()
            final_internal_stage = str(internal.get("final_stage", "unknown"))
            if internal.get("status") != "QI_GITHUB_ACTIONS_LOOP_RUN_EXECUTOR_READY":
                blockers.append("internal_loop_not_ready")
                stop_reason = "internal_loop_blocked"
                records.append(_record(index, internal, {}))
                break
            if str(internal.get("stop_reason", "")) not in INTERNAL_WAIT_STOP_REASONS:
                stop_reason = str(internal.get("stop_reason", "unknown"))
                records.append(_record(index, internal, {}))
                break
            external = build_qi_github_actions_external_bridge_executor(
                runtime_context=_external_context(root),
                external_bridge_executor_license=_external_license(),
            ).to_dict()
            final_external_stage = str(external.get("selected_stage", "unknown"))
            records.append(_record(index, internal, external))
            if external.get("status") != "QI_GITHUB_ACTIONS_EXTERNAL_BRIDGE_EXECUTOR_READY":
                blockers.append("external_bridge_not_ready")
                stop_reason = "external_bridge_blocked"
                break
            stage = str(external.get("selected_stage", "unknown"))
            if stage in EXTERNAL_TERMINALS:
                stop_reason = stage
                break
            if external.get("stage_result_class") != "local_external_stage_completed":
                blockers.append("external_stage_result_unknown")
                stop_reason = "external_stage_result_unknown"
                break

    status = "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_READY" if not blockers else "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_BLOCKED"
    packet_id = "qi-github-actions-integrated-bridge-" + _sha({"records": records, "stop": stop_reason, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_integrated_bridge_runner_v6_8",
        "status": status,
        "packet_id": packet_id,
        "cycles_run": len(records),
        "stop_reason": stop_reason,
        "final_internal_stage": final_internal_stage,
        "final_external_stage": final_external_stage,
        "cycle_records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsIntegratedBridgeRunnerResult(
        "kuuos_runtime_daemon_qi_github_actions_integrated_bridge_runner_v6_8",
        status,
        packet_id,
        str(root),
        len(records),
        stop_reason,
        final_internal_stage,
        final_external_stage,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
        records,
    )
