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
class QiGitHubActionsPolicyReentryAdapterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    reentry_state: str
    workflow_run_count: int
    raw_workflow_runs_path: str
    status_packet_path: str
    reentry_packet_path: str
    receipt_path: str
    audit_path: str
    raw_workflow_runs_written: bool
    status_packet_written: bool
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
    raw = packet.get("workflow_runs")
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _status_summary(runs: list[Mapping[str, Any]]) -> dict[str, Any]:
    conclusions = [str(run.get("conclusion")) for run in runs if run.get("conclusion") is not None]
    statuses = [str(run.get("status")) for run in runs]
    all_completed = bool(runs) and all(status == "completed" for status in statuses)
    any_failed = any(conclusion in {"failure", "cancelled", "timed_out"} for conclusion in conclusions)
    all_success = bool(runs) and all_completed and all(conclusion == "success" for conclusion in conclusions)
    any_pending = any(status not in {"completed"} for status in statuses)
    return {
        "all_completed": all_completed,
        "all_success": all_success,
        "any_failed": any_failed,
        "any_pending": any_pending,
        "workflow_run_count": len(runs),
        "workflow_runs": [dict(run) for run in runs],
        "epoch": int(time.time()),
    }


def _validate_reentry(packet: Mapping[str, Any], blockers: list[str]) -> list[dict[str, Any]]:
    if packet.get("reentry_bridge_allowed") is not True:
        blockers.append("reentry_bridge_allowed_not_true")
    if packet.get("bridge_state") != "policy_reentry_bridge_ready":
        blockers.append("bridge_state_not_policy_reentry_bridge_ready")
    runs = _workflow_runs(packet)
    if not runs:
        blockers.append("workflow_runs_empty_or_invalid")
    status = _m(packet.get("status_summary"))
    if not status:
        blockers.append("status_summary_missing_or_invalid")
    return runs


def _query_context(query: Mapping[str, Any], autopilot_query: Mapping[str, Any]) -> dict[str, Any]:
    source = dict(query) if query else dict(autopilot_query)
    if not source:
        return {}
    return {
        "repo_full_name": source.get("repo_full_name") or source.get("repository_full_name"),
        "pr_number": source.get("pr_number") or source.get("pull_number"),
        "required_workflows": source.get("required_workflows", []),
        "merge_when_green": source.get("merge_when_green", True),
        "rerun_when_failed": source.get("rerun_when_failed", True),
        "reobserve_when_pending": source.get("reobserve_when_pending", True),
        "source_query_digest": _sha(source),
    }


