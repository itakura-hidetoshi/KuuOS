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
        "reweight_candidate",
        "reinforce_admissible_candidate_seed",
        "cycle_gate_reentry_integration_admit",
        "integrated_cycle_gate_admit",
        "integrated_admissible_candidate_set_admit",
    ),
    "candidate_weighting_cycle_handoff_probe": (
        "hold_candidate",
        "probe_candidate_seed",
        "cycle_gate_reentry_integration_hold",
        "integrated_cycle_gate_hold",
        "integrated_admissible_candidate_set_probe",
    ),
    "candidate_weighting_cycle_handoff_barrier": (
        "block_candidate",
        "barrier_candidate_seed",
        "cycle_gate_reentry_integration_block",
        "integrated_cycle_gate_block",
        "integrated_admissible_candidate_set_block",
    ),
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
class PhysicalQuantumQiV13_3ToV13_4IntegrationBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_status: str
    handoff_status: str
    expected_v13_4_integration_status: str
    expected_v13_4_integrated_cycle_gate_status: str
    expected_v13_4_integrated_admissible_candidate_set_status: str
    path_weight_delta: int
    probe_potential_required: bool
    barrier_potential_required: bool
    integration_ready_state_written: bool
    bridge_ledger_appended: bool
    integration_ready_state_path: str
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
            blockers.append("v13_4_bridge_reinforce_weighting_invalid")
        if norm["memory_feedback_weight"] <= 0 or norm["external_backaction_weight"] <= 0 or norm["next_cycle_amplitude_delta"] <= 0:
            blockers.append("v13_4_bridge_reinforce_missing_process_tensor_effect_weight")
    elif handoff_status == "candidate_weighting_cycle_handoff_probe":
        if norm["path_weight_delta"] != 0 or not norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_4_bridge_probe_weighting_invalid")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("v13_4_bridge_probe_with_effect_weight")
    elif handoff_status == "candidate_weighting_cycle_handoff_barrier":
        if norm["path_weight_delta"] != 0 or norm["probe_potential_required"] or not norm["barrier_potential_required"] or not norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_4_bridge_barrier_weighting_invalid")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("v13_4_bridge_barrier_with_effect_weight")
    else:
        blockers.append("candidate_weighting_cycle_handoff_status_invalid")
    return norm


def _validate_receipt(record: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], str, str, str, str]:
    if not record:
        return {}, "candidate_weighting_cycle_handoff_barrier", "cycle_gate_reentry_integration_block", "integrated_cycle_gate_block", "integrated_admissible_candidate_set_block"
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
    expected_gate, expected_seed, integration_status, cycle_gate_status, candidate_set_status = INTEGRATION[handoff_status]
    gate_decision = str(record.get("cycle_gate_decision", ""))
    seed_mode = str(record.get("admissible_candidate_seed_mode", ""))
    if gate_decision != expected_gate:
        blockers.append("candidate_weighting_cycle_handoff_receipt_gate_decision_mismatch")
    if seed_mode != expected_seed:
        blockers.append("candidate_weighting_cycle_handoff_receipt_seed_mode_mismatch")
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(handoff_status, _m(record.get("candidate_weighting")), blockers)
    payload = {
        "handoff_status": handoff_status,
        "cycle_gate_decision": gate_decision,
        "admissible_candidate_seed_mode": seed_mode,
        "integration_status": integration_status,
        "integrated_cycle_gate_status": cycle_gate_status,
        "integrated_admissible_candidate_set_status": candidate_set_status,
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_candidate_weighting_cycle_handoff_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_candidate_weighting_cycle_handoff_digest": str(record.get("source_candidate_weighting_cycle_handoff_digest", "")),
    }
    return payload, handoff_status, integration_status, cycle_gate_status, candidate_set_status


