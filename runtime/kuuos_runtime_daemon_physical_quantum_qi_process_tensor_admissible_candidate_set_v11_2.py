#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


GATE_DECISIONS = {"admit_candidate", "hold_candidate", "block_candidate"}
REQUIRED_GATE_RECEIPT_BOUNDARY_FLAGS = (
    "receipt_ledger_only",
    "cycle_gate_receipt_only",
    "does_not_execute_path",
    "does_not_run_runner",
    "does_not_start_next_cycle",
    "does_not_commit_plan",
    "does_not_consume_memory",
    "does_not_authorize_execution",
    "candidate_weighting_not_truth",
    "receipt_does_not_mutate_gate_packet",
    "receipt_does_not_select_final_path",
    "receipt_does_not_promote_truth",
    "replayable_receipt",
    "fail_closed_on_boundary_loss",
)
REQUIRED_PROCESS_TENSOR_FLAGS = (
    "history_bearing_process_tensor",
    "non_markov_context_required",
    "multi_time_window_required",
    "finite_horizon_only",
    "memory_kernel_visible",
    "does_not_execute_path",
    "does_not_run_runner",
    "does_not_start_next_cycle",
    "does_not_authorize_execution",
    "candidate_set_build_only",
    "fail_closed_on_boundary_loss",
)


@dataclass(frozen=True)
class PhysicalQuantumQiProcessTensorAdmissibleCandidateSetResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    admitted_count: int
    probe_count: int
    blocked_count: int
    candidate_set_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    candidate_set_written: bool
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


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _read_jsonl(path: pathlib.Path, blockers: list[str]) -> list[dict[str, Any]]:
    if not path.is_file():
        blockers.append("next_cycle_gate_receipt_ledger_missing")
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            blockers.append("next_cycle_gate_receipt_ledger_line_invalid")
            continue
        if isinstance(value, dict):
            records.append(value)
        else:
            blockers.append("next_cycle_gate_receipt_ledger_record_invalid")
    if not records:
        blockers.append("next_cycle_gate_receipt_ledger_empty")
    return records


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _validate_process_tensor_context(ctx: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> dict[str, Any]:
    if not ctx:
        blockers.append("process_tensor_context_missing_or_invalid")
        return {}
    boundary = _m(ctx.get("boundary"))
    for name in REQUIRED_PROCESS_TENSOR_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"process_tensor_boundary_{name}_missing")
    if ctx.get("process_tensor_context_considered") is not True:
        blockers.append("process_tensor_context_considered_not_true")
    if ctx.get("qi_process_tensor_mode") not in {"history_bearing_non_markov", "finite_horizon_history_bearing"}:
        blockers.append("qi_process_tensor_mode_not_history_bearing_non_markov")
    window = ctx.get("history_window")
    if not isinstance(window, list) or len(window) < 2:
        blockers.append("history_window_requires_at_least_two_slots")
    instruments = ctx.get("instrument_trace")
    if not isinstance(instruments, list) or len(instruments) < 1:
        blockers.append("instrument_trace_missing")
    if len(instruments) > 0 and isinstance(window, list) and len(window) > 0 and len(instruments) != len(window):
        warnings.append("instrument_trace_length_differs_from_history_window")
    if not ctx.get("process_tensor_digest"):
        blockers.append("process_tensor_digest_missing")
    if not ctx.get("memory_kernel_digest"):
        blockers.append("memory_kernel_digest_missing")
    if ctx.get("markov_only_context") is True:
        blockers.append("markov_only_context_forbidden")
    return {
        "process_tensor_digest": str(ctx.get("process_tensor_digest", "")),
        "memory_kernel_digest": str(ctx.get("memory_kernel_digest", "")),
        "history_window_digest": _sha(ctx.get("history_window", [])),
        "instrument_trace_digest": _sha(ctx.get("instrument_trace", [])),
        "non_markov_context_digest": str(ctx.get("non_markov_context_digest", _sha(ctx))),
    }


def _validate_gate_receipt(record: Mapping[str, Any], idx: int, blockers: list[str]) -> dict[str, Any]:
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_GATE_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"gate_receipt_{idx}_boundary_{name}_missing")
    if record.get("record_type") != "physical_quantum_qi_next_cycle_gate_receipt":
        blockers.append(f"gate_receipt_{idx}_record_type_invalid")
    decision = str(record.get("cycle_gate_decision", "block_candidate"))
    if decision not in GATE_DECISIONS:
        blockers.append(f"gate_receipt_{idx}_decision_invalid")
        decision = "block_candidate"
    weighting = dict(_m(record.get("candidate_weighting")))
    delta = _int(weighting.get("path_weight_delta"))
    probe = weighting.get("probe_potential_required") is True
    barrier = weighting.get("barrier_potential_required") is True
    barrier_blocks = weighting.get("barrier_blocks_ready_weight") is True
    if decision == "admit_candidate":
        if delta <= 0:
            blockers.append(f"gate_receipt_{idx}_admit_without_positive_delta")
        if probe or barrier or barrier_blocks:
            blockers.append(f"gate_receipt_{idx}_admit_with_probe_or_barrier")
    elif decision == "hold_candidate":
        if delta != 0:
            blockers.append(f"gate_receipt_{idx}_hold_with_delta")
        if not probe:
            blockers.append(f"gate_receipt_{idx}_hold_without_probe")
        if barrier or barrier_blocks:
            blockers.append(f"gate_receipt_{idx}_hold_with_barrier")
    elif decision == "block_candidate":
        if delta != 0:
            blockers.append(f"gate_receipt_{idx}_block_with_delta")
        if probe:
            blockers.append(f"gate_receipt_{idx}_block_with_probe")
        if not barrier or not barrier_blocks:
            blockers.append(f"gate_receipt_{idx}_block_without_barrier")
    return {
        "gate_receipt_digest": str(record.get("record_digest", _sha(dict(record)))),
        "cycle_gate_decision": decision,
        "source_candidate_status": str(record.get("source_candidate_status", "blocked_candidate")),
        "candidate_weighting": weighting,
    }


