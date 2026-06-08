#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


DECISION_TO_ACTION = {
    "accept": "reinforce_path_weight",
    "hold": "open_probe_potential",
    "block": "add_barrier_potential",
}
ACTION_TO_BRIDGE_MODE = {
    "reinforce_path_weight": "increase_candidate_path_weight",
    "open_probe_potential": "open_probe_candidate_channel",
    "add_barrier_potential": "install_barrier_candidate_potential",
}
RECEIPT_BOUNDARY_FLAGS = (
    "receipt_ledger_only",
    "reentry_intake_receipt_only",
    "does_not_execute_path",
    "does_not_run_runner",
    "does_not_commit_plan",
    "does_not_consume_memory",
    "does_not_authorize_execution",
    "candidate_weighting_not_truth",
    "barrier_potential_can_only_block_or_probe",
    "receipt_does_not_authorize_execution",
    "replayable_receipt",
    "fail_closed_on_boundary_loss",
)


@dataclass(frozen=True)
class PhysicalQuantumQiNextCycleCandidateWeightingBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    reentry_intake_decision: str
    bridge_mode: str
    bridge_packet_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    bridge_packet_written: bool
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


def _read_latest_jsonl(path: pathlib.Path, blockers: list[str]) -> dict[str, Any]:
    if not path.is_file():
        blockers.append("reentry_intake_receipt_ledger_missing")
        return {}
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        blockers.append("reentry_intake_receipt_ledger_empty")
        return {}
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        blockers.append("reentry_intake_receipt_ledger_latest_line_invalid")
        return {}
    return value if isinstance(value, dict) else {}


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _validate_record(record: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[str, str, dict[str, Any]]:
    if not record:
        return "block", "install_barrier_candidate_potential", {}
    if record.get("record_type") != "physical_quantum_qi_path_integral_reentry_intake_receipt":
        blockers.append("receipt_record_type_invalid")
    boundary = _m(record.get("boundary"))
    for name in RECEIPT_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"receipt_boundary_{name}_missing")
    decision = str(record.get("reentry_intake_decision", "block"))
    action = str(record.get("intake_action", "add_barrier_potential"))
    if decision not in DECISION_TO_ACTION:
        blockers.append("receipt_decision_invalid")
        decision = "block"
    expected_action = DECISION_TO_ACTION[decision]
    if action != expected_action:
        blockers.append("receipt_action_decision_mismatch")
        action = expected_action
    potential = dict(_m(record.get("next_cycle_candidate_potential")))
    delta = _int(potential.get("path_weight_delta"))
    probe = potential.get("probe_potential_required") is True
    barrier = potential.get("barrier_potential_required") is True
    barrier_blocks = potential.get("barrier_blocks_ready_weight") is True
    if decision == "accept":
        if delta <= 0:
            blockers.append("accept_receipt_without_positive_path_weight_delta")
        if probe or barrier or barrier_blocks:
            blockers.append("accept_receipt_has_probe_or_barrier_potential")
    elif decision == "hold":
        if delta != 0:
            blockers.append("hold_receipt_has_path_weight_delta")
        if not probe:
            blockers.append("hold_receipt_without_probe_potential")
        if barrier or barrier_blocks:
            blockers.append("hold_receipt_has_barrier_potential")
    elif decision == "block":
        if delta != 0:
            blockers.append("block_receipt_has_path_weight_delta")
        if probe:
            blockers.append("block_receipt_has_probe_potential")
        if not barrier or not barrier_blocks:
            blockers.append("block_receipt_without_barrier_block")
    if str(record.get("prev_record_digest", "")) == "CORRUPT_PREVIOUS_LEDGER_LINE":
        warnings.append("previous_receipt_digest_corrupt_marker_visible")
    return decision, ACTION_TO_BRIDGE_MODE[action], potential


