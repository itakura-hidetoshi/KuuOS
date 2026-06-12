#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_process_tensor_execution_feedback_v12_7 import (
    build_physical_quantum_qi_process_tensor_execution_feedback,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_v13_11 import (
    build_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge,
)

EXPECTED_FEEDBACK = {
    "guarded_transition_executed": "process_tensor_feedback_reinforce_next_cycle",
    "guarded_transition_hold": "process_tensor_feedback_hold_context",
    "guarded_transition_block": "process_tensor_feedback_block_context",
}


@dataclass(frozen=True)
class PhysicalQuantumQiV13_25FeedbackReceiptActivationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    execution_status: str
    expected_feedback_status: str
    observed_feedback_status: str
    v12_7_feedback_invoked: bool
    v13_11_receipt_bridge_invoked: bool
    feedback_packet_written: bool
    path_integral_feedback_state_written: bool
    feedback_receipt_ready_state_written: bool
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


def build_physical_quantum_qi_v13_25_feedback_receipt_activation(
    *,
    runtime_context: Mapping[str, Any],
    v13_25_feedback_receipt_activation_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_25FeedbackReceiptActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_25_feedback_receipt_activation_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = ctx.get("runtime_root")
    if not root_value:
        blockers.append("runtime_root_missing")
        root = pathlib.Path(".").resolve()
    else:
        root = pathlib.Path(str(root_value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_activation_path = root / "physical_quantum_qi_v13_24_feedback_activation_record.json"
    v13_10_ready_path = root / "physical_quantum_qi_v12_7_process_tensor_feedback_ready_state.json"
    execution_path = root / "physical_quantum_qi_guarded_transition_execution_record.json"
    activation_record_path = root / "physical_quantum_qi_v13_25_feedback_receipt_activation_record.json"
    receipt_path = root / "physical_quantum_qi_v13_25_feedback_receipt_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_25_feedback_receipt_activation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_25_feedback_receipt_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_25_feedback_receipt_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_25_feedback_receipt_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_25_feedback_receipt_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_25_FEEDBACK_RECEIPT_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_25_feedback_receipt_activation_license_not_ready")
    for flag in (
        "v13_24_activation_record_read_allowed",
        "v13_10_feedback_ready_state_read_allowed",
        "v12_7_feedback_runtime_invoke_allowed",
        "v13_11_receipt_bridge_invoke_allowed",
        "activation_record_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source_activation = _read_json(source_activation_path)
    v13_10_ready = _read_json(v13_10_ready_path)
    execution = _read_json(execution_path)

    if not source_activation:
        blockers.append("v13_24_feedback_activation_record_missing_or_invalid")
    if not v13_10_ready:
        blockers.append("v13_10_feedback_ready_state_missing_or_invalid")
    if not execution:
        blockers.append("v12_6_execution_record_missing_or_invalid")

    execution_status = str(execution.get("execution_status", "guarded_transition_block"))
    if execution_status not in EXPECTED_FEEDBACK:
        blockers.append("v12_6_execution_status_invalid")
        execution_status = "guarded_transition_block"
    expected_feedback = EXPECTED_FEEDBACK[execution_status]

    if source_activation:
        if source_activation.get("activation_status") != "feedback_activation_completed":
            blockers.append("v13_24_feedback_activation_not_completed")
        if str(source_activation.get("execution_status", "")) != execution_status:
            blockers.append("v13_24_execution_status_mismatch")
        if str(source_activation.get("observed_feedback_status", "")) != expected_feedback:
            blockers.append("v13_24_feedback_status_mismatch")
        source_ready_digest = str(source_activation.get("source_v13_10_feedback_ready_state_digest", ""))
        actual_ready_digest = str(v13_10_ready.get("process_tensor_feedback_ready_state_digest", ""))
        if not source_ready_digest or source_ready_digest != actual_ready_digest:
            blockers.append("v13_24_feedback_ready_state_digest_mismatch")

    if v13_10_ready:
        if v13_10_ready.get("process_tensor_feedback_ready_state") is not True:
            blockers.append("v13_10_feedback_ready_state_not_true")
        if str(v13_10_ready.get("execution_status", "")) != execution_status:
            blockers.append("v13_10_ready_state_execution_status_mismatch")
        if str(v13_10_ready.get("expected_v12_7_feedback_status", "")) != expected_feedback:
            blockers.append("v13_10_ready_state_feedback_status_mismatch")
        source_exec_digest = str(v13_10_ready.get("source_execution_record_digest", ""))
        actual_exec_digest = str(execution.get("execution_record_digest", ""))
        if not source_exec_digest or source_exec_digest != actual_exec_digest:
            blockers.append("v13_10_ready_state_execution_record_digest_mismatch")

    v12_7_invoked = False
    v13_11_invoked = False
    v12_7_result: dict[str, Any] = {}
    v13_11_result: dict[str, Any] = {}

    if not blockers:
        v12_7_result = build_physical_quantum_qi_process_tensor_execution_feedback(
            runtime_context={
                "physical_quantum_qi_process_tensor_execution_feedback_enabled": True,
                "apply_physical_quantum_qi_process_tensor_execution_feedback": True,
                "runtime_root": str(root),
            },
            process_tensor_execution_feedback_license=dict(_m(lic.get("v12_7_feedback_license"))),
        ).to_dict()
        v12_7_invoked = True
        if v12_7_result.get("status") != "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_READY":
            blockers.append("v12_7_feedback_runtime_not_ready")
        if str(v12_7_result.get("execution_status", "")) != execution_status:
            blockers.append("v12_7_feedback_runtime_execution_status_mismatch")
        if str(v12_7_result.get("feedback_status", "")) != expected_feedback:
            blockers.append("v12_7_feedback_runtime_feedback_status_mismatch")

    if v12_7_invoked and not blockers:
        v13_11_result = build_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge(
            runtime_context={
                "physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge_enabled": True,
                "apply_physical_quantum_qi_v12_7_to_v12_8_feedback_receipt_bridge": True,
                "runtime_root": str(root),
            },
            v12_7_to_v12_8_feedback_receipt_bridge_license=dict(_m(lic.get("v13_11_receipt_bridge_license"))),
        ).to_dict()
        v13_11_invoked = True
        if v13_11_result.get("status") != "PHYSICAL_QUANTUM_QI_V12_7_TO_V12_8_FEEDBACK_RECEIPT_BRIDGE_READY":
            blockers.append("v13_11_feedback_receipt_bridge_not_ready")
        if str(v13_11_result.get("feedback_status", "")) != expected_feedback:
            blockers.append("v13_11_feedback_status_mismatch")
        if str(v13_11_result.get("execution_status", "")) != execution_status:
            blockers.append("v13_11_execution_status_mismatch")

    observed_feedback = str(
        v13_11_result.get(
            "feedback_status",
            v12_7_result.get("feedback_status", "process_tensor_feedback_block_context"),
        )
    )
    activation_status = (
        "feedback_receipt_activation_completed"
        if v12_7_invoked and v13_11_invoked and not blockers
        else "feedback_receipt_activation_blocked"
    )

    record_written = False
    if v12_7_invoked or v13_11_invoked:
        record = {
            "version": "physical_quantum_qi_v13_25_feedback_receipt_activation_record",
            "activation_status": activation_status,
            "execution_status": execution_status,
            "expected_feedback_status": expected_feedback,
            "observed_feedback_status": observed_feedback,
            "source_v13_24_feedback_activation_record_digest": str(
                source_activation.get("feedback_activation_record_digest", "")
            ),
            "source_v13_10_feedback_ready_state_digest": str(
                v13_10_ready.get("process_tensor_feedback_ready_state_digest", "")
            ),
            "source_v12_7_feedback_packet_digest": str(
                _read_json(root / "physical_quantum_qi_process_tensor_execution_feedback_packet.json").get(
                    "process_tensor_execution_feedback_digest", ""
                )
            ),
            "source_v13_11_feedback_receipt_ready_state_digest": str(
                _read_json(root / "physical_quantum_qi_v12_8_process_tensor_feedback_receipt_ready_state.json").get(
                    "process_tensor_feedback_receipt_ready_state_digest", ""
                )
            ),
            "boundary": {
                "two_stage_feedback_receipt_activation": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "license_gated_feedback_activation": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        record["feedback_receipt_activation_record_digest"] = _sha(record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(activation_record_path, record)
            record_written = True

    status = (
        "PHYSICAL_QUANTUM_QI_V13_25_FEEDBACK_RECEIPT_ACTIVATION_READY"
        if v12_7_invoked and v13_11_invoked and not blockers
        else "PHYSICAL_QUANTUM_QI_V13_25_FEEDBACK_RECEIPT_ACTIVATION_BLOCKED"
    )
    packet_id = "physical-quantum-qi-v13-25-feedback-receipt-activation-" + _sha(
        {"execution_status": execution_status, "feedback_status": observed_feedback, "blockers": blockers}
    )[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_25_feedback_receipt_activation",
        "status": status,
        "packet_id": packet_id,
        "activation_status": activation_status,
        "execution_status": execution_status,
        "expected_feedback_status": expected_feedback,
        "observed_feedback_status": observed_feedback,
        "v12_7_feedback_invoked": v12_7_invoked,
        "v13_11_receipt_bridge_invoked": v13_11_invoked,
        "activation_record_written": record_written,
        "feedback_packet_written": v12_7_result.get("process_tensor_feedback_appended") is True,
        "path_integral_feedback_state_written": v12_7_result.get("path_integral_feedback_state_updated") is True,
        "feedback_receipt_ready_state_written": v13_11_result.get("feedback_receipt_ready_state_written") is True,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_25FeedbackReceiptActivationResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v13_25_feedback_receipt_activation",
        status,
        packet_id,
        str(root),
        activation_status,
        execution_status,
        expected_feedback,
        observed_feedback,
        v12_7_invoked,
        v13_11_invoked,
        v12_7_result.get("process_tensor_feedback_appended") is True,
        v12_7_result.get("path_integral_feedback_state_updated") is True,
        v13_11_result.get("feedback_receipt_ready_state_written") is True,
        str(activation_record_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