def _build_set(records: list[dict[str, Any]], pt: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    admitted: list[dict[str, Any]] = []
    probes: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    for idx, record in enumerate(records):
        item = _validate_gate_receipt(record, idx, blockers)
        item["process_tensor_context"] = dict(pt)
        item["candidate_id"] = "candidate-" + _sha(item)[:16]
        if item["cycle_gate_decision"] == "admit_candidate":
            admitted.append(item)
        elif item["cycle_gate_decision"] == "hold_candidate":
            probes.append(item)
        else:
            blocked.append(item)
    packet = {
        "version": "physical_quantum_qi_process_tensor_admissible_candidate_set_v11_2",
        "physical_quantum_qi_process_tensor_candidate_set_considered": True,
        "admitted_candidates": admitted,
        "probe_candidates": probes,
        "blocked_candidates": blocked,
        "counts": {"admitted": len(admitted), "probe": len(probes), "blocked": len(blocked)},
        "process_tensor_context": dict(pt),
        "boundary": {
            "candidate_set_build_only": True,
            "history_bearing_process_tensor": True,
            "non_markov_context_required": True,
            "multi_time_window_required": True,
            "finite_horizon_only": True,
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
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    packet["candidate_set_digest"] = _sha(packet)
    return packet


def build_physical_quantum_qi_process_tensor_admissible_candidate_set(
    *,
    runtime_context: Mapping[str, Any],
    process_tensor_admissible_candidate_set_license: Mapping[str, Any],
) -> PhysicalQuantumQiProcessTensorAdmissibleCandidateSetResult:
    ctx = _m(runtime_context)
    lic = _m(process_tensor_admissible_candidate_set_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ledger_path = root / "physical_quantum_qi_next_cycle_gate_receipt_ledger.jsonl"
    pt_context_path = root / "physical_quantum_qi_process_tensor_candidate_context.json"
    candidate_set_path = root / "physical_quantum_qi_process_tensor_admissible_candidate_set.json"
    summary_path = root / "physical_quantum_qi_process_tensor_admissible_candidate_set_summary.json"
    receipt_path = root / "physical_quantum_qi_process_tensor_admissible_candidate_set_receipt.json"
    audit_path = root / "physical_quantum_qi_process_tensor_admissible_candidate_set_audit.jsonl"

    if ctx.get("physical_quantum_qi_process_tensor_admissible_candidate_set_enabled") is not True:
        blockers.append("physical_quantum_qi_process_tensor_admissible_candidate_set_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_process_tensor_admissible_candidate_set") is not True:
        blockers.append("apply_physical_quantum_qi_process_tensor_admissible_candidate_set_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_ADMISSIBLE_CANDIDATE_SET_LICENSE_READY":
        blockers.append("physical_quantum_qi_process_tensor_admissible_candidate_set_license_not_ready")
    for name in [
        "gate_receipt_ledger_read_allowed",
        "process_tensor_context_read_allowed",
        "candidate_set_write_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    records = _read_jsonl(ledger_path, blockers)
    pt_context = _validate_process_tensor_context(_read_json(pt_context_path), blockers, warnings)
    packet: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _build_set(records, pt_context, blockers)
    if not blockers:
        summary = {
            "version": "physical_quantum_qi_process_tensor_admissible_candidate_set_summary_v11_2",
            "counts": dict(packet["counts"]),
            "candidate_set_digest": packet["candidate_set_digest"],
            "process_tensor_context": dict(pt_context),
            "boundary": {
                "summary_only": True,
                "candidate_set_build_only": True,
                "history_bearing_process_tensor": True,
                "non_markov_context_required": True,
                "does_not_start_next_cycle": True,
                "does_not_authorize_execution": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(candidate_set_path, packet)
        _write_json(summary_path, summary)
        written = True

    status = "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_ADMISSIBLE_CANDIDATE_SET_READY" if not blockers else "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_ADMISSIBLE_CANDIDATE_SET_BLOCKED"
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_process_tensor_admissible_candidate_set_v11_2",
        "status": status,
        "packet_id": "physical-quantum-qi-process-tensor-admissible-candidate-set-" + _sha({"packet": packet, "blockers": blockers})[:16],
        "candidate_set_written": written,
        "candidate_set_digest": _sha(packet),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    counts = _m(packet.get("counts")) if packet else {}
    return PhysicalQuantumQiProcessTensorAdmissibleCandidateSetResult(
        "kuuos_runtime_daemon_physical_quantum_qi_process_tensor_admissible_candidate_set_v11_2",
        status,
        str(receipt["packet_id"]),
        str(root),
        _int(counts.get("admitted")),
        _int(counts.get("probe")),
        _int(counts.get("blocked")),
        str(candidate_set_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
