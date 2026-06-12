#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


EXECUTION_BY_INTENT = {
    "guarded_execution_intent_ready": "guarded_transition_executed",
    "guarded_execution_intent_hold": "guarded_transition_hold",
    "guarded_execution_intent_block": "guarded_transition_block",
}
REQUIRED_RECEIPT_BOUNDARY_FLAGS = (
    "receipt_ledger_only",
    "guarded_execution_intent_receipt_only",
    "execution_layer_entrypoint",
    "no_dry_run_required",
    "requires_guarded_execution_license",
    "intent_not_world_mutation",
    "does_not_start_next_cycle",
    "does_not_mutate_external_state",
    "does_not_commit_plan",
    "does_not_consume_memory",
    "does_not_promote_truth",
    "receipt_does_not_mutate_intent_packet",
    "replayable_receipt",
    "fail_closed_on_boundary_loss",
)
REQUIRED_INTENT_BOUNDARY_FLAGS = (
    "guarded_execution_intent_only",
    "execution_layer_entrypoint",
    "no_dry_run_required",
    "requires_guarded_execution_license",
    "intent_not_world_mutation",
    "does_not_start_next_cycle",
    "does_not_mutate_external_state",
    "does_not_consume_memory",
    "does_not_promote_truth",
)
REQUIRED_CONTEXT_KEYS = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)


