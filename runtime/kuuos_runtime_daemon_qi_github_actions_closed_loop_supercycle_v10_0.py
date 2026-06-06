#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_cycle_aware_super_executor_v9_6 import build_qi_github_actions_cycle_aware_super_executor
from runtime.kuuos_runtime_daemon_qi_github_actions_next_cycle_external_bridge_v9_7 import build_qi_github_actions_next_cycle_external_bridge
from runtime.kuuos_runtime_daemon_qi_github_actions_next_cycle_result_bridge_v9_8 import build_qi_github_actions_next_cycle_result_bridge
from runtime.kuuos_runtime_daemon_qi_github_actions_policy_reentry_adapter_v9_9 import build_qi_github_actions_policy_reentry_adapter


@dataclass(frozen=True)
class QiGitHubActionsClosedLoopSupercycleResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    phases_run: int
    final_stage: str
    supercycle_state: str
    connector_action: str
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
        "state": str(result.get("supercycle_state", result.get("reentry_state", result.get("bridge_state", result.get("execution_state", "unknown"))))),
        "connector_action": str(result.get("connector_action", "none")),
        "stop_reason": str(result.get("stop_reason", "unknown")),
        "digest": _sha(dict(result)),
        "blockers": list(result.get("blockers", [])) if isinstance(result.get("blockers", []), list) else [],
        "epoch": int(time.time()),
    }


def _cycle_context(root: pathlib.Path, ctx: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "qi_github_actions_cycle_aware_super_executor_enabled": True,
        "apply_github_actions_cycle_aware_super_executor": True,
        "runtime_root": str(root),
        "max_cycle_aware_super_executor_phases": _i(ctx.get("max_inner_cycle_aware_phases", 5), 5),
        "max_inner_super_orchestrator_phases": _i(ctx.get("max_inner_super_orchestrator_phases", 5), 5),
        "max_inner_routed_e2e_phases": _i(ctx.get("max_inner_routed_e2e_phases", 4), 4),
        "max_inner_e2e_phases": _i(ctx.get("max_inner_e2e_phases", 8), 8),
    }


def _cycle_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_CYCLE_AWARE_SUPER_EXECUTOR_LICENSE_READY",
        "super_orchestrator_run_allowed": True,
        "next_cycle_executor_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _external_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_next_cycle_external_bridge_enabled": True, "apply_github_actions_next_cycle_external_bridge": True, "runtime_root": str(root)}


def _external_license() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_NEXT_CYCLE_EXTERNAL_BRIDGE_LICENSE_READY", "execution_packet_read_allowed": True, "output_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _result_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_next_cycle_result_bridge_enabled": True, "apply_github_actions_next_cycle_result_bridge": True, "runtime_root": str(root)}


def _result_license() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_NEXT_CYCLE_RESULT_BRIDGE_LICENSE_READY", "external_call_packet_read_allowed": True, "raw_result_packet_read_allowed": True, "result_packet_write_allowed": True, "reentry_bridge_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _reentry_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_reentry_adapter_enabled": True, "apply_github_actions_policy_reentry_adapter": True, "runtime_root": str(root)}


