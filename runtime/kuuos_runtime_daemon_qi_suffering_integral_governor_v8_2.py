#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


PRESSURE_WEIGHT = {
    "suffering_pressure_relieved": 0,
    "suffering_pressure_low": 1,
    "suffering_pressure_moderate": 3,
    "suffering_pressure_high": 6,
}

PROGRESS_OUTCOME_WEIGHT = {
    "progress_completed": -3,
    "gap_probe_completed": -2,
    "exit_preserved_hold": 2,
    "progress_blocked": 4,
    "progress_not_run": 3,
}

ALLOWED_INTEGRAL_CLASSES = {
    "progress_pain_acceptable",
    "staying_suffering_dominates",
    "rebalance_required",
    "hold_requires_exit",
    "integral_relief_observed",
}


@dataclass(frozen=True)
class QiSufferingIntegralGovernorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    suffering_integral_class: str
    transient_progress_pain: int
    stagnant_safety_burden: int
    recommended_integral_action: str
    integral_packet_path: str
    receipt_path: str
    audit_path: str
    integral_packet_written: bool
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


def _outcome_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        k = str(row.get("progress_outcome_class", "unknown"))
        counts[k] = counts.get(k, 0) + 1
    return counts


def _burdens(suffering: Mapping[str, Any], rows: list[dict[str, Any]]) -> tuple[int, int, int, dict[str, int]]:
    pressure_class = str(suffering.get("suffering_pressure_class", "suffering_pressure_moderate"))
    pressure_weight = PRESSURE_WEIGHT.get(pressure_class, 3)
    counts = _outcome_counts(rows)
    transient = counts.get("gap_probe_completed", 0) + counts.get("progress_completed", 0)
    stagnant = pressure_weight
    net = pressure_weight
    for outcome, count in counts.items():
        weight = PROGRESS_OUTCOME_WEIGHT.get(outcome, 0)
        net += weight * count
        if weight > 0:
            stagnant += weight * count
        elif weight < 0:
            transient += abs(weight) * count
    return transient, stagnant, net, counts


def _classify(suffering: Mapping[str, Any], rows: list[dict[str, Any]]) -> tuple[str, str, list[str], int, int, int, dict[str, int]]:
    transient, stagnant, net, counts = _burdens(suffering, rows)
    pressure_class = str(suffering.get("suffering_pressure_class", "unknown"))
    reasons: list[str] = []
    if counts.get("progress_completed", 0) + counts.get("gap_probe_completed", 0) > 0 and net <= 0:
        reasons.append("progress_relief_reduces_integral")
        return "integral_relief_observed", "continue_light_progress", reasons, transient, stagnant, net, counts
    if counts.get("exit_preserved_hold", 0) >= 2 and counts.get("progress_completed", 0) == 0:
        reasons.append("hold_preserves_exit_but_does_not_reduce_integral")
        return "hold_requires_exit", "force_review_exit_or_small_probe", reasons, transient, stagnant, net, counts
    if pressure_class == "suffering_pressure_high" or stagnant >= transient + 4:
        reasons.append("staying_suffering_exceeds_transient_progress_pain")
        return "staying_suffering_dominates", "accept_small_progress_pain", reasons, transient, stagnant, net, counts
    if counts.get("progress_blocked", 0) >= 2:
        reasons.append("progress_attempt_blocked_repeatedly")
        return "rebalance_required", "rebalance_before_next_probe", reasons, transient, stagnant, net, counts
    reasons.append("transient_progress_pain_acceptable_under_integral")
    return "progress_pain_acceptable", "continue_small_probe", reasons, transient, stagnant, net, counts


