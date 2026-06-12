#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


HANDOFF = {
    "closed_loop_reentry_reinforced": ("reinforce_path_weight", "candidate_weighting_cycle_handoff_reinforce", "reweight_candidate", "reinforce_admissible_candidate_seed"),
    "closed_loop_reentry_probe_opened": ("open_probe_potential", "candidate_weighting_cycle_handoff_probe", "hold_candidate", "probe_candidate_seed"),
    "closed_loop_reentry_barrier_added": ("add_barrier_potential", "candidate_weighting_cycle_handoff_barrier", "block_candidate", "barrier_candidate_seed"),
}
REQUIRED_RECEIPT_BOUNDARY_FLAGS = (
    "receipt_ledger_only",
    "closed_loop_reentry_receipt_only",
    "candidate_weighting_cycle_traceable",
    "uses_process_tensor_feedback",
    "non_markov_feedback_preserved",
    "history_window_feedback_preserved",
    "memory_kernel_feedback_preserved",
    "external_backaction_visible",
    "candidate_weighting_not_truth",
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
class PhysicalQuantumQiV13_1ToV13_2CycleHandoffBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_status: str
    closed_loop_reentry_status: str
    reentry_weighting_action: str
    expected_v13_2_handoff_status: str
    expected_v13_2_cycle_gate_decision: str
    expected_v13_2_admissible_candidate_seed_mode: str
    path_weight_delta: int
    probe_potential_required: bool
    barrier_potential_required: bool
    handoff_ready_state_written: bool
    bridge_ledger_appended: bool
    handoff_ready_state_path: str
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
        blockers.append("closed_loop_reentry_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("closed_loop_reentry_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("closed_loop_reentry_receipt_ledger_latest_line_invalid")
        return {}
    return value if isinstance(value, dict) else {}


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


def _validate_weighting(status: str, weighting: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    norm = _normalize_weighting(weighting)
    if status == "closed_loop_reentry_reinforced":
        if norm["path_weight_delta"] <= 0:
            blockers.append("v13_2_bridge_reinforce_without_positive_path_weight_delta")
        if norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_2_bridge_reinforce_with_probe_or_barrier")
        if norm["memory_feedback_weight"] <= 0 or norm["external_backaction_weight"] <= 0 or norm["next_cycle_amplitude_delta"] <= 0:
            blockers.append("v13_2_bridge_reinforce_missing_process_tensor_effect_weight")
    elif status == "closed_loop_reentry_probe_opened":
        if norm["path_weight_delta"] != 0 or not norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_2_bridge_probe_weighting_invalid")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("v13_2_bridge_probe_with_effect_weight")
    elif status == "closed_loop_reentry_barrier_added":
        if norm["path_weight_delta"] != 0 or norm["probe_potential_required"] or not norm["barrier_potential_required"] or not norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_2_bridge_barrier_weighting_invalid")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("v13_2_bridge_barrier_with_effect_weight")
    else:
        blockers.append("closed_loop_reentry_status_invalid")
    return norm


def _validate_receipt(record: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], str, str, str, str, str]:
    if not record:
        return {}, "closed_loop_reentry_barrier_added", "add_barrier_potential", "candidate_weighting_cycle_handoff_barrier", "block_candidate", "barrier_candidate_seed"
    if record.get("record_type") != "physical_quantum_qi_closed_loop_reentry_receipt":
        blockers.append("closed_loop_reentry_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"closed_loop_reentry_receipt_boundary_{name}_missing")
    closed_status = str(record.get("closed_loop_reentry_status", "closed_loop_reentry_barrier_added"))
    if closed_status not in HANDOFF:
        blockers.append("closed_loop_reentry_status_invalid")
        closed_status = "closed_loop_reentry_barrier_added"
    expected_action, handoff_status, cycle_decision, seed_mode = HANDOFF[closed_status]
    action = str(record.get("reentry_weighting_action", "add_barrier_potential"))
    if action != expected_action:
        blockers.append("closed_loop_reentry_action_mismatch")
        action = expected_action
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(closed_status, _m(record.get("candidate_weighting")), blockers)
    payload = {
        "closed_loop_reentry_status": closed_status,
        "reentry_weighting_action": action,
        "expected_v13_2_handoff_status": handoff_status,
        "expected_v13_2_cycle_gate_decision": cycle_decision,
        "expected_v13_2_admissible_candidate_seed_mode": seed_mode,
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_closed_loop_reentry_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_closed_loop_path_integral_reentry_digest": str(record.get("source_closed_loop_path_integral_reentry_digest", "")),
    }
    return payload, closed_status, action, handoff_status, cycle_decision, seed_mode


def build_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge(
    *,
    runtime_context: Mapping[str, Any],
    v13_1_to_v13_2_cycle_handoff_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_1ToV13_2CycleHandoffBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(v13_1_to_v13_2_cycle_handoff_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_ledger_path = root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl"
    ready_state_path = root / "physical_quantum_qi_v13_2_candidate_weighting_cycle_handoff_ready_state.json"
    bridge_ledger_path = root / "physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_summary.json"
    receipt_path = root / "physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_license_not_ready")
    for name in [
        "v13_1_closed_loop_reentry_receipt_ledger_read_allowed",
        "v13_2_handoff_ready_state_write_allowed",
        "bridge_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, closed_status, action, handoff_status, cycle_decision, seed_mode = _validate_receipt(_latest_jsonl(receipt_ledger_path, blockers), blockers)
    ready_written = ledger_appended = False
    bridge_status = "v13_1_to_v13_2_cycle_handoff_bridge_block"
    weighting: dict[str, Any] = dict(_m(payload.get("candidate_weighting"))) if payload else {}
    if not blockers:
        epoch = int(time.time())
        bridge_status = "v13_1_to_v13_2_cycle_handoff_bridge_" + handoff_status.rsplit("_", 1)[-1]
        ready_state = {
            "version": "physical_quantum_qi_v13_2_candidate_weighting_cycle_handoff_ready_state_v13_14",
            "candidate_weighting_cycle_handoff_ready_state": True,
            "bridge_status": bridge_status,
            "closed_loop_reentry_status": closed_status,
            "reentry_weighting_action": action,
            "expected_v13_2_handoff_status": handoff_status,
            "expected_v13_2_cycle_gate_decision": cycle_decision,
            "expected_v13_2_admissible_candidate_seed_mode": seed_mode,
            "candidate_weighting": weighting,
            "source_closed_loop_reentry_receipt_digest": payload["source_closed_loop_reentry_receipt_digest"],
            "source_closed_loop_path_integral_reentry_digest": payload["source_closed_loop_path_integral_reentry_digest"],
            "process_tensor_context": dict(payload["process_tensor_context"]),
            "boundary": {
                "v13_2_cycle_handoff_ready_state_only": True,
                "v13_1_closed_loop_reentry_receipt_required": True,
                "can_feed_v13_2_candidate_weighting_cycle_handoff": True,
                "hands_off_to_cycle_gate": True,
                "hands_off_to_admissible_candidate_set": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "external_backaction_visible": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_handoff_execution": True,
                "does_not_run_handoff_runtime": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        ready_state["cycle_handoff_ready_state_digest"] = _sha(ready_state)
        _write_json(ready_state_path, ready_state)
        ready_written = True
        record = {
            "version": "physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_record_v13_14",
            "record_type": "physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge",
            "bridge_status": bridge_status,
            "closed_loop_reentry_status": closed_status,
            "reentry_weighting_action": action,
            "expected_v13_2_handoff_status": handoff_status,
            "expected_v13_2_cycle_gate_decision": cycle_decision,
            "expected_v13_2_admissible_candidate_seed_mode": seed_mode,
            "source_cycle_handoff_ready_state_digest": ready_state["cycle_handoff_ready_state_digest"],
            "source_closed_loop_reentry_receipt_digest": payload["source_closed_loop_reentry_receipt_digest"],
            "prev_record_digest": _last_digest(bridge_ledger_path),
            "boundary": {
                "bridge_receipt_only": True,
                "v13_2_cycle_handoff_ready_state_traceable": True,
                "hands_off_to_cycle_gate": True,
                "hands_off_to_admissible_candidate_set": True,
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
            "version": "physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_summary_v13_14",
            "bridge_status": bridge_status,
            "closed_loop_reentry_status": closed_status,
            "reentry_weighting_action": action,
            "expected_v13_2_handoff_status": handoff_status,
            "expected_v13_2_cycle_gate_decision": cycle_decision,
            "expected_v13_2_admissible_candidate_seed_mode": seed_mode,
            "cycle_handoff_ready_state_digest": ready_state["cycle_handoff_ready_state_digest"],
            "boundary": {
                "summary_only": True,
                "can_feed_v13_2_candidate_weighting_cycle_handoff": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    final_status = "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_BLOCKED"
    packet_id = "physical-quantum-qi-v13-1-to-v13-2-cycle-handoff-bridge-" + _sha({"payload": payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_v13_14",
        "status": final_status,
        "packet_id": packet_id,
        "bridge_status": bridge_status,
        "closed_loop_reentry_status": closed_status,
        "reentry_weighting_action": action,
        "expected_v13_2_handoff_status": handoff_status,
        "expected_v13_2_cycle_gate_decision": cycle_decision,
        "expected_v13_2_admissible_candidate_seed_mode": seed_mode,
        "handoff_ready_state_written": ready_written,
        "bridge_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiV13_1ToV13_2CycleHandoffBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_v13_14",
        final_status,
        packet_id,
        str(root),
        bridge_status,
        closed_status,
        action,
        handoff_status,
        cycle_decision,
        seed_mode,
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
