#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


OS_NAMES = ("MemoryOS", "PlanOS", "RunGovernance")
STAGE_FEEDBACK_MODES = {"final_stage_candidate", "stage_evidence_request", "stage_repair_quarantine"}
EXPECTED_FILES = {
    "MemoryOS": "memory_os_stage_feedback_action_packet.json",
    "PlanOS": "plan_os_stage_feedback_action_packet.json",
    "RunGovernance": "run_governance_stage_feedback_action_packet.json",
}


@dataclass(frozen=True)
class TriOSStageFeedbackActionIntakeValidatorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    memory_action_decision: str
    plan_action_decision: str
    run_governance_action_decision: str
    action_intake_packet_path: str
    receipt_path: str
    audit_path: str
    action_intake_packet_written: bool
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


def _decision(blockers: list[str], warnings: list[str]) -> str:
    if blockers:
        return "block"
    if warnings:
        return "hold"
    return "accept"


def _common(packet: Mapping[str, Any], os_name: str) -> tuple[list[str], list[str]]:
    blockers: list[str] = []
    warnings: list[str] = []
    if not packet:
        blockers.append(f"{os_name.lower()}_stage_feedback_action_packet_missing")
        return blockers, warnings
    if packet.get("target_os") != os_name:
        blockers.append(f"{os_name.lower()}_target_os_mismatch")
    mode = str(packet.get("stage_feedback_mode", ""))
    if mode not in STAGE_FEEDBACK_MODES:
        blockers.append(f"{os_name.lower()}_stage_feedback_mode_invalid")
    boundary = _m(packet.get("boundary"))
    if boundary.get("stage_feedback_action_packet_only") is not True:
        blockers.append(f"{os_name.lower()}_stage_feedback_action_packet_only_boundary_missing")
    if boundary.get("does_not_authorize_execution") is not True:
        blockers.append(f"{os_name.lower()}_execution_boundary_missing")
    if mode == "stage_repair_quarantine" and boundary.get("repair_quarantine_blocks_final_candidate") is not True:
        blockers.append(f"{os_name.lower()}_repair_quarantine_boundary_missing")
    if not packet.get("stage_feedback_action"):
        warnings.append(f"{os_name.lower()}_stage_feedback_action_missing")
    return blockers, warnings


def _validate_memory(packet: Mapping[str, Any]) -> tuple[str, list[str], list[str]]:
    blockers, warnings = _common(packet, "MemoryOS")
    boundary = _m(packet.get("boundary"))
    payload = _m(packet.get("action_payload"))
    if packet:
        if boundary.get("does_not_consume_memory") is not True:
            blockers.append("memory_consume_boundary_missing")
        if boundary.get("does_not_overwrite_memory") is not True:
            blockers.append("memory_overwrite_boundary_missing")
        if boundary.get("append_only_memory_required") is not True:
            blockers.append("memory_append_only_boundary_missing")
        if payload.get("allow_overwrite") is True:
            blockers.append("memory_stage_feedback_overwrite_attempt")
        if payload.get("append_only_required") is not True:
            warnings.append("memory_append_only_payload_not_visible")
    return _decision(blockers, warnings), blockers, warnings


def _validate_plan(packet: Mapping[str, Any]) -> tuple[str, list[str], list[str]]:
    blockers, warnings = _common(packet, "PlanOS")
    boundary = _m(packet.get("boundary"))
    payload = _m(packet.get("action_payload"))
    if packet:
        if boundary.get("does_not_commit_plan") is not True:
            blockers.append("plan_commit_boundary_missing")
        if boundary.get("candidate_weighting_not_truth") is not True:
            blockers.append("plan_candidate_weighting_boundary_missing")
        if payload.get("commit_allowed") is True:
            blockers.append("plan_stage_feedback_commit_attempt")
        if payload.get("candidate_weighting_authority") not in {"advisory_only", None}:
            blockers.append("plan_stage_feedback_authority_leak")
        if not payload.get("plan_stage_feedback_operation"):
            warnings.append("plan_stage_feedback_operation_missing")
    return _decision(blockers, warnings), blockers, warnings


def _validate_run(packet: Mapping[str, Any]) -> tuple[str, list[str], list[str]]:
    blockers, warnings = _common(packet, "RunGovernance")
    boundary = _m(packet.get("boundary"))
    payload = _m(packet.get("action_payload"))
    if packet:
        if boundary.get("does_not_run_runner") is not True:
            blockers.append("run_governance_runner_boundary_missing")
        if boundary.get("queue_gate_required") is not True:
            blockers.append("run_governance_queue_gate_boundary_missing")
        if boundary.get("exit_gate_required") is not True:
            blockers.append("run_governance_exit_gate_boundary_missing")
        if payload.get("run_allowed") is True:
            blockers.append("run_governance_stage_feedback_run_attempt")
        if payload.get("queue_gate_required") is not True:
            warnings.append("run_governance_queue_gate_payload_not_visible")
        if payload.get("exit_gate_required") is not True:
            warnings.append("run_governance_exit_gate_payload_not_visible")
    return _decision(blockers, warnings), blockers, warnings


