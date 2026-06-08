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
CANDIDATE_STATUS_BY_GATE = {
    "admit_candidate": "weighted_candidate",
    "hold_candidate": "probe_only_candidate",
    "block_candidate": "blocked_candidate",
}
REQUIRED_GATE_BOUNDARY_FLAGS = (
    "cycle_gate_only",
    "next_cycle_candidate_gate_only",
    "does_not_execute_path",
    "does_not_run_runner",
    "does_not_start_next_cycle",
    "does_not_commit_plan",
    "does_not_consume_memory",
    "does_not_authorize_execution",
    "candidate_weighting_not_truth",
    "gate_does_not_mutate_receipt_ledger",
    "gate_does_not_select_final_path",
    "gate_does_not_promote_truth",
    "barrier_potential_can_only_block_or_probe",
    "fail_closed_on_boundary_loss",
)


@dataclass(frozen=True)
class PhysicalQuantumQiNextCycleGateReceiptLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    cycle_gate_decision: str
    source_candidate_status: str
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


def _validate_gate_packet(packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[str, str, dict[str, Any]]:
    if not packet:
        blockers.append("next_cycle_candidate_weighting_cycle_gate_packet_missing_or_invalid")
        return "block_candidate", "blocked_candidate", {}
    if packet.get("physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_considered") is not True:
        blockers.append("cycle_gate_considered_not_true")
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_GATE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"cycle_gate_boundary_{name}_missing")
    decision = str(packet.get("cycle_gate_decision", "block_candidate"))
    candidate_status = str(packet.get("source_candidate_status", "blocked_candidate"))
    if decision not in GATE_DECISIONS:
        blockers.append("cycle_gate_decision_invalid")
        decision = "block_candidate"
    expected = CANDIDATE_STATUS_BY_GATE[decision]
    if candidate_status != expected:
        blockers.append("candidate_status_gate_decision_mismatch")
        candidate_status = "blocked_candidate"
    weighting = dict(_m(packet.get("candidate_weighting")))
    delta = _int(weighting.get("path_weight_delta"))
    probe = weighting.get("probe_potential_required") is True
    barrier = weighting.get("barrier_potential_required") is True
    barrier_blocks = weighting.get("barrier_blocks_ready_weight") is True
    if decision == "admit_candidate":
        if delta <= 0:
            blockers.append("admit_gate_without_positive_delta")
        if probe or barrier or barrier_blocks:
            blockers.append("admit_gate_with_probe_or_barrier")
    elif decision == "hold_candidate":
        if delta != 0:
            blockers.append("hold_gate_with_delta")
        if not probe:
            blockers.append("hold_gate_without_probe")
        if barrier or barrier_blocks:
            blockers.append("hold_gate_with_barrier")
    elif decision == "block_candidate":
        if delta != 0:
            blockers.append("block_gate_with_delta")
        if probe:
            blockers.append("block_gate_with_probe")
        if not barrier or not barrier_blocks:
            blockers.append("block_gate_without_barrier")
    if not packet.get("cycle_gate_packet_digest"):
        warnings.append("cycle_gate_packet_digest_missing")
    return decision, candidate_status, weighting


def _record(packet: Mapping[str, Any], decision: str, candidate_status: str, weighting: Mapping[str, Any], prev: str) -> dict[str, Any]:
    rec = {
        "version": "physical_quantum_qi_next_cycle_gate_receipt_record_v11_1",
        "record_type": "physical_quantum_qi_next_cycle_gate_receipt",
        "cycle_gate_decision": decision,
        "source_candidate_status": candidate_status,
        "candidate_weighting": dict(weighting),
        "source_cycle_gate_packet_digest": str(packet.get("cycle_gate_packet_digest", _sha(dict(packet)))),
        "prev_record_digest": prev,
        "boundary": {
            "receipt_ledger_only": True,
            "cycle_gate_receipt_only": True,
            "does_not_execute_path": True,
            "does_not_run_runner": True,
            "does_not_start_next_cycle": True,
            "does_not_commit_plan": True,
            "does_not_consume_memory": True,
            "does_not_authorize_execution": True,
            "candidate_weighting_not_truth": True,
            "receipt_does_not_mutate_gate_packet": True,
            "receipt_does_not_select_final_path": True,
            "receipt_does_not_promote_truth": True,
            "replayable_receipt": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def _summary(record: Mapping[str, Any]) -> dict[str, Any]:
    summary = {
        "version": "physical_quantum_qi_next_cycle_gate_receipt_summary_v11_1",
        "latest_cycle_gate_decision": str(record.get("cycle_gate_decision", "block_candidate")),
        "latest_source_candidate_status": str(record.get("source_candidate_status", "blocked_candidate")),
        "latest_record_digest": str(record.get("record_digest", "")),
        "source_cycle_gate_packet_digest": str(record.get("source_cycle_gate_packet_digest", "")),
        "boundary": {
            "summary_only": True,
            "does_not_execute_path": True,
            "does_not_run_runner": True,
            "does_not_start_next_cycle": True,
            "does_not_authorize_execution": True,
            "candidate_weighting_not_truth": True,
        },
        "epoch": int(time.time()),
    }
    summary["summary_digest"] = _sha(summary)
    return summary


def build_physical_quantum_qi_next_cycle_gate_receipt_ledger(
    *,
    runtime_context: Mapping[str, Any],
    next_cycle_gate_receipt_ledger_license: Mapping[str, Any],
) -> PhysicalQuantumQiNextCycleGateReceiptLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(next_cycle_gate_receipt_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_packet.json"
    ledger_path = root / "physical_quantum_qi_next_cycle_gate_receipt_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_next_cycle_gate_receipt_summary.json"
    receipt_path = root / "physical_quantum_qi_next_cycle_gate_receipt_ledger_receipt.json"
    audit_path = root / "physical_quantum_qi_next_cycle_gate_receipt_ledger_audit.jsonl"

    if ctx.get("physical_quantum_qi_next_cycle_gate_receipt_ledger_enabled") is not True:
        blockers.append("physical_quantum_qi_next_cycle_gate_receipt_ledger_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_next_cycle_gate_receipt_ledger") is not True:
        blockers.append("apply_physical_quantum_qi_next_cycle_gate_receipt_ledger_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_GATE_RECEIPT_LEDGER_LICENSE_READY":
        blockers.append("physical_quantum_qi_next_cycle_gate_receipt_ledger_license_not_ready")
    for name in ["cycle_gate_packet_read_allowed", "receipt_ledger_append_allowed", "summary_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(packet_path)
    decision, candidate_status, weighting = _validate_gate_packet(packet, blockers, warnings)
    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    if not blockers:
        record = _record(packet, decision, candidate_status, weighting, _last_digest(ledger_path))
        _append_jsonl(ledger_path, record)
        summary = _summary(record)
        _write_json(summary_path, summary)
        appended = True

    status = "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_GATE_RECEIPT_LEDGER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_GATE_RECEIPT_LEDGER_BLOCKED"
    packet_id = "physical-quantum-qi-next-cycle-gate-receipt-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_next_cycle_gate_receipt_ledger_v11_1",
        "status": status,
        "packet_id": packet_id,
        "cycle_gate_decision": decision,
        "source_candidate_status": candidate_status,
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
    return PhysicalQuantumQiNextCycleGateReceiptLedgerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_next_cycle_gate_receipt_ledger_v11_1",
        status,
        packet_id,
        str(root),
        decision,
        candidate_status,
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        appended,
        blockers,
        warnings,
    )
