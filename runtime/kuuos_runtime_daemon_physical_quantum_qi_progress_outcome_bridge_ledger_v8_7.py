#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


KNOWN_EXECUTION_CLASSES = {
    "progress_hold_with_exit",
    "progress_runner_completed",
    "progress_runner_blocked",
    "physical_qi_delegated_runner_blocked",
    "not_run",
}

KNOWN_PROGRESS_CLASSES = {
    "safe_progress_continue",
    "observe_with_progress_obligation",
    "retry_with_rebalance_probe",
    "hold_with_review_exit",
    "progress_gap_detected",
}


@dataclass(frozen=True)
class PhysicalQuantumQiProgressOutcomeBridgeLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    progress_class: str
    execution_class: str
    progress_outcome_class: str
    physical_ledger_path: str
    qi_ledger_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    physical_ledger_appended: bool
    qi_ledger_appended: bool
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


def _classify(receipt: Mapping[str, Any], runner_packet: Mapping[str, Any]) -> str:
    execution = str(receipt.get("execution_class", "not_run"))
    progress_class = str(runner_packet.get("progress_class", receipt.get("progress_class", "unknown")))
    if execution == "progress_runner_completed":
        if progress_class == "progress_gap_detected":
            return "gap_probe_completed"
        return "progress_completed"
    if execution == "progress_hold_with_exit":
        return "exit_preserved_hold"
    if execution in {"progress_runner_blocked", "physical_qi_delegated_runner_blocked"}:
        return "progress_blocked"
    return "progress_not_run"


