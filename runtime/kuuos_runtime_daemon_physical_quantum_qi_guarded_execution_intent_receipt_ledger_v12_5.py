#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


INTENT_STATUSES = {
    "guarded_execution_intent_ready",
    "guarded_execution_intent_hold",
    "guarded_execution_intent_block",
}
EXPECTED_ENVELOPE_STATUS = {
    "guarded_execution_intent_ready": "transition_candidate_envelope_ready",
    "guarded_execution_intent_hold": "transition_candidate_envelope_hold",
    "guarded_execution_intent_block": "transition_candidate_envelope_block",
}
EXPECTED_PRECHECK = {
    "guarded_execution_intent_ready": "transition_precheck_admit_candidate",
    "guarded_execution_intent_hold": "transition_precheck_hold_candidate",
    "guarded_execution_intent_block": "transition_precheck_block_candidate",
}
REQUIRED_PACKET_BOUNDARY_FLAGS = (
    "guarded_execution_intent_only",
    "execution_layer_entrypoint",
    "no_dry_run_required",
    "transition_candidate_envelope_required",
    "history_bearing_process_tensor",
    "non_markov_context_required",
    "multi_time_window_required",
    "finite_horizon_only",
    "memory_kernel_visible",
    "requires_guarded_execution_license",
    "intent_not_world_mutation",
    "does_not_start_next_cycle",
    "does_not_mutate_external_state",
    "does_not_commit_plan",
    "does_not_consume_memory",
    "does_not_promote_truth",
    "candidate_weighting_not_truth",
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
class PhysicalQuantumQiGuardedExecutionIntentReceiptLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    execution_intent_status: str
    intent_count: int
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
        blockers.append(f"guarded_execution_intent_{idx}_without_positive_delta")
    if probe or barrier or barrier_blocks:
        blockers.append(f"guarded_execution_intent_{idx}_with_probe_or_barrier")


def _validate_intent(intent: Mapping[str, Any], idx: int, context: Mapping[str, str], blockers: list[str]) -> dict[str, Any]:
    boundary = _m(intent.get("boundary"))
    for name in REQUIRED_INTENT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"guarded_execution_intent_{idx}_boundary_{name}_missing")
    if intent.get("intent_type") != "physical_quantum_qi_guarded_execution_intent":
        blockers.append(f"guarded_execution_intent_{idx}_type_invalid")
    if _int(intent.get("intent_index")) != idx:
        blockers.append(f"guarded_execution_intent_{idx}_index_mismatch")
    if intent.get("transition_precheck_decision") != "transition_precheck_admit_candidate":
        blockers.append(f"guarded_execution_intent_{idx}_precheck_decision_invalid")
    if intent.get("corridor_stability_gate_decision") != "corridor_stability_admit":
        blockers.append(f"guarded_execution_intent_{idx}_stability_decision_invalid")
    weighting = dict(_m(intent.get("candidate_weighting")))
    _validate_weighting(weighting, idx, blockers)
    item_context = dict(_m(intent.get("process_tensor_context")))
    for key, value in context.items():
        if not item_context.get(key):
            blockers.append(f"guarded_execution_intent_{idx}_{key}_missing")
        elif str(item_context.get(key)) != value:
            blockers.append(f"guarded_execution_intent_{idx}_{key}_mismatch")
    return {
        "intent_type": str(intent.get("intent_type", "")),
        "intent_index": idx,
        "candidate_id": str(intent.get("candidate_id", "")),
        "transition_precheck_decision": str(intent.get("transition_precheck_decision", "")),
        "corridor_stability_gate_decision": str(intent.get("corridor_stability_gate_decision", "")),
        "candidate_weighting": weighting,
        "process_tensor_context": item_context,
        "source_transition_candidate_envelope_digest": str(intent.get("source_transition_candidate_envelope_digest", "")),
        "guarded_execution_intent_digest": str(intent.get("guarded_execution_intent_digest", _sha(dict(intent)))),
    }


def _validate_packet(packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], str]:
    if not packet:
        blockers.append("guarded_execution_intent_packet_missing_or_invalid")
        return {}, "guarded_execution_intent_block"
    if packet.get("physical_quantum_qi_guarded_execution_intent_considered") is not True:
        blockers.append("guarded_execution_intent_considered_not_true")
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_PACKET_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"guarded_execution_intent_boundary_{name}_missing")
    status = str(packet.get("execution_intent_status", "guarded_execution_intent_block"))
    if status not in INTENT_STATUSES:
        blockers.append("guarded_execution_intent_status_invalid")
        status = "guarded_execution_intent_block"
    envelope_status = str(packet.get("envelope_status", "transition_candidate_envelope_block"))
    if envelope_status != EXPECTED_ENVELOPE_STATUS[status]:
        blockers.append("guarded_execution_intent_envelope_status_mismatch")
    precheck = str(packet.get("transition_precheck_decision", "transition_precheck_block_candidate"))
    if precheck != EXPECTED_PRECHECK[status]:
        blockers.append("guarded_execution_intent_precheck_decision_mismatch")
    context = _validate_context(_m(packet.get("process_tensor_context")), blockers)
    intents_raw = _as_list(packet.get("guarded_execution_intents"))
    intent_count = _int(packet.get("intent_count"))
    envelope_count = _int(packet.get("envelope_count"))
    if intent_count != len(intents_raw):
        blockers.append("guarded_execution_intent_count_mismatch")
    if status == "guarded_execution_intent_ready":
        if intent_count <= 0 or envelope_count <= 0:
            blockers.append("guarded_execution_intent_ready_without_intents")
    elif intent_count != 0:
        blockers.append("guarded_execution_intent_hold_or_block_with_intents")
    clean_intents = [_validate_intent(item, idx, context, blockers) for idx, item in enumerate(intents_raw)]
    if not packet.get("guarded_execution_intent_packet_digest"):
        warnings.append("guarded_execution_intent_packet_digest_missing")
    payload = {
        "execution_intent_status": status,
        "envelope_status": envelope_status,
        "transition_precheck_decision": precheck,
        "intent_count": len(clean_intents),
        "envelope_count": envelope_count,
        "guarded_execution_intents": clean_intents,
        "process_tensor_context": dict(context),
        "source_guarded_execution_intent_packet_digest": str(packet.get("guarded_execution_intent_packet_digest", _sha(dict(packet)))),
        "source_transition_candidate_envelope_receipt_digest": str(_m(packet.get("source_digests")).get("transition_candidate_envelope_receipt", "")),
        "source_transition_candidate_envelope_packet_digest": str(_m(packet.get("source_digests")).get("transition_candidate_envelope_packet", "")),
    }
    return payload, status


