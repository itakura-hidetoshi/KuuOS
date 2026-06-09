#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


FEEDBACK_TO_REENTRY = {
    "process_tensor_feedback_reinforce_next_cycle": ("reentry_weighting_reinforce", "reinforce_path_weight"),
    "process_tensor_feedback_hold_context": ("reentry_weighting_hold", "open_probe_potential"),
    "process_tensor_feedback_block_context": ("reentry_weighting_block", "add_barrier_potential"),
}
REQUIRED_RECEIPT_BOUNDARY_FLAGS = (
    "receipt_ledger_only",
    "process_tensor_feedback_receipt_only",
    "non_markov_feedback_preserved",
    "history_window_feedback_preserved",
    "memory_kernel_feedback_preserved",
    "external_backaction_visible",
    "path_integral_feedback_traceable",
    "feedback_not_direct_truth",
    "feedback_not_unbounded_execution",
    "replayable_receipt",
    "fail_closed_on_boundary_loss",
)
REQUIRED_CONTEXT_KEYS = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)


@dataclass(frozen=True)
class PhysicalQuantumQiFeedbackToReentryWeightingBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    feedback_status: str
    reentry_weighting_status: str
    reentry_weighting_action: str
    path_weight_delta: int
    probe_potential_required: bool
    barrier_potential_required: bool
    reentry_weighting_packet_path: str
    reentry_weighting_state_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    reentry_weighting_packet_written: bool
    reentry_weighting_state_updated: bool
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


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _latest_jsonl(path: pathlib.Path, blockers: list[str]) -> dict[str, Any]:
    if not path.is_file():
        blockers.append("process_tensor_feedback_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("process_tensor_feedback_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("process_tensor_feedback_receipt_ledger_latest_line_invalid")
        return {}
    return value if isinstance(value, dict) else {}


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _validate_context(ctx: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    out = {key: str(ctx.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, value in out.items():
        if not value:
            blockers.append(f"process_tensor_context_{key}_missing")
    return out


def _validate_receipt(record: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], str, str, str]:
    if not record:
        return {}, "process_tensor_feedback_block_context", "reentry_weighting_block", "add_barrier_potential"
    if record.get("record_type") != "physical_quantum_qi_process_tensor_feedback_receipt":
        blockers.append("process_tensor_feedback_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"process_tensor_feedback_receipt_boundary_{name}_missing")
    feedback_status = str(record.get("feedback_status", "process_tensor_feedback_block_context"))
    if feedback_status not in FEEDBACK_TO_REENTRY:
        blockers.append("process_tensor_feedback_status_invalid")
        feedback_status = "process_tensor_feedback_block_context"
    reentry_status, action = FEEDBACK_TO_REENTRY[feedback_status]
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    path_delta = _int(record.get("path_weight_delta"))
    memory_weight = _int(record.get("memory_feedback_weight"))
    external_weight = _int(record.get("external_backaction_weight"))
    amp_delta = _int(record.get("next_cycle_amplitude_delta"))
    if feedback_status == "process_tensor_feedback_reinforce_next_cycle":
        if path_delta <= 0:
            blockers.append("reinforce_receipt_without_positive_path_weight_delta")
        if memory_weight <= 0:
            blockers.append("reinforce_receipt_without_memory_feedback_weight")
        if external_weight <= 0:
            blockers.append("reinforce_receipt_without_external_backaction_weight")
        if amp_delta <= 0:
            blockers.append("reinforce_receipt_without_next_cycle_amplitude_delta")
    elif feedback_status == "process_tensor_feedback_hold_context":
        if path_delta != 0 or memory_weight != 0 or external_weight != 0 or amp_delta != 0:
            blockers.append("hold_feedback_receipt_has_effect_weight")
    else:
        if path_delta >= 0:
            blockers.append("block_feedback_receipt_without_negative_path_weight_delta")
        if memory_weight != 0 or external_weight != 0 or amp_delta != 0:
            blockers.append("block_feedback_receipt_has_effect_weight")
    payload = {
        "feedback_status": feedback_status,
        "execution_status": str(record.get("execution_status", "")),
        "path_weight_delta": path_delta,
        "memory_feedback_weight": memory_weight,
        "external_backaction_weight": external_weight,
        "next_cycle_amplitude_delta": amp_delta,
        "process_tensor_context": context,
        "source_process_tensor_feedback_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_process_tensor_execution_feedback_digest": str(record.get("source_process_tensor_execution_feedback_digest", "")),
        "source_execution_record_digest": str(record.get("source_execution_record_digest", "")),
    }
    return payload, feedback_status, reentry_status, action


def _candidate_weighting(payload: Mapping[str, Any], action: str) -> dict[str, Any]:
    if action == "reinforce_path_weight":
        return {
            "path_weight_delta": _int(payload.get("path_weight_delta")),
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": _int(payload.get("memory_feedback_weight")),
            "external_backaction_weight": _int(payload.get("external_backaction_weight")),
            "next_cycle_amplitude_delta": _int(payload.get("next_cycle_amplitude_delta")),
        }
    if action == "open_probe_potential":
        return {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def build_physical_quantum_qi_feedback_to_reentry_weighting_bridge(
    *,
    runtime_context: Mapping[str, Any],
    feedback_to_reentry_weighting_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiFeedbackToReentryWeightingBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(feedback_to_reentry_weighting_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ledger_path = root / "physical_quantum_qi_process_tensor_feedback_receipt_ledger.jsonl"
    packet_path = root / "physical_quantum_qi_feedback_to_reentry_weighting_bridge_packet.json"
    state_path = root / "physical_quantum_qi_reentry_weighting_state.json"
    summary_path = root / "physical_quantum_qi_feedback_to_reentry_weighting_bridge_summary.json"
    receipt_path = root / "physical_quantum_qi_feedback_to_reentry_weighting_bridge_receipt.json"
    audit_path = root / "physical_quantum_qi_feedback_to_reentry_weighting_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_feedback_to_reentry_weighting_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_feedback_to_reentry_weighting_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_feedback_to_reentry_weighting_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_feedback_to_reentry_weighting_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_feedback_to_reentry_weighting_bridge_license_not_ready")
    for name in [
        "process_tensor_feedback_receipt_ledger_read_allowed",
        "reentry_weighting_bridge_packet_write_allowed",
        "reentry_weighting_state_write_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, feedback_status, reentry_status, action = _validate_receipt(_latest_jsonl(ledger_path, blockers), blockers)
    packet: dict[str, Any] = {}
    state: dict[str, Any] = {}
    written = state_updated = False
    if not blockers:
        weighting = _candidate_weighting(payload, action)
        epoch = int(time.time())
        packet = {
            "version": "physical_quantum_qi_feedback_to_reentry_weighting_bridge_packet_v12_9",
            "feedback_to_reentry_weighting_bridge_considered": True,
            "feedback_status": feedback_status,
            "reentry_weighting_status": reentry_status,
            "reentry_weighting_action": action,
            "candidate_weighting": weighting,
            "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
            "source_digests": {
                "process_tensor_feedback_receipt": str(payload.get("source_process_tensor_feedback_receipt_digest", "")),
                "process_tensor_execution_feedback": str(payload.get("source_process_tensor_execution_feedback_digest", "")),
                "execution_record": str(payload.get("source_execution_record_digest", "")),
            },
            "boundary": {
                "feedback_to_reentry_weighting_bridge_only": True,
                "process_tensor_feedback_required": True,
                "feeds_next_path_integral_reentry": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "external_backaction_visible": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_unbounded_execution": True,
                "license_gated_bridge": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        packet["feedback_to_reentry_weighting_bridge_digest"] = _sha(packet)
        _write_json(packet_path, packet)
        written = True
        state = {
            "version": "physical_quantum_qi_reentry_weighting_state_v12_9",
            "reentry_weighting_state_ready": True,
            "feedback_status": feedback_status,
            "reentry_weighting_status": reentry_status,
            "reentry_weighting_action": action,
            "candidate_weighting": weighting,
            "can_feed_next_path_integral_reentry": True,
            "source_feedback_to_reentry_weighting_bridge_digest": packet["feedback_to_reentry_weighting_bridge_digest"],
            "process_tensor_context": dict(packet["process_tensor_context"]),
            "boundary": {
                "reentry_weighting_state_only": True,
                "can_feed_next_path_integral_reentry": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
            },
            "epoch": epoch,
        }
        state["reentry_weighting_state_digest"] = _sha(state)
        _write_json(state_path, state)
        state_updated = True
        summary = {
            "version": "physical_quantum_qi_feedback_to_reentry_weighting_bridge_summary_v12_9",
            "feedback_status": feedback_status,
            "reentry_weighting_status": reentry_status,
            "reentry_weighting_action": action,
            "candidate_weighting": weighting,
            "feedback_to_reentry_weighting_bridge_digest": packet["feedback_to_reentry_weighting_bridge_digest"],
            "reentry_weighting_state_digest": state["reentry_weighting_state_digest"],
            "boundary": {
                "summary_only": True,
                "feedback_to_reentry_weighting_bridge_only": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    status = "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_BLOCKED"
    packet_id = "physical-quantum-qi-feedback-to-reentry-weighting-bridge-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_feedback_to_reentry_weighting_bridge_v12_9",
        "status": status,
        "packet_id": packet_id,
        "feedback_status": feedback_status,
        "reentry_weighting_status": reentry_status,
        "reentry_weighting_action": action,
        "reentry_weighting_packet_written": written,
        "reentry_weighting_state_updated": state_updated,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    weighting = _m(packet.get("candidate_weighting")) if packet else {}
    return PhysicalQuantumQiFeedbackToReentryWeightingBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_feedback_to_reentry_weighting_bridge_v12_9",
        status,
        packet_id,
        str(root),
        feedback_status,
        reentry_status,
        action,
        _int(weighting.get("path_weight_delta")),
        weighting.get("probe_potential_required") is True,
        weighting.get("barrier_potential_required") is True,
        str(packet_path),
        str(state_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        written,
        state_updated,
        blockers,
        warnings,
    )