@dataclass(frozen=True)
class PhysicalQuantumQiV12_5ReceiptToV12_6ExecutorReadinessBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_status: str
    execution_intent_status: str
    expected_v12_6_execution_status: str
    intent_count: int
    readiness_state_written: bool
    bridge_ledger_appended: bool
    readiness_state_path: str
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


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _latest_jsonl(path: pathlib.Path, blockers: list[str]) -> dict[str, Any]:
    if not path.is_file():
        blockers.append("v12_5_guarded_execution_intent_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("v12_5_guarded_execution_intent_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("v12_5_guarded_execution_intent_receipt_ledger_latest_line_invalid")
        return {}
    return value if isinstance(value, dict) else {}


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


def _validate_context(context: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    out = {key: str(context.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, value in out.items():
        if not value:
            blockers.append(f"process_tensor_context_{key}_missing")
    return out


def _normalize_weighting(weighting: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "path_weight_delta": _int(weighting.get("path_weight_delta")),
        "probe_potential_required": weighting.get("probe_potential_required") is True,
        "barrier_potential_required": weighting.get("barrier_potential_required") is True,
        "barrier_blocks_ready_weight": weighting.get("barrier_blocks_ready_weight") is True,
        "memory_feedback_weight": _int(weighting.get("memory_feedback_weight")),
        "external_backaction_weight": _int(weighting.get("external_backaction_weight")),
        "next_cycle_amplitude_delta": _int(weighting.get("next_cycle_amplitude_delta")),
    }


def _validate_intent(intent: Mapping[str, Any], index: int, context: Mapping[str, str], blockers: list[str]) -> dict[str, Any]:
    boundary = _m(intent.get("boundary"))
    for flag in REQUIRED_INTENT_BOUNDARY_FLAGS:
        if boundary.get(flag) is not True:
            blockers.append(f"v13_22_intent_{index}_boundary_{flag}_missing")
    if intent.get("intent_type") != "physical_quantum_qi_guarded_execution_intent":
        blockers.append(f"v13_22_intent_{index}_type_invalid")
    if _int(intent.get("intent_index")) != index:
        blockers.append(f"v13_22_intent_{index}_index_mismatch")
    if intent.get("transition_precheck_decision") != "transition_precheck_admit_candidate":
        blockers.append(f"v13_22_intent_{index}_precheck_invalid")
    if intent.get("corridor_stability_gate_decision") != "corridor_stability_admit":
        blockers.append(f"v13_22_intent_{index}_stability_invalid")
    weighting = _normalize_weighting(_m(intent.get("candidate_weighting")))
    if weighting["path_weight_delta"] <= 0 or weighting["probe_potential_required"] or weighting["barrier_potential_required"] or weighting["barrier_blocks_ready_weight"]:
        blockers.append(f"v13_22_intent_{index}_weighting_not_executable")
    item_context = dict(_m(intent.get("process_tensor_context")))
    for key, value in context.items():
        if str(item_context.get(key, "")) != value:
            blockers.append(f"v13_22_intent_{index}_{key}_mismatch")
    return {
        "intent_index": index,
        "candidate_id": str(intent.get("candidate_id", f"v13-22-candidate-{index}")),
        "candidate_weighting": weighting,
        "process_tensor_context": item_context,
        "source_guarded_execution_intent_digest": str(intent.get("guarded_execution_intent_digest", _sha(dict(intent)))),
        "source_transition_candidate_envelope_digest": str(intent.get("source_transition_candidate_envelope_digest", "")),
    }


def _validate_receipt(record: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    if not record:
        return {}
    if record.get("record_type") != "physical_quantum_qi_guarded_execution_intent_receipt":
        blockers.append("v12_5_guarded_execution_intent_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for flag in REQUIRED_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(flag) is not True:
            blockers.append(f"v12_5_guarded_execution_intent_receipt_boundary_{flag}_missing")
    intent_status = str(record.get("execution_intent_status", "guarded_execution_intent_block"))
    if intent_status not in EXECUTION_BY_INTENT:
        blockers.append("v12_5_guarded_execution_intent_status_invalid")
        intent_status = "guarded_execution_intent_block"
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    intents_raw = record.get("guarded_execution_intents", [])
    intents = [dict(_m(item)) for item in intents_raw] if isinstance(intents_raw, list) else []
    count = _int(record.get("intent_count"))
    if count != len(intents):
        blockers.append("v12_5_guarded_execution_intent_count_mismatch")
    if intent_status == "guarded_execution_intent_ready" and count <= 0:
        blockers.append("v13_22_ready_without_intents")
    if intent_status != "guarded_execution_intent_ready" and count != 0:
        blockers.append("v13_22_hold_or_block_with_intents")
    clean = [_validate_intent(item, index, context, blockers) for index, item in enumerate(intents)] if intent_status == "guarded_execution_intent_ready" else []
    return {
        "execution_intent_status": intent_status,
        "expected_v12_6_execution_status": EXECUTION_BY_INTENT[intent_status],
        "intent_count": len(clean),
        "guarded_execution_intents": clean,
        "process_tensor_context": context,
        "source_v12_5_guarded_execution_intent_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_guarded_execution_intent_packet_digest": str(record.get("source_guarded_execution_intent_packet_digest", "")),
    }


def build_physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge(
    *,
    runtime_context: Mapping[str, Any],
    v12_5_receipt_to_v12_6_executor_readiness_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiV12_5ReceiptToV12_6ExecutorReadinessBridgeResult:
    ctx = _m(runtime_context)
    license_packet = _m(v12_5_receipt_to_v12_6_executor_readiness_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    source_ledger = root / "physical_quantum_qi_guarded_execution_intent_receipt_ledger.jsonl"
    ready_state = root / "physical_quantum_qi_v13_9_transition_executor_bridge_ready_state.json"
    bridge_ledger = root / "physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_ledger.jsonl"
    summary = root / "physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_summary.json"
    receipt = root / "physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_receipt.json"
    audit = root / "physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_not_true")
    if license_packet.get("license_status") != "PHYSICAL_QUANTUM_QI_V12_5_RECEIPT_TO_V12_6_EXECUTOR_READINESS_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_license_not_ready")
    for flag in (
        "v12_5_receipt_ledger_read_allowed",
        "v13_9_bridge_ready_state_write_allowed",
        "bridge_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_packet.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    payload = _validate_receipt(_latest_jsonl(source_ledger, blockers), blockers)
    state_written = ledger_appended = False
    bridge_status = "v12_5_receipt_to_v12_6_executor_readiness_bridge_block"
    if not blockers:
        epoch = int(time.time())
        execution_status = payload["expected_v12_6_execution_status"]
        bridge_status = "v12_5_receipt_to_v12_6_executor_readiness_bridge_" + execution_status.rsplit("_", 1)[-1]
        state = {
            "version": "physical_quantum_qi_v13_9_transition_executor_bridge_ready_state_v13_22",
            "transition_executor_bridge_ready_state": True,
            "bridge_status": bridge_status,
            **payload,
            "expected_effects": {
                "internal_transition_record": True,
                "next_cycle_state_update": execution_status == "guarded_transition_executed",
                "memory_consumption": execution_status == "guarded_transition_executed",
                "external_state_mutation": execution_status == "guarded_transition_executed",
            },
            "boundary": {
                "v13_9_transition_executor_bridge_ready_state_only": True,
                "v12_5_guarded_execution_intent_receipt_required": True,
                "can_feed_v13_9_v12_5_to_v12_6_transition_executor_bridge": True,
                "can_feed_v12_6_guarded_transition_executor_after_v13_9": True,
                "execution_layer_entrypoint": True,
                "no_dry_run_required": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_execution": True,
                "does_not_run_v13_9_bridge": True,
                "does_not_run_v12_6_executor": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        state["transition_executor_bridge_ready_state_digest"] = _sha(state)
        _write_json(ready_state, state)
        state_written = True
        record = {
            "version": "physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_record_v13_22",
            "record_type": "physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge",
            "bridge_status": bridge_status,
            "execution_intent_status": payload["execution_intent_status"],
            "expected_v12_6_execution_status": execution_status,
            "intent_count": payload["intent_count"],
            "source_transition_executor_bridge_ready_state_digest": state["transition_executor_bridge_ready_state_digest"],
            "source_v12_5_guarded_execution_intent_receipt_digest": payload["source_v12_5_guarded_execution_intent_receipt_digest"],
            "prev_record_digest": _last_digest(bridge_ledger),
            "boundary": {
                "bridge_receipt_only": True,
                "v13_9_transition_executor_bridge_ready_state_traceable": True,
                "same_semantic_root": True,
                "uses_process_tensor_feedback": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_execution": True,
                "replayable_receipt": True,
            },
            "epoch": epoch,
        }
        record["record_digest"] = _sha(record)
        _append_jsonl(bridge_ledger, record)
        ledger_appended = True
        summary_payload = {
            "version": "physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_summary_v13_22",
            "bridge_status": bridge_status,
            "execution_intent_status": payload["execution_intent_status"],
            "expected_v12_6_execution_status": execution_status,
            "intent_count": payload["intent_count"],
            "transition_executor_bridge_ready_state_digest": state["transition_executor_bridge_ready_state_digest"],
            "boundary": {
                "summary_only": True,
                "can_feed_v13_9_v12_5_to_v12_6_transition_executor_bridge": True,
                "bridge_not_direct_execution": True,
            },
            "epoch": epoch,
        }
        summary_payload["summary_digest"] = _sha(summary_payload)
        _write_json(summary, summary_payload)

    status = "PHYSICAL_QUANTUM_QI_V12_5_RECEIPT_TO_V12_6_EXECUTOR_READINESS_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_V12_5_RECEIPT_TO_V12_6_EXECUTOR_READINESS_BRIDGE_BLOCKED"
    execution_intent_status = str(payload.get("execution_intent_status", "guarded_execution_intent_block"))
    expected_execution_status = str(payload.get("expected_v12_6_execution_status", "guarded_transition_block"))
    intent_count = _int(payload.get("intent_count"))
    packet_id = "physical-quantum-qi-v12-5-receipt-to-v12-6-executor-readiness-bridge-" + _sha({"payload": payload, "blockers": blockers})[:16]
    receipt_payload = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_v13_22",
        "status": status,
        "packet_id": packet_id,
        "bridge_status": bridge_status,
        "execution_intent_status": execution_intent_status,
        "expected_v12_6_execution_status": expected_execution_status,
        "intent_count": intent_count,
        "readiness_state_written": state_written,
        "bridge_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if license_packet.get("receipt_write_allowed") is True:
        _write_json(receipt, receipt_payload)
    if license_packet.get("audit_append_allowed") is True:
        _append_jsonl(audit, {**receipt_payload, "audit_record_digest": _sha(receipt_payload)})
    return PhysicalQuantumQiV12_5ReceiptToV12_6ExecutorReadinessBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_v13_22",
        status,
        packet_id,
        str(root),
        bridge_status,
        execution_intent_status,
        expected_execution_status,
        intent_count,
        state_written,
        ledger_appended,
        str(ready_state),
        str(bridge_ledger),
        str(summary),
        str(receipt),
        str(audit),
        blockers,
        warnings,
    )
