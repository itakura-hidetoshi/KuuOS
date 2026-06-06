#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


@dataclass(frozen=True)
class QiGitHubActionsPolicyReentryEvaluatorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    evaluation_state: str
    action_prepared: str
    connector_action: str
    evaluation_packet_path: str
    handoff_packet_path: str
    external_call_packet_path: str
    receipt_path: str
    audit_path: str
    evaluation_packet_written: bool
    handoff_packet_written: bool
    external_call_packet_written: bool
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


def _runs(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = source.get("workflow_runs")
    if not isinstance(raw, list):
        status = _m(source.get("status_summary"))
        raw = status.get("workflow_runs")
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _status_summary(runs: list[Mapping[str, Any]], fallback: Mapping[str, Any]) -> dict[str, Any]:
    if not runs and fallback:
        return dict(fallback)
    conclusions = [str(run.get("conclusion")) for run in runs if run.get("conclusion") is not None]
    statuses = [str(run.get("status")) for run in runs]
    all_completed = bool(runs) and all(status == "completed" for status in statuses)
    any_failed = any(conclusion in {"failure", "cancelled", "timed_out"} for conclusion in conclusions)
    all_success = bool(runs) and all_completed and all(conclusion == "success" for conclusion in conclusions)
    any_pending = any(status != "completed" for status in statuses) or not all_completed
    return {
        "all_completed": all_completed,
        "all_success": all_success,
        "any_failed": any_failed,
        "any_pending": any_pending,
        "workflow_run_count": len(runs),
        "workflow_runs": [dict(run) for run in runs],
        "epoch": int(time.time()),
    }


def _query_context(packet: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    ctx = dict(_m(packet.get("query_context")))
    repo = str(ctx.get("repo_full_name") or ctx.get("repository_full_name") or "").strip()
    pr_number = _i(ctx.get("pr_number", ctx.get("pull_number")), 0)
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    if pr_number <= 0:
        blockers.append("pr_number_invalid")
    return {
        "repo_full_name": repo,
        "pr_number": pr_number,
        "required_workflows": list(ctx.get("required_workflows", [])) if isinstance(ctx.get("required_workflows"), list) else [],
        "merge_when_green": ctx.get("merge_when_green", True) is True,
        "rerun_when_failed": ctx.get("rerun_when_failed", True) is True,
        "reobserve_when_pending": ctx.get("reobserve_when_pending", True) is True,
        "source_query_digest": str(ctx.get("source_query_digest", "")),
    }


def _validate_reentry(packet: Mapping[str, Any], blockers: list[str]) -> None:
    if packet.get("policy_reentry_allowed") is not True:
        blockers.append("policy_reentry_allowed_not_true")
    if packet.get("reentry_state") != "policy_reentry_ready":
        blockers.append("reentry_state_not_policy_reentry_ready")
    status = _m(packet.get("status_summary"))
    runs = _runs(packet)
    if not status:
        blockers.append("status_summary_missing_or_invalid")
    if not runs and not status:
        blockers.append("workflow_runs_empty_or_invalid")


def _failed_run_id(runs: list[Mapping[str, Any]]) -> int:
    for run in runs:
        if str(run.get("status")) == "completed" and str(run.get("conclusion")) in {"failure", "cancelled", "timed_out"}:
            rid = _i(run.get("id"), 0)
            if rid > 0:
                return rid
    return 0


def _evaluation_state(status: Mapping[str, Any], runs: list[Mapping[str, Any]], query: Mapping[str, Any]) -> tuple[str, str, str, list[str]]:
    warnings: list[str] = []
    if status.get("all_success") is True:
        if query.get("merge_when_green") is True:
            return "pr_info_refresh_required", "merge_pull_request", "GitHub.get_pr_info", warnings
        return "green_hold", "none", "none", warnings
    if status.get("any_failed") is True:
        if query.get("rerun_when_failed") is True:
            if _failed_run_id(runs) <= 0:
                warnings.append("failed_run_id_missing")
                return "failed_reobserve_required", "commit_workflow_runs_reobserve", "GitHub.fetch_commit_workflow_runs", warnings
            return "rerun_ready", "rerun_failed_workflow_run_jobs", "none", warnings
        return "failed_hold", "none", "none", warnings
    if status.get("any_pending") is True or status.get("all_completed") is not True:
        if query.get("reobserve_when_pending") is True:
            return "pending_reobserve_required", "commit_workflow_runs_reobserve", "GitHub.fetch_commit_workflow_runs", warnings
        return "pending_hold", "none", "none", warnings
    return "hold_unknown_status", "none", "none", warnings


def _live_query_packet(query: Mapping[str, Any], status: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "query_allowed": True,
        "repo_full_name": query["repo_full_name"],
        "pr_number": query["pr_number"],
        "required_workflows": list(query.get("required_workflows", [])),
        "merge_when_green": query.get("merge_when_green", True),
        "rerun_when_failed": query.get("rerun_when_failed", True),
        "reobserve_when_pending": query.get("reobserve_when_pending", True),
        "source": "policy_reentry_evaluator_v10_1",
        "source_status_digest": _sha(dict(status)),
        "epoch": int(time.time()),
    }


def _handoff_packet(state: str, decision: str, action: str, reentry: Mapping[str, Any], status: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_policy_reentry_handoff_packet_v10_1",
        "handoff_allowed": True,
        "autopilot_state": "policy_ready",
        "policy_decision": decision,
        "action_prepared": action,
        "reentry_evaluation_state": state,
        "source_reentry_digest": _sha(dict(reentry)),
        "source_status_digest": _sha(dict(status)),
        "boundary": {
            "handoff_only": True,
            "does_not_call_connector_inside_runtime": True,
            "does_not_apply_policy_action": True,
            "feeds_v8_6_policy_action_handoff": True,
        },
        "epoch": int(time.time()),
    }


def _external_call_packet(action: str, query: Mapping[str, Any], status: Mapping[str, Any]) -> dict[str, Any]:
    if action == "GitHub.get_pr_info":
        payload = {"repository_full_name": query["repo_full_name"], "pr_number": query["pr_number"]}
        expected_file = "qi_github_actions_policy_reentry_pr_info_raw_result_packet.json"
    else:
        payload = {"repo_full_name": query["repo_full_name"], "commit_sha": str(status.get("commit_sha", ""))}
        expected_file = "qi_github_actions_policy_reentry_workflow_runs_raw_result_packet.json"
    return {
        "version": "qi_github_actions_policy_reentry_external_call_packet_v10_1",
        "external_call_allowed": True,
        "connector_action": action,
        "connector_payload": payload,
        "external_result_expected_file": expected_file,
        "source_status_digest": _sha(dict(status)),
        "boundary": {
            "packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "result_must_be_ingested_by_followup_bridge": True,
        },
        "epoch": int(time.time()),
    }


def _evaluation_packet(state: str, action: str, connector: str, query: Mapping[str, Any], status: Mapping[str, Any], runs: list[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_policy_reentry_evaluation_packet_v10_1",
        "evaluation_allowed": True,
        "evaluation_state": state,
        "action_prepared": action,
        "connector_action": connector,
        "query_context": dict(query),
        "status_summary": dict(status),
        "failed_run_id": _failed_run_id(runs),
        "workflow_runs": [dict(run) for run in runs],
        "boundary": {
            "evaluation_only": True,
            "does_not_call_connector_inside_runtime": True,
            "does_not_apply_policy_action": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_policy_reentry_evaluator(*, runtime_context: Mapping[str, Any], policy_reentry_evaluator_license: Mapping[str, Any]) -> QiGitHubActionsPolicyReentryEvaluatorResult:
    ctx = _m(runtime_context)
    lic = _m(policy_reentry_evaluator_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)

    reentry_path = root / "qi_github_actions_policy_reentry_packet.json"
    live_query_path = root / "qi_github_actions_pr_live_query_packet.json"
    status_path = root / "qi_github_actions_status_packet.json"
    evaluation_path = root / "qi_github_actions_policy_reentry_evaluation_packet.json"
    handoff_path = root / "qi_github_actions_pr_live_autopilot_handoff_packet.json"
    external_call_path = root / "qi_github_actions_policy_reentry_external_call_packet.json"
    receipt_path = root / "qi_github_actions_policy_reentry_evaluator_receipt.json"
    audit_path = root / "qi_github_actions_policy_reentry_evaluator_audit.jsonl"

    if ctx.get("qi_github_actions_policy_reentry_evaluator_enabled") is not True:
        blockers.append("qi_github_actions_policy_reentry_evaluator_enabled_not_true")
    if ctx.get("apply_github_actions_policy_reentry_evaluator") is not True:
        blockers.append("apply_github_actions_policy_reentry_evaluator_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_POLICY_REENTRY_EVALUATOR_LICENSE_READY":
        blockers.append("github_actions_policy_reentry_evaluator_license_not_ready")
    for name in ["policy_reentry_packet_read_allowed", "evaluation_packet_write_allowed", "handoff_packet_write_allowed", "external_call_packet_write_allowed", "live_query_packet_write_allowed", "status_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    reentry = _read_json(reentry_path)
    if not reentry:
        blockers.append("policy_reentry_packet_missing_or_invalid")
    if reentry:
        _validate_reentry(reentry, blockers)
    query = _query_context(reentry, blockers) if reentry else {}
    runs = _runs(reentry) if reentry else []
    status_summary = _status_summary(runs, _m(reentry.get("status_summary")) if reentry else {})
    state = "blocked"
    action_prepared = "none"
    connector_action = "none"
    evaluation_packet: dict[str, Any] = {}
    handoff_packet: dict[str, Any] = {}
    external_packet: dict[str, Any] = {}
    evaluation_written = False
    handoff_written = False
    external_written = False

    if not blockers:
        state, action_prepared, connector_action, extra_warnings = _evaluation_state(status_summary, runs, query)
        warnings.extend(extra_warnings)
        evaluation_packet = _evaluation_packet(state, action_prepared, connector_action, query, status_summary, runs)
        _write_json(evaluation_path, evaluation_packet)
        _write_json(live_query_path, _live_query_packet(query, status_summary))
        _write_json(status_path, status_summary)
        evaluation_written = True
        if action_prepared in {"rerun_failed_workflow_run_jobs", "commit_workflow_runs_reobserve"}:
            decision = "policy_failed_rerun" if action_prepared == "rerun_failed_workflow_run_jobs" else "policy_pending_reobserve"
            handoff_packet = _handoff_packet(state, decision, action_prepared, reentry, status_summary)
            _write_json(handoff_path, handoff_packet)
            handoff_written = True
        if connector_action != "none":
            external_packet = _external_call_packet(connector_action, query, status_summary)
            _write_json(external_call_path, external_packet)
            external_written = True

    status = "QI_GITHUB_ACTIONS_POLICY_REENTRY_EVALUATOR_READY" if not blockers else "QI_GITHUB_ACTIONS_POLICY_REENTRY_EVALUATOR_BLOCKED"
    packet_id = "qi-github-actions-policy-reentry-evaluator-" + _sha({"reentry": reentry, "state": state, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_policy_reentry_evaluator_v10_1",
        "status": status,
        "packet_id": packet_id,
        "evaluation_state": state,
        "action_prepared": action_prepared,
        "connector_action": connector_action,
        "evaluation_packet_written": evaluation_written,
        "handoff_packet_written": handoff_written,
        "external_call_packet_written": external_written,
        "evaluation_packet_digest": _sha(evaluation_packet),
        "handoff_packet_digest": _sha(handoff_packet),
        "external_call_packet_digest": _sha(external_packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPolicyReentryEvaluatorResult(
        "kuuos_runtime_daemon_qi_github_actions_policy_reentry_evaluator_v10_1",
        status,
        packet_id,
        str(root),
        state,
        action_prepared,
        connector_action,
        str(evaluation_path),
        str(handoff_path),
        str(external_call_path),
        str(receipt_path),
        str(audit_path),
        evaluation_written,
        handoff_written,
        external_written,
        blockers,
        warnings,
    )