def _reentry_license() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_POLICY_REENTRY_ADAPTER_LICENSE_READY", "reentry_bridge_packet_read_allowed": True, "context_packet_read_allowed": True, "raw_workflow_packet_write_allowed": True, "status_packet_write_allowed": True, "policy_reentry_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def build_qi_github_actions_closed_loop_supercycle(*, runtime_context: Mapping[str, Any], closed_loop_supercycle_license: Mapping[str, Any]) -> QiGitHubActionsClosedLoopSupercycleResult:
    ctx = _m(runtime_context)
    lic = _m(closed_loop_supercycle_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_closed_loop_supercycle_receipt.json"
    audit_path = root / "qi_github_actions_closed_loop_supercycle_audit.jsonl"

    if ctx.get("qi_github_actions_closed_loop_supercycle_enabled") is not True:
        blockers.append("qi_github_actions_closed_loop_supercycle_enabled_not_true")
    if ctx.get("apply_github_actions_closed_loop_supercycle") is not True:
        blockers.append("apply_github_actions_closed_loop_supercycle_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_CLOSED_LOOP_SUPERCYCLE_LICENSE_READY":
        blockers.append("github_actions_closed_loop_supercycle_license_not_ready")
    for name in ["cycle_aware_run_allowed", "external_bridge_run_allowed", "result_bridge_run_allowed", "reentry_adapter_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    max_phases = _i(ctx.get("max_closed_loop_supercycle_phases", 8), 8)
    if max_phases < 1:
        blockers.append("max_closed_loop_supercycle_phases_invalid")
        max_phases = 0
    if max_phases > 40:
        warnings.append("max_closed_loop_supercycle_phases_capped_to_40")
        max_phases = 40

    records: list[dict[str, Any]] = []
    final_stage = "not_run"
    supercycle_state = "not_run"
    connector_action = "none"
    stop_reason = "not_run"

    if not blockers:
        stop_reason = "max_phases_reached"
        for index in range(1, max_phases + 1):
            if _exists(root, "qi_github_actions_policy_reentry_packet.json"):
                packet = _read_json(root / "qi_github_actions_policy_reentry_packet.json")
                final_stage = "policy_reentry_present"
                supercycle_state = str(packet.get("reentry_state", "policy_reentry_ready"))
                connector_action = "none"
                stop_reason = "policy_reentry_ready"
                break

            if _exists(root, "qi_github_actions_next_cycle_closure_packet.json"):
                final_stage = "closure_present"
                supercycle_state = "cycle_closed"
                connector_action = "none"
                stop_reason = "closed_loop_cycle_closed"
                break

            if _exists(root, "qi_github_actions_next_cycle_reentry_bridge_packet.json"):
                final_stage = "run_policy_reentry_adapter"
                result = build_qi_github_actions_policy_reentry_adapter(runtime_context=_reentry_context(root), policy_reentry_adapter_license=_reentry_license()).to_dict()
            elif _exists(root, "qi_github_actions_next_cycle_external_call_raw_result_packet.json"):
                final_stage = "run_next_cycle_result_bridge"
                result = build_qi_github_actions_next_cycle_result_bridge(runtime_context=_result_context(root), next_cycle_result_bridge_license=_result_license()).to_dict()
            elif _exists(root, "qi_github_actions_next_cycle_external_call_packet.json"):
                call = _read_json(root / "qi_github_actions_next_cycle_external_call_packet.json")
                final_stage = "await_next_cycle_external_result"
                supercycle_state = "await_next_cycle_external_result"
                connector_action = str(call.get("connector_action", "GitHub.fetch_commit_workflow_runs"))
                stop_reason = "await_external_result"
                break
            elif _exists(root, "qi_github_actions_next_cycle_execution_packet.json"):
                final_stage = "run_next_cycle_external_bridge"
                result = build_qi_github_actions_next_cycle_external_bridge(runtime_context=_external_context(root), next_cycle_external_bridge_license=_external_license()).to_dict()
            else:
                final_stage = "run_cycle_aware_super_executor"
                result = build_qi_github_actions_cycle_aware_super_executor(runtime_context=_cycle_context(root, ctx), cycle_aware_super_executor_license=_cycle_license()).to_dict()

            records.append(_record(index, final_stage, result))
            if not str(result.get("status", "")).endswith("READY"):
                blockers.append(f"{final_stage}_not_ready")
                stop_reason = f"{final_stage}_blocked"
                break
            supercycle_state = str(result.get("reentry_state", result.get("bridge_state", result.get("execution_state", "unknown"))))
            connector_action = str(result.get("connector_action", "none"))
            stop_reason = str(result.get("stop_reason", supercycle_state))
            continue

    status = "QI_GITHUB_ACTIONS_CLOSED_LOOP_SUPERCYCLE_READY" if not blockers else "QI_GITHUB_ACTIONS_CLOSED_LOOP_SUPERCYCLE_BLOCKED"
    packet_id = "qi-github-actions-closed-loop-supercycle-" + _sha({"records": records, "blockers": blockers, "state": supercycle_state})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_closed_loop_supercycle_v10_0",
        "status": status,
        "packet_id": packet_id,
        "phases_run": len(records),
        "final_stage": final_stage,
        "supercycle_state": supercycle_state,
        "connector_action": connector_action,
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

    return QiGitHubActionsClosedLoopSupercycleResult(
        "kuuos_runtime_daemon_qi_github_actions_closed_loop_supercycle_v10_0",
        status,
        packet_id,
        str(root),
        len(records),
        final_stage,
        supercycle_state,
        connector_action,
        stop_reason,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
        records,
    )
