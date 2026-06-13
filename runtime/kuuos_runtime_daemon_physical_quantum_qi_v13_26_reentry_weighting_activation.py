#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_process_tensor_feedback_receipt_ledger_v12_8 import (
    build_physical_quantum_qi_process_tensor_feedback_receipt_ledger,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_feedback_to_reentry_weighting_bridge_v12_9 import (
    build_physical_quantum_qi_feedback_to_reentry_weighting_bridge,
)

EXPECTED = {
    "process_tensor_feedback_reinforce_next_cycle": ("reentry_weighting_reinforce", "reinforce_path_weight"),
    "process_tensor_feedback_hold_context": ("reentry_weighting_hold", "open_probe_potential"),
    "process_tensor_feedback_block_context": ("reentry_weighting_block", "add_barrier_potential"),
}


@dataclass(frozen=True)
class PhysicalQuantumQiV13_26ReentryWeightingActivationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    feedback_status: str
    expected_reentry_weighting_status: str
    observed_reentry_weighting_status: str
    observed_reentry_weighting_action: str
    v12_8_receipt_ledger_invoked: bool
    v12_9_reentry_bridge_invoked: bool
    receipt_ledger_appended: bool
    reentry_weighting_packet_written: bool
    reentry_weighting_state_updated: bool
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