def build_physical_quantum_qi_v13_3_to_v13_4_integration_bridge(
    *,
    runtime_context: Mapping[str, Any],
    v13_3_to_v13_4_integration_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_3ToV13_4IntegrationBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(v13_3_to_v13_4_integration_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    handoff_receipt_ledger_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl"
    ready_state_path = root / "physical_quantum_qi_v13_4_cycle_gate_reentry_integration_ready_state.json"
    bridge_ledger_path = root / "physical_quantum_qi_v13_3_to_v13_4_integration_bridge_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_v13_3_to_v13_4_integration_bridge_summary.json"
    receipt_path = root / "physical_quantum_qi_v13_3_to_v13_4_integration_bridge_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_3_to_v13_4_integration_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_3_to_v13_4_integration_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_3_to_v13_4_integration_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_3_to_v13_4_integration_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_v13_3_to_v13_4_integration_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_3_to_v13_4_integration_bridge_license_not_ready")
    for name in [
        "v13_3_handoff_receipt_ledger_read_allowed",
        "v13_4_integration_ready_state_write_allowed",
        "bridge_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, handoff_status, integration_status, cycle_gate_status, candidate_set_status = _validate_receipt(
        _latest_jsonl(handoff_receipt_ledger_path, blockers), blockers
    )
    ready_written = ledger_appended = False
    bridge_status = "v13_3_to_v13_4_integration_bridge_block"
    weighting: dict[str, Any] = dict(_m(payload.get("candidate_weighting"))) if payload else {}
    if not blockers:
        epoch = int(time.time())
        bridge_status = "v13_3_to_v13_4_integration_bridge_" + integration_status.rsplit("_", 1)[-1]
        ready_state = {
            "version": "physical_quantum_qi_v13_4_cycle_gate_reentry_integration_ready_state_v13_16",
            "cycle_gate_reentry_integration_ready_state": True,
            "bridge_status": bridge_status,
            "handoff_status": handoff_status,
            "integration_status": integration_status,
            "integrated_cycle_gate_status": cycle_gate_status,
            "integrated_admissible_candidate_set_status": candidate_set_status,
            "cycle_gate_decision": payload["cycle_gate_decision"],
            "admissible_candidate_seed_mode": payload["admissible_candidate_seed_mode"],
            "candidate_weighting": weighting,
            "source_candidate_weighting_cycle_handoff_receipt_digest": payload["source_candidate_weighting_cycle_handoff_receipt_digest"],
            "source_candidate_weighting_cycle_handoff_digest": payload["source_candidate_weighting_cycle_handoff_digest"],
            "process_tensor_context": dict(payload["process_tensor_context"]),
            "boundary": {
                "v13_4_cycle_gate_reentry_integration_ready_state_only": True,
                "v13_3_handoff_receipt_required": True,
                "can_feed_v13_4_cycle_gate_reentry_integration": True,
                "cycle_gate_input_traceable": True,
                "admissible_candidate_set_seed_traceable": True,
                "integrates_cycle_gate": True,
                "integrates_admissible_candidate_set": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "external_backaction_visible": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_integration_execution": True,
                "does_not_run_integration_runtime": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        ready_state["integration_ready_state_digest"] = _sha(ready_state)
        _write_json(ready_state_path, ready_state)
        ready_written = True
        record = {
            "version": "physical_quantum_qi_v13_3_to_v13_4_integration_bridge_record_v13_16",
            "record_type": "physical_quantum_qi_v13_3_to_v13_4_integration_bridge",
            "bridge_status": bridge_status,
            "handoff_status": handoff_status,
            "integration_status": integration_status,
            "integrated_cycle_gate_status": cycle_gate_status,
            "integrated_admissible_candidate_set_status": candidate_set_status,
            "source_integration_ready_state_digest": ready_state["integration_ready_state_digest"],
            "source_candidate_weighting_cycle_handoff_receipt_digest": payload["source_candidate_weighting_cycle_handoff_receipt_digest"],
            "prev_record_digest": _last_digest(bridge_ledger_path),
            "boundary": {
                "bridge_receipt_only": True,
                "v13_4_integration_ready_state_traceable": True,
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
            "version": "physical_quantum_qi_v13_3_to_v13_4_integration_bridge_summary_v13_16",
            "bridge_status": bridge_status,
            "handoff_status": handoff_status,
            "integration_status": integration_status,
            "integrated_cycle_gate_status": cycle_gate_status,
            "integrated_admissible_candidate_set_status": candidate_set_status,
            "integration_ready_state_digest": ready_state["integration_ready_state_digest"],
            "boundary": {
                "summary_only": True,
                "can_feed_v13_4_cycle_gate_reentry_integration": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    final_status = "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_BLOCKED"
    packet_id = "physical-quantum-qi-v13-3-to-v13-4-integration-bridge-" + _sha({"payload": payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_3_to_v13_4_integration_bridge_v13_16",
        "status": final_status,
        "packet_id": packet_id,
        "bridge_status": bridge_status,
        "handoff_status": handoff_status,
        "integration_status": integration_status,
        "integrated_cycle_gate_status": cycle_gate_status,
        "integrated_admissible_candidate_set_status": candidate_set_status,
        "integration_ready_state_written": ready_written,
        "bridge_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiV13_3ToV13_4IntegrationBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v13_3_to_v13_4_integration_bridge_v13_16",
        final_status,
        packet_id,
        str(root),
        bridge_status,
        handoff_status,
        integration_status,
        cycle_gate_status,
        candidate_set_status,
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
