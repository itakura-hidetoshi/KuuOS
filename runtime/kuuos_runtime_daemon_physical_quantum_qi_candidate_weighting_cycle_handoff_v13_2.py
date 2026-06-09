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
    "closed_loop_reentry_reinforced": ("candidate_weighting_cycle_handoff_reinforce", "reweight_candidate", "reinforce_admissible_candidate_seed"),
    "closed_loop_reentry_probe_opened": ("candidate_weighting_cycle_handoff_probe", "hold_candidate", "probe_candidate_seed"),
    "closed_loop_reentry_barrier_added": ("candidate_weighting_cycle_handoff_barrier", "block_candidate", "barrier_candidate_seed"),
}
EXPECTED_ACTION = {
    "closed_loop_reentry_reinforced": "reinforce_path_weight",
    "closed_loop_reentry_probe_opened": "open_probe_potential",
    "closed_loop_reentry_barrier_added": "add_barrier_potential",
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
class PhysicalQuantumQiCandidateWeightingCycleHandoffResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    handoff_status: str
    cycle_gate_decision: str
    admissible_candidate_seed_mode: str
    handoff_packet_written: bool
    cycle_gate_input_written: bool
    admissible_candidate_set_seed_written: bool
    handoff_ledger_appended: bool
    handoff_packet_path: str
    cycle_gate_input_path: str
    admissible_candidate_set_seed_path: str
    handoff_ledger_path: str
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
            blockers.append("handoff_reinforce_without_positive_path_weight_delta")
        if norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("handoff_reinforce_with_probe_or_barrier")
        if norm["memory_feedback_weight"] <= 0 or norm["external_backaction_weight"] <= 0 or norm["next_cycle_amplitude_delta"] <= 0:
            blockers.append("handoff_reinforce_missing_process_tensor_effect_weight")
    elif status == "closed_loop_reentry_probe_opened":
        if norm["path_weight_delta"] != 0:
            blockers.append("handoff_probe_with_path_weight_delta")
        if not norm["probe_potential_required"]:
            blockers.append("handoff_probe_without_probe_potential")
        if norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("handoff_probe_with_barrier")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("handoff_probe_with_effect_weight")
    elif status == "closed_loop_reentry_barrier_added":
        if norm["path_weight_delta"] != 0:
            blockers.append("handoff_barrier_with_path_weight_delta")
        if norm["probe_potential_required"]:
            blockers.append("handoff_barrier_with_probe")
        if not norm["barrier_potential_required"] or not norm["barrier_blocks_ready_weight"]:
            blockers.append("handoff_barrier_without_blocking_barrier")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("handoff_barrier_with_effect_weight")
    return norm


def _validate_receipt(record: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], str, str, str, str]:
    if not record:
        return {}, "closed_loop_reentry_barrier_added", "add_barrier_potential", "candidate_weighting_cycle_handoff_barrier", "block_candidate"
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
    action = str(record.get("reentry_weighting_action", "add_barrier_potential"))
    if action != EXPECTED_ACTION[closed_status]:
        blockers.append("closed_loop_reentry_action_mismatch")
        action = EXPECTED_ACTION[closed_status]
    handoff_status, cycle_decision, seed_mode = HANDOFF[closed_status]
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(closed_status, _m(record.get("candidate_weighting")), blockers)
    payload = {
        "closed_loop_reentry_status": closed_status,
        "reentry_weighting_action": action,
        "handoff_status": handoff_status,
        "cycle_gate_decision": cycle_decision,
        "admissible_candidate_seed_mode": seed_mode,
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_closed_loop_reentry_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_closed_loop_path_integral_reentry_digest": str(record.get("source_closed_loop_path_integral_reentry_digest", "")),
    }
    return payload, closed_status, action, handoff_status, cycle_decision


