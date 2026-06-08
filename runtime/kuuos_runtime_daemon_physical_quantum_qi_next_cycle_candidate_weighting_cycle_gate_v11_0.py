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
STATUS_TO_GATE = {
    "weighted_candidate": "admit_candidate",
    "probe_only_candidate": "hold_candidate",
    "blocked_candidate": "block_candidate",
}
MODE_TO_STATUS = {
    "increase_candidate_path_weight": "weighted_candidate",
    "open_probe_candidate_channel": "probe_only_candidate",
    "install_barrier_candidate_potential": "blocked_candidate",
}
REQUIRED_RECEIPT_BOUNDARY_FLAGS = (
    "receipt_ledger_only",
    "next_cycle_candidate_weighting_receipt_only",
    "does_not_execute_path",
    "does_not_run_runner",
    "does_not_start_next_cycle",
    "does_not_commit_plan",
    "does_not_consume_memory",
    "does_not_authorize_execution",
    "candidate_weighting_not_truth",
    "receipt_does_not_mutate_bridge_packet",
    "receipt_does_not_start_next_cycle",
    "barrier_potential_can_only_block_or_probe",
    "replayable_receipt",
    "fail_closed_on_boundary_loss",
)


@dataclass(frozen=True)
class PhysicalQuantumQiNextCycleCandidateWeightingCycleGateResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    source_candidate_status: str
    cycle_gate_decision: str
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
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


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
        blockers.append("candidate_weighting_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("candidate_weighting_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("candidate_weighting_receipt_ledger_latest_line_invalid")
        return {}
    return value if isinstance(value, dict) else {}


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _validate_receipt(record: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[str, str, dict[str, Any]]:
    if not record:
        return "blocked_candidate", "block_candidate", {}
    if record.get("record_type") != "physical_quantum_qi_next_cycle_candidate_weighting_receipt":
        blockers.append("candidate_weighting_receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in REQUIRED_RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"candidate_weighting_receipt_boundary_{name}_missing")
    mode = str(record.get("bridge_mode", "install_barrier_candidate_potential"))
    candidate_status = str(record.get("next_cycle_candidate_status", "blocked_candidate"))
    if mode not in MODE_TO_STATUS:
        blockers.append("candidate_weighting_receipt_bridge_mode_invalid")
        mode = "install_barrier_candidate_potential"
    expected_status = MODE_TO_STATUS[mode]
    if candidate_status != expected_status:
        blockers.append("candidate_status_bridge_mode_mismatch")
        candidate_status = "blocked_candidate"
    weighting = dict(_m(record.get("candidate_weighting")))
    delta = _int(weighting.get("path_weight_delta"))
    probe = weighting.get("probe_potential_required") is True
    barrier = weighting.get("barrier_potential_required") is True
    barrier_blocks = weighting.get("barrier_blocks_ready_weight") is True
    if candidate_status == "weighted_candidate":
        if delta <= 0:
            blockers.append("weighted_candidate_without_positive_delta")
        if probe or barrier or barrier_blocks:
            blockers.append("weighted_candidate_with_probe_or_barrier")
    elif candidate_status == "probe_only_candidate":
        if delta != 0:
            blockers.append("probe_candidate_with_delta")
        if not probe:
            blockers.append("probe_candidate_without_probe")
        if barrier or barrier_blocks:
            blockers.append("probe_candidate_with_barrier")
    elif candidate_status == "blocked_candidate":
        if delta != 0:
            blockers.append("blocked_candidate_with_delta")
        if probe:
            blockers.append("blocked_candidate_with_probe")
        if not barrier or not barrier_blocks:
            blockers.append("blocked_candidate_without_barrier")
    else:
        blockers.append("next_cycle_candidate_status_invalid")
        candidate_status = "blocked_candidate"
    if str(record.get("prev_record_digest", "")) == "CORRUPT_PREVIOUS_LEDGER_LINE":
        warnings.append("previous_candidate_weighting_receipt_digest_corrupt_marker_visible")
    return candidate_status, STATUS_TO_GATE[candidate_status], weighting


def _gate_packet(record: Mapping[str, Any], candidate_status: str, gate_decision: str, weighting: Mapping[str, Any]) -> dict[str, Any]:
    packet = {
        "version": "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_packet_v11_0",
        "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_considered": True,
        "source_candidate_status": candidate_status,
        "source_bridge_mode": str(record.get("bridge_mode", "install_barrier_candidate_potential")),
        "cycle_gate_decision": gate_decision,
        "candidate_weighting": dict(weighting),
        "source_digests": {
            "candidate_weighting_receipt_record": str(record.get("record_digest", _sha(dict(record))))
        },
        "boundary": {
            "cycle_gate_only": True,
            "next_cycle_candidate_gate_only": True,
            "does_not_execute_path": True,
            "does_not_run_runner": True,
            "does_not_start_next_cycle": True,
            "does_not_commit_plan": True,
            "does_not_consume_memory": True,
            "does_not_authorize_execution": True,
            "candidate_weighting_not_truth": True,
            "gate_does_not_mutate_receipt_ledger": True,
            "gate_does_not_select_final_path": True,
            "gate_does_not_promote_truth": True,
            "barrier_potential_can_only_block_or_probe": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    packet["cycle_gate_packet_digest"] = _sha(packet)
    return packet


def build_physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate(
    *,
    runtime_context: Mapping[str, Any],
    next_cycle_candidate_weighting_cycle_gate_license: Mapping[str, Any],
) -> PhysicalQuantumQiNextCycleCandidateWeightingCycleGateResult:
    ctx = _m(runtime_context)
    lic = _m(next_cycle_candidate_weighting_cycle_gate_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ledger_path = root / "physical_quantum_qi_next_cycle_candidate_weighting_receipt_ledger.jsonl"
    gate_packet_path = root / "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_packet.json"
    summary_path = root / "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_summary.json"
    receipt_path = root / "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_receipt.json"
    audit_path = root / "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_audit.jsonl"

    if ctx.get("physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_enabled") is not True:
        blockers.append("physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate") is not True:
        blockers.append("apply_physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_CYCLE_GATE_LICENSE_READY":
        blockers.append("physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_license_not_ready")
    for name in [
        "candidate_weighting_receipt_ledger_read_allowed",
        "cycle_gate_packet_write_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    record = _latest_jsonl(ledger_path, blockers)
    candidate_status, gate_decision, weighting = _validate_receipt(record, blockers, warnings)
    packet: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _gate_packet(record, candidate_status, gate_decision, weighting)
        summary = {
            "version": "physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_summary_v11_0",
            "source_candidate_status": candidate_status,
            "cycle_gate_decision": gate_decision,
            "cycle_gate_packet_digest": packet["cycle_gate_packet_digest"],
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
        _write_json(gate_packet_path, packet)
        _write_json(summary_path, summary)
        written = True

    status = "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_CYCLE_GATE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_CYCLE_GATE_BLOCKED"
    packet_id = "physical-quantum-qi-next-cycle-candidate-weighting-cycle-gate-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_v11_0",
        "status": status,
        "packet_id": packet_id,
        "source_candidate_status": candidate_status,
        "cycle_gate_decision": gate_decision,
        "gate_packet_written": written,
        "cycle_gate_packet_digest": _sha(packet),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiNextCycleCandidateWeightingCycleGateResult(
        "kuuos_runtime_daemon_physical_quantum_qi_next_cycle_candidate_weighting_cycle_gate_v11_0",
        status,
        packet_id,
        str(root),
        candidate_status,
        gate_decision,
        str(gate_packet_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
