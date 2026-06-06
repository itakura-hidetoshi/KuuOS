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

DEFAULT_REQUIRED_WORKFLOWS = [
    "All Governance Validation",
    "Core Governance Validation",
    "Emptiness Superposition Non-Collapse Validation",
    "Emptiness Two Truths Runtime Audit Validation",
    "KuuOS Runtime Full Check",
    "Qi Process Tensor Review Checks",
]


@dataclass(frozen=True)
class QiGitHubActionsObservationResultIngestorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    observation_kind: str
    result_class: str
    status_packet_path: str
    observation_packet_path: str
    receipt_path: str
    audit_path: str
    status_packet_emitted: bool
    observation_packet_emitted: bool
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


def _payload(result: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = result.get("connector_result")
    return nested if isinstance(nested, Mapping) else result


def _list_from(payload: Mapping[str, Any], key: str) -> list[dict[str, Any]]:
    raw = payload.get(key, [])
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _required(result: Mapping[str, Any]) -> list[str]:
    raw = result.get("required_workflows")
    if isinstance(raw, list) and raw:
        return [str(x) for x in raw]
    return list(DEFAULT_REQUIRED_WORKFLOWS)


def _normalize_run(run: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "id": _i(run.get("id"), 0),
        "name": str(run.get("name", "")),
        "status": str(run.get("status", "")),
        "conclusion": run.get("conclusion"),
        "run_number": _i(run.get("run_number"), 0),
        "jobs_url": str(run.get("jobs_url", "")),
        "logs_url": str(run.get("logs_url", "")),
        "workflow_id": _i(run.get("workflow_id"), 0),
    }


def _normalize_job(job: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "id": _i(job.get("id", job.get("job_id")), 0),
        "name": str(job.get("name", "")),
        "status": str(job.get("status", "")),
        "conclusion": job.get("conclusion"),
        "run_id": _i(job.get("run_id"), 0),
        "steps": _list_from(job, "steps"),
    }


def _status_packet(request: Mapping[str, Any], result: Mapping[str, Any], runs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_status_packet_from_observation_v5_9",
        "github_actions_status_allowed": True,
        "required_workflows": _required(result),
        "workflow_runs": runs,
        "source_request_digest": _sha(request),
        "source_result_digest": _sha(result),
        "compiled_from": "qi_github_actions_observation_result_ingestor_v5_9",
        "epoch": int(time.time()),
    }


def _observation_packet(kind: str, request: Mapping[str, Any], result: Mapping[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {
        "version": "qi_github_actions_observation_packet_from_result_v5_9",
        "observation_kind": kind,
        "source_request_digest": _sha(request),
        "source_result_digest": _sha(result),
        "compiled_from": "qi_github_actions_observation_result_ingestor_v5_9",
        "epoch": int(time.time()),
    }
    if kind == "workflow_run_jobs":
        body["jobs"] = [_normalize_job(job) for job in _list_from(payload, "jobs")]
    elif kind == "workflow_job_steps":
        body["steps"] = _list_from(payload, "steps")
    elif kind == "workflow_run_artifacts":
        body["artifacts"] = _list_from(payload, "artifacts")
    elif kind == "workflow_job_logs":
        body["logs_digest"] = _sha({"logs": payload.get("logs", payload.get("text", ""))})
        body["logs_available"] = bool(payload.get("logs") or payload.get("text"))
    else:
        body["payload_digest"] = _sha(payload)
    return body


def build_qi_github_actions_observation_result_ingestor(*, runtime_context: Mapping[str, Any], observation_result_ingestor_license: Mapping[str, Any]) -> QiGitHubActionsObservationResultIngestorResult:
    ctx = _m(runtime_context)
    lic = _m(observation_result_ingestor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    request_path = root / "qi_github_actions_observation_connector_request.json"
    result_path = root / "qi_github_actions_observation_connector_result_packet.json"
    status_packet_path = root / "qi_github_actions_status_packet.json"
    observation_packet_path = root / "qi_github_actions_observation_result_packet.json"
    receipt_path = root / "qi_github_actions_observation_result_receipt.json"
    audit_path = root / "qi_github_actions_observation_result_audit.jsonl"

    if ctx.get("qi_github_actions_observation_result_ingestor_enabled") is not True:
        blockers.append("qi_github_actions_observation_result_ingestor_enabled_not_true")
    if ctx.get("apply_github_actions_observation_result_ingestor") is not True:
        blockers.append("apply_github_actions_observation_result_ingestor_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_OBSERVATION_RESULT_INGESTOR_LICENSE_READY":
        blockers.append("github_actions_observation_result_ingestor_license_not_ready")
    for name in ["observation_request_read_allowed", "observation_result_read_allowed", "status_packet_write_allowed", "observation_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    request = _read_json(request_path)
    result = _read_json(result_path)
    if not request:
        blockers.append("observation_connector_request_missing_or_invalid")
    if not result:
        blockers.append("observation_connector_result_missing_or_invalid")
    if result and result.get("observation_result_allowed") is not True:
        blockers.append("observation_result_packet_allowed_not_true")
    kind = str(request.get("observation_kind", "unknown")) if request else "unknown"
    if result and result.get("observation_kind") not in (None, kind):
        blockers.append("observation_result_kind_mismatch")
    if kind not in OBSERVATION_KINDS:
        blockers.append("observation_kind_not_allowlisted")
    if lic.get(f"allow_{kind}_observation") is not True:
        blockers.append(f"{kind}_not_allowed_by_observation_result_ingestor_license")

    payload = _payload(result)
    status_packet_emitted = False
    observation_packet_emitted = False
    result_class = "not_classified"
    if not blockers:
        if kind == "commit_workflow_runs":
            runs = [_normalize_run(run) for run in _list_from(payload, "workflow_runs")]
            if not runs:
                blockers.append("workflow_runs_empty_or_invalid")
                result_class = "github_actions_status_packet_blocked"
            else:
                _write_json(status_packet_path, _status_packet(request, result, runs))
                status_packet_emitted = True
                result_class = "github_actions_status_packet_emitted"
        else:
            obs_packet = _observation_packet(kind, request, result, payload)
            _write_json(observation_packet_path, obs_packet)
            observation_packet_emitted = True
            result_class = "github_actions_observation_packet_emitted"

    status = "QI_GITHUB_ACTIONS_OBSERVATION_RESULT_INGESTOR_READY" if not blockers else "QI_GITHUB_ACTIONS_OBSERVATION_RESULT_INGESTOR_BLOCKED"
    packet_id = "qi-github-actions-observation-result-" + _sha({"request": request, "result": result, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_observation_result_ingestor_v5_9",
        "status": status,
        "packet_id": packet_id,
        "observation_kind": kind,
        "result_class": result_class,
        "status_packet_emitted": status_packet_emitted,
        "observation_packet_emitted": observation_packet_emitted,
        "request_digest": _sha(request),
        "result_digest": _sha(result),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsObservationResultIngestorResult(
        "kuuos_runtime_daemon_qi_github_actions_observation_result_ingestor_v5_9",
        status,
        packet_id,
        str(root),
        kind,
        result_class,
        str(status_packet_path),
        str(observation_packet_path),
        str(receipt_path),
        str(audit_path),
        status_packet_emitted,
        observation_packet_emitted,
        blockers,
        warnings,
    )
