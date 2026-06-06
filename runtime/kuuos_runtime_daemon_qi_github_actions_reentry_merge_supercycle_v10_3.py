#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_policy_reentry_evaluator_v10_1 import build_qi_github_actions_policy_reentry_evaluator
from runtime.kuuos_runtime_daemon_qi_github_actions_pr_info_result_bridge_v10_2 import build_qi_github_actions_pr_info_result_bridge
from runtime.kuuos_runtime_daemon_qi_github_actions_autopilot_policy_action_handoff_v8_6 import build_qi_github_actions_autopilot_policy_action_handoff
from runtime.kuuos_runtime_daemon_qi_github_actions_policy_action_external_call_bridge_v8_7 import build_qi_github_actions_policy_action_external_call_bridge
from runtime.kuuos_runtime_daemon_qi_github_actions_policy_action_external_result_bridge_v8_8 import build_qi_github_actions_policy_action_external_result_bridge
from runtime.kuuos_runtime_daemon_qi_github_actions_policy_action_final_receipt_v8_9 import build_qi_github_actions_policy_action_final_receipt


@dataclass(frozen=True)
class QiGitHubActionsReentryMergeSupercycleResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    phases_run: int
    final_stage: str
    supercycle_state: str
    connector_action: str
    action_prepared: str
    stop_reason: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]
    phase_records: list[dict[str, Any]]

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


def _exists(root: pathlib.Path, name: str) -> bool:
    path = root / name
    return path.is_file() and path.stat().st_size > 2


def _record(index: int, stage: str, result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "index": index,
        "stage": stage,
        "status": str(result.get("status", "unknown")),
        "state": str(result.get("evaluation_state", result.get("bridge_state", result.get("final_state", result.get("action_kind", "unknown"))))),
        "connector_action": str(result.get("connector_action", "none")),
        "action_prepared": str(result.get("action_prepared", "none")),
        "stop_reason": str(result.get("stop_reason", "unknown")),
        "digest": _sha(dict(result)),
        "blockers": list(result.get("blockers", [])) if isinstance(result.get("blockers", []), list) else [],
        "epoch": int(time.time()),
    }


def _reentry_eval_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_reentry_evaluator_enabled": True, "apply_github_actions_policy_reentry_evaluator": True, "runtime_root": str(root)}


def _reentry_eval_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_POLICY_REENTRY_EVALUATOR_LICENSE_READY",
        "policy_reentry_packet_read_allowed": True,
        "evaluation_packet_write_allowed": True,
        "handoff_packet_write_allowed": True,
        "external_call_packet_write_allowed": True,
        "live_query_packet_write_allowed": True,
        "status_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _pr_info_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_pr_info_result_bridge_enabled": True, "apply_github_actions_pr_info_result_bridge": True, "runtime_root": str(root)}


def _pr_info_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_INFO_RESULT_BRIDGE_LICENSE_READY",
        "external_call_packet_read_allowed": True,
        "raw_result_packet_read_allowed": True,
        "raw_pr_info_packet_write_allowed": True,
        "handoff_packet_write_allowed": True,
        "evaluation_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _policy_handoff_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_autopilot_policy_action_handoff_enabled": True, "apply_github_actions_autopilot_policy_action_handoff": True, "runtime_root": str(root)}


def _policy_handoff_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_AUTOPILOT_POLICY_ACTION_HANDOFF_LICENSE_READY",
        "handoff_packet_read_allowed": True,
        "context_packet_read_allowed": True,
        "action_handoff_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _action_call_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_action_external_call_bridge_enabled": True, "apply_github_actions_policy_action_external_call_bridge": True, "runtime_root": str(root)}


def _action_call_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_CALL_BRIDGE_LICENSE_READY",
        "action_handoff_packet_read_allowed": True,
        "external_call_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "allow_merge_pull_request_external_call": True,
        "allow_rerun_failed_workflow_run_jobs_external_call": True,
        "allow_reobserve_commit_workflow_runs_external_call": True,
    }


