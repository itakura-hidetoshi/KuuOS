#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_pr_live_autopilot_packet_runner_v8_4 import build_qi_github_actions_pr_live_autopilot_packet_runner
from runtime.kuuos_runtime_daemon_qi_github_actions_pr_live_autopilot_result_ingestor_v8_5 import build_qi_github_actions_pr_live_autopilot_result_ingestor
from runtime.kuuos_runtime_daemon_qi_github_actions_autopilot_policy_action_handoff_v8_6 import build_qi_github_actions_autopilot_policy_action_handoff
from runtime.kuuos_runtime_daemon_qi_github_actions_policy_action_external_call_bridge_v8_7 import build_qi_github_actions_policy_action_external_call_bridge
from runtime.kuuos_runtime_daemon_qi_github_actions_policy_action_external_result_bridge_v8_8 import build_qi_github_actions_policy_action_external_result_bridge
from runtime.kuuos_runtime_daemon_qi_github_actions_policy_action_final_receipt_v8_9 import build_qi_github_actions_policy_action_final_receipt


@dataclass(frozen=True)
class QiGitHubActionsPrLiveAutopilotE2EOrchestratorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    phases_run: int
    final_stage: str
    final_state: str
    stop_reason: str
    connector_action: str
    policy_decision: str
    action_prepared: str
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
        "state": str(result.get("autopilot_state", result.get("final_state", result.get("action_kind", "unknown")))),
        "stop_reason": str(result.get("stop_reason", "unknown")),
        "connector_action": str(result.get("connector_action", "none")),
        "policy_decision": str(result.get("policy_decision", "not_run")),
        "action_prepared": str(result.get("action_prepared", "none")),
        "digest": _sha(dict(result)),
        "blockers": list(result.get("blockers", [])) if isinstance(result.get("blockers", []), list) else [],
        "epoch": int(time.time()),
    }


def _autopilot_runner_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_pr_live_autopilot_packet_runner_enabled": True, "apply_github_actions_pr_live_autopilot_packet_runner": True, "runtime_root": str(root)}


def _autopilot_runner_license() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_PACKET_RUNNER_LICENSE_READY", "autopilot_query_read_allowed": True, "live_query_write_allowed": True, "external_cycle_run_allowed": True, "handoff_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _ingestor_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_pr_live_autopilot_result_ingestor_enabled": True, "apply_github_actions_pr_live_autopilot_result_ingestor": True, "runtime_root": str(root)}


def _ingestor_license() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_RESULT_INGESTOR_LICENSE_READY", "handoff_packet_read_allowed": True, "connector_result_read_allowed": True, "raw_result_packet_write_allowed": True, "autopilot_runner_run_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _action_handoff_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_autopilot_policy_action_handoff_enabled": True, "apply_github_actions_autopilot_policy_action_handoff": True, "runtime_root": str(root)}


def _action_handoff_license() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_AUTOPILOT_POLICY_ACTION_HANDOFF_LICENSE_READY", "handoff_packet_read_allowed": True, "context_packet_read_allowed": True, "action_handoff_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}


def _action_call_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_action_external_call_bridge_enabled": True, "apply_github_actions_policy_action_external_call_bridge": True, "runtime_root": str(root)}


def _action_call_license() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_CALL_BRIDGE_LICENSE_READY", "action_handoff_packet_read_allowed": True, "external_call_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True, "allow_merge_pull_request_external_call": True, "allow_rerun_failed_workflow_run_jobs_external_call": True, "allow_reobserve_commit_workflow_runs_external_call": True}


def _action_result_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_action_external_result_bridge_enabled": True, "apply_github_actions_policy_action_external_result_bridge": True, "runtime_root": str(root)}


def _action_result_license() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_POLICY_ACTION_EXTERNAL_RESULT_BRIDGE_LICENSE_READY", "external_call_packet_read_allowed": True, "raw_result_packet_read_allowed": True, "action_result_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True, "allow_merge_pull_request_result_bridge": True, "allow_rerun_failed_workflow_run_jobs_result_bridge": True, "allow_reobserve_commit_workflow_runs_result_bridge": True}


