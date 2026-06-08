#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


REQUIRED_CANDIDATE_SET_BOUNDARY_FLAGS = (
    "candidate_set_build_only",
    "history_bearing_process_tensor",
    "non_markov_context_required",
    "multi_time_window_required",
    "finite_horizon_only",
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
    "fail_closed_on_boundary_loss",
)
REQUIRED_PROCESS_TENSOR_CONTEXT_KEYS = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)


@dataclass(frozen=True)
class PhysicalQuantumQiProcessTensorCandidateSetReceiptLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
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


def _validate_weighting(kind: str, weighting: Mapping[str, Any], idx: int, blockers: list[str]) -> None:
    delta = _int(weighting.get("path_weight_delta"))
    probe = weighting.get("probe_potential_required") is True
    barrier = weighting.get("barrier_potential_required") is True
    barrier_blocks = weighting.get("barrier_blocks_ready_weight") is True
    if kind == "admitted":
        if delta <= 0:
            blockers.append(f"admitted_candidate_{idx}_without_positive_delta")
        if probe or barrier or barrier_blocks:
            blockers.append(f"admitted_candidate_{idx}_with_probe_or_barrier")
    elif kind == "probe":
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


def _validate_candidate_list(kind: str, items: list[dict[str, Any]], pt: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    expected_decision = {"admitted": "admit_candidate", "probe": "hold_candidate", "blocked": "block_candidate"}[kind]
    for idx, item in enumerate(items):
        decision = str(item.get("cycle_gate_decision", ""))
        if decision != expected_decision:
            blockers.append(f"{kind}_candidate_{idx}_decision_mismatch")
        weighting = dict(_m(item.get("candidate_weighting")))
        _validate_weighting(kind, weighting, idx, blockers)
        item_pt = dict(_m(item.get("process_tensor_context")))
        for key in REQUIRED_PROCESS_TENSOR_CONTEXT_KEYS:
            if not item_pt.get(key):
                blockers.append(f"{kind}_candidate_{idx}_process_tensor_{key}_missing")
            elif pt.get(key) and item_pt.get(key) != pt.get(key):
                blockers.append(f"{kind}_candidate_{idx}_process_tensor_{key}_mismatch")
        if not item.get("candidate_id"):
            warnings.append(f"{kind}_candidate_{idx}_candidate_id_missing")
        out.append({
            "candidate_id": str(item.get("candidate_id", f"missing-{kind}-{idx}")),
            "gate_receipt_digest": str(item.get("gate_receipt_digest", "")),
            "cycle_gate_decision": decision,
            "source_candidate_status": str(item.get("source_candidate_status", "")),
            "candidate_weighting": weighting,
            "process_tensor_context": item_pt,
        })
    return out


def _validate_candidate_set(packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], dict[str, int]]:
    if not packet:
        blockers.append("process_tensor_admissible_candidate_set_missing_or_invalid")
        return {}, {"admitted": 0, "probe": 0, "blocked": 0}
    if packet.get("physical_quantum_qi_process_tensor_candidate_set_considered") is not True:
        blockers.append("process_tensor_candidate_set_considered_not_true")
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_CANDIDATE_SET_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"candidate_set_boundary_{name}_missing")
    pt = dict(_m(packet.get("process_tensor_context")))
    for key in REQUIRED_PROCESS_TENSOR_CONTEXT_KEYS:
        if not pt.get(key):
            blockers.append(f"process_tensor_context_{key}_missing")
    admitted = _as_list(packet.get("admitted_candidates"))
    probe = _as_list(packet.get("probe_candidates"))
    blocked = _as_list(packet.get("blocked_candidates"))
    counts = dict(_m(packet.get("counts")))
    if _int(counts.get("admitted")) != len(admitted):
        blockers.append("admitted_count_mismatch")
    if _int(counts.get("probe")) != len(probe):
        blockers.append("probe_count_mismatch")
    if _int(counts.get("blocked")) != len(blocked):
        blockers.append("blocked_count_mismatch")
    if not packet.get("candidate_set_digest"):
        warnings.append("candidate_set_digest_missing")
    rec_payload = {
        "admitted_candidates": _validate_candidate_list("admitted", admitted, pt, blockers, warnings),
        "probe_candidates": _validate_candidate_list("probe", probe, pt, blockers, warnings),
        "blocked_candidates": _validate_candidate_list("blocked", blocked, pt, blockers, warnings),
        "process_tensor_context": pt,
        "source_candidate_set_digest": str(packet.get("candidate_set_digest", _sha(dict(packet)))),
    }
    rec_counts = {"admitted": len(admitted), "probe": len(probe), "blocked": len(blocked)}
    return rec_payload, rec_counts


