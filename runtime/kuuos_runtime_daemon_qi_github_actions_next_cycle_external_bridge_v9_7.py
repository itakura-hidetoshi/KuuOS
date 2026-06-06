#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ALLOWED_EXECUTION_STATES = {
    "cycle_closed",
    "external_reobserve_ready",
    "policy_reentry_ready",
}


@dataclass(frozen=True)
class QiGitHubActionsNextCycleExternalBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    execution_state: str
    bridge_state: str
    connector_action: str
    output_packet_path: str
    receipt_path: str
    audit_path: str
    output_packet_written: bool
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


def _workflow_runs(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = packet.get("workflow_runs", [])
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _status_summary(runs: list[Mapping[str, Any]]) -> dict[str, Any]:
    conclusions = [str(run.get("conclusion")) for run in runs if run.get("conclusion") is not None]
    statuses = [str(run.get("status")) for run in runs]
    all_completed = bool(runs) and all(status == "completed" for status in statuses)
    any_failed = any(conclusion in {"failure", "cancelled", "timed_out"} for conclusion in conclusions)
    all_success = bool(runs) and all_completed and all(conclusion == "success" for conclusion in conclusions)
    return {
        "all_completed": all_completed,
        "all_success": all_success,
        "any_failed": any_failed,
        "workflow_run_count": len(runs),
        "workflow_runs": [dict(run) for run in runs],
        "epoch": int(time.time()),
    }


def _validate_execution(packet: Mapping[str, Any], blockers: list[str]) -> str:
    if packet.get("execution_allowed") is not True:
        blockers.append("execution_allowed_not_true")
    state = str(packet.get("execution_state", "unknown"))
    if state not in ALLOWED_EXECUTION_STATES:
        blockers.append("execution_state_not_allowlisted")
    return state


def _validate_external_payload(payload: Mapping[str, Any], blockers: list[str]) -> None:
    repo = payload.get("repo_full_name") or payload.get("repository_full_name")
    if not isinstance(repo, str) or "/" not in repo:
        blockers.append("repo_full_name_invalid")
    if not str(payload.get("commit_sha", "")).strip():
        blockers.append("commit_sha_missing")


def _validate_reentry_payload(payload: Mapping[str, Any], blockers: list[str]) -> None:
    if payload.get("reentry_allowed") is not True:
        blockers.append("reentry_allowed_not_true")
    runs = _workflow_runs(payload)
    if not runs:
        blockers.append("workflow_runs_empty_or_invalid")
    if not isinstance(payload.get("status_summary"), Mapping):
        blockers.append("status_summary_missing_or_invalid")


def _closure_packet(execution: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_next_cycle_closure_packet_v9_7",
        "closure_allowed": True,
        "bridge_state": "cycle_closed_final",
        "source_execution_digest": _sha(dict(execution)),
        "boundary": {
            "closure_only": True,
            "does_not_call_connector_inside_runtime": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def _external_call_packet(execution: Mapping[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_next_cycle_external_call_packet_v9_7",
        "external_call_allowed": True,
        "bridge_state": "next_cycle_external_call_ready",
        "connector_action": "GitHub.fetch_commit_workflow_runs",
        "connector_payload": dict(payload),
        "external_result_expected_file": "qi_github_actions_next_cycle_external_call_raw_result_packet.json",
        "source_execution_digest": _sha(dict(execution)),
        "boundary": {
            "packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "result_must_be_ingested_by_next_cycle_result_bridge": True,
        },
        "epoch": int(time.time()),
    }


def _reentry_bridge_packet(execution: Mapping[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    runs = _workflow_runs(payload)
    return {
        "version": "qi_github_actions_next_cycle_reentry_bridge_packet_v9_7",
        "reentry_bridge_allowed": True,
        "bridge_state": "policy_reentry_bridge_ready",
        "workflow_runs": runs,
        "status_summary": _status_summary(runs),
        "next_runner": "kuuos_runtime_daemon_qi_github_actions_cycle_aware_super_executor_v9_6",
        "source_execution_digest": _sha(dict(execution)),
        "boundary": {
            "reentry_packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "feeds_policy_reentry_surface": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_next_cycle_external_bridge(*, runtime_context: Mapping[str, Any], next_cycle_external_bridge_license: Mapping[str, Any]) -> QiGitHubActionsNextCycleExternalBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(next_cycle_external_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)

    execution_path = root / "qi_github_actions_next_cycle_execution_packet.json"
    closure_path = root / "qi_github_actions_next_cycle_closure_packet.json"
    external_call_path = root / "qi_github_actions_next_cycle_external_call_packet.json"
    reentry_bridge_path = root / "qi_github_actions_next_cycle_reentry_bridge_packet.json"
    receipt_path = root / "qi_github_actions_next_cycle_external_bridge_receipt.json"
    audit_path = root / "qi_github_actions_next_cycle_external_bridge_audit.jsonl"

    if ctx.get("qi_github_actions_next_cycle_external_bridge_enabled") is not True:
        blockers.append("qi_github_actions_next_cycle_external_bridge_enabled_not_true")
    if ctx.get("apply_github_actions_next_cycle_external_bridge") is not True:
        blockers.append("apply_github_actions_next_cycle_external_bridge_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_NEXT_CYCLE_EXTERNAL_BRIDGE_LICENSE_READY":
        blockers.append("github_actions_next_cycle_external_bridge_license_not_ready")
    for name in ["execution_packet_read_allowed", "output_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    execution = _read_json(execution_path)
    if not execution:
        blockers.append("execution_packet_missing_or_invalid")
    state = _validate_execution(execution, blockers) if execution else "unknown"
    payload = _m(execution.get("connector_payload")) if execution else {}
    output_path = root / "qi_github_actions_next_cycle_blocked_packet.json"
    packet: dict[str, Any] = {}
    bridge_state = "blocked"
    connector_action = "none"

    if not blockers:
        if state == "cycle_closed":
            packet = _closure_packet(execution)
            output_path = closure_path
            bridge_state = "cycle_closed_final"
        elif state == "external_reobserve_ready":
            if execution.get("connector_action") != "GitHub.fetch_commit_workflow_runs":
                blockers.append("connector_action_mismatch")
            _validate_external_payload(payload, blockers)
            if not blockers:
                packet = _external_call_packet(execution, payload)
                output_path = external_call_path
                bridge_state = "next_cycle_external_call_ready"
                connector_action = "GitHub.fetch_commit_workflow_runs"
        elif state == "policy_reentry_ready":
            _validate_reentry_payload(payload, blockers)
            if not blockers:
                packet = _reentry_bridge_packet(execution, payload)
                output_path = reentry_bridge_path
                bridge_state = "policy_reentry_bridge_ready"

    written = False
    if not blockers:
        _write_json(output_path, packet)
        written = True

    status = "QI_GITHUB_ACTIONS_NEXT_CYCLE_EXTERNAL_BRIDGE_READY" if not blockers else "QI_GITHUB_ACTIONS_NEXT_CYCLE_EXTERNAL_BRIDGE_BLOCKED"
    packet_id = "qi-github-actions-next-cycle-external-bridge-" + _sha({"execution": execution, "state": state, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_next_cycle_external_bridge_v9_7",
        "status": status,
        "packet_id": packet_id,
        "execution_state": state,
        "bridge_state": bridge_state,
        "connector_action": connector_action,
        "output_packet_written": written,
        "output_packet_path": str(output_path),
        "output_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsNextCycleExternalBridgeResult(
        "kuuos_runtime_daemon_qi_github_actions_next_cycle_external_bridge_v9_7",
        status,
        packet_id,
        str(root),
        state,
        bridge_state,
        connector_action,
        str(output_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
