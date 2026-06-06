#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_direct_executor_v5_6 import build_qi_github_actions_direct_executor
from runtime.kuuos_runtime_daemon_qi_github_actions_full_cycle_orchestrator_v6_8 import build_qi_github_actions_full_cycle_orchestrator


@dataclass(frozen=True)
class QiGitHubActionsFullCyclePolicyRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    policy_decision: str
    action_prepared: str
    orchestrator_status: str
    stop_reason: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]
    policy_records: list[dict[str, Any]]

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


def _runs(status_packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = status_packet.get("workflow_runs", [])
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _required(status_packet: Mapping[str, Any], policy: Mapping[str, Any]) -> list[str]:
    raw = policy.get("required_workflows") or status_packet.get("required_workflows")
    if isinstance(raw, list) and raw:
        return [str(x) for x in raw]
    return [str(run.get("name", "")) for run in _runs(status_packet) if run.get("name")]


def _latest_by_name(runs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for run in runs:
        name = str(run.get("name", ""))
        if name and name not in out:
            out[name] = run
    return out


def _is_success(run: Mapping[str, Any]) -> bool:
    return run.get("status") == "completed" and run.get("conclusion") == "success"


def _is_pending(run: Mapping[str, Any]) -> bool:
    return str(run.get("status", "")).lower() in {"queued", "requested", "waiting", "pending", "in_progress"}


def _is_failed(run: Mapping[str, Any]) -> bool:
    return run.get("status") == "completed" and str(run.get("conclusion", "")).lower() not in {"success", "neutral", "skipped", "", "none"}


def _classify(status_packet: Mapping[str, Any], policy: Mapping[str, Any]) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    runs = _runs(status_packet)
    latest = _latest_by_name(runs)
    required = _required(status_packet, policy)
    missing = [name for name in required if name not in latest]
    pending = [latest[name] for name in required if name in latest and _is_pending(latest[name])]
    failed = [latest[name] for name in required if name in latest and _is_failed(latest[name])]
    if missing:
        return "policy_missing_required", pending, failed, missing
    if pending:
        return "policy_pending_reobserve", pending, failed, missing
    if failed:
        return "policy_failed_rerun", pending, failed, missing
    if required and all(_is_success(latest[name]) for name in required):
        return "policy_all_green", pending, failed, missing
    return "policy_hold", pending, failed, missing


def _repo(policy: Mapping[str, Any], blockers: list[str]) -> str:
    repo = str(policy.get("repo_full_name", "")).strip()
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    return repo


def _write_direct_packet(root: pathlib.Path, policy: Mapping[str, Any], decision: str, failed: list[dict[str, Any]], blockers: list[str]) -> str:
    repo = _repo(policy, blockers)
    if decision == "policy_all_green":
        pr_number = _i(policy.get("pr_number", policy.get("pull_number")), 0)
        if pr_number <= 0:
            blockers.append("pr_number_invalid")
        packet: dict[str, Any] = {
            "action": "merge_pull_request",
            "direct_execution_allowed": True,
            "repo_full_name": repo,
            "pr_number": pr_number,
            "merge_method": str(policy.get("merge_method", "merge")),
        }
        if policy.get("expected_head_sha"):
            packet["expected_head_sha"] = str(policy.get("expected_head_sha"))
        _write_json(root / "qi_github_actions_direct_execution_packet.json", packet)
        return "merge_pull_request"
    if decision == "policy_failed_rerun":
        run_id = _i(policy.get("run_id"), 0)
        if run_id <= 0 and failed:
            run_id = _i(failed[0].get("id"), 0)
        if run_id <= 0:
            blockers.append("run_id_invalid")
        packet = {
            "action": "rerun_failed_workflow_run_jobs",
            "direct_execution_allowed": True,
            "repo_full_name": repo,
            "run_id": run_id,
        }
        _write_json(root / "qi_github_actions_direct_execution_packet.json", packet)
        return "rerun_failed_workflow_run_jobs"
    return "none"


def _write_reobserve_packet(root: pathlib.Path, policy: Mapping[str, Any], pending: list[dict[str, Any]], blockers: list[str]) -> str:
    repo = _repo(policy, blockers)
    commit_sha = str(policy.get("commit_sha", policy.get("expected_head_sha", ""))).strip()
    if not commit_sha:
        blockers.append("commit_sha_missing")
    packet = {
        "reobserve_allowed": True,
        "observation_kind": "commit_workflow_runs",
        "repo_full_name": repo,
        "commit_sha": commit_sha,
        "pending_count": len(pending),
    }
    _write_json(root / "qi_github_actions_status_reobserve_request.json", packet)
    return "commit_workflow_runs_reobserve"


def _direct_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_direct_executor_enabled": True,
        "apply_github_actions_direct_executor": True,
        "runtime_root": str(root),
        "execution_mode": "connector_request",
    }


def _direct_license(action: str) -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_DIRECT_EXECUTOR_LICENSE_READY",
        "direct_execution_packet_read_allowed": True,
        "connector_execution_request_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        f"allow_{action}_action": True,
    }


def _orchestrator_context(root: pathlib.Path, policy: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "qi_github_actions_full_cycle_orchestrator_enabled": True,
        "apply_github_actions_full_cycle_orchestrator": True,
        "runtime_root": str(root),
        "max_full_cycle_phases": _i(policy.get("max_full_cycle_phases", 4), 4),
        "max_loop_steps_per_phase": _i(policy.get("max_loop_steps_per_phase", 5), 5),
    }


