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
class PhysicalQuantumQiGuardedTransitionExecutorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    execution_status: str
    intent_count: int
    internal_transition_record_written: bool
    next_cycle_state_updated: bool
    memory_consumption_appended: bool
    external_state_mutation_appended: bool
    execution_record_path: str
    next_cycle_state_path: str
    memory_ledger_path: str
    external_state_ledger_path: str
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
        blockers.append("guarded_execution_intent_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("guarded_execution_intent_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("guarded_execution_intent_receipt_ledger_latest_line_invalid")
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
        blockers.append(f"guarded_transition_executor_intent_{idx}_without_positive_delta")
    if probe or barrier or barrier_blocks:
        blockers.append(f"guarded_transition_executor_intent_{idx}_with_probe_or_barrier")


def _validate_intent(intent: Mapping[str, Any], idx: int, context: Mapping[str, str], blockers: list[str]) -> dict[str, Any]:
    boundary = _m(intent.get("boundary"))
    for name in REQUIRED_INTENT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"guarded_transition_executor_intent_{idx}_boundary_{name}_missing")
    if intent.get("intent_type") != "physical_quantum_qi_guarded_execution_intent":
        blockers.append(f"guarded_transition_executor_intent_{idx}_type_invalid")
    if _int(intent.get("intent_index")) != idx:
        blockers.append(f"guarded_transition_executor_intent_{idx}_index_mismatch")
    if intent.get("transition_precheck_decision") != "transition_precheck_admit_candidate":
        blockers.append(f"guarded_transition_executor_intent_{idx}_precheck_decision_invalid")
    if intent.get("corridor_stability_gate_decision") != "corridor_stability_admit":
        blockers.append(f"guarded_transition_executor_intent_{idx}_stability_decision_invalid")
    weighting = dict(_m(intent.get("candidate_weighting")))
    _validate_weighting(weighting, idx, blockers)
    item_context = dict(_m(intent.get("process_tensor_context")))
    for key, value in context.items():
        if not item_context.get(key):
            blockers.append(f"guarded_transition_executor_intent_{idx}_{key}_missing")
        elif str(item_context.get(key)) != value:
            blockers.append(f"guarded_transition_executor_intent_{idx}_{key}_mismatch")
    return {
        "intent_index": idx,
        "candidate_id": str(intent.get("candidate_id", f"missing-intent-{idx}")),
        "transition_precheck_decision": str(intent.get("transition_precheck_decision", "")),
        "corridor_stability_gate_decision": str(intent.get("corridor_stability_gate_decision", "")),
        "candidate_weighting": weighting,
        "process_tensor_context": item_context,
        "source_guarded_execution_intent_digest": str(intent.get("guarded_execution_intent_digest", _sha(dict(intent)))),
        "source_transition_candidate_envelope_digest": str(intent.get("source_transition_candidate_envelope_digest", "")),
    }


