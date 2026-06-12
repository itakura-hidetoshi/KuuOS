#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


EXPECTED_BY_HANDOFF = {
    "candidate_weighting_cycle_handoff_reinforce": ("reweight_candidate", "reinforce_admissible_candidate_seed"),
    "candidate_weighting_cycle_handoff_probe": ("hold_candidate", "probe_candidate_seed"),
    "candidate_weighting_cycle_handoff_barrier": ("block_candidate", "barrier_candidate_seed"),
}
REQUIRED_PACKET_BOUNDARY_FLAGS = (
    "candidate_weighting_cycle_handoff_only",
    "closed_loop_reentry_receipt_required",
    "hands_off_to_cycle_gate",
    "hands_off_to_admissible_candidate_set",
    "uses_process_tensor_feedback",
    "non_markov_feedback_preserved",
    "history_window_feedback_preserved",
    "memory_kernel_feedback_preserved",
    "external_backaction_visible",
    "candidate_weighting_not_truth",
    "handoff_not_direct_execution",
    "license_gated_handoff",
    "fail_closed_on_boundary_loss",
)
REQUIRED_GATE_BOUNDARY_FLAGS = (
    "cycle_gate_input_only",
    "from_closed_loop_reentry_handoff",
    "candidate_weighting_not_truth",
    "not_direct_execution_authority",
)
REQUIRED_SEED_BOUNDARY_FLAGS = (
    "admissible_candidate_set_seed_only",
    "from_closed_loop_reentry_handoff",
    "candidate_weighting_not_truth",
    "not_direct_execution_authority",
)
REQUIRED_CONTEXT_KEYS = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)


@dataclass(frozen=True)
class PhysicalQuantumQiV13_2ToV13_3HandoffReceiptBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_status: str
    handoff_status: str
    cycle_gate_decision: str
    admissible_candidate_seed_mode: str
    path_weight_delta: int
    probe_potential_required: bool
    barrier_potential_required: bool
    receipt_ready_state_written: bool
    bridge_ledger_appended: bool
    receipt_ready_state_path: str
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


def _normalize_weighting(weighting: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "path_weight_delta": _int(weighting.get("path_weight_delta")),
        "probe_potential_required": weighting.get("probe_potential_required") is True,
        "barrier_potential_required": weighting.get("barrier_potential_required") is True,
        "barrier_blocks_ready_weight": weighting.get("barrier_blocks_ready_weight") is True,
        "memory_feedback_weight": _int(weighting.get("memory_feedback_weight")),
        "external_backaction_weight": _int(weighting.get("external_backaction_weight")),
        "next_cycle_amplitude_delta": _int(weighting.get("next_cycle_amplitude_delta")),
    }


