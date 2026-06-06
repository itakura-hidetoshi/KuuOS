#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ALLOWED_GITHUB_ACTIONS_DIRECT_ACTIONS = {
    "workflow_dispatch",
    "rerun_failed_workflow_run_jobs",
    "rerun_workflow_job",
    "merge_pull_request",
}


@dataclass(frozen=True)
class QiGitHubActionsDirectExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    action: str
    connector_action: str
    execution_mode: str
    execution_request_path: str
    receipt_path: str
    audit_path: str
    execution_request_emitted: bool
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


def _connector_action_for(action: str) -> str:
    if action == "rerun_failed_workflow_run_jobs":
        return "GitHub.rerun_failed_workflow_run_jobs"
    if action == "rerun_workflow_job":
        return "GitHub.rerun_workflow_job"
    if action == "merge_pull_request":
        return "GitHub.merge_pull_request"
    if action == "workflow_dispatch":
        return "GitHub.workflow_dispatch_or_repository_dispatch"
    return "unknown"


def _validate_payload(action: str, packet: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    repo = str(packet.get("repo_full_name", "")).strip()
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    if action == "rerun_failed_workflow_run_jobs":
        run_id = _i(packet.get("run_id"), 0)
        if run_id <= 0:
            blockers.append("run_id_invalid")
        return {"repo_full_name": repo, "run_id": run_id}
    if action == "rerun_workflow_job":
        job_id = _i(packet.get("job_id"), 0)
        if job_id <= 0:
            blockers.append("job_id_invalid")
        return {"repo_full_name": repo, "job_id": job_id}
    if action == "merge_pull_request":
        pr_number = _i(packet.get("pr_number", packet.get("pull_number")), 0)
        if pr_number <= 0:
            blockers.append("pr_number_invalid")
        payload: dict[str, Any] = {"repository_full_name": repo, "pr_number": pr_number}
        for key in ["merge_method", "commit_title", "commit_message", "expected_head_sha"]:
            if packet.get(key) is not None:
                payload[key] = packet.get(key)
        return payload
    if action == "workflow_dispatch":
        workflow = str(packet.get("workflow_id_or_file", "")).strip()
        ref = str(packet.get("ref", "")).strip()
        if not workflow:
            blockers.append("workflow_id_or_file_missing")
        if not ref:
            blockers.append("ref_missing")
        return {"repo_full_name": repo, "workflow_id_or_file": workflow, "ref": ref, "inputs": dict(_m(packet.get("inputs")))}
    blockers.append("direct_action_not_allowlisted")
    return {}


def build_qi_github_actions_direct_executor(*, runtime_context: Mapping[str, Any], direct_executor_license: Mapping[str, Any]) -> QiGitHubActionsDirectExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(direct_executor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "qi_github_actions_direct_execution_packet.json"
    request_path = root / "qi_github_actions_connector_execution_request.json"
    receipt_path = root / "qi_github_actions_direct_executor_receipt.json"
    audit_path = root / "qi_github_actions_direct_executor_audit.jsonl"

    if ctx.get("qi_github_actions_direct_executor_enabled") is not True:
        blockers.append("qi_github_actions_direct_executor_enabled_not_true")
    if ctx.get("apply_github_actions_direct_executor") is not True:
        blockers.append("apply_github_actions_direct_executor_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_DIRECT_EXECUTOR_LICENSE_READY":
        blockers.append("github_actions_direct_executor_license_not_ready")
    for name in ["direct_execution_packet_read_allowed", "connector_execution_request_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(packet_path)
    if not packet:
        blockers.append("direct_execution_packet_missing_or_invalid")
    if packet and packet.get("direct_execution_allowed") is not True:
        blockers.append("direct_execution_packet_allowed_not_true")
    action = str(packet.get("action", "unknown")) if packet else "unknown"
    if action not in ALLOWED_GITHUB_ACTIONS_DIRECT_ACTIONS:
        blockers.append("direct_action_not_allowlisted")
    if lic.get(f"allow_{action}_action") is not True:
        blockers.append(f"{action}_not_allowed_by_direct_executor_license")
    execution_mode = str(packet.get("execution_mode", ctx.get("execution_mode", "connector_request"))) if packet else "connector_request"
    if execution_mode not in {"connector_request", "dry_run"}:
        blockers.append("execution_mode_not_allowlisted")
    connector_action = _connector_action_for(action)
    connector_payload = _validate_payload(action, packet, blockers) if packet else {}

    execution_request = {
        "version": "qi_github_actions_connector_execution_request_v5_6",
        "action": action,
        "connector_action": connector_action,
        "connector_payload": connector_payload,
        "execution_mode": execution_mode,
        "execute_now_allowed_by_packet": packet.get("execute_now_allowed_by_packet") is True if packet else False,
        "direct_execution_supported": True,
        "epoch": int(time.time()),
    }
    execution_request_emitted = False
    if not blockers:
        _write_json(request_path, execution_request)
        execution_request_emitted = True
    status = "QI_GITHUB_ACTIONS_DIRECT_EXECUTOR_READY" if not blockers else "QI_GITHUB_ACTIONS_DIRECT_EXECUTOR_BLOCKED"
    packet_id = "qi-github-actions-direct-executor-" + _sha({"packet": packet, "request": execution_request, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_direct_executor_v5_6",
        "status": status,
        "packet_id": packet_id,
        "action": action,
        "connector_action": connector_action,
        "execution_mode": execution_mode,
        "execution_request_path": str(request_path),
        "execution_request_emitted": execution_request_emitted,
        "request_digest": _sha(execution_request),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsDirectExecutorResult(
        "kuuos_runtime_daemon_qi_github_actions_direct_executor_v5_6",
        status,
        packet_id,
        str(root),
        action,
        connector_action,
        execution_mode,
        str(request_path),
        str(receipt_path),
        str(audit_path),
        execution_request_emitted,
        blockers,
        warnings,
    )
