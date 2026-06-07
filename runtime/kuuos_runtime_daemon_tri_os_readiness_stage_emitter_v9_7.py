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
READINESS_VALUES = {"ready", "needs_evidence", "repair_required"}


@dataclass(frozen=True)
class TriOSReadinessStageEmitterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    memory_stage_path: str
    plan_stage_path: str
    run_governance_stage_path: str
    receipt_path: str
    audit_path: str
    stage_packets_written: int
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


def _readiness(packet: Mapping[str, Any], os_name: str) -> Mapping[str, Any]:
    return _m(_m(packet.get("readiness")).get(os_name))


def _stage_mode(readiness: str) -> str:
    return {"ready": "stage_candidate", "needs_evidence": "stage_reobserve_request", "repair_required": "stage_repair_quarantine"}.get(readiness, "stage_repair_quarantine")


def _stage_packet(packet: Mapping[str, Any], os_name: str) -> dict[str, Any]:
    item = _readiness(packet, os_name)
    readiness = str(item.get("readiness", "repair_required"))
    next_stage_action = str(item.get("next_stage_action", "unknown"))
    base = {
        "version": "tri_os_readiness_stage_packet_v9_7",
        "target_os": os_name,
        "readiness": readiness,
        "stage_mode": _stage_mode(readiness),
        "next_stage_action": next_stage_action,
        "source_readiness_digest": _sha(dict(packet)),
        "history": item.get("history", {}),
        "epoch": int(time.time()),
    }
    if os_name == "MemoryOS":
        base["stage_payload"] = {
            "memory_stage": next_stage_action,
            "append_only_required": True,
            "allow_overwrite": False,
        }
        base["boundary"] = {
            "stage_packet_only": True,
            "does_not_consume_memory": True,
            "does_not_overwrite_memory": True,
            "append_only_memory_required": True,
            "does_not_authorize_execution": True,
            "repair_required_blocks_ready_state": readiness == "repair_required",
        }
    elif os_name == "PlanOS":
        base["stage_payload"] = {
            "plan_stage": next_stage_action,
            "candidate_weighting_authority": "advisory_only",
            "commit_allowed": False,
        }
        base["boundary"] = {
            "stage_packet_only": True,
            "does_not_commit_plan": True,
            "candidate_weighting_not_truth": True,
            "does_not_authorize_execution": True,
            "repair_required_blocks_ready_state": readiness == "repair_required",
        }
    else:
        base["stage_payload"] = {
            "run_governance_stage": next_stage_action,
            "queue_gate_required": True,
            "exit_gate_required": True,
            "run_allowed": False,
        }
        base["boundary"] = {
            "stage_packet_only": True,
            "does_not_run_runner": True,
            "queue_gate_required": True,
            "exit_gate_required": True,
            "does_not_authorize_execution": True,
            "repair_required_blocks_ready_state": readiness == "repair_required",
        }
    return base


def build_tri_os_readiness_stage_emitter(*, runtime_context: Mapping[str, Any], readiness_stage_license: Mapping[str, Any]) -> TriOSReadinessStageEmitterResult:
    ctx = _m(runtime_context)
    lic = _m(readiness_stage_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    readiness_path = root / "tri_os_feedback_action_readiness_router_packet.json"
    memory_path = root / "memory_os_readiness_stage_packet.json"
    plan_path = root / "plan_os_readiness_stage_packet.json"
    run_path = root / "run_governance_readiness_stage_packet.json"
    receipt_path = root / "tri_os_readiness_stage_emitter_receipt.json"
    audit_path = root / "tri_os_readiness_stage_emitter_audit.jsonl"

    if ctx.get("tri_os_readiness_stage_emitter_enabled") is not True:
        blockers.append("tri_os_readiness_stage_emitter_enabled_not_true")
    if ctx.get("apply_tri_os_readiness_stage_emitter") is not True:
        blockers.append("apply_tri_os_readiness_stage_emitter_not_true")
    if lic.get("license_status") != "TRI_OS_READINESS_STAGE_EMITTER_LICENSE_READY":
        blockers.append("tri_os_readiness_stage_emitter_license_not_ready")
    for name in ["readiness_packet_read_allowed", "memory_stage_write_allowed", "plan_stage_write_allowed", "run_governance_stage_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    readiness_packet = _read_json(readiness_path)
    if not readiness_packet:
        blockers.append("tri_os_feedback_action_readiness_router_packet_missing_or_invalid")
    elif readiness_packet.get("tri_os_feedback_action_readiness_considered") is not True:
        blockers.append("tri_os_feedback_action_readiness_considered_not_true")
    if readiness_packet and readiness_packet.get("boundary", {}).get("readiness_only") is not True:
        blockers.append("readiness_only_boundary_invalid")
    if readiness_packet and readiness_packet.get("boundary", {}).get("does_not_authorize_execution") is not True:
        blockers.append("readiness_execution_boundary_invalid")
    if readiness_packet:
        for os_name in OS_NAMES:
            value = str(_readiness(readiness_packet, os_name).get("readiness", "missing"))
            if value not in READINESS_VALUES:
                blockers.append(f"{os_name.lower()}_readiness_invalid")

    written = 0
    mem_packet: dict[str, Any] = {}
    plan_packet: dict[str, Any] = {}
    run_packet: dict[str, Any] = {}
    if not blockers:
        mem_packet = _stage_packet(readiness_packet, "MemoryOS")
        plan_packet = _stage_packet(readiness_packet, "PlanOS")
        run_packet = _stage_packet(readiness_packet, "RunGovernance")
        _write_json(memory_path, mem_packet)
        written += 1
        _write_json(plan_path, plan_packet)
        written += 1
        _write_json(run_path, run_packet)
        written += 1

    status = "TRI_OS_READINESS_STAGE_EMITTER_READY" if not blockers else "TRI_OS_READINESS_STAGE_EMITTER_BLOCKED"
    packet_id = "tri-os-readiness-stage-" + _sha({"memory": mem_packet, "plan": plan_packet, "run": run_packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_tri_os_readiness_stage_emitter_v9_7",
        "status": status,
        "packet_id": packet_id,
        "stage_packets_written": written,
        "memory_stage_digest": _sha(mem_packet),
        "plan_stage_digest": _sha(plan_packet),
        "run_governance_stage_digest": _sha(run_packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return TriOSReadinessStageEmitterResult(
        "kuuos_runtime_daemon_tri_os_readiness_stage_emitter_v9_7",
        status,
        packet_id,
        str(root),
        str(memory_path),
        str(plan_path),
        str(run_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
