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
REQUIRED_V12_5_RECEIPT_BOUNDARY_FLAGS = (
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
class PhysicalQuantumQiV12_5ToV12_6TransitionExecutorBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_status: str
    execution_intent_status: str
    expected_v12_6_execution_status: str
    intent_count: int
    executor_ready_state_written: bool
    bridge_ledger_appended: bool
    executor_ready_state_path: str
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


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _as_list(value: Any) -> list[dict[str, Any]]:
    return [dict(_m(item)) for item in value] if isinstance(value, list) else []


def _validate_context(ctx: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    out = {key: str(ctx.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
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


def _validate_intent(intent: Mapping[str, Any], idx: int, context: Mapping[str, str], blockers: list[str]) -> dict[str, Any]:
    boundary = _m(intent.get("boundary"))
    for name in REQUIRED_INTENT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"v12_6_bridge_intent_{idx}_boundary_{name}_missing")
    if intent.get("intent_type") != "physical_quantum_qi_guarded_execution_intent":
        blockers.append(f"v12_6_bridge_intent_{idx}_type_invalid")
    if _int(intent.get("intent_index")) != idx:
        blockers.append(f"v12_6_bridge_intent_{idx}_index_mismatch")
    if intent.get("transition_precheck_decision") != "transition_precheck_admit_candidate":
        blockers.append(f"v12_6_bridge_intent_{idx}_precheck_decision_invalid")
    if intent.get("corridor_stability_gate_decision") != "corridor_stability_admit":
        blockers.append(f"v12_6_bridge_intent_{idx}_stability_decision_invalid")
    weighting = _normalize_weighting(_m(intent.get("candidate_weighting")))
    if weighting["path_weight_delta"] <= 0 or weighting["probe_potential_required"] or weighting["barrier_potential_required"] or weighting["barrier_blocks_ready_weight"]:
        blockers.append(f"v12_6_bridge_intent_{idx}_weighting_not_executable")
    item_context = dict(_m(intent.get("process_tensor_context")))
    for key, value in context.items():
        if str(item_context.get(key, "")) != value:
            blockers.append(f"v12_6_bridge_intent_{idx}_{key}_mismatch")
    return {
        "intent_index": idx,
        "candidate_id": str(intent.get("candidate_id", f"v12-6-bridge-candidate-{idx}")),
        "transition_precheck_decision": str(intent.get("transition_precheck_decision", "")),
        "corridor_stability_gate_decision": str(intent.get("corridor_stability_gate_decision", "")),
        "candidate_weighting": weighting,
        "process_tensor_context": item_context,
        "source_guarded_execution_intent_digest": str(intent.get("guarded_execution_intent_digest", _sha(dict(intent)))),
        "source_transition_candidate_envelope_digest": str(intent.get("source_transition_candidate_envelope_digest", "")),
    }


def _validate_v12_5_receipt(record: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], str]:
    if not record:
        return {}, "guarded_transition_block"
    if record.get("record_type") != "physical_quantum_qi_guarded_execution_intent_receipt":
        blockers.append("v12_5_guarded_execution_intent_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_V12_5_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"v12_5_guarded_execution_intent_receipt_boundary_{name}_missing")
    intent_status = str(record.get("execution_intent_status", "guarded_execution_intent_block"))
    if intent_status not in EXECUTION_BY_INTENT:
        blockers.append("v12_5_guarded_execution_intent_status_invalid")
        intent_status = "guarded_execution_intent_block"
    execution_status = EXECUTION_BY_INTENT[intent_status]
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    intents = _as_list(record.get("guarded_execution_intents"))
    intent_count = _int(record.get("intent_count"))
    if intent_count != len(intents):
        blockers.append("v12_5_guarded_execution_intent_count_mismatch")
    if intent_status == "guarded_execution_intent_ready" and intent_count <= 0:
        blockers.append("v12_6_bridge_ready_without_intents")
    if intent_status != "guarded_execution_intent_ready" and intent_count != 0:
        blockers.append("v12_6_bridge_hold_or_block_with_intents")
    clean_intents = [_validate_intent(item, idx, context, blockers) for idx, item in enumerate(intents)] if intent_status == "guarded_execution_intent_ready" else []
    payload = {
        "execution_intent_status": intent_status,
        "expected_v12_6_execution_status": execution_status,
        "intent_count": len(clean_intents),
        "guarded_execution_intents": clean_intents,
        "process_tensor_context": context,
        "source_v12_5_guarded_execution_intent_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_guarded_execution_intent_packet_digest": str(record.get("source_guarded_execution_intent_packet_digest", "")),
    }
    return payload, execution_status


def _effects(execution_status: str) -> dict[str, bool]:
    return {
        "internal_transition_record": True,
        "next_cycle_state_update": execution_status == "guarded_transition_executed",
        "memory_consumption": execution_status == "guarded_transition_executed",
        "external_state_mutation": execution_status == "guarded_transition_executed",
    }


def build_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge(
    *,
    runtime_context: Mapping[str, Any],
    v12_5_to_v12_6_transition_executor_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiV12_5ToV12_6TransitionExecutorBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(v12_5_to_v12_6_transition_executor_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    v12_5_ledger_path = root / "physical_quantum_qi_guarded_execution_intent_receipt_ledger.jsonl"
    ready_state_path = root / "physical_quantum_qi_v12_6_guarded_transition_executor_ready_state.json"
    bridge_ledger_path = root / "physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_summary.json"
    receipt_path = root / "physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_receipt.json"
    audit_path = root / "physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V12_5_TO_V12_6_TRANSITION_EXECUTOR_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_license_not_ready")
    for name in [
        "v12_5_guarded_execution_intent_receipt_ledger_read_allowed",
        "v12_6_transition_executor_ready_state_write_allowed",
        "bridge_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, execution_status = _validate_v12_5_receipt(_latest_jsonl(v12_5_ledger_path, blockers), blockers)
    state_written = ledger_appended = False
    bridge_status = "v12_5_to_v12_6_transition_executor_bridge_block"
    if not blockers:
        epoch = int(time.time())
        bridge_status = "v12_5_to_v12_6_transition_executor_bridge_" + execution_status.rsplit("_", 1)[-1]
        effects = _effects(execution_status)
        state = {
            "version": "physical_quantum_qi_v12_6_guarded_transition_executor_ready_state_v13_9",
            "transition_executor_ready_state": True,
            "bridge_status": bridge_status,
            "execution_intent_status": payload["execution_intent_status"],
            "expected_v12_6_execution_status": execution_status,
            "intent_count": payload["intent_count"],
            "expected_effects": effects,
            "source_v12_5_guarded_execution_intent_receipt_digest": payload["source_v12_5_guarded_execution_intent_receipt_digest"],
            "source_guarded_execution_intent_packet_digest": payload["source_guarded_execution_intent_packet_digest"],
            "process_tensor_context": dict(payload["process_tensor_context"]),
            "boundary": {
                "v12_6_transition_executor_ready_state_only": True,
                "v12_5_guarded_execution_intent_receipt_required": True,
                "can_feed_v12_6_guarded_transition_executor": True,
                "execution_layer_entrypoint": True,
                "no_dry_run_required": True,
                "license_gated_execution": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_execution": True,
                "does_not_run_executor": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        state["transition_executor_ready_state_digest"] = _sha(state)
        _write_json(ready_state_path, state)
        state_written = True
        record = {
            "version": "physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_record_v13_9",
            "record_type": "physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge",
            "bridge_status": bridge_status,
            "execution_intent_status": payload["execution_intent_status"],
            "expected_v12_6_execution_status": execution_status,
            "intent_count": payload["intent_count"],
            "source_transition_executor_ready_state_digest": state["transition_executor_ready_state_digest"],
            "source_v12_5_guarded_execution_intent_receipt_digest": payload["source_v12_5_guarded_execution_intent_receipt_digest"],
            "prev_record_digest": _last_digest(bridge_ledger_path),
            "boundary": {
                "bridge_receipt_only": True,
                "v12_6_transition_executor_ready_state_traceable": True,
                "same_semantic_root": True,
                "uses_process_tensor_feedback": True,
                "bridge_not_direct_execution": True,
                "replayable_receipt": True,
            },
            "epoch": epoch,
        }
        record["record_digest"] = _sha(record)
        _append_jsonl(bridge_ledger_path, record)
        ledger_appended = True
        summary = {
            "version": "physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_summary_v13_9",
            "bridge_status": bridge_status,
            "execution_intent_status": payload["execution_intent_status"],
            "expected_v12_6_execution_status": execution_status,
            "intent_count": payload["intent_count"],
            "transition_executor_ready_state_digest": state["transition_executor_ready_state_digest"],
            "boundary": {
                "summary_only": True,
                "can_feed_v12_6_guarded_transition_executor": True,
                "bridge_not_direct_execution": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    final_status = "PHYSICAL_QUANTUM_QI_V12_5_TO_V12_6_TRANSITION_EXECUTOR_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_V12_5_TO_V12_6_TRANSITION_EXECUTOR_BRIDGE_BLOCKED"
    packet_id = "physical-quantum-qi-v12-5-to-v12-6-transition-executor-bridge-" + _sha({"payload": payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_v13_9",
        "status": final_status,
        "packet_id": packet_id,
        "bridge_status": bridge_status,
        "execution_intent_status": str(payload.get("execution_intent_status", "guarded_execution_intent_block")),
        "expected_v12_6_execution_status": execution_status,
        "intent_count": int(payload.get("intent_count", 0)) if payload else 0,
        "executor_ready_state_written": state_written,
        "bridge_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiV12_5ToV12_6TransitionExecutorBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_v13_9",
        final_status,
        packet_id,
        str(root),
        bridge_status,
        str(payload.get("execution_intent_status", "guarded_execution_intent_block")),
        execution_status,
        int(payload.get("intent_count", 0)) if payload else 0,
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
