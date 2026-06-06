#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


OBSERVATION_KINDS = {
    "commit_workflow_runs",
    "workflow_run_jobs",
    "workflow_job_steps",
    "workflow_job_logs",
    "workflow_run_artifacts",
}

CONNECTOR_ACTIONS = {
    "commit_workflow_runs": "GitHub.fetch_commit_workflow_runs",
    "workflow_run_jobs": "GitHub.fetch_workflow_run_jobs",
    "workflow_job_steps": "GitHub.fetch_workflow_job_steps",
    "workflow_job_logs": "GitHub.fetch_workflow_job_logs",
    "workflow_run_artifacts": "GitHub.fetch_workflow_run_artifacts",
}


@dataclass(frozen=True)
class QiGitHubActionsStatusReobserverResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    observation_kind: str
    connector_action: str
    request_path: str
    receipt_path: str
    audit_path: str
    request_emitted: bool
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


def _repo(packet: Mapping[str, Any], blockers: list[str]) -> str:
    repo = str(packet.get("repo_full_name", "")).strip()
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    return repo


def _payload_for(kind: str, packet: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    repo = _repo(packet, blockers)
    if kind == "commit_workflow_runs":
        sha = str(packet.get("commit_sha", packet.get("source_commit_sha", ""))).strip()
        if not sha:
            blockers.append("commit_sha_missing")
        return {"repo_full_name": repo, "commit_sha": sha}
    if kind in {"workflow_run_jobs", "workflow_run_artifacts"}:
        run_id = _i(packet.get("run_id"), 0)
        if run_id <= 0:
            blockers.append("run_id_invalid")
        payload = {"repo_full_name": repo, "run_id": run_id}
        if kind == "workflow_run_artifacts" and packet.get("artifact_name"):
            payload["name"] = str(packet.get("artifact_name"))
        return payload
    if kind in {"workflow_job_steps", "workflow_job_logs"}:
        job_id = _i(packet.get("job_id"), 0)
        if job_id <= 0:
            blockers.append("job_id_invalid")
        return {"repo_full_name": repo, "job_id": job_id}
    blockers.append("observation_kind_not_allowlisted")
    return {"repo_full_name": repo}


def build_qi_github_actions_status_reobserver(*, runtime_context: Mapping[str, Any], status_reobserver_license: Mapping[str, Any]) -> QiGitHubActionsStatusReobserverResult:
    ctx = _m(runtime_context)
    lic = _m(status_reobserver_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    reobserve_path = root / "qi_github_actions_status_reobserve_request.json"
    request_path = root / "qi_github_actions_observation_connector_request.json"
    receipt_path = root / "qi_github_actions_status_reobserver_receipt.json"
    audit_path = root / "qi_github_actions_status_reobserver_audit.jsonl"

    if ctx.get("qi_github_actions_status_reobserver_enabled") is not True:
        blockers.append("qi_github_actions_status_reobserver_enabled_not_true")
    if ctx.get("apply_github_actions_status_reobserver") is not True:
        blockers.append("apply_github_actions_status_reobserver_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_STATUS_REOBSERVER_LICENSE_READY":
        blockers.append("github_actions_status_reobserver_license_not_ready")
    for name in ["reobserve_request_read_allowed", "observation_request_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(reobserve_path)
    if not packet:
        blockers.append("status_reobserve_request_missing_or_invalid")
    if packet and packet.get("reobserve_allowed") is not True:
        blockers.append("status_reobserve_request_allowed_not_true")
    kind = str(packet.get("observation_kind", ctx.get("default_observation_kind", "commit_workflow_runs"))) if packet else "unknown"
    if kind not in OBSERVATION_KINDS:
        blockers.append("observation_kind_not_allowlisted")
    if lic.get(f"allow_{kind}_observation") is not True:
        blockers.append(f"{kind}_not_allowed_by_status_reobserver_license")

    payload = _payload_for(kind, packet, blockers) if packet else {}
    connector_action = CONNECTOR_ACTIONS.get(kind, "unknown")
    request = {
        "version": "qi_github_actions_observation_connector_request_v5_8",
        "observation_kind": kind,
        "connector_action": connector_action,
        "connector_payload": payload,
        "source_reobserve_digest": _sha(packet),
        "epoch": int(time.time()),
    }
    request_emitted = False
    if not blockers:
        _write_json(request_path, request)
        request_emitted = True
    status = "QI_GITHUB_ACTIONS_STATUS_REOBSERVER_READY" if not blockers else "QI_GITHUB_ACTIONS_STATUS_REOBSERVER_BLOCKED"
    packet_id = "qi-github-actions-status-reobserver-" + _sha({"packet": packet, "request": request, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_status_reobserver_v5_8",
        "status": status,
        "packet_id": packet_id,
        "observation_kind": kind,
        "connector_action": connector_action,
        "request_emitted": request_emitted,
        "request_digest": _sha(request),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsStatusReobserverResult(
        "kuuos_runtime_daemon_qi_github_actions_status_reobserver_v5_8",
        status,
        packet_id,
        str(root),
        kind,
        connector_action,
        str(request_path),
        str(receipt_path),
        str(audit_path),
        request_emitted,
        blockers,
        warnings,
    )
