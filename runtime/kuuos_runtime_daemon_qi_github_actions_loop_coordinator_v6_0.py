#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


STAGE_ORDER = [
    "observation_result_ingest",
    "status_reobserve",
    "operation_result_ingest",
    "await_connector_operation",
    "plan_from_status",
    "await_status_observation",
]


@dataclass(frozen=True)
class QiGitHubActionsLoopCoordinatorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    selected_stage: str
    next_command: str
    command_packet_path: str
    receipt_path: str
    audit_path: str
    command_emitted: bool
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


def _exists_json(root: pathlib.Path, name: str) -> bool:
    return bool(_read_json(root / name))


def _select_stage(root: pathlib.Path) -> tuple[str, str, str]:
    if _exists_json(root, "qi_github_actions_observation_connector_result_packet.json"):
        return "observation_result_ingest", "run_qi_github_actions_observation_result_ingestor_v5_9", "qi_github_actions_loop_command_packet.json"
    if _exists_json(root, "qi_github_actions_status_reobserve_request.json"):
        return "status_reobserve", "run_qi_github_actions_status_reobserver_v5_8", "qi_github_actions_loop_command_packet.json"
    if _exists_json(root, "qi_github_actions_connector_result_packet.json"):
        return "operation_result_ingest", "run_qi_github_actions_status_ingestor_v5_7", "qi_github_actions_loop_command_packet.json"
    if _exists_json(root, "qi_github_actions_connector_execution_request.json"):
        return "await_connector_operation", "await_github_connector_operation", "qi_github_actions_loop_command_packet.json"
    if _exists_json(root, "qi_github_actions_status_packet.json"):
        return "plan_from_status", "run_qi_github_actions_capability_planner_v5_5", "qi_github_actions_loop_command_packet.json"
    return "await_status_observation", "await_github_actions_status_packet", "qi_github_actions_loop_command_packet.json"


def _command(stage: str, command: str, root: pathlib.Path) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_loop_command_v6_0",
        "selected_stage": stage,
        "next_command": command,
        "runtime_root": str(root),
        "stage_order": STAGE_ORDER,
        "boundary": {
            "coordinator_only": True,
            "does_not_run_subprocess": True,
            "does_not_call_github_connector": True,
            "selects_next_loop_stage": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_loop_coordinator(*, runtime_context: Mapping[str, Any], loop_coordinator_license: Mapping[str, Any]) -> QiGitHubActionsLoopCoordinatorResult:
    ctx = _m(runtime_context)
    lic = _m(loop_coordinator_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    command_packet_path = root / "qi_github_actions_loop_command_packet.json"
    receipt_path = root / "qi_github_actions_loop_coordinator_receipt.json"
    audit_path = root / "qi_github_actions_loop_coordinator_audit.jsonl"

    if ctx.get("qi_github_actions_loop_coordinator_enabled") is not True:
        blockers.append("qi_github_actions_loop_coordinator_enabled_not_true")
    if ctx.get("apply_github_actions_loop_coordinator") is not True:
        blockers.append("apply_github_actions_loop_coordinator_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_LOOP_COORDINATOR_LICENSE_READY":
        blockers.append("github_actions_loop_coordinator_license_not_ready")
    for name in ["loop_state_read_allowed", "loop_command_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    stage, command, _ = _select_stage(root)
    if lic.get(f"allow_{stage}_stage") is not True:
        blockers.append(f"{stage}_not_allowed_by_loop_coordinator_license")
    payload = _command(stage, command, root)
    command_emitted = False
    if not blockers:
        _write_json(command_packet_path, payload)
        command_emitted = True

    status = "QI_GITHUB_ACTIONS_LOOP_COORDINATOR_READY" if not blockers else "QI_GITHUB_ACTIONS_LOOP_COORDINATOR_BLOCKED"
    packet_id = "qi-github-actions-loop-coordinator-" + _sha({"stage": stage, "command": command, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_loop_coordinator_v6_0",
        "status": status,
        "packet_id": packet_id,
        "selected_stage": stage,
        "next_command": command,
        "command_emitted": command_emitted,
        "command_digest": _sha(payload),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsLoopCoordinatorResult(
        "kuuos_runtime_daemon_qi_github_actions_loop_coordinator_v6_0",
        status,
        packet_id,
        str(root),
        stage,
        command,
        str(command_packet_path),
        str(receipt_path),
        str(audit_path),
        command_emitted,
        blockers,
        warnings,
    )
