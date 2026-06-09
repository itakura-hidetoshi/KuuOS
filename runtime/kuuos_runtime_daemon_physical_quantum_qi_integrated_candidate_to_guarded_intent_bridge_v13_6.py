#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


BRIDGE = {
    "cycle_gate_reentry_integration_admit": (
        "integrated_candidate_to_guarded_intent_ready",
        "guarded_execution_intent_ready",
        "emit_guarded_ready_intent",
    ),
    "cycle_gate_reentry_integration_hold": (
        "integrated_candidate_to_guarded_intent_hold",
        "guarded_execution_intent_hold",
        "emit_guarded_hold_intent",
    ),
    "cycle_gate_reentry_integration_block": (
        "integrated_candidate_to_guarded_intent_block",
        "guarded_execution_intent_block",
        "emit_guarded_block_intent",
    ),
}
EXPECTED_GATE = {
    "cycle_gate_reentry_integration_admit": "integrated_cycle_gate_admit",
    "cycle_gate_reentry_integration_hold": "integrated_cycle_gate_hold",
    "cycle_gate_reentry_integration_block": "integrated_cycle_gate_block",
}
EXPECTED_SET = {
    "cycle_gate_reentry_integration_admit": "integrated_admissible_candidate_set_admit",
    "cycle_gate_reentry_integration_hold": "integrated_admissible_candidate_set_probe",
    "cycle_gate_reentry_integration_block": "integrated_admissible_candidate_set_block",
}
REQUIRED_RECEIPT_BOUNDARY_FLAGS = (
    "receipt_ledger_only",
    "cycle_gate_reentry_integration_receipt_only",
    "integrated_cycle_gate_state_traceable",
    "integrated_admissible_candidate_set_traceable",
    "uses_process_tensor_feedback",
    "non_markov_feedback_preserved",
    "history_window_feedback_preserved",
    "memory_kernel_feedback_preserved",
    "external_backaction_visible",
    "candidate_weighting_not_truth",
    "integration_not_direct_execution",
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
class PhysicalQuantumQiIntegratedCandidateToGuardedIntentBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_status: str
    guarded_execution_intent_status: str
    guarded_intent_emit_action: str
    guarded_execution_intent_count: int
    bridge_packet_written: bool
    guarded_execution_intent_packet_written: bool
    bridge_state_written: bool
    bridge_ledger_appended: bool
    bridge_packet_path: str
    guarded_execution_intent_packet_path: str
    bridge_state_path: str
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
        blockers.append("cycle_gate_reentry_integration_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("cycle_gate_reentry_integration_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("cycle_gate_reentry_integration_receipt_ledger_latest_line_invalid")
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
    if status == "cycle_gate_reentry_integration_admit":
        if norm["path_weight_delta"] <= 0:
            blockers.append("guarded_intent_admit_without_positive_path_weight_delta")
        if norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("guarded_intent_admit_with_probe_or_barrier")
        if norm["memory_feedback_weight"] <= 0 or norm["external_backaction_weight"] <= 0 or norm["next_cycle_amplitude_delta"] <= 0:
            blockers.append("guarded_intent_admit_missing_process_tensor_effect_weight")
    elif status == "cycle_gate_reentry_integration_hold":
        if norm["path_weight_delta"] != 0:
            blockers.append("guarded_intent_hold_with_path_weight_delta")
        if not norm["probe_potential_required"]:
            blockers.append("guarded_intent_hold_without_probe_potential")
        if norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("guarded_intent_hold_with_barrier")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("guarded_intent_hold_with_effect_weight")
    elif status == "cycle_gate_reentry_integration_block":
        if norm["path_weight_delta"] != 0:
            blockers.append("guarded_intent_block_with_path_weight_delta")
        if norm["probe_potential_required"]:
            blockers.append("guarded_intent_block_with_probe")
        if not norm["barrier_potential_required"] or not norm["barrier_blocks_ready_weight"]:
            blockers.append("guarded_intent_block_without_blocking_barrier")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("guarded_intent_block_with_effect_weight")
    return norm


def _validate_receipt(record: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], str, str, str, int]:
    if not record:
        return {}, "cycle_gate_reentry_integration_block", "guarded_execution_intent_block", "emit_guarded_block_intent", 0
    if record.get("record_type") != "physical_quantum_qi_cycle_gate_reentry_integration_receipt":
        blockers.append("cycle_gate_reentry_integration_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"cycle_gate_reentry_integration_receipt_boundary_{name}_missing")
    integration_status = str(record.get("integration_status", "cycle_gate_reentry_integration_block"))
    if integration_status not in BRIDGE:
        blockers.append("cycle_gate_reentry_integration_status_invalid")
        integration_status = "cycle_gate_reentry_integration_block"
    bridge_status, guarded_status, emit_action = BRIDGE[integration_status]
    gate_status = str(record.get("integrated_cycle_gate_status", ""))
    set_status = str(record.get("integrated_admissible_candidate_set_status", ""))
    if gate_status != EXPECTED_GATE[integration_status]:
        blockers.append("cycle_gate_reentry_integration_receipt_gate_status_mismatch")
    if set_status != EXPECTED_SET[integration_status]:
        blockers.append("cycle_gate_reentry_integration_receipt_candidate_set_status_mismatch")
    candidate_count = _int(record.get("admissible_candidate_count"))
    if integration_status in {"cycle_gate_reentry_integration_admit", "cycle_gate_reentry_integration_hold"} and candidate_count <= 0:
        blockers.append("guarded_intent_bridge_requires_candidate_for_admit_or_hold")
    if integration_status == "cycle_gate_reentry_integration_block" and candidate_count != 0:
        blockers.append("guarded_intent_bridge_block_with_admissible_candidates")
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(integration_status, _m(record.get("candidate_weighting")), blockers)
    candidates = record.get("integrated_candidates", [])
    if not isinstance(candidates, list):
        blockers.append("integrated_candidates_not_list")
        candidates = []
    payload = {
        "integration_status": integration_status,
        "bridge_status": bridge_status,
        "guarded_execution_intent_status": guarded_status,
        "guarded_intent_emit_action": emit_action,
        "integrated_cycle_gate_status": gate_status,
        "integrated_admissible_candidate_set_status": set_status,
        "admissible_candidate_count": candidate_count,
        "candidate_weighting": weighting,
        "integrated_candidates": candidates,
        "process_tensor_context": context,
        "source_cycle_gate_reentry_integration_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_cycle_gate_reentry_integration_digest": str(record.get("source_cycle_gate_reentry_integration_digest", "")),
    }
    return payload, integration_status, guarded_status, emit_action, candidate_count


def _guarded_intents(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    status = str(payload.get("guarded_execution_intent_status", ""))
    if status != "guarded_execution_intent_ready":
        return []
    context = dict(_m(payload.get("process_tensor_context")))
    weighting = dict(_m(payload.get("candidate_weighting")))
    candidates = payload.get("integrated_candidates", [])
    source_digest = str(payload.get("source_cycle_gate_reentry_integration_receipt_digest", ""))
    intents: list[dict[str, Any]] = []
    for idx, candidate in enumerate(candidates if isinstance(candidates, list) else []):
        c = dict(_m(candidate))
        intent = {
            "intent_index": idx,
            "intent_type": "physical_quantum_qi_guarded_execution_intent",
            "candidate_id": str(c.get("candidate_id", f"integrated-candidate-{idx}")),
            "transition_precheck_decision": "transition_precheck_admit_candidate",
            "corridor_stability_gate_decision": "corridor_stability_admit",
            "candidate_weighting": weighting,
            "process_tensor_context": context,
            "source_integrated_candidate_digest": str(c.get("candidate_digest", _sha(c))),
            "source_cycle_gate_reentry_integration_receipt_digest": source_digest,
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
        intent["guarded_execution_intent_digest"] = _sha(intent)
        intents.append(intent)
    return intents


def build_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge(
    *,
    runtime_context: Mapping[str, Any],
    integrated_candidate_to_guarded_intent_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiIntegratedCandidateToGuardedIntentBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(integrated_candidate_to_guarded_intent_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_ledger_path = root / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl"
    bridge_packet_path = root / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_packet.json"
    intent_packet_path = root / "physical_quantum_qi_guarded_execution_intent_packet.json"
    bridge_state_path = root / "physical_quantum_qi_guarded_execution_intent_bridge_state.json"
    bridge_ledger_path = root / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_summary.json"
    receipt_path = root / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_receipt.json"
    audit_path = root / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_license_not_ready")
    for name in [
        "cycle_gate_reentry_integration_receipt_ledger_read_allowed",
        "bridge_packet_write_allowed",
        "guarded_execution_intent_packet_write_allowed",
        "bridge_state_write_allowed",
        "bridge_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, integration_status, guarded_status, emit_action, candidate_count = _validate_receipt(_latest_jsonl(receipt_ledger_path, blockers), blockers)
    bridge_status = str(payload.get("bridge_status", "integrated_candidate_to_guarded_intent_block"))
    intents = _guarded_intents(payload) if not blockers else []
    if guarded_status == "guarded_execution_intent_ready" and len(intents) != candidate_count:
        blockers.append("guarded_execution_intent_ready_count_mismatch")
    packet_written = intent_written = state_written = ledger_appended = False
    bridge_packet: dict[str, Any] = {}
    if not blockers:
        epoch = int(time.time())
        bridge_packet = {
            "version": "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_packet_v13_6",
            "integrated_candidate_to_guarded_intent_bridge_considered": True,
            "bridge_status": bridge_status,
            "integration_status": integration_status,
            "guarded_execution_intent_status": guarded_status,
            "guarded_intent_emit_action": emit_action,
            "guarded_execution_intent_count": len(intents),
            "candidate_weighting": dict(payload["candidate_weighting"]),
            "guarded_execution_intents": intents,
            "process_tensor_context": dict(payload["process_tensor_context"]),
            "source_digests": {
                "cycle_gate_reentry_integration_receipt": payload["source_cycle_gate_reentry_integration_receipt_digest"],
                "cycle_gate_reentry_integration": payload["source_cycle_gate_reentry_integration_digest"],
            },
            "boundary": {
                "integrated_candidate_to_guarded_intent_bridge_only": True,
                "cycle_gate_reentry_integration_receipt_required": True,
                "emits_guarded_execution_intent_packet": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "external_backaction_visible": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_execution": True,
                "does_not_run_runner": True,
                "does_not_mutate_external_state": True,
                "does_not_start_next_cycle": True,
                "license_gated_bridge": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        bridge_packet["integrated_candidate_to_guarded_intent_bridge_digest"] = _sha(bridge_packet)
        _write_json(bridge_packet_path, bridge_packet)
        packet_written = True
        intent_packet = {
            "version": "physical_quantum_qi_guarded_execution_intent_packet_v13_6",
            "guarded_execution_intent_packet_ready": True,
            "guarded_execution_intent_status": guarded_status,
            "guarded_execution_intent_count": len(intents),
            "guarded_execution_intents": intents,
            "candidate_weighting": dict(payload["candidate_weighting"]),
            "process_tensor_context": dict(payload["process_tensor_context"]),
            "source_integrated_candidate_to_guarded_intent_bridge_digest": bridge_packet["integrated_candidate_to_guarded_intent_bridge_digest"],
            "boundary": {
                "guarded_execution_intent_packet_only": True,
                "from_integrated_candidate_bridge": True,
                "requires_guarded_execution_license": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "does_not_run_runner": True,
                "does_not_mutate_external_state": True,
            },
            "epoch": epoch,
        }
        intent_packet["guarded_execution_intent_packet_digest"] = _sha(intent_packet)
        _write_json(intent_packet_path, intent_packet)
        intent_written = True
        bridge_state = {
            "version": "physical_quantum_qi_guarded_execution_intent_bridge_state_v13_6",
            "guarded_execution_intent_bridge_state_ready": True,
            "bridge_status": bridge_status,
            "guarded_execution_intent_status": guarded_status,
            "guarded_execution_intent_packet_digest": intent_packet["guarded_execution_intent_packet_digest"],
            "source_integrated_candidate_to_guarded_intent_bridge_digest": bridge_packet["integrated_candidate_to_guarded_intent_bridge_digest"],
            "process_tensor_context": dict(payload["process_tensor_context"]),
            "boundary": {
                "guarded_execution_intent_bridge_state_only": True,
                "from_integrated_candidate_bridge": True,
                "can_feed_guarded_execution_intent_receipt_layer": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
            },
            "epoch": epoch,
        }
        bridge_state["guarded_execution_intent_bridge_state_digest"] = _sha(bridge_state)
        _write_json(bridge_state_path, bridge_state)
        state_written = True
        ledger_record = {
            "version": "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_record_v13_6",
            "record_type": "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge",
            "bridge_status": bridge_status,
            "guarded_execution_intent_status": guarded_status,
            "guarded_execution_intent_count": len(intents),
            "source_integrated_candidate_to_guarded_intent_bridge_digest": bridge_packet["integrated_candidate_to_guarded_intent_bridge_digest"],
            "source_guarded_execution_intent_packet_digest": intent_packet["guarded_execution_intent_packet_digest"],
            "source_cycle_gate_reentry_integration_receipt_digest": payload["source_cycle_gate_reentry_integration_receipt_digest"],
            "prev_record_digest": _last_digest(bridge_ledger_path),
            "boundary": {
                "bridge_receipt_only": True,
                "guarded_execution_intent_packet_traceable": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_execution": True,
                "replayable_receipt": True,
            },
            "epoch": epoch,
        }
        ledger_record["record_digest"] = _sha(ledger_record)
        _append_jsonl(bridge_ledger_path, ledger_record)
        ledger_appended = True
        summary = {
            "version": "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_summary_v13_6",
            "bridge_status": bridge_status,
            "guarded_execution_intent_status": guarded_status,
            "guarded_execution_intent_count": len(intents),
            "integrated_candidate_to_guarded_intent_bridge_digest": bridge_packet["integrated_candidate_to_guarded_intent_bridge_digest"],
            "guarded_execution_intent_packet_digest": intent_packet["guarded_execution_intent_packet_digest"],
            "boundary": {
                "summary_only": True,
                "integrated_candidate_to_guarded_intent_bridge_only": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    status = "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_BLOCKED"
    packet_id = "physical-quantum-qi-integrated-candidate-to-guarded-intent-" + _sha({"packet": bridge_packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_v13_6",
        "status": status,
        "packet_id": packet_id,
        "bridge_status": bridge_status,
        "guarded_execution_intent_status": guarded_status,
        "guarded_intent_emit_action": emit_action,
        "guarded_execution_intent_count": len(intents),
        "bridge_packet_written": packet_written,
        "guarded_execution_intent_packet_written": intent_written,
        "bridge_state_written": state_written,
        "bridge_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiIntegratedCandidateToGuardedIntentBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_v13_6",
        status,
        packet_id,
        str(root),
        bridge_status,
        guarded_status,
        emit_action,
        len(intents),
        packet_written,
        intent_written,
        state_written,
        ledger_appended,
        str(bridge_packet_path),
        str(intent_packet_path),
        str(bridge_state_path),
        str(bridge_ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