def _validate_receipt(record: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], str]:
    if not record:
        return {}, "guarded_transition_block"
    if record.get("record_type") != "physical_quantum_qi_guarded_execution_intent_receipt":
        blockers.append("guarded_execution_intent_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"guarded_execution_intent_receipt_boundary_{name}_missing")
    intent_status = str(record.get("execution_intent_status", "guarded_execution_intent_block"))
    if intent_status not in EXECUTION_BY_INTENT:
        blockers.append("guarded_execution_intent_status_invalid")
        intent_status = "guarded_execution_intent_block"
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    intents = _as_list(record.get("guarded_execution_intents"))
    intent_count = _int(record.get("intent_count"))
    if intent_count != len(intents):
        blockers.append("guarded_execution_intent_count_mismatch")
    if intent_status == "guarded_execution_intent_ready" and intent_count <= 0:
        blockers.append("guarded_transition_ready_without_intents")
    if intent_status != "guarded_execution_intent_ready" and intent_count != 0:
        blockers.append("guarded_transition_hold_or_block_with_intents")
    clean_intents = [_validate_intent(item, idx, context, blockers) for idx, item in enumerate(intents)]
    payload = {
        "execution_intent_status": intent_status,
        "execution_status": EXECUTION_BY_INTENT[intent_status],
        "intent_count": len(clean_intents),
        "guarded_execution_intents": clean_intents,
        "process_tensor_context": dict(context),
        "source_guarded_execution_intent_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_guarded_execution_intent_packet_digest": str(record.get("source_guarded_execution_intent_packet_digest", "")),
    }
    if not payload["source_guarded_execution_intent_packet_digest"]:
        warnings.append("source_guarded_execution_intent_packet_digest_missing")
    return payload, payload["execution_status"]


def _effects(payload: Mapping[str, Any], execution_status: str) -> dict[str, Any]:
    base = {
        "internal_transition_record": True,
        "next_cycle_state_update": False,
        "memory_consumption": False,
        "external_state_mutation": False,
    }
    if execution_status == "guarded_transition_executed":
        base.update({
            "next_cycle_state_update": True,
            "memory_consumption": True,
            "external_state_mutation": True,
        })
    return base


def build_physical_quantum_qi_guarded_transition_executor(
    *,
    runtime_context: Mapping[str, Any],
    guarded_transition_executor_license: Mapping[str, Any],
) -> PhysicalQuantumQiGuardedTransitionExecutorResult:
    ctx = _m(runtime_context)
    lic = _m(guarded_transition_executor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ledger_path = root / "physical_quantum_qi_guarded_execution_intent_receipt_ledger.jsonl"
    execution_record_path = root / "physical_quantum_qi_guarded_transition_execution_record.json"
    next_cycle_state_path = root / "physical_quantum_qi_next_cycle_state.json"
    memory_ledger_path = root / "physical_quantum_qi_memory_consumption_ledger.jsonl"
    external_ledger_path = root / "physical_quantum_qi_external_state_mutation_ledger.jsonl"
    receipt_path = root / "physical_quantum_qi_guarded_transition_executor_receipt.json"
    audit_path = root / "physical_quantum_qi_guarded_transition_executor_audit.jsonl"

    if ctx.get("physical_quantum_qi_guarded_transition_executor_enabled") is not True:
        blockers.append("physical_quantum_qi_guarded_transition_executor_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_guarded_transition_executor") is not True:
        blockers.append("apply_physical_quantum_qi_guarded_transition_executor_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_LICENSE_READY":
        blockers.append("physical_quantum_qi_guarded_transition_executor_license_not_ready")
    for name in [
        "guarded_execution_intent_receipt_ledger_read_allowed",
        "internal_transition_record_write_allowed",
        "next_cycle_state_write_allowed",
        "memory_consumption_append_allowed",
        "external_state_mutation_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, execution_status = _validate_receipt(_latest_jsonl(ledger_path, blockers), blockers, warnings)
    effects = _effects(payload, execution_status)
    if execution_status == "guarded_transition_executed":
        for required in ["next_cycle_state_write_allowed", "memory_consumption_append_allowed", "external_state_mutation_append_allowed"]:
            if lic.get(required) is not True:
                blockers.append(required.replace("allowed", "not_allowed_for_execution"))

    record: dict[str, Any] = {}
    internal_written = next_updated = memory_appended = external_appended = False
    if not blockers:
        epoch = int(time.time())
        record = {
            "version": "physical_quantum_qi_guarded_transition_execution_record_v12_6",
            "execution_status": execution_status,
            "execution_layer_entrypoint": True,
            "no_dry_run_required": True,
            "effects": effects,
            "intent_count": int(payload.get("intent_count", 0)),
            "guarded_execution_intents": list(payload.get("guarded_execution_intents", [])),
            "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
            "source_guarded_execution_intent_receipt_digest": str(payload.get("source_guarded_execution_intent_receipt_digest", "")),
            "source_guarded_execution_intent_packet_digest": str(payload.get("source_guarded_execution_intent_packet_digest", "")),
            "boundary": {
                "guarded_transition_executor": True,
                "can_update_next_cycle_state": effects["next_cycle_state_update"],
                "can_consume_memory": effects["memory_consumption"],
                "can_mutate_runtime_external_state": effects["external_state_mutation"],
                "runtime_local_external_state_only": True,
                "license_gated_execution": True,
                "no_dry_run_required": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        record["execution_record_digest"] = _sha(record)
        _write_json(execution_record_path, record)
        internal_written = True
        if execution_status == "guarded_transition_executed":
            next_cycle = {
                "version": "physical_quantum_qi_next_cycle_state_v12_6",
                "next_cycle_started": True,
                "source_execution_record_digest": record["execution_record_digest"],
                "process_tensor_context": dict(record["process_tensor_context"]),
                "epoch": epoch,
            }
            next_cycle["next_cycle_state_digest"] = _sha(next_cycle)
            _write_json(next_cycle_state_path, next_cycle)
            next_updated = True
            memory_receipt = {
                "version": "physical_quantum_qi_memory_consumption_receipt_v12_6",
                "memory_consumed": True,
                "consumption_scope": "runtime_local_memory_ledger",
                "source_execution_record_digest": record["execution_record_digest"],
                "intent_count": record["intent_count"],
                "epoch": epoch,
            }
            memory_receipt["memory_consumption_digest"] = _sha(memory_receipt)
            _append_jsonl(memory_ledger_path, memory_receipt)
            memory_appended = True
            external_receipt = {
                "version": "physical_quantum_qi_external_state_mutation_receipt_v12_6",
                "external_state_mutated": True,
                "mutation_scope": "runtime_local_external_state_store",
                "source_execution_record_digest": record["execution_record_digest"],
                "intent_count": record["intent_count"],
                "epoch": epoch,
            }
            external_receipt["external_state_mutation_digest"] = _sha(external_receipt)
            _append_jsonl(external_ledger_path, external_receipt)
            external_appended = True

    status = "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_READY" if not blockers else "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_BLOCKED"
    packet_id = "physical-quantum-qi-guarded-transition-executor-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_guarded_transition_executor_v12_6",
        "status": status,
        "packet_id": packet_id,
        "execution_status": execution_status,
        "internal_transition_record_written": internal_written,
        "next_cycle_state_updated": next_updated,
        "memory_consumption_appended": memory_appended,
        "external_state_mutation_appended": external_appended,
        "execution_record_digest": str(record.get("execution_record_digest", "")),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiGuardedTransitionExecutorResult(
        "kuuos_runtime_daemon_physical_quantum_qi_guarded_transition_executor_v12_6",
        status,
        packet_id,
        str(root),
        execution_status,
        int(payload.get("intent_count", 0)) if payload else 0,
        internal_written,
        next_updated,
        memory_appended,
        external_appended,
        str(execution_record_path),
        str(next_cycle_state_path),
        str(memory_ledger_path),
        str(external_ledger_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
