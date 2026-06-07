#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_full_terminal_autopilot_v11_0 import build_qi_github_actions_full_terminal_autopilot
from runtime.kuuos_runtime_daemon_qi_github_actions_terminal_execution_bridge_v11_1 import build_qi_github_actions_terminal_execution_bridge

OUTPUT_FILES = [
    "qi_github_actions_terminal_cycle_closed_packet.json",
    "qi_github_actions_terminal_external_dispatch_packet.json",
    "qi_github_actions_terminal_blockers_packet.json",
    "qi_github_actions_terminal_hold_packet.json",
    "qi_github_actions_terminal_continue_packet.json",
]

@dataclass(frozen=True)
class QiGitHubActionsFullTerminalOutputResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    phases_run: int
    final_stage: str
    output_state: str
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


def _pick_output(root: pathlib.Path) -> tuple[str, dict[str, Any]]:
    for name in OUTPUT_FILES:
        packet = _read(root / name)
        if packet:
            return name, packet
    return "", {}


def _autopilot_ctx(root: pathlib.Path, ctx: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "qi_github_actions_full_terminal_autopilot_enabled": True,
        "apply_github_actions_full_terminal_autopilot": True,
        "runtime_root": str(root),
        "max_full_terminal_autopilot_phases": _i(ctx.get("max_inner_full_terminal_autopilot_phases"), 6),
        "max_inner_dispatch_supercycle_phases": _i(ctx.get("max_inner_dispatch_supercycle_phases"), 8),
        "max_inner_unified_closed_loop_phases": _i(ctx.get("max_inner_unified_closed_loop_phases"), 6),
    }


def _autopilot_lic() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_FULL_TERMINAL_AUTOPILOT_LICENSE_READY", "dispatch_supercycle_run_allowed": True, "terminal_finalizer_run_allowed": True, "terminal_scheduler_executor_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _bridge_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_terminal_execution_bridge_enabled": True, "apply_github_actions_terminal_execution_bridge": True, "runtime_root": str(root)}


def _bridge_lic() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_TERMINAL_EXECUTION_BRIDGE_LICENSE_READY", "terminal_execution_packet_read_allowed": True, "dispatch_packet_read_allowed": True, "output_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _record(i: int, stage: str, r: Mapping[str, Any]) -> dict[str, Any]:
    return {"index": i, "stage": stage, "status": str(r.get("status", "unknown")), "output_state": str(r.get("output_state", "unknown")), "execution_state": str(r.get("execution_state", "unknown")), "connector_action": str(r.get("connector_action", "none")), "digest": _sha(dict(r)), "blockers": list(r.get("blockers", [])) if isinstance(r.get("blockers", []), list) else [], "epoch": int(time.time())}


def build_qi_github_actions_full_terminal_output(*, runtime_context: Mapping[str, Any], full_terminal_output_license: Mapping[str, Any]) -> QiGitHubActionsFullTerminalOutputResult:
    ctx = _m(runtime_context)
    lic = _m(full_terminal_output_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_full_terminal_output_receipt.json"
    audit_path = root / "qi_github_actions_full_terminal_output_audit.jsonl"

    if ctx.get("qi_github_actions_full_terminal_output_enabled") is not True:
        blockers.append("qi_github_actions_full_terminal_output_enabled_not_true")
    if ctx.get("apply_github_actions_full_terminal_output") is not True:
        blockers.append("apply_github_actions_full_terminal_output_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_FULL_TERMINAL_OUTPUT_LICENSE_READY":
        blockers.append("github_actions_full_terminal_output_license_not_ready")
    for name in ["full_terminal_autopilot_run_allowed", "terminal_execution_bridge_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    max_phases = _i(ctx.get("max_full_terminal_output_phases"), 5)
    if max_phases < 1:
        blockers.append("max_full_terminal_output_phases_invalid")
        max_phases = 0

    records: list[dict[str, Any]] = []
    final_stage = "not_run"
    output_state = "not_run"
    execution_state = "none"
    connector = "none"
    stop = "not_run"
    if not blockers:
        stop = "max_phases_reached"
        for i in range(1, min(max_phases, 40) + 1):
            output_name, output_packet = _pick_output(root)
            if output_packet:
                final_stage = "terminal_output_present"
                output_state = str(output_packet.get("output_state", "unknown"))
                execution_state = str(output_packet.get("execution_state", "unknown"))
                connector = str(output_packet.get("connector_action", "none"))
                stop = "terminal_output_ready"
                break
            if _exists(root, "qi_github_actions_terminal_scheduler_execution_packet.json"):
                final_stage = "run_terminal_execution_bridge"
                r = build_qi_github_actions_terminal_execution_bridge(runtime_context=_bridge_ctx(root), terminal_execution_bridge_license=_bridge_lic()).to_dict()
            else:
                final_stage = "run_full_terminal_autopilot"
                r = build_qi_github_actions_full_terminal_autopilot(runtime_context=_autopilot_ctx(root, ctx), full_terminal_autopilot_license=_autopilot_lic()).to_dict()
            records.append(_record(i, final_stage, r))
            if not str(r.get("status", "")).endswith("READY"):
                blockers.append(f"{final_stage}_not_ready")
                stop = f"{final_stage}_blocked"
                break
            output_state = str(r.get("output_state", output_state))
            execution_state = str(r.get("execution_state", execution_state))
            connector = str(r.get("connector_action", connector))
            stop = str(r.get("stop_reason", output_state))
            continue
    status = "QI_GITHUB_ACTIONS_FULL_TERMINAL_OUTPUT_READY" if not blockers else "QI_GITHUB_ACTIONS_FULL_TERMINAL_OUTPUT_BLOCKED"
    packet_id = "qi-github-actions-full-terminal-output-" + _sha({"records": records, "blockers": blockers, "output_state": output_state})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_github_actions_full_terminal_output_v11_2", "status": status, "packet_id": packet_id, "phases_run": len(records), "final_stage": final_stage, "output_state": output_state, "execution_state": execution_state, "connector_action": connector, "stop_reason": stop, "phase_records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsFullTerminalOutputResult("kuuos_runtime_daemon_qi_github_actions_full_terminal_output_v11_2", status, packet_id, str(root), len(records), final_stage, output_state, execution_state, connector, stop, str(receipt_path), str(audit_path), blockers, warnings, records)
