#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_unified_closed_loop_v10_4 import build_qi_github_actions_unified_closed_loop
from runtime.kuuos_runtime_daemon_qi_github_actions_dispatch_router_v10_5 import build_qi_github_actions_dispatch_router
from runtime.kuuos_runtime_daemon_qi_github_actions_dispatch_result_router_v10_6 import build_qi_github_actions_dispatch_result_router

RAW_FILES = [
    "qi_github_actions_dispatch_pr_info_raw_result_packet.json",
    "qi_github_actions_dispatch_workflow_runs_raw_result_packet.json",
    "qi_github_actions_dispatch_merge_raw_result_packet.json",
    "qi_github_actions_dispatch_rerun_raw_result_packet.json",
    "qi_github_actions_unified_dispatch_raw_result_packet.json",
]

@dataclass(frozen=True)
class QiGitHubActionsDispatchSupercycleResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    phases_run: int
    final_stage: str
    supercycle_state: str
    connector_action: str
    action_prepared: str
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


def _has_raw(root: pathlib.Path) -> bool:
    return any(_exists(root, name) for name in RAW_FILES)


def _has_call(root: pathlib.Path) -> bool:
    return any(_exists(root, name) for name in [
        "qi_github_actions_policy_action_external_call_packet.json",
        "qi_github_actions_policy_reentry_external_call_packet.json",
        "qi_github_actions_next_cycle_external_call_packet.json",
        "qi_github_actions_pr_live_autopilot_handoff_packet.json",
    ])


def _closed_ctx(root: pathlib.Path, ctx: Mapping[str, Any]) -> dict[str, Any]:
    return {"qi_github_actions_unified_closed_loop_enabled": True, "apply_github_actions_unified_closed_loop": True, "runtime_root": str(root), "max_unified_closed_loop_phases": _i(ctx.get("max_inner_unified_closed_loop_phases"), 6), "max_inner_closed_loop_phases": _i(ctx.get("max_inner_closed_loop_phases"), 8), "max_inner_reentry_merge_phases": _i(ctx.get("max_inner_reentry_merge_phases"), 10)}


def _closed_lic() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_UNIFIED_CLOSED_LOOP_LICENSE_READY", "closed_loop_supercycle_run_allowed": True, "reentry_merge_supercycle_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _dispatch_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_dispatch_router_enabled": True, "apply_github_actions_dispatch_router": True, "runtime_root": str(root)}


def _dispatch_lic() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_DISPATCH_ROUTER_LICENSE_READY", "external_call_packet_read_allowed": True, "dispatch_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _result_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_dispatch_result_router_enabled": True, "apply_github_actions_dispatch_result_router": True, "runtime_root": str(root)}


def _result_lic() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_DISPATCH_RESULT_ROUTER_LICENSE_READY", "dispatch_packet_read_allowed": True, "raw_result_packet_read_allowed": True, "target_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _record(i: int, stage: str, r: Mapping[str, Any]) -> dict[str, Any]:
    return {"index": i, "stage": stage, "status": str(r.get("status", "unknown")), "state": str(r.get("supercycle_state", r.get("unified_state", r.get("dispatch_kind", "unknown")))), "connector_action": str(r.get("connector_action", "none")), "action_prepared": str(r.get("action_prepared", "none")), "stop_reason": str(r.get("stop_reason", "unknown")), "digest": _sha(dict(r)), "blockers": list(r.get("blockers", [])) if isinstance(r.get("blockers", []), list) else [], "epoch": int(time.time())}


