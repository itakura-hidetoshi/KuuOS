#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ENVELOPE_STATUSES = {
    "transition_candidate_envelope_ready",
    "transition_candidate_envelope_hold",
    "transition_candidate_envelope_block",
}
EXPECTED_PRECHECK = {
    "transition_candidate_envelope_ready": "transition_precheck_admit_candidate",
    "transition_candidate_envelope_hold": "transition_precheck_hold_candidate",
    "transition_candidate_envelope_block": "transition_precheck_block_candidate",
}
REQUIRED_PACKET_BOUNDARY_FLAGS = (
    "transition_candidate_envelope_only",
    "envelope_build_only",
    "stable_corridor_transition_precheck_required",
    "history_aware_candidate_corridor_only",
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
LANES = ("admit_lane", "probe_lane", "blocked_lane")
EXPECTED_CONSISTENCY = {
    "admit_lane": "memory_consistent_admit",
    "probe_lane": "memory_consistent_probe",
    "blocked_lane": "memory_consistent_block",
}


@dataclass(frozen=True)
class PhysicalQuantumQiTransitionCandidateEnvelopeReceiptLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    envelope_status: str
    transition_precheck_decision: str
    envelope_count: int
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
    seg_context = dict(_m(segment.get("process_tensor_context")))
    for key, value in context.items():
        if not seg_context.get(key):
            blockers.append(f"{lane}_segment_{idx}_{key}_missing")
        elif str(seg_context.get(key)) != value:
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
        "process_tensor_context": seg_context,
    }


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
    env_context = dict(_m(envelope.get("process_tensor_context")))
    for key, value in context.items():
        if not env_context.get(key):
            blockers.append(f"transition_candidate_envelope_{idx}_{key}_missing")
        elif str(env_context.get(key)) != value:
            blockers.append(f"transition_candidate_envelope_{idx}_{key}_mismatch")
    return {
        "envelope_type": str(envelope.get("envelope_type", "")),
        "candidate_id": str(envelope.get("candidate_id", "")),
        "corridor_lane": str(envelope.get("corridor_lane", "")),
        "corridor_rank": _int(envelope.get("corridor_rank")),
        "transition_precheck_decision": str(envelope.get("transition_precheck_decision", "")),
        "corridor_stability_gate_decision": str(envelope.get("corridor_stability_gate_decision", "")),
        "candidate_weighting": dict(_m(envelope.get("candidate_weighting"))),
        "process_tensor_context": env_context,
        "transition_candidate_envelope_digest": str(envelope.get("transition_candidate_envelope_digest", _sha(dict(envelope)))),
    }


