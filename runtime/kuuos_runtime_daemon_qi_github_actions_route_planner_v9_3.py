#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ALLOWED_ROUTE_STATES = {
    "close_autopilot_cycle",
    "wait_for_new_workflow_runs",
    "feed_reobserved_workflow_runs",
}


@dataclass(frozen=True)
class QiGitHubActionsRoutePlannerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    route_state: str
    next_cycle_state: str
    next_connector_action: str
    next_cycle_packet_path: str
    reobserve_request_path: str
    reentry_packet_path: str
    receipt_path: str
    audit_path: str
    next_cycle_packet_written: bool
    reobserve_request_written: bool
    reentry_packet_written: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


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


def _workflow_runs(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = packet.get("workflow_runs", [])
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _repo(query: Mapping[str, Any], pr: Mapping[str, Any], blockers: list[str]) -> str:
    repo = str(query.get("repo_full_name") or query.get("repository_full_name") or pr.get("repo_full_name") or pr.get("repository_full_name") or "").strip()
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    return repo


def _commit_sha(query: Mapping[str, Any], pr: Mapping[str, Any], blockers: list[str]) -> str:
    head = pr.get("head")
    nested_sha = head.get("sha") if isinstance(head, Mapping) else ""
    sha = str(query.get("commit_sha") or query.get("head_sha") or pr.get("head_sha") or nested_sha or "").strip()
    if not sha:
        blockers.append("commit_sha_missing")
    return sha


def _status_summary(runs: list[Mapping[str, Any]]) -> dict[str, Any]:
    conclusions = [str(run.get("conclusion")) for run in runs if run.get("conclusion") is not None]
    statuses = [str(run.get("status")) for run in runs]
    all_completed = bool(runs) and all(status == "completed" for status in statuses)
    any_failed = any(conclusion in {"failure", "cancelled", "timed_out"} for conclusion in conclusions)
    all_success = bool(runs) and all_completed and all(conclusion == "success" for conclusion in conclusions)
    return {
        "all_completed": all_completed,
        "all_success": all_success,
        "any_failed": any_failed,
        "workflow_run_count": len(runs),
        "workflow_runs": [dict(run) for run in runs],
        "epoch": int(time.time()),
    }


def _validate_route(route: Mapping[str, Any], blockers: list[str]) -> str:
    if route.get("route_allowed") is not True:
        blockers.append("route_allowed_not_true")
    state = str(route.get("route_state", "unknown"))
    if state not in ALLOWED_ROUTE_STATES:
        blockers.append("route_state_not_allowlisted")
    return state


def _next_cycle_packet(route: Mapping[str, Any], route_state: str, next_cycle_state: str, connector_action: str, extra: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_route_next_cycle_packet_v9_3",
        "next_cycle_allowed": True,
        "route_state": route_state,
        "next_cycle_state": next_cycle_state,
        "next_connector_action": connector_action,
        "extra": dict(extra),
        "source_route_digest": _sha(dict(route)),
        "boundary": {
            "planning_only": True,
            "does_not_call_connector_inside_runtime": True,
            "does_not_apply_policy_action": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_route_planner(*, runtime_context: Mapping[str, Any], route_planner_license: Mapping[str, Any]) -> QiGitHubActionsRoutePlannerResult:
    ctx = _m(runtime_context)
    lic = _m(route_planner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)

    route_path = root / "qi_github_actions_policy_action_final_route_packet.json"
    query_path = root / "qi_github_actions_pr_live_query_packet.json"
    pr_path = root / "qi_github_actions_raw_pr_info_packet.json"
    workflow_runs_path = root / "qi_github_actions_raw_commit_workflow_runs_packet.json"
    status_path = root / "qi_github_actions_status_packet.json"
    next_cycle_path = root / "qi_github_actions_route_next_cycle_packet.json"
    reobserve_request_path = root / "qi_github_actions_route_reobserve_request_packet.json"
    reentry_packet_path = root / "qi_github_actions_route_policy_reentry_packet.json"
    receipt_path = root / "qi_github_actions_route_planner_receipt.json"
    audit_path = root / "qi_github_actions_route_planner_audit.jsonl"

    if ctx.get("qi_github_actions_route_planner_enabled") is not True:
        blockers.append("qi_github_actions_route_planner_enabled_not_true")
    if ctx.get("apply_github_actions_route_planner") is not True:
        blockers.append("apply_github_actions_route_planner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_ROUTE_PLANNER_LICENSE_READY":
        blockers.append("github_actions_route_planner_license_not_ready")
    for name in ["route_packet_read_allowed", "context_packet_read_allowed", "next_cycle_packet_write_allowed", "reobserve_request_write_allowed", "reentry_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    route = _read_json(route_path)
    query = _read_json(query_path)
    pr = _read_json(pr_path)
    workflow_packet = _read_json(workflow_runs_path)
    if not route:
        blockers.append("route_packet_missing_or_invalid")
    route_state = _validate_route(route, blockers) if route else "unknown"

    next_cycle_state = "blocked"
    next_connector_action = "none"
    next_packet: dict[str, Any] = {}
    reobserve_request: dict[str, Any] = {}
    reentry_packet: dict[str, Any] = {}
    next_written = False
    request_written = False
    reentry_written = False

    if not blockers:
        if route_state == "close_autopilot_cycle":
            next_cycle_state = "closed"
            next_packet = _next_cycle_packet(route, route_state, next_cycle_state, "none", {"closed": True})
        elif route_state == "wait_for_new_workflow_runs":
            repo = _repo(query, pr, blockers)
            sha = _commit_sha(query, pr, blockers)
            if not blockers:
                next_cycle_state = "await_workflow_reobserve"
                next_connector_action = "GitHub.fetch_commit_workflow_runs"
                reobserve_request = {
                    "version": "qi_github_actions_route_reobserve_request_packet_v9_3",
                    "request_allowed": True,
                    "connector_action": next_connector_action,
                    "connector_payload": {"repo_full_name": repo, "commit_sha": sha},
                    "source_route_digest": _sha(dict(route)),
                    "epoch": int(time.time()),
                }
                next_packet = _next_cycle_packet(route, route_state, next_cycle_state, next_connector_action, {"repo_full_name": repo, "commit_sha": sha})
        elif route_state == "feed_reobserved_workflow_runs":
            runs = _workflow_runs(workflow_packet)
            if not runs:
                blockers.append("workflow_runs_empty_or_invalid")
            else:
                status_summary = _status_summary(runs)
                _write_json(status_path, status_summary)
                next_cycle_state = "reenter_policy_loop"
                reentry_packet = {
                    "version": "qi_github_actions_route_policy_reentry_packet_v9_3",
                    "reentry_allowed": True,
                    "workflow_runs": runs,
                    "status_summary": status_summary,
                    "source_route_digest": _sha(dict(route)),
                    "next_runner": "kuuos_runtime_daemon_qi_github_actions_routed_e2e_orchestrator_v9_2",
                    "epoch": int(time.time()),
                }
                next_packet = _next_cycle_packet(route, route_state, next_cycle_state, "none", {"workflow_run_count": len(runs), "all_success": status_summary["all_success"], "any_failed": status_summary["any_failed"]})

    if not blockers:
        _write_json(next_cycle_path, next_packet)
        next_written = True
        if reobserve_request:
            _write_json(reobserve_request_path, reobserve_request)
            request_written = True
        if reentry_packet:
            _write_json(reentry_packet_path, reentry_packet)
            reentry_written = True

    status = "QI_GITHUB_ACTIONS_ROUTE_PLANNER_READY" if not blockers else "QI_GITHUB_ACTIONS_ROUTE_PLANNER_BLOCKED"
    packet_id = "qi-github-actions-route-planner-" + _sha({"route": route, "route_state": route_state, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_route_planner_v9_3",
        "status": status,
        "packet_id": packet_id,
        "route_state": route_state,
        "next_cycle_state": next_cycle_state,
        "next_connector_action": next_connector_action,
        "next_cycle_packet_written": next_written,
        "reobserve_request_written": request_written,
        "reentry_packet_written": reentry_written,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsRoutePlannerResult(
        "kuuos_runtime_daemon_qi_github_actions_route_planner_v9_3",
        status,
        packet_id,
        str(root),
        route_state,
        next_cycle_state,
        next_connector_action,
        str(next_cycle_path),
        str(reobserve_request_path),
        str(reentry_packet_path),
        str(receipt_path),
        str(audit_path),
        next_written,
        request_written,
        reentry_written,
        blockers,
        warnings,
    )
