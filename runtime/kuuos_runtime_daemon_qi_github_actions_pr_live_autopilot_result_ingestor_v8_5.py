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


@dataclass(frozen=True)
class QiGitHubActionsPrLiveAutopilotResultIngestorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    ingestor_result: str
    autopilot_state: str
    stop_reason: str
    connector_action: str
    policy_decision: str
    action_prepared: str
    raw_result_path: str
    handoff_packet_path: str
    receipt_path: str
    audit_path: str
    raw_result_written: bool
    handoff_packet_written: bool
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


def _payload(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = raw.get("connector_result")
    return nested if isinstance(nested, Mapping) else raw


def _validate_handoff(handoff: Mapping[str, Any], result: Mapping[str, Any], blockers: list[str]) -> None:
    if handoff.get("handoff_allowed") is not True:
        blockers.append("handoff_allowed_not_true")
    if handoff.get("autopilot_state") != "await_external_connector":
        blockers.append("handoff_state_not_await_external_connector")
    action = str(handoff.get("connector_action", ""))
    if action not in {"GitHub.get_pr_info", "GitHub.fetch_commit_workflow_runs"}:
        blockers.append("connector_action_not_allowlisted")
    result_action = str(result.get("connector_action", action))
    if result_action != action:
        blockers.append("connector_action_mismatch")


def _validate_payload(action: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    if action == "GitHub.get_pr_info":
        head = payload.get("head")
        nested_sha = head.get("sha") if isinstance(head, Mapping) else ""
        if not str(payload.get("head_sha") or nested_sha or "").strip():
            blockers.append("head_sha_missing")
        if not (payload.get("number") or payload.get("pr_number")):
            blockers.append("pr_number_missing")
    elif action == "GitHub.fetch_commit_workflow_runs":
        runs = payload.get("workflow_runs")
        if not isinstance(runs, list) or not runs:
            blockers.append("workflow_runs_empty_or_invalid")


def _raw_result_packet(handoff: Mapping[str, Any], connector_result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_pr_live_external_call_raw_result_from_autopilot_ingestor_v8_5",
        "connector_action": str(handoff.get("connector_action", "unknown")),
        "connector_result": dict(_payload(connector_result)),
        "source_handoff_digest": _sha(dict(handoff)),
        "source_connector_result_digest": _sha(dict(connector_result)),
        "epoch": int(time.time()),
    }


def _runner_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_pr_live_autopilot_packet_runner_enabled": True,
        "apply_github_actions_pr_live_autopilot_packet_runner": True,
        "runtime_root": str(root),
    }


def _runner_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_PACKET_RUNNER_LICENSE_READY",
        "autopilot_query_read_allowed": True,
        "live_query_write_allowed": True,
        "external_cycle_run_allowed": True,
        "handoff_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_qi_github_actions_pr_live_autopilot_result_ingestor(*, runtime_context: Mapping[str, Any], autopilot_result_ingestor_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveAutopilotResultIngestorResult:
    ctx = _m(runtime_context)
    lic = _m(autopilot_result_ingestor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    handoff_path = root / "qi_github_actions_pr_live_autopilot_handoff_packet.json"
    connector_result_path = root / "qi_github_actions_pr_live_autopilot_connector_result_packet.json"
    raw_result_path = root / "qi_github_actions_pr_live_external_call_raw_result_packet.json"
    receipt_path = root / "qi_github_actions_pr_live_autopilot_result_ingestor_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_autopilot_result_ingestor_audit.jsonl"

    if ctx.get("qi_github_actions_pr_live_autopilot_result_ingestor_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_autopilot_result_ingestor_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_autopilot_result_ingestor") is not True:
        blockers.append("apply_github_actions_pr_live_autopilot_result_ingestor_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_RESULT_INGESTOR_LICENSE_READY":
        blockers.append("github_actions_pr_live_autopilot_result_ingestor_license_not_ready")
    for name in ["handoff_packet_read_allowed", "connector_result_read_allowed", "raw_result_packet_write_allowed", "autopilot_runner_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    handoff = _read_json(handoff_path)
    connector_result = _read_json(connector_result_path)
    if not handoff:
        blockers.append("handoff_packet_missing_or_invalid")
    if not connector_result:
        blockers.append("connector_result_packet_missing_or_invalid")
    if handoff and connector_result:
        _validate_handoff(handoff, connector_result, blockers)
        _validate_payload(str(handoff.get("connector_action", "")), _payload(connector_result), blockers)

    ingestor_result = "blocked"
    raw_written = False
    handoff_written = False
    state = "blocked"
    stop_reason = "not_run"
    connector_action = str(handoff.get("connector_action", "none")) if handoff else "none"
    policy_decision = "not_run"
    action_prepared = "none"
    if not blockers:
        raw_packet = _raw_result_packet(handoff, connector_result)
        _write_json(raw_result_path, raw_packet)
        raw_written = True
        ingestor_result = "raw_result_written"
        runner = build_qi_github_actions_pr_live_autopilot_packet_runner(
            runtime_context=_runner_context(root),
            autopilot_packet_runner_license=_runner_license(),
        ).to_dict()
        state = str(runner.get("autopilot_state", "unknown"))
        stop_reason = str(runner.get("stop_reason", "unknown"))
        connector_action = str(runner.get("connector_action", connector_action))
        policy_decision = str(runner.get("policy_decision", "not_run"))
        action_prepared = str(runner.get("action_prepared", "none"))
        handoff_written = runner.get("handoff_packet_written") is True
        if runner.get("status") != "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_PACKET_RUNNER_READY":
            blockers.append("autopilot_packet_runner_not_ready")
            ingestor_result = "autopilot_runner_blocked"

    status = "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_RESULT_INGESTOR_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_AUTOPILOT_RESULT_INGESTOR_BLOCKED"
    packet_id = "qi-github-actions-pr-live-autopilot-result-" + _sha({"handoff": handoff, "connector_result": connector_result, "state": state, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_live_autopilot_result_ingestor_v8_5",
        "status": status,
        "packet_id": packet_id,
        "ingestor_result": ingestor_result,
        "autopilot_state": state,
        "stop_reason": stop_reason,
        "connector_action": connector_action,
        "policy_decision": policy_decision,
        "action_prepared": action_prepared,
        "raw_result_written": raw_written,
        "handoff_packet_written": handoff_written,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPrLiveAutopilotResultIngestorResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_live_autopilot_result_ingestor_v8_5",
        status,
        packet_id,
        str(root),
        ingestor_result,
        state,
        stop_reason,
        connector_action,
        policy_decision,
        action_prepared,
        str(raw_result_path),
        str(handoff_path),
        str(receipt_path),
        str(audit_path),
        raw_written,
        handoff_written,
        blockers,
        warnings,
    )
