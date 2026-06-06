#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

TARGET_BY_ACTION = {
    "GitHub.get_pr_info": "qi_github_actions_policy_reentry_pr_info_raw_result_packet.json",
    "GitHub.fetch_commit_workflow_runs": "qi_github_actions_next_cycle_external_call_raw_result_packet.json",
    "GitHub.merge_pull_request": "qi_github_actions_policy_action_external_call_raw_result_packet.json",
    "GitHub.rerun_failed_workflow_run_jobs": "qi_github_actions_policy_action_external_call_raw_result_packet.json",
}

RAW_CANDIDATES = [
    "qi_github_actions_dispatch_pr_info_raw_result_packet.json",
    "qi_github_actions_dispatch_workflow_runs_raw_result_packet.json",
    "qi_github_actions_dispatch_merge_raw_result_packet.json",
    "qi_github_actions_dispatch_rerun_raw_result_packet.json",
    "qi_github_actions_unified_dispatch_raw_result_packet.json",
]

@dataclass(frozen=True)
class QiGitHubActionsDispatchResultRouterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    dispatch_kind: str
    connector_action: str
    target_packet_path: str
    receipt_path: str
    audit_path: str
    target_packet_written: bool
    blockers: list[str]
    warnings: list[str]
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(v: Any) -> Mapping[str, Any]:
    return v if isinstance(v, Mapping) else {}


def _sha(v: Any) -> str:
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _root(v: Any, blockers: list[str]) -> pathlib.Path:
    if not v:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(v)).expanduser().resolve()
    if str(root) == "/":
        blockers.append("runtime_root_forbidden")
    return root


def _read(p: pathlib.Path) -> dict[str, Any]:
    if not p.is_file():
        return {}
    try:
        v = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return v if isinstance(v, dict) else {}


def _write(p: pathlib.Path, payload: Mapping[str, Any]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, p)


def _append(p: pathlib.Path, payload: Mapping[str, Any]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _pick_raw(root: pathlib.Path, dispatch: Mapping[str, Any]) -> tuple[str, dict[str, Any]]:
    preferred = str(dispatch.get("raw_result_expected_file", ""))
    if preferred:
        raw = _read(root / preferred)
        if raw:
            return preferred, raw
    for name in RAW_CANDIDATES:
        raw = _read(root / name)
        if raw:
            return name, raw
    return "", {}


def _payload(raw: Mapping[str, Any]) -> dict[str, Any]:
    nested = raw.get("connector_result")
    if isinstance(nested, Mapping):
        return {**dict(nested), "connector_action": raw.get("connector_action", nested.get("connector_action"))}
    return dict(raw)


def _validate(dispatch: Mapping[str, Any], raw: Mapping[str, Any], blockers: list[str]) -> str:
    if dispatch.get("dispatch_allowed") is not True:
        blockers.append("dispatch_allowed_not_true")
    action = str(dispatch.get("connector_action", ""))
    if action not in TARGET_BY_ACTION:
        blockers.append("connector_action_not_allowlisted")
    raw_action = str(raw.get("connector_action", action))
    if raw_action and raw_action != action:
        blockers.append("raw_result_connector_action_mismatch")
    if action == "GitHub.get_pr_info":
        payload = _payload(raw)
        repo = payload.get("repo_full_name") or payload.get("repository_full_name")
        if not isinstance(repo, str) or "/" not in repo:
            blockers.append("repo_full_name_missing")
        try:
            n = int(payload.get("number") or payload.get("pr_number") or 0)
        except (TypeError, ValueError):
            n = 0
        if n <= 0:
            blockers.append("pr_number_missing")
    elif action == "GitHub.fetch_commit_workflow_runs":
        payload = _payload(raw)
        runs = payload.get("workflow_runs")
        if not isinstance(runs, list) or not runs:
            blockers.append("workflow_runs_empty_or_invalid")
    elif action == "GitHub.merge_pull_request":
        payload = _payload(raw)
        if payload.get("merged") is not True:
            blockers.append("merge_result_not_merged_true")
    elif action == "GitHub.rerun_failed_workflow_run_jobs":
        payload = _payload(raw)
        if not (payload.get("success") is True or payload.get("rerun_requested") is True or payload.get("status") in {"queued", "requested"}):
            blockers.append("rerun_result_not_acknowledged")
    return action


def _target_payload(dispatch: Mapping[str, Any], raw_name: str, raw: Mapping[str, Any]) -> dict[str, Any]:
    payload = _payload(raw)
    return {
        **payload,
        "connector_action": dispatch.get("connector_action"),
        "dispatch_kind": dispatch.get("dispatch_kind"),
        "source_dispatch_digest": _sha(dict(dispatch)),
        "source_dispatch_raw_file": raw_name,
        "source_dispatch_raw_digest": _sha(dict(raw)),
        "routed_by": "kuuos_runtime_daemon_qi_github_actions_dispatch_result_router_v10_6",
        "epoch": int(time.time()),
    }


def build_qi_github_actions_dispatch_result_router(*, runtime_context: Mapping[str, Any], dispatch_result_router_license: Mapping[str, Any]) -> QiGitHubActionsDispatchResultRouterResult:
    ctx = _m(runtime_context)
    lic = _m(dispatch_result_router_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    dispatch_path = root / "qi_github_actions_unified_dispatch_packet.json"
    receipt_path = root / "qi_github_actions_dispatch_result_router_receipt.json"
    audit_path = root / "qi_github_actions_dispatch_result_router_audit.jsonl"

    if ctx.get("qi_github_actions_dispatch_result_router_enabled") is not True:
        blockers.append("qi_github_actions_dispatch_result_router_enabled_not_true")
    if ctx.get("apply_github_actions_dispatch_result_router") is not True:
        blockers.append("apply_github_actions_dispatch_result_router_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_DISPATCH_RESULT_ROUTER_LICENSE_READY":
        blockers.append("github_actions_dispatch_result_router_license_not_ready")
    for name in ["dispatch_packet_read_allowed", "raw_result_packet_read_allowed", "target_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    dispatch = _read(dispatch_path)
    if not dispatch:
        blockers.append("dispatch_packet_missing_or_invalid")
    raw_name, raw = _pick_raw(root, dispatch) if dispatch else ("", {})
    if dispatch and not raw:
        blockers.append("dispatch_raw_result_missing_or_invalid")
    action = _validate(dispatch, raw, blockers) if dispatch and raw else "none"
    target_path = root / TARGET_BY_ACTION.get(action, "qi_github_actions_dispatch_result_blocked_packet.json")
    target: dict[str, Any] = {}
    written = False
    if not blockers:
        target = _target_payload(dispatch, raw_name, raw)
        _write(target_path, target)
        written = True

    status = "QI_GITHUB_ACTIONS_DISPATCH_RESULT_ROUTER_READY" if not blockers else "QI_GITHUB_ACTIONS_DISPATCH_RESULT_ROUTER_BLOCKED"
    packet_id = "qi-github-actions-dispatch-result-router-" + _sha({"dispatch": dispatch, "raw": raw, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_github_actions_dispatch_result_router_v10_6", "status": status, "packet_id": packet_id, "dispatch_kind": str(dispatch.get("dispatch_kind", "none")) if dispatch else "none", "connector_action": action, "target_packet_path": str(target_path), "target_packet_written": written, "target_packet_digest": _sha(target), "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsDispatchResultRouterResult("kuuos_runtime_daemon_qi_github_actions_dispatch_result_router_v10_6", status, packet_id, str(root), str(dispatch.get("dispatch_kind", "none")) if dispatch else "none", action, str(target_path), str(receipt_path), str(audit_path), written, blockers, warnings)
