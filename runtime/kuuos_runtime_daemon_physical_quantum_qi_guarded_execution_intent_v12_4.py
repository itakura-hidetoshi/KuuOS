#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ENVELOPE_TO_INTENT = {
    "transition_candidate_envelope_ready": "guarded_execution_intent_ready",
    "transition_candidate_envelope_hold": "guarded_execution_intent_hold",
    "transition_candidate_envelope_block": "guarded_execution_intent_block",
}
EXPECTED_PRECHECK = {
    "transition_candidate_envelope_ready": "transition_precheck_admit_candidate",
    "transition_candidate_envelope_hold": "transition_precheck_hold_candidate",
    "transition_candidate_envelope_block": "transition_precheck_block_candidate",
}
REQUIRED_RECEIPT_BOUNDARY_FLAGS = (
    "receipt_ledger_only",
    "transition_candidate_envelope_receipt_only",
    "envelope_receipt_only",
    "transition_candidate_envelope_only",
    "envelope_build_only",
    "history_bearing_process_tensor",
    "non_markov_context_required",
    "multi_time_window_required",
    "finite_horizon_only",
    "memory_kernel_visible",
    "does_not_execute_path",
    "does_not_run_runner",
    "does_not_start_next_cycle",
    "does_not_commit_plan",
    "does_not_consume_memory",
    "does_not_authorize_execution",
    "does_not_select_final_path",
    "does_not_promote_truth",
    "candidate_weighting_not_truth",
    "envelope_not_transition_start",
    "receipt_does_not_mutate_envelope_packet",
    "replayable_receipt",
    "fail_closed_on_boundary_loss",
)
REQUIRED_ENVELOPE_BOUNDARY_FLAGS = (
    "transition_candidate_envelope_only",
    "envelope_build_only",
    "does_not_start_next_cycle",
    "does_not_authorize_execution",
    "does_not_select_final_path",
    "does_not_execute_path",
)
REQUIRED_CONTEXT_KEYS = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)


@dataclass(frozen=True)
class PhysicalQuantumQiGuardedExecutionIntentResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    execution_intent_status: str
    envelope_status: str
    transition_precheck_decision: str
    intent_count: int
    envelope_count: int
    intent_packet_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    intent_packet_written: bool
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
        blockers.append("transition_candidate_envelope_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("transition_candidate_envelope_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("transition_candidate_envelope_receipt_ledger_latest_line_invalid")
        return {}
    return value if isinstance(value, dict) else {}


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


def _validate_weighting(weighting: Mapping[str, Any], idx: int, blockers: list[str]) -> None:
    delta = _int(weighting.get("path_weight_delta"))
    probe = weighting.get("probe_potential_required") is True
    barrier = weighting.get("barrier_potential_required") is True
    barrier_blocks = weighting.get("barrier_blocks_ready_weight") is True
    if delta <= 0:
        blockers.append(f"execution_intent_envelope_{idx}_without_positive_delta")
    if probe or barrier or barrier_blocks:
        blockers.append(f"execution_intent_envelope_{idx}_with_probe_or_barrier")


def _validate_envelope(envelope: Mapping[str, Any], idx: int, context: Mapping[str, str], blockers: list[str]) -> dict[str, Any]:
    boundary = _m(envelope.get("boundary"))
    for name in REQUIRED_ENVELOPE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"transition_candidate_envelope_{idx}_boundary_{name}_missing")
    if envelope.get("envelope_type") != "physical_quantum_qi_transition_candidate_envelope":
        blockers.append(f"transition_candidate_envelope_{idx}_type_invalid")
    if envelope.get("transition_precheck_decision") != "transition_precheck_admit_candidate":
        blockers.append(f"transition_candidate_envelope_{idx}_precheck_decision_invalid")
    if envelope.get("corridor_stability_gate_decision") != "corridor_stability_admit":
        blockers.append(f"transition_candidate_envelope_{idx}_stability_decision_invalid")
    if envelope.get("corridor_lane") != "admit_lane":
        blockers.append(f"transition_candidate_envelope_{idx}_lane_not_admit")
    if _int(envelope.get("corridor_rank")) != idx:
        blockers.append(f"transition_candidate_envelope_{idx}_rank_mismatch")
    weighting = dict(_m(envelope.get("candidate_weighting")))
    _validate_weighting(weighting, idx, blockers)
    env_context = dict(_m(envelope.get("process_tensor_context")))
    for key, value in context.items():
        if not env_context.get(key):
            blockers.append(f"transition_candidate_envelope_{idx}_{key}_missing")
        elif str(env_context.get(key)) != value:
            blockers.append(f"transition_candidate_envelope_{idx}_{key}_mismatch")
    return {
        "candidate_id": str(envelope.get("candidate_id", f"missing-envelope-{idx}")),
        "corridor_lane": str(envelope.get("corridor_lane", "")),
        "corridor_rank": _int(envelope.get("corridor_rank")),
        "transition_precheck_decision": str(envelope.get("transition_precheck_decision", "")),
        "corridor_stability_gate_decision": str(envelope.get("corridor_stability_gate_decision", "")),
        "candidate_weighting": weighting,
        "process_tensor_context": env_context,
        "source_transition_candidate_envelope_digest": str(envelope.get("transition_candidate_envelope_digest", _sha(dict(envelope)))),
    }


