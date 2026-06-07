#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_dispatch_supercycle_v10_7 import build_qi_github_actions_dispatch_supercycle
from runtime.kuuos_runtime_daemon_qi_github_actions_terminal_finalizer_v10_8 import build_qi_github_actions_terminal_finalizer
from runtime.kuuos_runtime_daemon_qi_github_actions_terminal_scheduler_executor_v10_9 import build_qi_github_actions_terminal_scheduler_executor

TERMINAL_SOURCES = [
    "qi_github_actions_policy_action_final_receipt_packet.json",
    "qi_github_actions_next_cycle_closure_packet.json",
    "qi_github_actions_dispatch_supercycle_receipt.json",
    "qi_github_actions_unified_closed_loop_receipt.json",
    "qi_github_actions_closed_loop_supercycle_receipt.json",
    "qi_github_actions_reentry_merge_supercycle_receipt.json",
]

@dataclass(frozen=True)
class QiGitHubActionsFullTerminalAutopilotResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    phases_run: int
    final_stage: str
    autopilot_state: str
    scheduler_action: str
    execution_state: str
    connector_action: str
    stop_reason: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]
    phase_records: list[dict[str, Any]]
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(v: Any) -> Mapping[str, Any]:
    return v if isinstance(v, Mapping) else {}


def _sha(v: Any) -> str:
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _i(v: Any, d: int) -> int:
    if isinstance(v, bool):
        return d
    try:
        return int(v)
    except (TypeError, ValueError):
        return d


def _root(v: Any, blockers: list[str]) -> pathlib.Path:
    if not v:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(v)).expanduser().resolve()
    if str(root) == "/":
        blockers.append("runtime_root_forbidden")
    return root


def _read(p: pathlib.Path) -> dict[str, Any]:
    if not p.is_file():
        return {}
    try:
        v = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return v if isinstance(v, dict) else {}


def _write(p: pathlib.Path, payload: Mapping[str, Any]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, p)


