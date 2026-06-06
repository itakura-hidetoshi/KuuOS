#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


DISPATCH_BY_ACTION = {
    "GitHub.get_pr_info": "pr_info",
    "GitHub.fetch_commit_workflow_runs": "commit_workflow_runs",
}

DISPATCH_FILE_BY_TARGET = {
    "pr_info": "qi_github_actions_pr_live_dispatch_pr_info_packet.json",
    "commit_workflow_runs": "qi_github_actions_pr_live_dispatch_commit_workflow_runs_packet.json",
}

RESULT_FILE_BY_TARGET = {
    "pr_info": "qi_github_actions_raw_pr_info_packet.json",
    "commit_workflow_runs": "qi_github_actions_raw_commit_workflow_runs_packet.json",
}


@dataclass(frozen=True)
class QiGitHubActionsPrLiveConnectorDispatcherResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    dispatch_target: str
    connector_action: str
    dispatch_packet_path: str
    bridge_request_path: str
    receipt_path: str
    audit_path: str
    dispatch_packet_written: bool
    bridge_request_written: bool
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


def _select_request(root: pathlib.Path) -> tuple[pathlib.Path, dict[str, Any]]:
    candidates = [
        root / "qi_github_actions_pr_live_connector_request.json",
        root / "qi_github_actions_pr_info_connector_request.json",
        root / "qi_github_actions_commit_workflow_runs_connector_request.json",
    ]
    for path in candidates:
        packet = _read_json(path)
        if packet:
            return path, packet
    return candidates[0], {}


def _validate_payload(target: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    repo = payload.get("repo_full_name") or payload.get("repository_full_name")
    if not isinstance(repo, str) or "/" not in repo:
        blockers.append("repo_full_name_invalid")
    if target == "pr_info" and _i(payload.get("pr_number", payload.get("pull_number")), 0) <= 0:
        blockers.append("pr_number_invalid")
    if target == "commit_workflow_runs" and not str(payload.get("commit_sha", "")).strip():
        blockers.append("commit_sha_missing")


def _canonical_payload(action: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    if action == "GitHub.get_pr_info":
        return {
            "repository_full_name": str(payload.get("repository_full_name") or payload.get("repo_full_name") or ""),
            "pr_number": _i(payload.get("pr_number", payload.get("pull_number")), 0),
        }
    return {
        "repo_full_name": str(payload.get("repo_full_name") or payload.get("repository_full_name") or ""),
        "commit_sha": str(payload.get("commit_sha", "")),
    }


def _dispatch_packet(source_path: pathlib.Path, request: Mapping[str, Any], target: str, action: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_pr_live_connector_dispatch_packet_v7_8",
        "dispatch_target": target,
        "connector_action": action,
        "connector_payload": dict(payload),
        "result_expected_file": RESULT_FILE_BY_TARGET[target],
        "bridge_result_file": "qi_github_actions_pr_live_connector_result_packet.json",
        "source_request_path": str(source_path),
        "source_request_digest": _sha(dict(request)),
        "boundary": {
            "dispatch_packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "feeds_pr_live_result_adapter_v7_6": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_pr_live_connector_dispatcher(*, runtime_context: Mapping[str, Any], pr_live_connector_dispatcher_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveConnectorDispatcherResult:
    ctx = _m(runtime_context)
    lic = _m(pr_live_connector_dispatcher_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_pr_live_connector_dispatcher_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_connector_dispatcher_audit.jsonl"
    bridge_request_path = root / "qi_github_actions_pr_live_connector_request.json"

    if ctx.get("qi_github_actions_pr_live_connector_dispatcher_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_connector_dispatcher_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_connector_dispatcher") is not True:
        blockers.append("apply_github_actions_pr_live_connector_dispatcher_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_CONNECTOR_DISPATCHER_LICENSE_READY":
        blockers.append("github_actions_pr_live_connector_dispatcher_license_not_ready")
    for name in ["connector_request_read_allowed", "dispatch_packet_write_allowed", "bridge_request_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    source_path, request = _select_request(root)
    if not request:
        blockers.append("connector_request_missing_or_invalid")
    action = str(request.get("connector_action", "unknown")) if request else "unknown"
    target = DISPATCH_BY_ACTION.get(action, "unknown")
    if target == "unknown":
        blockers.append("connector_action_not_dispatchable")
    if target != "unknown" and lic.get(f"allow_{target}_dispatch") is not True:
        blockers.append(f"{target}_not_allowed_by_pr_live_connector_dispatcher_license")
    raw_payload = _m(request.get("connector_payload")) if request else {}
    payload = _canonical_payload(action, raw_payload) if target != "unknown" else {}
    if target != "unknown":
        _validate_payload(target, payload, blockers)

    dispatch_path = root / DISPATCH_FILE_BY_TARGET.get(target, "qi_github_actions_pr_live_dispatch_blocked_packet.json")
    dispatch: dict[str, Any] = {}
    dispatch_written = False
    bridge_written = False
    if not blockers:
        dispatch = _dispatch_packet(source_path, request, target, action, payload)
        bridge_request = {
            "connector_action": action,
            "connector_payload": payload,
            "result_expected_file": RESULT_FILE_BY_TARGET[target],
            "source_dispatch_digest": _sha(dispatch),
            "epoch": int(time.time()),
        }
        _write_json(dispatch_path, dispatch)
        _write_json(bridge_request_path, bridge_request)
        dispatch_written = True
        bridge_written = True

    status = "QI_GITHUB_ACTIONS_PR_LIVE_CONNECTOR_DISPATCHER_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_CONNECTOR_DISPATCHER_BLOCKED"
    packet_id = "qi-github-actions-pr-live-dispatcher-" + _sha({"request": request, "target": target, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_live_connector_dispatcher_v7_8",
        "status": status,
        "packet_id": packet_id,
        "dispatch_target": target,
        "connector_action": action,
        "dispatch_packet_written": dispatch_written,
        "bridge_request_written": bridge_written,
        "dispatch_packet_digest": _sha(dispatch),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPrLiveConnectorDispatcherResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_live_connector_dispatcher_v7_8",
        status,
        packet_id,
        str(root),
        target,
        action,
        str(dispatch_path),
        str(bridge_request_path),
        str(receipt_path),
        str(audit_path),
        dispatch_written,
        bridge_written,
        blockers,
        warnings,
    )
