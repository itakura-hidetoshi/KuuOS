#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_v13_4 import build_physical_quantum_qi_cycle_gate_reentry_integration
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_3_to_v13_4_integration_bridge_v13_16 import build_physical_quantum_qi_v13_3_to_v13_4_integration_bridge

FLOW = {
    "candidate_weighting_cycle_handoff_reinforce": ("cycle_gate_reentry_integration_admit", "integrated_cycle_gate_admit", "integrated_admissible_candidate_set_admit"),
    "candidate_weighting_cycle_handoff_probe": ("cycle_gate_reentry_integration_hold", "integrated_cycle_gate_hold", "integrated_admissible_candidate_set_probe"),
    "candidate_weighting_cycle_handoff_barrier": ("cycle_gate_reentry_integration_block", "integrated_cycle_gate_block", "integrated_admissible_candidate_set_block"),
}


@dataclass(frozen=True)
class PhysicalQuantumQiV13_31CycleGateReentryIntegrationActivationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    handoff_status: str
    integration_status: str
    integrated_cycle_gate_status: str
    integrated_admissible_candidate_set_status: str
    v13_16_bridge_invoked: bool
    v13_4_integration_invoked: bool
    integration_ready_state_written: bool
    integration_packet_written: bool
    integrated_cycle_gate_state_written: bool
    integrated_admissible_candidate_set_written: bool
    integration_ledger_appended: bool
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


