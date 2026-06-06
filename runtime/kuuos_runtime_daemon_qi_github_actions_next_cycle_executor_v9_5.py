#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ALLOWED_NEXT_STATES = {
    "closed",
    "await_workflow_reobserve",
    "reenter_policy_loop",
}


@dataclass(frozen=True)
class QiGitHubActionsNextCycleExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    next_cycle_state: str
    execution_state: str
    connector_action: str
    execution_packet_path: str
    receipt_path: str
    audit_path: str
    execution_packet_written: bool
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


def _validate_next_packet(packet: Mapping[str, Any], blockers: list[str]) -> str:
    if packet.get("next_cycle_allowed") is not True:
        blockers.append("next_cycle_allowed_not_true")
    state = str(packet.get("next_cycle_state", "unknown"))
    if state not in ALLOWED_NEXT_STATES:
        blockers.append("next_cycle_state_not_allowlisted")
    return state


def _validate_reobserve_request(packet: Mapping[str, Any], blockers: list[str]) -> None:
    if packet.get("request_allowed") is not True:
        blockers.append("reobserve_request_allowed_not_true")
    if packet.get("connector_action") != "GitHub.fetch_commit_workflow_runs":
        blockers.append("reobserve_connector_action_mismatch")
    payload = _m(packet.get("connector_payload"))
    repo = payload.get("repo_full_name") or payload.get("repository_full_name")
    if not isinstance(repo, str) or "/" not in repo:
        blockers.append("repo_full_name_invalid")
    if not str(payload.get("commit_sha", "")).strip():
        blockers.append("commit_sha_missing")


def _validate_reentry_packet(packet: Mapping[str, Any], blockers: list[str]) -> None:
    if packet.get("reentry_allowed") is not True:
        blockers.append("reentry_allowed_not_true")
    runs = packet.get("workflow_runs")
    if not isinstance(runs, list) or not runs:
        blockers.append("workflow_runs_empty_or_invalid")
    status = _m(packet.get("status_summary"))
    if not status:
        blockers.append("status_summary_missing_or_invalid")


def _execution_packet(state: str, next_packet: Mapping[str, Any], source: Mapping[str, Any]) -> dict[str, Any]:
    if state == "closed":
        execution_state = "cycle_closed"
        connector_action = "none"
        payload: dict[str, Any] = {"closed": True}
    elif state == "await_workflow_reobserve":
        execution_state = "external_reobserve_ready"
        connector_action = str(source.get("connector_action", "GitHub.fetch_commit_workflow_runs"))
        payload = dict(_m(source.get("connector_payload")))
    else:
        execution_state = "policy_reentry_ready"
        connector_action = "none"
        payload = dict(source)
    return {
        "version": "qi_github_actions_next_cycle_execution_packet_v9_5",
        "execution_allowed": True,
        "next_cycle_state": state,
        "execution_state": execution_state,
        "connector_action": connector_action,
        "connector_payload": payload,
        "source_next_cycle_digest": _sha(dict(next_packet)),
        "source_payload_digest": _sha(dict(source)),
        "boundary": {
            "execution_packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "does_not_apply_policy_action": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_next_cycle_executor(*, runtime_context: Mapping[str, Any], next_cycle_executor_license: Mapping[str, Any]) -> QiGitHubActionsNextCycleExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(next_cycle_executor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)

    next_path = root / "qi_github_actions_route_next_cycle_packet.json"
    reobserve_path = root / "qi_github_actions_route_reobserve_request_packet.json"
    reentry_path = root / "qi_github_actions_route_policy_reentry_packet.json"
    execution_path = root / "qi_github_actions_next_cycle_execution_packet.json"
    receipt_path = root / "qi_github_actions_next_cycle_executor_receipt.json"
    audit_path = root / "qi_github_actions_next_cycle_executor_audit.jsonl"

    if ctx.get("qi_github_actions_next_cycle_executor_enabled") is not True:
        blockers.append("qi_github_actions_next_cycle_executor_enabled_not_true")
    if ctx.get("apply_github_actions_next_cycle_executor") is not True:
        blockers.append("apply_github_actions_next_cycle_executor_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_NEXT_CYCLE_EXECUTOR_LICENSE_READY":
        blockers.append("github_actions_next_cycle_executor_license_not_ready")
    for name in ["next_cycle_packet_read_allowed", "route_payload_read_allowed", "execution_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    next_packet = _read_json(next_path)
    if not next_packet:
        blockers.append("next_cycle_packet_missing_or_invalid")
    state = _validate_next_packet(next_packet, blockers) if next_packet else "unknown"
    source: dict[str, Any] = {}
    if not blockers:
        if state == "closed":
            source = {"closed": True}
        elif state == "await_workflow_reobserve":
            source = _read_json(reobserve_path)
            if not source:
                blockers.append("reobserve_request_packet_missing_or_invalid")
            else:
                _validate_reobserve_request(source, blockers)
        elif state == "reenter_policy_loop":
            source = _read_json(reentry_path)
            if not source:
                blockers.append("policy_reentry_packet_missing_or_invalid")
            else:
                _validate_reentry_packet(source, blockers)

    packet: dict[str, Any] = {}
    written = False
    execution_state = "blocked"
    connector_action = "none"
    if not blockers:
        packet = _execution_packet(state, next_packet, source)
        _write_json(execution_path, packet)
        written = True
        execution_state = str(packet.get("execution_state", "unknown"))
        connector_action = str(packet.get("connector_action", "none"))

    status = "QI_GITHUB_ACTIONS_NEXT_CYCLE_EXECUTOR_READY" if not blockers else "QI_GITHUB_ACTIONS_NEXT_CYCLE_EXECUTOR_BLOCKED"
    packet_id = "qi-github-actions-next-cycle-executor-" + _sha({"next": next_packet, "state": state, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_next_cycle_executor_v9_5",
        "status": status,
        "packet_id": packet_id,
        "next_cycle_state": state,
        "execution_state": execution_state,
        "connector_action": connector_action,
        "execution_packet_written": written,
        "execution_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsNextCycleExecutorResult(
        "kuuos_runtime_daemon_qi_github_actions_next_cycle_executor_v9_5",
        status,
        packet_id,
        str(root),
        state,
        execution_state,
        connector_action,
        str(execution_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
