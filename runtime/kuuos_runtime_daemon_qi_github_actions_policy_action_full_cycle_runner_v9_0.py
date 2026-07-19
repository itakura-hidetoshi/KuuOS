#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_autopilot_policy_action_handoff_v8_6 import build_qi_github_actions_autopilot_policy_action_handoff
from runtime.kuuos_runtime_daemon_qi_github_actions_policy_action_external_call_bridge_v8_7 import build_qi_github_actions_policy_action_external_call_bridge
from runtime.kuuos_runtime_daemon_qi_github_actions_policy_action_external_result_bridge_v8_8 import build_qi_github_actions_policy_action_external_result_bridge
from runtime.kuuos_runtime_daemon_qi_github_actions_policy_action_final_receipt_v8_9 import build_qi_github_actions_policy_action_final_receipt


ACTION_RESULT_FILES = [
    "qi_github_actions_policy_action_merge_result_packet.json",
    "qi_github_actions_policy_action_rerun_result_packet.json",
    "qi_github_actions_policy_action_reobserve_result_packet.json",
]


@dataclass(frozen=True)
class QiGitHubActionsPolicyActionFullCycleRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    phases_run: int
    final_stage: str
    stop_reason: str
    action_kind: str
    connector_action: str
    final_state: str
    next_expected: str
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
        "action_kind": str(result.get("action_kind", "unknown")),
        "connector_action": str(result.get("connector_action", "unknown")),
        "final_state": str(result.get("final_state", "unknown")),
        "next_expected": str(result.get("next_expected", "unknown")),
        "digest": _sha(dict(result)),
        "blockers": list(result.get("blockers", [])) if isinstance(result.get("blockers", []), list) else [],
        "epoch": int(time.time()),
    }


def _handoff_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_autopilot_policy_action_handoff_enabled": True,
        "apply_github_actions_autopilot_policy_action_handoff": True,
        "runtime_root": str(root),
    }


def _handoff_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_AUTOPILOT_POLICY_ACTION_HANDOFF_LICENSE_READY",
        "handoff_packet_read_allowed": True,
        "context_packet_read_allowed": True,
        "action_handoff_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _external_call_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_policy_action_external_call_bridge_enabled": True,
        "apply_github_actions_policy_action_external_call_bridge": True,
        "runtime_root": str(root),
    }


def _external_call_license() -> dict[str, Any]:
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


def _external_result_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_policy_action_external_result_bridge_enabled": True,
        "apply_github_actions_policy_action_external_result_bridge": True,
        "runtime_root": str(root),
    }


def _external_result_license() -> dict[str, Any]:
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
    return {
        "qi_github_actions_policy_action_final_receipt_enabled": True,
        "apply_github_actions_policy_action_final_receipt": True,
        "runtime_root": str(root),
    }


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
    return any(_exists(root, name) for name in ACTION_RESULT_FILES)