def _validate_packet(packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], dict[str, int], str, str]:
    if not packet:
        blockers.append("transition_candidate_envelope_packet_missing_or_invalid")
        return {}, {"admitted": 0, "probe": 0, "blocked": 0}, "transition_precheck_block_candidate", "transition_candidate_envelope_block"
    if packet.get("physical_quantum_qi_transition_candidate_envelope_considered") is not True:
        blockers.append("transition_candidate_envelope_considered_not_true")
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_PACKET_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"transition_candidate_envelope_boundary_{name}_missing")
    envelope_status = str(packet.get("envelope_status", "transition_candidate_envelope_block"))
    if envelope_status not in ENVELOPE_STATUSES:
        blockers.append("transition_candidate_envelope_status_invalid")
        envelope_status = "transition_candidate_envelope_block"
    precheck_decision = str(packet.get("transition_precheck_decision", "transition_precheck_block_candidate"))
    if precheck_decision != EXPECTED_PRECHECK[envelope_status]:
        blockers.append("transition_candidate_envelope_precheck_decision_mismatch")
        precheck_decision = EXPECTED_PRECHECK[envelope_status]
    context = _validate_context(_m(packet.get("process_tensor_context")), blockers)
    segments = _as_list(packet.get("corridor_segments"))
    counts = dict(_m(packet.get("counts")))
    lane_counts = dict(_m(packet.get("lane_counts")))
    envelopes_raw = _as_list(packet.get("transition_candidate_envelopes"))
    seen = {"admit_lane": 0, "probe_lane": 0, "blocked_lane": 0}
    clean_segments: list[dict[str, Any]] = []
    for idx, segment in enumerate(segments):
        lane = str(segment.get("corridor_lane", ""))
        rank = seen.get(lane, 0)
        clean = _validate_segment(segment, idx, rank, context, blockers, warnings)
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
    clean_envelopes = [_validate_envelope(item, idx, context, blockers) for idx, item in enumerate(envelopes_raw)]
    if envelope_status == "transition_candidate_envelope_ready":
        if precheck_decision != "transition_precheck_admit_candidate":
            blockers.append("ready_envelope_without_admit_precheck")
        if len(clean_envelopes) != seen["admit_lane"] or len(clean_envelopes) <= 0:
            blockers.append("ready_envelope_count_mismatch")
    elif clean_envelopes:
        blockers.append("hold_or_block_envelope_must_be_empty")
    if not packet.get("transition_candidate_envelope_packet_digest"):
        warnings.append("transition_candidate_envelope_packet_digest_missing")
    payload = {
        "envelope_status": envelope_status,
        "transition_precheck_decision": precheck_decision,
        "corridor_stability_gate_decision": str(packet.get("corridor_stability_gate_decision", "")),
        "corridor_status": str(packet.get("corridor_status", "")),
        "transition_candidate_envelopes": clean_envelopes,
        "corridor_segments": clean_segments,
        "lane_counts": dict(seen),
        "process_tensor_context": dict(context),
        "source_transition_candidate_envelope_packet_digest": str(packet.get("transition_candidate_envelope_packet_digest", _sha(dict(packet)))),
        "source_stable_corridor_transition_precheck_receipt_digest": str(_m(packet.get("source_digests")).get("stable_corridor_transition_precheck_receipt", "")),
        "source_stable_corridor_transition_precheck_digest": str(_m(packet.get("source_digests")).get("stable_corridor_transition_precheck", "")),
        "source_corridor_stability_gate_receipt_digest": str(_m(packet.get("source_digests")).get("corridor_stability_gate_receipt", "")),
        "source_corridor_stability_gate_digest": str(_m(packet.get("source_digests")).get("corridor_stability_gate", "")),
        "source_history_aware_candidate_corridor_receipt_digest": str(_m(packet.get("source_digests")).get("history_aware_candidate_corridor_receipt", "")),
        "source_history_aware_candidate_corridor_digest": str(_m(packet.get("source_digests")).get("history_aware_candidate_corridor", "")),
    }
    return payload, {"admitted": seen["admit_lane"], "probe": seen["probe_lane"], "blocked": seen["blocked_lane"]}, precheck_decision, envelope_status


