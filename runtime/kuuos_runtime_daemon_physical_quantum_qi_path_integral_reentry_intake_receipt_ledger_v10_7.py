#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


DECISIONS = {"accept", "hold", "block"}
INTAKE_ACTION_BY_DECISION = {
    "accept": "reinforce_path_weight",
    "hold": "open_probe_potential",
    "block": "add_barrier_potential",
}
REQUIRED_INTAKE_BOUNDARY_FLAGS = (
    "reentry_intake_validation_only",
    "does_not_execute_path",
    "does_not_run_runner",
    "does_not_commit_plan",
    "does_not_consume_memory",
    "does_not_authorize_execution",
    "candidate_weighting_not_truth",
    "barrier_potential_can_only_block_or_probe",
    "fail_closed_on_boundary_loss",
)


@dataclass(frozen=True)
class PhysicalQuantumQiPathIntegralReentryIntakeReceiptLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    reentry_intake_decision: str
    intake_action: str
    accepted_count: int
    held_count: int
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
    last = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            last = line
    if not last:
        return "GENESIS"
    try:
        payload = json.loads(last)
    except json.JSONDecodeError:
        return "CORRUPT_PREVIOUS_LEDGER_LINE"
    return str(payload.get("record_digest", _sha(payload)))


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _counts(packet: Mapping[str, Any]) -> dict[str, int]:
    raw = _m(packet.get("counts"))
    return {
        "reinforce_path_weight": _int(raw.get("reinforce_path_weight")),
        "open_probe_potential": _int(raw.get("open_probe_potential")),
        "add_barrier_potential": _int(raw.get("add_barrier_potential")),
    }


def _as_list(value: Any) -> list[str]:
    return [str(item) for item in value] if isinstance(value, list) else []


def _validate_intake_packet(packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[str, str, dict[str, int]]:
    if not packet:
        blockers.append("physical_quantum_qi_path_integral_reentry_intake_decision_packet_missing_or_invalid")
        return "block", "add_barrier_potential", {"reinforce_path_weight": 0, "open_probe_potential": 0, "add_barrier_potential": 0}
    if packet.get("physical_quantum_qi_path_integral_reentry_intake_considered") is not True:
        blockers.append("physical_quantum_qi_path_integral_reentry_intake_considered_not_true")
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_INTAKE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"{name}_missing")
    decision = str(packet.get("reentry_intake_decision", "block"))
    if decision not in DECISIONS:
        blockers.append("reentry_intake_decision_invalid")
        decision = "block"
    counts = _counts(packet)
    packet_blockers = _as_list(packet.get("blockers"))
    packet_warnings = _as_list(packet.get("warnings"))
    warnings.extend(packet_warnings)
    if decision == "accept":
        if counts["reinforce_path_weight"] <= 0:
            blockers.append("accept_without_reinforce_path_weight")
        if counts["open_probe_potential"] > 0:
            blockers.append("accept_with_probe_potential")
        if counts["add_barrier_potential"] > 0:
            blockers.append("accept_with_barrier_potential")
        if packet_blockers:
            blockers.append("accept_with_source_blockers")
        if packet_warnings:
            blockers.append("accept_with_source_warnings")
    elif decision == "hold":
        if counts["add_barrier_potential"] > 0:
            blockers.append("hold_with_barrier_potential")
        if packet_blockers:
            blockers.append("hold_with_source_blockers")
        if counts["open_probe_potential"] <= 0 and not packet_warnings:
            blockers.append("hold_without_probe_or_warning")
    elif decision == "block":
        if counts["add_barrier_potential"] <= 0 and not packet_blockers:
            blockers.append("block_without_barrier_or_source_blocker")
    return decision, INTAKE_ACTION_BY_DECISION[decision], counts


def _potential(decision: str, counts: Mapping[str, int]) -> dict[str, Any]:
    if decision == "accept":
        return {
            "path_weight_delta": int(counts.get("reinforce_path_weight", 0)),
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
        }
    if decision == "hold":
        return {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
        }
    return {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
    }