def build_physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation(*, runtime_context: Mapping[str, Any], v13_31_cycle_gate_reentry_integration_activation_license: Mapping[str, Any]) -> PhysicalQuantumQiV13_31CycleGateReentryIntegrationActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_31_cycle_gate_reentry_integration_activation_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_path = root / "physical_quantum_qi_v13_30_handoff_receipt_activation_record.json"
    receipt_ledger_path = root / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl"
    record_path = root / "physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_record.json"
    receipt_path = root / "physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_31_CYCLE_GATE_REENTRY_INTEGRATION_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_license_not_ready")
    for flag in ("v13_30_activation_record_read_allowed", "v13_3_receipt_ledger_read_allowed", "v13_16_bridge_invoke_allowed", "v13_4_integration_invoke_allowed", "activation_record_write_allowed", "receipt_write_allowed", "audit_append_allowed"):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source = _read_json(source_path)
    receipt_record = _latest(receipt_ledger_path)
    if not source:
        blockers.append("v13_30_activation_record_missing_or_invalid")
    if not receipt_record:
        blockers.append("v13_3_receipt_record_missing_or_invalid")

    handoff_status = str(source.get("handoff_status", "candidate_weighting_cycle_handoff_barrier"))
    if handoff_status not in FLOW:
        blockers.append("v13_30_handoff_status_invalid")
        handoff_status = "candidate_weighting_cycle_handoff_barrier"
    expected_integration, expected_cycle, expected_set = FLOW[handoff_status]

    if source:
        if source.get("activation_status") != "handoff_receipt_activation_completed":
            blockers.append("v13_30_activation_not_completed")
        if not source.get("handoff_receipt_activation_record_digest"):
            blockers.append("v13_30_activation_record_digest_missing")
        if str(source.get("source_v13_3_receipt_record_digest", "")) != str(receipt_record.get("record_digest", "")):
            blockers.append("v13_30_receipt_record_digest_mismatch")
    if receipt_record:
        if receipt_record.get("record_type") != "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt":
            blockers.append("v13_3_receipt_record_type_invalid")
        if str(receipt_record.get("handoff_status", "")) != handoff_status:
            blockers.append("v13_3_receipt_handoff_status_mismatch")

    bridge_invoked = integration_invoked = False
    bridge: dict[str, Any] = {}
    integration: dict[str, Any] = {}
    if not blockers:
        bridge = build_physical_quantum_qi_v13_3_to_v13_4_integration_bridge(
            runtime_context={"physical_quantum_qi_v13_3_to_v13_4_integration_bridge_enabled": True, "apply_physical_quantum_qi_v13_3_to_v13_4_integration_bridge": True, "runtime_root": str(root)},
            v13_3_to_v13_4_integration_bridge_license=dict(_m(lic.get("v13_16_bridge_license"))),
        ).to_dict()
        bridge_invoked = True
        if bridge.get("status") != "PHYSICAL_QUANTUM_QI_V13_3_TO_V13_4_INTEGRATION_BRIDGE_READY":
            blockers.append("v13_16_bridge_not_ready")
        if str(bridge.get("expected_v13_4_integration_status", "")) != expected_integration or str(bridge.get("expected_v13_4_integrated_cycle_gate_status", "")) != expected_cycle or str(bridge.get("expected_v13_4_integrated_admissible_candidate_set_status", "")) != expected_set:
            blockers.append("v13_16_bridge_output_mismatch")

    if bridge_invoked and not blockers:
        integration = build_physical_quantum_qi_cycle_gate_reentry_integration(
            runtime_context={"physical_quantum_qi_cycle_gate_reentry_integration_enabled": True, "apply_physical_quantum_qi_cycle_gate_reentry_integration": True, "runtime_root": str(root)},
            cycle_gate_reentry_integration_license=dict(_m(lic.get("v13_4_integration_license"))),
        ).to_dict()
        integration_invoked = True
        if integration.get("status") != "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_READY":
            blockers.append("v13_4_integration_not_ready")
        if str(integration.get("integration_status", "")) != expected_integration or str(integration.get("integrated_cycle_gate_status", "")) != expected_cycle or str(integration.get("integrated_admissible_candidate_set_status", "")) != expected_set:
            blockers.append("v13_4_integration_output_mismatch")

    integration_record = _latest(root / "physical_quantum_qi_cycle_gate_reentry_integration_ledger.jsonl")
    if integration_invoked and not str(integration_record.get("record_digest", "")):
        blockers.append("v13_4_integration_record_digest_missing")

    activation_status = "cycle_gate_reentry_integration_activation_completed" if bridge_invoked and integration_invoked and not blockers else "cycle_gate_reentry_integration_activation_blocked"
    if bridge_invoked or integration_invoked:
        ready_state = _read_json(root / "physical_quantum_qi_v13_4_cycle_gate_reentry_integration_ready_state.json")
        packet = _read_json(root / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json")
        record = {
            "version": "physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation_record",
            "activation_status": activation_status,
            "handoff_status": handoff_status,
            "integration_status": str(integration.get("integration_status", expected_integration)),
            "integrated_cycle_gate_status": str(integration.get("integrated_cycle_gate_status", expected_cycle)),
            "integrated_admissible_candidate_set_status": str(integration.get("integrated_admissible_candidate_set_status", expected_set)),
            "source_v13_30_activation_record_digest": str(source.get("handoff_receipt_activation_record_digest", "")),
            "source_v13_3_receipt_record_digest": str(receipt_record.get("record_digest", "")),
            "source_v13_16_integration_ready_state_digest": str(ready_state.get("integration_ready_state_digest", "")),
            "source_v13_4_integration_packet_digest": str(packet.get("cycle_gate_reentry_integration_digest", "")),
            "source_v13_4_integration_record_digest": str(integration_record.get("record_digest", "")),
            "boundary": {"two_stage_cycle_gate_reentry_integration_activation": True, "uses_process_tensor_feedback": True, "non_markov_feedback_preserved": True, "candidate_weighting_not_truth": True, "not_direct_execution_authority": True, "license_gated_integration": True, "runtime_local_external_state_only": True, "fail_closed_on_boundary_loss": True},
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        record["cycle_gate_reentry_integration_activation_record_digest"] = _sha(record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(record_path, record)

    status = "PHYSICAL_QUANTUM_QI_V13_31_CYCLE_GATE_REENTRY_INTEGRATION_ACTIVATION_READY" if bridge_invoked and integration_invoked and not blockers else "PHYSICAL_QUANTUM_QI_V13_31_CYCLE_GATE_REENTRY_INTEGRATION_ACTIVATION_BLOCKED"
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_31_cycle_gate_reentry_integration_activation",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-31-cycle-gate-reentry-integration-activation-" + _sha({"integration": expected_integration, "blockers": blockers})[:16],
        "activation_status": activation_status,
        "handoff_status": handoff_status,
        "integration_status": str(integration.get("integration_status", expected_integration)),
        "integrated_cycle_gate_status": str(integration.get("integrated_cycle_gate_status", expected_cycle)),
        "integrated_admissible_candidate_set_status": str(integration.get("integrated_admissible_candidate_set_status", expected_set)),
        "v13_16_bridge_invoked": bridge_invoked,
        "v13_4_integration_invoked": integration_invoked,
        "integration_ready_state_written": bridge.get("integration_ready_state_written") is True,
        "integration_packet_written": integration.get("integration_packet_written") is True,
        "integrated_cycle_gate_state_written": integration.get("integrated_cycle_gate_state_written") is True,
        "integrated_admissible_candidate_set_written": integration.get("integrated_admissible_candidate_set_written") is True,
        "integration_ledger_appended": integration.get("integration_ledger_appended") is True,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiV13_31CycleGateReentryIntegrationActivationResult(
        receipt["version"], status, receipt["packet_id"], str(root), activation_status, handoff_status,
        receipt["integration_status"], receipt["integrated_cycle_gate_status"], receipt["integrated_admissible_candidate_set_status"],
        bridge_invoked, integration_invoked, receipt["integration_ready_state_written"], receipt["integration_packet_written"],
        receipt["integrated_cycle_gate_state_written"], receipt["integrated_admissible_candidate_set_written"], receipt["integration_ledger_appended"],
        str(record_path), str(receipt_path), str(audit_path), blockers, warnings,
    )