def _orchestrator_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_FULL_CYCLE_ORCHESTRATOR_LICENSE_READY",
        "loop_run_allowed": True,
        "external_cycle_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _rec(stage: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage": stage,
        "status": str(payload.get("status", "ok")),
        "digest": _sha(dict(payload)),
        "epoch": int(time.time()),
    }


def build_qi_github_actions_full_cycle_policy_runner(*, runtime_context: Mapping[str, Any], policy_runner_license: Mapping[str, Any]) -> QiGitHubActionsFullCyclePolicyRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(policy_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    policy_path = root / "qi_github_actions_full_cycle_policy_packet.json"
    status_path = root / "qi_github_actions_status_packet.json"
    receipt_path = root / "qi_github_actions_full_cycle_policy_runner_receipt.json"
    audit_path = root / "qi_github_actions_full_cycle_policy_runner_audit.jsonl"

    if ctx.get("qi_github_actions_full_cycle_policy_runner_enabled") is not True:
        blockers.append("qi_github_actions_full_cycle_policy_runner_enabled_not_true")
    if ctx.get("apply_github_actions_full_cycle_policy_runner") is not True:
        blockers.append("apply_github_actions_full_cycle_policy_runner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_FULL_CYCLE_POLICY_RUNNER_LICENSE_READY":
        blockers.append("github_actions_full_cycle_policy_runner_license_not_ready")
    for name in ["policy_packet_read_allowed", "status_packet_read_allowed", "direct_executor_run_allowed", "orchestrator_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    policy = _read_json(policy_path)
    status_packet = _read_json(status_path)
    if not policy:
        blockers.append("policy_packet_missing_or_invalid")
    if policy and policy.get("policy_allowed") is not True:
        blockers.append("policy_packet_allowed_not_true")
    if not status_packet:
        blockers.append("status_packet_missing_or_invalid")
    if status_packet and status_packet.get("github_actions_status_allowed") is not True:
        blockers.append("status_packet_allowed_not_true")

    records: list[dict[str, Any]] = []
    decision = "not_classified"
    action = "none"
    orchestrator_status = "NOT_RUN"
    stop_reason = "not_run"
    if not blockers:
        decision, pending, failed, missing = _classify(status_packet, policy)
        records.append(_rec("policy_classification", {"status": "ok", "decision": decision, "pending": len(pending), "failed": len(failed), "missing": missing}))
        if decision == "policy_all_green" and policy.get("merge_when_green") is True:
            action = _write_direct_packet(root, policy, decision, failed, blockers)
        elif decision == "policy_failed_rerun" and policy.get("rerun_when_failed") is True:
            action = _write_direct_packet(root, policy, decision, failed, blockers)
        elif decision == "policy_pending_reobserve" and policy.get("reobserve_when_pending") is True:
            action = _write_reobserve_packet(root, policy, pending, blockers)
        elif decision in {"policy_missing_required", "policy_hold"}:
            stop_reason = decision
        else:
            stop_reason = "policy_action_not_enabled"

    if not blockers and action in {"merge_pull_request", "rerun_failed_workflow_run_jobs"}:
        direct = build_qi_github_actions_direct_executor(
            runtime_context=_direct_context(root),
            direct_executor_license=_direct_license(action),
        ).to_dict()
        records.append(_rec("v5_6_direct_executor", direct))
        if direct.get("status") != "QI_GITHUB_ACTIONS_DIRECT_EXECUTOR_READY":
            blockers.append("direct_executor_not_ready")
            stop_reason = "direct_executor_blocked"

    if not blockers and stop_reason in {"not_run", "policy_pending_reobserve"}:
        orch = build_qi_github_actions_full_cycle_orchestrator(
            runtime_context=_orchestrator_context(root, policy),
            full_cycle_orchestrator_license=_orchestrator_license(),
        ).to_dict()
        records.append(_rec("v6_8_full_cycle_orchestrator", orch))
        orchestrator_status = str(orch.get("status", "unknown"))
        stop_reason = str(orch.get("stop_reason", stop_reason))
        if orchestrator_status != "QI_GITHUB_ACTIONS_FULL_CYCLE_ORCHESTRATOR_READY":
            blockers.append("full_cycle_orchestrator_not_ready")
            stop_reason = "full_cycle_orchestrator_blocked"

    status = "QI_GITHUB_ACTIONS_FULL_CYCLE_POLICY_RUNNER_READY" if not blockers else "QI_GITHUB_ACTIONS_FULL_CYCLE_POLICY_RUNNER_BLOCKED"
    packet_id = "qi-github-actions-full-cycle-policy-" + _sha({"decision": decision, "action": action, "records": records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_full_cycle_policy_runner_v6_9",
        "status": status,
        "packet_id": packet_id,
        "policy_decision": decision,
        "action_prepared": action,
        "orchestrator_status": orchestrator_status,
        "stop_reason": stop_reason,
        "policy_records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsFullCyclePolicyRunnerResult(
        "kuuos_runtime_daemon_qi_github_actions_full_cycle_policy_runner_v6_9",
        status,
        packet_id,
        str(root),
        decision,
        action,
        orchestrator_status,
        stop_reason,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
        records,
    )
