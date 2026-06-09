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
    "process_tensor_feedback_reinforce_next_cycle": ("guarded_transition_executed", "reentry_weighting_reinforce", "reinforce_path_weight"),
    "process_tensor_feedback_hold_context": ("guarded_transition_hold", "reentry_weighting_hold", "open_probe_potential"),
    "process_tensor_feedback_block_context": ("guarded_transition_block", "reentry_weighting_block", "add_barrier_potential"),
}
REQUIRED_PACKET_BOUNDARY_FLAGS = (
    "process_tensor_execution_feedback_only",
    "uses_execution_effects_as_non_markov_feedback",
    "feeds_path_integral_weighting",
    "history_window_feedback_required",
    "memory_kernel_feedback_required",
    "external_backaction_visible",
    "feedback_not_direct_truth",
    "feedback_not_unbounded_execution",
    "runtime_local_feedback_only",
    "fail_closed_on_boundary_loss",
)
REQUIRED_STATE_BOUNDARY_FLAGS = (
    "path_integral_feedback_state_only",
    "non_markov_feedback_preserved",
    "feedback_not_direct_authority",
)
REQUIRED_KERNEL_FLAGS = (
    "non_markov_feedback_required",
    "history_window_feedback_required",
    "instrument_trace_feedback_required",
    "process_tensor_feedback_not_truth",
)
REQUIRED_CONTEXT_KEYS = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)


@dataclass(frozen=True)
class PhysicalQuantumQiV12_7ToV12_8FeedbackReceiptBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_status: str
    feedback_status: str
    execution_status: str
    expected_v12_9_reentry_weighting_status: str
    expected_v12_9_reentry_weighting_action: str
    path_weight_delta: int
    memory_feedback_weight: int
    external_backaction_weight: int
    next_cycle_amplitude_delta: int
    feedback_receipt_ready_state_written: bool
    bridge_ledger_appended: bool
    feedback_receipt_ready_state_path: str
    bridge_ledger_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
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


def _last_digest(path: pathlib.Path) -> str:
    if not path.is_file():
        return "GENESIS"
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        return "GENESIS"
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        return "CORRUPT_PREVIOUS_LEDGER_LINE"
    return str(value.get("record_digest", _sha(value)))


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


def _validate_packet(packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], str, str, str, str]:
    if not packet:
        blockers.append("v12_7_process_tensor_execution_feedback_packet_missing_or_invalid")
        return {}, "process_tensor_feedback_block_context", "guarded_transition_block", "reentry_weighting_block", "add_barrier_potential"
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_PACKET_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"v12_7_process_tensor_feedback_boundary_{name}_missing")
    feedback_status = str(packet.get("feedback_status", "process_tensor_feedback_block_context"))
    if feedback_status not in FEEDBACK_TO_REENTRY:
        blockers.append("v12_7_process_tensor_feedback_status_invalid")
        feedback_status = "process_tensor_feedback_block_context"
    expected_execution, reentry_status, action = FEEDBACK_TO_REENTRY[feedback_status]
    execution_status = str(packet.get("execution_status", ""))
    if execution_status != expected_execution:
        blockers.append("v12_7_process_tensor_feedback_execution_status_mismatch")
    kernel = dict(_m(packet.get("process_tensor_feedback_kernel")))
    for name in REQUIRED_KERNEL_FLAGS:
        if kernel.get(name) is not True:
            blockers.append(f"v12_7_process_tensor_feedback_kernel_{name}_missing")
    observed = dict(_m(packet.get("observed_effects")))
    path_delta = _int(kernel.get("path_weight_delta"))
    memory_weight = _int(kernel.get("memory_feedback_weight"))
    external_weight = _int(kernel.get("external_backaction_weight"))
    amp_delta = _int(kernel.get("next_cycle_amplitude_delta"))
    if feedback_status == "process_tensor_feedback_reinforce_next_cycle":
        if path_delta <= 0:
            blockers.append("v12_8_bridge_reinforce_without_positive_path_weight_delta")
        if memory_weight <= 0:
            blockers.append("v12_8_bridge_reinforce_without_memory_feedback_weight")
        if external_weight <= 0:
            blockers.append("v12_8_bridge_reinforce_without_external_backaction_weight")
        if amp_delta <= 0:
            blockers.append("v12_8_bridge_reinforce_without_next_cycle_amplitude_delta")
        for key in ["next_cycle_observed", "memory_feedback_observed", "external_backaction_observed"]:
            if observed.get(key) is not True:
                blockers.append(f"v12_8_bridge_reinforce_{key}_not_true")
    elif feedback_status == "process_tensor_feedback_hold_context":
        if path_delta != 0 or memory_weight != 0 or external_weight != 0 or amp_delta != 0:
            blockers.append("v12_8_bridge_hold_feedback_has_effect_weight")
    else:
        if path_delta >= 0:
            blockers.append("v12_8_bridge_block_feedback_without_negative_path_weight_delta")
        if memory_weight != 0 or external_weight != 0 or amp_delta != 0:
            blockers.append("v12_8_bridge_block_feedback_has_effect_weight")
    if not packet.get("process_tensor_execution_feedback_digest"):
        warnings.append("v12_7_process_tensor_execution_feedback_digest_missing")
    payload = {
        "feedback_status": feedback_status,
        "execution_status": execution_status,
        "expected_v12_9_reentry_weighting_status": reentry_status,
        "expected_v12_9_reentry_weighting_action": action,
        "path_weight_delta": path_delta,
        "memory_feedback_weight": memory_weight,
        "external_backaction_weight": external_weight,
        "next_cycle_amplitude_delta": amp_delta,
        "process_tensor_feedback_kernel": kernel,
        "observed_effects": observed,
        "process_tensor_context": _validate_context(_m(packet.get("process_tensor_context")), blockers),
        "source_process_tensor_execution_feedback_digest": str(packet.get("process_tensor_execution_feedback_digest", _sha(dict(packet)))),
        "source_execution_record_digest": str(_m(packet.get("source_digests")).get("execution_record", "")),
        "source_next_cycle_state_digest": str(_m(packet.get("source_digests")).get("next_cycle_state", "")),
        "source_memory_consumption_digest": str(_m(packet.get("source_digests")).get("memory_consumption", "")),
        "source_external_state_mutation_digest": str(_m(packet.get("source_digests")).get("external_state_mutation", "")),
    }
    return payload, feedback_status, expected_execution, reentry_status, action


