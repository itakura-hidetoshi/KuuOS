#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_pr_live_external_cycle_runner_v8_3 import build_qi_github_actions_pr_live_external_cycle_runner


@dataclass(frozen=True)
class QiGitHubActionsPrLiveAutopilotPacketRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    autopilot_state: str
    stop_reason: str
    connector_action: str
    policy_decision: str
    action_prepared: str
    handoff_packet_path: str
    receipt_path: str
    audit_path: str
    handoff_packet_written: bool
    blockers: list[str]
    warnings: list[str]

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


def _validate_query(query: Mapping[str, Any], blockers: list[str]) -> None:
    if query.get("autopilot_query_allowed") is not True:
        blockers.append("autopilot_query_allowed_not_true")
    repo = str(query.get("repo_full_name", query.get("repository_full_name", ""))).strip()
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    if _i(query.get("pr_number", query.get("pull_number")), 0) <= 0:
        blockers.append("pr_number_invalid")


def _write_live_query(root: pathlib.Path, query: Mapping[str, Any]) -> None:
    live = {
        "query_allowed": True,
        "repo_full_name": str(query.get("repo_full_name", query.get("repository_full_name", ""))),
        "pr_number": _i(query.get("pr_number", query.get("pull_number")), 0),
        "required_workflows": list(query.get("required_workflows", [])) if isinstance(query.get("required_workflows"), list) else ["Qi Process Tensor Review Checks"],
        "merge_when_green": query.get("merge_when_green", True) is True,
        "rerun_when_failed": query.get("rerun_when_failed", True) is True,
        "reobserve_when_pending": query.get("reobserve_when_pending", True) is True,
        "merge_method": str(query.get("merge_method", "merge")),
        "source_autopilot_query_digest": _sha(dict(query)),
        "epoch": int(time.time()),
    }
    _write_json(root / "qi_github_actions_pr_live_query_packet.json", live)


def _cycle_context(root: pathlib.Path, query: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "qi_github_actions_pr_live_external_cycle_runner_enabled": True,
        "apply_github_actions_pr_live_external_cycle_runner": True,
        "runtime_root": str(root),
        "max_pr_live_external_cycle_phases": _i(query.get("max_pr_live_external_cycle_phases", 8), 8),
        "max_pr_live_full_cycle_phases": _i(query.get("max_pr_live_full_cycle_phases", 6), 6),
        "max_pr_live_inner_loop_phases": _i(query.get("max_pr_live_inner_loop_phases", 3), 3),
    }


def _cycle_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CYCLE_RUNNER_LICENSE_READY",
        "full_cycle_run_allowed": True,
        "external_call_bridge_run_allowed": True,
        "external_result_bridge_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _classify(cycle: Mapping[str, Any]) -> str:
    if cycle.get("status") != "QI_GITHUB_ACTIONS_PR_LIVE_EXTERNAL_CYCLE_RUNNER_READY":
        return "blocked"
    if cycle.get("stop_reason") == "await_external_call_result":
        return "await_external_connector"
    if str(cycle.get("policy_decision", "not_run")) not in {"not_run", "unknown"}:
        return "policy_ready"
    return "hold"


def _handoff_packet(state: str, cycle: Mapping[str, Any], external_call: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_pr_live_autopilot_handoff_packet_v8_4",
        "handoff_allowed": True,
        "autopilot_state": state,
        "stop_reason": str(cycle.get("stop_reason", "unknown")),
        "connector_action": str(external_call.get("connector_action", cycle.get("request_action", "none"))),
        "connector_payload": dict(_m(external_call.get("connector_payload"))),
        "external_call_packet": dict(external_call),
        "policy_decision": str(cycle.get("policy_decision", "not_run")),
        "action_prepared": str(cycle.get("action_prepared", "none")),
        "cycle_digest": _sha(dict(cycle)),
        "external_call_digest": _sha(dict(external_call)),
        "next_expected": {
            "await_external_connector": "call connector, write qi_github_actions_pr_live_external_call_raw_result_packet.json, rerun v8.4",
            "policy_ready": "inspect prepared action packet and apply normal guarded action flow",
            "hold": "rerun after additional observation or packet update",
            "blocked": "inspect blockers and do not proceed",
        }.get(state, "inspect state"),
        "epoch": int(time.time()),
    }


def build_qi_github_actions_pr_live_autopilot_packet_runner(*, runtime_context: Mapping[str, Any], autopilot_packet_runner_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveAutopilotPacketRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(autopilot_packet_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    query_path = root / "qi_github_actions_pr_live_autopilot_query_packet.json"
    handoff_path = root / "qi_github_actions_pr_live_autopilot_handoff_packet.json"
    receipt_path = root / "qi_github_actions_pr_live_autopilot_packet_runner_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_autopilot_packet_runner_audit.jsonl"

    if ctx.get("qi_github_actions_pr_live_autopilot_packet_runner_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_autopilot_packet_runner_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_autopilot_packet_runner") is not True:
        blockers.append("apply_github_actions_pr_live_autopilot_packet_runner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_PACKET_RUNNER_LICENSE_READY":
        blockers.append("github_actions_pr_live_autopilot_packet_runner_license_not_ready")
    for name in ["autopilot_query_read_allowed", "live_query_write_allowed", "external_cycle_run_allowed", "handoff_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    query = _read_json(query_path)
    if not query:
        blockers.append("autopilot_query_packet_missing_or_invalid")
    if query:
        _validate_query(query, blockers)

    cycle: dict[str, Any] = {}
    external_call: dict[str, Any] = {}
    state = "blocked"
    handoff: dict[str, Any] = {}
    written = False
    stop_reason = "not_run"
    connector_action = "none"
    policy_decision = "not_run"
    action_prepared = "none"
    if not blockers:
        _write_live_query(root, query)
        cycle = build_qi_github_actions_pr_live_external_cycle_runner(
            runtime_context=_cycle_context(root, query),
            pr_live_external_cycle_runner_license=_cycle_license(),
        ).to_dict()
        external_call = _read_json(root / "qi_github_actions_pr_live_external_call_packet.json")
        state = _classify(cycle)
        if state == "blocked":
            blockers.append("external_cycle_runner_not_ready")
        stop_reason = str(cycle.get("stop_reason", "unknown"))
        connector_action = str(external_call.get("connector_action", cycle.get("request_action", "none")))
        policy_decision = str(cycle.get("policy_decision", "not_run"))
        action_prepared = str(cycle.get("action_prepared", "none"))
        handoff = _handoff_packet(state, cycle, external_call)
        if lic.get("handoff_packet_write_allowed") is True:
            _write_json(handoff_path, handoff)
            written = True

    status = "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_PACKET_RUNNER_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_PACKET_RUNNER_BLOCKED"
    packet_id = "qi-github-actions-pr-live-autopilot-" + _sha({"state": state, "cycle": cycle, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_live_autopilot_packet_runner_v8_4",
        "status": status,
        "packet_id": packet_id,
        "autopilot_state": state,
        "stop_reason": stop_reason,
        "connector_action": connector_action,
        "policy_decision": policy_decision,
        "action_prepared": action_prepared,
        "handoff_packet_written": written,
        "handoff_packet_digest": _sha(handoff),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPrLiveAutopilotPacketRunnerResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_live_autopilot_packet_runner_v8_4",
        status,
        packet_id,
        str(root),
        state,
        stop_reason,
        connector_action,
        policy_decision,
        action_prepared,
        str(handoff_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
