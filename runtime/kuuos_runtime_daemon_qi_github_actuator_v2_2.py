#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_pr_merge_gate_v2_1 import build_qi_pr_merge_gate


@dataclass(frozen=True)
class QiGitHubActuatorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    plan_path: str
    receipt_path: str
    audit_path: str
    gate_packet_path: str
    branch_create_requested: bool
    file_patch_requested: bool
    pr_create_requested: bool
    merge_gate_status: str
    merge_requested: bool
    merge_allowed: bool
    expected_head_sha: str
    action_count: int
    records: list[dict[str, Any]]
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


def _actions(plan: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = plan.get("actions", [])
    return [dict(item) for item in raw if isinstance(item, Mapping)] if isinstance(raw, list) else []


def _gate_license() -> dict[str, Any]:
    return {
        "license_status": "QI_PR_MERGE_GATE_LICENSE_READY",
        "gate_packet_read_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _classify(actions: list[dict[str, Any]]) -> tuple[bool, bool, bool, bool]:
    kinds = {str(action.get("kind", "")) for action in actions}
    return "create_branch" in kinds, "file_patch" in kinds or "create_file" in kinds or "update_file" in kinds, "create_pr" in kinds, "merge_pr" in kinds


def build_qi_github_actuator(*, runtime_context: Mapping[str, Any], actuator_license_packet: Mapping[str, Any]) -> QiGitHubActuatorResult:
    ctx = _m(runtime_context)
    lic = _m(actuator_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "github_actuator_plan.json"
    receipt_path = root / "github_actuator_receipt.json"
    audit_path = root / "github_actuator_audit.jsonl"
    gate_packet_path = root / "pr_merge_gate_packet.json"
    if ctx.get("qi_github_actuator_enabled") is not True:
        blockers.append("qi_github_actuator_enabled_not_true")
    if ctx.get("apply_github_actuator") is not True:
        blockers.append("apply_github_actuator_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTUATOR_LICENSE_READY":
        blockers.append("github_actuator_license_not_ready")
    for name in ["plan_read_allowed", "receipt_write_allowed", "audit_append_allowed", "branch_create_allowed", "file_patch_allowed", "pr_create_allowed", "merge_gate_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    plan = _read_json(plan_path)
    actions = _actions(plan)
    if not actions and not blockers:
        warnings.append("github_actuator_plan_empty")
    branch_req, file_req, pr_req, merge_req = _classify(actions)
    expected_head_sha = str(plan.get("expected_head_sha", plan.get("head_sha", "")))
    repository = str(plan.get("repository_full_name", ""))
    pr_number = int(plan.get("pr_number", 0) or 0)
    if not repository:
        blockers.append("repository_missing")
    if merge_req and not expected_head_sha:
        blockers.append("expected_head_sha_missing_for_merge")
    if merge_req and pr_number <= 0:
        blockers.append("pr_number_missing_for_merge")
    if branch_req and lic.get("branch_create_allowed") is not True:
        blockers.append("branch_create_not_allowed")
    if file_req and lic.get("file_patch_allowed") is not True:
        blockers.append("file_patch_not_allowed")
    if pr_req and lic.get("pr_create_allowed") is not True:
        blockers.append("pr_create_not_allowed")
    if merge_req and lic.get("merge_gate_allowed") is not True:
        blockers.append("merge_gate_not_allowed")
    ready = not blockers
    merge_gate_status = "NOT_RUN"
    merge_allowed = False
    if ready:
        for index, action in enumerate(actions):
            kind = str(action.get("kind", ""))
            record = {"index": index, "kind": kind, "action_digest": _sha(action), "status": "planned", "epoch": int(time.time())}
            if kind in {"create_branch", "create_file", "update_file", "file_patch", "create_pr"}:
                record["status"] = "external_action_required"
            elif kind == "merge_pr":
                gate_packet = {
                    "repository_full_name": repository,
                    "pr_number": pr_number,
                    "expected_head_sha": expected_head_sha,
                    "actual_head_sha": str(plan.get("actual_head_sha", expected_head_sha)),
                    "explicit_automerge_license": plan.get("explicit_automerge_license") is True,
                    "allowed_repository": plan.get("allowed_repository") is True,
                    "allowed_base_branch": plan.get("allowed_base_branch") is True,
                    "pull_request_created": plan.get("pull_request_created") is True,
                    "pull_request_not_draft": plan.get("pull_request_not_draft") is True,
                    "mergeable": plan.get("mergeable") is True,
                    "no_unresolved_blockers": plan.get("no_unresolved_blockers") is True,
                    "receipt_written": plan.get("receipt_written") is True,
                    "audit_written": plan.get("audit_written") is True,
                    "merge_allowed": plan.get("merge_allowed") is True,
                    "merge_method": str(plan.get("merge_method", "merge")),
                    "required_checks": plan.get("required_checks", []),
                }
                _write_json(gate_packet_path, gate_packet)
                gate_result = build_qi_pr_merge_gate(runtime_context={"qi_pr_merge_gate_enabled": True, "apply_pr_merge_gate": True, "runtime_root": str(root)}, gate_license_packet=_gate_license())
                gate_payload = gate_result.to_dict()
                merge_gate_status = str(gate_payload.get("status"))
                merge_allowed = bool(gate_payload.get("merge_allowed"))
                record.update({"status": "gate_evaluated", "gate_status": merge_gate_status, "merge_allowed": merge_allowed})
            else:
                record["status"] = "unknown_action"
                blockers.append(f"unknown_action_{kind}")
            record["record_digest"] = _sha(record)
            _append_jsonl(audit_path, record)
            records.append(record)
    else:
        warnings.append("github_actuator_blocked_before_plan")
    if blockers:
        status = "QI_GITHUB_ACTUATOR_BLOCKED"
    elif merge_req and merge_gate_status != "QI_PR_MERGE_GATE_PASSED":
        status = "QI_GITHUB_ACTUATOR_MERGE_BLOCKED"
    else:
        status = "QI_GITHUB_ACTUATOR_READY"
    packet_id = "qi-github-actuator-" + _sha({"plan": plan, "records": records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actuator_v2_2",
        "status": status,
        "packet_id": packet_id,
        "repository_full_name": repository,
        "pr_number": pr_number,
        "expected_head_sha": expected_head_sha,
        "branch_create_requested": branch_req,
        "file_patch_requested": file_req,
        "pr_create_requested": pr_req,
        "merge_requested": merge_req,
        "merge_gate_status": merge_gate_status,
        "merge_allowed": merge_allowed,
        "records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    return QiGitHubActuatorResult(
        "kuuos_runtime_daemon_qi_github_actuator_v2_2",
        status,
        packet_id,
        str(root),
        str(plan_path),
        str(receipt_path),
        str(audit_path),
        str(gate_packet_path),
        branch_req,
        file_req,
        pr_req,
        merge_gate_status,
        merge_req,
        merge_allowed,
        expected_head_sha,
        len(actions),
        records,
        blockers,
        warnings,
    )
