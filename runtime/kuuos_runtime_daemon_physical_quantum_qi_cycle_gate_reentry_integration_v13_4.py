#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


INTEGRATION = {
    "candidate_weighting_cycle_handoff_reinforce": (
        "cycle_gate_reentry_integration_admit",
        "integrated_cycle_gate_admit",
        "integrated_admissible_candidate_set_admit",
    ),
    "candidate_weighting_cycle_handoff_probe": (
        "cycle_gate_reentry_integration_hold",
        "integrated_cycle_gate_hold",
        "integrated_admissible_candidate_set_probe",
    ),
    "candidate_weighting_cycle_handoff_barrier": (
        "cycle_gate_reentry_integration_block",
        "integrated_cycle_gate_block",
        "integrated_admissible_candidate_set_block",
    ),
}
EXPECTED_GATE = {
    "candidate_weighting_cycle_handoff_reinforce": "reweight_candidate",
    "candidate_weighting_cycle_handoff_probe": "hold_candidate",
    "candidate_weighting_cycle_handoff_barrier": "block_candidate",
}
EXPECTED_SEED = {
    "candidate_weighting_cycle_handoff_reinforce": "reinforce_admissible_candidate_seed",
    "candidate_weighting_cycle_handoff_probe": "probe_candidate_seed",
    "candidate_weighting_cycle_handoff_barrier": "barrier_candidate_seed",
}
REQUIRED_RECEIPT_BOUNDARY_FLAGS = (
    "receipt_ledger_only",
    "candidate_weighting_cycle_handoff_receipt_only",
    "cycle_gate_input_traceable",
    "admissible_candidate_set_seed_traceable",
    "uses_process_tensor_feedback",
    "non_markov_feedback_preserved",
    "history_window_feedback_preserved",
    "memory_kernel_feedback_preserved",
    "external_backaction_visible",
    "candidate_weighting_not_truth",
    "handoff_not_direct_execution",
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
class PhysicalQuantumQiCycleGateReentryIntegrationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    integration_status: str
    integrated_cycle_gate_status: str
    integrated_admissible_candidate_set_status: str
    integration_packet_written: bool
    integrated_cycle_gate_state_written: bool
    integrated_admissible_candidate_set_written: bool
    integration_ledger_appended: bool
    integration_packet_path: str
    integrated_cycle_gate_state_path: str
    integrated_admissible_candidate_set_path: str
    integration_ledger_path: str
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
        blockers.append("candidate_weighting_cycle_handoff_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("candidate_weighting_cycle_handoff_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("candidate_weighting_cycle_handoff_receipt_ledger_latest_line_invalid")
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


def _validate_weighting(handoff_status: str, weighting: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    norm = _normalize_weighting(weighting)
    if handoff_status == "candidate_weighting_cycle_handoff_reinforce":
        if norm["path_weight_delta"] <= 0:
            blockers.append("integration_reinforce_without_positive_path_weight_delta")
        if norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("integration_reinforce_with_probe_or_barrier")
        if norm["memory_feedback_weight"] <= 0 or norm["external_backaction_weight"] <= 0 or norm["next_cycle_amplitude_delta"] <= 0:
            blockers.append("integration_reinforce_missing_process_tensor_effect_weight")
    elif handoff_status == "candidate_weighting_cycle_handoff_probe":
        if norm["path_weight_delta"] != 0:
            blockers.append("integration_probe_with_path_weight_delta")
        if not norm["probe_potential_required"]:
            blockers.append("integration_probe_without_probe_potential")
        if norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("integration_probe_with_barrier")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("integration_probe_with_effect_weight")
    elif handoff_status == "candidate_weighting_cycle_handoff_barrier":
        if norm["path_weight_delta"] != 0:
            blockers.append("integration_barrier_with_path_weight_delta")
        if norm["probe_potential_required"]:
            blockers.append("integration_barrier_with_probe")
        if not norm["barrier_potential_required"] or not norm["barrier_blocks_ready_weight"]:
            blockers.append("integration_barrier_without_blocking_barrier")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("integration_barrier_with_effect_weight")
    return norm


def _validate_receipt(record: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], str, str, str]:
    if not record:
        return {}, "candidate_weighting_cycle_handoff_barrier", "integrated_cycle_gate_block", "integrated_admissible_candidate_set_block"
    if record.get("record_type") != "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt":
        blockers.append("candidate_weighting_cycle_handoff_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"candidate_weighting_cycle_handoff_receipt_boundary_{name}_missing")
    handoff_status = str(record.get("handoff_status", "candidate_weighting_cycle_handoff_barrier"))
    if handoff_status not in INTEGRATION:
        blockers.append("candidate_weighting_cycle_handoff_status_invalid")
        handoff_status = "candidate_weighting_cycle_handoff_barrier"
    integration_status, cycle_status, candidate_set_status = INTEGRATION[handoff_status]
    gate_decision = str(record.get("cycle_gate_decision", ""))
    seed_mode = str(record.get("admissible_candidate_seed_mode", ""))
    if gate_decision != EXPECTED_GATE[handoff_status]:
        blockers.append("candidate_weighting_cycle_handoff_receipt_gate_decision_mismatch")
    if seed_mode != EXPECTED_SEED[handoff_status]:
        blockers.append("candidate_weighting_cycle_handoff_receipt_seed_mode_mismatch")
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(handoff_status, _m(record.get("candidate_weighting")), blockers)
    payload = {
        "handoff_status": handoff_status,
        "integration_status": integration_status,
        "integrated_cycle_gate_status": cycle_status,
        "integrated_admissible_candidate_set_status": candidate_set_status,
        "cycle_gate_decision": gate_decision,
        "admissible_candidate_seed_mode": seed_mode,
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_candidate_weighting_cycle_handoff_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_candidate_weighting_cycle_handoff_digest": str(record.get("source_candidate_weighting_cycle_handoff_digest", "")),
    }
    return payload, handoff_status, cycle_status, candidate_set_status


def _candidate_entries(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    status = str(payload.get("handoff_status", ""))
    weighting = dict(_m(payload.get("candidate_weighting")))
    context = dict(_m(payload.get("process_tensor_context")))
    if status == "candidate_weighting_cycle_handoff_reinforce":
        entry = {
            "candidate_id": "closed_loop_reentry_reinforced_candidate",
            "candidate_mode": "admit_candidate",
            "candidate_weighting": weighting,
            "process_tensor_context": context,
            "admissibility_status": "admissible_candidate_ready",
        }
        entry["candidate_digest"] = _sha(entry)
        return [entry]
    if status == "candidate_weighting_cycle_handoff_probe":
        entry = {
            "candidate_id": "closed_loop_reentry_probe_candidate",
            "candidate_mode": "probe_candidate",
            "candidate_weighting": weighting,
            "process_tensor_context": context,
            "admissibility_status": "admissible_candidate_probe_required",
        }
        entry["candidate_digest"] = _sha(entry)
        return [entry]
    return []


def build_physical_quantum_qi_cycle_gate_reentry_integration(
    *,
    runtime_context: Mapping[str, Any],
    cycle_gate_reentry_integration_license: Mapping[str, Any],
) -> PhysicalQuantumQiCycleGateReentryIntegrationResult:
    ctx = _m(runtime_context)
    lic = _m(cycle_gate_reentry_integration_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    handoff_receipt_ledger_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl"
    packet_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json"
    cycle_state_path = root / "physical_quantum_qi_integrated_cycle_gate_state.json"
    candidate_set_path = root / "physical_quantum_qi_integrated_admissible_candidate_set.json"
    integration_ledger_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_summary.json"
    receipt_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt.json"
    audit_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_audit.jsonl"

    if ctx.get("physical_quantum_qi_cycle_gate_reentry_integration_enabled") is not True:
        blockers.append("physical_quantum_qi_cycle_gate_reentry_integration_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_cycle_gate_reentry_integration") is not True:
        blockers.append("apply_physical_quantum_qi_cycle_gate_reentry_integration_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_cycle_gate_reentry_integration_license_not_ready")
    for name in [
        "candidate_weighting_cycle_handoff_receipt_ledger_read_allowed",
        "integration_packet_write_allowed",
        "integrated_cycle_gate_state_write_allowed",
        "integrated_admissible_candidate_set_write_allowed",
        "integration_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, handoff_status, cycle_status, candidate_set_status = _validate_receipt(_latest_jsonl(handoff_receipt_ledger_path, blockers), blockers)
    packet: dict[str, Any] = {}
    packet_written = cycle_written = set_written = ledger_appended = False
    if not blockers:
        epoch = int(time.time())
        candidates = _candidate_entries(payload)
        packet = {
            "version": "physical_quantum_qi_cycle_gate_reentry_integration_packet_v13_4",
            "cycle_gate_reentry_integration_considered": True,
            "integration_status": payload["integration_status"],
            "integrated_cycle_gate_status": cycle_status,
            "integrated_admissible_candidate_set_status": candidate_set_status,
            "handoff_status": handoff_status,
            "cycle_gate_decision": payload["cycle_gate_decision"],
            "admissible_candidate_seed_mode": payload["admissible_candidate_seed_mode"],
            "candidate_weighting": dict(payload["candidate_weighting"]),
            "integrated_candidates": candidates,
            "process_tensor_context": dict(payload["process_tensor_context"]),
            "source_digests": {
                "candidate_weighting_cycle_handoff_receipt": payload["source_candidate_weighting_cycle_handoff_receipt_digest"],
                "candidate_weighting_cycle_handoff": payload["source_candidate_weighting_cycle_handoff_digest"],
            },
            "boundary": {
                "cycle_gate_reentry_integration_only": True,
                "candidate_weighting_cycle_handoff_receipt_required": True,
                "integrates_cycle_gate": True,
                "integrates_admissible_candidate_set": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "external_backaction_visible": True,
                "candidate_weighting_not_truth": True,
                "integration_not_direct_execution": True,
                "license_gated_integration": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        packet["cycle_gate_reentry_integration_digest"] = _sha(packet)
        _write_json(packet_path, packet)
        packet_written = True
        cycle_state = {
            "version": "physical_quantum_qi_integrated_cycle_gate_state_v13_4",
            "integrated_cycle_gate_ready": True,
            "integrated_cycle_gate_status": cycle_status,
            "cycle_gate_decision": payload["cycle_gate_decision"],
            "candidate_weighting": dict(payload["candidate_weighting"]),
            "source_cycle_gate_reentry_integration_digest": packet["cycle_gate_reentry_integration_digest"],
            "process_tensor_context": dict(packet["process_tensor_context"]),
            "boundary": {
                "integrated_cycle_gate_state_only": True,
                "from_candidate_weighting_cycle_handoff_receipt": True,
                "uses_process_tensor_feedback": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
            },
            "epoch": epoch,
        }
        cycle_state["integrated_cycle_gate_state_digest"] = _sha(cycle_state)
        _write_json(cycle_state_path, cycle_state)
        cycle_written = True
        candidate_set = {
            "version": "physical_quantum_qi_integrated_admissible_candidate_set_v13_4",
            "integrated_admissible_candidate_set_ready": True,
            "integrated_admissible_candidate_set_status": candidate_set_status,
            "admissible_candidate_count": len(candidates),
            "integrated_candidates": candidates,
            "candidate_weighting": dict(payload["candidate_weighting"]),
            "source_cycle_gate_reentry_integration_digest": packet["cycle_gate_reentry_integration_digest"],
            "process_tensor_context": dict(packet["process_tensor_context"]),
            "boundary": {
                "integrated_admissible_candidate_set_only": True,
                "from_candidate_weighting_cycle_handoff_receipt": True,
                "uses_process_tensor_feedback": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
            },
            "epoch": epoch,
        }
        candidate_set["integrated_admissible_candidate_set_digest"] = _sha(candidate_set)
        _write_json(candidate_set_path, candidate_set)
        set_written = True
        ledger_record = {
            "version": "physical_quantum_qi_cycle_gate_reentry_integration_record_v13_4",
            "record_type": "physical_quantum_qi_cycle_gate_reentry_integration",
            "integration_status": packet["integration_status"],
            "integrated_cycle_gate_status": cycle_status,
            "integrated_admissible_candidate_set_status": candidate_set_status,
            "handoff_status": handoff_status,
            "candidate_weighting": dict(payload["candidate_weighting"]),
            "admissible_candidate_count": len(candidates),
            "source_cycle_gate_reentry_integration_digest": packet["cycle_gate_reentry_integration_digest"],
            "source_candidate_weighting_cycle_handoff_receipt_digest": payload["source_candidate_weighting_cycle_handoff_receipt_digest"],
            "prev_record_digest": _last_digest(integration_ledger_path),
            "boundary": {
                "integration_receipt_only": True,
                "cycle_gate_integrated": True,
                "admissible_candidate_set_integrated": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "replayable_receipt": True,
            },
            "epoch": epoch,
        }
        ledger_record["record_digest"] = _sha(ledger_record)
        _append_jsonl(integration_ledger_path, ledger_record)
        ledger_appended = True
        summary = {
            "version": "physical_quantum_qi_cycle_gate_reentry_integration_summary_v13_4",
            "integration_status": packet["integration_status"],
            "integrated_cycle_gate_status": cycle_status,
            "integrated_admissible_candidate_set_status": candidate_set_status,
            "admissible_candidate_count": len(candidates),
            "cycle_gate_reentry_integration_digest": packet["cycle_gate_reentry_integration_digest"],
            "boundary": {
                "summary_only": True,
                "cycle_gate_reentry_integration_only": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    status = "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_READY" if not blockers else "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_BLOCKED"
    packet_id = "physical-quantum-qi-cycle-gate-reentry-integration-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_v13_4",
        "status": status,
        "packet_id": packet_id,
        "integration_status": str(packet.get("integration_status", "cycle_gate_reentry_integration_block")),
        "integrated_cycle_gate_status": cycle_status,
        "integrated_admissible_candidate_set_status": candidate_set_status,
        "integration_packet_written": packet_written,
        "integrated_cycle_gate_state_written": cycle_written,
        "integrated_admissible_candidate_set_written": set_written,
        "integration_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiCycleGateReentryIntegrationResult(
        "kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_v13_4",
        status,
        packet_id,
        str(root),
        str(packet.get("integration_status", "cycle_gate_reentry_integration_block")),
        cycle_status,
        candidate_set_status,
        packet_written,
        cycle_written,
        set_written,
        ledger_appended,
        str(packet_path),
        str(cycle_state_path),
        str(candidate_set_path),
        str(integration_ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
