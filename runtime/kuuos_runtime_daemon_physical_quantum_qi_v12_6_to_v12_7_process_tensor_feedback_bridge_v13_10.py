#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


FEEDBACK_BY_EXECUTION = {
    "guarded_transition_executed": "process_tensor_feedback_reinforce_next_cycle",
    "guarded_transition_hold": "process_tensor_feedback_hold_context",
    "guarded_transition_block": "process_tensor_feedback_block_context",
}
REQUIRED_EXECUTION_BOUNDARY_FLAGS = (
    "guarded_transition_executor",
    "runtime_local_external_state_only",
    "license_gated_execution",
    "no_dry_run_required",
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
class PhysicalQuantumQiV12_6ToV12_7ProcessTensorFeedbackBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_status: str
    execution_status: str
    expected_v12_7_feedback_status: str
    next_cycle_observed: bool
    memory_feedback_observed: bool
    external_backaction_observed: bool
    feedback_ready_state_written: bool
    bridge_ledger_appended: bool
    feedback_ready_state_path: str
    bridge_ledger_path: str
    summary_path: str
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


def _last_digest(path: pathlib.Path) -> str:
    if not path.is_file():
        return "GENESIS"
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        return "GENESIS"
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        return "CORRUPT_PREVIOUS_LEDGER_LINE"
    return str(value.get("record_digest", _sha(value)))


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _validate_context(ctx: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    out = {key: str(ctx.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, value in out.items():
        if not value:
            blockers.append(f"process_tensor_context_{key}_missing")
    return out


def _validate_execution_record(record: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], str]:
    if not record:
        blockers.append("v12_6_guarded_transition_execution_record_missing_or_invalid")
        return {}, "guarded_transition_block"
    if record.get("version") != "physical_quantum_qi_guarded_transition_execution_record_v12_6":
        blockers.append("v12_6_guarded_transition_execution_record_version_invalid")
    execution_status = str(record.get("execution_status", "guarded_transition_block"))
    if execution_status not in FEEDBACK_BY_EXECUTION:
        blockers.append("v12_6_guarded_transition_execution_status_invalid")
        execution_status = "guarded_transition_block"
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_EXECUTION_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"v12_6_guarded_transition_execution_boundary_{name}_missing")
    effects = dict(_m(record.get("effects")))
    expected_effect = execution_status == "guarded_transition_executed"
    for key in ["next_cycle_state_update", "memory_consumption", "external_state_mutation"]:
        if effects.get(key) is not expected_effect:
            blockers.append(f"v12_6_guarded_transition_{execution_status}_{key}_effect_mismatch")
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    payload = {
        "execution_status": execution_status,
        "expected_v12_7_feedback_status": FEEDBACK_BY_EXECUTION[execution_status],
        "intent_count": _int(record.get("intent_count")),
        "effects": effects,
        "process_tensor_context": context,
        "source_execution_record_digest": str(record.get("execution_record_digest", _sha(dict(record)))),
        "source_guarded_execution_intent_receipt_digest": str(record.get("source_guarded_execution_intent_receipt_digest", "")),
    }
    if execution_status == "guarded_transition_executed" and payload["intent_count"] <= 0:
        blockers.append("v12_6_executed_transition_without_intents")
    if execution_status != "guarded_transition_executed" and payload["intent_count"] != 0:
        blockers.append("v12_6_hold_or_block_transition_with_intents")
    return payload, execution_status


def _validate_effect_receipts(
    *,
    payload: Mapping[str, Any],
    execution_status: str,
    next_cycle: Mapping[str, Any],
    memory_receipt: Mapping[str, Any],
    external_receipt: Mapping[str, Any],
    blockers: list[str],
) -> tuple[bool, bool, bool]:
    next_seen = next_cycle.get("next_cycle_started") is True
    memory_seen = memory_receipt.get("memory_consumed") is True
    external_seen = external_receipt.get("external_state_mutated") is True
    if execution_status == "guarded_transition_executed":
        if not next_seen:
            blockers.append("v12_7_bridge_executed_transition_next_cycle_state_not_observed")
        if not memory_seen:
            blockers.append("v12_7_bridge_executed_transition_memory_consumption_not_observed")
        if not external_seen:
            blockers.append("v12_7_bridge_executed_transition_external_state_mutation_not_observed")
        source = str(payload.get("source_execution_record_digest", ""))
        if str(next_cycle.get("source_execution_record_digest", "")) != source:
            blockers.append("v12_7_bridge_next_cycle_source_execution_record_mismatch")
        if str(memory_receipt.get("source_execution_record_digest", "")) != source:
            blockers.append("v12_7_bridge_memory_source_execution_record_mismatch")
        if str(external_receipt.get("source_execution_record_digest", "")) != source:
            blockers.append("v12_7_bridge_external_source_execution_record_mismatch")
    elif next_seen or memory_seen or external_seen:
        blockers.append("v12_7_bridge_hold_or_block_with_unexpected_runtime_effect_observed")
    return next_seen, memory_seen, external_seen


def _kernel(*, execution_status: str, next_seen: bool, memory_seen: bool, external_seen: bool, intent_count: int) -> dict[str, Any]:
    if execution_status == "guarded_transition_executed":
        return {
            "feedback_status": "process_tensor_feedback_reinforce_next_cycle",
            "path_weight_delta": max(1, intent_count),
            "memory_feedback_weight": 1 if memory_seen else 0,
            "external_backaction_weight": 1 if external_seen else 0,
            "next_cycle_amplitude_delta": 1 if next_seen else 0,
        }
    if execution_status == "guarded_transition_hold":
        return {
            "feedback_status": "process_tensor_feedback_hold_context",
            "path_weight_delta": 0,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return {
        "feedback_status": "process_tensor_feedback_block_context",
        "path_weight_delta": -1,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def build_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge(
    *,
    runtime_context: Mapping[str, Any],
    v12_6_to_v12_7_process_tensor_feedback_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiV12_6ToV12_7ProcessTensorFeedbackBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(v12_6_to_v12_7_process_tensor_feedback_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    execution_record_path = root / "physical_quantum_qi_guarded_transition_execution_record.json"
    next_cycle_state_path = root / "physical_quantum_qi_next_cycle_state.json"
    memory_ledger_path = root / "physical_quantum_qi_memory_consumption_ledger.jsonl"
    external_ledger_path = root / "physical_quantum_qi_external_state_mutation_ledger.jsonl"
    ready_state_path = root / "physical_quantum_qi_v12_7_process_tensor_feedback_ready_state.json"
    bridge_ledger_path = root / "physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_summary.json"
    receipt_path = root / "physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_receipt.json"
    audit_path = root / "physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_license_not_ready")
    for name in [
        "v12_6_execution_record_read_allowed",
        "v12_6_next_cycle_state_read_allowed",
        "v12_6_memory_consumption_ledger_read_allowed",
        "v12_6_external_state_mutation_ledger_read_allowed",
        "v12_7_feedback_ready_state_write_allowed",
        "bridge_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, execution_status = _validate_execution_record(_read_json(execution_record_path), blockers)
    next_seen, memory_seen, external_seen = _validate_effect_receipts(
        payload=payload,
        execution_status=execution_status,
        next_cycle=_read_json(next_cycle_state_path),
        memory_receipt=_latest_jsonl(memory_ledger_path),
        external_receipt=_latest_jsonl(external_ledger_path),
        blockers=blockers,
    )
    state_written = ledger_appended = False
    bridge_status = "v12_6_to_v12_7_process_tensor_feedback_bridge_block"
    kernel: dict[str, Any] = {"feedback_status": FEEDBACK_BY_EXECUTION.get(execution_status, "process_tensor_feedback_block_context")}
    if not blockers:
        epoch = int(time.time())
        kernel = _kernel(
            execution_status=execution_status,
            next_seen=next_seen,
            memory_seen=memory_seen,
            external_seen=external_seen,
            intent_count=int(payload.get("intent_count", 0)),
        )
        bridge_status = "v12_6_to_v12_7_process_tensor_feedback_bridge_" + kernel["feedback_status"].rsplit("_", 1)[-1]
        state = {
            "version": "physical_quantum_qi_v12_7_process_tensor_feedback_ready_state_v13_10",
            "process_tensor_feedback_ready_state": True,
            "bridge_status": bridge_status,
            "execution_status": execution_status,
            "expected_v12_7_feedback_status": kernel["feedback_status"],
            "observed_effects": {
                "next_cycle_observed": next_seen,
                "memory_feedback_observed": memory_seen,
                "external_backaction_observed": external_seen,
            },
            "expected_feedback_kernel": kernel,
            "source_execution_record_digest": payload["source_execution_record_digest"],
            "source_guarded_execution_intent_receipt_digest": payload["source_guarded_execution_intent_receipt_digest"],
            "process_tensor_context": dict(payload["process_tensor_context"]),
            "boundary": {
                "v12_7_process_tensor_feedback_ready_state_only": True,
                "v12_6_guarded_transition_execution_record_required": True,
                "can_feed_v12_7_process_tensor_execution_feedback": True,
                "uses_execution_effects_as_non_markov_feedback": True,
                "history_window_feedback_required": True,
                "memory_kernel_feedback_required": True,
                "external_backaction_visible": True,
                "feedback_not_direct_truth": True,
                "bridge_not_direct_feedback_append": True,
                "does_not_run_feedback_runtime": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        state["process_tensor_feedback_ready_state_digest"] = _sha(state)
        _write_json(ready_state_path, state)
        state_written = True
        record = {
            "version": "physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_record_v13_10",
            "record_type": "physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge",
            "bridge_status": bridge_status,
            "execution_status": execution_status,
            "expected_v12_7_feedback_status": kernel["feedback_status"],
            "observed_effects": dict(state["observed_effects"]),
            "source_process_tensor_feedback_ready_state_digest": state["process_tensor_feedback_ready_state_digest"],
            "source_execution_record_digest": payload["source_execution_record_digest"],
            "prev_record_digest": _last_digest(bridge_ledger_path),
            "boundary": {
                "bridge_receipt_only": True,
                "v12_7_feedback_ready_state_traceable": True,
                "same_semantic_root": True,
                "uses_process_tensor_feedback": True,
                "feedback_not_direct_truth": True,
                "bridge_not_direct_execution": True,
                "replayable_receipt": True,
            },
            "epoch": epoch,
        }
        record["record_digest"] = _sha(record)
        _append_jsonl(bridge_ledger_path, record)
        ledger_appended = True
        summary = {
            "version": "physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_summary_v13_10",
            "bridge_status": bridge_status,
            "execution_status": execution_status,
            "expected_v12_7_feedback_status": kernel["feedback_status"],
            "observed_effects": dict(state["observed_effects"]),
            "process_tensor_feedback_ready_state_digest": state["process_tensor_feedback_ready_state_digest"],
            "boundary": {
                "summary_only": True,
                "can_feed_v12_7_process_tensor_execution_feedback": True,
                "feedback_not_direct_truth": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    final_status = "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_BLOCKED"
    packet_id = "physical-quantum-qi-v12-6-to-v12-7-process-tensor-feedback-bridge-" + _sha({"payload": payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_v13_10",
        "status": final_status,
        "packet_id": packet_id,
        "bridge_status": bridge_status,
        "execution_status": execution_status,
        "expected_v12_7_feedback_status": str(kernel.get("feedback_status", "process_tensor_feedback_block_context")),
        "next_cycle_observed": next_seen,
        "memory_feedback_observed": memory_seen,
        "external_backaction_observed": external_seen,
        "feedback_ready_state_written": state_written,
        "bridge_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiV12_6ToV12_7ProcessTensorFeedbackBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_v13_10",
        final_status,
        packet_id,
        str(root),
        bridge_status,
        execution_status,
        str(kernel.get("feedback_status", "process_tensor_feedback_block_context")),
        next_seen,
        memory_seen,
        external_seen,
        state_written,
        ledger_appended,
        str(ready_state_path),
        str(bridge_ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
