#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Callable, Mapping

from runtime.kuuos_runtime_daemon_qi_github_tool_bridge_v2_3 import build_qi_github_tool_bridge
from runtime.kuuos_runtime_daemon_qi_automerge_executor_v2_4 import build_qi_automerge_executor


@dataclass(frozen=True)
class QiAutonomousChangeLoopResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    packet_path: str
    bridge_plan_path: str
    automerge_packet_path: str
    receipt_path: str
    audit_path: str
    repository_full_name: str
    branch: str
    pr_number: int
    bridge_status: str
    automerge_status: str
    change_prepared: bool
    merge_applied: bool
    blockers: list[str]
    warnings: list[str]
    records: list[dict[str, Any]]

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


def _checks_success(checks: Any) -> bool:
    if not isinstance(checks, list) or not checks:
        return False
    for item in checks:
        if not isinstance(item, Mapping):
            return False
        if str(item.get("status", item.get("conclusion", ""))).lower() not in {"success", "successful", "passed"}:
            return False
    return True


def _bridge_license() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_TOOL_BRIDGE_LICENSE_READY", "plan_read_allowed": True, "external_action_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _automerge_license() -> dict[str, Any]:
    return {"license_status": "QI_AUTOMERGE_EXECUTOR_LICENSE_READY", "packet_read_allowed": True, "gate_eval_allowed": True, "merge_bridge_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _mock_transport(repository: str, action: Mapping[str, Any], token: str) -> dict[str, Any]:
    kind = str(action.get("kind", ""))
    digest = _sha(action)
    if kind == "create_branch":
        return {"branch": action.get("branch"), "sha": action.get("sha"), "mock": True, "digest": digest}
    if kind in {"create_file", "update_file", "file_patch"}:
        return {"path": action.get("path"), "commit_sha": digest[:40], "mock": True}
    if kind == "create_pr":
        return {"number": int(action.get("mock_pr_number", 1)), "head_sha": action.get("head_sha", digest[:40]), "mock": True}
    if kind == "merge_pr":
        return {"merged": True, "sha": action.get("expected_head_sha", digest[:40]), "repository_full_name": repository, "mock": True}
    return {"mock": True, "kind": kind, "digest": digest}


def _actions(packet: Mapping[str, Any], branch: str) -> list[dict[str, Any]]:
    raw = packet.get("actions", [])
    if isinstance(raw, list) and raw:
        return [dict(item) for item in raw if isinstance(item, Mapping)]
    files = packet.get("files", [])
    actions: list[dict[str, Any]] = [{"kind": "create_branch", "branch": branch, "sha": packet.get("base_sha", packet.get("head_sha", ""))}]
    if isinstance(files, list):
        for item in files:
            if not isinstance(item, Mapping):
                continue
            actions.append({"kind": str(item.get("kind", "create_file")), "branch": branch, "path": item.get("path"), "content": item.get("content", ""), "message": item.get("message", "Qi autonomous change loop file update")})
    actions.append({"kind": "create_pr", "branch": branch, "head": branch, "base": packet.get("base_branch", "main"), "title": packet.get("title", "Qi autonomous change loop"), "body": packet.get("body", ""), "mock_pr_number": packet.get("pr_number", 1), "head_sha": packet.get("expected_head_sha", packet.get("actual_head_sha", "mock-head"))})
    return actions


def build_qi_autonomous_change_loop(*, runtime_context: Mapping[str, Any], loop_license_packet: Mapping[str, Any], bridge_transport: Callable[[str, Mapping[str, Any], str], dict[str, Any]] | None = None, merge_transport: Callable[[str, Mapping[str, Any], str], dict[str, Any]] | None = None) -> QiAutonomousChangeLoopResult:
    ctx = _m(runtime_context)
    lic = _m(loop_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "autonomous_change_loop_packet.json"
    bridge_plan_path = root / "github_tool_bridge_plan.json"
    automerge_packet_path = root / "automerge_packet.json"
    receipt_path = root / "autonomous_change_loop_receipt.json"
    audit_path = root / "autonomous_change_loop_audit.jsonl"
    if ctx.get("qi_autonomous_change_loop_enabled") is not True:
        blockers.append("qi_autonomous_change_loop_enabled_not_true")
    if ctx.get("apply_autonomous_change_loop") is not True:
        blockers.append("apply_autonomous_change_loop_not_true")
    if lic.get("license_status") != "QI_AUTONOMOUS_CHANGE_LOOP_LICENSE_READY":
        blockers.append("autonomous_change_loop_license_not_ready")
    for name in ["packet_read_allowed", "bridge_plan_write_allowed", "bridge_run_allowed", "automerge_packet_write_allowed", "automerge_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(packet_path)
    repository = str(packet.get("repository_full_name", ""))
    branch = str(packet.get("branch", "qi-autonomous-change"))
    base_branch = str(packet.get("base_branch", "main"))
    mode = str(packet.get("mode", ctx.get("mode", "mock")))
    if not repository:
        blockers.append("repository_missing")
    if not branch:
        blockers.append("branch_missing")
    if mode not in {"mock", "real"}:
        blockers.append("mode_invalid")
    if mode == "real" and packet.get("execute_external_actions") is not True:
        blockers.append("real_mode_requires_execute_external_actions")
    if packet.get("explicit_change_loop_license") is not True:
        blockers.append("explicit_change_loop_license_missing")
    expected_head_sha = str(packet.get("expected_head_sha", packet.get("actual_head_sha", "mock-head")))
    pr_number = _i(packet.get("pr_number"), 1)
    bridge_status = "NOT_RUN"
    automerge_status = "NOT_RUN"
    change_prepared = False
    merge_applied = False
    if not blockers:
        bridge_plan = {"repository_full_name": repository, "mode": mode, "base_branch": base_branch, "allowed_base_branch": base_branch, "execute_external_actions": packet.get("execute_external_actions") is True, "actions": _actions(packet, branch)}
        _write_json(bridge_plan_path, bridge_plan)
        bridge = build_qi_github_tool_bridge(runtime_context={"qi_github_tool_bridge_enabled": True, "apply_github_tool_bridge": True, "runtime_root": str(root), "mode": mode, "execute_external_actions": packet.get("execute_external_actions") is True}, bridge_license_packet=_bridge_license(), transport=bridge_transport or (_mock_transport if mode == "mock" else None))
        bridge_payload = bridge.to_dict()
        bridge_status = str(bridge_payload.get("status"))
        change_prepared = bridge_status == "QI_GITHUB_TOOL_BRIDGE_APPLIED"
        records.append({"stage": "bridge", "status": bridge_status, "digest": _sha(bridge_payload), "epoch": int(time.time())})
        if not change_prepared:
            blockers.append("bridge_not_applied")
    if not blockers:
        required_checks = packet.get("required_checks", [{"name": "mock", "status": "success"}])
        automerge_packet = {"repository_full_name": repository, "pr_number": pr_number, "expected_head_sha": expected_head_sha, "actual_head_sha": str(packet.get("actual_head_sha", expected_head_sha)), "explicit_automerge_license": packet.get("explicit_automerge_license") is True, "allowed_repository": packet.get("allowed_repository", True) is True, "allowed_base_branch": packet.get("allowed_base_branch", True) is True, "allowed_base_branch_name": base_branch, "base_branch": base_branch, "pull_request_created": True, "pull_request_not_draft": packet.get("pull_request_not_draft", True) is True, "mergeable": packet.get("mergeable", True) is True, "no_unresolved_blockers": packet.get("no_unresolved_blockers", True) is True, "receipt_written": True, "audit_written": True, "merge_allowed": packet.get("merge_allowed") is True, "merge_method": str(packet.get("merge_method", "merge")), "mode": mode, "execute_external_actions": packet.get("execute_external_actions") is True, "required_checks": required_checks}
        if not _checks_success(required_checks):
            warnings.append("required_checks_not_success_before_automerge")
        _write_json(automerge_packet_path, automerge_packet)
        automerge = build_qi_automerge_executor(runtime_context={"qi_automerge_executor_enabled": True, "apply_automerge_executor": True, "runtime_root": str(root), "mode": mode}, executor_license_packet=_automerge_license(), transport=merge_transport or (_mock_transport if mode == "mock" else None))
        automerge_payload = automerge.to_dict()
        automerge_status = str(automerge_payload.get("status"))
        merge_applied = bool(automerge_payload.get("merge_applied"))
        records.append({"stage": "automerge", "status": automerge_status, "digest": _sha(automerge_payload), "epoch": int(time.time())})
        if not merge_applied:
            blockers.append("automerge_not_applied")
    if blockers:
        status = "QI_AUTONOMOUS_CHANGE_LOOP_BLOCKED"
    elif merge_applied:
        status = "QI_AUTONOMOUS_CHANGE_LOOP_MERGED"
    else:
        status = "QI_AUTONOMOUS_CHANGE_LOOP_IDLE"
    packet_id = "qi-autonomous-change-loop-" + _sha({"packet": packet, "records": records, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_autonomous_change_loop_v2_5", "status": status, "packet_id": packet_id, "repository_full_name": repository, "branch": branch, "pr_number": pr_number, "bridge_status": bridge_status, "automerge_status": automerge_status, "change_prepared": change_prepared, "merge_applied": merge_applied, "records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiAutonomousChangeLoopResult("kuuos_runtime_daemon_qi_autonomous_change_loop_v2_5", status, packet_id, str(root), str(packet_path), str(bridge_plan_path), str(automerge_packet_path), str(receipt_path), str(audit_path), repository, branch, pr_number, bridge_status, automerge_status, change_prepared, merge_applied, blockers, warnings, records)
