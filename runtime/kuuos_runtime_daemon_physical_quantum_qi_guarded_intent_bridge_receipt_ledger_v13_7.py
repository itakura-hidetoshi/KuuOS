#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


BRIDGE_STATUSES = {
    "integrated_candidate_to_guarded_intent_ready",
    "integrated_candidate_to_guarded_intent_hold",
    "integrated_candidate_to_guarded_intent_block",
}
EXPECTED_GUARDED_STATUS = {
    "integrated_candidate_to_guarded_intent_ready": "guarded_execution_intent_ready",
    "integrated_candidate_to_guarded_intent_hold": "guarded_execution_intent_hold",
    "integrated_candidate_to_guarded_intent_block": "guarded_execution_intent_block",
}
EXPECTED_EMIT_ACTION = {
    "integrated_candidate_to_guarded_intent_ready": "emit_guarded_ready_intent",
    "integrated_candidate_to_guarded_intent_hold": "emit_guarded_hold_intent",
    "integrated_candidate_to_guarded_intent_block": "emit_guarded_block_intent",
}
REQUIRED_BRIDGE_BOUNDARY_FLAGS = (
    "integrated_candidate_to_guarded_intent_bridge_only",
    "cycle_gate_reentry_integration_receipt_required",
    "emits_guarded_execution_intent_packet",
    "uses_process_tensor_feedback",
    "non_markov_feedback_preserved",
    "history_window_feedback_preserved",
    "memory_kernel_feedback_preserved",
    "external_backaction_visible",
    "candidate_weighting_not_truth",
    "bridge_not_direct_execution",
    "does_not_run_runner",
    "does_not_mutate_external_state",
    "does_not_start_next_cycle",
    "license_gated_bridge",
    "fail_closed_on_boundary_loss",
)
REQUIRED_INTENT_PACKET_BOUNDARY_FLAGS = (
    "guarded_execution_intent_packet_only",
    "from_integrated_candidate_bridge",
    "requires_guarded_execution_license",
    "candidate_weighting_not_truth",
    "not_direct_execution_authority",
    "does_not_run_runner",
    "does_not_mutate_external_state",
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
REQUIRED_STATE_BOUNDARY_FLAGS = (
    "guarded_execution_intent_bridge_state_only",
    "from_integrated_candidate_bridge",
    "can_feed_guarded_execution_intent_receipt_layer",
    "candidate_weighting_not_truth",
    "not_direct_execution_authority",
)
REQUIRED_CONTEXT_KEYS = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)


@dataclass(frozen=True)
class PhysicalQuantumQiGuardedIntentBridgeReceiptLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_status: str
    guarded_execution_intent_status: str
    guarded_intent_emit_action: str
    guarded_execution_intent_count: int
    ledger_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    ledger_appended: bool
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


