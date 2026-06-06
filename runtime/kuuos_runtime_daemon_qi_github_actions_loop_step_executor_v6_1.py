#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_capability_planner_v5_5 import build_qi_github_actions_capability_planner
from runtime.kuuos_runtime_daemon_qi_github_actions_result_ingestor_v5_7 import build_qi_github_actions_result_ingestor
from runtime.kuuos_runtime_daemon_qi_github_actions_status_reobserver_v5_8 import build_qi_github_actions_status_reobserver
from runtime.kuuos_runtime_daemon_qi_github_actions_observation_result_ingestor_v5_9 import build_qi_github_actions_observation_result_ingestor


LOCAL_STAGE_COMMANDS = {
    "plan_from_status": "run_qi_github_actions_capability_planner_v5_5",
    "operation_result_ingest": "run_qi_github_actions_status_ingestor_v5_7",
    "status_reobserve": "run_qi_github_actions_status_reobserver_v5_8",
    "observation_result_ingest": "run_qi_github_actions_observation_result_ingestor_v5_9",
}

WAIT_STAGE_COMMANDS = {
    "await_connector_operation": "await_github_connector_operation",
    "await_status_observation": "await_github_actions_status_packet",
}


@dataclass(frozen=True)
class QiGitHubActionsLoopStepExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    selected_stage: str
    next_command: str
    step_result_class: str
    substage_status: str
    receipt_path: str
    audit_path: str
    local_step_performed: bool
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


def _planner_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_capability_planner_enabled": True,
        "apply_github_actions_capability_planner": True,
        "runtime_root": str(root),
    }


def _planner_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_CAPABILITY_PLANNER_LICENSE_READY",
        "github_actions_status_packet_read_allowed": True,
        "capability_recipe_batch_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _result_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_result_ingestor_enabled": True,
        "apply_github_actions_result_ingestor": True,
        "runtime_root": str(root),
    }


def _result_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_RESULT_INGESTOR_LICENSE_READY",
        "connector_request_read_allowed": True,
        "connector_result_read_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _reobserve_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_status_reobserver_enabled": True,
        "apply_github_actions_status_reobserver": True,
        "runtime_root": str(root),
    }


def _reobserve_license(kind: str) -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_STATUS_REOBSERVER_LICENSE_READY",
        "reobserve_request_read_allowed": True,
        "observation_request_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        f"allow_{kind}_observation": True,
    }


def _observation_result_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_observation_result_ingestor_enabled": True,
        "apply_github_actions_observation_result_ingestor": True,
        "runtime_root": str(root),
    }


def _observation_result_license(kind: str) -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_OBSERVATION_RESULT_INGESTOR_LICENSE_READY",
        "observation_request_read_allowed": True,
        "observation_result_read_allowed": True,
        "status_packet_write_allowed": True,
        "observation_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        f"allow_{kind}_observation": True,
    }


def _stage_payload(root: pathlib.Path, stage: str) -> Mapping[str, Any]:
    if stage == "status_reobserve":
        return _read_json(root / "qi_github_actions_status_reobserve_request.json")
    if stage == "observation_result_ingest":
        return _read_json(root / "qi_github_actions_observation_connector_request.json")
    return {}


def _observation_kind(root: pathlib.Path, stage: str) -> str:
    payload = _stage_payload(root, stage)
    return str(payload.get("observation_kind", "commit_workflow_runs")) if payload else "commit_workflow_runs"


def _run_local_stage(stage: str, root: pathlib.Path) -> Mapping[str, Any]:
    if stage == "plan_from_status":
        return build_qi_github_actions_capability_planner(
            runtime_context=_planner_context(root),
            github_actions_planner_license=_planner_license(),
        ).to_dict()
    if stage == "operation_result_ingest":
        return build_qi_github_actions_result_ingestor(
            runtime_context=_result_context(root),
            result_ingestor_license=_result_license(),
        ).to_dict()
    if stage == "status_reobserve":
        kind = _observation_kind(root, stage)
        return build_qi_github_actions_status_reobserver(
            runtime_context=_reobserve_context(root),
            status_reobserver_license=_reobserve_license(kind),
        ).to_dict()
    if stage == "observation_result_ingest":
        kind = _observation_kind(root, stage)
        return build_qi_github_actions_observation_result_ingestor(
            runtime_context=_observation_result_context(root),
            observation_result_ingestor_license=_observation_result_license(kind),
        ).to_dict()
    return {}


def build_qi_github_actions_loop_step_executor(*, runtime_context: Mapping[str, Any], loop_step_executor_license: Mapping[str, Any]) -> QiGitHubActionsLoopStepExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(loop_step_executor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    command_path = root / "qi_github_actions_loop_command_packet.json"
    receipt_path = root / "qi_github_actions_loop_step_executor_receipt.json"
    audit_path = root / "qi_github_actions_loop_step_executor_audit.jsonl"

    if ctx.get("qi_github_actions_loop_step_executor_enabled") is not True:
        blockers.append("qi_github_actions_loop_step_executor_enabled_not_true")
    if ctx.get("apply_github_actions_loop_step_executor") is not True:
        blockers.append("apply_github_actions_loop_step_executor_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_LOOP_STEP_EXECUTOR_LICENSE_READY":
        blockers.append("github_actions_loop_step_executor_license_not_ready")
    for name in ["loop_command_read_allowed", "local_step_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    command_packet = _read_json(command_path)
    if not command_packet:
        blockers.append("loop_command_packet_missing_or_invalid")
    stage = str(command_packet.get("selected_stage", "unknown")) if command_packet else "unknown"
    next_command = str(command_packet.get("next_command", "unknown")) if command_packet else "unknown"
    if stage not in LOCAL_STAGE_COMMANDS and stage not in WAIT_STAGE_COMMANDS:
        blockers.append("selected_stage_not_allowlisted")
    if lic.get(f"allow_{stage}_stage") is not True:
        blockers.append(f"{stage}_not_allowed_by_loop_step_executor_license")

    substage_result: Mapping[str, Any] = {}
    local_step_performed = False
    step_result_class = "not_run"
    substage_status = "NOT_RUN"
    if not blockers:
        if stage in LOCAL_STAGE_COMMANDS:
            substage_result = _run_local_stage(stage, root)
            local_step_performed = True
            substage_status = str(substage_result.get("status", "unknown"))
            if substage_status.endswith("READY"):
                step_result_class = "local_stage_completed"
            else:
                step_result_class = "local_stage_blocked"
                blockers.append("local_stage_not_ready")
        else:
            step_result_class = "waiting_for_external_observation" if stage == "await_status_observation" else "waiting_for_connector_operation"
            substage_status = "WAITING"

    status = "QI_GITHUB_ACTIONS_LOOP_STEP_EXECUTOR_READY" if not blockers else "QI_GITHUB_ACTIONS_LOOP_STEP_EXECUTOR_BLOCKED"
    packet_id = "qi-github-actions-loop-step-" + _sha({"command": command_packet, "substage": substage_result, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_loop_step_executor_v6_1",
        "status": status,
        "packet_id": packet_id,
        "selected_stage": stage,
        "next_command": next_command,
        "step_result_class": step_result_class,
        "substage_status": substage_status,
        "local_step_performed": local_step_performed,
        "substage_digest": _sha(substage_result),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsLoopStepExecutorResult(
        "kuuos_runtime_daemon_qi_github_actions_loop_step_executor_v6_1",
        status,
        packet_id,
        str(root),
        stage,
        next_command,
        step_result_class,
        substage_status,
        str(receipt_path),
        str(audit_path),
        local_step_performed,
        blockers,
        warnings,
    )
