#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_v13_5 import build_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge_v13_17 import build_physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge

FLOW = {
    "cycle_gate_reentry_integration_admit": ("integrated_cycle_gate_admit", "integrated_admissible_candidate_set_admit", 1),
    "cycle_gate_reentry_integration_hold": ("integrated_cycle_gate_hold", "integrated_admissible_candidate_set_probe", 1),
    "cycle_gate_reentry_integration_block": ("integrated_cycle_gate_block", "integrated_admissible_candidate_set_block", 0),
}


@dataclass(frozen=True)
class PhysicalQuantumQiV13_32IntegrationReceiptActivationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    integration_status: str
    integrated_cycle_gate_status: str
    integrated_admissible_candidate_set_status: str
    admissible_candidate_count: int
    v13_17_bridge_invoked: bool
    v13_5_receipt_ledger_invoked: bool
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


def build_physical_quantum_qi_v13_32_integration_receipt_activation(*, runtime_context: Mapping[str, Any], v13_32_integration_receipt_activation_license: Mapping[str, Any]) -> PhysicalQuantumQiV13_32IntegrationReceiptActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_32_integration_receipt_activation_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_path = root / "physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_record.json"
    packet_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json"
    integration_ledger_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_ledger.jsonl"
    record_path = root / "physical_quantum_qi_v13_32_integration_receipt_activation_record.json"
    receipt_path = root / "physical_quantum_qi_v13_32_integration_receipt_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_32_integration_receipt_activation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_32_integration_receipt_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_32_integration_receipt_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_32_integration_receipt_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_32_integration_receipt_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_32_INTEGRATION_RECEIPT_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_32_integration_receipt_activation_license_not_ready")
    for flag in ("v13_31_activation_record_read_allowed", "v13_4_integration_packet_read_allowed", "v13_4_integration_ledger_read_allowed", "v13_17_bridge_invoke_allowed", "v13_5_receipt_ledger_invoke_allowed", "activation_record_write_allowed", "receipt_write_allowed", "audit_append_allowed"):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source = _read_json(source_path)
    packet = _read_json(packet_path)
    integration_record = _latest(integration_ledger_path)
    if not source:
        blockers.append("v13_31_activation_record_missing_or_invalid")
    if not packet:
        blockers.append("v13_4_integration_packet_missing_or_invalid")
    if not integration_record:
        blockers.append("v13_4_integration_record_missing_or_invalid")

    integration_status = str(source.get("integration_status", "cycle_gate_reentry_integration_block"))
    if integration_status not in FLOW:
        blockers.append("v13_31_integration_status_invalid")
        integration_status = "cycle_gate_reentry_integration_block"
    expected_gate, expected_set, expected_count = FLOW[integration_status]
    gate_status = str(source.get("integrated_cycle_gate_status", expected_gate))
    set_status = str(source.get("integrated_admissible_candidate_set_status", expected_set))
    if gate_status != expected_gate:
        blockers.append("v13_31_integrated_cycle_gate_status_mismatch")
        gate_status = expected_gate
    if set_status != expected_set:
        blockers.append("v13_31_integrated_candidate_set_status_mismatch")
        set_status = expected_set

    if source:
        if source.get("activation_status") != "cycle_gate_reentry_integration_activation_completed":
            blockers.append("v13_31_activation_not_completed")
        if not source.get("cycle_gate_reentry_integration_activation_record_digest"):
            blockers.append("v13_31_activation_record_digest_missing")
        if str(source.get("source_v13_4_integration_packet_digest", "")) != str(packet.get("cycle_gate_reentry_integration_digest", "")):
            blockers.append("v13_31_integration_packet_digest_mismatch")
        if str(source.get("source_v13_4_integration_record_digest", "")) != str(integration_record.get("record_digest", "")):
            blockers.append("v13_31_integration_record_digest_mismatch")
    if packet:
        if str(packet.get("integration_status", "")) != integration_status:
            blockers.append("v13_4_packet_integration_status_mismatch")
        if str(packet.get("integrated_cycle_gate_status", "")) != gate_status:
            blockers.append("v13_4_packet_gate_status_mismatch")
        if str(packet.get("integrated_admissible_candidate_set_status", "")) != set_status:
            blockers.append("v13_4_packet_candidate_set_status_mismatch")
        candidates = packet.get("integrated_candidates", [])
        count = len(candidates) if isinstance(candidates, list) else 0
        if count != expected_count:
            blockers.append("v13_4_packet_candidate_count_mismatch")
    else:
        count = expected_count
    if integration_record:
        if integration_record.get("record_type") != "physical_quantum_qi_cycle_gate_reentry_integration":
            blockers.append("v13_4_integration_record_type_invalid")
        if str(integration_record.get("source_cycle_gate_reentry_integration_digest", "")) != str(packet.get("cycle_gate_reentry_integration_digest", "")):
            blockers.append("v13_4_integration_record_packet_digest_mismatch")

    bridge_invoked = ledger_invoked = False
    bridge: dict[str, Any] = {}
    ledger: dict[str, Any] = {}
    if not blockers:
        bridge = build_physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge(
            runtime_context={"physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge_enabled": True, "apply_physical_quantum_qi_v13_4_to_v13_5_integration_receipt_bridge": True, "runtime_root": str(root)},
            v13_4_to_v13_5_integration_receipt_bridge_license=dict(_m(lic.get("v13_17_bridge_license"))),
        ).to_dict()
        bridge_invoked = True
        if bridge.get("status") != "PHYSICAL_QUANTUM_QI_V13_4_TO_V13_5_INTEGRATION_RECEIPT_BRIDGE_READY":
            blockers.append("v13_17_bridge_not_ready")
        if str(bridge.get("integration_status", "")) != integration_status or str(bridge.get("integrated_cycle_gate_status", "")) != gate_status or str(bridge.get("integrated_admissible_candidate_set_status", "")) != set_status or int(bridge.get("admissible_candidate_count", -1)) != expected_count:
            blockers.append("v13_17_bridge_output_mismatch")

    if bridge_invoked and not blockers:
        ledger = build_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger(
            runtime_context={"physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_enabled": True, "apply_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger": True, "runtime_root": str(root)},
            cycle_gate_reentry_integration_receipt_ledger_license=dict(_m(lic.get("v13_5_receipt_ledger_license"))),
        ).to_dict()
        ledger_invoked = True
        if ledger.get("status") != "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_READY":
            blockers.append("v13_5_receipt_ledger_not_ready")
        if str(ledger.get("integration_status", "")) != integration_status or str(ledger.get("integrated_cycle_gate_status", "")) != gate_status or str(ledger.get("integrated_admissible_candidate_set_status", "")) != set_status or int(ledger.get("admissible_candidate_count", -1)) != expected_count:
            blockers.append("v13_5_receipt_ledger_output_mismatch")

    ledger_receipt = _read_json(root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_receipt.json")
    receipt_record = _latest(root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl")
    if ledger_invoked and (not str(ledger_receipt.get("record_digest", "")) or ledger_receipt.get("record_digest") != receipt_record.get("record_digest")):
        blockers.append("v13_5_receipt_record_digest_missing_or_mismatch")

    activation_status = "integration_receipt_activation_completed" if bridge_invoked and ledger_invoked and not blockers else "integration_receipt_activation_blocked"
    if bridge_invoked or ledger_invoked:
        ready_state = _read_json(root / "physical_quantum_qi_v13_5_cycle_gate_reentry_integration_receipt_ready_state.json")
        record = {
            "version": "physical_quantum_qi_v13_32_integration_receipt_activation_record",
            "activation_status": activation_status,
            "integration_status": integration_status,
            "integrated_cycle_gate_status": gate_status,
            "integrated_admissible_candidate_set_status": set_status,
            "admissible_candidate_count": expected_count,
            "source_v13_31_activation_record_digest": str(source.get("cycle_gate_reentry_integration_activation_record_digest", "")),
            "source_v13_4_integration_packet_digest": str(packet.get("cycle_gate_reentry_integration_digest", "")),
            "source_v13_4_integration_record_digest": str(integration_record.get("record_digest", "")),
            "source_v13_17_receipt_ready_state_digest": str(ready_state.get("integration_receipt_ready_state_digest", "")),
            "source_v13_5_receipt_record_digest": str(receipt_record.get("record_digest", "")),
            "boundary": {"two_stage_integration_receipt_activation": True, "uses_process_tensor_feedback": True, "non_markov_feedback_preserved": True, "candidate_weighting_not_truth": True, "not_direct_execution_authority": True, "license_gated_receipt_activation": True, "runtime_local_external_state_only": True, "fail_closed_on_boundary_loss": True},
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        record["integration_receipt_activation_record_digest"] = _sha(record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(record_path, record)

    status = "PHYSICAL_QUANTUM_QI_V13_32_INTEGRATION_RECEIPT_ACTIVATION_READY" if bridge_invoked and ledger_invoked and not blockers else "PHYSICAL_QUANTUM_QI_V13_32_INTEGRATION_RECEIPT_ACTIVATION_BLOCKED"
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_32_integration_receipt_activation",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-32-integration-receipt-activation-" + _sha({"integration": integration_status, "blockers": blockers})[:16],
        "activation_status": activation_status,
        "integration_status": integration_status,
        "integrated_cycle_gate_status": gate_status,
        "integrated_admissible_candidate_set_status": set_status,
        "admissible_candidate_count": expected_count,
        "v13_17_bridge_invoked": bridge_invoked,
        "v13_5_receipt_ledger_invoked": ledger_invoked,
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
    return PhysicalQuantumQiV13_32IntegrationReceiptActivationResult(
        receipt["version"], status, receipt["packet_id"], str(root), activation_status, integration_status, gate_status, set_status, expected_count,
        bridge_invoked, ledger_invoked, receipt["receipt_ready_state_written"], receipt["bridge_ledger_appended"], receipt["receipt_ledger_appended"],
        str(record_path), str(receipt_path), str(audit_path), blockers, warnings,
    )