def _has_external_raw_result(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_policy_action_external_call_raw_result_packet.json")


def _has_external_call(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_policy_action_external_call_packet.json")


def _has_action_handoff(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_autopilot_policy_action_handoff_packet.json")


def _has_policy_ready_handoff(root: pathlib.Path) -> bool:
    handoff = _read_json(root / "qi_github_actions_pr_live_autopilot_handoff_packet.json")
    return bool(handoff) and handoff.get("autopilot_state") == "policy_ready"


def build_qi_github_actions_policy_action_full_cycle_runner(*, runtime_context: Mapping[str, Any], policy_action_full_cycle_runner_license: Mapping[str, Any]) -> QiGitHubActionsPolicyActionFullCycleRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(policy_action_full_cycle_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_policy_action_full_cycle_runner_receipt.json"
    audit_path = root / "qi_github_actions_policy_action_full_cycle_runner_audit.jsonl"

    if ctx.get("qi_github_actions_policy_action_full_cycle_runner_enabled") is not True:
        blockers.append("qi_github_actions_policy_action_full_cycle_runner_enabled_not_true")
    if ctx.get("apply_github_actions_policy_action_full_cycle_runner") is not True:
        blockers.append("apply_github_actions_policy_action_full_cycle_runner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_POLICY_ACTION_FULL_CYCLE_RUNNER_LICENSE_READY":
        blockers.append("github_actions_policy_action_full_cycle_runner_license_not_ready")
    for name in ["policy_handoff_run_allowed", "external_call_bridge_run_allowed", "external_result_bridge_run_allowed", "final_receipt_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    max_phases = _i(ctx.get("max_policy_action_full_cycle_phases", 6), 6)
    if max_phases < 1:
        blockers.append("max_policy_action_full_cycle_phases_invalid")
        max_phases = 0
    if max_phases > 20:
        warnings.append("max_policy_action_full_cycle_phases_capped_to_20")
        max_phases = 20

    records: list[dict[str, Any]] = []
    final_stage = "not_run"
    stop_reason = "not_run"
    action_kind = "unknown"
    connector_action = "unknown"
    final_state = "unknown"
    next_expected = "unknown"

    if not blockers:
        stop_reason = "max_phases_reached"
        for index in range(1, max_phases + 1):
            if _has_action_result(root):
                final_stage = "synthesize_final_receipt"
                result = build_qi_github_actions_policy_action_final_receipt(
                    runtime_context=_final_receipt_context(root),
                    policy_action_final_receipt_license=_final_receipt_license(),
                ).to_dict()
                records.append(_record(index, final_stage, result))
                action_kind = str(result.get("action_kind", action_kind))
                final_state = str(result.get("final_state", final_state))
                next_expected = str(result.get("next_expected", next_expected))
                if result.get("status") != "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_RECEIPT_READY":
                    blockers.append("policy_action_final_receipt_not_ready")
                    stop_reason = "final_receipt_blocked"
                    break
                stop_reason = "final_receipt_ready"
                break

            if _has_external_raw_result(root):
                final_stage = "bridge_external_action_result"
                result = build_qi_github_actions_policy_action_external_result_bridge(
                    runtime_context=_external_result_context(root),
                    policy_action_external_result_bridge_license=_external_result_license(),
                ).to_dict()
                records.append(_record(index, final_stage, result))
                action_kind = str(result.get("action_kind", action_kind))
                connector_action = str(result.get("connector_action", connector_action))
                if result.get("status") != "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_RESULT_BRIDGE_READY":
                    blockers.append("policy_action_external_result_bridge_not_ready")
                    stop_reason = "external_result_bridge_blocked"
                    break
                continue

            if _has_external_call(root):
                final_stage = "await_policy_action_external_result"
                call = _read_json(root / "qi_github_actions_policy_action_external_call_packet.json")
                action_kind = str(call.get("action_kind", action_kind))
                connector_action = str(call.get("connector_action", connector_action))
                stop_reason = "await_policy_action_external_result"
                break

            if _has_action_handoff(root):
                final_stage = "bridge_policy_action_external_call"
                result = build_qi_github_actions_policy_action_external_call_bridge(
                    runtime_context=_external_call_context(root),
                    policy_action_external_call_bridge_license=_external_call_license(),
                ).to_dict()
                records.append(_record(index, final_stage, result))
                action_kind = str(result.get("action_kind", action_kind))
                connector_action = str(result.get("connector_action", connector_action))
                if result.get("status") != "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_CALL_BRIDGE_READY":
                    blockers.append("policy_action_external_call_bridge_not_ready")
                    stop_reason = "external_call_bridge_blocked"
                    break
                stop_reason = "await_policy_action_external_result"
                break

            if _has_policy_ready_handoff(root):
                final_stage = "build_policy_action_handoff"
                result = build_qi_github_actions_autopilot_policy_action_handoff(
                    runtime_context=_handoff_context(root),
                    policy_action_handoff_license=_handoff_license(),
                ).to_dict()
                records.append(_record(index, final_stage, result))
                action_kind = str(result.get("action_kind", action_kind))
                connector_action = str(result.get("connector_action", connector_action))
                if result.get("status") != "QI_GITHUB_ACTIONS_AUTOPILOT_POLICY_ACTION_HANDOFF_READY":
                    blockers.append("autopilot_policy_action_handoff_not_ready")
                    stop_reason = "policy_action_handoff_blocked"
                    break
                continue

            stop_reason = "policy_action_input_missing"
            blockers.append("policy_action_input_missing")
            break

    status = "QI_GITHUB_ACTIONS_POLICY_ACTION_FULL_CYCLE_RUNNER_READY" if not blockers else "QI_GITHUB_ACTIONS_POLICY_ACTION_FULL_CYCLE_RUNNER_BLOCKED"
    packet_id = "qi-github-actions-policy-action-full-cycle-" + _sha({"records": records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_policy_action_full_cycle_runner_v9_0",
        "status": status,
        "packet_id": packet_id,
        "phases_run": len(records),
        "final_stage": final_stage,
        "stop_reason": stop_reason,
        "action_kind": action_kind,
        "connector_action": connector_action,
        "final_state": final_state,
        "next_expected": next_expected,
        "phase_records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPolicyActionFullCycleRunnerResult(
        "kuuos_runtime_daemon_qi_github_actions_policy_action_full_cycle_runner_v9_0",
        status,
        packet_id,
        str(root),
        len(records),
        final_stage,
        stop_reason,
        action_kind,
        connector_action,
        final_state,
        next_expected,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
        records,
    )