def _validate_record(record: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], str, str]:
    if not record:
        return {}, "transition_candidate_envelope_block", "transition_precheck_block_candidate"
    if record.get("record_type") != "physical_quantum_qi_transition_candidate_envelope_receipt":
        blockers.append("transition_candidate_envelope_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"transition_candidate_envelope_receipt_boundary_{name}_missing")
    envelope_status = str(record.get("envelope_status", "transition_candidate_envelope_block"))
    if envelope_status not in ENVELOPE_TO_INTENT:
        blockers.append("transition_candidate_envelope_status_invalid")
        envelope_status = "transition_candidate_envelope_block"
    precheck_decision = str(record.get("transition_precheck_decision", "transition_precheck_block_candidate"))
    if precheck_decision != EXPECTED_PRECHECK[envelope_status]:
        blockers.append("transition_candidate_envelope_precheck_decision_mismatch")
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    envelopes_raw = _as_list(record.get("transition_candidate_envelopes"))
    envelope_count = _int(record.get("envelope_count"))
    if envelope_count != len(envelopes_raw):
        blockers.append("transition_candidate_envelope_count_mismatch")
    if envelope_status == "transition_candidate_envelope_ready" and envelope_count <= 0:
        blockers.append("ready_envelope_without_envelopes")
    if envelope_status != "transition_candidate_envelope_ready" and envelope_count != 0:
        blockers.append("hold_or_block_envelope_count_not_zero")
    clean_envelopes = [_validate_envelope(item, idx, context, blockers) for idx, item in enumerate(envelopes_raw)]
    payload = {
        "envelope_status": envelope_status,
        "transition_precheck_decision": precheck_decision,
        "execution_intent_status": ENVELOPE_TO_INTENT[envelope_status],
        "transition_candidate_envelopes": clean_envelopes,
        "process_tensor_context": dict(context),
        "source_transition_candidate_envelope_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_transition_candidate_envelope_packet_digest": str(record.get("source_transition_candidate_envelope_packet_digest", "")),
        "source_stable_corridor_transition_precheck_receipt_digest": str(record.get("source_stable_corridor_transition_precheck_receipt_digest", "")),
    }
    if not payload["source_transition_candidate_envelope_packet_digest"]:
        warnings.append("source_transition_candidate_envelope_packet_digest_missing")
    return payload, envelope_status, precheck_decision


def _intents(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    if payload.get("execution_intent_status") != "guarded_execution_intent_ready":
        return []
    out = []
    for idx, envelope in enumerate(payload.get("transition_candidate_envelopes", [])):
        intent = {
            "intent_type": "physical_quantum_qi_guarded_execution_intent",
            "intent_index": idx,
            "candidate_id": envelope.get("candidate_id"),
            "transition_precheck_decision": envelope.get("transition_precheck_decision"),
            "corridor_stability_gate_decision": envelope.get("corridor_stability_gate_decision"),
            "candidate_weighting": dict(_m(envelope.get("candidate_weighting"))),
            "process_tensor_context": dict(_m(envelope.get("process_tensor_context"))),
            "source_transition_candidate_envelope_digest": envelope.get("source_transition_candidate_envelope_digest"),
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
        out.append(intent)
    return out


def _packet(payload: Mapping[str, Any], envelope_status: str, precheck_decision: str) -> dict[str, Any]:
    intents = _intents(payload)
    packet = {
        "version": "physical_quantum_qi_guarded_execution_intent_packet_v12_4",
        "physical_quantum_qi_guarded_execution_intent_considered": True,
        "execution_intent_status": str(payload.get("execution_intent_status", "guarded_execution_intent_block")),
        "envelope_status": envelope_status,
        "transition_precheck_decision": precheck_decision,
        "intent_count": len(intents),
        "envelope_count": len(payload.get("transition_candidate_envelopes", [])),
        "guarded_execution_intents": intents,
        "transition_candidate_envelopes": list(payload.get("transition_candidate_envelopes", [])),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_digests": {
            "transition_candidate_envelope_receipt": str(payload.get("source_transition_candidate_envelope_receipt_digest", "")),
            "transition_candidate_envelope_packet": str(payload.get("source_transition_candidate_envelope_packet_digest", "")),
            "stable_corridor_transition_precheck_receipt": str(payload.get("source_stable_corridor_transition_precheck_receipt_digest", "")),
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
        "epoch": int(time.time()),
    }
    packet["guarded_execution_intent_packet_digest"] = _sha(packet)
    return packet


def build_physical_quantum_qi_guarded_execution_intent(
    *,
    runtime_context: Mapping[str, Any],
    guarded_execution_intent_license: Mapping[str, Any],
) -> PhysicalQuantumQiGuardedExecutionIntentResult:
    ctx = _m(runtime_context)
    lic = _m(guarded_execution_intent_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ledger_path = root / "physical_quantum_qi_transition_candidate_envelope_receipt_ledger.jsonl"
    intent_packet_path = root / "physical_quantum_qi_guarded_execution_intent_packet.json"
    summary_path = root / "physical_quantum_qi_guarded_execution_intent_summary.json"
    receipt_path = root / "physical_quantum_qi_guarded_execution_intent_receipt.json"
    audit_path = root / "physical_quantum_qi_guarded_execution_intent_audit.jsonl"

    if ctx.get("physical_quantum_qi_guarded_execution_intent_enabled") is not True:
        blockers.append("physical_quantum_qi_guarded_execution_intent_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_guarded_execution_intent") is not True:
        blockers.append("apply_physical_quantum_qi_guarded_execution_intent_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_LICENSE_READY":
        blockers.append("physical_quantum_qi_guarded_execution_intent_license_not_ready")
    for name in [
        "transition_candidate_envelope_receipt_ledger_read_allowed",
        "guarded_execution_intent_packet_write_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, envelope_status, precheck_decision = _validate_record(_latest_jsonl(ledger_path, blockers), blockers, warnings)
    packet: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _packet(payload, envelope_status, precheck_decision)
        summary = {
            "version": "physical_quantum_qi_guarded_execution_intent_summary_v12_4",
            "execution_intent_status": packet["execution_intent_status"],
            "envelope_status": envelope_status,
            "transition_precheck_decision": precheck_decision,
            "intent_count": packet["intent_count"],
            "envelope_count": packet["envelope_count"],
            "guarded_execution_intent_packet_digest": packet["guarded_execution_intent_packet_digest"],
            "process_tensor_context": dict(packet["process_tensor_context"]),
            "boundary": {
                "summary_only": True,
                "guarded_execution_intent_only": True,
                "execution_layer_entrypoint": True,
                "no_dry_run_required": True,
                "does_not_start_next_cycle": True,
                "does_not_mutate_external_state": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(intent_packet_path, packet)
        _write_json(summary_path, summary)
        written = True

    status = "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_READY" if not blockers else "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_BLOCKED"
    packet_id = "physical-quantum-qi-guarded-execution-intent-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_guarded_execution_intent_v12_4",
        "status": status,
        "packet_id": packet_id,
        "execution_intent_status": str(packet.get("execution_intent_status", "guarded_execution_intent_block")),
        "intent_packet_written": written,
        "guarded_execution_intent_packet_digest": _sha(packet),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiGuardedExecutionIntentResult(
        "kuuos_runtime_daemon_physical_quantum_qi_guarded_execution_intent_v12_4",
        status,
        packet_id,
        str(root),
        str(packet.get("execution_intent_status", "guarded_execution_intent_block")),
        envelope_status,
        precheck_decision,
        _int(packet.get("intent_count")),
        _int(packet.get("envelope_count")),
        str(intent_packet_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
