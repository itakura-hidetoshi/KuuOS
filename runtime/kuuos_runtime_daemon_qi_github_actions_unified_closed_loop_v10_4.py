#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_closed_loop_supercycle_v10_0 import build_qi_github_actions_closed_loop_supercycle
from runtime.kuuos_runtime_daemon_qi_github_actions_reentry_merge_supercycle_v10_3 import build_qi_github_actions_reentry_merge_supercycle


@dataclass(frozen=True)
class QiGitHubActionsUnifiedClosedLoopResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    phases_run: int
    final_stage: str
    unified_state: str
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


MERGE_SURFACE = [
    "qi_github_actions_policy_reentry_packet.json",
    "qi_github_actions_policy_reentry_external_call_packet.json",
    "qi_github_actions_policy_reentry_pr_info_raw_result_packet.json",
    "qi_github_actions_pr_live_autopilot_handoff_packet.json",
    "qi_github_actions_autopilot_policy_action_handoff_packet.json",
    "qi_github_actions_policy_action_external_call_packet.json",
    "qi_github_actions_policy_action_external_call_raw_result_packet.json",
    "qi_github_actions_policy_action_merge_result_packet.json",
    "qi_github_actions_policy_action_rerun_result_packet.json",
    "qi_github_actions_policy_action_reobserve_result_packet.json",
]


def _has_merge_surface(root: pathlib.Path) -> bool:
    return any(_exists(root, name) for name in MERGE_SURFACE)


def _closed_ctx(root: pathlib.Path, ctx: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "qi_github_actions_closed_loop_supercycle_enabled": True,
        "apply_github_actions_closed_loop_supercycle": True,
        "runtime_root": str(root),
        "max_closed_loop_supercycle_phases": _i(ctx.get("max_inner_closed_loop_phases"), 8),
        "max_inner_cycle_aware_phases": _i(ctx.get("max_inner_cycle_aware_phases"), 5),
        "max_inner_super_orchestrator_phases": _i(ctx.get("max_inner_super_orchestrator_phases"), 5),
        "max_inner_routed_e2e_phases": _i(ctx.get("max_inner_routed_e2e_phases"), 4),
        "max_inner_e2e_phases": _i(ctx.get("max_inner_e2e_phases"), 8),
    }


def _closed_lic() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_CLOSED_LOOP_SUPERCYCLE_LICENSE_READY", "cycle_aware_run_allowed": True, "external_bridge_run_allowed": True, "result_bridge_run_allowed": True, "reentry_adapter_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _merge_ctx(root: pathlib.Path, ctx: Mapping[str, Any]) -> dict[str, Any]:
    return {"qi_github_actions_reentry_merge_supercycle_enabled": True, "apply_github_actions_reentry_merge_supercycle": True, "runtime_root": str(root), "max_reentry_merge_supercycle_phases": _i(ctx.get("max_inner_reentry_merge_phases"), 10)}


def _merge_lic() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_REENTRY_MERGE_SUPERCYCLE_LICENSE_READY", "reentry_evaluator_run_allowed": True, "pr_info_result_bridge_run_allowed": True, "policy_action_handoff_run_allowed": True, "policy_action_external_call_run_allowed": True, "policy_action_external_result_run_allowed": True, "policy_action_final_receipt_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _record(i: int, stage: str, r: Mapping[str, Any]) -> dict[str, Any]:
    return {"index": i, "stage": stage, "status": str(r.get("status", "unknown")), "state": str(r.get("supercycle_state", "unknown")), "connector_action": str(r.get("connector_action", "none")), "action_prepared": str(r.get("action_prepared", "none")), "stop_reason": str(r.get("stop_reason", "unknown")), "digest": _sha(dict(r)), "blockers": list(r.get("blockers", [])) if isinstance(r.get("blockers", []), list) else [], "epoch": int(time.time())}


