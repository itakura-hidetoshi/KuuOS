#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ROUTE_BY_FINAL_STATE = {
    "action_completed": "close_autopilot_cycle",
    "action_rerun_requested": "wait_for_new_workflow_runs",
    "action_reobserve_ready": "feed_reobserved_workflow_runs",
}


@dataclass(frozen=True)
class QiGitHubActionsPolicyActionFinalRouterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    final_state: str
    route_state: str
    route_packet_path: str
    receipt_path: str
    audit_path: str
    route_packet_written: bool
    feedback_packets_written: bool
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


def _workflow_runs(receipt: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = receipt.get("connector_result", {}).get("workflow_runs") if isinstance(receipt.get("connector_result"), Mapping) else []
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _validate_receipt(receipt: Mapping[str, Any], blockers: list[str]) -> str:
    if receipt.get("final_receipt_allowed") is not True:
        blockers.append("final_receipt_allowed_not_true")
    state = str(receipt.get("final_state", "unknown"))
    if state not in ROUTE_BY_FINAL_STATE:
        blockers.append("final_state_not_allowlisted")
    if state == "action_reobserve_ready" and not _workflow_runs(receipt):
        blockers.append("workflow_runs_empty_or_invalid")
    return state


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


def _route_packet(receipt: Mapping[str, Any], final_state: str, route_state: str, feedback_written: bool) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_policy_action_final_route_packet_v9_1",
        "route_allowed": True,
        "final_state": final_state,
        "route_state": route_state,
        "feedback_packets_written": feedback_written,
        "next_expected": {
            "close_autopilot_cycle": "autopilot cycle closed after completed policy action",
            "wait_for_new_workflow_runs": "wait, then observe workflow runs for the same head commit",
            "feed_reobserved_workflow_runs": "rerun PR live policy evaluation using reobserved workflow runs",
        }[route_state],
        "source_final_receipt_digest": _sha(dict(receipt)),
        "boundary": {
            "route_only": True,
            "does_not_apply_additional_action": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_policy_action_final_router(*, runtime_context: Mapping[str, Any], policy_action_final_router_license: Mapping[str, Any]) -> QiGitHubActionsPolicyActionFinalRouterResult:
    ctx = _m(runtime_context)
    lic = _m(policy_action_final_router_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    final_receipt_path = root / "qi_github_actions_policy_action_final_receipt_packet.json"
    route_path = root / "qi_github_actions_policy_action_final_route_packet.json"
    workflow_runs_path = root / "qi_github_actions_raw_commit_workflow_runs_packet.json"
    status_packet_path = root / "qi_github_actions_status_packet.json"
    receipt_path = root / "qi_github_actions_policy_action_final_router_receipt.json"
    audit_path = root / "qi_github_actions_policy_action_final_router_audit.jsonl"

    if ctx.get("qi_github_actions_policy_action_final_router_enabled") is not True:
        blockers.append("qi_github_actions_policy_action_final_router_enabled_not_true")
    if ctx.get("apply_github_actions_policy_action_final_router") is not True:
        blockers.append("apply_github_actions_policy_action_final_router_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_ROUTER_LICENSE_READY":
        blockers.append("github_actions_policy_action_final_router_license_not_ready")
    for name in ["final_receipt_packet_read_allowed", "route_packet_write_allowed", "feedback_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    final_receipt = _read_json(final_receipt_path)
    if not final_receipt:
        blockers.append("final_receipt_packet_missing_or_invalid")
    final_state = _validate_receipt(final_receipt, blockers) if final_receipt else "unknown"
    route_state = ROUTE_BY_FINAL_STATE.get(final_state, "unknown")
    feedback_written = False
    route: dict[str, Any] = {}
    route_written = False

    if not blockers:
        if final_state == "action_reobserve_ready":
            runs = _workflow_runs(final_receipt)
            feedback = {
                "version": "qi_github_actions_reobserved_commit_workflow_runs_feedback_v9_1",
                "workflow_runs": runs,
                "required_workflows": [str(run.get("name")) for run in runs if run.get("name")],
                "source_final_receipt_digest": _sha(dict(final_receipt)),
                "epoch": int(time.time()),
            }
            _write_json(workflow_runs_path, feedback)
            _write_json(status_packet_path, _status_summary(runs))
            feedback_written = True
        route = _route_packet(final_receipt, final_state, route_state, feedback_written)
        _write_json(route_path, route)
        route_written = True

    status = "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_ROUTER_READY" if not blockers else "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_ROUTER_BLOCKED"
    packet_id = "qi-github-actions-policy-action-final-router-" + _sha({"final_receipt": final_receipt, "route_state": route_state, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_policy_action_final_router_v9_1",
        "status": status,
        "packet_id": packet_id,
        "final_state": final_state,
        "route_state": route_state,
        "route_packet_written": route_written,
        "feedback_packets_written": feedback_written,
        "route_packet_digest": _sha(route),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPolicyActionFinalRouterResult(
        "kuuos_runtime_daemon_qi_github_actions_policy_action_final_router_v9_1",
        status,
        packet_id,
        str(root),
        final_state,
        route_state,
        str(route_path),
        str(receipt_path),
        str(audit_path),
        route_written,
        feedback_written,
        blockers,
        warnings,
    )
