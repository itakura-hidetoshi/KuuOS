#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_v13_6 import build_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_v13_18 import build_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge

FLOW = {
    "cycle_gate_reentry_integration_admit": ("integrated_candidate_to_guarded_intent_ready", "guarded_execution_intent_ready", "emit_guarded_ready_intent", 1),
    "cycle_gate_reentry_integration_hold": ("integrated_candidate_to_guarded_intent_hold", "guarded_execution_intent_hold", "emit_guarded_hold_intent", 0),
    "cycle_gate_reentry_integration_block": ("integrated_candidate_to_guarded_intent_block", "guarded_execution_intent_block", "emit_guarded_block_intent", 0),
}


@dataclass(frozen=True)
class PhysicalQuantumQiV13_33GuardedIntentActivationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    integration_status: str
    bridge_status: str
    guarded_execution_intent_status: str
    guarded_intent_emit_action: str
    guarded_execution_intent_count: int
    v13_18_bridge_invoked: bool
    v13_6_guarded_intent_bridge_invoked: bool
    guarded_intent_ready_state_written: bool
    bridge_packet_written: bool
    guarded_execution_intent_packet_written: bool
    bridge_state_written: bool
    bridge_ledger_appended: bool
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


def build_physical_quantum_qi_v13_33_guarded_intent_activation(*, runtime_context: Mapping[str, Any], v13_33_guarded_intent_activation_license: Mapping[str, Any]) -> PhysicalQuantumQiV13_33GuardedIntentActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_33_guarded_intent_activation_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_path = root / "physical_quantum_qi_v13_32_integration_receipt_activation_record.json"
    receipt_ledger_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl"
    record_path = root / "physical_quantum_qi_v13_33_guarded_intent_activation_record.json"
    receipt_path = root / "physical_quantum_qi_v13_33_guarded_intent_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_33_guarded_intent_activation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_33_guarded_intent_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_33_guarded_intent_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_33_guarded_intent_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_33_guarded_intent_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_33_GUARDED_INTENT_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_33_guarded_intent_activation_license_not_ready")
    for flag in (
        "v13_32_activation_record_read_allowed",
        "v13_5_receipt_ledger_read_allowed",
        "v13_18_bridge_invoke_allowed",
        "v13_6_guarded_intent_bridge_invoke_allowed",
        "activation_record_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source = _read_json(source_path)
    receipt_record = _latest(receipt_ledger_path)
    if not source:
        blockers.append("v13_32_activation_record_missing_or_invalid")
    if not receipt_record:
        blockers.append("v13_5_receipt_record_missing_or_invalid")

    integration_status = str(source.get("integration_status", "cycle_gate_reentry_integration_block"))
    if integration_status not in FLOW:
        blockers.append("v13_32_integration_status_invalid")
        integration_status = "cycle_gate_reentry_integration_block"
    bridge_status, guarded_status, emit_action, expected_count = FLOW[integration_status]

    if source:
        if source.get("activation_status") != "integration_receipt_activation_completed":
            blockers.append("v13_32_activation_not_completed")
        if not source.get("integration_receipt_activation_record_digest"):
            blockers.append("v13_32_activation_record_digest_missing")
        if str(source.get("source_v13_5_receipt_record_digest", "")) != str(receipt_record.get("record_digest", "")):
            blockers.append("v13_32_receipt_record_digest_mismatch")
        if int(source.get("admissible_candidate_count", -1)) != int(receipt_record.get("admissible_candidate_count", -2)):
            blockers.append("v13_32_candidate_count_mismatch")
    if receipt_record:
        if receipt_record.get("record_type") != "physical_quantum_qi_cycle_gate_reentry_integration_receipt":
            blockers.append("v13_5_receipt_record_type_invalid")
        if str(receipt_record.get("integration_status", "")) != integration_status:
            blockers.append("v13_5_receipt_integration_status_mismatch")
        candidates = receipt_record.get("integrated_candidates", [])
        if not isinstance(candidates, list):
            blockers.append("v13_5_receipt_integrated_candidates_not_list")
            candidates = []
        expected_source_count = 0 if integration_status == "cycle_gate_reentry_integration_block" else 1
        if int(receipt_record.get("admissible_candidate_count", -1)) != expected_source_count or len(candidates) != expected_source_count:
            blockers.append("v13_5_receipt_candidate_count_mismatch")

    v13_18_invoked = v13_6_invoked = False
    bridge: dict[str, Any] = {}
    guarded: dict[str, Any] = {}
    if not blockers:
        bridge = build_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge(
            runtime_context={
                "physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge_enabled": True,
                "apply_physical_quantum_qi_v13_5_to_v13_6_guarded_intent_bridge": True,
                "runtime_root": str(root),
            },
            v13_5_to_v13_6_guarded_intent_bridge_license=dict(_m(lic.get("v13_18_bridge_license"))),
        ).to_dict()
        v13_18_invoked = True
        if bridge.get("status") != "PHYSICAL_QUANTUM_QI_V13_5_TO_V13_6_GUARDED_INTENT_BRIDGE_READY":
            blockers.append("v13_18_bridge_not_ready")
        if (
            str(bridge.get("bridge_status", "")) != bridge_status
            or str(bridge.get("guarded_execution_intent_status", "")) != guarded_status
            or str(bridge.get("guarded_intent_emit_action", "")) != emit_action
            or int(bridge.get("expected_guarded_execution_intent_count", -1)) != expected_count
        ):
            blockers.append("v13_18_bridge_output_mismatch")

    if v13_18_invoked and not blockers:
        guarded = build_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge(
            runtime_context={
                "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_enabled": True,
                "apply_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge": True,
                "runtime_root": str(root),
            },
            integrated_candidate_to_guarded_intent_bridge_license=dict(_m(lic.get("v13_6_guarded_intent_bridge_license"))),
        ).to_dict()
        v13_6_invoked = True
        if guarded.get("status") != "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_READY":
            blockers.append("v13_6_guarded_intent_bridge_not_ready")
        if (
            str(guarded.get("bridge_status", "")) != bridge_status
            or str(guarded.get("guarded_execution_intent_status", "")) != guarded_status
            or str(guarded.get("guarded_intent_emit_action", "")) != emit_action
            or int(guarded.get("guarded_execution_intent_count", -1)) != expected_count
        ):
            blockers.append("v13_6_guarded_intent_bridge_output_mismatch")

    ready_state = _read_json(root / "physical_quantum_qi_v13_6_integrated_candidate_to_guarded_intent_ready_state.json")
    bridge_packet = _read_json(root / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_packet.json")
    intent_packet = _read_json(root / "physical_quantum_qi_guarded_execution_intent_packet.json")
    bridge_record = _latest(root / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_ledger.jsonl")
    if v13_6_invoked:
        if not str(ready_state.get("guarded_intent_bridge_ready_state_digest", "")):
            blockers.append("v13_18_ready_state_digest_missing")
        if not str(bridge_packet.get("integrated_candidate_to_guarded_intent_bridge_digest", "")):
            blockers.append("v13_6_bridge_packet_digest_missing")
        if not str(intent_packet.get("guarded_execution_intent_packet_digest", "")):
            blockers.append("v13_6_guarded_intent_packet_digest_missing")
        if not str(bridge_record.get("record_digest", "")):
            blockers.append("v13_6_bridge_record_digest_missing")
        if str(bridge_record.get("source_integrated_candidate_to_guarded_intent_bridge_digest", "")) != str(bridge_packet.get("integrated_candidate_to_guarded_intent_bridge_digest", "")):
            blockers.append("v13_6_bridge_record_packet_digest_mismatch")
        if str(bridge_record.get("source_guarded_execution_intent_packet_digest", "")) != str(intent_packet.get("guarded_execution_intent_packet_digest", "")):
            blockers.append("v13_6_bridge_record_intent_digest_mismatch")

    activation_status = "guarded_intent_activation_completed" if v13_18_invoked and v13_6_invoked and not blockers else "guarded_intent_activation_blocked"
    if v13_18_invoked or v13_6_invoked:
        record = {
            "version": "physical_quantum_qi_v13_33_guarded_intent_activation_record",
            "activation_status": activation_status,
            "integration_status": integration_status,
            "bridge_status": bridge_status,
            "guarded_execution_intent_status": guarded_status,
            "guarded_intent_emit_action": emit_action,
            "guarded_execution_intent_count": expected_count,
            "source_v13_32_activation_record_digest": str(source.get("integration_receipt_activation_record_digest", "")),
            "source_v13_5_receipt_record_digest": str(receipt_record.get("record_digest", "")),
            "source_v13_18_ready_state_digest": str(ready_state.get("guarded_intent_bridge_ready_state_digest", "")),
            "source_v13_6_bridge_packet_digest": str(bridge_packet.get("integrated_candidate_to_guarded_intent_bridge_digest", "")),
            "source_v13_6_guarded_intent_packet_digest": str(intent_packet.get("guarded_execution_intent_packet_digest", "")),
            "source_v13_6_bridge_record_digest": str(bridge_record.get("record_digest", "")),
            "boundary": {
                "two_stage_guarded_intent_activation": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "guarded_intent_not_world_mutation": True,
                "not_direct_execution_authority": True,
                "license_gated_guarded_intent": True,
                "runtime_local_external_state_only": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        record["guarded_intent_activation_record_digest"] = _sha(record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(record_path, record)

    status = "PHYSICAL_QUANTUM_QI_V13_33_GUARDED_INTENT_ACTIVATION_READY" if v13_18_invoked and v13_6_invoked and not blockers else "PHYSICAL_QUANTUM_QI_V13_33_GUARDED_INTENT_ACTIVATION_BLOCKED"
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_33_guarded_intent_activation",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-33-guarded-intent-activation-" + _sha({"integration": integration_status, "blockers": blockers})[:16],
        "activation_status": activation_status,
        "integration_status": integration_status,
        "bridge_status": bridge_status,
        "guarded_execution_intent_status": guarded_status,
        "guarded_intent_emit_action": emit_action,
        "guarded_execution_intent_count": expected_count,
        "v13_18_bridge_invoked": v13_18_invoked,
        "v13_6_guarded_intent_bridge_invoked": v13_6_invoked,
        "guarded_intent_ready_state_written": bridge.get("guarded_intent_ready_state_written") is True,
        "bridge_packet_written": guarded.get("bridge_packet_written") is True,
        "guarded_execution_intent_packet_written": guarded.get("guarded_execution_intent_packet_written") is True,
        "bridge_state_written": guarded.get("bridge_state_written") is True,
        "bridge_ledger_appended": guarded.get("bridge_ledger_appended") is True,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiV13_33GuardedIntentActivationResult(
        receipt["version"], status, receipt["packet_id"], str(root), activation_status, integration_status,
        bridge_status, guarded_status, emit_action, expected_count, v13_18_invoked, v13_6_invoked,
        receipt["guarded_intent_ready_state_written"], receipt["bridge_packet_written"],
        receipt["guarded_execution_intent_packet_written"], receipt["bridge_state_written"],
        receipt["bridge_ledger_appended"], str(record_path), str(receipt_path), str(audit_path), blockers, warnings,
    )
