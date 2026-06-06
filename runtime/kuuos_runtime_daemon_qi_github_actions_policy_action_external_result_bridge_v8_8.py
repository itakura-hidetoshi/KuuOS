#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


RESULT_FILE_BY_ACTION = {
    "merge_pull_request": "qi_github_actions_policy_action_merge_result_packet.json",
    "rerun_failed_workflow_run_jobs": "qi_github_actions_policy_action_rerun_result_packet.json",
    "reobserve_commit_workflow_runs": "qi_github_actions_policy_action_reobserve_result_packet.json",
}

CONNECTOR_ACTION_BY_KIND = {
    "merge_pull_request": "GitHub.merge_pull_request",
    "rerun_failed_workflow_run_jobs": "GitHub.rerun_failed_workflow_run_jobs",
    "reobserve_commit_workflow_runs": "GitHub.fetch_commit_workflow_runs",
}


@dataclass(frozen=True)
class QiGitHubActionsPolicyActionExternalResultBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    action_kind: str
    connector_action: str
    action_result_path: str
    receipt_path: str
    audit_path: str
    action_result_written: bool
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


def _validate_payload(kind: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    if kind == "merge_pull_request":
        if payload.get("merged") is not True:
            blockers.append("merge_result_not_merged_true")
        if not str(payload.get("sha", "")).strip():
            blockers.append("merge_result_sha_missing")
    elif kind == "rerun_failed_workflow_run_jobs":
        if payload.get("success") is not True and str(payload.get("status", "")).lower() not in {"queued", "requested", "accepted", "success"}:
            blockers.append("rerun_result_not_success_like")
    elif kind == "reobserve_commit_workflow_runs":
        runs = payload.get("workflow_runs")
        if not isinstance(runs, list) or not runs:
            blockers.append("workflow_runs_empty_or_invalid")


def _action_result_packet(call: Mapping[str, Any], raw: Mapping[str, Any], kind: str) -> dict[str, Any]:
    payload = dict(_payload(raw))
    return {
        "version": "qi_github_actions_policy_action_external_result_packet_v8_8",
        "action_result_allowed": True,
        "action_kind": kind,
        "connector_action": CONNECTOR_ACTION_BY_KIND[kind],
        "connector_result": payload,
        "source_external_call_digest": _sha(dict(call)),
        "source_raw_result_digest": _sha(dict(raw)),
        "boundary": {
            "result_packet_only": True,
            "does_not_apply_additional_action": True,
            "feeds_policy_action_receipt_or_review": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_policy_action_external_result_bridge(*, runtime_context: Mapping[str, Any], policy_action_external_result_bridge_license: Mapping[str, Any]) -> QiGitHubActionsPolicyActionExternalResultBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(policy_action_external_result_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    call_path = root / "qi_github_actions_policy_action_external_call_packet.json"
    raw_result_path = root / "qi_github_actions_policy_action_external_call_raw_result_packet.json"
    receipt_path = root / "qi_github_actions_policy_action_external_result_bridge_receipt.json"
    audit_path = root / "qi_github_actions_policy_action_external_result_bridge_audit.jsonl"

    if ctx.get("qi_github_actions_policy_action_external_result_bridge_enabled") is not True:
        blockers.append("qi_github_actions_policy_action_external_result_bridge_enabled_not_true")
    if ctx.get("apply_github_actions_policy_action_external_result_bridge") is not True:
        blockers.append("apply_github_actions_policy_action_external_result_bridge_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_RESULT_BRIDGE_LICENSE_READY":
        blockers.append("github_actions_policy_action_external_result_bridge_license_not_ready")
    for name in ["external_call_packet_read_allowed", "raw_result_packet_read_allowed", "action_result_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    call = _read_json(call_path)
    raw = _read_json(raw_result_path)
    if not call:
        blockers.append("external_call_packet_missing_or_invalid")
    if not raw:
        blockers.append("raw_result_packet_missing_or_invalid")
    if call and call.get("external_call_allowed") is not True:
        blockers.append("external_call_allowed_not_true")

    kind = str(call.get("action_kind", "unknown")) if call else "unknown"
    if kind not in RESULT_FILE_BY_ACTION:
        blockers.append("action_kind_not_allowlisted")
    if kind in RESULT_FILE_BY_ACTION and lic.get(f"allow_{kind}_result_bridge") is not True:
        blockers.append(f"{kind}_not_allowed_by_policy_action_external_result_bridge_license")
    action = str(call.get("connector_action", "unknown")) if call else "unknown"
    expected_action = CONNECTOR_ACTION_BY_KIND.get(kind, "unknown")
    if kind in CONNECTOR_ACTION_BY_KIND and action != expected_action:
        blockers.append("connector_action_mismatch")
    expected_file = str(call.get("action_result_expected_file", "")) if call else ""
    if kind in RESULT_FILE_BY_ACTION and expected_file and expected_file != RESULT_FILE_BY_ACTION[kind]:
        blockers.append("action_result_expected_file_mismatch")
    result_action = str(raw.get("connector_action", action)) if raw else action
    if raw and result_action != action:
        blockers.append("raw_result_connector_action_mismatch")
    payload = _payload(raw) if raw else {}
    if kind in RESULT_FILE_BY_ACTION and raw:
        _validate_payload(kind, payload, blockers)

    action_result_path = root / RESULT_FILE_BY_ACTION.get(kind, "qi_github_actions_policy_action_blocked_result_packet.json")
    packet: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _action_result_packet(call, raw, kind)
        _write_json(action_result_path, packet)
        written = True

    status = "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_RESULT_BRIDGE_READY" if not blockers else "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_RESULT_BRIDGE_BLOCKED"
    packet_id = "qi-github-actions-policy-action-external-result-" + _sha({"call": call, "raw": raw, "kind": kind, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_policy_action_external_result_bridge_v8_8",
        "status": status,
        "packet_id": packet_id,
        "action_kind": kind,
        "connector_action": expected_action,
        "action_result_written": written,
        "action_result_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPolicyActionExternalResultBridgeResult(
        "kuuos_runtime_daemon_qi_github_actions_policy_action_external_result_bridge_v8_8",
        status,
        packet_id,
        str(root),
        kind,
        expected_action,
        str(action_result_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