def _validate_weighting(bridge_status: str, weighting: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    norm = _normalize_weighting(weighting)
    if bridge_status == "integrated_candidate_to_guarded_intent_ready":
        if norm["path_weight_delta"] <= 0:
            blockers.append("guarded_intent_receipt_ready_without_positive_path_weight_delta")
        if norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("guarded_intent_receipt_ready_with_probe_or_barrier")
        if norm["memory_feedback_weight"] <= 0 or norm["external_backaction_weight"] <= 0 or norm["next_cycle_amplitude_delta"] <= 0:
            blockers.append("guarded_intent_receipt_ready_missing_process_tensor_effect_weight")
    elif bridge_status == "integrated_candidate_to_guarded_intent_hold":
        if norm["path_weight_delta"] != 0:
            blockers.append("guarded_intent_receipt_hold_with_path_weight_delta")
        if not norm["probe_potential_required"]:
            blockers.append("guarded_intent_receipt_hold_without_probe_potential")
        if norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("guarded_intent_receipt_hold_with_barrier")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("guarded_intent_receipt_hold_with_effect_weight")
    elif bridge_status == "integrated_candidate_to_guarded_intent_block":
        if norm["path_weight_delta"] != 0:
            blockers.append("guarded_intent_receipt_block_with_path_weight_delta")
        if norm["probe_potential_required"]:
            blockers.append("guarded_intent_receipt_block_with_probe")
        if not norm["barrier_potential_required"] or not norm["barrier_blocks_ready_weight"]:
            blockers.append("guarded_intent_receipt_block_without_blocking_barrier")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("guarded_intent_receipt_block_with_effect_weight")
    return norm


def _validate_bridge_packet(packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], str, str, str, int]:
    if not packet:
        blockers.append("integrated_candidate_to_guarded_intent_bridge_packet_missing_or_invalid")
        return {}, "integrated_candidate_to_guarded_intent_block", "guarded_execution_intent_block", "emit_guarded_block_intent", 0
    if packet.get("integrated_candidate_to_guarded_intent_bridge_considered") is not True:
        blockers.append("integrated_candidate_to_guarded_intent_bridge_considered_not_true")
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_BRIDGE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"integrated_candidate_to_guarded_intent_bridge_boundary_{name}_missing")
    bridge_status = str(packet.get("bridge_status", "integrated_candidate_to_guarded_intent_block"))
    if bridge_status not in BRIDGE_STATUSES:
        blockers.append("integrated_candidate_to_guarded_intent_bridge_status_invalid")
        bridge_status = "integrated_candidate_to_guarded_intent_block"
    guarded_status = str(packet.get("guarded_execution_intent_status", ""))
    emit_action = str(packet.get("guarded_intent_emit_action", ""))
    if guarded_status != EXPECTED_GUARDED_STATUS[bridge_status]:
        blockers.append("guarded_execution_intent_status_mismatch")
        guarded_status = EXPECTED_GUARDED_STATUS[bridge_status]
    if emit_action != EXPECTED_EMIT_ACTION[bridge_status]:
        blockers.append("guarded_intent_emit_action_mismatch")
        emit_action = EXPECTED_EMIT_ACTION[bridge_status]
    count = _int(packet.get("guarded_execution_intent_count"))
    intents = packet.get("guarded_execution_intents", [])
    if not isinstance(intents, list):
        blockers.append("guarded_execution_intents_not_list")
        intents = []
    if count != len(intents):
        blockers.append("guarded_execution_intent_count_mismatch")
    if bridge_status == "integrated_candidate_to_guarded_intent_ready" and count <= 0:
        blockers.append("guarded_intent_receipt_ready_requires_intent")
    if bridge_status != "integrated_candidate_to_guarded_intent_ready" and count != 0:
        blockers.append("guarded_intent_receipt_hold_or_block_with_intent")
    context = _validate_context(_m(packet.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(bridge_status, _m(packet.get("candidate_weighting")), blockers)
    for idx, intent in enumerate(intents):
        ib = _m(_m(intent).get("boundary"))
        for name in REQUIRED_INTENT_BOUNDARY_FLAGS:
            if ib.get(name) is not True:
                blockers.append(f"guarded_execution_intent_{idx}_boundary_{name}_missing")
        if str(_m(intent).get("transition_precheck_decision", "")) != "transition_precheck_admit_candidate":
            blockers.append(f"guarded_execution_intent_{idx}_transition_precheck_decision_invalid")
        if str(_m(intent).get("corridor_stability_gate_decision", "")) != "corridor_stability_admit":
            blockers.append(f"guarded_execution_intent_{idx}_corridor_stability_gate_decision_invalid")
    if not packet.get("integrated_candidate_to_guarded_intent_bridge_digest"):
        warnings.append("integrated_candidate_to_guarded_intent_bridge_digest_missing")
    payload = {
        "bridge_status": bridge_status,
        "guarded_execution_intent_status": guarded_status,
        "guarded_intent_emit_action": emit_action,
        "guarded_execution_intent_count": count,
        "guarded_execution_intents": intents,
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_integrated_candidate_to_guarded_intent_bridge_digest": str(packet.get("integrated_candidate_to_guarded_intent_bridge_digest", _sha(dict(packet)))),
        "source_cycle_gate_reentry_integration_receipt_digest": str(_m(packet.get("source_digests")).get("cycle_gate_reentry_integration_receipt", "")),
        "source_cycle_gate_reentry_integration_digest": str(_m(packet.get("source_digests")).get("cycle_gate_reentry_integration", "")),
    }
    return payload, bridge_status, guarded_status, emit_action, count


def _validate_intent_packet(intent_packet: Mapping[str, Any], payload: Mapping[str, Any], blockers: list[str]) -> None:
    if not intent_packet:
        blockers.append("guarded_execution_intent_packet_missing_or_invalid")
        return
    if intent_packet.get("guarded_execution_intent_packet_ready") is not True:
        blockers.append("guarded_execution_intent_packet_not_ready")
    if str(intent_packet.get("guarded_execution_intent_status", "")) != payload.get("guarded_execution_intent_status"):
        blockers.append("guarded_execution_intent_packet_status_mismatch")
    if _int(intent_packet.get("guarded_execution_intent_count")) != _int(payload.get("guarded_execution_intent_count")):
        blockers.append("guarded_execution_intent_packet_count_mismatch")
    if _normalize_weighting(_m(intent_packet.get("candidate_weighting"))) != payload.get("candidate_weighting"):
        blockers.append("guarded_execution_intent_packet_weighting_mismatch")
    if str(intent_packet.get("source_integrated_candidate_to_guarded_intent_bridge_digest", "")) != payload.get("source_integrated_candidate_to_guarded_intent_bridge_digest"):
        blockers.append("guarded_execution_intent_packet_source_digest_mismatch")
    boundary = _m(intent_packet.get("boundary"))
    for name in REQUIRED_INTENT_PACKET_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"guarded_execution_intent_packet_boundary_{name}_missing")


def _validate_bridge_state(state: Mapping[str, Any], payload: Mapping[str, Any], intent_packet: Mapping[str, Any], blockers: list[str]) -> None:
    if not state:
        blockers.append("guarded_execution_intent_bridge_state_missing_or_invalid")
        return
    if state.get("guarded_execution_intent_bridge_state_ready") is not True:
        blockers.append("guarded_execution_intent_bridge_state_not_ready")
    if str(state.get("bridge_status", "")) != payload.get("bridge_status"):
        blockers.append("guarded_execution_intent_bridge_state_bridge_status_mismatch")
    if str(state.get("guarded_execution_intent_status", "")) != payload.get("guarded_execution_intent_status"):
        blockers.append("guarded_execution_intent_bridge_state_intent_status_mismatch")
    if str(state.get("source_integrated_candidate_to_guarded_intent_bridge_digest", "")) != payload.get("source_integrated_candidate_to_guarded_intent_bridge_digest"):
        blockers.append("guarded_execution_intent_bridge_state_source_digest_mismatch")
    expected_intent_digest = str(intent_packet.get("guarded_execution_intent_packet_digest", "")) if intent_packet else ""
    if str(state.get("guarded_execution_intent_packet_digest", "")) != expected_intent_digest:
        blockers.append("guarded_execution_intent_bridge_state_intent_packet_digest_mismatch")
    boundary = _m(state.get("boundary"))
    for name in REQUIRED_STATE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"guarded_execution_intent_bridge_state_boundary_{name}_missing")


