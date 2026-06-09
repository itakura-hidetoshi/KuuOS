#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


CORRIDOR_TO_GATE = {
    "history_aware_admissible_corridor": "corridor_stability_admit",
    "history_aware_probe_corridor": "corridor_stability_hold",
    "history_aware_blocked_corridor": "corridor_stability_block",
}
REQUIRED_RECEIPT_BOUNDARY_FLAGS = (
    "receipt_ledger_only",
    "history_aware_candidate_corridor_receipt_only",
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
    "corridor_not_execution_path",
    "receipt_does_not_mutate_corridor_packet",
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
LANES = ("admit_lane", "probe_lane", "blocked_lane")
EXPECTED_CONSISTENCY = {
    "admit_lane": "memory_consistent_admit",
    "probe_lane": "memory_consistent_probe",
    "blocked_lane": "memory_consistent_block",
}


@dataclass(frozen=True)
class PhysicalQuantumQiCorridorStabilityGateResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    corridor_stability_gate_decision: str
    admitted_count: int
    probe_count: int
    blocked_count: int
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
        blockers.append("history_aware_candidate_corridor_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("history_aware_candidate_corridor_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("history_aware_candidate_corridor_receipt_ledger_latest_line_invalid")
        return {}
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[dict[str, Any]]:
    return [dict(_m(item)) for item in value] if isinstance(value, list) else []


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _validate_context(ctx: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    out = {key: str(ctx.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, value in out.items():
        if not value:
            blockers.append(f"process_tensor_context_{key}_missing")
    return out


def _validate_weighting(lane: str, weighting: Mapping[str, Any], idx: int, blockers: list[str]) -> None:
    delta = _int(weighting.get("path_weight_delta"))
    probe = weighting.get("probe_potential_required") is True
    barrier = weighting.get("barrier_potential_required") is True
    barrier_blocks = weighting.get("barrier_blocks_ready_weight") is True
    if lane == "admit_lane":
        if delta <= 0:
            blockers.append(f"admit_lane_segment_{idx}_without_positive_delta")
        if probe or barrier or barrier_blocks:
            blockers.append(f"admit_lane_segment_{idx}_with_probe_or_barrier")
    elif lane == "probe_lane":
        if delta != 0:
            blockers.append(f"probe_lane_segment_{idx}_with_delta")
        if not probe:
            blockers.append(f"probe_lane_segment_{idx}_without_probe")
        if barrier or barrier_blocks:
            blockers.append(f"probe_lane_segment_{idx}_with_barrier")
    elif lane == "blocked_lane":
        if delta != 0:
            blockers.append(f"blocked_lane_segment_{idx}_with_delta")
        if probe:
            blockers.append(f"blocked_lane_segment_{idx}_with_probe")
        if not barrier or not barrier_blocks:
            blockers.append(f"blocked_lane_segment_{idx}_without_barrier")
    else:
        blockers.append(f"corridor_segment_{idx}_lane_invalid")


def _validate_segment(segment: Mapping[str, Any], idx: int, expected_rank: int, context: Mapping[str, str], blockers: list[str], warnings: list[str]) -> dict[str, Any]:
    lane = str(segment.get("corridor_lane", ""))
    if lane not in LANES:
        blockers.append(f"corridor_segment_{idx}_lane_invalid")
        lane = "blocked_lane"
    if _int(segment.get("corridor_rank")) != expected_rank:
        blockers.append(f"{lane}_segment_{idx}_rank_mismatch")
    if str(segment.get("memory_kernel_consistency_decision", "")) != EXPECTED_CONSISTENCY[lane]:
        blockers.append(f"{lane}_segment_{idx}_memory_kernel_consistency_decision_mismatch")
    weighting = dict(_m(segment.get("candidate_weighting")))
    _validate_weighting(lane, weighting, idx, blockers)
    segment_context = dict(_m(segment.get("process_tensor_context")))
    for key, value in context.items():
        if not segment_context.get(key):
            blockers.append(f"{lane}_segment_{idx}_{key}_missing")
        elif str(segment_context.get(key)) != value:
            blockers.append(f"{lane}_segment_{idx}_{key}_mismatch")
    if not segment.get("candidate_id"):
        warnings.append(f"{lane}_segment_{idx}_candidate_id_missing")
    return {
        "corridor_lane": lane,
        "corridor_rank": expected_rank,
        "candidate_id": str(segment.get("candidate_id", f"missing-{lane}-{idx}")),
        "gate_receipt_digest": str(segment.get("gate_receipt_digest", "")),
        "cycle_gate_decision": str(segment.get("cycle_gate_decision", "")),
        "memory_kernel_consistency_decision": str(segment.get("memory_kernel_consistency_decision", "")),
        "candidate_weighting": weighting,
        "process_tensor_context": segment_context,
    }


def _validate_record(record: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], dict[str, int], str]:
    if not record:
        return {}, {"admitted": 0, "probe": 0, "blocked": 0}, "corridor_stability_block"
    if record.get("record_type") != "physical_quantum_qi_history_aware_candidate_corridor_receipt":
        blockers.append("history_aware_candidate_corridor_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"history_aware_corridor_receipt_boundary_{name}_missing")
    corridor_status = str(record.get("corridor_status", "history_aware_blocked_corridor"))
    if corridor_status not in CORRIDOR_TO_GATE:
        blockers.append("corridor_status_invalid")
        corridor_status = "history_aware_blocked_corridor"
    context = _validate_context(_m(record.get("process_tensor_context")), blockers)
    segments = _as_list(record.get("corridor_segments"))
    counts = dict(_m(record.get("counts")))
    lane_counts = dict(_m(record.get("lane_counts")))
    seen = {"admit_lane": 0, "probe_lane": 0, "blocked_lane": 0}
    clean_segments: list[dict[str, Any]] = []
    for idx, segment in enumerate(segments):
        lane = str(segment.get("corridor_lane", ""))
        expected_rank = seen.get(lane, 0)
        clean = _validate_segment(segment, idx, expected_rank, context, blockers, warnings)
        clean_segments.append(clean)
        if clean["corridor_lane"] in seen:
            seen[clean["corridor_lane"]] += 1
    if _int(counts.get("admitted")) != seen["admit_lane"]:
        blockers.append("admitted_count_mismatch")
    if _int(counts.get("probe")) != seen["probe_lane"]:
        blockers.append("probe_count_mismatch")
    if _int(counts.get("blocked")) != seen["blocked_lane"]:
        blockers.append("blocked_count_mismatch")
    if _int(lane_counts.get("admit_lane")) != seen["admit_lane"]:
        blockers.append("admit_lane_count_mismatch")
    if _int(lane_counts.get("probe_lane")) != seen["probe_lane"]:
        blockers.append("probe_lane_count_mismatch")
    if _int(lane_counts.get("blocked_lane")) != seen["blocked_lane"]:
        blockers.append("blocked_lane_count_mismatch")
    if corridor_status == "history_aware_admissible_corridor" and seen["admit_lane"] <= 0:
        blockers.append("admissible_corridor_without_admit_lane")
    if corridor_status == "history_aware_probe_corridor" and (seen["admit_lane"] > 0 or seen["probe_lane"] <= 0):
        blockers.append("probe_corridor_requires_probe_lane_only")
    if corridor_status == "history_aware_blocked_corridor" and (seen["admit_lane"] > 0 or seen["probe_lane"] > 0):
        blockers.append("blocked_corridor_with_admit_or_probe_lane")
    if not record.get("source_history_aware_candidate_corridor_digest"):
        warnings.append("source_history_aware_candidate_corridor_digest_missing")
    payload = {
        "source_history_aware_candidate_corridor_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "source_history_aware_candidate_corridor_digest": str(record.get("source_history_aware_candidate_corridor_digest", "")),
        "process_tensor_context": dict(context),
        "corridor_status": corridor_status,
        "corridor_segments": clean_segments,
        "lane_counts": dict(seen),
    }
    return payload, {"admitted": seen["admit_lane"], "probe": seen["probe_lane"], "blocked": seen["blocked_lane"]}, CORRIDOR_TO_GATE[corridor_status]


def _gate_packet(payload: Mapping[str, Any], counts: Mapping[str, int], decision: str) -> dict[str, Any]:
    packet = {
        "version": "physical_quantum_qi_corridor_stability_gate_packet_v11_8",
        "physical_quantum_qi_corridor_stability_gate_considered": True,
        "corridor_stability_gate_decision": decision,
        "corridor_status": str(payload.get("corridor_status", "history_aware_blocked_corridor")),
        "counts": dict(counts),
        "lane_counts": dict(_m(payload.get("lane_counts"))),
        "corridor_segments": list(payload.get("corridor_segments", [])),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_digests": {
            "history_aware_candidate_corridor_receipt": str(payload.get("source_history_aware_candidate_corridor_receipt_digest", "")),
            "history_aware_candidate_corridor": str(payload.get("source_history_aware_candidate_corridor_digest", "")),
        },
        "boundary": {
            "corridor_stability_gate_only": True,
            "stability_gate_only": True,
            "history_aware_candidate_corridor_only": True,
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
            "corridor_stability_not_execution_authority": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    packet["corridor_stability_gate_digest"] = _sha(packet)
    return packet


def build_physical_quantum_qi_corridor_stability_gate(
    *,
    runtime_context: Mapping[str, Any],
    corridor_stability_gate_license: Mapping[str, Any],
) -> PhysicalQuantumQiCorridorStabilityGateResult:
    ctx = _m(runtime_context)
    lic = _m(corridor_stability_gate_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ledger_path = root / "physical_quantum_qi_history_aware_candidate_corridor_receipt_ledger.jsonl"
    gate_packet_path = root / "physical_quantum_qi_corridor_stability_gate_packet.json"
    summary_path = root / "physical_quantum_qi_corridor_stability_gate_summary.json"
    receipt_path = root / "physical_quantum_qi_corridor_stability_gate_receipt.json"
    audit_path = root / "physical_quantum_qi_corridor_stability_gate_audit.jsonl"

    if ctx.get("physical_quantum_qi_corridor_stability_gate_enabled") is not True:
        blockers.append("physical_quantum_qi_corridor_stability_gate_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_corridor_stability_gate") is not True:
        blockers.append("apply_physical_quantum_qi_corridor_stability_gate_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_CORRIDOR_STABILITY_GATE_LICENSE_READY":
        blockers.append("physical_quantum_qi_corridor_stability_gate_license_not_ready")
    for name in [
        "history_aware_candidate_corridor_receipt_ledger_read_allowed",
        "corridor_stability_gate_packet_write_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, counts, gate_decision = _validate_record(_latest_jsonl(ledger_path, blockers), blockers, warnings)
    packet: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _gate_packet(payload, counts, gate_decision)
        summary = {
            "version": "physical_quantum_qi_corridor_stability_gate_summary_v11_8",
            "corridor_stability_gate_decision": gate_decision,
            "corridor_status": packet["corridor_status"],
            "counts": dict(counts),
            "corridor_stability_gate_digest": packet["corridor_stability_gate_digest"],
            "process_tensor_context": dict(packet["process_tensor_context"]),
            "boundary": {
                "summary_only": True,
                "corridor_stability_gate_only": True,
                "stability_gate_only": True,
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

    status = "PHYSICAL_QUANTUM_QI_CORRIDOR_STABILITY_GATE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_CORRIDOR_STABILITY_GATE_BLOCKED"
    packet_id = "physical-quantum-qi-corridor-stability-gate-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_corridor_stability_gate_v11_8",
        "status": status,
        "packet_id": packet_id,
        "corridor_stability_gate_decision": gate_decision,
        "gate_packet_written": written,
        "corridor_stability_gate_digest": _sha(packet),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiCorridorStabilityGateResult(
        "kuuos_runtime_daemon_physical_quantum_qi_corridor_stability_gate_v11_8",
        status,
        packet_id,
        str(root),
        gate_decision,
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
