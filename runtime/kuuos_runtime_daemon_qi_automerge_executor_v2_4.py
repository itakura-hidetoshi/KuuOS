#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Callable, Mapping

from runtime.kuuos_runtime_daemon_qi_pr_merge_gate_v2_1 import build_qi_pr_merge_gate
from runtime.kuuos_runtime_daemon_qi_github_tool_bridge_v2_3 import build_qi_github_tool_bridge


@dataclass(frozen=True)
class QiAutomergeExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    packet_path: str
    receipt_path: str
    audit_path: str
    repository_full_name: str
    pr_number: int
    expected_head_sha: str
    gate_status: str
    bridge_status: str
    merge_attempted: bool
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


def _gate_license() -> dict[str, Any]:
    return {"license_status": "QI_PR_MERGE_GATE_LICENSE_READY", "gate_packet_read_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _bridge_license() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_TOOL_BRIDGE_LICENSE_READY", "plan_read_allowed": True, "external_action_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _mock_merge_transport(repository: str, action: Mapping[str, Any], token: str) -> dict[str, Any]:
    if str(action.get("kind")) == "merge_pr":
        return {"merged": True, "sha": action.get("expected_head_sha"), "repository_full_name": repository, "mock": True}
    return {"mock": True, "ignored": action.get("kind")}


def build_qi_automerge_executor(*, runtime_context: Mapping[str, Any], executor_license_packet: Mapping[str, Any], transport: Callable[[str, Mapping[str, Any], str], dict[str, Any]] | None = None) -> QiAutomergeExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(executor_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "automerge_packet.json"
    receipt_path = root / "automerge_receipt.json"
    audit_path = root / "automerge_audit.jsonl"
    gate_packet_path = root / "pr_merge_gate_packet.json"
    bridge_plan_path = root / "github_tool_bridge_plan.json"
    if ctx.get("qi_automerge_executor_enabled") is not True:
        blockers.append("qi_automerge_executor_enabled_not_true")
    if ctx.get("apply_automerge_executor") is not True:
        blockers.append("apply_automerge_executor_not_true")
    if lic.get("license_status") != "QI_AUTOMERGE_EXECUTOR_LICENSE_READY":
        blockers.append("automerge_executor_license_not_ready")
    for name in ["packet_read_allowed", "gate_eval_allowed", "merge_bridge_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(packet_path)
    repository = str(packet.get("repository_full_name", ""))
    pr_number = _i(packet.get("pr_number"), 0)
    expected_head_sha = str(packet.get("expected_head_sha", ""))
    actual_head_sha = str(packet.get("actual_head_sha", expected_head_sha))
    if not repository:
        blockers.append("repository_missing")
    if pr_number <= 0:
        blockers.append("pr_number_invalid")
    if not expected_head_sha:
        blockers.append("expected_head_sha_missing")
    if actual_head_sha != expected_head_sha:
        blockers.append("head_sha_mismatch")
    if packet.get("explicit_automerge_license") is not True:
        blockers.append("explicit_automerge_license_missing")
    if packet.get("pull_request_not_draft") is not True:
        blockers.append("pull_request_is_draft")
    if packet.get("mergeable") is not True:
        blockers.append("pull_request_not_mergeable")
    if not _checks_success(packet.get("required_checks", [])):
        blockers.append("required_checks_not_success")
    mode = str(packet.get("mode", ctx.get("mode", "mock")))
    if mode not in {"mock", "real"}:
        blockers.append("mode_invalid")
    if mode == "real" and packet.get("execute_external_actions") is not True:
        blockers.append("real_mode_requires_execute_external_actions")
    gate_status = "NOT_RUN"
    bridge_status = "NOT_RUN"
    merge_attempted = False
    merge_applied = False
    if not blockers:
        gate_packet = {
            "repository_full_name": repository,
            "pr_number": pr_number,
            "expected_head_sha": expected_head_sha,
            "actual_head_sha": actual_head_sha,
            "explicit_automerge_license": True,
            "allowed_repository": packet.get("allowed_repository") is True,
            "allowed_base_branch": packet.get("allowed_base_branch") is True,
            "pull_request_created": packet.get("pull_request_created") is True,
            "pull_request_not_draft": True,
            "mergeable": True,
            "no_unresolved_blockers": packet.get("no_unresolved_blockers") is True,
            "receipt_written": packet.get("receipt_written") is True,
            "audit_written": packet.get("audit_written") is True,
            "merge_allowed": packet.get("merge_allowed") is True,
            "merge_method": str(packet.get("merge_method", "merge")),
            "required_checks": packet.get("required_checks", []),
        }
        _write_json(gate_packet_path, gate_packet)
        gate = build_qi_pr_merge_gate(runtime_context={"qi_pr_merge_gate_enabled": True, "apply_pr_merge_gate": True, "runtime_root": str(root)}, gate_license_packet=_gate_license())
        gate_payload = gate.to_dict()
        gate_status = str(gate_payload.get("status"))
        records.append({"stage": "gate", "status": gate_status, "digest": _sha(gate_payload), "epoch": int(time.time())})
        if gate_status != "QI_PR_MERGE_GATE_PASSED" or gate_payload.get("merge_allowed") is not True:
            blockers.append("merge_gate_not_passed")
    if not blockers:
        bridge_plan = {
            "repository_full_name": repository,
            "mode": mode,
            "base_branch": str(packet.get("base_branch", "main")),
            "allowed_base_branch": str(packet.get("allowed_base_branch_name", packet.get("base_branch", "main"))),
            "execute_external_actions": packet.get("execute_external_actions") is True,
            "actions": [{"kind": "merge_pr", "pr_number": pr_number, "expected_head_sha": expected_head_sha, "merge_method": str(packet.get("merge_method", "merge"))}],
        }
        _write_json(bridge_plan_path, bridge_plan)
        merge_attempted = True
        bridge = build_qi_github_tool_bridge(runtime_context={"qi_github_tool_bridge_enabled": True, "apply_github_tool_bridge": True, "runtime_root": str(root), "mode": mode, "execute_external_actions": packet.get("execute_external_actions") is True}, bridge_license_packet=_bridge_license(), transport=transport or (_mock_merge_transport if mode == "mock" else None))
        bridge_payload = bridge.to_dict()
        bridge_status = str(bridge_payload.get("status"))
        merge_applied = bridge_status == "QI_GITHUB_TOOL_BRIDGE_APPLIED"
        records.append({"stage": "bridge", "status": bridge_status, "digest": _sha(bridge_payload), "epoch": int(time.time())})
        if not merge_applied:
            blockers.append("merge_bridge_not_applied")
    if blockers:
        status = "QI_AUTOMERGE_EXECUTOR_BLOCKED"
    elif merge_applied:
        status = "QI_AUTOMERGE_EXECUTOR_MERGED"
    else:
        status = "QI_AUTOMERGE_EXECUTOR_IDLE"
    packet_id = "qi-automerge-executor-" + _sha({"packet": packet, "records": records, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_automerge_executor_v2_4", "status": status, "packet_id": packet_id, "repository_full_name": repository, "pr_number": pr_number, "expected_head_sha": expected_head_sha, "gate_status": gate_status, "bridge_status": bridge_status, "merge_attempted": merge_attempted, "merge_applied": merge_applied, "records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiAutomergeExecutorResult("kuuos_runtime_daemon_qi_automerge_executor_v2_4", status, packet_id, str(root), str(packet_path), str(receipt_path), str(audit_path), repository, pr_number, expected_head_sha, gate_status, bridge_status, merge_attempted, merge_applied, blockers, warnings, records)