def _validate_weighting(handoff_status: str, weighting: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    norm = _normalize_weighting(weighting)
    if handoff_status == "candidate_weighting_cycle_handoff_reinforce":
        if norm["path_weight_delta"] <= 0 or norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_3_bridge_reinforce_weighting_invalid")
        if norm["memory_feedback_weight"] <= 0 or norm["external_backaction_weight"] <= 0 or norm["next_cycle_amplitude_delta"] <= 0:
            blockers.append("v13_3_bridge_reinforce_missing_process_tensor_effect_weight")
    elif handoff_status == "candidate_weighting_cycle_handoff_probe":
        if norm["path_weight_delta"] != 0 or not norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_3_bridge_probe_weighting_invalid")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("v13_3_bridge_probe_with_effect_weight")
    elif handoff_status == "candidate_weighting_cycle_handoff_barrier":
        if norm["path_weight_delta"] != 0 or norm["probe_potential_required"] or not norm["barrier_potential_required"] or not norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_3_bridge_barrier_weighting_invalid")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("v13_3_bridge_barrier_with_effect_weight")
    else:
        blockers.append("candidate_weighting_cycle_handoff_status_invalid")
    return norm


def _validate_packet(packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], str, str, str]:
    if not packet:
        blockers.append("candidate_weighting_cycle_handoff_packet_missing_or_invalid")
        return {}, "candidate_weighting_cycle_handoff_barrier", "block_candidate", "barrier_candidate_seed"
    if packet.get("candidate_weighting_cycle_handoff_considered") is not True:
        blockers.append("candidate_weighting_cycle_handoff_considered_not_true")
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_PACKET_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"candidate_weighting_cycle_handoff_boundary_{name}_missing")
    handoff_status = str(packet.get("handoff_status", "candidate_weighting_cycle_handoff_barrier"))
    if handoff_status not in EXPECTED_BY_HANDOFF:
        blockers.append("candidate_weighting_cycle_handoff_status_invalid")
        handoff_status = "candidate_weighting_cycle_handoff_barrier"
    expected_gate, expected_seed = EXPECTED_BY_HANDOFF[handoff_status]
    gate = str(packet.get("cycle_gate_decision", ""))
    seed = str(packet.get("admissible_candidate_seed_mode", ""))
    if gate != expected_gate:
        blockers.append("candidate_weighting_cycle_handoff_gate_decision_mismatch")
        gate = expected_gate
    if seed != expected_seed:
        blockers.append("candidate_weighting_cycle_handoff_seed_mode_mismatch")
        seed = expected_seed
    if not packet.get("candidate_weighting_cycle_handoff_digest"):
        warnings.append("candidate_weighting_cycle_handoff_digest_missing")
    context = _validate_context(_m(packet.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(handoff_status, _m(packet.get("candidate_weighting")), blockers)
    payload = {
        "handoff_status": handoff_status,
        "cycle_gate_decision": gate,
        "admissible_candidate_seed_mode": seed,
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_candidate_weighting_cycle_handoff_digest": str(packet.get("candidate_weighting_cycle_handoff_digest", _sha(dict(packet)))),
        "source_closed_loop_reentry_receipt_digest": str(_m(packet.get("source_digests")).get("closed_loop_reentry_receipt", "")),
        "source_closed_loop_path_integral_reentry_digest": str(_m(packet.get("source_digests")).get("closed_loop_path_integral_reentry", "")),
    }
    return payload, handoff_status, gate, seed


def _validate_gate(gate_payload: Mapping[str, Any], payload: Mapping[str, Any], blockers: list[str]) -> None:
    if not gate_payload:
        blockers.append("next_cycle_gate_input_missing_or_invalid")
        return
    if gate_payload.get("cycle_gate_input_ready") is not True:
        blockers.append("next_cycle_gate_input_not_ready")
    if str(gate_payload.get("cycle_gate_decision", "")) != payload.get("cycle_gate_decision"):
        blockers.append("next_cycle_gate_input_decision_mismatch")
    if _normalize_weighting(_m(gate_payload.get("candidate_weighting"))) != payload.get("candidate_weighting"):
        blockers.append("next_cycle_gate_input_weighting_mismatch")
    if str(gate_payload.get("source_candidate_weighting_cycle_handoff_digest", "")) != payload.get("source_candidate_weighting_cycle_handoff_digest"):
        blockers.append("next_cycle_gate_input_source_digest_mismatch")
    boundary = _m(gate_payload.get("boundary"))
    for name in REQUIRED_GATE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"next_cycle_gate_input_boundary_{name}_missing")


def _validate_seed(seed_payload: Mapping[str, Any], payload: Mapping[str, Any], blockers: list[str]) -> None:
    if not seed_payload:
        blockers.append("admissible_candidate_set_seed_missing_or_invalid")
        return
    if seed_payload.get("admissible_candidate_set_seed_ready") is not True:
        blockers.append("admissible_candidate_set_seed_not_ready")
    if str(seed_payload.get("admissible_candidate_seed_mode", "")) != payload.get("admissible_candidate_seed_mode"):
        blockers.append("admissible_candidate_set_seed_mode_mismatch")
    if _normalize_weighting(_m(seed_payload.get("candidate_weighting"))) != payload.get("candidate_weighting"):
        blockers.append("admissible_candidate_set_seed_weighting_mismatch")
    if str(seed_payload.get("source_candidate_weighting_cycle_handoff_digest", "")) != payload.get("source_candidate_weighting_cycle_handoff_digest"):
        blockers.append("admissible_candidate_set_seed_source_digest_mismatch")
    boundary = _m(seed_payload.get("boundary"))
    for name in REQUIRED_SEED_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"admissible_candidate_set_seed_boundary_{name}_missing")


