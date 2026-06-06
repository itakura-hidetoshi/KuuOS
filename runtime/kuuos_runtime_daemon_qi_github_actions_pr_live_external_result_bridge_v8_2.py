#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


RESULT_FILE_BY_TARGET = {
    "pr_info": "qi_github_actions_pr_live_dispatch_pr_info_result.json",
    "commit_workflow_runs": "qi_github_actions_pr_live_dispatch_commit_workflow_runs_result.json",
}

ALLOWED_ACTION_BY_TARGET = {
    "pr_info": "GitHub.get_pr_info",
    "commit_workflow_runs": "GitHub.fetch_commit_workflow_runs",
}


@dataclass(frozen=True)
class QiGitHubActionsPrLiveExternalResultBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    dispatch_target: str
    connector_action: str
    dispatch_result_path: str
    receipt_path: str
    audit_path: str
    dispatch_result_written: bool
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


def _validate_payload(target: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    if target == "pr_info":
        head = payload.get("head")
        nested_sha = head.get("sha") if isinstance(head, Mapping) else ""
        if not str(payload.get("head_sha") or nested_sha or "").strip():
            blockers.append("head_sha_missing")
        if not (payload.get("number") or payload.get("pr_number")):
            blockers.append("pr_number_missing")
    elif target == "commit_workflow_runs":
        runs = payload.get("workflow_runs")
        if not isinstance(runs, list) or not runs:
            blockers.append("workflow_runs_empty_or_invalid")


def _dispatch_result(call: Mapping[str, Any], raw: Mapping[str, Any], target: str) -> dict[str, Any]:
    payload = dict(_payload(raw))
    return {
        "version": "qi_github_actions_pr_live_dispatch_result_from_external_call_v8_2",
        "dispatch_result_allowed": True,
        "dispatch_target": target,
        "connector_action": ALLOWED_ACTION_BY_TARGET[target],
        "connector_result": payload,
        "source_external_call_digest": _sha(dict(call)),
        "source_raw_result_digest": _sha(dict(raw)),
        "epoch": int(time.time()),
    }


def build_qi_github_actions_pr_live_external_result_bridge(*, runtime_context: Mapping[str, Any], pr_live_external_result_bridge_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveExternalResultBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(pr_live_external_result_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    call_path = root / "qi_github_actions_pr_live_external_call_packet.json"
    raw_result_path = root / "qi_github_actions_pr_live_external_call_raw_result_packet.json"
    receipt_path = root / "qi_github_actions_pr_live_external_result_bridge_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_external_result_bridge_audit.jsonl"

    if ctx.get("qi_github_actions_pr_live_external_result_bridge_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_external_result_bridge_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_external_result_bridge") is not True:
        blockers.append("apply_github_actions_pr_live_external_result_bridge_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_RESULT_BRIDGE_LICENSE_READY":
        blockers.append("github_actions_pr_live_external_result_bridge_license_not_ready")
    for name in ["external_call_packet_read_allowed", "raw_result_packet_read_allowed", "dispatch_result_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
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

    target = str(call.get("dispatch_target", "unknown")) if call else "unknown"
    if target not in RESULT_FILE_BY_TARGET:
        blockers.append("dispatch_target_not_allowlisted")
    if target in RESULT_FILE_BY_TARGET and lic.get(f"allow_{target}_result_bridge") is not True:
        blockers.append(f"{target}_not_allowed_by_external_result_bridge_license")
    action = str(call.get("connector_action", "unknown")) if call else "unknown"
    if target in ALLOWED_ACTION_BY_TARGET and action != ALLOWED_ACTION_BY_TARGET[target]:
        blockers.append("connector_action_mismatch")
    expected_file = str(call.get("dispatch_result_expected_file", "")) if call else ""
    if target in RESULT_FILE_BY_TARGET and expected_file and expected_file != RESULT_FILE_BY_TARGET[target]:
        blockers.append("dispatch_result_expected_file_mismatch")
    payload = _payload(raw) if raw else {}
    if target in RESULT_FILE_BY_TARGET and raw:
        _validate_payload(target, payload, blockers)

    dispatch_path = root / RESULT_FILE_BY_TARGET.get(target, "qi_github_actions_pr_live_dispatch_blocked_result.json")
    dispatch_result: dict[str, Any] = {}
    written = False
    if not blockers:
        dispatch_result = _dispatch_result(call, raw, target)
        _write_json(dispatch_path, dispatch_result)
        written = True

    status = "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_RESULT_BRIDGE_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_RESULT_BRIDGE_BLOCKED"
    packet_id = "qi-github-actions-pr-live-external-result-" + _sha({"call": call, "raw": raw, "target": target, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_live_external_result_bridge_v8_2",
        "status": status,
        "packet_id": packet_id,
        "dispatch_target": target,
        "connector_action": ALLOWED_ACTION_BY_TARGET.get(target, "unknown"),
        "dispatch_result_written": written,
        "dispatch_result_digest": _sha(dispatch_result),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPrLiveExternalResultBridgeResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_live_external_result_bridge_v8_2",
        status,
        packet_id,
        str(root),
        target,
        ALLOWED_ACTION_BY_TARGET.get(target, "unknown"),
        str(dispatch_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