def _bridge_packet(record: Mapping[str, Any], decision: str, mode: str, potential: Mapping[str, Any]) -> dict[str, Any]:
    if decision == "accept":
        candidate_status = "weighted_candidate"
    elif decision == "hold":
        candidate_status = "probe_only_candidate"
    else:
        candidate_status = "blocked_candidate"
    packet = {
        "version": "physical_quantum_qi_next_cycle_candidate_weighting_bridge_packet_v10_8",
        "physical_quantum_qi_next_cycle_candidate_weighting_bridge_considered": True,
        "source_reentry_intake_decision": decision,
        "source_intake_action": str(record.get("intake_action", "add_barrier_potential")),
        "bridge_mode": mode,
        "next_cycle_candidate_status": candidate_status,
        "candidate_weighting": {
            "path_weight_delta": _int(potential.get("path_weight_delta")),
            "probe_potential_required": potential.get("probe_potential_required") is True,
            "barrier_potential_required": potential.get("barrier_potential_required") is True,
            "barrier_blocks_ready_weight": potential.get("barrier_blocks_ready_weight") is True,
        },
        "source_digests": {
            "reentry_intake_receipt_record": str(record.get("record_digest", _sha(dict(record))))
        },
        "boundary": {
            "next_cycle_candidate_weighting_bridge_only": True,
            "next_cycle_candidate_weighting_only": True,
            "does_not_execute_path": True,
            "does_not_run_runner": True,
            "does_not_start_next_cycle": True,
            "does_not_commit_plan": True,
            "does_not_consume_memory": True,
            "does_not_authorize_execution": True,
            "candidate_weighting_not_truth": True,
            "bridge_does_not_mutate_receipt_ledger": True,
            "barrier_potential_can_only_block_or_probe": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    packet["bridge_packet_digest"] = _sha(packet)
    return packet


def build_physical_quantum_qi_next_cycle_candidate_weighting_bridge(
    *,
    runtime_context: Mapping[str, Any],
    next_cycle_candidate_weighting_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiNextCycleCandidateWeightingBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(next_cycle_candidate_weighting_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ledger_path = root / "physical_quantum_qi_path_integral_reentry_intake_receipt_ledger.jsonl"
    packet_path = root / "physical_quantum_qi_next_cycle_candidate_weighting_bridge_packet.json"
    summary_path = root / "physical_quantum_qi_next_cycle_candidate_weighting_bridge_summary.json"
    receipt_path = root / "physical_quantum_qi_next_cycle_candidate_weighting_bridge_receipt.json"
    audit_path = root / "physical_quantum_qi_next_cycle_candidate_weighting_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_next_cycle_candidate_weighting_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_next_cycle_candidate_weighting_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_next_cycle_candidate_weighting_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_next_cycle_candidate_weighting_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_next_cycle_candidate_weighting_bridge_license_not_ready")
    for name in [
        "receipt_ledger_read_allowed",
        "bridge_packet_write_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    record = _read_latest_jsonl(ledger_path, blockers)
    decision, mode, potential = _validate_record(record, blockers, warnings)
    packet: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _bridge_packet(record, decision, mode, potential)
        summary = {
            "version": "physical_quantum_qi_next_cycle_candidate_weighting_bridge_summary_v10_8",
            "source_reentry_intake_decision": decision,
            "bridge_mode": mode,
            "next_cycle_candidate_status": packet["next_cycle_candidate_status"],
            "bridge_packet_digest": packet["bridge_packet_digest"],
            "boundary": {
                "summary_only": True,
                "does_not_execute_path": True,
                "does_not_run_runner": True,
                "does_not_start_next_cycle": True,
                "does_not_authorize_execution": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(packet_path, packet)
        _write_json(summary_path, summary)
        written = True

    status = "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_NEXT_CYCLE_CANDIDATE_WEIGHTING_BRIDGE_BLOCKED"
    packet_id = "physical-quantum-qi-next-cycle-candidate-weighting-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_next_cycle_candidate_weighting_bridge_v10_8",
        "status": status,
        "packet_id": packet_id,
        "source_reentry_intake_decision": decision,
        "bridge_mode": mode,
        "bridge_packet_written": written,
        "bridge_packet_digest": _sha(packet),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiNextCycleCandidateWeightingBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_next_cycle_candidate_weighting_bridge_v10_8",
        status,
        packet_id,
        str(root),
        decision,
        mode,
        str(packet_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