def build_qi_github_actions_dispatch_supercycle(*, runtime_context: Mapping[str, Any], dispatch_supercycle_license: Mapping[str, Any]) -> QiGitHubActionsDispatchSupercycleResult:
    ctx = _m(runtime_context)
    lic = _m(dispatch_supercycle_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_dispatch_supercycle_receipt.json"
    audit_path = root / "qi_github_actions_dispatch_supercycle_audit.jsonl"
    if ctx.get("qi_github_actions_dispatch_supercycle_enabled") is not True:
        blockers.append("qi_github_actions_dispatch_supercycle_enabled_not_true")
    if ctx.get("apply_github_actions_dispatch_supercycle") is not True:
        blockers.append("apply_github_actions_dispatch_supercycle_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_DISPATCH_SUPERCYCLE_LICENSE_READY":
        blockers.append("github_actions_dispatch_supercycle_license_not_ready")
    for name in ["unified_closed_loop_run_allowed", "dispatch_router_run_allowed", "dispatch_result_router_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    max_phases = _i(ctx.get("max_dispatch_supercycle_phases"), 8)
    if max_phases < 1:
        blockers.append("max_dispatch_supercycle_phases_invalid")
        max_phases = 0
    records: list[dict[str, Any]] = []
    stage = "not_run"
    state = "not_run"
    connector = "none"
    action = "none"
    stop = "not_run"
    if not blockers:
        stop = "max_phases_reached"
        for i in range(1, min(max_phases, 40) + 1):
            if _exists(root, "qi_github_actions_policy_action_final_receipt_packet.json"):
                p = _read(root / "qi_github_actions_policy_action_final_receipt_packet.json")
                stage = "final_receipt_present"
                state = str(p.get("final_state", "action_completed"))
                connector = str(p.get("connector_action", "none"))
                action = str(p.get("action_kind", "none"))
                stop = str(p.get("next_expected", "final_receipt_ready"))
                break
            if _exists(root, "qi_github_actions_next_cycle_closure_packet.json"):
                stage = "closure_present"
                state = "cycle_closed"
                stop = "closed_loop_cycle_closed"
                break
            if _has_raw(root):
                stage = "run_dispatch_result_router"
                r = build_qi_github_actions_dispatch_result_router(runtime_context=_result_ctx(root), dispatch_result_router_license=_result_lic()).to_dict()
            elif _exists(root, "qi_github_actions_unified_dispatch_packet.json"):
                p = _read(root / "qi_github_actions_unified_dispatch_packet.json")
                stage = "await_dispatch_external_result"
                state = "await_dispatch_external_result"
                connector = str(p.get("connector_action", "unknown"))
                action = str(p.get("dispatch_kind", "unknown"))
                stop = "await_dispatch_external_result"
                break
            elif _has_call(root):
                stage = "run_dispatch_router"
                r = build_qi_github_actions_dispatch_router(runtime_context=_dispatch_ctx(root), dispatch_router_license=_dispatch_lic()).to_dict()
            else:
                stage = "run_unified_closed_loop"
                r = build_qi_github_actions_unified_closed_loop(runtime_context=_closed_ctx(root, ctx), unified_closed_loop_license=_closed_lic()).to_dict()
            records.append(_record(i, stage, r))
            if not str(r.get("status", "")).endswith("READY"):
                blockers.append(f"{stage}_not_ready")
                stop = f"{stage}_blocked"
                break
            state = str(r.get("supercycle_state", r.get("unified_state", r.get("dispatch_kind", "unknown"))))
            connector = str(r.get("connector_action", connector))
            action = str(r.get("action_prepared", r.get("dispatch_kind", action)))
            stop = str(r.get("stop_reason", state))
            continue
    status = "QI_GITHUB_ACTIONS_DISPATCH_SUPERCYCLE_READY" if not blockers else "QI_GITHUB_ACTIONS_DISPATCH_SUPERCYCLE_BLOCKED"
    packet_id = "qi-github-actions-dispatch-supercycle-" + _sha({"records": records, "blockers": blockers, "state": state})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_github_actions_dispatch_supercycle_v10_7", "status": status, "packet_id": packet_id, "phases_run": len(records), "final_stage": stage, "supercycle_state": state, "connector_action": connector, "action_prepared": action, "stop_reason": stop, "phase_records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsDispatchSupercycleResult("kuuos_runtime_daemon_qi_github_actions_dispatch_supercycle_v10_7", status, packet_id, str(root), len(records), stage, state, connector, action, stop, str(receipt_path), str(audit_path), blockers, warnings, records)
