#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_pr_live_request_planner_v7_5 import build_qi_github_actions_pr_live_request_planner
from runtime.kuuos_runtime_daemon_qi_github_actions_pr_live_result_adapter_v7_6 import build_qi_github_actions_pr_live_result_adapter


@dataclass(frozen=True)
class QiGitHubActionsPrLiveLoopRunnerResult:
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


def _planner_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_pr_live_request_planner_enabled": True,
        "apply_github_actions_pr_live_request_planner": True,
        "runtime_root": str(root),
    }


def _planner_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_LIVE_REQUEST_PLANNER_LICENSE_READY",
        "query_packet_read_allowed": True,
        "connector_request_write_allowed": True,
        "collector_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _adapter_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_pr_live_result_adapter_enabled": True,
        "apply_github_actions_pr_live_result_adapter": True,
        "runtime_root": str(root),
        "continue_planner": True,
    }


def _adapter_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_LIVE_RESULT_ADAPTER_LICENSE_READY",
        "connector_request_read_allowed": True,
        "connector_result_read_allowed": True,
        "adapted_packet_write_allowed": True,
        "planner_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "allow_pr_info_result": True,
        "allow_commit_workflow_runs_result": True,
    }


def _record(index: int, stage: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "index": index,
        "stage": stage,
        "status": str(payload.get("status", "unknown")),
        "stop_reason": str(payload.get("stop_reason", "unknown")),
        "request_action": str(payload.get("request_action", "none")),
        "policy_decision": str(payload.get("policy_decision", "not_run")),
        "action_prepared": str(payload.get("action_prepared", "none")),
        "digest": _sha(dict(payload)),
        "blockers": list(payload.get("blockers", [])) if isinstance(payload.get("blockers", []), list) else [],
        "epoch": int(time.time()),
    }


def _copy_request_for_adapter(root: pathlib.Path) -> None:
    pr_req = _read_json(root / "qi_github_actions_pr_info_connector_request.json")
    runs_req = _read_json(root / "qi_github_actions_commit_workflow_runs_connector_request.json")
    target = root / "qi_github_actions_pr_live_connector_request.json"
    if pr_req and not _exists(root, "qi_github_actions_raw_pr_info_packet.json"):
        _write_json(target, pr_req)
    elif runs_req:
        _write_json(target, runs_req)


def _has_connector_result(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_pr_live_connector_result_packet.json")


def build_qi_github_actions_pr_live_loop_runner(*, runtime_context: Mapping[str, Any], pr_live_loop_runner_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveLoopRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(pr_live_loop_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_pr_live_loop_runner_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_loop_runner_audit.jsonl"

    if ctx.get("qi_github_actions_pr_live_loop_runner_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_loop_runner_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_loop_runner") is not True:
        blockers.append("apply_github_actions_pr_live_loop_runner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_LOOP_RUNNER_LICENSE_READY":
        blockers.append("github_actions_pr_live_loop_runner_license_not_ready")
    for name in ["planner_run_allowed", "adapter_run_allowed", "request_bridge_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    max_phases = _i(ctx.get("max_pr_live_loop_phases", 4), 4)
    if max_phases < 1:
        blockers.append("max_pr_live_loop_phases_invalid")
        max_phases = 0
    if max_phases > 20:
        warnings.append("max_pr_live_loop_phases_capped_to_20")
        max_phases = 20

    records: list[dict[str, Any]] = []
    final_stage = "not_run"
    stop_reason = "not_run"
    request_action = "none"
    policy_decision = "not_run"
    action_prepared = "none"
    if not blockers:
        stop_reason = "max_phases_reached"
        for index in range(1, max_phases + 1):
            if _has_connector_result(root):
                _copy_request_for_adapter(root)
                final_stage = "adapt_connector_result"
                result = build_qi_github_actions_pr_live_result_adapter(
                    runtime_context=_adapter_context(root),
                    pr_live_result_adapter_license=_adapter_license(),
                ).to_dict()
                records.append(_record(index, final_stage, result))
                if result.get("status") != "QI_GITHUB_ACTIONS_PR_LIVE_RESULT_ADAPTER_READY":
                    blockers.append("pr_live_result_adapter_not_ready")
                    stop_reason = "adapter_blocked"
                    break
                stop_reason = str(result.get("stop_reason", "unknown"))
                request_action = str(result.get("request_action", "none"))
                policy_decision = str(result.get("policy_decision", "not_run"))
                action_prepared = str(result.get("action_prepared", "none"))
                if stop_reason in {"await_commit_workflow_runs", "await_pr_info"}:
                    break
                if policy_decision != "not_run" and policy_decision != "unknown":
                    break
                continue

            final_stage = "plan_live_request"
            result = build_qi_github_actions_pr_live_request_planner(
                runtime_context=_planner_context(root),
                pr_live_request_planner_license=_planner_license(),
            ).to_dict()
            records.append(_record(index, final_stage, result))
            if result.get("status") != "QI_GITHUB_ACTIONS_PR_LIVE_REQUEST_PLANNER_READY":
                blockers.append("pr_live_request_planner_not_ready")
                stop_reason = "planner_blocked"
                break
            stop_reason = str(result.get("stop_reason", "unknown"))
            request_action = str(result.get("request_action", "none"))
            policy_decision = str(result.get("policy_decision", "not_run"))
            action_prepared = str(result.get("action_prepared", "none"))
            if stop_reason in {"await_pr_info", "await_commit_workflow_runs"}:
                break
            if policy_decision != "not_run" and policy_decision != "unknown":
                break

    status = "QI_GITHUB_ACTIONS_PR_LIVE_LOOP_RUNNER_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_LOOP_RUNNER_BLOCKED"
    packet_id = "qi-github-actions-pr-live-loop-" + _sha({"records": records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_live_loop_runner_v7_7",
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

    return QiGitHubActionsPrLiveLoopRunnerResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_live_loop_runner_v7_7",
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
