#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


EXECUTION_STATUSES = {
    "guarded_transition_executed",
    "guarded_transition_hold",
    "guarded_transition_block",
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
class PhysicalQuantumQiProcessTensorExecutionFeedbackResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    execution_status: str
    feedback_status: str
    process_tensor_feedback_appended: bool
    path_integral_feedback_state_updated: bool
    memory_feedback_observed: bool
    external_backaction_observed: bool
    next_cycle_observed: bool
    feedback_packet_path: str
    feedback_ledger_path: str
    path_integral_feedback_state_path: str
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


def _validate_context(ctx: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    out = {key: str(ctx.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, value in out.items():
        if not value:
            blockers.append(f"process_tensor_context_{key}_missing")
    return out


def _validate_execution_record(record: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], str]:
    if not record:
        blockers.append("guarded_transition_execution_record_missing_or_invalid")
        return {}, "guarded_transition_block"
    status = str(record.get("execution_status", "guarded_transition_block"))
    if status not in EXECUTION_STATUSES:
        blockers.append("guarded_transition_execution_status_invalid")
        status = "guarded_transition_block"
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_EXECUTION_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"guarded_transition_execution_boundary_{name}_missing")
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    effects = dict(_m(record.get("effects")))
    payload = {
        "execution_status": status,
        "effects": effects,
        "intent_count": int(record.get("intent_count", 0) or 0),
        "process_tensor_context": context,
        "source_execution_record_digest": str(record.get("execution_record_digest", _sha(dict(record)))),
        "source_guarded_execution_intent_receipt_digest": str(record.get("source_guarded_execution_intent_receipt_digest", "")),
    }
    if status == "guarded_transition_executed":
        for key in ["next_cycle_state_update", "memory_consumption", "external_state_mutation"]:
            if effects.get(key) is not True:
                blockers.append(f"executed_transition_without_{key}")
    else:
        for key in ["next_cycle_state_update", "memory_consumption", "external_state_mutation"]:
            if effects.get(key) is True:
                blockers.append(f"{status}_unexpected_{key}")
    return payload, status


def _feedback_kernel(*, execution_status: str, memory_seen: bool, external_seen: bool, next_seen: bool, intent_count: int) -> dict[str, Any]:
    if execution_status == "guarded_transition_executed":
        path_weight_delta = max(1, intent_count)
        memory_feedback_weight = 1 if memory_seen else 0
        external_backaction_weight = 1 if external_seen else 0
        next_cycle_amplitude_delta = 1 if next_seen else 0
        feedback_status = "process_tensor_feedback_reinforce_next_cycle"
    elif execution_status == "guarded_transition_hold":
        path_weight_delta = 0
        memory_feedback_weight = 0
        external_backaction_weight = 0
        next_cycle_amplitude_delta = 0
        feedback_status = "process_tensor_feedback_hold_context"
    else:
        path_weight_delta = -1
        memory_feedback_weight = 0
        external_backaction_weight = 0
        next_cycle_amplitude_delta = 0
        feedback_status = "process_tensor_feedback_block_context"
    return {
        "feedback_status": feedback_status,
        "path_weight_delta": path_weight_delta,
        "memory_feedback_weight": memory_feedback_weight,
        "external_backaction_weight": external_backaction_weight,
        "next_cycle_amplitude_delta": next_cycle_amplitude_delta,
        "non_markov_feedback_required": True,
        "history_window_feedback_required": True,
        "instrument_trace_feedback_required": True,
        "process_tensor_feedback_not_truth": True,
    }


def build_physical_quantum_qi_process_tensor_execution_feedback(
    *,
    runtime_context: Mapping[str, Any],
    process_tensor_execution_feedback_license: Mapping[str, Any],
) -> PhysicalQuantumQiProcessTensorExecutionFeedbackResult:
    ctx = _m(runtime_context)
    lic = _m(process_tensor_execution_feedback_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    execution_record_path = root / "physical_quantum_qi_guarded_transition_execution_record.json"
    next_cycle_state_path = root / "physical_quantum_qi_next_cycle_state.json"
    memory_ledger_path = root / "physical_quantum_qi_memory_consumption_ledger.jsonl"
    external_ledger_path = root / "physical_quantum_qi_external_state_mutation_ledger.jsonl"
    feedback_packet_path = root / "physical_quantum_qi_process_tensor_execution_feedback_packet.json"
    feedback_ledger_path = root / "physical_quantum_qi_process_tensor_execution_feedback_ledger.jsonl"
    path_integral_feedback_state_path = root / "physical_quantum_qi_path_integral_feedback_state.json"
    receipt_path = root / "physical_quantum_qi_process_tensor_execution_feedback_receipt.json"
    audit_path = root / "physical_quantum_qi_process_tensor_execution_feedback_audit.jsonl"

    if ctx.get("physical_quantum_qi_process_tensor_execution_feedback_enabled") is not True:
        blockers.append("physical_quantum_qi_process_tensor_execution_feedback_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_process_tensor_execution_feedback") is not True:
        blockers.append("apply_physical_quantum_qi_process_tensor_execution_feedback_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_LICENSE_READY":
        blockers.append("physical_quantum_qi_process_tensor_execution_feedback_license_not_ready")
    for name in [
        "guarded_transition_execution_record_read_allowed",
        "next_cycle_state_read_allowed",
        "memory_consumption_ledger_read_allowed",
        "external_state_mutation_ledger_read_allowed",
        "process_tensor_feedback_append_allowed",
        "path_integral_feedback_state_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, execution_status = _validate_execution_record(_read_json(execution_record_path), blockers)
    next_cycle = _read_json(next_cycle_state_path)
    memory_receipt = _latest_jsonl(memory_ledger_path)
    external_receipt = _latest_jsonl(external_ledger_path)
    next_seen = bool(next_cycle.get("next_cycle_started") is True)
    memory_seen = bool(memory_receipt.get("memory_consumed") is True)
    external_seen = bool(external_receipt.get("external_state_mutated") is True)
    if execution_status == "guarded_transition_executed":
        if not next_seen:
            blockers.append("executed_transition_next_cycle_state_not_observed")
        if not memory_seen:
            blockers.append("executed_transition_memory_consumption_not_observed")
        if not external_seen:
            blockers.append("executed_transition_external_state_mutation_not_observed")
    elif next_seen or memory_seen or external_seen:
        blockers.append("hold_or_block_transition_with_unexpected_runtime_effect_observed")

    packet: dict[str, Any] = {}
    appended = feedback_state_updated = False
    feedback_status = "process_tensor_feedback_block_context"
    if not blockers:
        epoch = int(time.time())
        kernel = _feedback_kernel(
            execution_status=execution_status,
            memory_seen=memory_seen,
            external_seen=external_seen,
            next_seen=next_seen,
            intent_count=int(payload.get("intent_count", 0) or 0),
        )
        feedback_status = str(kernel["feedback_status"])
        packet = {
            "version": "physical_quantum_qi_process_tensor_execution_feedback_packet_v12_7",
            "feedback_status": feedback_status,
            "execution_status": execution_status,
            "process_tensor_feedback_kernel": kernel,
            "observed_effects": {
                "next_cycle_observed": next_seen,
                "memory_feedback_observed": memory_seen,
                "external_backaction_observed": external_seen,
            },
            "process_tensor_context": dict(payload.get("process_tensor_context", {})),
            "source_digests": {
                "execution_record": str(payload.get("source_execution_record_digest", "")),
                "next_cycle_state": str(next_cycle.get("next_cycle_state_digest", "")),
                "memory_consumption": str(memory_receipt.get("memory_consumption_digest", "")),
                "external_state_mutation": str(external_receipt.get("external_state_mutation_digest", "")),
            },
            "boundary": {
                "process_tensor_execution_feedback_only": True,
                "uses_execution_effects_as_non_markov_feedback": True,
                "feeds_path_integral_weighting": True,
                "history_window_feedback_required": True,
                "memory_kernel_feedback_required": True,
                "external_backaction_visible": True,
                "feedback_not_direct_truth": True,
                "feedback_not_unbounded_execution": True,
                "runtime_local_feedback_only": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        packet["process_tensor_execution_feedback_digest"] = _sha(packet)
        _write_json(feedback_packet_path, packet)
        _append_jsonl(feedback_ledger_path, packet)
        appended = True
        path_integral_state = {
            "version": "physical_quantum_qi_path_integral_feedback_state_v12_7",
            "path_integral_feedback_ready": True,
            "feedback_status": feedback_status,
            "path_weight_delta": kernel["path_weight_delta"],
            "memory_feedback_weight": kernel["memory_feedback_weight"],
            "external_backaction_weight": kernel["external_backaction_weight"],
            "next_cycle_amplitude_delta": kernel["next_cycle_amplitude_delta"],
            "source_process_tensor_execution_feedback_digest": packet["process_tensor_execution_feedback_digest"],
            "process_tensor_context": dict(packet["process_tensor_context"]),
            "boundary": {
                "path_integral_feedback_state_only": True,
                "can_feed_next_path_integral_cycle": execution_status == "guarded_transition_executed",
                "non_markov_feedback_preserved": True,
                "feedback_not_direct_authority": True,
            },
            "epoch": epoch,
        }
        path_integral_state["path_integral_feedback_state_digest"] = _sha(path_integral_state)
        _write_json(path_integral_feedback_state_path, path_integral_state)
        feedback_state_updated = True

    status = "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_READY" if not blockers else "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_BLOCKED"
    packet_id = "physical-quantum-qi-process-tensor-execution-feedback-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_process_tensor_execution_feedback_v12_7",
        "status": status,
        "packet_id": packet_id,
        "execution_status": execution_status,
        "feedback_status": feedback_status,
        "process_tensor_feedback_appended": appended,
        "path_integral_feedback_state_updated": feedback_state_updated,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiProcessTensorExecutionFeedbackResult(
        "kuuos_runtime_daemon_physical_quantum_qi_process_tensor_execution_feedback_v12_7",
        status,
        packet_id,
        str(root),
        execution_status,
        feedback_status,
        appended,
        feedback_state_updated,
        memory_seen,
        external_seen,
        next_seen,
        str(feedback_packet_path),
        str(feedback_ledger_path),
        str(path_integral_feedback_state_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
