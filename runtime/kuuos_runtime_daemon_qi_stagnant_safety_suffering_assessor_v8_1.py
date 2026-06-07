#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


STAGNANT_PROGRESS_OUTCOMES = {
    "exit_preserved_hold",
    "progress_blocked",
    "progress_not_run",
}

RELIEVING_PROGRESS_OUTCOMES = {
    "progress_completed",
    "gap_probe_completed",
}

ALLOWED_PRESSURE_CLASSES = {
    "suffering_pressure_low",
    "suffering_pressure_moderate",
    "suffering_pressure_high",
    "suffering_pressure_relieved",
}


@dataclass(frozen=True)
class QiStagnantSafetySufferingAssessorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    suffering_pressure_class: str
    stagnant_safety_count: int
    relieving_progress_count: int
    recommended_relief_action: str
    suffering_packet_path: str
    receipt_path: str
    audit_path: str
    suffering_packet_written: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _i(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


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


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _window(rows: list[dict[str, Any]], size: int) -> list[dict[str, Any]]:
    return rows[-size:] if size > 0 else []


def _counts(rows: list[dict[str, Any]]) -> tuple[int, int, int]:
    stagnant = 0
    relief = 0
    hold_exit = 0
    for row in rows:
        outcome = str(row.get("progress_outcome_class", "unknown"))
        if outcome in STAGNANT_PROGRESS_OUTCOMES:
            stagnant += 1
        if outcome in RELIEVING_PROGRESS_OUTCOMES:
            relief += 1
        if outcome == "exit_preserved_hold":
            hold_exit += 1
    return stagnant, relief, hold_exit


def _pressure(stagnant: int, relief: int, hold_exit: int, window_len: int) -> tuple[str, str, list[str]]:
    reasons: list[str] = []
    if relief > 0 and stagnant == 0:
        reasons.append("recent_progress_relieved_pressure")
        return "suffering_pressure_relieved", "continue_light_progress", reasons
    if window_len == 0:
        reasons.append("no_recent_progress_outcomes")
        return "suffering_pressure_moderate", "open_small_probe", reasons
    if stagnant >= 4 and relief == 0:
        reasons.append("repeated_safety_without_progress")
        if hold_exit >= 2:
            reasons.append("hold_exit_repeated_without_release")
        return "suffering_pressure_high", "force_review_exit_or_small_probe", reasons
    if stagnant >= 2 and relief == 0:
        reasons.append("safety_stagnation_accumulating")
        return "suffering_pressure_moderate", "open_small_probe", reasons
    reasons.append("stagnation_pressure_low")
    return "suffering_pressure_low", "maintain_progress_obligation", reasons


def _packet(progress_rows: list[dict[str, Any]], safety: Mapping[str, Any], window_size: int) -> dict[str, Any]:
    sample = _window(progress_rows, window_size)
    stagnant, relief, hold_exit = _counts(sample)
    pressure, action, reasons = _pressure(stagnant, relief, hold_exit, len(sample))
    return {
        "version": "qi_stagnant_safety_suffering_packet_v8_1",
        "suffering_pressure_considered": True,
        "safety_without_progress_increases_suffering": True,
        "suffering_pressure_class": pressure,
        "recommended_relief_action": action,
        "stagnant_safety_count": stagnant,
        "relieving_progress_count": relief,
        "hold_exit_count": hold_exit,
        "window_records_used": len(sample),
        "suffering_reason_codes": reasons,
        "source_progress_window_digest": _sha(sample),
        "source_safety_digest": _sha(dict(safety)),
        "boundary": {
            "assessment_only": True,
            "does_not_run_runner": True,
            "progress_obligation_preserved": True,
            "stagnant_safety_not_equivalent_to_relief": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_stagnant_safety_suffering_assessor(*, runtime_context: Mapping[str, Any], suffering_assessor_license: Mapping[str, Any]) -> QiStagnantSafetySufferingAssessorResult:
    ctx = _m(runtime_context)
    lic = _m(suffering_assessor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    progress_path = root / "qi_progress_outcome_ledger.jsonl"
    safety_path = root / "qi_progress_bearing_safety_packet.json"
    packet_path = root / "qi_stagnant_safety_suffering_packet.json"
    receipt_path = root / "qi_stagnant_safety_suffering_assessor_receipt.json"
    audit_path = root / "qi_stagnant_safety_suffering_assessor_audit.jsonl"

    if ctx.get("qi_stagnant_safety_suffering_assessor_enabled") is not True:
        blockers.append("qi_stagnant_safety_suffering_assessor_enabled_not_true")
    if ctx.get("apply_qi_stagnant_safety_suffering_assessor") is not True:
        blockers.append("apply_qi_stagnant_safety_suffering_assessor_not_true")
    if lic.get("license_status") != "QI_STAGNANT_SAFETY_SUFFERING_ASSESSOR_LICENSE_READY":
        blockers.append("qi_stagnant_safety_suffering_assessor_license_not_ready")
    for name in ["progress_outcome_ledger_read_allowed", "safety_packet_read_allowed", "suffering_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    window = _i(ctx.get("suffering_window_records", 5), 5)
    if window < 1:
        blockers.append("suffering_window_records_invalid")
        window = 0
    if window > 50:
        warnings.append("suffering_window_records_capped_to_50")
        window = 50

    progress_rows = [r for r in _read_jsonl(progress_path) if r.get("record_type") == "progress_outcome"]
    safety = _read_json(safety_path)
    if not progress_rows:
        warnings.append("progress_outcome_ledger_empty_or_missing")
    if not safety:
        blockers.append("qi_progress_bearing_safety_packet_missing_or_invalid")
    if safety and safety.get("progress_required") is not True:
        blockers.append("progress_required_not_true")

    packet: dict[str, Any] = {}
    written = False
    pressure = "unknown"
    action = "unknown"
    stagnant = 0
    relief = 0
    if not blockers:
        packet = _packet(progress_rows, safety, window)
        pressure = str(packet["suffering_pressure_class"])
        action = str(packet["recommended_relief_action"])
        stagnant = int(packet["stagnant_safety_count"])
        relief = int(packet["relieving_progress_count"])
        if pressure not in ALLOWED_PRESSURE_CLASSES:
            blockers.append("suffering_pressure_class_not_allowlisted")
        else:
            _write_json(packet_path, packet)
            written = True

    status = "QI_STAGNANT_SAFETY_SUFFERING_ASSESSOR_READY" if not blockers else "QI_STAGNANT_SAFETY_SUFFERING_ASSESSOR_BLOCKED"
    packet_id = "qi-stagnant-safety-suffering-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_stagnant_safety_suffering_assessor_v8_1",
        "status": status,
        "packet_id": packet_id,
        "suffering_pressure_class": pressure,
        "recommended_relief_action": action,
        "stagnant_safety_count": stagnant,
        "relieving_progress_count": relief,
        "suffering_packet_written": written,
        "suffering_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiStagnantSafetySufferingAssessorResult(
        "kuuos_runtime_daemon_qi_stagnant_safety_suffering_assessor_v8_1",
        status,
        packet_id,
        str(root),
        pressure,
        stagnant,
        relief,
        action,
        str(packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
