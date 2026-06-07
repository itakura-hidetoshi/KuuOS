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
FEEDBACK_MODES = {"open_next_stage", "request_more_evidence", "quarantine_or_repair"}


@dataclass(frozen=True)
class TriOSFeedbackActionEmitterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    memory_action_path: str
    plan_action_path: str
    run_governance_action_path: str
    receipt_path: str
    audit_path: str
    action_packets_written: int
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _m(value: object) -> Mapping[str, object]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _root(value: object, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, object]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _feedback(packet: Mapping[str, object], os_name: str) -> Mapping[str, object]:
    return _m(_m(packet.get("feedback")).get(os_name))


def _action_packet(packet: Mapping[str, object], os_name: str) -> dict[str, object]:
    feedback = _feedback(packet, os_name)
    mode = str(feedback.get("feedback_mode", "quarantine_or_repair"))
    action = str(feedback.get("feedback_action", "unknown"))
    base = {
        "version": "tri_os_feedback_action_packet_v9_3",
        "target_os": os_name,
        "feedback_mode": mode,
        "feedback_action": action,
        "source_feedback_digest": _sha(dict(packet)),
        "reason_window": feedback.get("reason_window", {}),
        "epoch": int(time.time()),
    }
    if os_name == "MemoryOS":
        base["action_payload"] = {
            "memory_operation": {
                "open_next_stage": "append_recall_anchor_candidate",
                "request_more_evidence": "reobserve_memory_anchor",
                "quarantine_or_repair": "quarantine_memory_handoff",
            }.get(mode, "quarantine_memory_handoff"),
            "allow_overwrite": False,
        }
        base["boundary"] = {
            "action_packet_only": True,
            "does_not_consume_memory": True,
            "does_not_overwrite_memory": True,
            "append_only_memory_required": True,
            "does_not_authorize_execution": True,
        }
    elif os_name == "PlanOS":
        base["action_payload"] = {
            "plan_operation": {
                "open_next_stage": "open_weighted_candidate_front",
                "request_more_evidence": "request_redecomposition_evidence",
                "quarantine_or_repair": "quarantine_plan_handoff",
            }.get(mode, "quarantine_plan_handoff"),
            "candidate_weighting_authority": "advisory_only",
        }
        base["boundary"] = {
            "action_packet_only": True,
            "does_not_commit_plan": True,
            "candidate_weighting_not_truth": True,
            "does_not_authorize_execution": True,
        }
    else:
        base["action_payload"] = {
            "run_governance_operation": {
                "open_next_stage": "open_bounded_queue_gate_candidate",
                "request_more_evidence": "request_exit_blocker_review",
                "quarantine_or_repair": "quarantine_governance_handoff",
            }.get(mode, "quarantine_governance_handoff"),
            "queue_gate_required": True,
            "exit_gate_required": True,
        }
        base["boundary"] = {
            "action_packet_only": True,
            "does_not_run_runner": True,
            "queue_gate_required": True,
            "exit_gate_required": True,
            "does_not_authorize_execution": True,
        }
    return base


def build_tri_os_feedback_action_emitter(*, runtime_context: Mapping[str, object], feedback_action_license: Mapping[str, object]) -> TriOSFeedbackActionEmitterResult:
    ctx = _m(runtime_context)
    lic = _m(feedback_action_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    feedback_path = root / "tri_os_intake_feedback_router_packet.json"
    memory_path = root / "memory_os_feedback_action_packet.json"
    plan_path = root / "plan_os_feedback_action_packet.json"
    run_path = root / "run_governance_feedback_action_packet.json"
    receipt_path = root / "tri_os_feedback_action_emitter_receipt.json"
    audit_path = root / "tri_os_feedback_action_emitter_audit.jsonl"

    if ctx.get("tri_os_feedback_action_emitter_enabled") is not True:
        blockers.append("tri_os_feedback_action_emitter_enabled_not_true")
    if ctx.get("apply_tri_os_feedback_action_emitter") is not True:
        blockers.append("apply_tri_os_feedback_action_emitter_not_true")
    if lic.get("license_status") != "TRI_OS_FEEDBACK_ACTION_EMITTER_LICENSE_READY":
        blockers.append("tri_os_feedback_action_emitter_license_not_ready")
    for name in ["feedback_packet_read_allowed", "memory_action_write_allowed", "plan_action_write_allowed", "run_governance_action_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    feedback_packet = _read_json(feedback_path)
    if not feedback_packet:
        blockers.append("tri_os_intake_feedback_router_packet_missing_or_invalid")
    elif feedback_packet.get("tri_os_intake_feedback_considered") is not True:
        blockers.append("tri_os_intake_feedback_considered_not_true")
    if feedback_packet and feedback_packet.get("boundary", {}).get("does_not_authorize_execution") is not True:
        blockers.append("feedback_router_execution_boundary_invalid")
    if feedback_packet:
        for os_name in OS_NAMES:
            mode = str(_feedback(feedback_packet, os_name).get("feedback_mode", "missing"))
            if mode not in FEEDBACK_MODES:
                blockers.append(f"{os_name.lower()}_feedback_mode_invalid")

    written = 0
    mem_packet: dict[str, object] = {}
    plan_packet: dict[str, object] = {}
    run_packet: dict[str, object] = {}
    if not blockers:
        mem_packet = _action_packet(feedback_packet, "MemoryOS")
        plan_packet = _action_packet(feedback_packet, "PlanOS")
        run_packet = _action_packet(feedback_packet, "RunGovernance")
        _write_json(memory_path, mem_packet)
        written += 1
        _write_json(plan_path, plan_packet)
        written += 1
        _write_json(run_path, run_packet)
        written += 1

    status = "TRI_OS_FEEDBACK_ACTION_EMITTER_READY" if not blockers else "TRI_OS_FEEDBACK_ACTION_EMITTER_BLOCKED"
    packet_id = "tri-os-feedback-action-" + _sha({"memory": mem_packet, "plan": plan_packet, "run": run_packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_tri_os_feedback_action_emitter_v9_3",
        "status": status,
        "packet_id": packet_id,
        "action_packets_written": written,
        "memory_action_digest": _sha(mem_packet),
        "plan_action_digest": _sha(plan_packet),
        "run_governance_action_digest": _sha(run_packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return TriOSFeedbackActionEmitterResult(
        "kuuos_runtime_daemon_tri_os_feedback_action_emitter_v9_3",
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
