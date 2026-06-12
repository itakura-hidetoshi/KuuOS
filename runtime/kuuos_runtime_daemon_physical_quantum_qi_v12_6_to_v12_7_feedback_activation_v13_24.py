#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_v13_10 import (
    build_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge,
)

FEEDBACK_BY_EXECUTION = {
    "guarded_transition_executed": "process_tensor_feedback_reinforce_next_cycle",
    "guarded_transition_hold": "process_tensor_feedback_hold_context",
    "guarded_transition_block": "process_tensor_feedback_block_context",
}


@dataclass(frozen=True)
class PhysicalQuantumQiV12_6ToV12_7FeedbackActivationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    execution_status: str
    expected_feedback_status: str
    observed_feedback_status: str
    feedback_bridge_invoked: bool
    feedback_ready_state_written: bool
    feedback_bridge_ledger_appended: bool
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


def build_physical_quantum_qi_v12_6_to_v12_7_feedback_activation(
    *,
    runtime_context: Mapping[str, Any],
    v12_6_to_v12_7_feedback_activation_license: Mapping[str, Any],
) -> PhysicalQuantumQiV12_6ToV12_7FeedbackActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v12_6_to_v12_7_feedback_activation_license)
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

    activation_path = root / "physical_quantum_qi_v13_23_executor_activation_record.json"
    execution_path = root / "physical_quantum_qi_guarded_transition_execution_record.json"
    output_activation_path = root / "physical_quantum_qi_v13_24_feedback_activation_record.json"
    receipt_path = root / "physical_quantum_qi_v13_24_feedback_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_24_feedback_activation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v12_6_to_v12_7_feedback_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v12_6_to_v12_7_feedback_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v12_6_to_v12_7_feedback_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v12_6_to_v12_7_feedback_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_FEEDBACK_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v12_6_to_v12_7_feedback_activation_license_not_ready")
    for flag in (
        "v13_23_activation_record_read_allowed",
        "v12_6_execution_record_read_allowed",
        "v13_10_feedback_bridge_invoke_allowed",
        "activation_record_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    activation = _read_json(activation_path)
    execution = _read_json(execution_path)
    if not activation:
        blockers.append("v13_23_executor_activation_record_missing_or_invalid")
    if not execution:
        blockers.append("v12_6_execution_record_missing_or_invalid")

    execution_status = str(execution.get("execution_status", "guarded_transition_block"))
    if execution_status not in FEEDBACK_BY_EXECUTION:
        blockers.append("v12_6_execution_status_invalid")
        execution_status = "guarded_transition_block"
    expected_feedback = FEEDBACK_BY_EXECUTION[execution_status]

    if activation:
        if activation.get("activation_status") != "executor_activation_completed":
            blockers.append("v13_23_activation_not_completed")
        if str(activation.get("observed_execution_status", "")) != execution_status:
            blockers.append("v13_23_activation_execution_status_mismatch")
        source_digest = str(activation.get("source_v12_6_execution_record_digest", ""))
        actual_digest = str(execution.get("execution_record_digest", ""))
        if not source_digest or source_digest != actual_digest:
            blockers.append("v13_23_activation_execution_record_digest_mismatch")

    invoked = False
    bridge_result: dict[str, Any] = {}
    if not blockers:
        bridge_result = build_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge(
            runtime_context={
                "physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_enabled": True,
                "apply_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge": True,
                "runtime_root": str(root),
            },
            v12_6_to_v12_7_process_tensor_feedback_bridge_license=dict(_m(lic.get("feedback_bridge_license"))),
        ).to_dict()
        invoked = True
        if bridge_result.get("status") != "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_READY":
            blockers.append("v13_10_feedback_bridge_not_ready")
        if str(bridge_result.get("execution_status", "")) != execution_status:
            blockers.append("v13_10_feedback_bridge_execution_status_mismatch")
        if str(bridge_result.get("expected_v12_7_feedback_status", "")) != expected_feedback:
            blockers.append("v13_10_feedback_status_mismatch")

    observed_feedback = str(
        bridge_result.get("expected_v12_7_feedback_status", "process_tensor_feedback_block_context")
    )
    activation_status = "feedback_activation_completed" if invoked and not blockers else "feedback_activation_blocked"
    record_written = False
    if invoked:
        record = {
            "version": "physical_quantum_qi_v13_24_feedback_activation_record",
            "activation_status": activation_status,
            "execution_status": execution_status,
            "expected_feedback_status": expected_feedback,
            "observed_feedback_status": observed_feedback,
            "source_v13_23_activation_record_digest": str(activation.get("activation_record_digest", "")),
            "source_v12_6_execution_record_digest": str(execution.get("execution_record_digest", "")),
            "source_v13_10_feedback_ready_state_digest": str(
                _read_json(root / "physical_quantum_qi_v12_7_process_tensor_feedback_ready_state.json").get(
                    "process_tensor_feedback_ready_state_digest", ""
                )
            ),
            "boundary": {
                "post_execution_feedback_activation": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "license_gated_feedback_activation": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        record["feedback_activation_record_digest"] = _sha(record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(output_activation_path, record)
            record_written = True

    status = (
        "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_FEEDBACK_ACTIVATION_READY"
        if invoked and not blockers
        else "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_FEEDBACK_ACTIVATION_BLOCKED"
    )
    packet_id = "physical-quantum-qi-v13-24-feedback-activation-" + _sha(
        {"execution_status": execution_status, "feedback_status": observed_feedback, "blockers": blockers}
    )[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v12_6_to_v12_7_feedback_activation_v13_24",
        "status": status,
        "packet_id": packet_id,
        "activation_status": activation_status,
        "execution_status": execution_status,
        "expected_feedback_status": expected_feedback,
        "observed_feedback_status": observed_feedback,
        "feedback_bridge_invoked": invoked,
        "feedback_activation_record_written": record_written,
        "feedback_ready_state_written": bridge_result.get("feedback_ready_state_written") is True,
        "feedback_bridge_ledger_appended": bridge_result.get("bridge_ledger_appended") is True,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV12_6ToV12_7FeedbackActivationResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v12_6_to_v12_7_feedback_activation_v13_24",
        status,
        packet_id,
        str(root),
        activation_status,
        execution_status,
        expected_feedback,
        observed_feedback,
        invoked,
        bridge_result.get("feedback_ready_state_written") is True,
        bridge_result.get("bridge_ledger_appended") is True,
        str(output_activation_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
