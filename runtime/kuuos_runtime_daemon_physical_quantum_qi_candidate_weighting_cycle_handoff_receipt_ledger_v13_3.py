#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


HANDOFF_STATUSES = {
    "candidate_weighting_cycle_handoff_reinforce",
    "candidate_weighting_cycle_handoff_probe",
    "candidate_weighting_cycle_handoff_barrier",
}
EXPECTED_BY_STATUS = {
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
class PhysicalQuantumQiCandidateWeightingCycleHandoffReceiptLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    handoff_status: str
    cycle_gate_decision: str
    admissible_candidate_seed_mode: str
    ledger_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    ledger_appended: bool
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


def _validate_context(ctx: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    out = {key: str(ctx.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, value in out.items():
        if not value:
            blockers.append(f"process_tensor_context_{key}_missing")
    return out


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
    if handoff_status not in HANDOFF_STATUSES:
        blockers.append("candidate_weighting_cycle_handoff_status_invalid")
        handoff_status = "candidate_weighting_cycle_handoff_barrier"
    expected_gate, expected_seed = EXPECTED_BY_STATUS[handoff_status]
    gate = str(packet.get("cycle_gate_decision", ""))
    seed = str(packet.get("admissible_candidate_seed_mode", ""))
    if gate != expected_gate:
        blockers.append("candidate_weighting_cycle_handoff_gate_decision_mismatch")
        gate = expected_gate
    if seed != expected_seed:
        blockers.append("candidate_weighting_cycle_handoff_seed_mode_mismatch")
        seed = expected_seed
    context = _validate_context(_m(packet.get("process_tensor_context")), blockers)
    weighting = _normalize_weighting(_m(packet.get("candidate_weighting")))
    if handoff_status == "candidate_weighting_cycle_handoff_reinforce":
        if weighting["path_weight_delta"] <= 0 or weighting["probe_potential_required"] or weighting["barrier_potential_required"]:
            blockers.append("handoff_receipt_reinforce_weighting_invalid")
    elif handoff_status == "candidate_weighting_cycle_handoff_probe":
        if weighting["path_weight_delta"] != 0 or not weighting["probe_potential_required"] or weighting["barrier_potential_required"]:
            blockers.append("handoff_receipt_probe_weighting_invalid")
    else:
        if weighting["path_weight_delta"] != 0 or weighting["probe_potential_required"] or not weighting["barrier_potential_required"] or not weighting["barrier_blocks_ready_weight"]:
            blockers.append("handoff_receipt_barrier_weighting_invalid")
    if not packet.get("candidate_weighting_cycle_handoff_digest"):
        warnings.append("candidate_weighting_cycle_handoff_digest_missing")
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


def _record(payload: Mapping[str, Any], prev_digest: str) -> dict[str, Any]:
    rec = {
        "version": "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_record_v13_3",
        "record_type": "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt",
        "handoff_status": str(payload.get("handoff_status", "")),
        "cycle_gate_decision": str(payload.get("cycle_gate_decision", "")),
        "admissible_candidate_seed_mode": str(payload.get("admissible_candidate_seed_mode", "")),
        "candidate_weighting": dict(_m(payload.get("candidate_weighting"))),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_candidate_weighting_cycle_handoff_digest": str(payload.get("source_candidate_weighting_cycle_handoff_digest", "")),
        "source_closed_loop_reentry_receipt_digest": str(payload.get("source_closed_loop_reentry_receipt_digest", "")),
        "source_closed_loop_path_integral_reentry_digest": str(payload.get("source_closed_loop_path_integral_reentry_digest", "")),
        "prev_record_digest": prev_digest,
        "boundary": {
            "receipt_ledger_only": True,
            "candidate_weighting_cycle_handoff_receipt_only": True,
            "cycle_gate_input_traceable": True,
            "admissible_candidate_set_seed_traceable": True,
            "uses_process_tensor_feedback": True,
            "non_markov_feedback_preserved": True,
            "history_window_feedback_preserved": True,
            "memory_kernel_feedback_preserved": True,
            "external_backaction_visible": True,
            "candidate_weighting_not_truth": True,
            "handoff_not_direct_execution": True,
            "replayable_receipt": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def build_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger(
    *,
    runtime_context: Mapping[str, Any],
    candidate_weighting_cycle_handoff_receipt_ledger_license: Mapping[str, Any],
) -> PhysicalQuantumQiCandidateWeightingCycleHandoffReceiptLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(candidate_weighting_cycle_handoff_receipt_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json"
    gate_path = root / "physical_quantum_qi_next_cycle_gate_input.json"
    seed_path = root / "physical_quantum_qi_admissible_candidate_set_seed.json"
    ledger_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_summary.json"
    receipt_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_receipt.json"
    audit_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_audit.jsonl"

    if ctx.get("physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_enabled") is not True:
        blockers.append("physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger") is not True:
        blockers.append("apply_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_LICENSE_READY":
        blockers.append("physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_license_not_ready")
    for name in [
        "handoff_packet_read_allowed",
        "cycle_gate_input_read_allowed",
        "admissible_candidate_set_seed_read_allowed",
        "receipt_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, handoff_status, cycle_decision, seed_mode = _validate_packet(_read_json(packet_path), blockers, warnings)
    _validate_gate(_read_json(gate_path), payload, blockers)
    _validate_seed(_read_json(seed_path), payload, blockers)
    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    if not blockers:
        record = _record(payload, _last_digest(ledger_path))
        _append_jsonl(ledger_path, record)
        summary = {
            "version": "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_summary_v13_3",
            "handoff_status": handoff_status,
            "cycle_gate_decision": cycle_decision,
            "admissible_candidate_seed_mode": seed_mode,
            "candidate_weighting": dict(record["candidate_weighting"]),
            "latest_record_digest": record["record_digest"],
            "source_candidate_weighting_cycle_handoff_digest": record["source_candidate_weighting_cycle_handoff_digest"],
            "boundary": {
                "summary_only": True,
                "candidate_weighting_cycle_handoff_receipt_only": True,
                "cycle_gate_input_traceable": True,
                "admissible_candidate_set_seed_traceable": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)
        appended = True

    final_status = "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_BLOCKED"
    packet_id = "physical-quantum-qi-candidate-weighting-cycle-handoff-receipt-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_v13_3",
        "status": final_status,
        "packet_id": packet_id,
        "handoff_status": handoff_status,
        "cycle_gate_decision": cycle_decision,
        "admissible_candidate_seed_mode": seed_mode,
        "ledger_appended": appended,
        "record_digest": str(record.get("record_digest", "")),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiCandidateWeightingCycleHandoffReceiptLedgerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_v13_3",
        final_status,
        packet_id,
        str(root),
        handoff_status,
        cycle_decision,
        seed_mode,
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        appended,
        blockers,
        warnings,
    )