def _append(p: pathlib.Path, payload: Mapping[str, Any]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _exists(root: pathlib.Path, name: str) -> bool:
    p = root / name
    return p.is_file() and p.stat().st_size > 2


def _has_terminal_source(root: pathlib.Path) -> bool:
    return any(_exists(root, name) for name in TERMINAL_SOURCES)


def _dispatch_ctx(root: pathlib.Path, ctx: Mapping[str, Any]) -> dict[str, Any]:
    return {"qi_github_actions_dispatch_supercycle_enabled": True, "apply_github_actions_dispatch_supercycle": True, "runtime_root": str(root), "max_dispatch_supercycle_phases": _i(ctx.get("max_inner_dispatch_supercycle_phases"), 8), "max_inner_unified_closed_loop_phases": _i(ctx.get("max_inner_unified_closed_loop_phases"), 6)}


def _dispatch_lic() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_DISPATCH_SUPERCYCLE_LICENSE_READY", "unified_closed_loop_run_allowed": True, "dispatch_router_run_allowed": True, "dispatch_result_router_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _finalizer_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_terminal_finalizer_enabled": True, "apply_github_actions_terminal_finalizer": True, "runtime_root": str(root)}


def _finalizer_lic() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_TERMINAL_FINALIZER_LICENSE_READY", "terminal_source_read_allowed": True, "scheduler_packet_write_allowed": True, "terminal_receipt_write_allowed": True, "audit_append_allowed": True}


def _executor_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_terminal_scheduler_executor_enabled": True, "apply_github_actions_terminal_scheduler_executor": True, "runtime_root": str(root)}


def _executor_lic() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_TERMINAL_SCHEDULER_EXECUTOR_LICENSE_READY", "scheduler_packet_read_allowed": True, "execution_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _record(i: int, stage: str, r: Mapping[str, Any]) -> dict[str, Any]:
    return {"index": i, "stage": stage, "status": str(r.get("status", "unknown")), "state": str(r.get("autopilot_state", r.get("supercycle_state", r.get("terminal_state", r.get("execution_state", "unknown"))))), "scheduler_action": str(r.get("scheduler_action", "none")), "execution_state": str(r.get("execution_state", "none")), "connector_action": str(r.get("connector_action", "none")), "digest": _sha(dict(r)), "blockers": list(r.get("blockers", [])) if isinstance(r.get("blockers", []), list) else [], "epoch": int(time.time())}


def build_qi_github_actions_full_terminal_autopilot(*, runtime_context: Mapping[str, Any], full_terminal_autopilot_license: Mapping[str, Any]) -> QiGitHubActionsFullTerminalAutopilotResult:
    ctx = _m(runtime_context)
    lic = _m(full_terminal_autopilot_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_full_terminal_autopilot_receipt.json"
    audit_path = root / "qi_github_actions_full_terminal_autopilot_audit.jsonl"
    if ctx.get("qi_github_actions_full_terminal_autopilot_enabled") is not True:
        blockers.append("qi_github_actions_full_terminal_autopilot_enabled_not_true")
    if ctx.get("apply_github_actions_full_terminal_autopilot") is not True:
        blockers.append("apply_github_actions_full_terminal_autopilot_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_FULL_TERMINAL_AUTOPILOT_LICENSE_READY":
        blockers.append("github_actions_full_terminal_autopilot_license_not_ready")
    for name in ["dispatch_supercycle_run_allowed", "terminal_finalizer_run_allowed", "terminal_scheduler_executor_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    max_phases = _i(ctx.get("max_full_terminal_autopilot_phases"), 6)
    if max_phases < 1:
        blockers.append("max_full_terminal_autopilot_phases_invalid")
        max_phases = 0
    records: list[dict[str, Any]] = []
    stage = "not_run"
    state = "not_run"
    scheduler_action = "none"
    execution_state = "none"
    connector = "none"
    stop = "not_run"
    if not blockers:
        stop = "max_phases_reached"
        for i in range(1, min(max_phases, 40) + 1):
            if _exists(root, "qi_github_actions_terminal_scheduler_execution_packet.json"):
                p = _read(root / "qi_github_actions_terminal_scheduler_execution_packet.json")
                stage = "terminal_execution_present"
                state = "terminal_execution_ready"
                scheduler_action = str(p.get("scheduler_action", "none"))
                execution_state = str(p.get("execution_state", "unknown"))
                connector = str(p.get("connector_action", "none"))
                stop = "terminal_execution_ready"
                break
            if _exists(root, "qi_github_actions_terminal_scheduler_packet.json"):
                stage = "run_terminal_scheduler_executor"
                r = build_qi_github_actions_terminal_scheduler_executor(runtime_context=_executor_ctx(root), terminal_scheduler_executor_license=_executor_lic()).to_dict()
            elif _has_terminal_source(root):
                stage = "run_terminal_finalizer"
                r = build_qi_github_actions_terminal_finalizer(runtime_context=_finalizer_ctx(root), terminal_finalizer_license=_finalizer_lic()).to_dict()
            else:
                stage = "run_dispatch_supercycle"
                r = build_qi_github_actions_dispatch_supercycle(runtime_context=_dispatch_ctx(root, ctx), dispatch_supercycle_license=_dispatch_lic()).to_dict()
            records.append(_record(i, stage, r))
            if not str(r.get("status", "")).endswith("READY"):
                blockers.append(f"{stage}_not_ready")
                stop = f"{stage}_blocked"
                break
            state = str(r.get("supercycle_state", r.get("terminal_state", r.get("execution_state", "unknown"))))
            scheduler_action = str(r.get("scheduler_action", scheduler_action))
            execution_state = str(r.get("execution_state", execution_state))
            connector = str(r.get("connector_action", connector))
            stop = str(r.get("stop_reason", state))
            continue
    status = "QI_GITHUB_ACTIONS_FULL_TERMINAL_AUTOPILOT_READY" if not blockers else "QI_GITHUB_ACTIONS_FULL_TERMINAL_AUTOPILOT_BLOCKED"
    packet_id = "qi-github-actions-full-terminal-autopilot-" + _sha({"records": records, "blockers": blockers, "state": state})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_github_actions_full_terminal_autopilot_v11_0", "status": status, "packet_id": packet_id, "phases_run": len(records), "final_stage": stage, "autopilot_state": state, "scheduler_action": scheduler_action, "execution_state": execution_state, "connector_action": connector, "stop_reason": stop, "phase_records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsFullTerminalAutopilotResult("kuuos_runtime_daemon_qi_github_actions_full_terminal_autopilot_v11_0", status, packet_id, str(root), len(records), stage, state, scheduler_action, execution_state, connector, stop, str(receipt_path), str(audit_path), blockers, warnings, records)
