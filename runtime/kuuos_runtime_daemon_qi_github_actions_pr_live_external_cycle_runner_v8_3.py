#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_pr_live_full_cycle_runner_v8_0 import build_qi_github_actions_pr_live_full_cycle_runner
from runtime.kuuos_runtime_daemon_qi_github_actions_pr_live_external_call_bridge_v8_1 import build_qi_github_actions_pr_live_external_call_bridge
from runtime.kuuos_runtime_daemon_qi_github_actions_pr_live_external_result_bridge_v8_2 import build_qi_github_actions_pr_live_external_result_bridge


@dataclass(frozen=True)
class QiGitHubActionsPrLiveExternalCycleRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    phases_run: int
    final_stage: str
    stop_reason: str
    request_action: str
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
        "stop_reason": str(result.get("stop_reason", "unknown")),
        "request_action": str(result.get("request_action", result.get("connector_action", "none"))),
        "policy_decision": str(result.get("policy_decision", "not_run")),
        "action_prepared": str(result.get("action_prepared", "none")),
        "digest": _sha(dict(result)),
        "blockers": list(result.get("blockers", [])) if isinstance(result.get("blockers", []), list) else [],
        "epoch": int(time.time()),
    }


def _full_context(root: pathlib.Path, max_phases: int, inner_phases: int) -> dict[str, Any]:
    return {
        "qi_github_actions_pr_live_full_cycle_runner_enabled": True,
        "apply_github_actions_pr_live_full_cycle_runner": True,
        "runtime_root": str(root),
        "max_pr_live_full_cycle_phases": max_phases,
        "max_pr_live_inner_loop_phases": inner_phases,
    }


def _full_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_LIVE_FULL_CYCLE_RUNNER_LICENSE_READY",
        "loop_run_allowed": True,
        "dispatcher_run_allowed": True,
        "collector_run_allowed": True,
        "adapter_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _call_bridge_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_pr_live_external_call_bridge_enabled": True,
        "apply_github_actions_pr_live_external_call_bridge": True,
        "runtime_root": str(root),
    }


def _call_bridge_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CALL_BRIDGE_LICENSE_READY",
        "dispatch_packet_read_allowed": True,
        "external_call_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "allow_pr_info_external_call": True,
        "allow_commit_workflow_runs_external_call": True,
    }


def _result_bridge_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_pr_live_external_result_bridge_enabled": True,
        "apply_github_actions_pr_live_external_result_bridge": True,
        "runtime_root": str(root),
    }


def _result_bridge_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_RESULT_BRIDGE_LICENSE_READY",
        "external_call_packet_read_allowed": True,
        "raw_result_packet_read_allowed": True,
        "dispatch_result_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "allow_pr_info_result_bridge": True,
        "allow_commit_workflow_runs_result_bridge": True,
    }


