#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


TARGET_TO_TOOL = {
    "commit_workflow_runs": "GitHub.fetch_commit_workflow_runs",
    "workflow_run_jobs": "GitHub.fetch_workflow_run_jobs",
    "workflow_job_steps": "GitHub.fetch_workflow_job_steps",
    "workflow_job_logs": "GitHub.fetch_workflow_job_logs",
    "workflow_run_artifacts": "GitHub.fetch_workflow_run_artifacts",
    "rerun_failed_workflow_run_jobs": "GitHub.rerun_failed_workflow_run_jobs",
    "rerun_workflow_job": "GitHub.rerun_workflow_job",
    "merge_pull_request": "GitHub.merge_pull_request",
}

DISPATCH_PACKET_FILES = {
    "commit_workflow_runs": "qi_github_actions_dispatch_commit_workflow_runs_packet.json",
    "workflow_run_jobs": "qi_github_actions_dispatch_workflow_run_jobs_packet.json",
    "workflow_job_steps": "qi_github_actions_dispatch_workflow_job_steps_packet.json",
    "workflow_job_logs": "qi_github_actions_dispatch_workflow_job_logs_packet.json",
    "workflow_run_artifacts": "qi_github_actions_dispatch_workflow_run_artifacts_packet.json",
    "rerun_failed_workflow_run_jobs": "qi_github_actions_dispatch_rerun_failed_workflow_run_jobs_packet.json",
    "rerun_workflow_job": "qi_github_actions_dispatch_rerun_workflow_job_packet.json",
    "merge_pull_request": "qi_github_actions_dispatch_merge_pull_request_packet.json",
}

DISPATCH_RESULT_FILES = {
    "commit_workflow_runs": "qi_github_actions_dispatch_commit_workflow_runs_result.json",
    "workflow_run_jobs": "qi_github_actions_dispatch_workflow_run_jobs_result.json",
    "workflow_job_steps": "qi_github_actions_dispatch_workflow_job_steps_result.json",
    "workflow_job_logs": "qi_github_actions_dispatch_workflow_job_logs_result.json",
    "workflow_run_artifacts": "qi_github_actions_dispatch_workflow_run_artifacts_result.json",
    "rerun_failed_workflow_run_jobs": "qi_github_actions_dispatch_rerun_failed_workflow_run_jobs_result.json",
    "rerun_workflow_job": "qi_github_actions_dispatch_rerun_workflow_job_result.json",
    "merge_pull_request": "qi_github_actions_dispatch_merge_pull_request_result.json",
}


@dataclass(frozen=True)
class QiGitHubActionsHandoffPacketizerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    handoff_target: str
    connector_tool: str
    handoff_packet_path: str
    receipt_path: str
    audit_path: str
    handoff_packet_emitted: bool
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


def _find_dispatch(root: pathlib.Path) -> tuple[str, dict[str, Any], pathlib.Path]:
    for target, file_name in DISPATCH_PACKET_FILES.items():
        path = root / file_name
        packet = _read_json(path)
        if packet:
            return target, packet, path
    return "unknown", {}, root / "qi_github_actions_dispatch_missing_packet.json"


def _repo_arg(payload: Mapping[str, Any]) -> str:
    return str(payload.get("repo_full_name") or payload.get("repository_full_name") or "")