def _packet(suffering: Mapping[str, Any], rows: list[dict[str, Any]], window: int) -> dict[str, Any]:
    sample = _window(rows, window)
    integral_class, action, reasons, transient, stagnant, net, counts = _classify(suffering, sample)
    return {
        "version": "qi_suffering_integral_packet_v8_2",
        "suffering_integral_considered": True,
        "transient_progress_pain_can_be_acceptable": True,
        "staying_can_increase_total_suffering": True,
        "suffering_integral_class": integral_class,
        "recommended_integral_action": action,
        "transient_progress_pain": transient,
        "stagnant_safety_burden": stagnant,
        "net_suffering_integral_proxy": net,
        "window_records_used": len(sample),
        "progress_outcome_counts": counts,
        "integral_reason_codes": reasons,
        "source_suffering_digest": _sha(dict(suffering)),
        "source_progress_window_digest": _sha(sample),
        "boundary": {
            "assessment_only": True,
            "does_not_run_runner": True,
            "does_not_ignore_transient_pain": True,
            "does_not_equate_short_term_pain_with_total_harm": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_suffering_integral_governor(*, runtime_context: Mapping[str, Any], suffering_integral_license: Mapping[str, Any]) -> QiSufferingIntegralGovernorResult:
    ctx = _m(runtime_context)
    lic = _m(suffering_integral_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    suffering_path = root / "qi_stagnant_safety_suffering_packet.json"
    progress_path = root / "qi_progress_outcome_ledger.jsonl"
    packet_path = root / "qi_suffering_integral_packet.json"
    receipt_path = root / "qi_suffering_integral_governor_receipt.json"
    audit_path = root / "qi_suffering_integral_governor_audit.jsonl"

    if ctx.get("qi_suffering_integral_governor_enabled") is not True:
        blockers.append("qi_suffering_integral_governor_enabled_not_true")
    if ctx.get("apply_qi_suffering_integral_governor") is not True:
        blockers.append("apply_qi_suffering_integral_governor_not_true")
    if lic.get("license_status") != "QI_SUFFERING_INTEGRAL_GOVERNOR_LICENSE_READY":
        blockers.append("qi_suffering_integral_governor_license_not_ready")
    for name in ["suffering_packet_read_allowed", "progress_outcome_ledger_read_allowed", "integral_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    window = _i(ctx.get("integral_window_records", 6), 6)
    if window < 1:
        blockers.append("integral_window_records_invalid")
        window = 0
    if window > 50:
        warnings.append("integral_window_records_capped_to_50")
        window = 50

    suffering = _read_json(suffering_path)
    progress_rows = [r for r in _read_jsonl(progress_path) if r.get("record_type") == "progress_outcome"]
    if not suffering:
        blockers.append("qi_stagnant_safety_suffering_packet_missing_or_invalid")
    if not progress_rows:
        warnings.append("progress_outcome_ledger_empty_or_missing")
    if suffering and suffering.get("suffering_pressure_considered") is not True:
        blockers.append("suffering_pressure_considered_not_true")

    packet: dict[str, Any] = {}
    written = False
    integral_class = "unknown"
    action = "unknown"
    transient = 0
    stagnant = 0
    if not blockers:
        packet = _packet(suffering, progress_rows, window)
        integral_class = str(packet["suffering_integral_class"])
        action = str(packet["recommended_integral_action"])
        transient = int(packet["transient_progress_pain"])
        stagnant = int(packet["stagnant_safety_burden"])
        if integral_class not in ALLOWED_INTEGRAL_CLASSES:
            blockers.append("suffering_integral_class_not_allowlisted")
        else:
            _write_json(packet_path, packet)
            written = True

    status = "QI_SUFFERING_INTEGRAL_GOVERNOR_READY" if not blockers else "QI_SUFFERING_INTEGRAL_GOVERNOR_BLOCKED"
    packet_id = "qi-suffering-integral-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_suffering_integral_governor_v8_2",
        "status": status,
        "packet_id": packet_id,
        "suffering_integral_class": integral_class,
        "recommended_integral_action": action,
        "transient_progress_pain": transient,
        "stagnant_safety_burden": stagnant,
        "integral_packet_written": written,
        "integral_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiSufferingIntegralGovernorResult(
        "kuuos_runtime_daemon_qi_suffering_integral_governor_v8_2",
        status,
        packet_id,
        str(root),
        integral_class,
        transient,
        stagnant,
        action,
        str(packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