def _record(payload: Mapping[str, Any], intent_packet: Mapping[str, Any], prev_digest: str) -> dict[str, Any]:
    rec = {
        "version": "physical_quantum_qi_guarded_intent_bridge_receipt_record_v13_7",
        "record_type": "physical_quantum_qi_guarded_intent_bridge_receipt",
        "bridge_status": str(payload.get("bridge_status", "")),
        "guarded_execution_intent_status": str(payload.get("guarded_execution_intent_status", "")),
        "guarded_intent_emit_action": str(payload.get("guarded_intent_emit_action", "")),
        "guarded_execution_intent_count": _int(payload.get("guarded_execution_intent_count")),
        "guarded_execution_intents": list(payload.get("guarded_execution_intents", [])),
        "candidate_weighting": dict(_m(payload.get("candidate_weighting"))),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_integrated_candidate_to_guarded_intent_bridge_digest": str(payload.get("source_integrated_candidate_to_guarded_intent_bridge_digest", "")),
        "source_guarded_execution_intent_packet_digest": str(intent_packet.get("guarded_execution_intent_packet_digest", "")),
        "source_cycle_gate_reentry_integration_receipt_digest": str(payload.get("source_cycle_gate_reentry_integration_receipt_digest", "")),
        "source_cycle_gate_reentry_integration_digest": str(payload.get("source_cycle_gate_reentry_integration_digest", "")),
        "prev_record_digest": prev_digest,
        "boundary": {
            "receipt_ledger_only": True,
            "guarded_intent_bridge_receipt_only": True,
            "guarded_execution_intent_packet_traceable": True,
            "guarded_execution_intent_bridge_state_traceable": True,
            "uses_process_tensor_feedback": True,
            "non_markov_feedback_preserved": True,
            "history_window_feedback_preserved": True,
            "memory_kernel_feedback_preserved": True,
            "external_backaction_visible": True,
            "candidate_weighting_not_truth": True,
            "bridge_not_direct_execution": True,
            "replayable_receipt": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def build_physical_quantum_qi_guarded_intent_bridge_receipt_ledger(
    *,
    runtime_context: Mapping[str, Any],
    guarded_intent_bridge_receipt_ledger_license: Mapping[str, Any],
) -> PhysicalQuantumQiGuardedIntentBridgeReceiptLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(guarded_intent_bridge_receipt_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    bridge_packet_path = root / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_packet.json"
    intent_packet_path = root / "physical_quantum_qi_guarded_execution_intent_packet.json"
    bridge_state_path = root / "physical_quantum_qi_guarded_execution_intent_bridge_state.json"
    ledger_path = root / "physical_quantum_qi_guarded_intent_bridge_receipt_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_guarded_intent_bridge_receipt_summary.json"
    receipt_path = root / "physical_quantum_qi_guarded_intent_bridge_receipt_ledger_receipt.json"
    audit_path = root / "physical_quantum_qi_guarded_intent_bridge_receipt_ledger_audit.jsonl"

    if ctx.get("physical_quantum_qi_guarded_intent_bridge_receipt_ledger_enabled") is not True:
        blockers.append("physical_quantum_qi_guarded_intent_bridge_receipt_ledger_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_guarded_intent_bridge_receipt_ledger") is not True:
        blockers.append("apply_physical_quantum_qi_guarded_intent_bridge_receipt_ledger_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_LICENSE_READY":
        blockers.append("physical_quantum_qi_guarded_intent_bridge_receipt_ledger_license_not_ready")
    for name in [
        "bridge_packet_read_allowed",
        "guarded_execution_intent_packet_read_allowed",
        "bridge_state_read_allowed",
        "receipt_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    bridge_packet = _read_json(bridge_packet_path)
    intent_packet = _read_json(intent_packet_path)
    payload, bridge_status, guarded_status, emit_action, count = _validate_bridge_packet(bridge_packet, blockers, warnings)
    _validate_intent_packet(intent_packet, payload, blockers)
    _validate_bridge_state(_read_json(bridge_state_path), payload, intent_packet, blockers)
    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    if not blockers:
        record = _record(payload, intent_packet, _last_digest(ledger_path))
        _append_jsonl(ledger_path, record)
        summary = {
            "version": "physical_quantum_qi_guarded_intent_bridge_receipt_summary_v13_7",
            "bridge_status": bridge_status,
            "guarded_execution_intent_status": guarded_status,
            "guarded_intent_emit_action": emit_action,
            "guarded_execution_intent_count": count,
            "latest_record_digest": record["record_digest"],
            "source_integrated_candidate_to_guarded_intent_bridge_digest": record["source_integrated_candidate_to_guarded_intent_bridge_digest"],
            "source_guarded_execution_intent_packet_digest": record["source_guarded_execution_intent_packet_digest"],
            "boundary": {
                "summary_only": True,
                "guarded_intent_bridge_receipt_only": True,
                "guarded_execution_intent_packet_traceable": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)
        appended = True

    final_status = "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_BLOCKED"
    packet_id = "physical-quantum-qi-guarded-intent-bridge-receipt-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_guarded_intent_bridge_receipt_ledger_v13_7",
        "status": final_status,
        "packet_id": packet_id,
        "bridge_status": bridge_status,
        "guarded_execution_intent_status": guarded_status,
        "guarded_intent_emit_action": emit_action,
        "guarded_execution_intent_count": count,
        "ledger_appended": appended,
        "record_digest": str(record.get("record_digest", "")),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiGuardedIntentBridgeReceiptLedgerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_guarded_intent_bridge_receipt_ledger_v13_7",
        final_status,
        packet_id,
        str(root),
        bridge_status,
        guarded_status,
        emit_action,
        count,
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        appended,
        blockers,
        warnings,
    )
