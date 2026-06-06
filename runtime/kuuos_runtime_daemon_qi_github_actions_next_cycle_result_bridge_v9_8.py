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
class QiGitHubActionsNextCycleResultBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_state: str
    connector_action: str
    result_packet_path: str
    reentry_bridge_path: str
    receipt_path: str
    audit_path: str
    result_packet_written: bool
    reentry_bridge_written: bool
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


def _payload(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = raw.get("connector_result")
    return nested if isinstance(nested, Mapping) else raw


def _workflow_runs(raw: Mapping[str, Any]) -> list[dict[str, Any]]:
    payload = _payload(raw)
    runs = payload.get("workflow_runs")
    if not isinstance(runs, list):
        return []
    return [dict(item) for item in runs if isinstance(item, Mapping)]


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


def _validate_call(call: Mapping[str, Any], blockers: list[str]) -> None:
    if call.get("external_call_allowed") is not True:
        blockers.append("external_call_allowed_not_true")
    if call.get("bridge_state") != "next_cycle_external_call_ready":
        blockers.append("bridge_state_not_next_cycle_external_call_ready")
    if call.get("connector_action") != "GitHub.fetch_commit_workflow_runs":
        blockers.append("connector_action_mismatch")
    payload = _m(call.get("connector_payload"))
    repo = payload.get("repo_full_name") or payload.get("repository_full_name")
    if not isinstance(repo, str) or "/" not in repo:
        blockers.append("repo_full_name_invalid")
    if not str(payload.get("commit_sha", "")).strip():
        blockers.append("commit_sha_missing")


def _validate_raw(call: Mapping[str, Any], raw: Mapping[str, Any], blockers: list[str]) -> list[dict[str, Any]]:
    raw_action = str(raw.get("connector_action", call.get("connector_action", "")))
    if raw_action != "GitHub.fetch_commit_workflow_runs":
        blockers.append("raw_result_connector_action_mismatch")
    runs = _workflow_runs(raw)
    if not runs:
        blockers.append("workflow_runs_empty_or_invalid")
    return runs


def _result_packet(call: Mapping[str, Any], raw: Mapping[str, Any], runs: list[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_next_cycle_external_result_packet_v9_8",
        "external_result_allowed": True,
        "bridge_state": "next_cycle_external_result_ready",
        "connector_action": "GitHub.fetch_commit_workflow_runs",
        "workflow_runs": [dict(run) for run in runs],
        "status_summary": _status_summary(runs),
        "source_external_call_digest": _sha(dict(call)),
        "source_raw_result_digest": _sha(dict(raw)),
        "boundary": {
            "result_packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "feeds_reentry_bridge": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def _reentry_bridge(result_packet: Mapping[str, Any]) -> dict[str, Any]:
    runs = result_packet.get("workflow_runs")
    runs_list = [dict(run) for run in runs] if isinstance(runs, list) else []
    status = _m(result_packet.get("status_summary"))
    return {
        "version": "qi_github_actions_next_cycle_reentry_bridge_packet_from_result_v9_8",
        "reentry_bridge_allowed": True,
        "bridge_state": "policy_reentry_bridge_ready",
        "workflow_runs": runs_list,
        "status_summary": dict(status),
        "next_runner": "kuuos_runtime_daemon_qi_github_actions_cycle_aware_super_executor_v9_6",
        "source_external_result_digest": _sha(dict(result_packet)),
        "boundary": {
            "reentry_packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "feeds_policy_reentry_surface": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_next_cycle_result_bridge(*, runtime_context: Mapping[str, Any], next_cycle_result_bridge_license: Mapping[str, Any]) -> QiGitHubActionsNextCycleResultBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(next_cycle_result_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)

    call_path = root / "qi_github_actions_next_cycle_external_call_packet.json"
    raw_path = root / "qi_github_actions_next_cycle_external_call_raw_result_packet.json"
    result_path = root / "qi_github_actions_next_cycle_external_result_packet.json"
    workflow_path = root / "qi_github_actions_raw_commit_workflow_runs_packet.json"
    status_path = root / "qi_github_actions_status_packet.json"
    reentry_path = root / "qi_github_actions_next_cycle_reentry_bridge_packet.json"
    receipt_path = root / "qi_github_actions_next_cycle_result_bridge_receipt.json"
    audit_path = root / "qi_github_actions_next_cycle_result_bridge_audit.jsonl"

    if ctx.get("qi_github_actions_next_cycle_result_bridge_enabled") is not True:
        blockers.append("qi_github_actions_next_cycle_result_bridge_enabled_not_true")
    if ctx.get("apply_github_actions_next_cycle_result_bridge") is not True:
        blockers.append("apply_github_actions_next_cycle_result_bridge_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_NEXT_CYCLE_RESULT_BRIDGE_LICENSE_READY":
        blockers.append("github_actions_next_cycle_result_bridge_license_not_ready")
    for name in ["external_call_packet_read_allowed", "raw_result_packet_read_allowed", "result_packet_write_allowed", "reentry_bridge_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    call = _read_json(call_path)
    raw = _read_json(raw_path)
    if not call:
        blockers.append("external_call_packet_missing_or_invalid")
    if not raw:
        blockers.append("raw_result_packet_missing_or_invalid")
    if call:
        _validate_call(call, blockers)
    runs: list[dict[str, Any]] = []
    if call and raw:
        runs = _validate_raw(call, raw, blockers)

    result_packet: dict[str, Any] = {}
    reentry_packet: dict[str, Any] = {}
    result_written = False
    reentry_written = False
    bridge_state = "blocked"
    if not blockers:
        result_packet = _result_packet(call, raw, runs)
        reentry_packet = _reentry_bridge(result_packet)
        _write_json(result_path, result_packet)
        _write_json(workflow_path, {"version": "qi_github_actions_next_cycle_feedback_workflow_runs_v9_8", "workflow_runs": runs, "source_external_result_digest": _sha(result_packet), "epoch": int(time.time())})
        _write_json(status_path, dict(result_packet["status_summary"]))
        _write_json(reentry_path, reentry_packet)
        result_written = True
        reentry_written = True
        bridge_state = "policy_reentry_bridge_ready"

    status = "QI_GITHUB_ACTIONS_NEXT_CYCLE_RESULT_BRIDGE_READY" if not blockers else "QI_GITHUB_ACTIONS_NEXT_CYCLE_RESULT_BRIDGE_BLOCKED"
    packet_id = "qi-github-actions-next-cycle-result-bridge-" + _sha({"call": call, "raw": raw, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_next_cycle_result_bridge_v9_8",
        "status": status,
        "packet_id": packet_id,
        "bridge_state": bridge_state,
        "connector_action": "GitHub.fetch_commit_workflow_runs",
        "result_packet_written": result_written,
        "reentry_bridge_written": reentry_written,
        "result_packet_digest": _sha(result_packet),
        "reentry_bridge_digest": _sha(reentry_packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsNextCycleResultBridgeResult(
        "kuuos_runtime_daemon_qi_github_actions_next_cycle_result_bridge_v9_8",
        status,
        packet_id,
        str(root),
        bridge_state,
        "GitHub.fetch_commit_workflow_runs",
        str(result_path),
        str(reentry_path),
        str(receipt_path),
        str(audit_path),
        result_written,
        reentry_written,
        blockers,
        warnings,
    )
