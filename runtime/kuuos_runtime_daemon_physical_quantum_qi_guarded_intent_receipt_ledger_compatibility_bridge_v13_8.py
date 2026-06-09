#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


STATUS_TO_V12 = {
    "guarded_execution_intent_ready": ("transition_candidate_envelope_ready", "transition_precheck_admit_candidate"),
    "guarded_execution_intent_hold": ("transition_candidate_envelope_hold", "transition_precheck_hold_candidate"),
    "guarded_execution_intent_block": ("transition_candidate_envelope_block", "transition_precheck_block_candidate"),
}
EXPECTED_BRIDGE = {
    "guarded_execution_intent_ready": "integrated_candidate_to_guarded_intent_ready",
    "guarded_execution_intent_hold": "integrated_candidate_to_guarded_intent_hold",
    "guarded_execution_intent_block": "integrated_candidate_to_guarded_intent_block",
}
REQUIRED_RECEIPT_BOUNDARY_FLAGS = (
    "receipt_ledger_only",
    "guarded_intent_bridge_receipt_only",
    "guarded_execution_intent_packet_traceable",
    "guarded_execution_intent_bridge_state_traceable",
    "uses_process_tensor_feedback",
    "non_markov_feedback_preserved",
    "history_window_feedback_preserved",
    "memory_kernel_feedback_preserved",
    "external_backaction_visible",
    "candidate_weighting_not_truth",
    "bridge_not_direct_execution",
    "replayable_receipt",
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
class PhysicalQuantumQiGuardedIntentReceiptLedgerCompatibilityBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    compatibility_bridge_status: str
    execution_intent_status: str
    intent_count: int
    v12_5_packet_written: bool
    compatibility_state_written: bool
    compatibility_ledger_appended: bool
    v12_5_packet_path: str
    compatibility_state_path: str
    compatibility_ledger_path: str
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
        blockers.append("guarded_intent_bridge_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("guarded_intent_bridge_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("guarded_intent_bridge_receipt_ledger_latest_line_invalid")
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


def _validate_context(ctx: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    out = {key: str(ctx.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, value in out.items():
        if not value:
            blockers.append(f"process_tensor_context_{key}_missing")
    return out


def _validate_weighting(status: str, weighting: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    norm = _normalize_weighting(weighting)
    if status == "guarded_execution_intent_ready":
        if norm["path_weight_delta"] <= 0:
            blockers.append("v12_5_compat_ready_without_positive_path_weight_delta")
        if norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("v12_5_compat_ready_with_probe_or_barrier")
    elif status == "guarded_execution_intent_hold":
        if norm["path_weight_delta"] != 0 or not norm["probe_potential_required"] or norm["barrier_potential_required"]:
            blockers.append("v12_5_compat_hold_weighting_invalid")
    elif status == "guarded_execution_intent_block":
        if norm["path_weight_delta"] != 0 or norm["probe_potential_required"] or not norm["barrier_potential_required"] or not norm["barrier_blocks_ready_weight"]:
            blockers.append("v12_5_compat_block_weighting_invalid")
    return norm


def _validate_receipt(record: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], str]:
    if not record:
        return {}, "guarded_execution_intent_block"
    if record.get("record_type") != "physical_quantum_qi_guarded_intent_bridge_receipt":
        blockers.append("guarded_intent_bridge_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"guarded_intent_bridge_receipt_boundary_{name}_missing")
    status = str(record.get("guarded_execution_intent_status", "guarded_execution_intent_block"))
    if status not in STATUS_TO_V12:
        blockers.append("guarded_execution_intent_status_invalid")
        status = "guarded_execution_intent_block"
    bridge_status = str(record.get("bridge_status", ""))
    if bridge_status != EXPECTED_BRIDGE[status]:
        blockers.append("guarded_intent_bridge_status_mismatch")
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(status, _m(record.get("candidate_weighting")), blockers)
    intents = record.get("guarded_execution_intents", [])
    if not isinstance(intents, list):
        blockers.append("guarded_execution_intents_not_list")
        intents = []
    count = _int(record.get("guarded_execution_intent_count"))
    if count != len(intents):
        blockers.append("guarded_execution_intent_count_mismatch")
    if status == "guarded_execution_intent_ready" and count <= 0:
        blockers.append("v12_5_compat_ready_requires_intent")
    if status != "guarded_execution_intent_ready" and count != 0:
        blockers.append("v12_5_compat_hold_or_block_with_intent")
    payload = {
        "execution_intent_status": status,
        "bridge_status": bridge_status,
        "guarded_execution_intents": [dict(_m(item)) for item in intents],
        "intent_count": count,
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_guarded_intent_bridge_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_guarded_execution_intent_packet_digest": str(record.get("source_guarded_execution_intent_packet_digest", "")),
        "source_integrated_candidate_to_guarded_intent_bridge_digest": str(record.get("source_integrated_candidate_to_guarded_intent_bridge_digest", "")),
    }
    return payload, status


def _normalized_v12_5_intents(payload: Mapping[str, Any], blockers: list[str]) -> list[dict[str, Any]]:
    status = str(payload.get("execution_intent_status", "guarded_execution_intent_block"))
    if status != "guarded_execution_intent_ready":
        return []
    context = dict(_m(payload.get("process_tensor_context")))
    out: list[dict[str, Any]] = []
    for idx, raw in enumerate(payload.get("guarded_execution_intents", [])):
        item = dict(_m(raw))
        weighting = _normalize_weighting(_m(item.get("candidate_weighting") or payload.get("candidate_weighting")))
        if weighting != payload.get("candidate_weighting"):
            blockers.append(f"guarded_execution_intent_{idx}_weighting_mismatch")
        item_context = dict(_m(item.get("process_tensor_context") or context))
        for key, value in context.items():
            if str(item_context.get(key, "")) != value:
                blockers.append(f"guarded_execution_intent_{idx}_{key}_mismatch")
        intent = {
            "intent_index": idx,
            "intent_type": "physical_quantum_qi_guarded_execution_intent",
            "candidate_id": str(item.get("candidate_id", f"v13-compat-candidate-{idx}")),
            "transition_precheck_decision": "transition_precheck_admit_candidate",
            "corridor_stability_gate_decision": "corridor_stability_admit",
            "candidate_weighting": weighting,
            "process_tensor_context": context,
            "source_transition_candidate_envelope_digest": str(item.get("source_transition_candidate_envelope_digest") or item.get("source_integrated_candidate_digest") or payload.get("source_guarded_intent_bridge_receipt_digest", "")),
            "guarded_execution_intent_digest": str(item.get("guarded_execution_intent_digest", _sha(item))),
            "boundary": {
                "guarded_execution_intent_only": True,
                "execution_layer_entrypoint": True,
                "no_dry_run_required": True,
                "requires_guarded_execution_license": True,
                "intent_not_world_mutation": True,
                "does_not_start_next_cycle": True,
                "does_not_mutate_external_state": True,
                "does_not_consume_memory": True,
                "does_not_promote_truth": True,
            },
        }
        out.append(intent)
    return out


def _v12_5_packet(payload: Mapping[str, Any], normalized_intents: list[dict[str, Any]]) -> dict[str, Any]:
    status = str(payload.get("execution_intent_status", "guarded_execution_intent_block"))
    envelope_status, precheck = STATUS_TO_V12[status]
    packet = {
        "version": "physical_quantum_qi_guarded_execution_intent_packet_v13_8_compat_v12_5",
        "physical_quantum_qi_guarded_execution_intent_considered": True,
        "execution_intent_status": status,
        "envelope_status": envelope_status,
        "transition_precheck_decision": precheck,
        "intent_count": len(normalized_intents),
        "envelope_count": len(normalized_intents),
        "guarded_execution_intents": normalized_intents,
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_digests": {
            "transition_candidate_envelope_receipt": str(payload.get("source_guarded_intent_bridge_receipt_digest", "")),
            "transition_candidate_envelope_packet": str(payload.get("source_integrated_candidate_to_guarded_intent_bridge_digest", "")),
            "guarded_intent_bridge_receipt": str(payload.get("source_guarded_intent_bridge_receipt_digest", "")),
            "guarded_execution_intent_packet_v13_6": str(payload.get("source_guarded_execution_intent_packet_digest", "")),
        },
        "boundary": {
            "guarded_execution_intent_only": True,
            "execution_layer_entrypoint": True,
            "no_dry_run_required": True,
            "transition_candidate_envelope_required": True,
            "history_bearing_process_tensor": True,
            "non_markov_context_required": True,
            "multi_time_window_required": True,
            "finite_horizon_only": True,
            "memory_kernel_visible": True,
            "requires_guarded_execution_license": True,
            "intent_not_world_mutation": True,
            "does_not_start_next_cycle": True,
            "does_not_mutate_external_state": True,
            "does_not_commit_plan": True,
            "does_not_consume_memory": True,
            "does_not_promote_truth": True,
            "candidate_weighting_not_truth": True,
            "fail_closed_on_boundary_loss": True,
        },
        "compatibility": {
            "source_version": "v13_7_guarded_intent_bridge_receipt",
            "target_version": "v12_5_guarded_execution_intent_receipt_ledger",
            "compatibility_bridge": "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_v13_8",
            "same_semantic_root": True,
        },
        "epoch": int(time.time()),
    }
    packet["guarded_execution_intent_packet_digest"] = _sha(packet)
    return packet


def build_physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge(
    *,
    runtime_context: Mapping[str, Any],
    guarded_intent_receipt_ledger_compatibility_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiGuardedIntentReceiptLedgerCompatibilityBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(guarded_intent_receipt_ledger_compatibility_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    source_ledger_path = root / "physical_quantum_qi_guarded_intent_bridge_receipt_ledger.jsonl"
    v12_packet_path = root / "physical_quantum_qi_guarded_execution_intent_packet.json"
    state_path = root / "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_state.json"
    ledger_path = root / "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_summary.json"
    receipt_path = root / "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_receipt.json"
    audit_path = root / "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_license_not_ready")
    for name in [
        "guarded_intent_bridge_receipt_ledger_read_allowed",
        "v12_5_guarded_execution_intent_packet_write_allowed",
        "compatibility_bridge_state_write_allowed",
        "compatibility_bridge_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, status_value = _validate_receipt(_latest_jsonl(source_ledger_path, blockers), blockers)
    normalized_intents = _normalized_v12_5_intents(payload, blockers) if payload else []
    v12_packet: dict[str, Any] = {}
    packet_written = state_written = ledger_appended = False
    bridge_status = "guarded_intent_receipt_ledger_compatibility_bridge_block"
    if not blockers:
        bridge_status = "guarded_intent_receipt_ledger_compatibility_bridge_" + status_value.rsplit("_", 1)[-1]
        v12_packet = _v12_5_packet(payload, normalized_intents)
        _write_json(v12_packet_path, v12_packet)
        packet_written = True
        state = {
            "version": "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_state_v13_8",
            "compatibility_bridge_state_ready": True,
            "compatibility_bridge_status": bridge_status,
            "execution_intent_status": status_value,
            "target_v12_5_packet_digest": v12_packet["guarded_execution_intent_packet_digest"],
            "source_guarded_intent_bridge_receipt_digest": payload["source_guarded_intent_bridge_receipt_digest"],
            "boundary": {
                "compatibility_bridge_state_only": True,
                "target_v12_5_guarded_execution_intent_packet_ready": True,
                "can_feed_v12_5_guarded_execution_intent_receipt_ledger": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
            },
            "epoch": int(time.time()),
        }
        state["compatibility_bridge_state_digest"] = _sha(state)
        _write_json(state_path, state)
        state_written = True
        record = {
            "version": "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_record_v13_8",
            "record_type": "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge",
            "compatibility_bridge_status": bridge_status,
            "execution_intent_status": status_value,
            "target_v12_5_packet_digest": v12_packet["guarded_execution_intent_packet_digest"],
            "source_guarded_intent_bridge_receipt_digest": payload["source_guarded_intent_bridge_receipt_digest"],
            "prev_record_digest": _last_digest(ledger_path),
            "boundary": {
                "compatibility_bridge_receipt_only": True,
                "target_v12_5_packet_traceable": True,
                "same_semantic_root": True,
                "uses_process_tensor_feedback": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_execution": True,
                "replayable_receipt": True,
            },
            "epoch": int(time.time()),
        }
        record["record_digest"] = _sha(record)
        _append_jsonl(ledger_path, record)
        ledger_appended = True
        summary = {
            "version": "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_summary_v13_8",
            "compatibility_bridge_status": bridge_status,
            "execution_intent_status": status_value,
            "intent_count": len(normalized_intents),
            "target_v12_5_packet_digest": v12_packet["guarded_execution_intent_packet_digest"],
            "source_guarded_intent_bridge_receipt_digest": payload["source_guarded_intent_bridge_receipt_digest"],
            "boundary": {
                "summary_only": True,
                "compatibility_bridge_only": True,
                "target_v12_5_packet_traceable": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    final_status = "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_BLOCKED"
    packet_id = "physical-quantum-qi-guarded-intent-receipt-compatibility-" + _sha({"packet": v12_packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_v13_8",
        "status": final_status,
        "packet_id": packet_id,
        "compatibility_bridge_status": bridge_status,
        "execution_intent_status": status_value,
        "intent_count": len(normalized_intents),
        "v12_5_packet_written": packet_written,
        "compatibility_state_written": state_written,
        "compatibility_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiGuardedIntentReceiptLedgerCompatibilityBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_v13_8",
        final_status,
        packet_id,
        str(root),
        bridge_status,
        status_value,
        len(normalized_intents),
        packet_written,
        state_written,
        ledger_appended,
        str(v12_packet_path),
        str(state_path),
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
