#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_closed_loop_reentry_receipt_ledger_v13_1 import (
    build_physical_quantum_qi_closed_loop_reentry_receipt_ledger,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_v13_13 import (
    build_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge,
)

EXPECTED_ACTION = {
    "closed_loop_reentry_reinforced": "reinforce_path_weight",
    "closed_loop_reentry_probe_opened": "open_probe_potential",
    "closed_loop_reentry_barrier_added": "add_barrier_potential",
}


@dataclass(frozen=True)
class PhysicalQuantumQiV13_28ClosedLoopReentryReceiptActivationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    closed_loop_reentry_status: str
    reentry_weighting_action: str
    v13_13_receipt_bridge_invoked: bool
    v13_1_receipt_ledger_invoked: bool
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
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


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


def build_physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation(
    *,
    runtime_context: Mapping[str, Any],
    v13_28_closed_loop_reentry_receipt_activation_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_28ClosedLoopReentryReceiptActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_28_closed_loop_reentry_receipt_activation_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_activation_path = root / "physical_quantum_qi_v13_27_closed_loop_reentry_activation_record.json"
    packet_path = root / "physical_quantum_qi_closed_loop_path_integral_reentry_packet.json"
    cycle_state_path = root / "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state.json"
    activation_record_path = root / "physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation_record.json"
    receipt_path = root / "physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_28_CLOSED_LOOP_REENTRY_RECEIPT_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation_license_not_ready")
    for flag in (
        "v13_27_activation_record_read_allowed",
        "v13_0_closed_loop_packet_read_allowed",
        "v13_0_candidate_weighting_cycle_state_read_allowed",
        "v13_13_receipt_bridge_invoke_allowed",
        "v13_1_receipt_ledger_invoke_allowed",
        "activation_record_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source_activation = _read_json(source_activation_path)
    packet = _read_json(packet_path)
    cycle = _read_json(cycle_state_path)
    if not source_activation:
        blockers.append("v13_27_closed_loop_reentry_activation_record_missing_or_invalid")
    if not packet:
        blockers.append("v13_0_closed_loop_reentry_packet_missing_or_invalid")
    if not cycle:
        blockers.append("v13_0_candidate_weighting_cycle_state_missing_or_invalid")

    closed_status = str(packet.get("closed_loop_reentry_status", "closed_loop_reentry_barrier_added"))
    if closed_status not in EXPECTED_ACTION:
        blockers.append("v13_0_closed_loop_reentry_status_invalid")
        closed_status = "closed_loop_reentry_barrier_added"
    action = str(packet.get("reentry_weighting_action", "add_barrier_potential"))
    if action != EXPECTED_ACTION[closed_status]:
        blockers.append("v13_0_closed_loop_reentry_action_mismatch")
        action = EXPECTED_ACTION[closed_status]

    if source_activation:
        if source_activation.get("activation_status") != "closed_loop_reentry_activation_completed":
            blockers.append("v13_27_closed_loop_reentry_activation_not_completed")
        if str(source_activation.get("observed_closed_loop_reentry_status", "")) != closed_status:
            blockers.append("v13_27_closed_loop_reentry_status_mismatch")
        if str(source_activation.get("reentry_weighting_action", "")) != action:
            blockers.append("v13_27_reentry_weighting_action_mismatch")
        source_cycle_digest = str(source_activation.get("source_v13_0_candidate_weighting_cycle_state_digest", ""))
        actual_cycle_digest = str(cycle.get("candidate_weighting_cycle_state_digest", ""))
        if not source_cycle_digest or source_cycle_digest != actual_cycle_digest:
            blockers.append("v13_27_candidate_weighting_cycle_state_digest_mismatch")

    if packet and cycle:
        packet_digest = str(packet.get("closed_loop_path_integral_reentry_digest", ""))
        cycle_source_digest = str(cycle.get("source_closed_loop_path_integral_reentry_digest", ""))
        if not packet_digest or packet_digest != cycle_source_digest:
            blockers.append("v13_0_packet_cycle_digest_mismatch")
        if str(cycle.get("closed_loop_reentry_status", "")) != closed_status:
            blockers.append("v13_0_packet_cycle_status_mismatch")
        if str(cycle.get("reentry_weighting_action", "")) != action:
            blockers.append("v13_0_packet_cycle_action_mismatch")
        if cycle.get("candidate_weighting_cycle_ready") is not True:
            blockers.append("v13_0_candidate_weighting_cycle_state_not_ready")

    v13_13_invoked = False
    v13_1_invoked = False
    bridge_result: dict[str, Any] = {}
    ledger_result: dict[str, Any] = {}

    if not blockers:
        bridge_result = build_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge(
            runtime_context={
                "physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_enabled": True,
                "apply_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge": True,
                "runtime_root": str(root),
            },
            v13_0_to_v13_1_reentry_receipt_bridge_license=dict(_m(lic.get("v13_13_receipt_bridge_license"))),
        ).to_dict()
        v13_13_invoked = True
        if bridge_result.get("status") != "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_READY":
            blockers.append("v13_13_reentry_receipt_bridge_not_ready")
        if str(bridge_result.get("closed_loop_reentry_status", "")) != closed_status:
            blockers.append("v13_13_closed_loop_reentry_status_mismatch")
        if str(bridge_result.get("reentry_weighting_action", "")) != action:
            blockers.append("v13_13_reentry_weighting_action_mismatch")

    if v13_13_invoked and not blockers:
        ledger_result = build_physical_quantum_qi_closed_loop_reentry_receipt_ledger(
            runtime_context={
                "physical_quantum_qi_closed_loop_reentry_receipt_ledger_enabled": True,
                "apply_physical_quantum_qi_closed_loop_reentry_receipt_ledger": True,
                "runtime_root": str(root),
            },
            closed_loop_reentry_receipt_ledger_license=dict(_m(lic.get("v13_1_receipt_ledger_license"))),
        ).to_dict()
        v13_1_invoked = True
        if ledger_result.get("status") != "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_READY":
            blockers.append("v13_1_closed_loop_reentry_receipt_ledger_not_ready")
        if str(ledger_result.get("closed_loop_reentry_status", "")) != closed_status:
            blockers.append("v13_1_closed_loop_reentry_status_mismatch")
        if str(ledger_result.get("reentry_weighting_action", "")) != action:
            blockers.append("v13_1_reentry_weighting_action_mismatch")

    activation_status = (
        "closed_loop_reentry_receipt_activation_completed"
        if v13_13_invoked and v13_1_invoked and not blockers
        else "closed_loop_reentry_receipt_activation_blocked"
    )

    if v13_13_invoked or v13_1_invoked:
        ready_state = _read_json(root / "physical_quantum_qi_v13_1_closed_loop_reentry_receipt_ready_state.json")
        ledger_receipt = _read_json(root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger_receipt.json")
        record = {
            "version": "physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation_record",
            "activation_status": activation_status,
            "closed_loop_reentry_status": closed_status,
            "reentry_weighting_action": action,
            "source_v13_27_closed_loop_reentry_activation_record_digest": str(
                source_activation.get("closed_loop_reentry_activation_record_digest", "")
            ),
            "source_v13_0_closed_loop_path_integral_reentry_digest": str(
                packet.get("closed_loop_path_integral_reentry_digest", "")
            ),
            "source_v13_0_candidate_weighting_cycle_state_digest": str(
                cycle.get("candidate_weighting_cycle_state_digest", "")
            ),
            "source_v13_13_reentry_receipt_ready_state_digest": str(
                ready_state.get("closed_loop_reentry_receipt_ready_state_digest", "")
            ),
            "source_v13_1_reentry_receipt_record_digest": str(ledger_receipt.get("record_digest", "")),
            "boundary": {
                "two_stage_closed_loop_reentry_receipt_activation": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "license_gated_receipt_activation": True,
                "runtime_local_external_state_only": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        record["closed_loop_reentry_receipt_activation_record_digest"] = _sha(record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(activation_record_path, record)

    status = (
        "PHYSICAL_QUANTUM_QI_V13_28_CLOSED_LOOP_REENTRY_RECEIPT_ACTIVATION_READY"
        if v13_13_invoked and v13_1_invoked and not blockers
        else "PHYSICAL_QUANTUM_QI_V13_28_CLOSED_LOOP_REENTRY_RECEIPT_ACTIVATION_BLOCKED"
    )
    packet_id = "physical-quantum-qi-v13-28-closed-loop-reentry-receipt-activation-" + _sha(
        {"closed_loop_reentry_status": closed_status, "action": action, "blockers": blockers}
    )[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation",
        "status": status,
        "packet_id": packet_id,
        "activation_status": activation_status,
        "closed_loop_reentry_status": closed_status,
        "reentry_weighting_action": action,
        "v13_13_receipt_bridge_invoked": v13_13_invoked,
        "v13_1_receipt_ledger_invoked": v13_1_invoked,
        "receipt_ready_state_written": bridge_result.get("receipt_ready_state_written") is True,
        "bridge_ledger_appended": bridge_result.get("bridge_ledger_appended") is True,
        "receipt_ledger_appended": ledger_result.get("ledger_appended") is True,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_28ClosedLoopReentryReceiptActivationResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation",
        status,
        packet_id,
        str(root),
        activation_status,
        closed_status,
        action,
        v13_13_invoked,
        v13_1_invoked,
        bridge_result.get("receipt_ready_state_written") is True,
        bridge_result.get("bridge_ledger_appended") is True,
        ledger_result.get("ledger_appended") is True,
        str(activation_record_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
