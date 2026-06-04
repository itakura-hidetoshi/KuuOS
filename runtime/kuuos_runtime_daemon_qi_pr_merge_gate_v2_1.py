#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


@dataclass(frozen=True)
class QiPRMergeGateResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    gate_packet_path: str
    receipt_path: str
    audit_path: str
    repository_full_name: str
    pr_number: int
    expected_head_sha: str
    gate_passed: bool
    merge_allowed: bool
    merge_method: str
    reasons: list[str]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


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


def _all_checks_success(checks: Any) -> bool:
    if not isinstance(checks, list):
        return False
    if not checks:
        return False
    for item in checks:
        if not isinstance(item, Mapping):
            return False
        status = str(item.get("status", item.get("conclusion", ""))).lower()
        if status not in {"success", "successful", "passed"}:
            return False
    return True


def build_qi_pr_merge_gate(*, runtime_context: Mapping[str, Any], gate_license_packet: Mapping[str, Any]) -> QiPRMergeGateResult:
    ctx = _m(runtime_context)
    lic = _m(gate_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    reasons: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    gate_packet_path = root / "pr_merge_gate_packet.json"
    receipt_path = root / "pr_merge_receipt.json"
    audit_path = root / "pr_merge_gate_audit.jsonl"
    packet = _read_json(gate_packet_path)
    if ctx.get("qi_pr_merge_gate_enabled") is not True:
        blockers.append("qi_pr_merge_gate_enabled_not_true")
    if ctx.get("apply_pr_merge_gate") is not True:
        blockers.append("apply_pr_merge_gate_not_true")
    if lic.get("license_status") != "QI_PR_MERGE_GATE_LICENSE_READY":
        blockers.append("merge_gate_license_not_ready")
    for name in ["gate_packet_read_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    repository = str(packet.get("repository_full_name", ""))
    pr_number = _i(packet.get("pr_number"), 0)
    expected_head_sha = str(packet.get("expected_head_sha", ""))
    actual_head_sha = str(packet.get("actual_head_sha", expected_head_sha))
    merge_method = str(packet.get("merge_method", "merge"))
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
    if packet.get("allowed_repository") is not True:
        blockers.append("repository_not_allowed")
    if packet.get("allowed_base_branch") is not True:
        blockers.append("base_branch_not_allowed")
    if packet.get("pull_request_created") is not True:
        blockers.append("pull_request_not_created")
    if packet.get("pull_request_not_draft") is not True:
        blockers.append("pull_request_is_draft")
    if packet.get("mergeable") is not True:
        blockers.append("pull_request_not_mergeable")
    if packet.get("no_unresolved_blockers") is not True:
        blockers.append("unresolved_blockers_present")
    if packet.get("receipt_written") is not True:
        blockers.append("pre_merge_receipt_missing")
    if packet.get("audit_written") is not True:
        blockers.append("pre_merge_audit_missing")
    if merge_method not in {"merge", "squash", "rebase"}:
        blockers.append("merge_method_invalid")
    checks_ok = _all_checks_success(packet.get("required_checks", []))
    if not checks_ok:
        blockers.append("required_checks_not_success")
    if not blockers:
        reasons.append("all_merge_gates_passed")
    else:
        reasons.extend(blockers)
    gate_passed = not blockers
    merge_allowed = gate_passed and packet.get("merge_allowed") is True
    if gate_passed and not merge_allowed:
        warnings.append("gate_passed_but_merge_allowed_not_true")
    status = "QI_PR_MERGE_GATE_PASSED" if gate_passed else "QI_PR_MERGE_GATE_BLOCKED"
    packet_id = "qi-pr-merge-gate-" + _sha({"packet": packet, "status": status, "reasons": reasons})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_pr_merge_gate_v2_1",
        "status": status,
        "packet_id": packet_id,
        "repository_full_name": repository,
        "pr_number": pr_number,
        "expected_head_sha": expected_head_sha,
        "actual_head_sha": actual_head_sha,
        "gate_passed": gate_passed,
        "merge_allowed": merge_allowed,
        "merge_method": merge_method,
        "reasons": reasons,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiPRMergeGateResult(
        "kuuos_runtime_daemon_qi_pr_merge_gate_v2_1",
        status,
        packet_id,
        str(root),
        str(gate_packet_path),
        str(receipt_path),
        str(audit_path),
        repository,
        pr_number,
        expected_head_sha,
        gate_passed,
        merge_allowed,
        merge_method,
        reasons,
        blockers,
        warnings,
    )
