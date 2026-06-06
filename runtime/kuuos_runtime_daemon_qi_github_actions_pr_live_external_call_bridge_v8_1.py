#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


DISPATCH_PACKET_BY_TARGET = {
    "pr_info": "qi_github_actions_pr_live_dispatch_pr_info_packet.json",
    "commit_workflow_runs": "qi_github_actions_pr_live_dispatch_commit_workflow_runs_packet.json",
}

DISPATCH_RESULT_BY_TARGET = {
    "pr_info": "qi_github_actions_pr_live_dispatch_pr_info_result.json",
    "commit_workflow_runs": "qi_github_actions_pr_live_dispatch_commit_workflow_runs_result.json",
}

ALLOWED_ACTION_BY_TARGET = {
    "pr_info": "GitHub.get_pr_info",
    "commit_workflow_runs": "GitHub.fetch_commit_workflow_runs",
}


@dataclass(frozen=True)
class QiGitHubActionsPrLiveExternalCallBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    dispatch_target: str
    connector_action: str
    external_call_packet_path: str
    receipt_path: str
    audit_path: str
    external_call_packet_written: bool
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


def _infer_target(root: pathlib.Path, ctx: Mapping[str, Any]) -> str:
    explicit = str(ctx.get("dispatch_target", ""))
    if explicit in DISPATCH_PACKET_BY_TARGET:
        return explicit
    for target, file_name in DISPATCH_PACKET_BY_TARGET.items():
        if _read_json(root / file_name):
            return target
    return "unknown"


def _validate_payload(target: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    repo = payload.get("repo_full_name") or payload.get("repository_full_name")
    if not isinstance(repo, str) or "/" not in repo:
        blockers.append("repo_full_name_invalid")
    if target == "pr_info" and _i(payload.get("pr_number", payload.get("pull_number")), 0) <= 0:
        blockers.append("pr_number_invalid")
    if target == "commit_workflow_runs" and not str(payload.get("commit_sha", "")).strip():
        blockers.append("commit_sha_missing")


def _canonical_payload(target: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    if target == "pr_info":
        return {
            "repository_full_name": str(payload.get("repository_full_name") or payload.get("repo_full_name") or ""),
            "pr_number": _i(payload.get("pr_number", payload.get("pull_number")), 0),
        }
    return {
        "repo_full_name": str(payload.get("repo_full_name") or payload.get("repository_full_name") or ""),
        "commit_sha": str(payload.get("commit_sha", "")),
    }


def _external_call_packet(dispatch: Mapping[str, Any], target: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_pr_live_external_call_packet_v8_1",
        "external_call_allowed": True,
        "dispatch_target": target,
        "connector_action": ALLOWED_ACTION_BY_TARGET[target],
        "connector_payload": dict(payload),
        "dispatch_result_expected_file": DISPATCH_RESULT_BY_TARGET[target],
        "pr_live_connector_result_file": "qi_github_actions_pr_live_connector_result_packet.json",
        "next_collector": "kuuos_runtime_daemon_qi_github_actions_pr_live_dispatch_result_collector_v7_9",
        "source_dispatch_digest": _sha(dict(dispatch)),
        "boundary": {
            "packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "result_must_be_collected_by_v7_9": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_pr_live_external_call_bridge(*, runtime_context: Mapping[str, Any], pr_live_external_call_bridge_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveExternalCallBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(pr_live_external_call_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    external_call_path = root / "qi_github_actions_pr_live_external_call_packet.json"
    receipt_path = root / "qi_github_actions_pr_live_external_call_bridge_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_external_call_bridge_audit.jsonl"

    if ctx.get("qi_github_actions_pr_live_external_call_bridge_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_external_call_bridge_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_external_call_bridge") is not True:
        blockers.append("apply_github_actions_pr_live_external_call_bridge_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CALL_BRIDGE_LICENSE_READY":
        blockers.append("github_actions_pr_live_external_call_bridge_license_not_ready")
    for name in ["dispatch_packet_read_allowed", "external_call_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    target = _infer_target(root, ctx)
    if target not in DISPATCH_PACKET_BY_TARGET:
        blockers.append("dispatch_target_not_allowlisted")
    if target in DISPATCH_PACKET_BY_TARGET and lic.get(f"allow_{target}_external_call") is not True:
        blockers.append(f"{target}_not_allowed_by_external_call_bridge_license")

    dispatch = _read_json(root / DISPATCH_PACKET_BY_TARGET.get(target, "missing")) if target in DISPATCH_PACKET_BY_TARGET else {}
    if not dispatch:
        blockers.append("dispatch_packet_missing_or_invalid")
    action = str(dispatch.get("connector_action", "unknown")) if dispatch else "unknown"
    if target in ALLOWED_ACTION_BY_TARGET and action != ALLOWED_ACTION_BY_TARGET[target]:
        blockers.append("connector_action_mismatch")
    if dispatch and str(dispatch.get("dispatch_target", "")) != target:
        blockers.append("dispatch_target_mismatch")
    payload = _canonical_payload(target, _m(dispatch.get("connector_payload"))) if target in DISPATCH_PACKET_BY_TARGET and dispatch else {}
    if target in DISPATCH_PACKET_BY_TARGET and dispatch:
        _validate_payload(target, payload, blockers)

    packet: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _external_call_packet(dispatch, target, payload)
        _write_json(external_call_path, packet)
        written = True

    status = "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CALL_BRIDGE_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CALL_BRIDGE_BLOCKED"
    packet_id = "qi-github-actions-pr-live-external-call-" + _sha({"target": target, "dispatch": dispatch, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_live_external_call_bridge_v8_1",
        "status": status,
        "packet_id": packet_id,
        "dispatch_target": target,
        "connector_action": ALLOWED_ACTION_BY_TARGET.get(target, "unknown"),
        "external_call_packet_written": written,
        "external_call_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPrLiveExternalCallBridgeResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_live_external_call_bridge_v8_1",
        status,
        packet_id,
        str(root),
        target,
        ALLOWED_ACTION_BY_TARGET.get(target, "unknown"),
        str(external_call_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