def _record(payload: Mapping[str, Any], status: str, prev_digest: str) -> dict[str, Any]:
    rec = {
        "version": "physical_quantum_qi_guarded_execution_intent_receipt_record_v12_5",
        "record_type": "physical_quantum_qi_guarded_execution_intent_receipt",
        "execution_intent_status": status,
        "envelope_status": str(payload.get("envelope_status", "")),
        "transition_precheck_decision": str(payload.get("transition_precheck_decision", "")),
        "intent_count": _int(payload.get("intent_count")),
        "envelope_count": _int(payload.get("envelope_count")),
        "guarded_execution_intents": list(payload.get("guarded_execution_intents", [])),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_guarded_execution_intent_packet_digest": str(payload.get("source_guarded_execution_intent_packet_digest", "")),
        "source_transition_candidate_envelope_receipt_digest": str(payload.get("source_transition_candidate_envelope_receipt_digest", "")),
        "source_transition_candidate_envelope_packet_digest": str(payload.get("source_transition_candidate_envelope_packet_digest", "")),
        "prev_record_digest": prev_digest,
        "boundary": {
            "receipt_ledger_only": True,
            "guarded_execution_intent_receipt_only": True,
            "execution_layer_entrypoint": True,
            "no_dry_run_required": True,
            "requires_guarded_execution_license": True,
            "intent_not_world_mutation": True,
            "does_not_start_next_cycle": True,
            "does_not_mutate_external_state": True,
            "does_not_commit_plan": True,
            "does_not_consume_memory": True,
            "does_not_promote_truth": True,
            "receipt_does_not_mutate_intent_packet": True,
            "replayable_receipt": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def build_physical_quantum_qi_guarded_execution_intent_receipt_ledger(
    *,
    runtime_context: Mapping[str, Any],
    guarded_execution_intent_receipt_ledger_license: Mapping[str, Any],
) -> PhysicalQuantumQiGuardedExecutionIntentReceiptLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(guarded_execution_intent_receipt_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_guarded_execution_intent_packet.json"
    ledger_path = root / "physical_quantum_qi_guarded_execution_intent_receipt_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_guarded_execution_intent_receipt_summary.json"
    receipt_path = root / "physical_quantum_qi_guarded_execution_intent_receipt_ledger_receipt.json"
    audit_path = root / "physical_quantum_qi_guarded_execution_intent_receipt_ledger_audit.jsonl"

    if ctx.get("physical_quantum_qi_guarded_execution_intent_receipt_ledger_enabled") is not True:
        blockers.append("physical_quantum_qi_guarded_execution_intent_receipt_ledger_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_guarded_execution_intent_receipt_ledger") is not True:
        blockers.append("apply_physical_quantum_qi_guarded_execution_intent_receipt_ledger_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_LICENSE_READY":
        blockers.append("physical_quantum_qi_guarded_execution_intent_receipt_ledger_license_not_ready")
    for name in [
        "guarded_execution_intent_packet_read_allowed",
        "receipt_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, status_value = _validate_packet(_read_json(packet_path), blockers, warnings)
    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    if not blockers:
        record = _record(payload, status_value, _last_digest(ledger_path))
        _append_jsonl(ledger_path, record)
        summary = {
            "version": "physical_quantum_qi_guarded_execution_intent_receipt_summary_v12_5",
            "execution_intent_status": status_value,
            "intent_count": record["intent_count"],
            "latest_record_digest": record["record_digest"],
            "source_guarded_execution_intent_packet_digest": record["source_guarded_execution_intent_packet_digest"],
            "process_tensor_context": dict(record["process_tensor_context"]),
            "boundary": {
                "summary_only": True,
                "guarded_execution_intent_receipt_only": True,
                "execution_layer_entrypoint": True,
                "no_dry_run_required": True,
                "does_not_start_next_cycle": True,
                "does_not_mutate_external_state": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)
        appended = True

    status = "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_BLOCKED"
    packet_id = "physical-quantum-qi-guarded-execution-intent-receipt-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_guarded_execution_intent_receipt_ledger_v12_5",
        "status": status,
        "packet_id": packet_id,
        "execution_intent_status": status_value,
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
    return PhysicalQuantumQiGuardedExecutionIntentReceiptLedgerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_guarded_execution_intent_receipt_ledger_v12_5",
        status,
        packet_id,
        str(root),
        status_value,
        _int(record.get("intent_count")) if record else 0,
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        appended,
        blockers,
        warnings,
    )