def _tool_args(target: str, payload: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    repo = _repo_arg(payload)
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    if target == "commit_workflow_runs":
        sha = str(payload.get("commit_sha", ""))
        if not sha:
            blockers.append("commit_sha_missing")
        return {"repo_full_name": repo, "commit_sha": sha}
    if target in {"workflow_run_jobs", "workflow_run_artifacts", "rerun_failed_workflow_run_jobs"}:
        run_id = payload.get("run_id")
        if not isinstance(run_id, int) or run_id <= 0:
            blockers.append("run_id_invalid")
        out = {"repo_full_name": repo, "run_id": run_id}
        if target == "workflow_run_artifacts" and payload.get("name"):
            out["name"] = payload.get("name")
        return out
    if target in {"workflow_job_steps", "workflow_job_logs", "rerun_workflow_job"}:
        job_id = payload.get("job_id")
        if not isinstance(job_id, int) or job_id <= 0:
            blockers.append("job_id_invalid")
        return {"repo_full_name": repo, "job_id": job_id}
    if target == "merge_pull_request":
        pr_number = payload.get("pr_number") or payload.get("pull_number")
        if not isinstance(pr_number, int) or pr_number <= 0:
            blockers.append("pr_number_invalid")
        out: dict[str, Any] = {"repository_full_name": repo, "pr_number": pr_number}
        for key in ["merge_method", "commit_title", "commit_message", "expected_head_sha"]:
            if payload.get(key) is not None:
                out[key] = payload.get(key)
        return out
    blockers.append("handoff_target_not_allowlisted")
    return {}


def _handoff_packet(target: str, packet: Mapping[str, Any], packet_path: pathlib.Path, tool_args: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_handoff_packet_v6_9",
        "handoff_target": target,
        "connector_tool": TARGET_TO_TOOL[target],
        "connector_tool_args": dict(tool_args),
        "source_dispatch_packet_path": str(packet_path),
        "source_dispatch_packet_digest": _sha(dict(packet)),
        "dispatch_result_file": DISPATCH_RESULT_FILES[target],
        "post_call_next_step": "write_dispatch_result_then_run_v6_6_v6_4_v5_ingestor",
        "boundary": {
            "handoff_packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "operator_or_chatgpt_connector_executes_tool": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_handoff_packetizer(*, runtime_context: Mapping[str, Any], handoff_packetizer_license: Mapping[str, Any]) -> QiGitHubActionsHandoffPacketizerResult:
    ctx = _m(runtime_context)
    lic = _m(handoff_packetizer_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    handoff_path = root / "qi_github_actions_handoff_packet.json"
    receipt_path = root / "qi_github_actions_handoff_packetizer_receipt.json"
    audit_path = root / "qi_github_actions_handoff_packetizer_audit.jsonl"

    if ctx.get("qi_github_actions_handoff_packetizer_enabled") is not True:
        blockers.append("qi_github_actions_handoff_packetizer_enabled_not_true")
    if ctx.get("apply_github_actions_handoff_packetizer") is not True:
        blockers.append("apply_github_actions_handoff_packetizer_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_HANDOFF_PACKETIZER_LICENSE_READY":
        blockers.append("github_actions_handoff_packetizer_license_not_ready")
    for name in ["dispatch_packet_read_allowed", "handoff_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    target, dispatch_packet, dispatch_path = _find_dispatch(root)
    if target == "unknown" or not dispatch_packet:
        blockers.append("dispatch_packet_missing_or_invalid")
    if target != "unknown" and lic.get(f"allow_{target}_handoff") is not True:
        blockers.append(f"{target}_not_allowed_by_handoff_packetizer_license")
    payload = _m(dispatch_packet.get("connector_payload")) if dispatch_packet else {}
    if not payload:
        blockers.append("connector_payload_missing_or_invalid")
    tool_args = _tool_args(target, payload, blockers) if target != "unknown" else {}
    connector_tool = TARGET_TO_TOOL.get(target, "unknown")

    handoff: dict[str, Any] = {}
    emitted = False
    if not blockers:
        handoff = _handoff_packet(target, dispatch_packet, dispatch_path, tool_args)
        _write_json(handoff_path, handoff)
        emitted = True
    status = "QI_GITHUB_ACTIONS_HANDOFF_PACKETIZER_READY" if not blockers else "QI_GITHUB_ACTIONS_HANDOFF_PACKETIZER_BLOCKED"
    packet_id = "qi-github-actions-handoff-" + _sha({"target": target, "dispatch": dispatch_packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_handoff_packetizer_v6_9",
        "status": status,
        "packet_id": packet_id,
        "handoff_target": target,
        "connector_tool": connector_tool,
        "handoff_packet_emitted": emitted,
        "handoff_packet_digest": _sha(handoff),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsHandoffPacketizerResult(
        "kuuos_runtime_daemon_qi_github_actions_handoff_packetizer_v6_9",
        status,
        packet_id,
        str(root),
        target,
        connector_tool,
        str(handoff_path),
        str(receipt_path),
        str(audit_path),
        emitted,
        blockers,
        warnings,
    )
