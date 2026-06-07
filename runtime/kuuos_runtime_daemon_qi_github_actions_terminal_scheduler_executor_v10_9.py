#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

ACTIONS = {
    "close_scheduler_cycle": "scheduler_cycle_closed",
    "dispatch_external_connector": "external_dispatch_ready",
    "surface_blockers": "blockers_surface_ready",
    "hold_for_review": "hold_for_review_ready",
    "continue_supercycle": "continue_supercycle_ready",
}

@dataclass(frozen=True)
class QiGitHubActionsTerminalSchedulerExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    scheduler_action: str
    execution_state: str
    connector_action: str
    execution_packet_path: str
    receipt_path: str
    audit_path: str
    execution_packet_written: bool
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


def _validate(packet: Mapping[str, Any], blockers: list[str]) -> str:
    if packet.get("scheduler_packet_allowed") is not True:
        blockers.append("scheduler_packet_allowed_not_true")
    action = str(packet.get("scheduler_action", ""))
    if action not in ACTIONS:
        blockers.append("scheduler_action_not_allowlisted")
    if action == "dispatch_external_connector" and str(packet.get("connector_action", "none")) in {"", "none"}:
        blockers.append("connector_action_missing_for_dispatch")
    return action


def _execution_packet(packet: Mapping[str, Any], action: str) -> dict[str, Any]:
    state = ACTIONS[action]
    connector = str(packet.get("connector_action", "none"))
    return {
        "version": "qi_github_actions_terminal_scheduler_execution_packet_v10_9",
        "terminal_scheduler_execution_allowed": True,
        "scheduler_action": action,
        "execution_state": state,
        "terminal_state": str(packet.get("terminal_state", "unknown")),
        "terminal_kind": str(packet.get("terminal_kind", "unknown")),
        "connector_action": connector,
        "action_prepared": str(packet.get("action_prepared", "none")),
        "source_kind": str(packet.get("source_kind", "unknown")),
        "source_scheduler_digest": _sha(dict(packet)),
        "boundary": {
            "execution_packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "does_not_apply_policy_action": True,
            "does_not_mutate_scheduler_source": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_terminal_scheduler_executor(*, runtime_context: Mapping[str, Any], terminal_scheduler_executor_license: Mapping[str, Any]) -> QiGitHubActionsTerminalSchedulerExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(terminal_scheduler_executor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    scheduler_path = root / "qi_github_actions_terminal_scheduler_packet.json"
    execution_path = root / "qi_github_actions_terminal_scheduler_execution_packet.json"
    receipt_path = root / "qi_github_actions_terminal_scheduler_executor_receipt.json"
    audit_path = root / "qi_github_actions_terminal_scheduler_executor_audit.jsonl"

    if ctx.get("qi_github_actions_terminal_scheduler_executor_enabled") is not True:
        blockers.append("qi_github_actions_terminal_scheduler_executor_enabled_not_true")
    if ctx.get("apply_github_actions_terminal_scheduler_executor") is not True:
        blockers.append("apply_github_actions_terminal_scheduler_executor_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_TERMINAL_SCHEDULER_EXECUTOR_LICENSE_READY":
        blockers.append("github_actions_terminal_scheduler_executor_license_not_ready")
    for name in ["scheduler_packet_read_allowed", "execution_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read(scheduler_path)
    if not packet:
        blockers.append("scheduler_packet_missing_or_invalid")
    action = _validate(packet, blockers) if packet else "none"
    execution: dict[str, Any] = {}
    written = False
    if not blockers:
        execution = _execution_packet(packet, action)
        _write(execution_path, execution)
        written = True
    state = str(execution.get("execution_state", "blocked"))
    connector = str(execution.get("connector_action", packet.get("connector_action", "none") if packet else "none"))
    status = "QI_GITHUB_ACTIONS_TERMINAL_SCHEDULER_EXECUTOR_READY" if not blockers else "QI_GITHUB_ACTIONS_TERMINAL_SCHEDULER_EXECUTOR_BLOCKED"
    packet_id = "qi-github-actions-terminal-scheduler-executor-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_terminal_scheduler_executor_v10_9",
        "status": status,
        "packet_id": packet_id,
        "scheduler_action": action,
        "execution_state": state,
        "connector_action": connector,
        "execution_packet_written": written,
        "execution_packet_digest": _sha(execution),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsTerminalSchedulerExecutorResult("kuuos_runtime_daemon_qi_github_actions_terminal_scheduler_executor_v10_9", status, packet_id, str(root), action, state, connector, str(execution_path), str(receipt_path), str(audit_path), written, blockers, warnings)