def _raw_workflow_packet(reentry: Mapping[str, Any], runs: list[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_policy_reentry_raw_workflow_runs_v9_9",
        "workflow_runs": [dict(run) for run in runs],
        "required_workflows": [str(run.get("name")) for run in runs if run.get("name")],
        "source_reentry_bridge_digest": _sha(dict(reentry)),
        "epoch": int(time.time()),
    }


def _policy_reentry_packet(reentry: Mapping[str, Any], query_ctx: Mapping[str, Any], status: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_policy_reentry_packet_v9_9",
        "policy_reentry_allowed": True,
        "reentry_state": "policy_reentry_ready",
        "query_context": dict(query_ctx),
        "status_summary": dict(status),
        "next_runner": "kuuos_runtime_daemon_qi_github_actions_cycle_aware_super_executor_v9_6",
        "source_reentry_bridge_digest": _sha(dict(reentry)),
        "boundary": {
            "adapter_only": True,
            "does_not_call_connector_inside_runtime": True,
            "does_not_apply_policy_action": True,
            "feeds_pr_live_policy_surface": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_policy_reentry_adapter(*, runtime_context: Mapping[str, Any], policy_reentry_adapter_license: Mapping[str, Any]) -> QiGitHubActionsPolicyReentryAdapterResult:
    ctx = _m(runtime_context)
    lic = _m(policy_reentry_adapter_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)

    reentry_bridge_path = root / "qi_github_actions_next_cycle_reentry_bridge_packet.json"
    live_query_path = root / "qi_github_actions_pr_live_query_packet.json"
    autopilot_query_path = root / "qi_github_actions_pr_live_autopilot_query_packet.json"
    raw_workflow_path = root / "qi_github_actions_raw_commit_workflow_runs_packet.json"
    status_path = root / "qi_github_actions_status_packet.json"
    reentry_packet_path = root / "qi_github_actions_policy_reentry_packet.json"
    receipt_path = root / "qi_github_actions_policy_reentry_adapter_receipt.json"
    audit_path = root / "qi_github_actions_policy_reentry_adapter_audit.jsonl"

    if ctx.get("qi_github_actions_policy_reentry_adapter_enabled") is not True:
        blockers.append("qi_github_actions_policy_reentry_adapter_enabled_not_true")
    if ctx.get("apply_github_actions_policy_reentry_adapter") is not True:
        blockers.append("apply_github_actions_policy_reentry_adapter_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_POLICY_REENTRY_ADAPTER_LICENSE_READY":
        blockers.append("github_actions_policy_reentry_adapter_license_not_ready")
    for name in ["reentry_bridge_packet_read_allowed", "context_packet_read_allowed", "raw_workflow_packet_write_allowed", "status_packet_write_allowed", "policy_reentry_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    reentry_bridge = _read_json(reentry_bridge_path)
    live_query = _read_json(live_query_path)
    autopilot_query = _read_json(autopilot_query_path)
    if not reentry_bridge:
        blockers.append("reentry_bridge_packet_missing_or_invalid")
    runs = _validate_reentry(reentry_bridge, blockers) if reentry_bridge else []
    query_ctx = _query_context(live_query, autopilot_query)
    if not query_ctx:
        warnings.append("query_context_missing")

    raw_packet: dict[str, Any] = {}
    status_packet: dict[str, Any] = {}
    reentry_packet: dict[str, Any] = {}
    raw_written = False
    status_written = False
    reentry_written = False
    reentry_state = "blocked"
    if not blockers:
        raw_packet = _raw_workflow_packet(reentry_bridge, runs)
        status_packet = _status_summary(runs)
        reentry_packet = _policy_reentry_packet(reentry_bridge, query_ctx, status_packet)
        _write_json(raw_workflow_path, raw_packet)
        _write_json(status_path, status_packet)
        _write_json(reentry_packet_path, reentry_packet)
        raw_written = True
        status_written = True
        reentry_written = True
        reentry_state = "policy_reentry_ready"

    status = "QI_GITHUB_ACTIONS_POLICY_REENTRY_ADAPTER_READY" if not blockers else "QI_GITHUB_ACTIONS_POLICY_REENTRY_ADAPTER_BLOCKED"
    packet_id = "qi-github-actions-policy-reentry-adapter-" + _sha({"reentry": reentry_bridge, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_policy_reentry_adapter_v9_9",
        "status": status,
        "packet_id": packet_id,
        "reentry_state": reentry_state,
        "workflow_run_count": len(runs),
        "raw_workflow_runs_written": raw_written,
        "status_packet_written": status_written,
        "reentry_packet_written": reentry_written,
        "raw_workflow_runs_digest": _sha(raw_packet),
        "status_packet_digest": _sha(status_packet),
        "reentry_packet_digest": _sha(reentry_packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPolicyReentryAdapterResult(
        "kuuos_runtime_daemon_qi_github_actions_policy_reentry_adapter_v9_9",
        status,
        packet_id,
        str(root),
        reentry_state,
        len(runs),
        str(raw_workflow_path),
        str(status_path),
        str(reentry_packet_path),
        str(receipt_path),
        str(audit_path),
        raw_written,
        status_written,
        reentry_written,
        blockers,
        warnings,
    )
