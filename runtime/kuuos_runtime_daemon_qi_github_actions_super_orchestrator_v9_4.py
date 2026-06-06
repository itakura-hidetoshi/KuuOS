#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_routed_e2e_orchestrator_v9_2 import build_qi_github_actions_routed_e2e_orchestrator
from runtime.kuuos_runtime_daemon_qi_github_actions_route_planner_v9_3 import build_qi_github_actions_route_planner


@dataclass(frozen=True)
class QiGitHubActionsSuperOrchestratorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    phases_run: int
    final_stage: str
    route_state: str
    next_cycle_state: str
    next_connector_action: str
    stop_reason: str
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


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


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
    path = root / name
    return path.is_file() and path.stat().st_size > 2


def _record(index: int, stage: str, result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "index": index,
        "stage": stage,
        "status": str(result.get("status", "unknown")),
        "route_state": str(result.get("route_state", "unknown")),
        "next_cycle_state": str(result.get("next_cycle_state", "unknown")),
        "next_connector_action": str(result.get("next_connector_action", result.get("connector_action", "none"))),
        "stop_reason": str(result.get("stop_reason", "unknown")),
        "digest": _sha(dict(result)),
        "blockers": list(result.get("blockers", [])) if isinstance(result.get("blockers", []), list) else [],
        "epoch": int(time.time()),
    }


def _routed_context(root: pathlib.Path, ctx: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "qi_github_actions_routed_e2e_orchestrator_enabled": True,
        "apply_github_actions_routed_e2e_orchestrator": True,
        "runtime_root": str(root),
        "max_routed_e2e_phases": _i(ctx.get("max_inner_routed_e2e_phases", 4), 4),
        "max_inner_e2e_phases": _i(ctx.get("max_inner_e2e_phases", 8), 8),
    }


def _routed_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_ROUTED_E2E_ORCHESTRATOR_LICENSE_READY",
        "e2e_orchestrator_run_allowed": True,
        "final_router_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _route_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_route_planner_enabled": True,
        "apply_github_actions_route_planner": True,
        "runtime_root": str(root),
    }


def _route_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_ROUTE_PLANNER_LICENSE_READY",
        "route_packet_read_allowed": True,
        "context_packet_read_allowed": True,
        "next_cycle_packet_write_allowed": True,
        "reobserve_request_write_allowed": True,
        "reentry_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_qi_github_actions_super_orchestrator(*, runtime_context: Mapping[str, Any], super_orchestrator_license: Mapping[str, Any]) -> QiGitHubActionsSuperOrchestratorResult:
    ctx = _m(runtime_context)
    lic = _m(super_orchestrator_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_super_orchestrator_receipt.json"
    audit_path = root / "qi_github_actions_super_orchestrator_audit.jsonl"

    if ctx.get("qi_github_actions_super_orchestrator_enabled") is not True:
        blockers.append("qi_github_actions_super_orchestrator_enabled_not_true")
    if ctx.get("apply_github_actions_super_orchestrator") is not True:
        blockers.append("apply_github_actions_super_orchestrator_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_SUPER_ORCHESTRATOR_LICENSE_READY":
        blockers.append("github_actions_super_orchestrator_license_not_ready")
    for name in ["routed_e2e_run_allowed", "route_planner_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    max_phases = _i(ctx.get("max_super_orchestrator_phases", 5), 5)
    if max_phases < 1:
        blockers.append("max_super_orchestrator_phases_invalid")
        max_phases = 0
    if max_phases > 20:
        warnings.append("max_super_orchestrator_phases_capped_to_20")
        max_phases = 20

    records: list[dict[str, Any]] = []
    final_stage = "not_run"
    route_state = "not_routed"
    next_cycle_state = "not_planned"
    next_connector_action = "none"
    stop_reason = "not_run"

    if not blockers:
        stop_reason = "max_phases_reached"
        for index in range(1, max_phases + 1):
            next_packet = _read_json(root / "qi_github_actions_route_next_cycle_packet.json")
            if next_packet:
                final_stage = "next_cycle_present"
                route_state = str(next_packet.get("route_state", "unknown"))
                next_cycle_state = str(next_packet.get("next_cycle_state", "unknown"))
                next_connector_action = str(next_packet.get("next_connector_action", "none"))
                stop_reason = "next_cycle_ready"
                break

            if _exists(root, "qi_github_actions_policy_action_final_route_packet.json"):
                final_stage = "run_route_planner"
                result = build_qi_github_actions_route_planner(runtime_context=_route_context(root), route_planner_license=_route_license()).to_dict()
            else:
                final_stage = "run_routed_e2e"
                result = build_qi_github_actions_routed_e2e_orchestrator(runtime_context=_routed_context(root, ctx), routed_e2e_orchestrator_license=_routed_license()).to_dict()

            records.append(_record(index, final_stage, result))
            if not str(result.get("status", "")).endswith("READY"):
                blockers.append(f"{final_stage}_not_ready")
                stop_reason = f"{final_stage}_blocked"
                break
            route_state = str(result.get("route_state", route_state))
            next_cycle_state = str(result.get("next_cycle_state", next_cycle_state))
            next_connector_action = str(result.get("next_connector_action", result.get("connector_action", next_connector_action)))
            stop_reason = str(result.get("stop_reason", stop_reason))
            if final_stage == "run_route_planner":
                stop_reason = "next_cycle_planned"
                break
            if _exists(root, "qi_github_actions_policy_action_final_route_packet.json"):
                continue
            break

    status = "QI_GITHUB_ACTIONS_SUPER_ORCHESTRATOR_READY" if not blockers else "QI_GITHUB_ACTIONS_SUPER_ORCHESTRATOR_BLOCKED"
    packet_id = "qi-github-actions-super-orchestrator-" + _sha({"records": records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_super_orchestrator_v9_4",
        "status": status,
        "packet_id": packet_id,
        "phases_run": len(records),
        "final_stage": final_stage,
        "route_state": route_state,
        "next_cycle_state": next_cycle_state,
        "next_connector_action": next_connector_action,
        "stop_reason": stop_reason,
        "phase_records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsSuperOrchestratorResult(
        "kuuos_runtime_daemon_qi_github_actions_super_orchestrator_v9_4",
        status,
        packet_id,
        str(root),
        len(records),
        final_stage,
        route_state,
        next_cycle_state,
        next_connector_action,
        stop_reason,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
        records,
    )
