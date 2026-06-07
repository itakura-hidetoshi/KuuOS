#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

STATE_TO_OUTPUT = {
    "scheduler_cycle_closed": ("qi_github_actions_terminal_cycle_closed_packet.json", "cycle_closed_final"),
    "external_dispatch_ready": ("qi_github_actions_terminal_external_dispatch_packet.json", "external_dispatch_ready"),
    "blockers_surface_ready": ("qi_github_actions_terminal_blockers_packet.json", "blockers_ready"),
    "hold_for_review_ready": ("qi_github_actions_terminal_hold_packet.json", "hold_ready"),
    "continue_supercycle_ready": ("qi_github_actions_terminal_continue_packet.json", "continue_ready"),
}

@dataclass(frozen=True)
class QiGitHubActionsTerminalExecutionBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    execution_state: str
    output_state: str
    output_packet_path: str
    receipt_path: str
    audit_path: str
    output_packet_written: bool
    blockers: list[str]
    warnings: list[str]
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(v: Any) -> Mapping[str, Any]:
    return v if isinstance(v, Mapping) else {}


def _sha(v: Any) -> str:
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


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


def _validate(exec_packet: Mapping[str, Any], dispatch_packet: Mapping[str, Any], blockers: list[str]) -> str:
    if exec_packet.get("terminal_scheduler_execution_allowed") is not True:
        blockers.append("terminal_scheduler_execution_allowed_not_true")
    state = str(exec_packet.get("execution_state", ""))
    if state not in STATE_TO_OUTPUT:
        blockers.append("execution_state_not_allowlisted")
    if state == "external_dispatch_ready":
        if not dispatch_packet:
            blockers.append("unified_dispatch_packet_missing_for_external_dispatch")
        elif dispatch_packet.get("dispatch_allowed") is not True:
            blockers.append("unified_dispatch_allowed_not_true")
        elif str(dispatch_packet.get("connector_action", "")) != str(exec_packet.get("connector_action", "")):
            blockers.append("dispatch_connector_action_mismatch")
    return state


def _base(exec_packet: Mapping[str, Any], state: str, output_state: str) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_terminal_execution_output_packet_v11_1",
        "terminal_execution_output_allowed": True,
        "execution_state": state,
        "output_state": output_state,
        "scheduler_action": str(exec_packet.get("scheduler_action", "none")),
        "connector_action": str(exec_packet.get("connector_action", "none")),
        "action_prepared": str(exec_packet.get("action_prepared", "none")),
        "source_execution_digest": _sha(dict(exec_packet)),
        "boundary": {
            "terminal_output_packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "does_not_apply_policy_action": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def _output(exec_packet: Mapping[str, Any], dispatch_packet: Mapping[str, Any], state: str, output_state: str) -> dict[str, Any]:
    packet = _base(exec_packet, state, output_state)
    if state == "external_dispatch_ready":
        packet.update({
            "dispatch_allowed": True,
            "dispatch_kind": dispatch_packet.get("dispatch_kind"),
            "connector_payload": dict(_m(dispatch_packet.get("connector_payload"))),
            "raw_result_expected_file": dispatch_packet.get("raw_result_expected_file"),
            "source_dispatch_digest": _sha(dict(dispatch_packet)),
        })
    elif state == "blockers_surface_ready":
        packet["blocker_surface"] = {"source_kind": exec_packet.get("source_kind"), "terminal_kind": exec_packet.get("terminal_kind")}
    elif state == "hold_for_review_ready":
        packet["review_surface"] = {"source_kind": exec_packet.get("source_kind"), "terminal_kind": exec_packet.get("terminal_kind")}
    elif state == "continue_supercycle_ready":
        packet["next_runner"] = "kuuos_runtime_daemon_qi_github_actions_full_terminal_autopilot_v11_0"
    elif state == "scheduler_cycle_closed":
        packet["closed"] = True
    return packet


def build_qi_github_actions_terminal_execution_bridge(*, runtime_context: Mapping[str, Any], terminal_execution_bridge_license: Mapping[str, Any]) -> QiGitHubActionsTerminalExecutionBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(terminal_execution_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    exec_path = root / "qi_github_actions_terminal_scheduler_execution_packet.json"
    dispatch_path = root / "qi_github_actions_unified_dispatch_packet.json"
    receipt_path = root / "qi_github_actions_terminal_execution_bridge_receipt.json"
    audit_path = root / "qi_github_actions_terminal_execution_bridge_audit.jsonl"

    if ctx.get("qi_github_actions_terminal_execution_bridge_enabled") is not True:
        blockers.append("qi_github_actions_terminal_execution_bridge_enabled_not_true")
    if ctx.get("apply_github_actions_terminal_execution_bridge") is not True:
        blockers.append("apply_github_actions_terminal_execution_bridge_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_TERMINAL_EXECUTION_BRIDGE_LICENSE_READY":
        blockers.append("github_actions_terminal_execution_bridge_license_not_ready")
    for name in ["terminal_execution_packet_read_allowed", "dispatch_packet_read_allowed", "output_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    exec_packet = _read(exec_path)
    if not exec_packet:
        blockers.append("terminal_execution_packet_missing_or_invalid")
    dispatch_packet = _read(dispatch_path)
    state = _validate(exec_packet, dispatch_packet, blockers) if exec_packet else "blocked"
    output_file, output_state = STATE_TO_OUTPUT.get(state, ("qi_github_actions_terminal_execution_blocked_packet.json", "blocked"))
    output_path = root / output_file
    packet: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _output(exec_packet, dispatch_packet, state, output_state)
        _write(output_path, packet)
        written = True

    status = "QI_GITHUB_ACTIONS_TERMINAL_EXECUTION_BRIDGE_READY" if not blockers else "QI_GITHUB_ACTIONS_TERMINAL_EXECUTION_BRIDGE_BLOCKED"
    packet_id = "qi-github-actions-terminal-execution-bridge-" + _sha({"exec": exec_packet, "dispatch": dispatch_packet, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_github_actions_terminal_execution_bridge_v11_1", "status": status, "packet_id": packet_id, "execution_state": state, "output_state": output_state, "output_packet_path": str(output_path), "output_packet_written": written, "output_packet_digest": _sha(packet), "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsTerminalExecutionBridgeResult("kuuos_runtime_daemon_qi_github_actions_terminal_execution_bridge_v11_1", status, packet_id, str(root), state, output_state, str(output_path), str(receipt_path), str(audit_path), written, blockers, warnings)
