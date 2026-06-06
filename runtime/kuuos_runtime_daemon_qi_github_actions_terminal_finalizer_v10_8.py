#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


TERMINAL_SOURCES = [
    ("final_receipt", "qi_github_actions_policy_action_final_receipt_packet.json"),
    ("closure", "qi_github_actions_next_cycle_closure_packet.json"),
    ("dispatch_supercycle", "qi_github_actions_dispatch_supercycle_receipt.json"),
    ("unified_closed_loop", "qi_github_actions_unified_closed_loop_receipt.json"),
    ("closed_loop", "qi_github_actions_closed_loop_supercycle_receipt.json"),
    ("reentry_merge", "qi_github_actions_reentry_merge_supercycle_receipt.json"),
]

AWAIT_STATES = {
    "await_dispatch_external_result",
    "await_next_cycle_external_result",
    "await_pr_info_external_result",
    "await_policy_action_external_result",
}

DONE_STATES = {"action_completed", "cycle_closed", "closed_loop_cycle_closed"}


@dataclass(frozen=True)
class QiGitHubActionsTerminalFinalizerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    terminal_state: str
    terminal_kind: str
    source_kind: str
    connector_action: str
    action_prepared: str
    scheduler_packet_path: str
    terminal_receipt_path: str
    audit_path: str
    scheduler_packet_written: bool
    terminal_receipt_written: bool
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


def _pick(root: pathlib.Path) -> tuple[str, str, dict[str, Any]]:
    for kind, name in TERMINAL_SOURCES:
        packet = _read(root / name)
        if packet:
            return kind, name, packet
    return "none", "", {}


def _state(kind: str, packet: Mapping[str, Any]) -> str:
    if kind == "final_receipt":
        return str(packet.get("final_state", "action_completed"))
    if kind == "closure":
        return "cycle_closed"
    return str(packet.get("supercycle_state") or packet.get("unified_state") or packet.get("terminal_state") or packet.get("stop_reason") or "unknown")


def _terminal_kind(state: str, packet: Mapping[str, Any]) -> str:
    if state in DONE_STATES:
        return "done"
    if state in AWAIT_STATES or str(packet.get("stop_reason", "")) in AWAIT_STATES:
        return "await_external"
    if packet.get("status", "").endswith("BLOCKED") or packet.get("blockers"):
        return "blocked"
    if "hold" in state:
        return "hold"
    return "open"


def _scheduler_action(kind: str, connector: str) -> str:
    if kind == "done":
        return "close_scheduler_cycle"
    if kind == "await_external":
        return "dispatch_external_connector"
    if kind == "blocked":
        return "surface_blockers"
    if kind == "hold":
        return "hold_for_review"
    return "continue_supercycle"


def _scheduler_packet(source_kind: str, source_file: str, source: Mapping[str, Any], terminal_state: str, terminal_kind: str, connector: str, action: str) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_terminal_scheduler_packet_v10_8",
        "scheduler_packet_allowed": True,
        "terminal_state": terminal_state,
        "terminal_kind": terminal_kind,
        "scheduler_action": _scheduler_action(terminal_kind, connector),
        "connector_action": connector,
        "action_prepared": action,
        "source_kind": source_kind,
        "source_file": source_file,
        "source_packet_digest": _sha(dict(source)),
        "boundary": {
            "scheduler_surface_only": True,
            "does_not_call_connector_inside_runtime": True,
            "does_not_apply_policy_action": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_terminal_finalizer(*, runtime_context: Mapping[str, Any], terminal_finalizer_license: Mapping[str, Any]) -> QiGitHubActionsTerminalFinalizerResult:
    ctx = _m(runtime_context)
    lic = _m(terminal_finalizer_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    scheduler_path = root / "qi_github_actions_terminal_scheduler_packet.json"
    terminal_path = root / "qi_github_actions_terminal_final_receipt.json"
    audit_path = root / "qi_github_actions_terminal_finalizer_audit.jsonl"

    if ctx.get("qi_github_actions_terminal_finalizer_enabled") is not True:
        blockers.append("qi_github_actions_terminal_finalizer_enabled_not_true")
    if ctx.get("apply_github_actions_terminal_finalizer") is not True:
        blockers.append("apply_github_actions_terminal_finalizer_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_TERMINAL_FINALIZER_LICENSE_READY":
        blockers.append("github_actions_terminal_finalizer_license_not_ready")
    for name in ["terminal_source_read_allowed", "scheduler_packet_write_allowed", "terminal_receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    source_kind, source_file, source = _pick(root)
    if not source:
        blockers.append("terminal_source_packet_missing_or_invalid")
    terminal_state = _state(source_kind, source) if source else "blocked"
    terminal_kind = _terminal_kind(terminal_state, source) if source else "blocked"
    connector = str(source.get("connector_action", "none")) if source else "none"
    action = str(source.get("action_prepared") or source.get("action_kind") or "none") if source else "none"
    scheduler: dict[str, Any] = {}
    terminal: dict[str, Any] = {}
    scheduler_written = False
    terminal_written = False

    if not blockers:
        scheduler = _scheduler_packet(source_kind, source_file, source, terminal_state, terminal_kind, connector, action)
        terminal = {
            "version": "qi_github_actions_terminal_final_receipt_v10_8",
            "terminal_receipt_allowed": True,
            "terminal_state": terminal_state,
            "terminal_kind": terminal_kind,
            "connector_action": connector,
            "action_prepared": action,
            "scheduler_action": scheduler["scheduler_action"],
            "source_kind": source_kind,
            "source_file": source_file,
            "source_packet_digest": _sha(dict(source)),
            "blockers": list(source.get("blockers", [])) if isinstance(source.get("blockers", []), list) else [],
            "warnings": list(source.get("warnings", [])) if isinstance(source.get("warnings", []), list) else [],
            "epoch": int(time.time()),
        }
        _write(scheduler_path, scheduler)
        _write(terminal_path, terminal)
        scheduler_written = True
        terminal_written = True

    status = "QI_GITHUB_ACTIONS_TERMINAL_FINALIZER_READY" if not blockers else "QI_GITHUB_ACTIONS_TERMINAL_FINALIZER_BLOCKED"
    packet_id = "qi-github-actions-terminal-finalizer-" + _sha({"source": source, "state": terminal_state, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_terminal_finalizer_v10_8",
        "status": status,
        "packet_id": packet_id,
        "terminal_state": terminal_state,
        "terminal_kind": terminal_kind,
        "source_kind": source_kind,
        "connector_action": connector,
        "action_prepared": action,
        "scheduler_packet_written": scheduler_written,
        "terminal_receipt_written": terminal_written,
        "scheduler_packet_digest": _sha(scheduler),
        "terminal_receipt_digest": _sha(terminal),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("terminal_receipt_write_allowed") is True:
        _write(root / "qi_github_actions_terminal_finalizer_receipt.json", receipt)
    if lic.get("audit_append_allowed") is True:
        _append(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsTerminalFinalizerResult(
        "kuuos_runtime_daemon_qi_github_actions_terminal_finalizer_v10_8",
        status,
        packet_id,
        str(root),
        terminal_state,
        terminal_kind,
        source_kind,
        connector,
        action,
        str(scheduler_path),
        str(terminal_path),
        str(audit_path),
        scheduler_written,
        terminal_written,
        blockers,
        warnings,
    )
