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
    "memory_kernel_consistency_gate_receipt_only",
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
    "receipt_does_not_mutate_gate_packet",
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
DECISIONS = {
    "memory_kernel_consistency_admit": ("history_aware_admissible_corridor", "admitted_candidates"),
    "memory_kernel_consistency_hold": ("history_aware_probe_corridor", "probe_candidates"),
    "memory_kernel_consistency_block": ("history_aware_blocked_corridor", "blocked_candidates"),
}
LANES = (
    ("admitted_candidates", "admit_lane", "memory_consistent_admit"),
    ("probe_candidates", "probe_lane", "memory_consistent_probe"),
    ("blocked_candidates", "blocked_lane", "memory_consistent_block"),
)


@dataclass(frozen=True)
class PhysicalQuantumQiHistoryAwareCandidateCorridorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    corridor_status: str
    admitted_count: int
    probe_count: int
    blocked_count: int
    corridor_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    corridor_written: bool
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
        blockers.append("memory_kernel_consistency_gate_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("memory_kernel_consistency_gate_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("memory_kernel_consistency_gate_receipt_ledger_latest_line_invalid")
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


def _validate_weighting(lane_name: str, weighting: Mapping[str, Any], idx: int, blockers: list[str]) -> None:
    delta = _int(weighting.get("path_weight_delta"))
    probe = weighting.get("probe_potential_required") is True
    barrier = weighting.get("barrier_potential_required") is True
    barrier_blocks = weighting.get("barrier_blocks_ready_weight") is True
    if lane_name == "admit_lane":
        if delta <= 0:
            blockers.append(f"admit_lane_candidate_{idx}_without_positive_delta")
        if probe or barrier or barrier_blocks:
            blockers.append(f"admit_lane_candidate_{idx}_with_probe_or_barrier")
    elif lane_name == "probe_lane":
        if delta != 0:
            blockers.append(f"probe_lane_candidate_{idx}_with_delta")
        if not probe:
            blockers.append(f"probe_lane_candidate_{idx}_without_probe")
        if barrier or barrier_blocks:
            blockers.append(f"probe_lane_candidate_{idx}_with_barrier")
    else:
        if delta != 0:
            blockers.append(f"blocked_lane_candidate_{idx}_with_delta")
        if probe:
            blockers.append(f"blocked_lane_candidate_{idx}_with_probe")
        if not barrier or not barrier_blocks:
            blockers.append(f"blocked_lane_candidate_{idx}_without_barrier")


def _candidate_segment(kind: str, lane_name: str, expected_consistency: str, item: Mapping[str, Any], idx: int, context: Mapping[str, str], blockers: list[str], warnings: list[str]) -> dict[str, Any]:
    if str(item.get("memory_kernel_consistency_decision", "")) != expected_consistency:
        blockers.append(f"{kind}_{idx}_memory_kernel_consistency_decision_mismatch")
    weighting = dict(_m(item.get("candidate_weighting")))
    _validate_weighting(lane_name, weighting, idx, blockers)
    item_context = dict(_m(item.get("process_tensor_context")))
    for key, value in context.items():
        if not item_context.get(key):
            blockers.append(f"{kind}_{idx}_{key}_missing")
        elif str(item_context.get(key)) != value:
            blockers.append(f"{kind}_{idx}_{key}_mismatch")
    if not item.get("candidate_id"):
        warnings.append(f"{kind}_{idx}_candidate_id_missing")
    return {
        "corridor_lane": lane_name,
        "corridor_rank": idx,
        "candidate_id": str(item.get("candidate_id", f"missing-{kind}-{idx}")),
        "gate_receipt_digest": str(item.get("gate_receipt_digest", "")),
        "cycle_gate_decision": str(item.get("cycle_gate_decision", "")),
        "memory_kernel_consistency_decision": str(item.get("memory_kernel_consistency_decision", "")),
        "candidate_weighting": weighting,
        "process_tensor_context": item_context,
    }


def _validate_record(record: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], dict[str, int], str]:
    if not record:
        return {}, {"admitted": 0, "probe": 0, "blocked": 0}, "history_aware_blocked_corridor"
    if record.get("record_type") != "physical_quantum_qi_memory_kernel_consistency_gate_receipt":
        blockers.append("memory_kernel_consistency_gate_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"memory_kernel_consistency_receipt_boundary_{name}_missing")
    decision = str(record.get("memory_kernel_consistency_gate_decision", "memory_kernel_consistency_block"))
    if decision not in DECISIONS:
        blockers.append("memory_kernel_consistency_gate_decision_invalid")
        decision = "memory_kernel_consistency_block"
    corridor_status, expected_nonempty = DECISIONS[decision]
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
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
    if decision == "memory_kernel_consistency_admit" and len(admitted) <= 0:
        blockers.append("admit_corridor_without_admitted_candidates")
    if decision == "memory_kernel_consistency_hold" and (len(admitted) > 0 or len(probe) <= 0):
        blockers.append("hold_corridor_requires_probe_only_candidates")
    if decision == "memory_kernel_consistency_block" and (len(admitted) > 0 or len(probe) > 0):
        blockers.append("blocked_corridor_with_admitted_or_probe_candidates")
    segments: list[dict[str, Any]] = []
    lane_counts: dict[str, int] = {}
    for kind, lane_name, expected_consistency in LANES:
        items = {"admitted_candidates": admitted, "probe_candidates": probe, "blocked_candidates": blocked}[kind]
        lane_counts[lane_name] = len(items)
        for idx, item in enumerate(items):
            segments.append(_candidate_segment(kind, lane_name, expected_consistency, item, idx, context, blockers, warnings))
    payload = {
        "source_memory_kernel_consistency_gate_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_memory_kernel_consistency_gate_digest": str(record.get("source_memory_kernel_consistency_gate_digest", "")),
        "source_process_tensor_candidate_set_receipt_digest": str(record.get("source_process_tensor_candidate_set_receipt_digest", "")),
        "source_process_tensor_admissible_candidate_set_digest": str(record.get("source_process_tensor_admissible_candidate_set_digest", "")),
        "process_tensor_context": dict(context),
        "corridor_status": corridor_status,
        "expected_nonempty_class": expected_nonempty,
        "corridor_segments": segments,
        "lane_counts": lane_counts,
    }
    result_counts = {"admitted": len(admitted), "probe": len(probe), "blocked": len(blocked)}
    return payload, result_counts, corridor_status


def _corridor_packet(payload: Mapping[str, Any], counts: Mapping[str, int]) -> dict[str, Any]:
    packet = {
        "version": "physical_quantum_qi_history_aware_candidate_corridor_packet_v11_6",
        "physical_quantum_qi_history_aware_candidate_corridor_considered": True,
        "corridor_status": str(payload.get("corridor_status", "history_aware_blocked_corridor")),
        "counts": dict(counts),
        "lane_counts": dict(_m(payload.get("lane_counts"))),
        "corridor_segments": list(payload.get("corridor_segments", [])),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_digests": {
            "memory_kernel_consistency_gate_receipt": str(payload.get("source_memory_kernel_consistency_gate_receipt_digest", "")),
            "memory_kernel_consistency_gate": str(payload.get("source_memory_kernel_consistency_gate_digest", "")),
            "process_tensor_candidate_set_receipt": str(payload.get("source_process_tensor_candidate_set_receipt_digest", "")),
            "process_tensor_admissible_candidate_set": str(payload.get("source_process_tensor_admissible_candidate_set_digest", "")),
        },
        "boundary": {
            "history_aware_candidate_corridor_only": True,
            "corridor_build_only": True,
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
            "corridor_not_execution_path": True,
            "admissible_set_not_execution_set": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    packet["history_aware_candidate_corridor_digest"] = _sha(packet)
    return packet


def build_physical_quantum_qi_history_aware_candidate_corridor(
    *,
    runtime_context: Mapping[str, Any],
    history_aware_candidate_corridor_license: Mapping[str, Any],
) -> PhysicalQuantumQiHistoryAwareCandidateCorridorResult:
    ctx = _m(runtime_context)
    lic = _m(history_aware_candidate_corridor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ledger_path = root / "physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger.jsonl"
    corridor_path = root / "physical_quantum_qi_history_aware_candidate_corridor.json"
    summary_path = root / "physical_quantum_qi_history_aware_candidate_corridor_summary.json"
    receipt_path = root / "physical_quantum_qi_history_aware_candidate_corridor_receipt.json"
    audit_path = root / "physical_quantum_qi_history_aware_candidate_corridor_audit.jsonl"

    if ctx.get("physical_quantum_qi_history_aware_candidate_corridor_enabled") is not True:
        blockers.append("physical_quantum_qi_history_aware_candidate_corridor_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_history_aware_candidate_corridor") is not True:
        blockers.append("apply_physical_quantum_qi_history_aware_candidate_corridor_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_LICENSE_READY":
        blockers.append("physical_quantum_qi_history_aware_candidate_corridor_license_not_ready")
    for name in [
        "memory_kernel_consistency_gate_receipt_ledger_read_allowed",
        "history_aware_candidate_corridor_write_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, counts, corridor_status = _validate_record(_latest_jsonl(ledger_path, blockers), blockers, warnings)
    packet: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _corridor_packet(payload, counts)
        summary = {
            "version": "physical_quantum_qi_history_aware_candidate_corridor_summary_v11_6",
            "corridor_status": corridor_status,
            "counts": dict(counts),
            "history_aware_candidate_corridor_digest": packet["history_aware_candidate_corridor_digest"],
            "process_tensor_context": dict(packet["process_tensor_context"]),
            "boundary": {
                "summary_only": True,
                "history_aware_candidate_corridor_only": True,
                "corridor_build_only": True,
                "does_not_start_next_cycle": True,
                "does_not_authorize_execution": True,
                "does_not_select_final_path": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(corridor_path, packet)
        _write_json(summary_path, summary)
        written = True

    status = "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_READY" if not blockers else "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_BLOCKED"
    packet_id = "physical-quantum-qi-history-aware-candidate-corridor-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_history_aware_candidate_corridor_v11_6",
        "status": status,
        "packet_id": packet_id,
        "corridor_status": corridor_status,
        "corridor_written": written,
        "history_aware_candidate_corridor_digest": _sha(packet),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiHistoryAwareCandidateCorridorResult(
        "kuuos_runtime_daemon_physical_quantum_qi_history_aware_candidate_corridor_v11_6",
        status,
        packet_id,
        str(root),
        corridor_status,
        _int(counts.get("admitted")),
        _int(counts.get("probe")),
        _int(counts.get("blocked")),
        str(corridor_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
