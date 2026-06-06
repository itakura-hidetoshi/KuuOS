#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


RESULT_FILE_BY_ACTION = {
    "merge_pull_request": "qi_github_actions_policy_action_merge_result_packet.json",
    "rerun_failed_workflow_run_jobs": "qi_github_actions_policy_action_rerun_result_packet.json",
    "reobserve_commit_workflow_runs": "qi_github_actions_policy_action_reobserve_result_packet.json",
}

CONNECTOR_ACTION_BY_KIND = {
    "merge_pull_request": "GitHub.merge_pull_request",
    "rerun_failed_workflow_run_jobs": "GitHub.rerun_failed_workflow_run_jobs",
    "reobserve_commit_workflow_runs": "GitHub.fetch_commit_workflow_runs",
}

FINAL_STATE_BY_KIND = {
    "merge_pull_request": "action_completed",
    "rerun_failed_workflow_run_jobs": "action_rerun_requested",
    "reobserve_commit_workflow_runs": "action_reobserve_ready",
}

NEXT_EXPECTED_BY_KIND = {
    "merge_pull_request": "close_autopilot_cycle",
    "rerun_failed_workflow_run_jobs": "wait_for_new_workflow_runs_then_reobserve",
    "reobserve_commit_workflow_runs": "feed_reobserved_workflow_runs_into_pr_live_loop",
}


@dataclass(frozen=True)
class QiGitHubActionsPolicyActionFinalReceiptResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    action_kind: str
    final_state: str
    next_expected: str
    final_receipt_path: str
    receipt_path: str
    audit_path: str
    final_receipt_written: bool
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


def _infer_kind(root: pathlib.Path, ctx: Mapping[str, Any]) -> str:
    explicit = str(ctx.get("action_kind", ""))
    if explicit in RESULT_FILE_BY_ACTION:
        return explicit
    for kind, file_name in RESULT_FILE_BY_ACTION.items():
        if _read_json(root / file_name):
            return kind
    return "unknown"


def _payload(packet: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = packet.get("connector_result")
    return nested if isinstance(nested, Mapping) else packet


def _validate_packet(kind: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    if packet.get("action_result_allowed") is not True:
        blockers.append("action_result_allowed_not_true")
    if str(packet.get("action_kind", "")) != kind:
        blockers.append("action_kind_mismatch")
    if str(packet.get("connector_action", "")) != CONNECTOR_ACTION_BY_KIND.get(kind, "unknown"):
        blockers.append("connector_action_mismatch")
    payload = _payload(packet)
    if kind == "merge_pull_request":
        if payload.get("merged") is not True:
            blockers.append("merge_result_not_merged_true")
        if not str(payload.get("sha", "")).strip():
            blockers.append("merge_result_sha_missing")
    elif kind == "rerun_failed_workflow_run_jobs":
        ok = payload.get("success") is True or str(payload.get("status", "")).lower() in {"queued", "requested", "accepted", "success"}
        if not ok:
            blockers.append("rerun_result_not_success_like")
    elif kind == "reobserve_commit_workflow_runs":
        runs = payload.get("workflow_runs")
        if not isinstance(runs, list) or not runs:
            blockers.append("workflow_runs_empty_or_invalid")


def _final_receipt(kind: str, result_packet: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_policy_action_final_receipt_packet_v8_9",
        "final_receipt_allowed": True,
        "action_kind": kind,
        "final_state": FINAL_STATE_BY_KIND[kind],
        "next_expected": NEXT_EXPECTED_BY_KIND[kind],
        "connector_action": CONNECTOR_ACTION_BY_KIND[kind],
        "connector_result": dict(_payload(result_packet)),
        "source_action_result_digest": _sha(dict(result_packet)),
        "boundary": {
            "receipt_only": True,
            "does_not_apply_additional_action": True,
            "closes_or_routes_policy_action": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_policy_action_final_receipt(*, runtime_context: Mapping[str, Any], policy_action_final_receipt_license: Mapping[str, Any]) -> QiGitHubActionsPolicyActionFinalReceiptResult:
    ctx = _m(runtime_context)
    lic = _m(policy_action_final_receipt_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    final_receipt_path = root / "qi_github_actions_policy_action_final_receipt_packet.json"
    receipt_path = root / "qi_github_actions_policy_action_final_receipt_receipt.json"
    audit_path = root / "qi_github_actions_policy_action_final_receipt_audit.jsonl"

    if ctx.get("qi_github_actions_policy_action_final_receipt_enabled") is not True:
        blockers.append("qi_github_actions_policy_action_final_receipt_enabled_not_true")
    if ctx.get("apply_github_actions_policy_action_final_receipt") is not True:
        blockers.append("apply_github_actions_policy_action_final_receipt_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_RECEIPT_LICENSE_READY":
        blockers.append("github_actions_policy_action_final_receipt_license_not_ready")
    for name in ["action_result_packet_read_allowed", "final_receipt_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    kind = _infer_kind(root, ctx)
    if kind not in RESULT_FILE_BY_ACTION:
        blockers.append("action_kind_not_allowlisted")
    if kind in RESULT_FILE_BY_ACTION and lic.get(f"allow_{kind}_final_receipt") is not True:
        blockers.append(f"{kind}_not_allowed_by_policy_action_final_receipt_license")

    result_path = root / RESULT_FILE_BY_ACTION.get(kind, "missing")
    result_packet = _read_json(result_path) if kind in RESULT_FILE_BY_ACTION else {}
    if not result_packet:
        blockers.append("action_result_packet_missing_or_invalid")
    if kind in RESULT_FILE_BY_ACTION and result_packet:
        _validate_packet(kind, result_packet, blockers)

    packet: dict[str, Any] = {}
    written = False
    final_state = FINAL_STATE_BY_KIND.get(kind, "unknown")
    next_expected = NEXT_EXPECTED_BY_KIND.get(kind, "unknown")
    if not blockers:
        packet = _final_receipt(kind, result_packet)
        _write_json(final_receipt_path, packet)
        written = True

    status = "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_RECEIPT_READY" if not blockers else "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_RECEIPT_BLOCKED"
    packet_id = "qi-github-actions-policy-action-final-receipt-" + _sha({"kind": kind, "result": result_packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_policy_action_final_receipt_v8_9",
        "status": status,
        "packet_id": packet_id,
        "action_kind": kind,
        "final_state": final_state,
        "next_expected": next_expected,
        "final_receipt_written": written,
        "final_receipt_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPolicyActionFinalReceiptResult(
        "kuuos_runtime_daemon_qi_github_actions_policy_action_final_receipt_v8_9",
        status,
        packet_id,
        str(root),
        kind,
        final_state,
        next_expected,
        str(final_receipt_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
