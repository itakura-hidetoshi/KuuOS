#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_pr_live_snapshot_collector_v7_4 import build_qi_github_actions_pr_live_snapshot_collector


@dataclass(frozen=True)
class QiGitHubActionsPrLiveRequestPlannerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    planner_stage: str
    request_action: str
    collector_status: str
    policy_decision: str
    action_prepared: str
    stop_reason: str
    request_packet_path: str
    receipt_path: str
    audit_path: str
    request_packet_written: bool
    blockers: list[str]
    warnings: list[str]

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


def _repo(query: Mapping[str, Any], blockers: list[str]) -> str:
    repo = str(query.get("repo_full_name", query.get("repository_full_name", ""))).strip()
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    return repo


def _pr_number(query: Mapping[str, Any], blockers: list[str]) -> int:
    number = _i(query.get("pr_number", query.get("pull_number")), 0)
    if number <= 0:
        blockers.append("pr_number_invalid")
    return number


def _head_sha(raw_pr: Mapping[str, Any], query: Mapping[str, Any], blockers: list[str]) -> str:
    nested = raw_pr.get("head")
    nested_sha = nested.get("sha") if isinstance(nested, Mapping) else ""
    sha = str(query.get("head_sha") or query.get("expected_head_sha") or raw_pr.get("head_sha") or nested_sha or "").strip()
    if not sha:
        blockers.append("head_sha_missing")
    return sha


def _write_policy_config(root: pathlib.Path, query: Mapping[str, Any]) -> None:
    config = dict(_m(query.get("policy_config")))
    for key in [
        "adapter_allowed",
        "required_workflows",
        "merge_when_green",
        "rerun_when_failed",
        "reobserve_when_pending",
        "merge_method",
        "base_branch",
        "repo_full_name",
        "pr_number",
        "head_sha",
        "expected_head_sha",
        "commit_sha",
    ]:
        if key in query and key not in config:
            config[key] = query[key]
    config.setdefault("adapter_allowed", True)
    _write_json(root / "qi_github_actions_pr_live_policy_config.json", config)


def _pr_info_request(query: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_pr_info_connector_request_v7_5",
        "connector_action": "GitHub.get_pr_info",
        "connector_payload": {
            "repository_full_name": _repo(query, blockers),
            "pr_number": _pr_number(query, blockers),
        },
        "result_expected_file": "qi_github_actions_raw_pr_info_packet.json",
        "epoch": int(time.time()),
    }


def _runs_request(query: Mapping[str, Any], raw_pr: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_commit_workflow_runs_connector_request_v7_5",
        "connector_action": "GitHub.fetch_commit_workflow_runs",
        "connector_payload": {
            "repo_full_name": _repo(query, blockers),
            "commit_sha": _head_sha(raw_pr, query, blockers),
        },
        "result_expected_file": "qi_github_actions_raw_commit_workflow_runs_packet.json",
        "epoch": int(time.time()),
    }


def _collector_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_pr_live_snapshot_collector_enabled": True,
        "apply_github_actions_pr_live_snapshot_collector": True,
        "runtime_root": str(root),
    }


def _collector_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_COLLECTOR_LICENSE_READY",
        "raw_pr_info_read_allowed": True,
        "raw_workflow_runs_read_allowed": True,
        "snapshot_packet_write_allowed": True,
        "adapter_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_qi_github_actions_pr_live_request_planner(*, runtime_context: Mapping[str, Any], pr_live_request_planner_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveRequestPlannerResult:
    ctx = _m(runtime_context)
    lic = _m(pr_live_request_planner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    query_path = root / "qi_github_actions_pr_live_query_packet.json"
    raw_pr_path = root / "qi_github_actions_raw_pr_info_packet.json"
    raw_runs_path = root / "qi_github_actions_raw_commit_workflow_runs_packet.json"
    pr_request_path = root / "qi_github_actions_pr_info_connector_request.json"
    runs_request_path = root / "qi_github_actions_commit_workflow_runs_connector_request.json"
    receipt_path = root / "qi_github_actions_pr_live_request_planner_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_request_planner_audit.jsonl"

    if ctx.get("qi_github_actions_pr_live_request_planner_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_request_planner_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_request_planner") is not True:
        blockers.append("apply_github_actions_pr_live_request_planner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_REQUEST_PLANNER_LICENSE_READY":
        blockers.append("github_actions_pr_live_request_planner_license_not_ready")
    for name in ["query_packet_read_allowed", "connector_request_write_allowed", "collector_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    query = _read_json(query_path)
    raw_pr = _read_json(raw_pr_path)
    raw_runs = _read_json(raw_runs_path)
    if not query:
        blockers.append("query_packet_missing_or_invalid")
    if query and query.get("query_allowed") is not True:
        blockers.append("query_allowed_not_true")
    if query:
        _repo(query, blockers)
        _pr_number(query, blockers)

    planner_stage = "blocked"
    request_action = "none"
    collector_status = "NOT_RUN"
    policy_decision = "not_run"
    action_prepared = "none"
    stop_reason = "not_run"
    request_path = root / "qi_github_actions_pr_live_request_blocked.json"
    request_written = False

    if not blockers:
        _write_policy_config(root, query)
        if not raw_pr:
            planner_stage = "request_pr_info"
            request = _pr_info_request(query, blockers)
            request_path = pr_request_path
            if not blockers:
                _write_json(request_path, request)
                request_written = True
                request_action = "GitHub.get_pr_info"
                stop_reason = "await_pr_info"
        elif not raw_runs:
            planner_stage = "request_commit_workflow_runs"
            request = _runs_request(query, raw_pr, blockers)
            request_path = runs_request_path
            if not blockers:
                _write_json(request_path, request)
                request_written = True
                request_action = "GitHub.fetch_commit_workflow_runs"
                stop_reason = "await_commit_workflow_runs"
        else:
            planner_stage = "collect_live_snapshot"
            collector = build_qi_github_actions_pr_live_snapshot_collector(
                runtime_context=_collector_context(root),
                pr_live_snapshot_collector_license=_collector_license(),
            ).to_dict()
            collector_status = str(collector.get("status", "unknown"))
            policy_decision = str(collector.get("policy_decision", "unknown"))
            action_prepared = str(collector.get("action_prepared", "none"))
            stop_reason = str(collector.get("stop_reason", "unknown"))
            if collector_status != "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_COLLECTOR_READY":
                blockers.append("pr_live_snapshot_collector_not_ready")
                stop_reason = "collector_blocked"

    status = "QI_GITHUB_ACTIONS_PR_LIVE_REQUEST_PLANNER_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_REQUEST_PLANNER_BLOCKED"
    packet_id = "qi-github-actions-pr-live-request-planner-" + _sha({"query": query, "stage": planner_stage, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_live_request_planner_v7_5",
        "status": status,
        "packet_id": packet_id,
        "planner_stage": planner_stage,
        "request_action": request_action,
        "collector_status": collector_status,
        "policy_decision": policy_decision,
        "action_prepared": action_prepared,
        "stop_reason": stop_reason,
        "request_packet_written": request_written,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPrLiveRequestPlannerResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_live_request_planner_v7_5",
        status,
        packet_id,
        str(root),
        planner_stage,
        request_action,
        collector_status,
        policy_decision,
        action_prepared,
        stop_reason,
        str(request_path),
        str(receipt_path),
        str(audit_path),
        request_written,
        blockers,
        warnings,
    )
