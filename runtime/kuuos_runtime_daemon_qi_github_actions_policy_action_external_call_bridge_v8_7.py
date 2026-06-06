#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ALLOWED_ACTIONS = {
    "merge_pull_request": "GitHub.merge_pull_request",
    "rerun_failed_workflow_run_jobs": "GitHub.rerun_failed_workflow_run_jobs",
    "reobserve_commit_workflow_runs": "GitHub.fetch_commit_workflow_runs",
}

RESULT_FILE_BY_ACTION = {
    "merge_pull_request": "qi_github_actions_policy_action_merge_result_packet.json",
    "rerun_failed_workflow_run_jobs": "qi_github_actions_policy_action_rerun_result_packet.json",
    "reobserve_commit_workflow_runs": "qi_github_actions_policy_action_reobserve_result_packet.json",
}


@dataclass(frozen=True)
class QiGitHubActionsPolicyActionExternalCallBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    action_kind: str
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


def _validate_payload(kind: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    repo = payload.get("repo_full_name") or payload.get("repository_full_name")
    if not isinstance(repo, str) or "/" not in repo:
        blockers.append("repo_full_name_invalid")
    if kind == "merge_pull_request":
        if _i(payload.get("pr_number"), 0) <= 0:
            blockers.append("pr_number_invalid")
        if not str(payload.get("expected_head_sha", "")).strip():
            blockers.append("expected_head_sha_missing")
        if str(payload.get("merge_method", "merge")) not in {"merge", "squash", "rebase"}:
            blockers.append("merge_method_invalid")
    elif kind == "rerun_failed_workflow_run_jobs":
        if _i(payload.get("run_id"), 0) <= 0:
            blockers.append("run_id_invalid")
    elif kind == "reobserve_commit_workflow_runs":
        if not str(payload.get("commit_sha", "")).strip():
            blockers.append("commit_sha_missing")


def _canonical_payload(kind: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    if kind == "merge_pull_request":
        return {
            "repository_full_name": str(payload.get("repository_full_name") or payload.get("repo_full_name") or ""),
            "pr_number": _i(payload.get("pr_number"), 0),
            "merge_method": str(payload.get("merge_method", "merge")),
            "expected_head_sha": str(payload.get("expected_head_sha", "")),
        }
    if kind == "rerun_failed_workflow_run_jobs":
        return {
            "repo_full_name": str(payload.get("repo_full_name") or payload.get("repository_full_name") or ""),
            "run_id": _i(payload.get("run_id"), 0),
        }
    return {
        "repo_full_name": str(payload.get("repo_full_name") or payload.get("repository_full_name") or ""),
        "commit_sha": str(payload.get("commit_sha", "")),
    }


def _external_call_packet(handoff: Mapping[str, Any], kind: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_policy_action_external_call_packet_v8_7",
        "external_call_allowed": True,
        "action_kind": kind,
        "connector_action": ALLOWED_ACTIONS[kind],
        "connector_payload": dict(payload),
        "action_result_expected_file": RESULT_FILE_BY_ACTION[kind],
        "source_handoff_digest": _sha(dict(handoff)),
        "boundary": {
            "packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "requires_action_handoff_allowed": True,
            "result_must_be_collected_by_next_result_bridge": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_policy_action_external_call_bridge(*, runtime_context: Mapping[str, Any], policy_action_external_call_bridge_license: Mapping[str, Any]) -> QiGitHubActionsPolicyActionExternalCallBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(policy_action_external_call_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    handoff_path = root / "qi_github_actions_autopilot_policy_action_handoff_packet.json"
    external_call_path = root / "qi_github_actions_policy_action_external_call_packet.json"
    receipt_path = root / "qi_github_actions_policy_action_external_call_bridge_receipt.json"
    audit_path = root / "qi_github_actions_policy_action_external_call_bridge_audit.jsonl"

    if ctx.get("qi_github_actions_policy_action_external_call_bridge_enabled") is not True:
        blockers.append("qi_github_actions_policy_action_external_call_bridge_enabled_not_true")
    if ctx.get("apply_github_actions_policy_action_external_call_bridge") is not True:
        blockers.append("apply_github_actions_policy_action_external_call_bridge_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_CALL_BRIDGE_LICENSE_READY":
        blockers.append("github_actions_policy_action_external_call_bridge_license_not_ready")
    for name in ["action_handoff_packet_read_allowed", "external_call_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    handoff = _read_json(handoff_path)
    if not handoff:
        blockers.append("action_handoff_packet_missing_or_invalid")
    if handoff and handoff.get("action_handoff_allowed") is not True:
        blockers.append("action_handoff_allowed_not_true")
    kind = str(handoff.get("action_kind", "unknown")) if handoff else "unknown"
    if kind not in ALLOWED_ACTIONS:
        blockers.append("action_kind_not_allowlisted")
    if kind in ALLOWED_ACTIONS and lic.get(f"allow_{kind}_external_call") is not True:
        blockers.append(f"{kind}_not_allowed_by_policy_action_external_call_bridge_license")
    expected_action = ALLOWED_ACTIONS.get(kind, "unknown")
    if handoff and str(handoff.get("connector_action", "unknown")) != expected_action:
        blockers.append("connector_action_mismatch")

    payload = _canonical_payload(kind, _m(handoff.get("connector_payload"))) if kind in ALLOWED_ACTIONS and handoff else {}
    if kind in ALLOWED_ACTIONS and handoff:
        _validate_payload(kind, payload, blockers)

    packet: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _external_call_packet(handoff, kind, payload)
        _write_json(external_call_path, packet)
        written = True

    status = "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_CALL_BRIDGE_READY" if not blockers else "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_CALL_BRIDGE_BLOCKED"
    packet_id = "qi-github-actions-policy-action-external-call-" + _sha({"handoff": handoff, "kind": kind, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_policy_action_external_call_bridge_v8_7",
        "status": status,
        "packet_id": packet_id,
        "action_kind": kind,
        "connector_action": expected_action,
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

    return QiGitHubActionsPolicyActionExternalCallBridgeResult(
        "kuuos_runtime_daemon_qi_github_actions_policy_action_external_call_bridge_v8_7",
        status,
        packet_id,
        str(root),
        kind,
        expected_action,
        str(external_call_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
