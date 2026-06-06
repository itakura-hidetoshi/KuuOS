#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ALLOWED_REQUEST_ACTIONS = {
    "rerun_failed_workflow_run_jobs",
    "rerun_workflow_job",
    "merge_pull_request",
    "workflow_dispatch",
}

SUCCESS_CLASSES = {
    "rerun_failed_workflow_run_jobs": "github_actions_rerun_accepted",
    "rerun_workflow_job": "github_actions_job_rerun_accepted",
    "merge_pull_request": "github_pr_merge_accepted",
    "workflow_dispatch": "github_workflow_dispatch_accepted",
}


@dataclass(frozen=True)
class QiGitHubActionsResultIngestorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    action: str
    result_class: str
    receipt_path: str
    audit_path: str
    reobserve_request_path: str
    reobserve_request_emitted: bool
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


def _truthy_success(result: Mapping[str, Any]) -> bool:
    if result.get("success") is True:
        return True
    if result.get("merged") is True:
        return True
    if str(result.get("status", "")).lower() in {"success", "accepted", "ok", "ready"}:
        return True
    http_status = result.get("http_status")
    try:
        code = int(http_status)
    except (TypeError, ValueError):
        code = 0
    return 200 <= code < 300


def _retryable(result: Mapping[str, Any]) -> bool:
    if result.get("retryable") is True:
        return True
    http_status = result.get("http_status")
    try:
        code = int(http_status)
    except (TypeError, ValueError):
        code = 0
    return code in {408, 409, 429, 500, 502, 503, 504}


def _classify(action: str, result: Mapping[str, Any]) -> str:
    if _truthy_success(result):
        return SUCCESS_CLASSES.get(action, "github_operation_accepted")
    if _retryable(result):
        return "github_operation_retryable"
    if result.get("reobserve_required") is True:
        return "github_operation_reobserve_required"
    return "github_operation_hold"


def build_qi_github_actions_result_ingestor(*, runtime_context: Mapping[str, Any], result_ingestor_license: Mapping[str, Any]) -> QiGitHubActionsResultIngestorResult:
    ctx = _m(runtime_context)
    lic = _m(result_ingestor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    request_path = root / "qi_github_actions_connector_execution_request.json"
    result_path = root / "qi_github_actions_connector_result_packet.json"
    receipt_path = root / "qi_github_actions_result_receipt.json"
    audit_path = root / "qi_github_actions_result_audit.jsonl"
    reobserve_path = root / "qi_github_actions_status_reobserve_request.json"

    if ctx.get("qi_github_actions_result_ingestor_enabled") is not True:
        blockers.append("qi_github_actions_result_ingestor_enabled_not_true")
    if ctx.get("apply_github_actions_result_ingestor") is not True:
        blockers.append("apply_github_actions_result_ingestor_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_RESULT_INGESTOR_LICENSE_READY":
        blockers.append("github_actions_result_ingestor_license_not_ready")
    for name in ["connector_request_read_allowed", "connector_result_read_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    request = _read_json(request_path)
    result = _read_json(result_path)
    if not request:
        blockers.append("connector_execution_request_missing_or_invalid")
    if not result:
        blockers.append("connector_result_packet_missing_or_invalid")
    action = str(request.get("action", "unknown")) if request else "unknown"
    if action not in ALLOWED_REQUEST_ACTIONS:
        blockers.append("request_action_not_allowlisted")
    if result and result.get("result_packet_allowed") is not True:
        blockers.append("connector_result_packet_allowed_not_true")
    if request and result and result.get("action") not in (None, action):
        blockers.append("connector_result_action_mismatch")

    result_class = "not_classified"
    reobserve = False
    if not blockers:
        result_class = _classify(action, result)
        reobserve = result_class in {"github_operation_retryable", "github_operation_reobserve_required"}
        if reobserve:
            reobserve_payload = {
                "version": "qi_github_actions_status_reobserve_request_v5_7",
                "reason": result_class,
                "source_action": action,
                "source_request_digest": _sha(request),
                "source_result_digest": _sha(result),
                "epoch": int(time.time()),
            }
            _write_json(reobserve_path, reobserve_payload)

    status = "QI_GITHUB_ACTIONS_RESULT_INGESTOR_READY" if not blockers else "QI_GITHUB_ACTIONS_RESULT_INGESTOR_BLOCKED"
    packet_id = "qi-github-actions-result-ingestor-" + _sha({"request": request, "result": result, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_result_ingestor_v5_7",
        "status": status,
        "packet_id": packet_id,
        "action": action,
        "result_class": result_class,
        "request_digest": _sha(request),
        "result_digest": _sha(result),
        "reobserve_request_emitted": reobserve,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsResultIngestorResult(
        "kuuos_runtime_daemon_qi_github_actions_result_ingestor_v5_7",
        status,
        packet_id,
        str(root),
        action,
        result_class,
        str(receipt_path),
        str(audit_path),
        str(reobserve_path),
        reobserve,
        blockers,
        warnings,
    )
