#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_guarded_transition_executor_v12_6 import (
    build_physical_quantum_qi_guarded_transition_executor,
)

EXPECTED_EFFECTS = {
    "guarded_transition_executed": {
        "internal_transition_record": True,
        "next_cycle_state_update": True,
        "memory_consumption": True,
        "external_state_mutation": True,
    },
    "guarded_transition_hold": {
        "internal_transition_record": True,
        "next_cycle_state_update": False,
        "memory_consumption": False,
        "external_state_mutation": False,
    },
    "guarded_transition_block": {
        "internal_transition_record": True,
        "next_cycle_state_update": False,
        "memory_consumption": False,
        "external_state_mutation": False,
    },
}
REQUIRED_READY_BOUNDARY = (
    "v12_6_transition_executor_ready_state_only",
    "v12_5_guarded_execution_intent_receipt_required",
    "can_feed_v12_6_guarded_transition_executor",
    "execution_layer_entrypoint",
    "no_dry_run_required",
    "uses_process_tensor_feedback",
    "non_markov_feedback_preserved",
    "history_window_feedback_preserved",
    "memory_kernel_feedback_preserved",
    "candidate_weighting_not_truth",
    "bridge_not_direct_execution",
    "license_gated_bridge",
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
class PhysicalQuantumQiV13_9ToV12_6ExecutorActivationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    expected_execution_status: str
    observed_execution_status: str
    execution_invoked: bool
    execution_record_written: bool
    next_cycle_state_updated: bool
    memory_consumption_appended: bool
    external_state_mutation_appended: bool
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


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _latest_jsonl(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        return {}
    try:
        value = json.loads(latest)
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


def _validate_ready_state(
    ready: Mapping[str, Any],
    latest_receipt: Mapping[str, Any],
    blockers: list[str],
) -> tuple[str, dict[str, bool], dict[str, str]]:
    if not ready:
        blockers.append("v13_9_transition_executor_ready_state_missing_or_invalid")
        return "guarded_transition_block", EXPECTED_EFFECTS["guarded_transition_block"], {}
    if ready.get("transition_executor_ready_state") is not True:
        blockers.append("v13_9_transition_executor_ready_state_not_true")
    boundary = _m(ready.get("boundary"))
    for flag in REQUIRED_READY_BOUNDARY:
        if boundary.get(flag) is not True:
            blockers.append(f"v13_9_transition_executor_ready_state_boundary_{flag}_missing")
    expected = str(ready.get("expected_v12_6_execution_status", "guarded_transition_block"))
    if expected not in EXPECTED_EFFECTS:
        blockers.append("v13_9_expected_v12_6_execution_status_invalid")
        expected = "guarded_transition_block"
    effects = dict(_m(ready.get("expected_effects")))
    if effects != EXPECTED_EFFECTS[expected]:
        blockers.append("v13_9_expected_effects_mismatch")
    context = {key: str(_m(ready.get("process_tensor_context")).get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, value in context.items():
        if not value:
            blockers.append(f"v13_9_process_tensor_context_{key}_missing")
    source_digest = str(ready.get("source_v12_5_guarded_execution_intent_receipt_digest", ""))
    latest_digest = str(latest_receipt.get("record_digest", ""))
    if not source_digest or source_digest != latest_digest:
        blockers.append("v13_9_ready_state_receipt_digest_mismatch")
    if str(ready.get("execution_intent_status", "")) != str(latest_receipt.get("execution_intent_status", "")):
        blockers.append("v13_9_ready_state_intent_status_mismatch")
    if int(ready.get("intent_count", 0) or 0) != int(latest_receipt.get("intent_count", 0) or 0):
        blockers.append("v13_9_ready_state_intent_count_mismatch")
    return expected, EXPECTED_EFFECTS[expected], context


def build_physical_quantum_qi_v13_9_to_v12_6_executor_activation(
    *,
    runtime_context: Mapping[str, Any],
    v13_9_to_v12_6_executor_activation_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_9ToV12_6ExecutorActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_9_to_v12_6_executor_activation_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ready_path = root / "physical_quantum_qi_v12_6_guarded_transition_executor_ready_state.json"
    receipt_ledger_path = root / "physical_quantum_qi_guarded_execution_intent_receipt_ledger.jsonl"
    activation_record_path = root / "physical_quantum_qi_v13_23_executor_activation_record.json"
    receipt_path = root / "physical_quantum_qi_v13_23_executor_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_23_executor_activation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_9_to_v12_6_executor_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_9_to_v12_6_executor_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_9_to_v12_6_executor_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_9_to_v12_6_executor_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_9_TO_V12_6_EXECUTOR_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_9_to_v12_6_executor_activation_license_not_ready")
    for flag in (
        "v13_9_ready_state_read_allowed",
        "v12_5_receipt_ledger_read_allowed",
        "v12_6_executor_invoke_allowed",
        "activation_record_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    latest_receipt = _latest_jsonl(receipt_ledger_path)
    if not latest_receipt:
        blockers.append("v12_5_guarded_execution_intent_receipt_ledger_missing_or_empty")
    expected, expected_effects, context = _validate_ready_state(
        _read_json(ready_path), latest_receipt, blockers
    )

    invoked = False
    executor_result: dict[str, Any] = {}
    if not blockers:
        executor_license = dict(_m(lic.get("executor_license")))
        executor_result = build_physical_quantum_qi_guarded_transition_executor(
            runtime_context={
                "physical_quantum_qi_guarded_transition_executor_enabled": True,
                "apply_physical_quantum_qi_guarded_transition_executor": True,
                "runtime_root": str(root),
            },
            guarded_transition_executor_license=executor_license,
        ).to_dict()
        invoked = True
        if executor_result.get("status") != "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_READY":
            blockers.append("v12_6_executor_not_ready")
        observed = str(executor_result.get("execution_status", "guarded_transition_block"))
        if observed != expected:
            blockers.append("v12_6_execution_status_mismatch")
        observed_effects = {
            "internal_transition_record": executor_result.get("internal_transition_record_written") is True,
            "next_cycle_state_update": executor_result.get("next_cycle_state_updated") is True,
            "memory_consumption": executor_result.get("memory_consumption_appended") is True,
            "external_state_mutation": executor_result.get("external_state_mutation_appended") is True,
        }
        if observed_effects != expected_effects:
            blockers.append("v12_6_execution_effects_mismatch")
    else:
        observed = "guarded_transition_block"

    activation_status = (
        "executor_activation_completed"
        if invoked and not blockers
        else "executor_activation_blocked"
    )
    record_written = False
    if invoked:
        record = {
            "version": "physical_quantum_qi_v13_23_executor_activation_record",
            "activation_status": activation_status,
            "expected_execution_status": expected,
            "observed_execution_status": observed,
            "expected_effects": expected_effects,
            "process_tensor_context": context,
            "source_v13_9_ready_state_digest": str(
                _read_json(ready_path).get("transition_executor_ready_state_digest", "")
            ),
            "source_v12_5_receipt_digest": str(latest_receipt.get("record_digest", "")),
            "source_v12_6_execution_record_digest": str(
                _read_json(root / "physical_quantum_qi_guarded_transition_execution_record.json").get(
                    "execution_record_digest", ""
                )
            ),
            "boundary": {
                "actual_executor_activation": True,
                "license_gated_execution": True,
                "no_dry_run_required": True,
                "runtime_local_external_state_only": True,
                "uses_process_tensor_feedback": True,
                "candidate_weighting_not_truth": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        record["activation_record_digest"] = _sha(record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(activation_record_path, record)
            record_written = True

    status = (
        "PHYSICAL_QUANTUM_QI_V13_9_TO_V12_6_EXECUTOR_ACTIVATION_READY"
        if invoked and not blockers
        else "PHYSICAL_QUANTUM_QI_V13_9_TO_V12_6_EXECUTOR_ACTIVATION_BLOCKED"
    )
    packet_id = "physical-quantum-qi-v13-23-executor-activation-" + _sha(
        {"expected": expected, "observed": observed, "blockers": blockers}
    )[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_9_to_v12_6_executor_activation_v13_23",
        "status": status,
        "packet_id": packet_id,
        "activation_status": activation_status,
        "expected_execution_status": expected,
        "observed_execution_status": observed,
        "execution_invoked": invoked,
        "activation_record_written": record_written,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_9ToV12_6ExecutorActivationResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v13_9_to_v12_6_executor_activation_v13_23",
        status,
        packet_id,
        str(root),
        activation_status,
        expected,
        observed,
        invoked,
        executor_result.get("internal_transition_record_written") is True,
        executor_result.get("next_cycle_state_updated") is True,
        executor_result.get("memory_consumption_appended") is True,
        executor_result.get("external_state_mutation_appended") is True,
        str(activation_record_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
