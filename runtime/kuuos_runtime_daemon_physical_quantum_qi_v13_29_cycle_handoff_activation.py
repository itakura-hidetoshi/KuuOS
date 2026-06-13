#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_candidate_weighting_cycle_handoff_v13_2 import build_physical_quantum_qi_candidate_weighting_cycle_handoff
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_v13_14 import build_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge

FLOW = {
    "closed_loop_reentry_reinforced": ("reinforce_path_weight", "candidate_weighting_cycle_handoff_reinforce", "reweight_candidate", "reinforce_admissible_candidate_seed"),
    "closed_loop_reentry_probe_opened": ("open_probe_potential", "candidate_weighting_cycle_handoff_probe", "hold_candidate", "probe_candidate_seed"),
    "closed_loop_reentry_barrier_added": ("add_barrier_potential", "candidate_weighting_cycle_handoff_barrier", "block_candidate", "barrier_candidate_seed"),
}


@dataclass(frozen=True)
class PhysicalQuantumQiV13_29CycleHandoffActivationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    closed_loop_reentry_status: str
    reentry_weighting_action: str
    handoff_status: str
    cycle_gate_decision: str
    admissible_candidate_seed_mode: str
    v13_14_bridge_invoked: bool
    v13_2_handoff_invoked: bool
    handoff_ready_state_written: bool
    handoff_packet_written: bool
    cycle_gate_input_written: bool
    admissible_candidate_set_seed_written: bool
    handoff_ledger_appended: bool
    activation_record_path: str
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


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _latest(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return {}
    try:
        value = json.loads(lines[-1])
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


def build_physical_quantum_qi_v13_29_cycle_handoff_activation(*, runtime_context: Mapping[str, Any], v13_29_cycle_handoff_activation_license: Mapping[str, Any]) -> PhysicalQuantumQiV13_29CycleHandoffActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_29_cycle_handoff_activation_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_path = root / "physical_quantum_qi_v13_28_reentry_receipt_activation_record.json"
    receipt_ledger_path = root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl"
    record_path = root / "physical_quantum_qi_v13_29_cycle_handoff_activation_record.json"
    receipt_path = root / "physical_quantum_qi_v13_29_cycle_handoff_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_29_cycle_handoff_activation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_29_cycle_handoff_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_29_cycle_handoff_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_29_cycle_handoff_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_29_cycle_handoff_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_29_CYCLE_HANDOFF_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_29_cycle_handoff_activation_license_not_ready")
    for flag in ("v13_28_activation_record_read_allowed", "v13_1_receipt_ledger_read_allowed", "v13_14_bridge_invoke_allowed", "v13_2_handoff_invoke_allowed", "activation_record_write_allowed", "receipt_write_allowed", "audit_append_allowed"):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source = _read_json(source_path)
    receipt_record = _latest(receipt_ledger_path)
    if not source:
        blockers.append("v13_28_activation_record_missing_or_invalid")
    if not receipt_record:
        blockers.append("v13_1_receipt_record_missing_or_invalid")

    closed_status = str(source.get("closed_loop_reentry_status", "closed_loop_reentry_barrier_added"))
    if closed_status not in FLOW:
        blockers.append("v13_28_closed_loop_reentry_status_invalid")
        closed_status = "closed_loop_reentry_barrier_added"
    expected_action, expected_handoff, expected_decision, expected_seed = FLOW[closed_status]
    action = str(source.get("reentry_weighting_action", "add_barrier_potential"))
    if action != expected_action:
        blockers.append("v13_28_reentry_weighting_action_mismatch")
        action = expected_action

    if source:
        if source.get("activation_status") != "reentry_receipt_activation_completed":
            blockers.append("v13_28_activation_not_completed")
        expected_digest = str(source.get("source_v13_1_receipt_record_digest", ""))
        actual_digest = str(receipt_record.get("record_digest", ""))
        if not expected_digest or expected_digest != actual_digest:
            blockers.append("v13_28_receipt_record_digest_mismatch")
        if not source.get("reentry_receipt_activation_record_digest"):
            blockers.append("v13_28_activation_record_digest_missing")
    if receipt_record:
        if receipt_record.get("record_type") != "physical_quantum_qi_closed_loop_reentry_receipt":
            blockers.append("v13_1_receipt_record_type_invalid")
        if str(receipt_record.get("closed_loop_reentry_status", "")) != closed_status:
            blockers.append("v13_1_receipt_status_mismatch")
        if str(receipt_record.get("reentry_weighting_action", "")) != action:
            blockers.append("v13_1_receipt_action_mismatch")

    bridge_invoked = handoff_invoked = False
    bridge: dict[str, Any] = {}
    handoff: dict[str, Any] = {}
    if not blockers:
        bridge = build_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge(
            runtime_context={"physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_enabled": True, "apply_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge": True, "runtime_root": str(root)},
            v13_1_to_v13_2_cycle_handoff_bridge_license=dict(_m(lic.get("v13_14_bridge_license"))),
        ).to_dict()
        bridge_invoked = True
        if bridge.get("status") != "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_READY":
            blockers.append("v13_14_bridge_not_ready")
        if str(bridge.get("expected_v13_2_handoff_status", "")) != expected_handoff or str(bridge.get("expected_v13_2_cycle_gate_decision", "")) != expected_decision or str(bridge.get("expected_v13_2_admissible_candidate_seed_mode", "")) != expected_seed:
            blockers.append("v13_14_bridge_expectation_mismatch")

    if bridge_invoked and not blockers:
        handoff = build_physical_quantum_qi_candidate_weighting_cycle_handoff(
            runtime_context={"physical_quantum_qi_candidate_weighting_cycle_handoff_enabled": True, "apply_physical_quantum_qi_candidate_weighting_cycle_handoff": True, "runtime_root": str(root)},
            candidate_weighting_cycle_handoff_license=dict(_m(lic.get("v13_2_handoff_license"))),
        ).to_dict()
        handoff_invoked = True
        if handoff.get("status") != "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_READY":
            blockers.append("v13_2_handoff_not_ready")
        if str(handoff.get("handoff_status", "")) != expected_handoff or str(handoff.get("cycle_gate_decision", "")) != expected_decision or str(handoff.get("admissible_candidate_seed_mode", "")) != expected_seed:
            blockers.append("v13_2_handoff_output_mismatch")

    activation_status = "cycle_handoff_activation_completed" if bridge_invoked and handoff_invoked and not blockers else "cycle_handoff_activation_blocked"
    handoff_record = _latest(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_ledger.jsonl")
    if handoff_invoked and not str(handoff_record.get("record_digest", "")):
        blockers.append("v13_2_handoff_record_digest_missing")
        activation_status = "cycle_handoff_activation_blocked"

    if bridge_invoked or handoff_invoked:
        ready_state = _read_json(root / "physical_quantum_qi_v13_2_candidate_weighting_cycle_handoff_ready_state.json")
        handoff_packet = _read_json(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json")
        record = {
            "version": "physical_quantum_qi_v13_29_cycle_handoff_activation_record",
            "activation_status": activation_status,
            "closed_loop_reentry_status": closed_status,
            "reentry_weighting_action": action,
            "handoff_status": str(handoff.get("handoff_status", expected_handoff)),
            "cycle_gate_decision": str(handoff.get("cycle_gate_decision", expected_decision)),
            "admissible_candidate_seed_mode": str(handoff.get("admissible_candidate_seed_mode", expected_seed)),
            "source_v13_28_activation_record_digest": str(source.get("reentry_receipt_activation_record_digest", "")),
            "source_v13_1_receipt_record_digest": str(receipt_record.get("record_digest", "")),
            "source_v13_14_handoff_ready_state_digest": str(ready_state.get("cycle_handoff_ready_state_digest", "")),
            "source_v13_2_handoff_packet_digest": str(handoff_packet.get("candidate_weighting_cycle_handoff_digest", "")),
            "source_v13_2_handoff_record_digest": str(handoff_record.get("record_digest", "")),
            "boundary": {"two_stage_cycle_handoff_activation": True, "uses_process_tensor_feedback": True, "non_markov_feedback_preserved": True, "candidate_weighting_not_truth": True, "not_direct_execution_authority": True, "license_gated_cycle_handoff": True, "runtime_local_external_state_only": True, "fail_closed_on_boundary_loss": True},
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        record["cycle_handoff_activation_record_digest"] = _sha(record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(record_path, record)

    status = "PHYSICAL_QUANTUM_QI_V13_29_CYCLE_HANDOFF_ACTIVATION_READY" if bridge_invoked and handoff_invoked and not blockers else "PHYSICAL_QUANTUM_QI_V13_29_CYCLE_HANDOFF_ACTIVATION_BLOCKED"
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_29_cycle_handoff_activation",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-29-cycle-handoff-activation-" + _sha({"handoff": expected_handoff, "blockers": blockers})[:16],
        "activation_status": activation_status,
        "closed_loop_reentry_status": closed_status,
        "reentry_weighting_action": action,
        "handoff_status": str(handoff.get("handoff_status", expected_handoff)),
        "cycle_gate_decision": str(handoff.get("cycle_gate_decision", expected_decision)),
        "admissible_candidate_seed_mode": str(handoff.get("admissible_candidate_seed_mode", expected_seed)),
        "v13_14_bridge_invoked": bridge_invoked,
        "v13_2_handoff_invoked": handoff_invoked,
        "handoff_ready_state_written": bridge.get("handoff_ready_state_written") is True,
        "handoff_packet_written": handoff.get("handoff_packet_written") is True,
        "cycle_gate_input_written": handoff.get("cycle_gate_input_written") is True,
        "admissible_candidate_set_seed_written": handoff.get("admissible_candidate_set_seed_written") is True,
        "handoff_ledger_appended": handoff.get("handoff_ledger_appended") is True,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiV13_29CycleHandoffActivationResult(
        receipt["version"], status, receipt["packet_id"], str(root), activation_status, closed_status, action,
        receipt["handoff_status"], receipt["cycle_gate_decision"], receipt["admissible_candidate_seed_mode"],
        bridge_invoked, handoff_invoked, receipt["handoff_ready_state_written"], receipt["handoff_packet_written"],
        receipt["cycle_gate_input_written"], receipt["admissible_candidate_set_seed_written"], receipt["handoff_ledger_appended"],
        str(record_path), str(receipt_path), str(audit_path), blockers, warnings,
    )