def build_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge(
    *,
    runtime_context: Mapping[str, Any],
    v13_2_to_v13_3_handoff_receipt_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_2ToV13_3HandoffReceiptBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(v13_2_to_v13_3_handoff_receipt_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json"
    gate_path = root / "physical_quantum_qi_next_cycle_gate_input.json"
    seed_path = root / "physical_quantum_qi_admissible_candidate_set_seed.json"
    ready_state_path = root / "physical_quantum_qi_v13_3_candidate_weighting_cycle_handoff_receipt_ready_state.json"
    bridge_ledger_path = root / "physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_summary.json"
    receipt_path = root / "physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_license_not_ready")
    for name in [
        "v13_2_handoff_packet_read_allowed",
        "v13_2_cycle_gate_input_read_allowed",
        "v13_2_admissible_candidate_set_seed_read_allowed",
        "v13_3_handoff_receipt_ready_state_write_allowed",
        "bridge_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, handoff_status, gate, seed = _validate_packet(_read_json(packet_path), blockers, warnings)
    _validate_gate(_read_json(gate_path), payload, blockers)
    _validate_seed(_read_json(seed_path), payload, blockers)
    ready_written = ledger_appended = False
    bridge_status = "v13_2_to_v13_3_handoff_receipt_bridge_block"
    weighting: dict[str, Any] = dict(_m(payload.get("candidate_weighting"))) if payload else {}
    if not blockers:
        epoch = int(time.time())
        bridge_status = "v13_2_to_v13_3_handoff_receipt_bridge_" + handoff_status.rsplit("_", 1)[-1]
        ready_state = {
            "version": "physical_quantum_qi_v13_3_candidate_weighting_cycle_handoff_receipt_ready_state_v13_15",
            "candidate_weighting_cycle_handoff_receipt_ready_state": True,
            "bridge_status": bridge_status,
            "handoff_status": handoff_status,
            "cycle_gate_decision": gate,
            "admissible_candidate_seed_mode": seed,
            "candidate_weighting": weighting,
            "source_candidate_weighting_cycle_handoff_digest": payload["source_candidate_weighting_cycle_handoff_digest"],
            "source_closed_loop_reentry_receipt_digest": payload["source_closed_loop_reentry_receipt_digest"],
            "source_closed_loop_path_integral_reentry_digest": payload["source_closed_loop_path_integral_reentry_digest"],
            "process_tensor_context": dict(payload["process_tensor_context"]),
            "boundary": {
                "v13_3_handoff_receipt_ready_state_only": True,
                "v13_2_handoff_packet_required": True,
                "v13_2_cycle_gate_input_required": True,
                "v13_2_admissible_candidate_set_seed_required": True,
                "can_feed_v13_3_candidate_weighting_cycle_handoff_receipt_ledger": True,
                "cycle_gate_input_traceable": True,
                "admissible_candidate_set_seed_traceable": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "external_backaction_visible": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_receipt_append": True,
                "does_not_run_receipt_ledger": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        ready_state["handoff_receipt_ready_state_digest"] = _sha(ready_state)
        _write_json(ready_state_path, ready_state)
        ready_written = True
        record = {
            "version": "physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_record_v13_15",
            "record_type": "physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge",
            "bridge_status": bridge_status,
            "handoff_status": handoff_status,
            "cycle_gate_decision": gate,
            "admissible_candidate_seed_mode": seed,
            "source_handoff_receipt_ready_state_digest": ready_state["handoff_receipt_ready_state_digest"],
            "source_candidate_weighting_cycle_handoff_digest": payload["source_candidate_weighting_cycle_handoff_digest"],
            "prev_record_digest": _last_digest(bridge_ledger_path),
            "boundary": {
                "bridge_receipt_only": True,
                "v13_3_handoff_receipt_ready_state_traceable": True,
                "cycle_gate_input_traceable": True,
                "admissible_candidate_set_seed_traceable": True,
                "same_semantic_root": True,
                "uses_process_tensor_feedback": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_execution": True,
                "replayable_receipt": True,
            },
            "epoch": epoch,
        }
        record["record_digest"] = _sha(record)
        _append_jsonl(bridge_ledger_path, record)
        ledger_appended = True
        summary = {
            "version": "physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_summary_v13_15",
            "bridge_status": bridge_status,
            "handoff_status": handoff_status,
            "cycle_gate_decision": gate,
            "admissible_candidate_seed_mode": seed,
            "handoff_receipt_ready_state_digest": ready_state["handoff_receipt_ready_state_digest"],
            "boundary": {
                "summary_only": True,
                "can_feed_v13_3_candidate_weighting_cycle_handoff_receipt_ledger": True,
                "cycle_gate_input_traceable": True,
                "admissible_candidate_set_seed_traceable": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    final_status = "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_BLOCKED"
    packet_id = "physical-quantum-qi-v13-2-to-v13-3-handoff-receipt-bridge-" + _sha({"payload": payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_v13_15",
        "status": final_status,
        "packet_id": packet_id,
        "bridge_status": bridge_status,
        "handoff_status": handoff_status,
        "cycle_gate_decision": gate,
        "admissible_candidate_seed_mode": seed,
        "receipt_ready_state_written": ready_written,
        "bridge_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiV13_2ToV13_3HandoffReceiptBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_v13_15",
        final_status,
        packet_id,
        str(root),
        bridge_status,
        handoff_status,
        gate,
        seed,
        _int(weighting.get("path_weight_delta")),
        weighting.get("probe_potential_required") is True,
        weighting.get("barrier_potential_required") is True,
        ready_written,
        ledger_appended,
        str(ready_state_path),
        str(bridge_ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
