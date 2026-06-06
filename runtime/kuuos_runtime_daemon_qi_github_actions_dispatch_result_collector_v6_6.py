#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


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

OBSERVATION_TARGETS = {
    "commit_workflow_runs",
    "workflow_run_jobs",
    "workflow_job_steps",
    "workflow_job_logs",
    "workflow_run_artifacts",
}

OPERATION_TARGETS = {
    "rerun_failed_workflow_run_jobs",
    "rerun_workflow_job",
    "merge_pull_request",
}


@dataclass(frozen=True)
class QiGitHubActionsDispatchResultCollectorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    dispatch_target: str
    raw_result_packet_path: str
    receipt_path: str
    audit_path: str
    raw_result_packet_written: bool
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


def _raw_result(dispatch: Mapping[str, Any], result: Mapping[str, Any]) -> dict[str, Any]:
    target = str(dispatch.get("dispatch_target", "unknown"))
    connector_result = dict(_m(result.get("connector_result"))) if isinstance(result.get("connector_result"), Mapping) else dict(result)
    return {
        "version": "qi_github_actions_external_call_raw_result_packet_from_dispatch_v6_6",
        "dispatch_target": target,
        "connector_action": str(dispatch.get("connector_action", "unknown")),
        "connector_result": connector_result,
        "result_expected_file": str(dispatch.get("result_expected_file", "unknown")),
        "dispatch_digest": _sha(dict(dispatch)),
        "dispatch_result_digest": _sha(dict(result)),
        "epoch": int(time.time()),
    }


def _target_from_available(root: pathlib.Path) -> str:
    for target in DISPATCH_RESULT_FILES:
        if _read_json(root / _dispatch_file(target)) and _read_json(root / DISPATCH_RESULT_FILES[target]):
            return target
    for target in DISPATCH_RESULT_FILES:
        if _read_json(root / _dispatch_file(target)):
            return target
    return "unknown"


def build_qi_github_actions_dispatch_result_collector(*, runtime_context: Mapping[str, Any], dispatch_result_collector_license: Mapping[str, Any]) -> QiGitHubActionsDispatchResultCollectorResult:
    ctx = _m(runtime_context)
    lic = _m(dispatch_result_collector_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_dispatch_result_collector_receipt.json"
    audit_path = root / "qi_github_actions_dispatch_result_collector_audit.jsonl"
    raw_result_packet_path = root / "qi_github_actions_external_call_raw_result_packet.json"

    if ctx.get("qi_github_actions_dispatch_result_collector_enabled") is not True:
        blockers.append("qi_github_actions_dispatch_result_collector_enabled_not_true")
    if ctx.get("apply_github_actions_dispatch_result_collector") is not True:
        blockers.append("apply_github_actions_dispatch_result_collector_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_DISPATCH_RESULT_COLLECTOR_LICENSE_READY":
        blockers.append("github_actions_dispatch_result_collector_license_not_ready")
    for name in ["dispatch_packet_read_allowed", "dispatch_result_read_allowed", "raw_result_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    target = str(ctx.get("dispatch_target") or _target_from_available(root))
    if target not in DISPATCH_RESULT_FILES:
        blockers.append("dispatch_target_not_allowlisted")
    if target in DISPATCH_RESULT_FILES and lic.get(f"allow_{target}_collect") is not True:
        blockers.append(f"{target}_not_allowed_by_dispatch_result_collector_license")

    dispatch = _read_json(root / _dispatch_file(target)) if target in DISPATCH_RESULT_FILES else {}
    result = _read_json(root / DISPATCH_RESULT_FILES[target]) if target in DISPATCH_RESULT_FILES else {}
    if not dispatch:
        blockers.append("dispatch_packet_missing_or_invalid")
    if not result:
        blockers.append("dispatch_result_missing_or_invalid")
    if dispatch and str(dispatch.get("dispatch_target", "unknown")) != target:
        blockers.append("dispatch_target_mismatch")
    if result and result.get("dispatch_result_allowed") is not True:
        blockers.append("dispatch_result_allowed_not_true")

    raw: dict[str, Any] = {}
    written = False
    if not blockers:
        raw = _raw_result(dispatch, result)
        _write_json(raw_result_packet_path, raw)
        written = True

    status = "QI_GITHUB_ACTIONS_DISPATCH_RESULT_COLLECTOR_READY" if not blockers else "QI_GITHUB_ACTIONS_DISPATCH_RESULT_COLLECTOR_BLOCKED"
    packet_id = "qi-github-actions-dispatch-result-" + _sha({"target": target, "dispatch": dispatch, "result": result, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_dispatch_result_collector_v6_6",
        "status": status,
        "packet_id": packet_id,
        "dispatch_target": target,
        "raw_result_packet_written": written,
        "raw_result_packet_digest": _sha(raw),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsDispatchResultCollectorResult(
        "kuuos_runtime_daemon_qi_github_actions_dispatch_result_collector_v6_6",
        status,
        packet_id,
        str(root),
        target,
        str(raw_result_packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