def _final_receipt_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_policy_action_final_receipt_enabled": True, "apply_github_actions_policy_action_final_receipt": True, "runtime_root": str(root)}


def _final_receipt_license() -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_POLICY_ACTION_FINAL_RECEIPT_LICENSE_READY", "action_result_packet_read_allowed": True, "final_receipt_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True, "allow_merge_pull_request_final_receipt": True, "allow_rerun_failed_workflow_run_jobs_final_receipt": True, "allow_reobserve_commit_workflow_runs_final_receipt": True}


def _has_action_result(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_policy_action_merge_result_packet.json") or _exists(root, "qi_github_actions_policy_action_rerun_result_packet.json") or _exists(root, "qi_github_actions_policy_action_reobserve_result_packet.json")


def _has_final_receipt(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_policy_action_final_receipt_packet.json")


def _has_action_raw_result(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_policy_action_external_call_raw_result_packet.json")


def _has_action_call(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_policy_action_external_call_packet.json")


def _has_action_handoff(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_autopilot_policy_action_handoff_packet.json")


def _has_autopilot_connector_result(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_pr_live_autopilot_connector_result_packet.json")


def _has_autopilot_handoff(root: pathlib.Path) -> bool:
    return _exists(root, "qi_github_actions_pr_live_autopilot_handoff_packet.json")


def _classify_handoff(root: pathlib.Path) -> str:
    handoff = _read_json(root / "qi_github_actions_pr_live_autopilot_handoff_packet.json")
    return str(handoff.get("autopilot_state", "unknown"))


def build_qi_github_actions_pr_live_autopilot_e2e_orchestrator(*, runtime_context: Mapping[str, Any], e2e_orchestrator_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveAutopilotE2EOrchestratorResult:
    ctx = _m(runtime_context)
    lic = _m(e2e_orchestrator_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_pr_live_autopilot_e2e_orchestrator_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_autopilot_e2e_orchestrator_audit.jsonl"

    if ctx.get("qi_github_actions_pr_live_autopilot_e2e_orchestrator_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_autopilot_e2e_orchestrator_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_autopilot_e2e_orchestrator") is not True:
        blockers.append("apply_github_actions_pr_live_autopilot_e2e_orchestrator_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_E2E_ORCHESTRATOR_LICENSE_READY":
        blockers.append("github_actions_pr_live_autopilot_e2e_orchestrator_license_not_ready")
    for name in ["autopilot_run_allowed", "autopilot_ingest_allowed", "policy_action_handoff_allowed", "policy_action_external_call_allowed", "policy_action_external_result_allowed", "policy_action_final_receipt_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    max_phases = _i(ctx.get("max_autopilot_e2e_phases", 8), 8)
    if max_phases < 1:
        blockers.append("max_autopilot_e2e_phases_invalid")
        max_phases = 0
    if max_phases > 40:
        warnings.append("max_autopilot_e2e_phases_capped_to_40")
        max_phases = 40

    records: list[dict[str, Any]] = []
    final_stage = "not_run"
    final_state = "not_run"
    stop_reason = "not_run"
    connector_action = "none"
    policy_decision = "not_run"
    action_prepared = "none"

    if not blockers:
        stop_reason = "max_phases_reached"
        for index in range(1, max_phases + 1):
            if _has_final_receipt(root):
                packet = _read_json(root / "qi_github_actions_policy_action_final_receipt_packet.json")
                final_stage = "final_receipt_present"
                final_state = str(packet.get("final_state", "unknown"))
                stop_reason = str(packet.get("next_expected", "closed"))
                connector_action = str(packet.get("connector_action", "none"))
                break
            if _has_action_result(root):
                final_stage = "synthesize_final_receipt"
                result = build_qi_github_actions_policy_action_final_receipt(runtime_context=_final_receipt_context(root), policy_action_final_receipt_license=_final_receipt_license()).to_dict()
            elif _has_action_raw_result(root):
                final_stage = "bridge_action_external_result"
                result = build_qi_github_actions_policy_action_external_result_bridge(runtime_context=_action_result_context(root), policy_action_external_result_bridge_license=_action_result_license()).to_dict()
            elif _has_action_call(root):
                final_stage = "await_policy_action_external_result"
                packet = _read_json(root / "qi_github_actions_policy_action_external_call_packet.json")
                final_state = "await_policy_action_external_result"
                stop_reason = "await_policy_action_external_result"
                connector_action = str(packet.get("connector_action", "unknown"))
                break
            elif _has_action_handoff(root):
                final_stage = "bridge_policy_action_external_call"
                result = build_qi_github_actions_policy_action_external_call_bridge(runtime_context=_action_call_context(root), policy_action_external_call_bridge_license=_action_call_license()).to_dict()
            elif _has_autopilot_connector_result(root):
                final_stage = "ingest_autopilot_connector_result"
                result = build_qi_github_actions_pr_live_autopilot_result_ingestor(runtime_context=_ingestor_context(root), autopilot_result_ingestor_license=_ingestor_license()).to_dict()
            elif _has_autopilot_handoff(root) and _classify_handoff(root) == "policy_ready":
                final_stage = "build_policy_action_handoff"
                result = build_qi_github_actions_autopilot_policy_action_handoff(runtime_context=_action_handoff_context(root), policy_action_handoff_license=_action_handoff_license()).to_dict()
            elif _has_autopilot_handoff(root) and _classify_handoff(root) == "await_external_connector":
                packet = _read_json(root / "qi_github_actions_pr_live_autopilot_handoff_packet.json")
                final_stage = "await_autopilot_external_connector"
                final_state = "await_autopilot_external_connector"
                stop_reason = "await_autopilot_external_connector"
                connector_action = str(packet.get("connector_action", "unknown"))
                break
            else:
                final_stage = "run_autopilot_packet_runner"
                result = build_qi_github_actions_pr_live_autopilot_packet_runner(runtime_context=_autopilot_runner_context(root), autopilot_packet_runner_license=_autopilot_runner_license()).to_dict()

            records.append(_record(index, final_stage, result))
            if not str(result.get("status", "")).endswith("READY"):
                blockers.append(f"{final_stage}_not_ready")
                stop_reason = f"{final_stage}_blocked"
                break
            final_state = str(result.get("autopilot_state", result.get("final_state", result.get("action_kind", "unknown"))))
            stop_reason = str(result.get("stop_reason", result.get("next_expected", "unknown")))
            connector_action = str(result.get("connector_action", "none"))
            policy_decision = str(result.get("policy_decision", policy_decision))
            action_prepared = str(result.get("action_prepared", action_prepared))
            if final_stage == "synthesize_final_receipt":
                break
            continue

    status = "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_E2E_ORCHESTRATOR_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_E2E_ORCHESTRATOR_BLOCKED"
    packet_id = "qi-github-actions-pr-live-autopilot-e2e-" + _sha({"records": records, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_github_actions_pr_live_autopilot_e2e_orchestrator_v9_0", "status": status, "packet_id": packet_id, "phases_run": len(records), "final_stage": final_stage, "final_state": final_state, "stop_reason": stop_reason, "connector_action": connector_action, "policy_decision": policy_decision, "action_prepared": action_prepared, "phase_records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPrLiveAutopilotE2EOrchestratorResult("kuuos_runtime_daemon_qi_github_actions_pr_live_autopilot_e2e_orchestrator_v9_0", status, packet_id, str(root), len(records), final_stage, final_state, stop_reason, connector_action, policy_decision, action_prepared, str(receipt_path), str(audit_path), blockers, warnings, records)