def _packet(memory: Mapping[str, Any], plan: Mapping[str, Any], run: Mapping[str, Any]) -> dict[str, Any]:
    mem_dec, mem_block, mem_warn = _validate_memory(memory)
    plan_dec, plan_block, plan_warn = _validate_plan(plan)
    run_dec, run_block, run_warn = _validate_run(run)
    return {
        "version": "tri_os_stage_feedback_action_intake_decision_packet_v10_2",
        "tri_os_stage_feedback_action_intake_considered": True,
        "decisions": {
            "MemoryOS": {"decision": mem_dec, "blockers": mem_block, "warnings": mem_warn},
            "PlanOS": {"decision": plan_dec, "blockers": plan_block, "warnings": plan_warn},
            "RunGovernance": {"decision": run_dec, "blockers": run_block, "warnings": run_warn},
        },
        "source_digests": {
            "memory_stage_feedback_action": _sha(dict(memory)),
            "plan_stage_feedback_action": _sha(dict(plan)),
            "run_governance_stage_feedback_action": _sha(dict(run)),
        },
        "boundary": {
            "stage_feedback_action_intake_validation_only": True,
            "does_not_consume_memory": True,
            "does_not_commit_plan": True,
            "does_not_run_runner": True,
            "does_not_authorize_execution": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }


def build_tri_os_stage_feedback_action_intake_validator(*, runtime_context: Mapping[str, Any], stage_feedback_action_intake_license: Mapping[str, Any]) -> TriOSStageFeedbackActionIntakeValidatorResult:
    ctx = _m(runtime_context)
    lic = _m(stage_feedback_action_intake_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    memory_path = root / EXPECTED_FILES["MemoryOS"]
    plan_path = root / EXPECTED_FILES["PlanOS"]
    run_path = root / EXPECTED_FILES["RunGovernance"]
    packet_path = root / "tri_os_stage_feedback_action_intake_decision_packet.json"
    receipt_path = root / "tri_os_stage_feedback_action_intake_validator_receipt.json"
    audit_path = root / "tri_os_stage_feedback_action_intake_validator_audit.jsonl"

    if ctx.get("tri_os_stage_feedback_action_intake_validator_enabled") is not True:
        blockers.append("tri_os_stage_feedback_action_intake_validator_enabled_not_true")
    if ctx.get("apply_tri_os_stage_feedback_action_intake_validator") is not True:
        blockers.append("apply_tri_os_stage_feedback_action_intake_validator_not_true")
    if lic.get("license_status") != "TRI_OS_STAGE_FEEDBACK_ACTION_INTAKE_VALIDATOR_LICENSE_READY":
        blockers.append("tri_os_stage_feedback_action_intake_validator_license_not_ready")
    for name in ["stage_feedback_action_packets_read_allowed", "stage_feedback_action_intake_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    memory = _read_json(memory_path)
    plan = _read_json(plan_path)
    run = _read_json(run_path)
    packet: dict[str, Any] = {}
    written = False
    mem_dec = plan_dec = run_dec = "block"
    if not blockers:
        packet = _packet(memory, plan, run)
        if packet.get("boundary", {}).get("fail_closed_on_boundary_loss") is not True:
            blockers.append("stage_feedback_action_intake_fail_closed_boundary_missing")
        else:
            mem_dec = str(packet["decisions"]["MemoryOS"]["decision"])
            plan_dec = str(packet["decisions"]["PlanOS"]["decision"])
            run_dec = str(packet["decisions"]["RunGovernance"]["decision"])
            _write_json(packet_path, packet)
            written = True

    status = "TRI_OS_STAGE_FEEDBACK_ACTION_INTAKE_VALIDATOR_READY" if not blockers else "TRI_OS_STAGE_FEEDBACK_ACTION_INTAKE_VALIDATOR_BLOCKED"
    packet_id = "tri-os-stage-feedback-action-intake-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_tri_os_stage_feedback_action_intake_validator_v10_2",
        "status": status,
        "packet_id": packet_id,
        "memory_action_decision": mem_dec,
        "plan_action_decision": plan_dec,
        "run_governance_action_decision": run_dec,
        "action_intake_packet_written": written,
        "action_intake_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return TriOSStageFeedbackActionIntakeValidatorResult(
        "kuuos_runtime_daemon_tri_os_stage_feedback_action_intake_validator_v10_2",
        status,
        packet_id,
        str(root),
        mem_dec,
        plan_dec,
        run_dec,
        str(packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