def build_qi_github_actions_unified_closed_loop(*, runtime_context: Mapping[str, Any], unified_closed_loop_license: Mapping[str, Any]) -> QiGitHubActionsUnifiedClosedLoopResult:
    ctx = _m(runtime_context)
    lic = _m(unified_closed_loop_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_unified_closed_loop_receipt.json"
    audit_path = root / "qi_github_actions_unified_closed_loop_audit.jsonl"
    if ctx.get("qi_github_actions_unified_closed_loop_enabled") is not True:
        blockers.append("qi_github_actions_unified_closed_loop_enabled_not_true")
    if ctx.get("apply_github_actions_unified_closed_loop") is not True:
        blockers.append("apply_github_actions_unified_closed_loop_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_UNIFIED_CLOSED_LOOP_LICENSE_READY":
        blockers.append("github_actions_unified_closed_loop_license_not_ready")
    for name in ["closed_loop_supercycle_run_allowed", "reentry_merge_supercycle_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    max_phases = _i(ctx.get("max_unified_closed_loop_phases"), 6)
    if max_phases < 1:
        blockers.append("max_unified_closed_loop_phases_invalid")
        max_phases = 0
    records: list[dict[str, Any]] = []
    final_stage = "not_run"
    state = "not_run"
    connector = "none"
    action = "none"
    stop = "not_run"
    if not blockers:
        stop = "max_phases_reached"
        for i in range(1, min(max_phases, 40) + 1):
            if _exists(root, "qi_github_actions_policy_action_final_receipt_packet.json"):
                p = _read(root / "qi_github_actions_policy_action_final_receipt_packet.json")
                final_stage = "policy_action_final_receipt_present"
                state = str(p.get("final_state", "action_completed"))
                connector = str(p.get("connector_action", "none"))
                action = str(p.get("action_kind", "none"))
                stop = str(p.get("next_expected", "final_receipt_ready"))
                break
            if _exists(root, "qi_github_actions_next_cycle_closure_packet.json"):
                final_stage = "closure_present"
                state = "cycle_closed"
                connector = "none"
                action = "none"
                stop = "closed_loop_cycle_closed"
                break
            if _has_merge_surface(root):
                final_stage = "run_reentry_merge_supercycle"
                r = build_qi_github_actions_reentry_merge_supercycle(runtime_context=_merge_ctx(root, ctx), reentry_merge_supercycle_license=_merge_lic()).to_dict()
            else:
                final_stage = "run_closed_loop_supercycle"
                r = build_qi_github_actions_closed_loop_supercycle(runtime_context=_closed_ctx(root, ctx), closed_loop_supercycle_license=_closed_lic()).to_dict()
            records.append(_record(i, final_stage, r))
            if not str(r.get("status", "")).endswith("READY"):
                blockers.append(f"{final_stage}_not_ready")
                stop = f"{final_stage}_blocked"
                break
            state = str(r.get("supercycle_state", "unknown"))
            connector = str(r.get("connector_action", "none"))
            action = str(r.get("action_prepared", action))
            stop = str(r.get("stop_reason", state))
            if state == "policy_reentry_ready" or _has_merge_surface(root):
                continue
            break
    status = "QI_GITHUB_ACTIONS_UNIFIED_CLOSED_LOOP_READY" if not blockers else "QI_GITHUB_ACTIONS_UNIFIED_CLOSED_LOOP_BLOCKED"
    packet_id = "qi-github-actions-unified-closed-loop-" + _sha({"records": records, "blockers": blockers, "state": state})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_github_actions_unified_closed_loop_v10_4", "status": status, "packet_id": packet_id, "phases_run": len(records), "final_stage": final_stage, "unified_state": state, "connector_action": connector, "action_prepared": action, "stop_reason": stop, "phase_records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsUnifiedClosedLoopResult("kuuos_runtime_daemon_qi_github_actions_unified_closed_loop_v10_4", status, packet_id, str(root), len(records), final_stage, state, connector, action, stop, str(receipt_path), str(audit_path), blockers, warnings, records)