def _validate_state(state: Mapping[str, Any], payload: Mapping[str, Any], blockers: list[str]) -> None:
    if not state:
        blockers.append("v12_7_path_integral_feedback_state_missing_or_invalid")
        return
    if state.get("path_integral_feedback_ready") is not True:
        blockers.append("v12_7_path_integral_feedback_state_not_ready")
    if str(state.get("feedback_status", "")) != payload.get("feedback_status"):
        blockers.append("v12_7_path_integral_feedback_state_status_mismatch")
    for key in ["path_weight_delta", "memory_feedback_weight", "external_backaction_weight", "next_cycle_amplitude_delta"]:
        if _int(state.get(key)) != _int(payload.get(key)):
            blockers.append(f"v12_7_path_integral_feedback_state_{key}_mismatch")
    if str(state.get("source_process_tensor_execution_feedback_digest", "")) != payload.get("source_process_tensor_execution_feedback_digest"):
        blockers.append("v12_7_path_integral_feedback_state_source_digest_mismatch")
    boundary = _m(state.get("boundary"))
    for name in REQUIRED_STATE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"v12_7_path_integral_feedback_state_boundary_{name}_missing")
    reinforce = payload.get("feedback_status") == "process_tensor_feedback_reinforce_next_cycle"
    if boundary.get("can_feed_next_path_integral_cycle") is not reinforce:
        blockers.append("v12_7_path_integral_feedback_state_can_feed_next_cycle_mismatch")


