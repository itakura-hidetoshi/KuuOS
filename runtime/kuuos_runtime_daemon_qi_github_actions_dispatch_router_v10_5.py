#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


SOURCES = [
    ("policy_action", "qi_github_actions_policy_action_external_call_packet.json"),
    ("policy_reentry_pr_info", "qi_github_actions_policy_reentry_external_call_packet.json"),
    ("next_cycle_reobserve", "qi_github_actions_next_cycle_external_call_packet.json"),
    ("autopilot_observe", "qi_github_actions_pr_live_autopilot_handoff_packet.json"),
]

ALLOWED_CONNECTORS = {
    "GitHub.get_pr_info",
    "GitHub.fetch_commit_workflow_runs",
    "GitHub.merge_pull_request",
    "GitHub.rerun_failed_workflow_run_jobs",
}

EXPECTED_RESULT_FILE = {
    "GitHub.get_pr_info": "qi_github_actions_dispatch_pr_info_raw_result_packet.json",
    "GitHub.fetch_commit_workflow_runs": "qi_github_actions_dispatch_workflow_runs_raw_result_packet.json",
    "GitHub.merge_pull_request": "qi_github_actions_dispatch_merge_raw_result_packet.json",
    "GitHub.rerun_failed_workflow_run_jobs": "qi_github_actions_dispatch_rerun_raw_result_packet.json",
}


@dataclass(frozen=True)
class QiGitHubActionsDispatchRouterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    dispatch_kind: str
    connector_action: str
    dispatch_packet_path: str
    receipt_path: str
    audit_path: str
    dispatch_packet_written: bool
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


def _pick_source(root: pathlib.Path) -> tuple[str, str, dict[str, Any]]:
    for kind, name in SOURCES:
        packet = _read(root / name)
        if packet:
            return kind, name, packet
    return "none", "", {}


def _payload(packet: Mapping[str, Any]) -> dict[str, Any]:
    direct = _m(packet.get("connector_payload"))
    if direct:
        return dict(direct)
    action = str(packet.get("connector_action", ""))
    if action == "GitHub.get_pr_info":
        return {
            "repository_full_name": packet.get("repo_full_name") or packet.get("repository_full_name"),
            "pr_number": packet.get("pr_number") or packet.get("number"),
        }
    return {}


def _validate(action: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    if action not in ALLOWED_CONNECTORS:
        blockers.append("connector_action_not_allowlisted")
        return
    if action in {"GitHub.get_pr_info", "GitHub.merge_pull_request"}:
        repo = payload.get("repository_full_name") or payload.get("repo_full_name")
        if not isinstance(repo, str) or "/" not in repo:
            blockers.append("repository_full_name_invalid")
        try:
            pr_number = int(payload.get("pr_number") or payload.get("pull_number") or 0)
        except (TypeError, ValueError):
            pr_number = 0
        if pr_number <= 0:
            blockers.append("pr_number_invalid")
    elif action == "GitHub.fetch_commit_workflow_runs":
        repo = payload.get("repo_full_name") or payload.get("repository_full_name")
        if not isinstance(repo, str) or "/" not in repo:
            blockers.append("repo_full_name_invalid")
        if not str(payload.get("commit_sha", "")).strip():
            blockers.append("commit_sha_missing")
    elif action == "GitHub.rerun_failed_workflow_run_jobs":
        repo = payload.get("repo_full_name") or payload.get("repository_full_name")
        if not isinstance(repo, str) or "/" not in repo:
            blockers.append("repo_full_name_invalid")
        try:
            run_id = int(payload.get("run_id") or 0)
        except (TypeError, ValueError):
            run_id = 0
        if run_id <= 0:
            blockers.append("run_id_invalid")


def _dispatch_packet(kind: str, source_file: str, source: Mapping[str, Any], action: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_unified_dispatch_packet_v10_5",
        "dispatch_allowed": True,
        "dispatch_kind": kind,
        "connector_action": action,
        "connector_payload": dict(payload),
        "raw_result_expected_file": EXPECTED_RESULT_FILE.get(action, "qi_github_actions_dispatch_raw_result_packet.json"),
        "source_file": source_file,
        "source_packet_digest": _sha(dict(source)),
        "boundary": {
            "dispatch_packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "result_must_return_via_matching_bridge": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_dispatch_router(*, runtime_context: Mapping[str, Any], dispatch_router_license: Mapping[str, Any]) -> QiGitHubActionsDispatchRouterResult:
    ctx = _m(runtime_context)
    lic = _m(dispatch_router_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    dispatch_path = root / "qi_github_actions_unified_dispatch_packet.json"
    receipt_path = root / "qi_github_actions_dispatch_router_receipt.json"
    audit_path = root / "qi_github_actions_dispatch_router_audit.jsonl"

    if ctx.get("qi_github_actions_dispatch_router_enabled") is not True:
        blockers.append("qi_github_actions_dispatch_router_enabled_not_true")
    if ctx.get("apply_github_actions_dispatch_router") is not True:
        blockers.append("apply_github_actions_dispatch_router_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_DISPATCH_ROUTER_LICENSE_READY":
        blockers.append("github_actions_dispatch_router_license_not_ready")
    for name in ["external_call_packet_read_allowed", "dispatch_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    kind, source_file, source = _pick_source(root)
    if not source:
        blockers.append("dispatch_source_packet_missing_or_invalid")
    action = str(source.get("connector_action", "")) if source else "none"
    payload = _payload(source) if source else {}
    if source:
        _validate(action, payload, blockers)

    packet: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _dispatch_packet(kind, source_file, source, action, payload)
        _write(dispatch_path, packet)
        written = True

    status = "QI_GITHUB_ACTIONS_DISPATCH_ROUTER_READY" if not blockers else "QI_GITHUB_ACTIONS_DISPATCH_ROUTER_BLOCKED"
    packet_id = "qi-github-actions-dispatch-router-" + _sha({"kind": kind, "source": source, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_github_actions_dispatch_router_v10_5", "status": status, "packet_id": packet_id, "dispatch_kind": kind, "connector_action": action, "dispatch_packet_written": written, "dispatch_packet_digest": _sha(packet), "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsDispatchRouterResult("kuuos_runtime_daemon_qi_github_actions_dispatch_router_v10_5", status, packet_id, str(root), kind, action, str(dispatch_path), str(receipt_path), str(audit_path), written, blockers, warnings)
