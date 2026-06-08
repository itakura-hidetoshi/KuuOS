#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


REQUIRED_RECEIPT_BOUNDARY_FLAGS = (
    "receipt_ledger_only",
    "process_tensor_candidate_set_receipt_only",
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
GATE_DECISION_BY_CLASS = {
    "admitted_candidates": "memory_consistent_admit",
    "probe_candidates": "memory_consistent_probe",
    "blocked_candidates": "memory_consistent_block",
}


@dataclass(frozen=True)
class PhysicalQuantumQiMemoryKernelConsistencyGateResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    consistency_gate_decision: str
    admitted_consistent_count: int
    probe_consistent_count: int
    blocked_consistent_count: int
    gate_packet_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    gate_packet_written: bool
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
        blockers.append("process_tensor_candidate_set_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("process_tensor_candidate_set_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("process_tensor_candidate_set_receipt_ledger_latest_line_invalid")
        return {}
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[dict[str, Any]]:
    return [dict(_m(item)) for item in value] if isinstance(value, list) else []


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


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


def _validate_context(record_context: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    ctx = {key: str(record_context.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, value in ctx.items():
        if not value:
            blockers.append(f"record_process_tensor_context_{key}_missing")
    return ctx


def _validate_candidate_class(kind: str, items: list[dict[str, Any]], record_context: Mapping[str, str], blockers: list[str], warnings: list[str]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    expected_decision = {
        "admitted_candidates": "admit_candidate",
        "probe_candidates": "hold_candidate",
        "blocked_candidates": "block_candidate",
    }[kind]
    for idx, item in enumerate(items):
        if str(item.get("cycle_gate_decision", "")) != expected_decision:
            blockers.append(f"{kind}_{idx}_cycle_gate_decision_mismatch")
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
            "memory_kernel_consistency_decision": GATE_DECISION_BY_CLASS[kind],
            "candidate_weighting": weighting,
            "process_tensor_context": item_context,
        })
    return out


def _validate_record(record: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], dict[str, int]]:
    if not record:
        return {}, {"admitted": 0, "probe": 0, "blocked": 0}
    if record.get("record_type") != "physical_quantum_qi_process_tensor_candidate_set_receipt":
        blockers.append("process_tensor_candidate_set_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"candidate_set_receipt_boundary_{name}_missing")
    record_context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    admitted = _as_list(record.get("admitted_candidates"))
    probe = _as_list(record.get("probe_candidates"))
    blocked = _as_list(record.get("blocked_candidates"))
    counts = _m(record.get("counts"))
    if _int(counts.get("admitted")) != len(admitted):
        blockers.append("admitted_count_mismatch")
    if _int(counts.get("probe")) != len(probe):
        blockers.append("probe_count_mismatch")
    if _int(counts.get("blocked")) != len(blocked):
        blockers.append("blocked_count_mismatch")
    if str(record.get("prev_record_digest", "")) == "CORRUPT_PREVIOUS_LEDGER_LINE":
        warnings.append("previous_candidate_set_receipt_digest_corrupt_marker_visible")
    payload = {
        "source_candidate_set_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_candidate_set_digest": str(record.get("source_candidate_set_digest", "")),
        "process_tensor_context": dict(record_context),
        "admitted_candidates": _validate_candidate_class("admitted_candidates", admitted, record_context, blockers, warnings),
        "probe_candidates": _validate_candidate_class("probe_candidates", probe, record_context, blockers, warnings),
        "blocked_candidates": _validate_candidate_class("blocked_candidates", blocked, record_context, blockers, warnings),
    }
    if not payload["source_candidate_set_digest"]:
        warnings.append("source_candidate_set_digest_missing")
    result_counts = {"admitted": len(admitted), "probe": len(probe), "blocked": len(blocked)}
    return payload, result_counts


def _gate_decision(counts: Mapping[str, int]) -> str:
    if _int(counts.get("admitted")) > 0:
        return "memory_kernel_consistency_admit"
    if _int(counts.get("probe")) > 0:
        return "memory_kernel_consistency_hold"
    return "memory_kernel_consistency_block"


def _packet(payload: Mapping[str, Any], counts: Mapping[str, int]) -> dict[str, Any]:
    gate_decision = _gate_decision(counts)
    packet = {
        "version": "physical_quantum_qi_memory_kernel_consistency_gate_packet_v11_4",
        "physical_quantum_qi_memory_kernel_consistency_gate_considered": True,
        "memory_kernel_consistency_gate_decision": gate_decision,
        "counts": dict(counts),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "admitted_candidates": list(payload.get("admitted_candidates", [])),
        "probe_candidates": list(payload.get("probe_candidates", [])),
        "blocked_candidates": list(payload.get("blocked_candidates", [])),
        "source_digests": {
            "process_tensor_candidate_set_receipt": str(payload.get("source_candidate_set_receipt_digest", "")),
            "process_tensor_admissible_candidate_set": str(payload.get("source_candidate_set_digest", "")),
        },
        "boundary": {
            "memory_kernel_consistency_gate_only": True,
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
            "gate_does_not_mutate_candidate_set_receipt": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    packet["memory_kernel_consistency_gate_digest"] = _sha(packet)
    return packet


def build_physical_quantum_qi_memory_kernel_consistency_gate(
    *,
    runtime_context: Mapping[str, Any],
    memory_kernel_consistency_gate_license: Mapping[str, Any],
) -> PhysicalQuantumQiMemoryKernelConsistencyGateResult:
    ctx = _m(runtime_context)
    lic = _m(memory_kernel_consistency_gate_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ledger_path = root / "physical_quantum_qi_process_tensor_candidate_set_receipt_ledger.jsonl"
    gate_packet_path = root / "physical_quantum_qi_memory_kernel_consistency_gate_packet.json"
    summary_path = root / "physical_quantum_qi_memory_kernel_consistency_gate_summary.json"
    receipt_path = root / "physical_quantum_qi_memory_kernel_consistency_gate_receipt.json"
    audit_path = root / "physical_quantum_qi_memory_kernel_consistency_gate_audit.jsonl"

    if ctx.get("physical_quantum_qi_memory_kernel_consistency_gate_enabled") is not True:
        blockers.append("physical_quantum_qi_memory_kernel_consistency_gate_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_memory_kernel_consistency_gate") is not True:
        blockers.append("apply_physical_quantum_qi_memory_kernel_consistency_gate_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_LICENSE_READY":
        blockers.append("physical_quantum_qi_memory_kernel_consistency_gate_license_not_ready")
    for name in [
        "candidate_set_receipt_ledger_read_allowed",
        "memory_kernel_consistency_gate_packet_write_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, counts = _validate_record(_latest_jsonl(ledger_path, blockers), blockers, warnings)
    packet: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _packet(payload, counts)
        summary = {
            "version": "physical_quantum_qi_memory_kernel_consistency_gate_summary_v11_4",
            "memory_kernel_consistency_gate_decision": packet["memory_kernel_consistency_gate_decision"],
            "counts": dict(counts),
            "process_tensor_context": dict(packet["process_tensor_context"]),
            "memory_kernel_consistency_gate_digest": packet["memory_kernel_consistency_gate_digest"],
            "boundary": {
                "summary_only": True,
                "memory_kernel_consistency_gate_only": True,
                "does_not_start_next_cycle": True,
                "does_not_authorize_execution": True,
                "does_not_select_final_path": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(gate_packet_path, packet)
        _write_json(summary_path, summary)
        written = True

    status = "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_BLOCKED"
    packet_id = "physical-quantum-qi-memory-kernel-consistency-gate-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_memory_kernel_consistency_gate_v11_4",
        "status": status,
        "packet_id": packet_id,
        "memory_kernel_consistency_gate_decision": str(packet.get("memory_kernel_consistency_gate_decision", "memory_kernel_consistency_block")),
        "gate_packet_written": written,
        "memory_kernel_consistency_gate_digest": _sha(packet),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiMemoryKernelConsistencyGateResult(
        "kuuos_runtime_daemon_physical_quantum_qi_memory_kernel_consistency_gate_v11_4",
        status,
        packet_id,
        str(root),
        str(packet.get("memory_kernel_consistency_gate_decision", "memory_kernel_consistency_block")),
        _int(counts.get("admitted")),
        _int(counts.get("probe")),
        _int(counts.get("blocked")),
        str(gate_packet_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