def _record(payload: Mapping[str, Any], counts: Mapping[str, int], prev_digest: str) -> dict[str, Any]:
    rec = {
        "version": "physical_quantum_qi_process_tensor_candidate_set_receipt_record_v11_3",
        "record_type": "physical_quantum_qi_process_tensor_candidate_set_receipt",
        "counts": dict(counts),
        "admitted_candidates": list(payload.get("admitted_candidates", [])),
        "probe_candidates": list(payload.get("probe_candidates", [])),
        "blocked_candidates": list(payload.get("blocked_candidates", [])),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_candidate_set_digest": str(payload.get("source_candidate_set_digest", "")),
        "prev_record_digest": prev_digest,
        "boundary": {
            "receipt_ledger_only": True,
            "process_tensor_candidate_set_receipt_only": True,
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
            "replayable_receipt": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def build_physical_quantum_qi_process_tensor_candidate_set_receipt_ledger(
    *,
    runtime_context: Mapping[str, Any],
    process_tensor_candidate_set_receipt_ledger_license: Mapping[str, Any],
) -> PhysicalQuantumQiProcessTensorCandidateSetReceiptLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(process_tensor_candidate_set_receipt_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_process_tensor_admissible_candidate_set.json"
    ledger_path = root / "physical_quantum_qi_process_tensor_candidate_set_receipt_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_process_tensor_candidate_set_receipt_summary.json"
    receipt_path = root / "physical_quantum_qi_process_tensor_candidate_set_receipt_ledger_receipt.json"
    audit_path = root / "physical_quantum_qi_process_tensor_candidate_set_receipt_ledger_audit.jsonl"

    if ctx.get("physical_quantum_qi_process_tensor_candidate_set_receipt_ledger_enabled") is not True:
        blockers.append("physical_quantum_qi_process_tensor_candidate_set_receipt_ledger_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_process_tensor_candidate_set_receipt_ledger") is not True:
        blockers.append("apply_physical_quantum_qi_process_tensor_candidate_set_receipt_ledger_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_CANDIDATE_SET_RECEIPT_LEDGER_LICENSE_READY":
        blockers.append("physical_quantum_qi_process_tensor_candidate_set_receipt_ledger_license_not_ready")
    for name in [
        "candidate_set_read_allowed",
        "receipt_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, counts = _validate_candidate_set(_read_json(packet_path), blockers, warnings)
    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    if not blockers:
        record = _record(payload, counts, _last_digest(ledger_path))
        _append_jsonl(ledger_path, record)
        summary = {
            "version": "physical_quantum_qi_process_tensor_candidate_set_receipt_summary_v11_3",
            "counts": dict(counts),
            "latest_record_digest": record["record_digest"],
            "source_candidate_set_digest": record["source_candidate_set_digest"],
            "process_tensor_context": dict(record["process_tensor_context"]),
            "boundary": {
                "summary_only": True,
                "history_bearing_process_tensor": True,
                "non_markov_context_required": True,
                "does_not_start_next_cycle": True,
                "does_not_authorize_execution": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)
        appended = True

    status = "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_CANDIDATE_SET_RECEIPT_LEDGER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_CANDIDATE_SET_RECEIPT_LEDGER_BLOCKED"
    packet_id = "physical-quantum-qi-process-tensor-candidate-set-receipt-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_process_tensor_candidate_set_receipt_ledger_v11_3",
        "status": status,
        "packet_id": packet_id,
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
    return PhysicalQuantumQiProcessTensorCandidateSetReceiptLedgerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_process_tensor_candidate_set_receipt_ledger_v11_3",
        status,
        packet_id,
        str(root),
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
