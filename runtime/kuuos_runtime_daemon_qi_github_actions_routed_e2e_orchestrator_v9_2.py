#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_pr_live_autopilot_e2e_orchestrator_v9_0 import build_qi_github_actions_pr_live_autopilot_e2e_orchestrator
from runtime.kuuos_runtime_daemon_qi_github_actions_policy_action_final_router_v9_1 import build_qi_github_actions_policy_action_final_router


@dataclass(frozen=True)
class QiGitHubActionsRoutedE2EOrchestratorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    phases_run: int
    final_stage: str
    final_state: str
    route_state: str
    stop_reason: str
    connector_action: str
    policy_decision: str
    action_prepared: str
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
        "final_state": str(result.get("final_state", "unknown")),
        "route_state": str(result.get("route_state", "unknown")),
        "stop_reason": str(result.get("stop_reason", "unknown")),
        "connector_action": str(result.get("connector_action", "none")),
        "policy_decision": str(result.get("policy_decision", "not_run")),
        "action_prepared": str(result.get("action_prepared", "none")),
        "digest": _sha(dict(result)),
        "blockers": list(result.get("blockers", [])) if isinstance(result.get("blockers", []), list) else [],
        "epoch": int(time.time()),
    }


def _e2e_context(root: pathlib.Path, ctx: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "qi_github_actions_pr_live_autopilot_e2e_orchestrator_enabled": True,
        "apply_github_actions_pr_live_autopilot_e2e_orchestrator": True,
        "runtime_root": str(root),
        "max_autopilot_e2e_phases": _i(ctx.get("max_inner_e2e_phases", 8), 8),
    }


def _e2e_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_E2E_ORCHESTRATOR_LICENSE_READY",
        "autopilot_run_allowed": True,
        "autopilot_ingest_allowed": True,
        "policy_action_handoff_allowed": True,
        "policy_action_external_call_allowed": True,
        "policy_action_external_result_allowed": True,
        "policy_action_final_receipt_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _router_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_policy_action_final_router_enabled": True,
        "apply_github_actions_policy_action_final_router": True,
        "runtime_root": str(root),
    }


def _router_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_ROUTER_LICENSE_READY",
        "final_receipt_packet_read_allowed": True,
        "route_packet_write_allowed": True,
        "feedback_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _final_route(root: pathlib.Path) -> dict[str, Any]:
    return _read_json(root / "qi_github_actions_policy_action_final_route_packet.json")


def _final_receipt(root: pathlib.Path) -> dict[str, Any]:
    return _read_json(root / "qi_github_actions_policy_action_final_receipt_packet.json")


def _status_ready(value: Mapping[str, Any], suffix: str) -> bool:
    return str(value.get("status", "")).endswith(suffix)


def build_qi_github_actions_routed_e2e_orchestrator(*, runtime_context: Mapping[str, Any], routed_e2e_orchestrator_license: Mapping[str, Any]) -> QiGitHubActionsRoutedE2EOrchestratorResult:
    ctx = _m(runtime_context)
    lic = _m(routed_e2e_orchestrator_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_routed_e2e_orchestrator_receipt.json"
    audit_path = root / "qi_github_actions_routed_e2e_orchestrator_audit.jsonl"

    if ctx.get("qi_github_actions_routed_e2e_orchestrator_enabled") is not True:
        blockers.append("qi_github_actions_routed_e2e_orchestrator_enabled_not_true")
    if ctx.get("apply_github_actions_routed_e2e_orchestrator") is not True:
        blockers.append("apply_github_actions_routed_e2e_orchestrator_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_ROUTED_E2E_ORCHESTRATOR_LICENSE_READY":
        blockers.append("github_actions_routed_e2e_orchestrator_license_not_ready")
    for name in ["e2e_orchestrator_run_allowed", "final_router_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    max_phases = _i(ctx.get("max_routed_e2e_phases", 4), 4)
    if max_phases < 1:
        blockers.append("max_routed_e2e_phases_invalid")
        max_phases = 0
    if max_phases > 20:
        warnings.append("max_routed_e2e_phases_capped_to_20")
        max_phases = 20

    records: list[dict[str, Any]] = []
    final_stage = "not_run"
    final_state = "not_run"
    route_state = "not_routed"
    stop_reason = "not_run"
    connector_action = "none"
    policy_decision = "not_run"
    action_prepared = "none"

    if not blockers:
        stop_reason = "max_phases_reached"
        for index in range(1, max_phases + 1):
            route = _final_route(root)
            if route:
                final_stage = "final_route_present"
                final_state = str(route.get("final_state", "unknown"))
                route_state = str(route.get("route_state", "unknown"))
                stop_reason = str(route.get("next_expected", "routed"))
                break

            receipt = _final_receipt(root)
            if receipt:
                final_stage = "run_final_router"
                result = build_qi_github_actions_policy_action_final_router(
                    runtime_context=_router_context(root),
                    policy_action_final_router_license=_router_license(),
                ).to_dict()
                records.append(_record(index, final_stage, result))
                if not _status_ready(result, "READY"):
                    blockers.append("final_router_not_ready")
                    stop_reason = "final_router_blocked"
                    break
                final_state = str(result.get("final_state", "unknown"))
                route_state = str(result.get("route_state", "unknown"))
                stop_reason = str(result.get("route_state", "routed"))
                break

            final_stage = "run_e2e_orchestrator"
            result = build_qi_github_actions_pr_live_autopilot_e2e_orchestrator(
                runtime_context=_e2e_context(root, ctx),
                e2e_orchestrator_license=_e2e_license(),
            ).to_dict()
            records.append(_record(index, final_stage, result))
            if not _status_ready(result, "READY"):
                blockers.append("e2e_orchestrator_not_ready")
                stop_reason = "e2e_orchestrator_blocked"
                break
            final_state = str(result.get("final_state", "unknown"))
            stop_reason = str(result.get("stop_reason", "unknown"))
            connector_action = str(result.get("connector_action", "none"))
            policy_decision = str(result.get("policy_decision", "not_run"))
            action_prepared = str(result.get("action_prepared", "none"))
            if _exists(root, "qi_github_actions_policy_action_final_receipt_packet.json"):
                continue
            break

    status = "QI_GITHUB_ACTIONS_ROUTED_E2E_ORCHESTRATOR_READY" if not blockers else "QI_GITHUB_ACTIONS_ROUTED_E2E_ORCHESTRATOR_BLOCKED"
    packet_id = "qi-github-actions-routed-e2e-" + _sha({"records": records, "blockers": blockers, "route_state": route_state})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_routed_e2e_orchestrator_v9_2",
        "status": status,
        "packet_id": packet_id,
        "phases_run": len(records),
        "final_stage": final_stage,
        "final_state": final_state,
        "route_state": route_state,
        "stop_reason": stop_reason,
        "connector_action": connector_action,
        "policy_decision": policy_decision,
        "action_prepared": action_prepared,
        "phase_records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsRoutedE2EOrchestratorResult(
        "kuuos_runtime_daemon_qi_github_actions_routed_e2e_orchestrator_v9_2",
        status,
        packet_id,
        str(root),
        len(records),
        final_stage,
        final_state,
        route_state,
        stop_reason,
        connector_action,
        policy_decision,
        action_prepared,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
        records,
    )