def _record(payload: Mapping[str, Any], counts: Mapping[str, int], precheck_decision: str, envelope_status: str, prev_digest: str) -> dict[str, Any]:
    rec = {
        "version": "physical_quantum_qi_transition_candidate_envelope_receipt_record_v12_3",
        "record_type": "physical_quantum_qi_transition_candidate_envelope_receipt",
        "envelope_status": envelope_status,
        "transition_precheck_decision": precheck_decision,
        "corridor_stability_gate_decision": str(payload.get("corridor_stability_gate_decision", "")),
        "corridor_status": str(payload.get("corridor_status", "")),
        "counts": dict(counts),
        "lane_counts": dict(_m(payload.get("lane_counts"))),
        "envelope_count": len(payload.get("transition_candidate_envelopes", [])),
        "transition_candidate_envelopes": list(payload.get("transition_candidate_envelopes", [])),
        "corridor_segments": list(payload.get("corridor_segments", [])),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_transition_candidate_envelope_packet_digest": str(payload.get("source_transition_candidate_envelope_packet_digest", "")),
        "source_stable_corridor_transition_precheck_receipt_digest": str(payload.get("source_stable_corridor_transition_precheck_receipt_digest", "")),
        "source_stable_corridor_transition_precheck_digest": str(payload.get("source_stable_corridor_transition_precheck_digest", "")),
        "source_corridor_stability_gate_receipt_digest": str(payload.get("source_corridor_stability_gate_receipt_digest", "")),
        "source_corridor_stability_gate_digest": str(payload.get("source_corridor_stability_gate_digest", "")),
        "source_history_aware_candidate_corridor_receipt_digest": str(payload.get("source_history_aware_candidate_corridor_receipt_digest", "")),
        "source_history_aware_candidate_corridor_digest": str(payload.get("source_history_aware_candidate_corridor_digest", "")),
        "prev_record_digest": prev_digest,
        "boundary": {
            "receipt_ledger_only": True,
            "transition_candidate_envelope_receipt_only": True,
            "envelope_receipt_only": True,
            "transition_candidate_envelope_only": True,
            "envelope_build_only": True,
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
            "envelope_not_transition_start": True,
            "receipt_does_not_mutate_envelope_packet": True,
            "replayable_receipt": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def build_physical_quantum_qi_transition_candidate_envelope_receipt_ledger(
    *,
    runtime_context: Mapping[str, Any],
    transition_candidate_envelope_receipt_ledger_license: Mapping[str, Any],
) -> PhysicalQuantumQiTransitionCandidateEnvelopeReceiptLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(transition_candidate_envelope_receipt_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_transition_candidate_envelope_packet.json"
    ledger_path = root / "physical_quantum_qi_transition_candidate_envelope_receipt_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_transition_candidate_envelope_receipt_summary.json"
    receipt_path = root / "physical_quantum_qi_transition_candidate_envelope_receipt_ledger_receipt.json"
    audit_path = root / "physical_quantum_qi_transition_candidate_envelope_receipt_ledger_audit.jsonl"

    if ctx.get("physical_quantum_qi_transition_candidate_envelope_receipt_ledger_enabled") is not True:
        blockers.append("physical_quantum_qi_transition_candidate_envelope_receipt_ledger_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_transition_candidate_envelope_receipt_ledger") is not True:
        blockers.append("apply_physical_quantum_qi_transition_candidate_envelope_receipt_ledger_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_RECEIPT_LEDGER_LICENSE_READY":
        blockers.append("physical_quantum_qi_transition_candidate_envelope_receipt_ledger_license_not_ready")
    for name in [
        "transition_candidate_envelope_packet_read_allowed",
        "receipt_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, counts, precheck_decision, envelope_status = _validate_packet(_read_json(packet_path), blockers, warnings)
    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    if not blockers:
        record = _record(payload, counts, precheck_decision, envelope_status, _last_digest(ledger_path))
        _append_jsonl(ledger_path, record)
        summary = {
            "version": "physical_quantum_qi_transition_candidate_envelope_receipt_summary_v12_3",
            "envelope_status": envelope_status,
            "transition_precheck_decision": precheck_decision,
            "envelope_count": record["envelope_count"],
            "counts": dict(counts),
            "latest_record_digest": record["record_digest"],
            "source_transition_candidate_envelope_packet_digest": record["source_transition_candidate_envelope_packet_digest"],
            "process_tensor_context": dict(record["process_tensor_context"]),
            "boundary": {
                "summary_only": True,
                "transition_candidate_envelope_receipt_only": True,
                "envelope_receipt_only": True,
                "does_not_start_next_cycle": True,
                "does_not_authorize_execution": True,
                "does_not_select_final_path": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)
        appended = True

    status = "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_RECEIPT_LEDGER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_RECEIPT_LEDGER_BLOCKED"
    packet_id = "physical-quantum-qi-transition-candidate-envelope-receipt-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_transition_candidate_envelope_receipt_ledger_v12_3",
        "status": status,
        "packet_id": packet_id,
        "envelope_status": envelope_status,
        "transition_precheck_decision": precheck_decision,
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
    return PhysicalQuantumQiTransitionCandidateEnvelopeReceiptLedgerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_transition_candidate_envelope_receipt_ledger_v12_3",
        status,
        packet_id,
        str(root),
        envelope_status,
        precheck_decision,
        len(record.get("transition_candidate_envelopes", [])) if record else 0,
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