def build_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge(
    *,
    runtime_context: Mapping[str, Any],
    v12_7_to_v12_8_feedback_receipt_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiV12_7ToV12_8FeedbackReceiptBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(v12_7_to_v12_8_feedback_receipt_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_process_tensor_execution_feedback_packet.json"
    state_path = root / "physical_quantum_qi_path_integral_feedback_state.json"
    ready_state_path = root / "physical_quantum_qi_v12_8_process_tensor_feedback_receipt_ready_state.json"
    bridge_ledger_path = root / "physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_summary.json"
    receipt_path = root / "physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_receipt.json"
    audit_path = root / "physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_license_not_ready")
    for name in [
        "v12_7_process_tensor_feedback_packet_read_allowed",
        "v12_7_path_integral_feedback_state_read_allowed",
        "v12_8_feedback_receipt_ready_state_write_allowed",
        "bridge_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, feedback_status, execution_status, reentry_status, action = _validate_packet(_read_json(packet_path), blockers, warnings)
    _validate_state(_read_json(state_path), payload, blockers)
    state_written = ledger_appended = False
    bridge_status = "v12_7_to_v12_8_feedback_receipt_bridge_block"
    if not blockers:
        epoch = int(time.time())
        bridge_status = "v12_7_to_v12_8_feedback_receipt_bridge_" + feedback_status.rsplit("_", 1)[-1]
        ready_state = {
            "version": "physical_quantum_qi_v12_8_process_tensor_feedback_receipt_ready_state_v13_11",
            "process_tensor_feedback_receipt_ready_state": True,
            "bridge_status": bridge_status,
            "feedback_status": feedback_status,
            "execution_status": execution_status,
            "expected_v12_9_reentry_weighting_status": reentry_status,
            "expected_v12_9_reentry_weighting_action": action,
            "path_weight_delta": payload["path_weight_delta"],
            "memory_feedback_weight": payload["memory_feedback_weight"],
            "external_backaction_weight": payload["external_backaction_weight"],
            "next_cycle_amplitude_delta": payload["next_cycle_amplitude_delta"],
            "source_process_tensor_execution_feedback_digest": payload["source_process_tensor_execution_feedback_digest"],
            "process_tensor_context": dict(payload["process_tensor_context"]),
            "boundary": {
                "v12_8_feedback_receipt_ready_state_only": True,
                "v12_7_process_tensor_feedback_packet_required": True,
                "v12_7_path_integral_feedback_state_required": True,
                "can_feed_v12_8_process_tensor_feedback_receipt_ledger": True,
                "can_feed_v12_9_feedback_to_reentry_weighting_bridge_after_receipt": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "external_backaction_visible": True,
                "feedback_not_direct_truth": True,
                "bridge_not_direct_receipt_append": True,
                "does_not_run_receipt_ledger": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        ready_state["feedback_receipt_ready_state_digest"] = _sha(ready_state)
        _write_json(ready_state_path, ready_state)
        state_written = True
        record = {
            "version": "physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_record_v13_11",
            "record_type": "physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge",
            "bridge_status": bridge_status,
            "feedback_status": feedback_status,
            "execution_status": execution_status,
            "expected_v12_9_reentry_weighting_status": reentry_status,
            "expected_v12_9_reentry_weighting_action": action,
            "source_feedback_receipt_ready_state_digest": ready_state["feedback_receipt_ready_state_digest"],
            "source_process_tensor_execution_feedback_digest": payload["source_process_tensor_execution_feedback_digest"],
            "prev_record_digest": _last_digest(bridge_ledger_path),
            "boundary": {
                "bridge_receipt_only": True,
                "v12_8_feedback_receipt_ready_state_traceable": True,
                "same_semantic_root": True,
                "non_markov_feedback_preserved": True,
                "feedback_not_direct_truth": True,
                "bridge_not_direct_execution": True,
                "replayable_receipt": True,
            },
            "epoch": epoch,
        }
        record["record_digest"] = _sha(record)
        _append_jsonl(bridge_ledger_path, record)
        ledger_appended = True
        summary = {
            "version": "physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_summary_v13_11",
            "bridge_status": bridge_status,
            "feedback_status": feedback_status,
            "execution_status": execution_status,
            "expected_v12_9_reentry_weighting_status": reentry_status,
            "expected_v12_9_reentry_weighting_action": action,
            "feedback_receipt_ready_state_digest": ready_state["feedback_receipt_ready_state_digest"],
            "boundary": {
                "summary_only": True,
                "can_feed_v12_8_process_tensor_feedback_receipt_ledger": True,
                "can_feed_v12_9_feedback_to_reentry_weighting_bridge_after_receipt": True,
                "feedback_not_direct_truth": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    final_status = "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_BLOCKED"
    packet_id = "physical-quantum-qi-v12-7-to-v12-8-feedback-receipt-bridge-" + _sha({"payload": payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_v13_11",
        "status": final_status,
        "packet_id": packet_id,
        "bridge_status": bridge_status,
        "feedback_status": feedback_status,
        "execution_status": execution_status,
        "expected_v12_9_reentry_weighting_status": reentry_status,
        "expected_v12_9_reentry_weighting_action": action,
        "feedback_receipt_ready_state_written": state_written,
        "bridge_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiV12_7ToV12_8FeedbackReceiptBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_v13_11",
        final_status,
        packet_id,
        str(root),
        bridge_status,
        feedback_status,
        execution_status,
        reentry_status,
        action,
        int(payload.get("path_weight_delta", 0)) if payload else 0,
        int(payload.get("memory_feedback_weight", 0)) if payload else 0,
        int(payload.get("external_backaction_weight", 0)) if payload else 0,
        int(payload.get("next_cycle_amplitude_delta", 0)) if payload else 0,
        state_written,
        ledger_appended,
        str(ready_state_path),
        str(bridge_ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