def _action_result_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_action_external_result_bridge_enabled": True, "apply_github_actions_policy_action_external_result_bridge": True, "runtime_root": str(root)}


def _action_result_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_RESULT_BRIDGE_LICENSE_READY",
        "external_call_packet_read_allowed": True,
        "raw_result_packet_read_allowed": True,
        "action_result_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "allow_merge_pull_request_result_bridge": True,
        "allow_rerun_failed_workflow_run_jobs_result_bridge": True,
        "allow_reobserve_commit_workflow_runs_result_bridge": True,
    }


def _final_receipt_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_action_final_receipt_enabled": True, "apply_github_actions_policy_action_final_receipt": True, "runtime_root": str(root)}


def _final_receipt_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_RECEIPT_LICENSE_READY",
        "action_result_packet_read_allowed": True,
        "final_receipt_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "allow_merge_pull_request_final_receipt": True,
        "allow_rerun_failed_workflow_run_jobs_final_receipt": True,
        "allow_reobserve_commit_workflow_runs_final_receipt": True,
    }


def _has_action_result(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_policy_action_merge_result_packet.json") or _exists(root, "qi_github_actions_policy_action_rerun_result_packet.json") or _exists(root, "qi_github_actions_policy_action_reobserve_result_packet.json")


def build_qi_github_actions_reentry_merge_supercycle(*, runtime_context: Mapping[str, Any], reentry_merge_supercycle_license: Mapping[str, Any]) -> QiGitHubActionsReentryMergeSupercycleResult:
    ctx = _m(runtime_context)
    lic = _m(reentry_merge_supercycle_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_reentry_merge_supercycle_receipt.json"
    audit_path = root / "qi_github_actions_reentry_merge_supercycle_audit.jsonl"

    if ctx.get("qi_github_actions_reentry_merge_supercycle_enabled") is not True:
        blockers.append("qi_github_actions_reentry_merge_supercycle_enabled_not_true")
    if ctx.get("apply_github_actions_reentry_merge_supercycle") is not True:
        blockers.append("apply_github_actions_reentry_merge_supercycle_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_REENTRY_MERGE_SUPERCYCLE_LICENSE_READY":
        blockers.append("github_actions_reentry_merge_supercycle_license_not_ready")
    for name in ["reentry_evaluator_run_allowed", "pr_info_result_bridge_run_allowed", "policy_action_handoff_run_allowed", "policy_action_external_call_run_allowed", "policy_action_external_result_run_allowed", "policy_action_final_receipt_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    max_phases = _i(ctx.get("max_reentry_merge_supercycle_phases", 10), 10)
    if max_phases < 1:
        blockers.append("max_reentry_merge_supercycle_phases_invalid")
        max_phases = 0
    if max_phases > 40:
        warnings.append("max_reentry_merge_supercycle_phases_capped_to_40")
        max_phases = 40

    records: list[dict[str, Any]] = []
    final_stage = "not_run"
    supercycle_state = "not_run"
    connector_action = "none"
    action_prepared = "none"
    stop_reason = "not_run"

    if not blockers:
        stop_reason = "max_phases_reached"
        for index in range(1, max_phases + 1):
            if _exists(root, "qi_github_actions_policy_action_final_receipt_packet.json"):
                packet = _read_json(root / "qi_github_actions_policy_action_final_receipt_packet.json")
                final_stage = "final_receipt_present"
                supercycle_state = str(packet.get("final_state", "action_completed"))
                connector_action = str(packet.get("connector_action", "none"))
                action_prepared = str(packet.get("action_kind", "none"))
                stop_reason = str(packet.get("next_expected", "final_receipt_ready"))
                break
            if _has_action_result(root):
                final_stage = "run_policy_action_final_receipt"
                result = build_qi_github_actions_policy_action_final_receipt(runtime_context=_final_receipt_context(root), policy_action_final_receipt_license=_final_receipt_license()).to_dict()
            elif _exists(root, "qi_github_actions_policy_action_external_call_raw_result_packet.json"):
                final_stage = "run_policy_action_external_result_bridge"
                result = build_qi_github_actions_policy_action_external_result_bridge(runtime_context=_action_result_context(root), policy_action_external_result_bridge_license=_action_result_license()).to_dict()
            elif _exists(root, "qi_github_actions_policy_action_external_call_packet.json"):
                packet = _read_json(root / "qi_github_actions_policy_action_external_call_packet.json")
                final_stage = "await_policy_action_external_result"
                supercycle_state = "await_policy_action_external_result"
                connector_action = str(packet.get("connector_action", "unknown"))
                action_prepared = str(packet.get("action_kind", "unknown"))
                stop_reason = "await_policy_action_external_result"
                break
            elif _exists(root, "qi_github_actions_autopilot_policy_action_handoff_packet.json"):
                final_stage = "run_policy_action_external_call_bridge"
                result = build_qi_github_actions_policy_action_external_call_bridge(runtime_context=_action_call_context(root), policy_action_external_call_bridge_license=_action_call_license()).to_dict()
            elif _exists(root, "qi_github_actions_pr_live_autopilot_handoff_packet.json"):
                final_stage = "run_policy_action_handoff"
                result = build_qi_github_actions_autopilot_policy_action_handoff(runtime_context=_policy_handoff_context(root), policy_action_handoff_license=_policy_handoff_license()).to_dict()
            elif _exists(root, "qi_github_actions_policy_reentry_pr_info_raw_result_packet.json"):
                final_stage = "run_pr_info_result_bridge"
                result = build_qi_github_actions_pr_info_result_bridge(runtime_context=_pr_info_context(root), pr_info_result_bridge_license=_pr_info_license()).to_dict()
            elif _exists(root, "qi_github_actions_policy_reentry_external_call_packet.json"):
                packet = _read_json(root / "qi_github_actions_policy_reentry_external_call_packet.json")
                final_stage = "await_pr_info_external_result"
                supercycle_state = "await_pr_info_external_result"
                connector_action = str(packet.get("connector_action", "GitHub.get_pr_info"))
                action_prepared = "merge_pull_request"
                stop_reason = "await_pr_info_external_result"
                break
            elif _exists(root, "qi_github_actions_policy_reentry_packet.json"):
                final_stage = "run_policy_reentry_evaluator"
                result = build_qi_github_actions_policy_reentry_evaluator(runtime_context=_reentry_eval_context(root), policy_reentry_evaluator_license=_reentry_eval_license()).to_dict()
            else:
                blockers.append("policy_reentry_or_followup_packet_missing")
                stop_reason = "missing_entry_packet"
                break

            records.append(_record(index, final_stage, result))
            if not str(result.get("status", "")).endswith("READY"):
                blockers.append(f"{final_stage}_not_ready")
                stop_reason = f"{final_stage}_blocked"
                break
            supercycle_state = str(result.get("evaluation_state", result.get("bridge_state", result.get("final_state", result.get("action_kind", "unknown")))))
            connector_action = str(result.get("connector_action", "none"))
            action_prepared = str(result.get("action_prepared", action_prepared))
            stop_reason = supercycle_state
            continue

    status = "QI_GITHUB_ACTIONS_REENTRY_MERGE_SUPERCYCLE_READY" if not blockers else "QI_GITHUB_ACTIONS_REENTRY_MERGE_SUPERCYCLE_BLOCKED"
    packet_id = "qi-github-actions-reentry-merge-supercycle-" + _sha({"records": records, "blockers": blockers, "state": supercycle_state})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_reentry_merge_supercycle_v10_3",
        "status": status,
        "packet_id": packet_id,
        "phases_run": len(records),
        "final_stage": final_stage,
        "supercycle_state": supercycle_state,
        "connector_action": connector_action,
        "action_prepared": action_prepared,
        "stop_reason": stop_reason,
        "phase_records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsReentryMergeSupercycleResult(
        "kuuos_runtime_daemon_qi_github_actions_reentry_merge_supercycle_v10_3",
        status,
        packet_id,
        str(root),
        len(records),
        final_stage,
        supercycle_state,
        connector_action,
        action_prepared,
        stop_reason,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
        records,
    )
