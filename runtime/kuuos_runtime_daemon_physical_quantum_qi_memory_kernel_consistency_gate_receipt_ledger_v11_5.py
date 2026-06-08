#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


GATE_DECISIONS = {
    "memory_kernel_consistency_admit",
    "memory_kernel_consistency_hold",
    "memory_kernel_consistency_block",
}
REQUIRED_GATE_BOUNDARY_FLAGS = (
    "memory_kernel_consistency_gate_only",
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
    "admissible_set_not_execution_set",
    "gate_does_not_mutate_candidate_set_receipt",
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
class PhysicalQuantumQiMemoryKernelConsistencyGateReceiptLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    consistency_gate_decision: str
    admitted_count: int
    probe_count: int
    blocked_count: int
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


def _validate_weighting(kind: str, weighting: Mapping[str, Any], idx: int, blockers: list[str]) -> None:
    delta = _int(weighting.get("path_weight_delta"))
    probe = weighting.get("probe_potential_required") is True
    barrier = weighting.get("barrier_potential_required") is True
    barrier_blocks = weighting.get("barrier_blocks_ready_weight") is True
    if kind == "admitted_candidates":
        if delta <= 0:
            blockers.append(f"admitted_candidate_{idx}_without_positive_delta")
        if probe or barrier or barrier_blocks:
            blockers.append(f"admitted_candidate_{idx}_with_probe_or_barrier")
    elif kind == "probe_candidates":
        if delta != 0:
            blockers.append(f"probe_candidate_{idx}_with_delta")
        if not probe:
            blockers.append(f"probe_candidate_{idx}_without_probe")
        if barrier or barrier_blocks:
            blockers.append(f"probe_candidate_{idx}_with_barrier")
    else:
        if delta != 0:
            blockers.append(f"blocked_candidate_{idx}_with_delta")
        if probe:
            blockers.append(f"blocked_candidate_{idx}_with_probe")
        if not barrier or not barrier_blocks:
            blockers.append(f"blocked_candidate_{idx}_without_barrier")


def _validate_candidate_class(kind: str, items: list[dict[str, Any]], record_context: Mapping[str, str], blockers: list[str], warnings: list[str]) -> list[dict[str, Any]]:
    expected_gate = {
        "admitted_candidates": "memory_consistent_admit",
        "probe_candidates": "memory_consistent_probe",
        "blocked_candidates": "memory_consistent_block",
    }[kind]
    out: list[dict[str, Any]] = []
    for idx, item in enumerate(items):
        if str(item.get("memory_kernel_consistency_decision", "")) != expected_gate:
            blockers.append(f"{kind}_{idx}_memory_kernel_consistency_decision_mismatch")
        if not item.get("gate_receipt_digest"):
            warnings.append(f"{kind}_{idx}_gate_receipt_digest_missing")
        weighting = dict(_m(item.get("candidate_weighting")))
        _validate_weighting(kind, weighting, idx, blockers)
        item_context = dict(_m(item.get("process_tensor_context")))
        for key, value in record_context.items():
            if not item_context.get(key):
                blockers.append(f"{kind}_{idx}_{key}_missing")
            elif str(item_context.get(key)) != value:
                blockers.append(f"{kind}_{idx}_{key}_mismatch")
        out.append({
            "candidate_id": str(item.get("candidate_id", f"missing-{kind}-{idx}")),
            "gate_receipt_digest": str(item.get("gate_receipt_digest", "")),
            "cycle_gate_decision": str(item.get("cycle_gate_decision", "")),
            "memory_kernel_consistency_decision": str(item.get("memory_kernel_consistency_decision", "")),
            "candidate_weighting": weighting,
            "process_tensor_context": item_context,
        })
    return out


def _validate_gate_packet(packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], dict[str, int], str]:
    if not packet:
        blockers.append("memory_kernel_consistency_gate_packet_missing_or_invalid")
        return {}, {"admitted": 0, "probe": 0, "blocked": 0}, "memory_kernel_consistency_block"
    if packet.get("physical_quantum_qi_memory_kernel_consistency_gate_considered") is not True:
        blockers.append("memory_kernel_consistency_gate_considered_not_true")
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_GATE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"memory_kernel_consistency_gate_boundary_{name}_missing")
    decision = str(packet.get("memory_kernel_consistency_gate_decision", "memory_kernel_consistency_block"))
    if decision not in GATE_DECISIONS:
        blockers.append("memory_kernel_consistency_gate_decision_invalid")
        decision = "memory_kernel_consistency_block"
    counts = dict(_m(packet.get("counts")))
    admitted = _as_list(packet.get("admitted_candidates"))
    probe = _as_list(packet.get("probe_candidates"))
    blocked = _as_list(packet.get("blocked_candidates"))
    if _int(counts.get("admitted")) != len(admitted):
        blockers.append("admitted_count_mismatch")
    if _int(counts.get("probe")) != len(probe):
        blockers.append("probe_count_mismatch")
    if _int(counts.get("blocked")) != len(blocked):
        blockers.append("blocked_count_mismatch")
    if decision == "memory_kernel_consistency_admit" and len(admitted) <= 0:
        blockers.append("admit_decision_without_admitted_candidates")
    if decision == "memory_kernel_consistency_hold" and len(admitted) > 0:
        blockers.append("hold_decision_with_admitted_candidates")
    if decision == "memory_kernel_consistency_hold" and len(probe) <= 0:
        blockers.append("hold_decision_without_probe_candidates")
    if decision == "memory_kernel_consistency_block" and (len(admitted) > 0 or len(probe) > 0):
        blockers.append("block_decision_with_admitted_or_probe_candidates")
    record_context = _validate_context(_m(packet.get("process_tensor_context")), blockers)
    if not packet.get("memory_kernel_consistency_gate_digest"):
        warnings.append("memory_kernel_consistency_gate_digest_missing")
    payload = {
        "source_memory_kernel_consistency_gate_digest": str(packet.get("memory_kernel_consistency_gate_digest", _sha(dict(packet)))),
        "source_process_tensor_candidate_set_receipt_digest": str(_m(packet.get("source_digests")).get("process_tensor_candidate_set_receipt", "")),
        "source_process_tensor_admissible_candidate_set_digest": str(_m(packet.get("source_digests")).get("process_tensor_admissible_candidate_set", "")),
        "process_tensor_context": dict(record_context),
        "admitted_candidates": _validate_candidate_class("admitted_candidates", admitted, record_context, blockers, warnings),
        "probe_candidates": _validate_candidate_class("probe_candidates", probe, record_context, blockers, warnings),
        "blocked_candidates": _validate_candidate_class("blocked_candidates", blocked, record_context, blockers, warnings),
    }
    result_counts = {"admitted": len(admitted), "probe": len(probe), "blocked": len(blocked)}
    return payload, result_counts, decision