def _has_dispatch_packet(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_pr_live_dispatch_pr_info_packet.json") or _exists(root, "qi_github_actions_pr_live_dispatch_commit_workflow_runs_packet.json")


def _has_external_call(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_pr_live_external_call_packet.json")


def _has_external_raw_result(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_pr_live_external_call_raw_result_packet.json")


def _summarize(result: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(result.get("stop_reason", "unknown")),
        str(result.get("request_action", result.get("connector_action", "none"))),
        str(result.get("policy_decision", "not_run")),
        str(result.get("action_prepared", "none")),
    )


def build_qi_github_actions_pr_live_external_cycle_runner(*, runtime_context: Mapping[str, Any], pr_live_external_cycle_runner_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveExternalCycleRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(pr_live_external_cycle_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_pr_live_external_cycle_runner_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_external_cycle_runner_audit.jsonl"

    if ctx.get("qi_github_actions_pr_live_external_cycle_runner_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_external_cycle_runner_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_external_cycle_runner") is not True:
        blockers.append("apply_github_actions_pr_live_external_cycle_runner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CYCLE_RUNNER_LICENSE_READY":
        blockers.append("github_actions_pr_live_external_cycle_runner_license_not_ready")
    for name in ["full_cycle_run_allowed", "external_call_bridge_run_allowed", "external_result_bridge_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    max_phases = _i(ctx.get("max_pr_live_external_cycle_phases", 8), 8)
    inner_full_phases = _i(ctx.get("max_pr_live_full_cycle_phases", 6), 6)
    inner_loop_phases = _i(ctx.get("max_pr_live_inner_loop_phases", 3), 3)
    if max_phases < 1:
        blockers.append("max_pr_live_external_cycle_phases_invalid")
        max_phases = 0
    if inner_full_phases < 1:
        blockers.append("max_pr_live_full_cycle_phases_invalid")
        inner_full_phases = 0
    if inner_loop_phases < 1:
        blockers.append("max_pr_live_inner_loop_phases_invalid")
        inner_loop_phases = 0
    if max_phases > 40:
        warnings.append("max_pr_live_external_cycle_phases_capped_to_40")
        max_phases = 40

    records: list[dict[str, Any]] = []
    final_stage = "not_run"
    stop_reason = "not_run"
    request_action = "none"
    policy_decision = "not_run"
    action_prepared = "none"

    if not blockers:
        stop_reason = "max_phases_reached"
        for index in range(1, max_phases + 1):
            if _has_external_raw_result(root):
                final_stage = "bridge_external_result"
                result = build_qi_github_actions_pr_live_external_result_bridge(
                    runtime_context=_result_bridge_context(root),
                    pr_live_external_result_bridge_license=_result_bridge_license(),
                ).to_dict()
                records.append(_record(index, final_stage, result))
                if result.get("status") != "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_RESULT_BRIDGE_READY":
                    blockers.append("pr_live_external_result_bridge_not_ready")
                    stop_reason = "external_result_bridge_blocked"
                    break
                continue

            if _has_external_call(root):
                final_stage = "await_external_call"
                call = _read_json(root / "qi_github_actions_pr_live_external_call_packet.json")
                request_action = str(call.get("connector_action", "unknown"))
                stop_reason = "await_external_call_result"
                break

            if _has_dispatch_packet(root):
                final_stage = "bridge_external_call"
                result = build_qi_github_actions_pr_live_external_call_bridge(
                    runtime_context=_call_bridge_context(root),
                    pr_live_external_call_bridge_license=_call_bridge_license(),
                ).to_dict()
                records.append(_record(index, final_stage, result))
                if result.get("status") != "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CALL_BRIDGE_READY":
                    blockers.append("pr_live_external_call_bridge_not_ready")
                    stop_reason = "external_call_bridge_blocked"
                    break
                request_action = str(result.get("connector_action", "none"))
                stop_reason = "await_external_call_result"
                break

            final_stage = "run_pr_live_full_cycle"
            result = build_qi_github_actions_pr_live_full_cycle_runner(
                runtime_context=_full_context(root, inner_full_phases, inner_loop_phases),
                pr_live_full_cycle_runner_license=_full_license(),
            ).to_dict()
            records.append(_record(index, final_stage, result))
            if result.get("status") != "QI_GITHUB_ACTIONS_PR_LIVE_FULL_CYCLE_RUNNER_READY":
                blockers.append("pr_live_full_cycle_runner_not_ready")
                stop_reason = "full_cycle_blocked"
                break
            stop_reason, request_action, policy_decision, action_prepared = _summarize(result)
            if stop_reason == "await_dispatch_result":
                continue
            if policy_decision not in {"not_run", "unknown"}:
                break
            break

    status = "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CYCLE_RUNNER_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CYCLE_RUNNER_BLOCKED"
    packet_id = "qi-github-actions-pr-live-external-cycle-" + _sha({"records": records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_live_external_cycle_runner_v8_3",
        "status": status,
        "packet_id": packet_id,
        "phases_run": len(records),
        "final_stage": final_stage,
        "stop_reason": stop_reason,
        "request_action": request_action,
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

    return QiGitHubActionsPrLiveExternalCycleRunnerResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_live_external_cycle_runner_v8_3",
        status,
        packet_id,
        str(root),
        len(records),
        final_stage,
        stop_reason,
        request_action,
        policy_decision,
        action_prepared,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
        records,
    )
