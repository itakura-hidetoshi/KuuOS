#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


EXPECTED_RESULT_FILES = {
    "qi_github_actions_connector_result_packet.json",
    "qi_github_actions_observation_connector_result_packet.json",
}


@dataclass(frozen=True)
class QiGitHubActionsExternalCallResultAdapterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    wait_stage: str
    result_file: str
    adapted_result_path: str
    receipt_path: str
    audit_path: str
    adapted_result_written: bool
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


def _external_result(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = raw.get("connector_result")
    return nested if isinstance(nested, Mapping) else raw


def _adapt_operation_result(call: Mapping[str, Any], raw: Mapping[str, Any]) -> dict[str, Any]:
    result = _external_result(raw)
    action = str(call.get("connector_action", "unknown")).split(".")[-1]
    if action == "connector_operation":
        action = str(raw.get("action", "connector_operation"))
    return {
        "version": "qi_github_actions_connector_result_packet_from_external_call_v6_4",
        "result_packet_allowed": True,
        "action": str(raw.get("action", action)),
        "success": result.get("success", raw.get("success")),
        "merged": result.get("merged", raw.get("merged")),
        "http_status": result.get("http_status", raw.get("http_status")),
        "retryable": result.get("retryable", raw.get("retryable")),
        "reobserve_required": result.get("reobserve_required", raw.get("reobserve_required")),
        "source_call_digest": _sha(dict(call)),
        "source_raw_result_digest": _sha(dict(raw)),
        "epoch": int(time.time()),
    }


def _adapt_observation_result(call: Mapping[str, Any], raw: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(_external_result(raw))
    kind = str(call.get("wait_stage", ""))
    observation_kind = str(raw.get("observation_kind", call.get("observation_kind", "unknown")))
    if observation_kind == "unknown":
        connector_action = str(call.get("connector_action", ""))
        if "commit_workflow_runs" in connector_action:
            observation_kind = "commit_workflow_runs"
        elif "workflow_run_jobs" in connector_action:
            observation_kind = "workflow_run_jobs"
        elif "workflow_job_steps" in connector_action:
            observation_kind = "workflow_job_steps"
        elif "workflow_job_logs" in connector_action:
            observation_kind = "workflow_job_logs"
        elif "workflow_run_artifacts" in connector_action:
            observation_kind = "workflow_run_artifacts"
    adapted = {
        "version": "qi_github_actions_observation_connector_result_packet_from_external_call_v6_4",
        "observation_result_allowed": True,
        "observation_kind": observation_kind,
        "source_wait_stage": kind,
        "source_call_digest": _sha(dict(call)),
        "source_raw_result_digest": _sha(dict(raw)),
        "epoch": int(time.time()),
    }
    adapted.update(result)
    return adapted


def build_qi_github_actions_external_call_result_adapter(*, runtime_context: Mapping[str, Any], result_adapter_license: Mapping[str, Any]) -> QiGitHubActionsExternalCallResultAdapterResult:
    ctx = _m(runtime_context)
    lic = _m(result_adapter_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    call_path = root / "qi_github_actions_external_call_packet.json"
    raw_result_path = root / "qi_github_actions_external_call_raw_result_packet.json"
    receipt_path = root / "qi_github_actions_external_call_result_adapter_receipt.json"
    audit_path = root / "qi_github_actions_external_call_result_adapter_audit.jsonl"

    if ctx.get("qi_github_actions_external_call_result_adapter_enabled") is not True:
        blockers.append("qi_github_actions_external_call_result_adapter_enabled_not_true")
    if ctx.get("apply_github_actions_external_call_result_adapter") is not True:
        blockers.append("apply_github_actions_external_call_result_adapter_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_EXTERNAL_CALL_RESULT_ADAPTER_LICENSE_READY":
        blockers.append("github_actions_external_call_result_adapter_license_not_ready")
    for name in ["external_call_packet_read_allowed", "raw_result_packet_read_allowed", "adapted_result_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    call = _read_json(call_path)
    raw = _read_json(raw_result_path)
    if not call:
        blockers.append("external_call_packet_missing_or_invalid")
    if not raw:
        blockers.append("external_call_raw_result_packet_missing_or_invalid")
    result_file = str(call.get("result_expected_file", "unknown")) if call else "unknown"
    if result_file not in EXPECTED_RESULT_FILES:
        blockers.append("result_expected_file_not_allowlisted")
    wait_stage = str(call.get("wait_stage", "unknown")) if call else "unknown"
    if lic.get(f"allow_{wait_stage}_stage") is not True:
        blockers.append(f"{wait_stage}_not_allowed_by_result_adapter_license")

    adapted_path = root / result_file if result_file in EXPECTED_RESULT_FILES else root / "qi_github_actions_adapted_result_blocked.json"
    adapted: dict[str, Any] = {}
    written = False
    if not blockers:
        if result_file == "qi_github_actions_connector_result_packet.json":
            adapted = _adapt_operation_result(call, raw)
        else:
            adapted = _adapt_observation_result(call, raw)
        _write_json(adapted_path, adapted)
        written = True

    status = "QI_GITHUB_ACTIONS_EXTERNAL_CALL_RESULT_ADAPTER_READY" if not blockers else "QI_GITHUB_ACTIONS_EXTERNAL_CALL_RESULT_ADAPTER_BLOCKED"
    packet_id = "qi-github-actions-external-call-result-" + _sha({"call": call, "raw": raw, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_external_call_result_adapter_v6_4",
        "status": status,
        "packet_id": packet_id,
        "wait_stage": wait_stage,
        "result_file": result_file,
        "adapted_result_written": written,
        "adapted_result_digest": _sha(adapted),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsExternalCallResultAdapterResult(
        "kuuos_runtime_daemon_qi_github_actions_external_call_result_adapter_v6_4",
        status,
        packet_id,
        str(root),
        wait_stage,
        result_file,
        str(adapted_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
