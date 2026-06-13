#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_v13_3 import build_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_v13_15 import build_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge

FLOW = {
    "candidate_weighting_cycle_handoff_reinforce": ("reweight_candidate", "reinforce_admissible_candidate_seed"),
    "candidate_weighting_cycle_handoff_probe": ("hold_candidate", "probe_candidate_seed"),
    "candidate_weighting_cycle_handoff_barrier": ("block_candidate", "barrier_candidate_seed"),
}


@dataclass(frozen=True)
class PhysicalQuantumQiV13_30HandoffReceiptActivationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    handoff_status: str
    cycle_gate_decision: str
    admissible_candidate_seed_mode: str
    v13_15_bridge_invoked: bool
    v13_3_receipt_ledger_invoked: bool
    receipt_ready_state_written: bool
    bridge_ledger_appended: bool
    receipt_ledger_appended: bool
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


def build_physical_quantum_qi_v13_30_handoff_receipt_activation(*, runtime_context: Mapping[str, Any], v13_30_handoff_receipt_activation_license: Mapping[str, Any]) -> PhysicalQuantumQiV13_30HandoffReceiptActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_30_handoff_receipt_activation_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_path = root / "physical_quantum_qi_v13_29_cycle_handoff_activation_record.json"
    packet_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json"
    handoff_ledger_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_ledger.jsonl"
    record_path = root / "physical_quantum_qi_v13_30_handoff_receipt_activation_record.json"
    receipt_path = root / "physical_quantum_qi_v13_30_handoff_receipt_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_30_handoff_receipt_activation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_30_handoff_receipt_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_30_handoff_receipt_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_30_handoff_receipt_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_30_handoff_receipt_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_30_HANDOFF_RECEIPT_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_30_handoff_receipt_activation_license_not_ready")
    for flag in ("v13_29_activation_record_read_allowed", "v13_2_handoff_packet_read_allowed", "v13_2_handoff_ledger_read_allowed", "v13_15_bridge_invoke_allowed", "v13_3_receipt_ledger_invoke_allowed", "activation_record_write_allowed", "receipt_write_allowed", "audit_append_allowed"):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source = _read_json(source_path)
    packet = _read_json(packet_path)
    handoff_record = _latest(handoff_ledger_path)
    if not source:
        blockers.append("v13_29_activation_record_missing_or_invalid")
    if not packet:
        blockers.append("v13_2_handoff_packet_missing_or_invalid")
    if not handoff_record:
        blockers.append("v13_2_handoff_record_missing_or_invalid")

    handoff_status = str(source.get("handoff_status", "candidate_weighting_cycle_handoff_barrier"))
    if handoff_status not in FLOW:
        blockers.append("v13_29_handoff_status_invalid")
        handoff_status = "candidate_weighting_cycle_handoff_barrier"
    expected_decision, expected_seed = FLOW[handoff_status]
    decision = str(source.get("cycle_gate_decision", "block_candidate"))
    seed = str(source.get("admissible_candidate_seed_mode", "barrier_candidate_seed"))
    if decision != expected_decision:
        blockers.append("v13_29_cycle_gate_decision_mismatch")
        decision = expected_decision
    if seed != expected_seed:
        blockers.append("v13_29_candidate_seed_mode_mismatch")
        seed = expected_seed

    if source:
        if source.get("activation_status") != "cycle_handoff_activation_completed":
            blockers.append("v13_29_activation_not_completed")
        if not source.get("cycle_handoff_activation_record_digest"):
            blockers.append("v13_29_activation_record_digest_missing")
        if str(source.get("source_v13_2_handoff_packet_digest", "")) != str(packet.get("candidate_weighting_cycle_handoff_digest", "")):
            blockers.append("v13_29_handoff_packet_digest_mismatch")
        if str(source.get("source_v13_2_handoff_record_digest", "")) != str(handoff_record.get("record_digest", "")):
            blockers.append("v13_29_handoff_record_digest_mismatch")
    if packet:
        if str(packet.get("handoff_status", "")) != handoff_status:
            blockers.append("v13_2_packet_handoff_status_mismatch")
        if str(packet.get("cycle_gate_decision", "")) != decision:
            blockers.append("v13_2_packet_cycle_gate_decision_mismatch")
        if str(packet.get("admissible_candidate_seed_mode", "")) != seed:
            blockers.append("v13_2_packet_candidate_seed_mode_mismatch")
    if handoff_record:
        if handoff_record.get("record_type") != "physical_quantum_qi_candidate_weighting_cycle_handoff":
            blockers.append("v13_2_handoff_record_type_invalid")
        if str(handoff_record.get("source_candidate_weighting_cycle_handoff_digest", "")) != str(packet.get("candidate_weighting_cycle_handoff_digest", "")):
            blockers.append("v13_2_handoff_record_packet_digest_mismatch")

    bridge_invoked = ledger_invoked = False
    bridge: dict[str, Any] = {}
    ledger: dict[str, Any] = {}
    if not blockers:
        bridge = build_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge(
            runtime_context={"physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_enabled": True, "apply_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge": True, "runtime_root": str(root)},
            v13_2_to_v13_3_handoff_receipt_bridge_license=dict(_m(lic.get("v13_15_bridge_license"))),
        ).to_dict()
        bridge_invoked = True
        if bridge.get("status") != "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_READY":
            blockers.append("v13_15_bridge_not_ready")
        if str(bridge.get("handoff_status", "")) != handoff_status or str(bridge.get("cycle_gate_decision", "")) != decision or str(bridge.get("admissible_candidate_seed_mode", "")) != seed:
            blockers.append("v13_15_bridge_output_mismatch")

    if bridge_invoked and not blockers:
        ledger = build_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger(
            runtime_context={"physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_enabled": True, "apply_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger": True, "runtime_root": str(root)},
            candidate_weighting_cycle_handoff_receipt_ledger_license=dict(_m(lic.get("v13_3_receipt_ledger_license"))),
        ).to_dict()
        ledger_invoked = True
        if ledger.get("status") != "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_READY":
            blockers.append("v13_3_receipt_ledger_not_ready")
        if str(ledger.get("handoff_status", "")) != handoff_status or str(ledger.get("cycle_gate_decision", "")) != decision or str(ledger.get("admissible_candidate_seed_mode", "")) != seed:
            blockers.append("v13_3_receipt_ledger_output_mismatch")

    ledger_receipt = _read_json(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_receipt.json")
    receipt_record = _latest(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl")
    if ledger_invoked and (not str(ledger_receipt.get("record_digest", "")) or ledger_receipt.get("record_digest") != receipt_record.get("record_digest")):
        blockers.append("v13_3_receipt_record_digest_missing_or_mismatch")

    activation_status = "handoff_receipt_activation_completed" if bridge_invoked and ledger_invoked and not blockers else "handoff_receipt_activation_blocked"
    if bridge_invoked or ledger_invoked:
        ready_state = _read_json(root / "physical_quantum_qi_v13_3_candidate_weighting_cycle_handoff_receipt_ready_state.json")
        record = {
            "version": "physical_quantum_qi_v13_30_handoff_receipt_activation_record",
            "activation_status": activation_status,
            "handoff_status": handoff_status,
            "cycle_gate_decision": decision,
            "admissible_candidate_seed_mode": seed,
            "source_v13_29_activation_record_digest": str(source.get("cycle_handoff_activation_record_digest", "")),
            "source_v13_2_handoff_packet_digest": str(packet.get("candidate_weighting_cycle_handoff_digest", "")),
            "source_v13_2_handoff_record_digest": str(handoff_record.get("record_digest", "")),
            "source_v13_15_receipt_ready_state_digest": str(ready_state.get("handoff_receipt_ready_state_digest", "")),
            "source_v13_3_receipt_record_digest": str(receipt_record.get("record_digest", "")),
            "boundary": {"two_stage_handoff_receipt_activation": True, "uses_process_tensor_feedback": True, "non_markov_feedback_preserved": True, "candidate_weighting_not_truth": True, "not_direct_execution_authority": True, "license_gated_receipt_activation": True, "runtime_local_external_state_only": True, "fail_closed_on_boundary_loss": True},
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        record["handoff_receipt_activation_record_digest"] = _sha(record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(record_path, record)

    status = "PHYSICAL_QUANTUM_QI_V13_30_HANDOFF_RECEIPT_ACTIVATION_READY" if bridge_invoked and ledger_invoked and not blockers else "PHYSICAL_QUANTUM_QI_V13_30_HANDOFF_RECEIPT_ACTIVATION_BLOCKED"
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_30_handoff_receipt_activation",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-30-handoff-receipt-activation-" + _sha({"handoff": handoff_status, "blockers": blockers})[:16],
        "activation_status": activation_status,
        "handoff_status": handoff_status,
        "cycle_gate_decision": decision,
        "admissible_candidate_seed_mode": seed,
        "v13_15_bridge_invoked": bridge_invoked,
        "v13_3_receipt_ledger_invoked": ledger_invoked,
        "receipt_ready_state_written": bridge.get("receipt_ready_state_written") is True,
        "bridge_ledger_appended": bridge.get("bridge_ledger_appended") is True,
        "receipt_ledger_appended": ledger.get("ledger_appended") is True,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiV13_30HandoffReceiptActivationResult(
        receipt["version"], status, receipt["packet_id"], str(root), activation_status, handoff_status, decision, seed,
        bridge_invoked, ledger_invoked, receipt["receipt_ready_state_written"], receipt["bridge_ledger_appended"], receipt["receipt_ledger_appended"],
        str(record_path), str(receipt_path), str(audit_path), blockers, warnings,
    )