def build_physical_quantum_qi_v13_26_reentry_weighting_activation(
    *,
    runtime_context: Mapping[str, Any],
    v13_26_reentry_weighting_activation_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_26ReentryWeightingActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_26_reentry_weighting_activation_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    activation_path = root / "physical_quantum_qi_v13_25_feedback_receipt_activation_record.json"
    ready_state_path = root / "physical_quantum_qi_v12_8_process_tensor_feedback_receipt_ready_state.json"
    packet_path = root / "physical_quantum_qi_process_tensor_execution_feedback_packet.json"
    state_path = root / "physical_quantum_qi_path_integral_feedback_state.json"
    output_record_path = root / "physical_quantum_qi_v13_26_reentry_weighting_activation_record.json"
    receipt_path = root / "physical_quantum_qi_v13_26_reentry_weighting_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_26_reentry_weighting_activation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_26_reentry_weighting_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_26_reentry_weighting_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_26_reentry_weighting_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_26_reentry_weighting_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_26_REENTRY_WEIGHTING_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_26_reentry_weighting_activation_license_not_ready")
    for flag in (
        "v13_25_activation_record_read_allowed",
        "v12_8_feedback_receipt_ready_state_read_allowed",
        "v12_8_receipt_ledger_invoke_allowed",
        "v12_9_reentry_bridge_invoke_allowed",
        "activation_record_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source_activation = _read_json(activation_path)
    ready_state = _read_json(ready_state_path)
    feedback_packet = _read_json(packet_path)
    path_state = _read_json(state_path)

    if not source_activation:
        blockers.append("v13_25_feedback_receipt_activation_record_missing_or_invalid")
    if not ready_state:
        blockers.append("v12_8_feedback_receipt_ready_state_missing_or_invalid")
    if not feedback_packet:
        blockers.append("v12_7_feedback_packet_missing_or_invalid")
    if not path_state:
        blockers.append("v12_7_path_integral_feedback_state_missing_or_invalid")

    feedback_status = str(ready_state.get("feedback_status", "process_tensor_feedback_block_context"))
    if feedback_status not in EXPECTED:
        blockers.append("v12_8_feedback_receipt_ready_state_status_invalid")
        feedback_status = "process_tensor_feedback_block_context"
    expected_reentry_status, expected_action = EXPECTED[feedback_status]

    if source_activation:
        if source_activation.get("activation_status") != "feedback_receipt_activation_completed":
            blockers.append("v13_25_feedback_receipt_activation_not_completed")
        if str(source_activation.get("observed_feedback_status", "")) != feedback_status:
            blockers.append("v13_25_feedback_status_mismatch")
        source_ready_digest = str(source_activation.get("source_v13_11_feedback_receipt_ready_state_digest", ""))
        actual_ready_digest = str(ready_state.get("process_tensor_feedback_receipt_ready_state_digest", ""))
        if not source_ready_digest or source_ready_digest != actual_ready_digest:
            blockers.append("v13_25_feedback_receipt_ready_state_digest_mismatch")

    if ready_state:
        if ready_state.get("process_tensor_feedback_receipt_ready_state") is not True:
            blockers.append("v12_8_feedback_receipt_ready_state_not_true")
        if str(ready_state.get("expected_v12_9_reentry_weighting_status", "")) != expected_reentry_status:
            blockers.append("v12_8_expected_reentry_weighting_status_mismatch")
        if str(ready_state.get("expected_v12_9_reentry_weighting_action", "")) != expected_action:
            blockers.append("v12_8_expected_reentry_weighting_action_mismatch")
        source_feedback_digest = str(ready_state.get("source_process_tensor_execution_feedback_digest", ""))
        actual_feedback_digest = str(feedback_packet.get("process_tensor_execution_feedback_digest", ""))
        if not source_feedback_digest or source_feedback_digest != actual_feedback_digest:
            blockers.append("v12_8_ready_state_feedback_packet_digest_mismatch")
        if str(path_state.get("feedback_status", "")) != feedback_status:
            blockers.append("v12_8_ready_state_path_feedback_status_mismatch")

    v12_8_invoked = False
    v12_9_invoked = False
    v12_8_result: dict[str, Any] = {}
    v12_9_result: dict[str, Any] = {}

    if not blockers:
        v12_8_result = build_physical_quantum_qi_process_tensor_feedback_receipt_ledger(
            runtime_context={
                "physical_quantum_qi_process_tensor_feedback_receipt_ledger_enabled": True,
                "apply_physical_quantum_qi_process_tensor_feedback_receipt_ledger": True,
                "runtime_root": str(root),
            },
            process_tensor_feedback_receipt_ledger_license=dict(_m(lic.get("v12_8_receipt_ledger_license"))),
        ).to_dict()
        v12_8_invoked = True
        if v12_8_result.get("status") != "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_READY":
            blockers.append("v12_8_feedback_receipt_ledger_not_ready")
        if str(v12_8_result.get("feedback_status", "")) != feedback_status:
            blockers.append("v12_8_feedback_receipt_ledger_status_mismatch")

    if v12_8_invoked and not blockers:
        v12_9_result = build_physical_quantum_qi_feedback_to_reentry_weighting_bridge(
            runtime_context={
                "physical_quantum_qi_feedback_to_reentry_weighting_bridge_enabled": True,
                "apply_physical_quantum_qi_feedback_to_reentry_weighting_bridge": True,
                "runtime_root": str(root),
            },
            feedback_to_reentry_weighting_bridge_license=dict(_m(lic.get("v12_9_reentry_bridge_license"))),
        ).to_dict()
        v12_9_invoked = True
        if v12_9_result.get("status") != "PHYSICAL_QUANTUM_QI_FEEDBACK_TO_REENTRY_WEIGHTING_BRIDGE_READY":
            blockers.append("v12_9_reentry_weighting_bridge_not_ready")
        if str(v12_9_result.get("reentry_weighting_status", "")) != expected_reentry_status:
            blockers.append("v12_9_reentry_weighting_status_mismatch")
        if str(v12_9_result.get("reentry_weighting_action", "")) != expected_action:
            blockers.append("v12_9_reentry_weighting_action_mismatch")

    observed_reentry_status = str(v12_9_result.get("reentry_weighting_status", "reentry_weighting_block"))
    observed_action = str(v12_9_result.get("reentry_weighting_action", "add_barrier_potential"))
    activation_status = (
        "reentry_weighting_activation_completed"
        if v12_8_invoked and v12_9_invoked and not blockers
        else "reentry_weighting_activation_blocked"
    )

    if v12_8_invoked or v12_9_invoked:
        record = {
            "version": "physical_quantum_qi_v13_26_reentry_weighting_activation_record",
            "activation_status": activation_status,
            "feedback_status": feedback_status,
            "expected_reentry_weighting_status": expected_reentry_status,
            "observed_reentry_weighting_status": observed_reentry_status,
            "observed_reentry_weighting_action": observed_action,
            "source_v13_25_activation_record_digest": str(
                source_activation.get("feedback_receipt_activation_record_digest", "")
            ),
            "source_v12_8_feedback_receipt_ready_state_digest": str(
                ready_state.get("process_tensor_feedback_receipt_ready_state_digest", "")
            ),
            "source_v12_8_feedback_receipt_record_digest": str(
                v12_8_result.get("latest_record_digest", "")
            ),
            "source_v12_9_reentry_weighting_state_digest": str(
                _read_json(root / "physical_quantum_qi_reentry_weighting_state.json").get(
                    "reentry_weighting_state_digest", ""
                )
            ),
            "boundary": {
                "two_stage_reentry_weighting_activation": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "license_gated_reentry_activation": True,
                "not_direct_execution_authority": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        record["reentry_weighting_activation_record_digest"] = _sha(record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(output_record_path, record)

    status = (
        "PHYSICAL_QUANTUM_QI_V13_26_REENTRY_WEIGHTING_ACTIVATION_READY"
        if v12_8_invoked and v12_9_invoked and not blockers
        else "PHYSICAL_QUANTUM_QI_V13_26_REENTRY_WEIGHTING_ACTIVATION_BLOCKED"
    )
    packet_id = "physical-quantum-qi-v13-26-reentry-weighting-activation-" + _sha(
        {"feedback_status": feedback_status, "reentry_status": observed_reentry_status, "blockers": blockers}
    )[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_26_reentry_weighting_activation",
        "status": status,
        "packet_id": packet_id,
        "activation_status": activation_status,
        "feedback_status": feedback_status,
        "expected_reentry_weighting_status": expected_reentry_status,
        "observed_reentry_weighting_status": observed_reentry_status,
        "observed_reentry_weighting_action": observed_action,
        "v12_8_receipt_ledger_invoked": v12_8_invoked,
        "v12_9_reentry_bridge_invoked": v12_9_invoked,
        "receipt_ledger_appended": v12_8_result.get("ledger_appended") is True,
        "reentry_weighting_packet_written": v12_9_result.get("reentry_weighting_packet_written") is True,
        "reentry_weighting_state_updated": v12_9_result.get("reentry_weighting_state_updated") is True,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_26ReentryWeightingActivationResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v13_26_reentry_weighting_activation",
        status,
        packet_id,
        str(root),
        activation_status,
        feedback_status,
        expected_reentry_status,
        observed_reentry_status,
        observed_action,
        v12_8_invoked,
        v12_9_invoked,
        v12_8_result.get("ledger_appended") is True,
        v12_9_result.get("reentry_weighting_packet_written") is True,
        v12_9_result.get("reentry_weighting_state_updated") is True,
        str(output_record_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