def _record(payload: Mapping[str, Any], counts: Mapping[str, int], decision: str, prev_digest: str) -> dict[str, Any]:
    rec = {
        "version": "physical_quantum_qi_memory_kernel_consistency_gate_receipt_record_v11_5",
        "record_type": "physical_quantum_qi_memory_kernel_consistency_gate_receipt",
        "memory_kernel_consistency_gate_decision": decision,
        "counts": dict(counts),
        "admitted_candidates": list(payload.get("admitted_candidates", [])),
        "probe_candidates": list(payload.get("probe_candidates", [])),
        "blocked_candidates": list(payload.get("blocked_candidates", [])),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_memory_kernel_consistency_gate_digest": str(payload.get("source_memory_kernel_consistency_gate_digest", "")),
        "source_process_tensor_candidate_set_receipt_digest": str(payload.get("source_process_tensor_candidate_set_receipt_digest", "")),
        "source_process_tensor_admissible_candidate_set_digest": str(payload.get("source_process_tensor_admissible_candidate_set_digest", "")),
        "prev_record_digest": prev_digest,
        "boundary": {
            "receipt_ledger_only": True,
            "memory_kernel_consistency_gate_receipt_only": True,
            "history_bearing_process_tensor": True,
            "non_markov_context_required": True,
            "multi_time_window_required": True,
            "finite_horizon_only": True,
            "memory_kernel_visible": True,
            "does_not_execute_path": True,
            "does_not_run_runner": True,
            "does_not_start_next_cycle": True,
            "does_not_commit_plan": True,
            "does_not_consume_memory": True,
            "does_not_authorize_execution": True,
            "does_not_select_final_path": True,
            "does_not_promote_truth": True,
            "candidate_weighting_not_truth": True,
            "admissible_set_not_execution_set": True,
            "receipt_does_not_mutate_gate_packet": True,
            "replayable_receipt": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def build_physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger(
    *,
    runtime_context: Mapping[str, Any],
    memory_kernel_consistency_gate_receipt_ledger_license: Mapping[str, Any],
) -> PhysicalQuantumQiMemoryKernelConsistencyGateReceiptLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(memory_kernel_consistency_gate_receipt_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_memory_kernel_consistency_gate_packet.json"
    ledger_path = root / "physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_memory_kernel_consistency_gate_receipt_summary.json"
    receipt_path = root / "physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger_receipt.json"
    audit_path = root / "physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger_audit.jsonl"

    if ctx.get("physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger_enabled") is not True:
        blockers.append("physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger") is not True:
        blockers.append("apply_physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_RECEIPT_LEDGER_LICENSE_READY":
        blockers.append("physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger_license_not_ready")
    for name in [
        "memory_kernel_consistency_gate_packet_read_allowed",
        "receipt_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, counts, decision = _validate_gate_packet(_read_json(packet_path), blockers, warnings)
    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    if not blockers:
        record = _record(payload, counts, decision, _last_digest(ledger_path))
        _append_jsonl(ledger_path, record)
        summary = {
            "version": "physical_quantum_qi_memory_kernel_consistency_gate_receipt_summary_v11_5",
            "memory_kernel_consistency_gate_decision": decision,
            "counts": dict(counts),
            "latest_record_digest": record["record_digest"],
            "source_memory_kernel_consistency_gate_digest": record["source_memory_kernel_consistency_gate_digest"],
            "process_tensor_context": dict(record["process_tensor_context"]),
            "boundary": {
                "summary_only": True,
                "memory_kernel_consistency_gate_receipt_only": True,
                "history_bearing_process_tensor": True,
                "non_markov_context_required": True,
                "does_not_start_next_cycle": True,
                "does_not_authorize_execution": True,
                "does_not_select_final_path": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)
        appended = True

    status = "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_RECEIPT_LEDGER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_RECEIPT_LEDGER_BLOCKED"
    packet_id = "physical-quantum-qi-memory-kernel-consistency-gate-receipt-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger_v11_5",
        "status": status,
        "packet_id": packet_id,
        "memory_kernel_consistency_gate_decision": decision,
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
    return PhysicalQuantumQiMemoryKernelConsistencyGateReceiptLedgerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger_v11_5",
        status,
        packet_id,
        str(root),
        decision,
        _int(counts.get("admitted")),
        _int(counts.get("probe")),
        _int(counts.get("blocked")),
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        appended,
        blockers,
        warnings,
    )