def build_physical_quantum_qi_candidate_weighting_cycle_handoff(
    *,
    runtime_context: Mapping[str, Any],
    candidate_weighting_cycle_handoff_license: Mapping[str, Any],
) -> PhysicalQuantumQiCandidateWeightingCycleHandoffResult:
    ctx = _m(runtime_context)
    lic = _m(candidate_weighting_cycle_handoff_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_ledger_path = root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl"
    handoff_packet_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json"
    cycle_gate_input_path = root / "physical_quantum_qi_next_cycle_gate_input.json"
    seed_path = root / "physical_quantum_qi_admissible_candidate_set_seed.json"
    handoff_ledger_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_summary.json"
    receipt_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt.json"
    audit_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_audit.jsonl"

    if ctx.get("physical_quantum_qi_candidate_weighting_cycle_handoff_enabled") is not True:
        blockers.append("physical_quantum_qi_candidate_weighting_cycle_handoff_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_candidate_weighting_cycle_handoff") is not True:
        blockers.append("apply_physical_quantum_qi_candidate_weighting_cycle_handoff_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_LICENSE_READY":
        blockers.append("physical_quantum_qi_candidate_weighting_cycle_handoff_license_not_ready")
    for name in [
        "closed_loop_reentry_receipt_ledger_read_allowed",
        "handoff_packet_write_allowed",
        "cycle_gate_input_write_allowed",
        "admissible_candidate_set_seed_write_allowed",
        "handoff_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, closed_status, action, handoff_status, cycle_decision = _validate_receipt(_latest_jsonl(receipt_ledger_path, blockers), blockers)
    packet: dict[str, Any] = {}
    packet_written = cycle_written = seed_written = ledger_appended = False
    if not blockers:
        epoch = int(time.time())
        weighting = dict(_m(payload.get("candidate_weighting")))
        packet = {
            "version": "physical_quantum_qi_candidate_weighting_cycle_handoff_packet_v13_2",
            "candidate_weighting_cycle_handoff_considered": True,
            "handoff_status": handoff_status,
            "closed_loop_reentry_status": closed_status,
            "reentry_weighting_action": action,
            "cycle_gate_decision": cycle_decision,
            "admissible_candidate_seed_mode": payload["admissible_candidate_seed_mode"],
            "candidate_weighting": weighting,
            "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
            "source_digests": {
                "closed_loop_reentry_receipt": payload["source_closed_loop_reentry_receipt_digest"],
                "closed_loop_path_integral_reentry": payload["source_closed_loop_path_integral_reentry_digest"],
            },
            "boundary": {
                "candidate_weighting_cycle_handoff_only": True,
                "closed_loop_reentry_receipt_required": True,
                "hands_off_to_cycle_gate": True,
                "hands_off_to_admissible_candidate_set": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "external_backaction_visible": True,
                "candidate_weighting_not_truth": True,
                "handoff_not_direct_execution": True,
                "license_gated_handoff": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        packet["candidate_weighting_cycle_handoff_digest"] = _sha(packet)
        _write_json(handoff_packet_path, packet)
        packet_written = True
        cycle_gate_input = {
            "version": "physical_quantum_qi_next_cycle_gate_input_v13_2",
            "cycle_gate_input_ready": True,
            "cycle_gate_decision": cycle_decision,
            "candidate_weighting": weighting,
            "source_candidate_weighting_cycle_handoff_digest": packet["candidate_weighting_cycle_handoff_digest"],
            "process_tensor_context": dict(packet["process_tensor_context"]),
            "boundary": {
                "cycle_gate_input_only": True,
                "from_closed_loop_reentry_handoff": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
            },
            "epoch": epoch,
        }
        cycle_gate_input["cycle_gate_input_digest"] = _sha(cycle_gate_input)
        _write_json(cycle_gate_input_path, cycle_gate_input)
        cycle_written = True
        seed = {
            "version": "physical_quantum_qi_admissible_candidate_set_seed_v13_2",
            "admissible_candidate_set_seed_ready": True,
            "admissible_candidate_seed_mode": payload["admissible_candidate_seed_mode"],
            "candidate_weighting": weighting,
            "source_candidate_weighting_cycle_handoff_digest": packet["candidate_weighting_cycle_handoff_digest"],
            "process_tensor_context": dict(packet["process_tensor_context"]),
            "boundary": {
                "admissible_candidate_set_seed_only": True,
                "from_closed_loop_reentry_handoff": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
            },
            "epoch": epoch,
        }
        seed["admissible_candidate_set_seed_digest"] = _sha(seed)
        _write_json(seed_path, seed)
        seed_written = True
        ledger_record = {
            "version": "physical_quantum_qi_candidate_weighting_cycle_handoff_record_v13_2",
            "record_type": "physical_quantum_qi_candidate_weighting_cycle_handoff",
            "handoff_status": handoff_status,
            "cycle_gate_decision": cycle_decision,
            "admissible_candidate_seed_mode": payload["admissible_candidate_seed_mode"],
            "candidate_weighting": weighting,
            "source_candidate_weighting_cycle_handoff_digest": packet["candidate_weighting_cycle_handoff_digest"],
            "source_closed_loop_reentry_receipt_digest": payload["source_closed_loop_reentry_receipt_digest"],
            "prev_record_digest": _last_digest(handoff_ledger_path),
            "boundary": {
                "handoff_receipt_only": True,
                "hands_off_to_cycle_gate": True,
                "hands_off_to_admissible_candidate_set": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "replayable_receipt": True,
            },
            "epoch": epoch,
        }
        ledger_record["record_digest"] = _sha(ledger_record)
        _append_jsonl(handoff_ledger_path, ledger_record)
        ledger_appended = True
        summary = {
            "version": "physical_quantum_qi_candidate_weighting_cycle_handoff_summary_v13_2",
            "handoff_status": handoff_status,
            "cycle_gate_decision": cycle_decision,
            "admissible_candidate_seed_mode": payload["admissible_candidate_seed_mode"],
            "candidate_weighting": weighting,
            "candidate_weighting_cycle_handoff_digest": packet["candidate_weighting_cycle_handoff_digest"],
            "boundary": {
                "summary_only": True,
                "candidate_weighting_cycle_handoff_only": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    status = "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_READY" if not blockers else "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_BLOCKED"
    packet_id = "physical-quantum-qi-candidate-weighting-cycle-handoff-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_candidate_weighting_cycle_handoff_v13_2",
        "status": status,
        "packet_id": packet_id,
        "handoff_status": handoff_status,
        "cycle_gate_decision": cycle_decision,
        "admissible_candidate_seed_mode": str(packet.get("admissible_candidate_seed_mode", "barrier_candidate_seed")),
        "handoff_packet_written": packet_written,
        "cycle_gate_input_written": cycle_written,
        "admissible_candidate_set_seed_written": seed_written,
        "handoff_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiCandidateWeightingCycleHandoffResult(
        "kuuos_runtime_daemon_physical_quantum_qi_candidate_weighting_cycle_handoff_v13_2",
        status,
        packet_id,
        str(root),
        handoff_status,
        cycle_decision,
        str(packet.get("admissible_candidate_seed_mode", "barrier_candidate_seed")),
        packet_written,
        cycle_written,
        seed_written,
        ledger_appended,
        str(handoff_packet_path),
        str(cycle_gate_input_path),
        str(seed_path),
        str(handoff_ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