def _record(packet: Mapping[str, Any], decision: str, action: str, counts: Mapping[str, int], prev_digest: str) -> dict[str, Any]:
    rec = {
        "version": "physical_quantum_qi_path_integral_reentry_intake_receipt_record_v10_7",
        "record_type": "physical_quantum_qi_path_integral_reentry_intake_receipt",
        "reentry_intake_decision": decision,
        "intake_action": action,
        "counts": dict(counts),
        "next_cycle_candidate_potential": _potential(decision, counts),
        "source_intake_decision_packet_digest": _sha(dict(packet)),
        "prev_record_digest": prev_digest,
        "boundary": {
            "receipt_ledger_only": True,
            "reentry_intake_receipt_only": True,
            "does_not_execute_path": True,
            "does_not_run_runner": True,
            "does_not_commit_plan": True,
            "does_not_consume_memory": True,
            "does_not_authorize_execution": True,
            "candidate_weighting_not_truth": True,
            "barrier_potential_can_only_block_or_probe": True,
            "receipt_does_not_authorize_execution": True,
            "replayable_receipt": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def _summary(record: Mapping[str, Any]) -> dict[str, Any]:
    decision = str(record.get("reentry_intake_decision", "block"))
    summary = {
        "version": "physical_quantum_qi_path_integral_reentry_intake_receipt_summary_v10_7",
        "latest_reentry_intake_decision": decision,
        "latest_intake_action": str(record.get("intake_action", "add_barrier_potential")),
        "accepted_count": 1 if decision == "accept" else 0,
        "held_count": 1 if decision == "hold" else 0,
        "blocked_count": 1 if decision == "block" else 0,
        "latest_record_digest": str(record.get("record_digest", "")),
        "source_intake_decision_packet_digest": str(record.get("source_intake_decision_packet_digest", "")),
        "boundary": {
            "summary_only": True,
            "does_not_execute_path": True,
            "does_not_run_runner": True,
            "does_not_commit_plan": True,
            "does_not_consume_memory": True,
            "does_not_authorize_execution": True,
            "candidate_weighting_not_truth": True,
        },
        "epoch": int(time.time()),
    }
    summary["summary_digest"] = _sha(summary)
    return summary


def build_physical_quantum_qi_path_integral_reentry_intake_receipt_ledger(
    *,
    runtime_context: Mapping[str, Any],
    reentry_intake_receipt_ledger_license: Mapping[str, Any],
) -> PhysicalQuantumQiPathIntegralReentryIntakeReceiptLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(reentry_intake_receipt_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    intake_path = root / "physical_quantum_qi_path_integral_reentry_intake_decision_packet.json"
    ledger_path = root / "physical_quantum_qi_path_integral_reentry_intake_receipt_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_path_integral_reentry_intake_receipt_summary.json"
    receipt_path = root / "physical_quantum_qi_path_integral_reentry_intake_receipt_ledger_receipt.json"
    audit_path = root / "physical_quantum_qi_path_integral_reentry_intake_receipt_ledger_audit.jsonl"

    if ctx.get("physical_quantum_qi_path_integral_reentry_intake_receipt_ledger_enabled") is not True:
        blockers.append("physical_quantum_qi_path_integral_reentry_intake_receipt_ledger_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_path_integral_reentry_intake_receipt_ledger") is not True:
        blockers.append("apply_physical_quantum_qi_path_integral_reentry_intake_receipt_ledger_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_RECEIPT_LEDGER_LICENSE_READY":
        blockers.append("physical_quantum_qi_path_integral_reentry_intake_receipt_ledger_license_not_ready")
    for name in [
        "reentry_intake_packet_read_allowed",
        "receipt_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    intake = _read_json(intake_path)
    decision, action, counts = _validate_intake_packet(intake, blockers, warnings)

    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    if not blockers:
        record = _record(intake, decision, action, counts, _last_digest(ledger_path))
        _append_jsonl(ledger_path, record)
        summary = _summary(record)
        _write_json(summary_path, summary)
        appended = True

    accepted = 1 if appended and decision == "accept" else 0
    held = 1 if appended and decision == "hold" else 0
    blocked = 1 if appended and decision == "block" else 0
    status = "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_RECEIPT_LEDGER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_RECEIPT_LEDGER_BLOCKED"
    packet_id = "physical-quantum-qi-reentry-intake-receipt-ledger-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_path_integral_reentry_intake_receipt_ledger_v10_7",
        "status": status,
        "packet_id": packet_id,
        "reentry_intake_decision": decision,
        "intake_action": action,
        "accepted_count": accepted,
        "held_count": held,
        "blocked_count": blocked,
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
    return PhysicalQuantumQiPathIntegralReentryIntakeReceiptLedgerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_path_integral_reentry_intake_receipt_ledger_v10_7",
        status,
        packet_id,
        str(root),
        decision,
        action,
        accepted,
        held,
        blocked,
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        appended,
        blockers,
        warnings,
    )
