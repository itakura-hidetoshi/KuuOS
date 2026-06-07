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
class QiProgressOutcomeLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    progress_class: str
    execution_class: str
    progress_outcome_class: str
    outcome_ledger_path: str
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


def _classify(runner: Mapping[str, Any], packet: Mapping[str, Any]) -> str:
    execution = str(runner.get("execution_class", "not_run"))
    progress_class = str(packet.get("progress_class", runner.get("progress_class", "unknown")))
    if execution == "progress_runner_completed":
        if progress_class == "progress_gap_detected":
            return "gap_probe_completed"
        return "progress_completed"
    if execution == "progress_hold_with_exit":
        return "exit_preserved_hold"
    if execution == "progress_runner_blocked":
        return "progress_blocked"
    return "progress_not_run"


def _record(runner: Mapping[str, Any], packet: Mapping[str, Any], prev: str) -> dict[str, Any]:
    rec = {
        "version": "qi_progress_outcome_record_v8_0",
        "record_type": "progress_outcome",
        "runner_mode": str(packet.get("runner_mode", runner.get("runner_mode", "unknown"))),
        "progress_class": str(packet.get("progress_class", runner.get("progress_class", "unknown"))),
        "progress_action": str(packet.get("progress_action", "unknown")),
        "execution_class": str(runner.get("execution_class", "unknown")),
        "runner_status": str(runner.get("status", "unknown")),
        "integrated_runner_status": str(runner.get("integrated_runner_status", "unknown")),
        "integrated_runner_invoked": runner.get("integrated_runner_invoked") is True,
        "progress_outcome_class": _classify(runner, packet),
        "progress_required": packet.get("progress_required") is True,
        "review_exit_required": packet.get("review_exit_required") is True,
        "small_probe_required": packet.get("small_probe_required") is True,
        "runner_packet_digest": _sha(dict(packet)),
        "runner_receipt_digest": _sha(dict(runner)),
        "prev_record_digest": prev,
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def _summary(record: Mapping[str, Any]) -> dict[str, Any]:
    summary = {
        "version": "qi_progress_outcome_summary_v8_0",
        "progress_class": str(record.get("progress_class", "unknown")),
        "execution_class": str(record.get("execution_class", "unknown")),
        "progress_outcome_class": str(record.get("progress_outcome_class", "unknown")),
        "integrated_runner_invoked": record.get("integrated_runner_invoked") is True,
        "progress_required": record.get("progress_required") is True,
        "record_digest": str(record.get("record_digest", "")),
        "epoch": int(time.time()),
    }
    summary["summary_digest"] = _sha(summary)
    return summary


def build_qi_progress_outcome_ledger(*, runtime_context: Mapping[str, Any], progress_outcome_ledger_license: Mapping[str, Any]) -> QiProgressOutcomeLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(progress_outcome_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    runner_packet_path = root / "qi_progress_aware_runner_packet.json"
    runner_receipt_path = root / "qi_progress_aware_integrated_runner_receipt.json"
    ledger_path = root / "qi_progress_outcome_ledger.jsonl"
    summary_path = root / "qi_progress_outcome_summary.json"
    receipt_path = root / "qi_progress_outcome_ledger_receipt.json"
    audit_path = root / "qi_progress_outcome_ledger_audit.jsonl"

    if ctx.get("qi_progress_outcome_ledger_enabled") is not True:
        blockers.append("qi_progress_outcome_ledger_enabled_not_true")
    if ctx.get("apply_qi_progress_outcome_ledger") is not True:
        blockers.append("apply_qi_progress_outcome_ledger_not_true")
    if lic.get("license_status") != "QI_PROGRESS_OUTCOME_LEDGER_LICENSE_READY":
        blockers.append("qi_progress_outcome_ledger_license_not_ready")
    for name in ["runner_packet_read_allowed", "runner_receipt_read_allowed", "outcome_ledger_append_allowed", "summary_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    runner_packet = _read_json(runner_packet_path)
    runner = _read_json(runner_receipt_path)
    if not runner_packet:
        blockers.append("qi_progress_aware_runner_packet_missing_or_invalid")
    if not runner:
        blockers.append("qi_progress_aware_integrated_runner_receipt_missing_or_invalid")
    progress_class = str(runner_packet.get("progress_class", runner.get("progress_class", "unknown"))) if (runner_packet or runner) else "unknown"
    execution_class = str(runner.get("execution_class", "unknown")) if runner else "unknown"
    if runner_packet and runner_packet.get("progress_required") is not True:
        blockers.append("progress_required_not_true")
    if progress_class not in KNOWN_PROGRESS_CLASSES and (runner_packet or runner):
        blockers.append("progress_class_not_allowlisted")
    if execution_class not in KNOWN_EXECUTION_CLASSES and runner:
        warnings.append("execution_class_not_known")
    if runner and str(runner.get("status", "unknown")) not in {"QI_PROGRESS_AWARE_INTEGRATED_RUNNER_READY", "QI_PROGRESS_AWARE_INTEGRATED_RUNNER_BLOCKED"}:
        blockers.append("progress_aware_runner_receipt_status_invalid")
    if runner_packet and runner and str(runner.get("runner_mode", runner_packet.get("runner_mode"))) != str(runner_packet.get("runner_mode", "unknown")):
        blockers.append("runner_mode_mismatch")

    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    outcome = "unknown"
    if not blockers:
        record = _record(runner, runner_packet, _last_digest(ledger_path))
        outcome = str(record["progress_outcome_class"])
        summary = _summary(record)
        _append_jsonl(ledger_path, record)
        _write_json(summary_path, summary)
        appended = True

    status = "QI_PROGRESS_OUTCOME_LEDGER_READY" if not blockers else "QI_PROGRESS_OUTCOME_LEDGER_BLOCKED"
    packet_id = "qi-progress-outcome-ledger-" + _sha({"runner": runner, "packet": runner_packet, "record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_progress_outcome_ledger_v8_0",
        "status": status,
        "packet_id": packet_id,
        "progress_class": progress_class,
        "execution_class": execution_class,
        "progress_outcome_class": outcome,
        "ledger_appended": appended,
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

    return QiProgressOutcomeLedgerResult(
        "kuuos_runtime_daemon_qi_progress_outcome_ledger_v8_0",
        status,
        packet_id,
        str(root),
        progress_class,
        execution_class,
        outcome,
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        appended,
        blockers,
        warnings,
    )
