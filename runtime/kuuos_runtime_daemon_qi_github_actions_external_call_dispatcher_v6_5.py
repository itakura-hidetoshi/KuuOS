#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


DISPATCH_TARGETS = {
    "GitHub.fetch_commit_workflow_runs": "commit_workflow_runs",
    "GitHub.fetch_workflow_run_jobs": "workflow_run_jobs",
    "GitHub.fetch_workflow_job_steps": "workflow_job_steps",
    "GitHub.fetch_workflow_job_logs": "workflow_job_logs",
    "GitHub.fetch_workflow_run_artifacts": "workflow_run_artifacts",
    "GitHub.rerun_failed_workflow_run_jobs": "rerun_failed_workflow_run_jobs",
    "GitHub.rerun_workflow_job": "rerun_workflow_job",
    "GitHub.merge_pull_request": "merge_pull_request",
}

RESULT_FILE_BY_TARGET = {
    "commit_workflow_runs": "qi_github_actions_observation_connector_result_packet.json",
    "workflow_run_jobs": "qi_github_actions_observation_connector_result_packet.json",
    "workflow_job_steps": "qi_github_actions_observation_connector_result_packet.json",
    "workflow_job_logs": "qi_github_actions_observation_connector_result_packet.json",
    "workflow_run_artifacts": "qi_github_actions_observation_connector_result_packet.json",
    "rerun_failed_workflow_run_jobs": "qi_github_actions_connector_result_packet.json",
    "rerun_workflow_job": "qi_github_actions_connector_result_packet.json",
    "merge_pull_request": "qi_github_actions_connector_result_packet.json",
}


@dataclass(frozen=True)
class QiGitHubActionsExternalCallDispatcherResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    dispatch_target: str
    dispatch_packet_path: str
    receipt_path: str
    audit_path: str
    dispatch_packet_emitted: bool
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


def _dispatch_file(target: str) -> str:
    return f"qi_github_actions_dispatch_{target}_packet.json"


def _dispatch_packet(call: Mapping[str, Any], target: str) -> dict[str, Any]:
    payload = dict(_m(call.get("connector_payload")))
    return {
        "version": "qi_github_actions_external_call_dispatch_packet_v6_5",
        "dispatch_target": target,
        "connector_action": str(call.get("connector_action", "unknown")),
        "connector_payload": payload,
        "result_expected_file": RESULT_FILE_BY_TARGET[target],
        "source_external_call_digest": _sha(dict(call)),
        "boundary": {
            "dispatch_packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "target_specific_payload": True,
        },
        "epoch": int(time.time()),
    }


def _payload_valid(target: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    repo = payload.get("repo_full_name") or payload.get("repository_full_name")
    if not isinstance(repo, str) or "/" not in repo:
        blockers.append("repo_full_name_invalid")
    if target == "commit_workflow_runs" and not payload.get("commit_sha"):
        blockers.append("commit_sha_missing")
    if target in {"workflow_run_jobs", "workflow_run_artifacts", "rerun_failed_workflow_run_jobs"} and not payload.get("run_id"):
        blockers.append("run_id_missing")
    if target in {"workflow_job_steps", "workflow_job_logs", "rerun_workflow_job"} and not payload.get("job_id"):
        blockers.append("job_id_missing")
    if target == "merge_pull_request" and not (payload.get("pr_number") or payload.get("pull_number")):
        blockers.append("pr_number_missing")


def build_qi_github_actions_external_call_dispatcher(*, runtime_context: Mapping[str, Any], external_call_dispatcher_license: Mapping[str, Any]) -> QiGitHubActionsExternalCallDispatcherResult:
    ctx = _m(runtime_context)
    lic = _m(external_call_dispatcher_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    call_path = root / "qi_github_actions_external_call_packet.json"
    receipt_path = root / "qi_github_actions_external_call_dispatcher_receipt.json"
    audit_path = root / "qi_github_actions_external_call_dispatcher_audit.jsonl"

    if ctx.get("qi_github_actions_external_call_dispatcher_enabled") is not True:
        blockers.append("qi_github_actions_external_call_dispatcher_enabled_not_true")
    if ctx.get("apply_github_actions_external_call_dispatcher") is not True:
        blockers.append("apply_github_actions_external_call_dispatcher_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_EXTERNAL_CALL_DISPATCHER_LICENSE_READY":
        blockers.append("github_actions_external_call_dispatcher_license_not_ready")
    for name in ["external_call_packet_read_allowed", "dispatch_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    call = _read_json(call_path)
    if not call:
        blockers.append("external_call_packet_missing_or_invalid")
    connector_action = str(call.get("connector_action", "unknown")) if call else "unknown"
    target = DISPATCH_TARGETS.get(connector_action, "unknown")
    if target == "unknown":
        blockers.append("connector_action_not_dispatchable")
    if target != "unknown" and lic.get(f"allow_{target}_dispatch") is not True:
        blockers.append(f"{target}_not_allowed_by_external_call_dispatcher_license")
    payload = _m(call.get("connector_payload")) if call else {}
    if target != "unknown":
        _payload_valid(target, payload, blockers)

    packet = _dispatch_packet(call, target) if target != "unknown" else {}
    dispatch_path = root / _dispatch_file(target) if target != "unknown" else root / "qi_github_actions_dispatch_blocked_packet.json"
    emitted = False
    if not blockers:
        _write_json(dispatch_path, packet)
        emitted = True

    status = "QI_GITHUB_ACTIONS_EXTERNAL_CALL_DISPATCHER_READY" if not blockers else "QI_GITHUB_ACTIONS_EXTERNAL_CALL_DISPATCHER_BLOCKED"
    packet_id = "qi-github-actions-external-call-dispatcher-" + _sha({"call": call, "target": target, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_external_call_dispatcher_v6_5",
        "status": status,
        "packet_id": packet_id,
        "dispatch_target": target,
        "connector_action": connector_action,
        "dispatch_packet_emitted": emitted,
        "dispatch_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsExternalCallDispatcherResult(
        "kuuos_runtime_daemon_qi_github_actions_external_call_dispatcher_v6_5",
        status,
        packet_id,
        str(root),
        target,
        str(dispatch_path),
        str(receipt_path),
        str(audit_path),
        emitted,
        blockers,
        warnings,
    )