def _record(receipt: Mapping[str, Any], runner_packet: Mapping[str, Any], physical_prev: str, qi_prev: str) -> dict[str, Any]:
    rec = {
        "version": "physical_quantum_qi_progress_outcome_record_v8_7",
        "record_type": "progress_outcome",
        "source": "physical_quantum_qi",
        "runner_mode": str(runner_packet.get("runner_mode", receipt.get("runner_mode", "unknown"))),
        "progress_class": str(runner_packet.get("progress_class", receipt.get("progress_class", "unknown"))),
        "progress_action": str(runner_packet.get("progress_action", "unknown")),
        "execution_class": str(receipt.get("execution_class", "unknown")),
        "runner_status": str(receipt.get("status", "unknown")),
        "delegated_runner_status": str(receipt.get("delegated_runner_status", "unknown")),
        "delegated_runner_invoked": receipt.get("delegated_runner_invoked") is True,
        "progress_outcome_class": _classify(receipt, runner_packet),
        "physical_quantum_qi_motion_bias_used": receipt.get("physical_quantum_qi_motion_bias_used") is True,
        "path_integral_candidate_weighting_preserved": receipt.get("path_integral_candidate_weighting_preserved") is True,
        "progress_required": runner_packet.get("progress_required") is True,
        "review_exit_required": runner_packet.get("review_exit_required") is True,
        "small_probe_required": runner_packet.get("small_probe_required") is True,
        "runner_packet_digest": _sha(dict(runner_packet)),
        "physical_runner_receipt_digest": _sha(dict(receipt)),
        "prev_physical_record_digest": physical_prev,
        "prev_qi_record_digest": qi_prev,
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def _summary(record: Mapping[str, Any]) -> dict[str, Any]:
    summary = {
        "version": "physical_quantum_qi_progress_outcome_summary_v8_7",
        "source": "physical_quantum_qi",
        "progress_class": str(record.get("progress_class", "unknown")),
        "execution_class": str(record.get("execution_class", "unknown")),
        "progress_outcome_class": str(record.get("progress_outcome_class", "unknown")),
        "delegated_runner_invoked": record.get("delegated_runner_invoked") is True,
        "path_integral_candidate_weighting_preserved": record.get("path_integral_candidate_weighting_preserved") is True,
        "record_digest": str(record.get("record_digest", "")),
        "epoch": int(time.time()),
    }
    summary["summary_digest"] = _sha(summary)
    return summary


def build_physical_quantum_qi_progress_outcome_bridge_ledger(*, runtime_context: Mapping[str, Any], bridge_ledger_license: Mapping[str, Any]) -> PhysicalQuantumQiProgressOutcomeBridgeLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(bridge_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    runner_packet_path = root / "qi_progress_aware_runner_packet.json"
    receipt_in_path = root / "physical_quantum_qi_progress_aware_integrated_runner_receipt.json"
    physical_ledger_path = root / "physical_quantum_qi_progress_outcome_ledger.jsonl"
    qi_ledger_path = root / "qi_progress_outcome_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_progress_outcome_summary.json"
    receipt_path = root / "physical_quantum_qi_progress_outcome_bridge_ledger_receipt.json"
    audit_path = root / "physical_quantum_qi_progress_outcome_bridge_ledger_audit.jsonl"

    if ctx.get("physical_quantum_qi_progress_outcome_bridge_ledger_enabled") is not True:
        blockers.append("physical_quantum_qi_progress_outcome_bridge_ledger_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_progress_outcome_bridge_ledger") is not True:
        blockers.append("apply_physical_quantum_qi_progress_outcome_bridge_ledger_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_PROGRESS_OUTCOME_BRIDGE_LEDGER_LICENSE_READY":
        blockers.append("physical_quantum_qi_progress_outcome_bridge_ledger_license_not_ready")
    for name in ["runner_packet_read_allowed", "physical_runner_receipt_read_allowed", "physical_ledger_append_allowed", "qi_ledger_append_allowed", "summary_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    runner_packet = _read_json(runner_packet_path)
    receipt_in = _read_json(receipt_in_path)
    if not runner_packet:
        blockers.append("qi_progress_aware_runner_packet_missing_or_invalid")
    if not receipt_in:
        blockers.append("physical_quantum_qi_progress_aware_integrated_runner_receipt_missing_or_invalid")
    progress_class = str(runner_packet.get("progress_class", receipt_in.get("progress_class", "unknown"))) if (runner_packet or receipt_in) else "unknown"
    execution_class = str(receipt_in.get("execution_class", "unknown")) if receipt_in else "unknown"
    if progress_class not in KNOWN_PROGRESS_CLASSES and (runner_packet or receipt_in):
        blockers.append("progress_class_not_allowlisted")
    if execution_class not in KNOWN_EXECUTION_CLASSES and receipt_in:
        warnings.append("execution_class_not_known")
    if runner_packet and runner_packet.get("physical_quantum_qi_motion_bias_used") is not True:
        blockers.append("physical_quantum_qi_motion_bias_used_not_true")
    if runner_packet and runner_packet.get("progress_required") is not True:
        blockers.append("progress_required_not_true")
    if receipt_in and receipt_in.get("physical_quantum_qi_motion_bias_used") is not True:
        blockers.append("physical_qi_receipt_origin_missing")
    if receipt_in and receipt_in.get("path_integral_candidate_weighting_preserved") is not True:
        blockers.append("path_integral_candidate_weighting_not_preserved")
    if runner_packet and receipt_in and str(runner_packet.get("runner_mode", "unknown")) != str(receipt_in.get("runner_mode", "unknown")):
        blockers.append("runner_mode_mismatch")

    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    physical_appended = False
    qi_appended = False
    outcome = "unknown"
    if not blockers:
        record = _record(receipt_in, runner_packet, _last_digest(physical_ledger_path), _last_digest(qi_ledger_path))
        outcome = str(record["progress_outcome_class"])
        summary = _summary(record)
        _append_jsonl(physical_ledger_path, record)
        physical_appended = True
        _append_jsonl(qi_ledger_path, record)
        qi_appended = True
        _write_json(summary_path, summary)

    status = "PHYSICAL_QUANTUM_QI_PROGRESS_OUTCOME_BRIDGE_LEDGER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_PROGRESS_OUTCOME_BRIDGE_LEDGER_BLOCKED"
    packet_id = "physical-quantum-qi-progress-outcome-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_progress_outcome_bridge_ledger_v8_7",
        "status": status,
        "packet_id": packet_id,
        "progress_class": progress_class,
        "execution_class": execution_class,
        "progress_outcome_class": outcome,
        "physical_ledger_appended": physical_appended,
        "qi_ledger_appended": qi_appended,
        "outcome_record_digest": _sha(record),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return PhysicalQuantumQiProgressOutcomeBridgeLedgerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_progress_outcome_bridge_ledger_v8_7",
        status,
        packet_id,
        str(root),
        progress_class,
        execution_class,
        outcome,
        str(physical_ledger_path),
        str(qi_ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        physical_appended,
        qi_appended,
        blockers,
        warnings,
    )
