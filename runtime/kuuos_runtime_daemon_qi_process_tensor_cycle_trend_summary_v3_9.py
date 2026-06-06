#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from collections import Counter
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


@dataclass(frozen=True)
class QiProcessTensorCycleTrendSummaryResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    summary_path: str
    receipt_path: str
    audit_path: str
    trend_class: str
    recommendation: str
    reliability_score: float
    records_used: int
    trajectory_length: int
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


def _f(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


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


def _trajectory_length(packet: Mapping[str, Any]) -> int:
    raw = packet.get("trajectory", [])
    return len(raw) if isinstance(raw, list) else 0


def _collect_records(receipt: Mapping[str, Any], audit_rows: list[dict[str, Any]], max_records: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row in audit_rows:
        if isinstance(row.get("cycle_records"), list):
            records.extend([dict(item) for item in row["cycle_records"] if isinstance(item, Mapping)])
        else:
            records.append(dict(row))
    if isinstance(receipt.get("cycle_records"), list):
        records.extend([dict(item) for item in receipt["cycle_records"] if isinstance(item, Mapping)])
    elif receipt:
        records.append(dict(receipt))
    if max_records > 0:
        records = records[-max_records:]
    return records


def _rate(count: int, total: int) -> float:
    return round(count / total, 6) if total else 0.0


def _stop_reason(record: Mapping[str, Any]) -> str:
    return str(record.get("stop_reason_after_cycle") or record.get("stop_reason") or "unknown")


def _scheduled_status(record: Mapping[str, Any]) -> str:
    return str(record.get("scheduled_closed_loop_status") or record.get("final_scheduled_status") or "unknown")


def _summary(records: list[dict[str, Any]], trajectory_len: int) -> dict[str, Any]:
    total = len(records)
    stop_counts = Counter(_stop_reason(record) for record in records)
    scheduled_counts = Counter(_scheduled_status(record) for record in records)
    converged = stop_counts.get("converged", 0) + scheduled_counts.get("QI_SCHEDULED_CLOSED_LOOP_CONVERGED", 0)
    blocked = stop_counts.get("blocked", 0) + sum(count for status, count in scheduled_counts.items() if "BLOCKED" in status)
    hold = stop_counts.get("hold_overlay", 0)
    no_progress = stop_counts.get("no_progress", 0)
    cap = stop_counts.get("cycle_cap_reached", 0)
    continue_count = stop_counts.get("continue", 0)
    converged_rate = _rate(converged, total)
    blocked_rate = _rate(blocked, total)
    hold_rate = _rate(hold, total)
    no_progress_rate = _rate(no_progress, total)
    cap_rate = _rate(cap, total)
    continue_rate = _rate(continue_count, total)
    reliability = _clamp(0.55 + 0.35 * converged_rate + 0.10 * continue_rate - 0.40 * blocked_rate - 0.25 * hold_rate - 0.20 * no_progress_rate - 0.10 * cap_rate)
    reliability = round(reliability, 6)
    if total == 0:
        trend = "insufficient_history_trend"
        rec = "observe_more_history"
    elif blocked_rate >= 0.34:
        trend = "blocked_dominant_trend"
        rec = "repair_blocked_path"
    elif hold_rate >= 0.34:
        trend = "hold_dominant_trend"
        rec = "review_hold_condition"
    elif no_progress_rate >= 0.34:
        trend = "no_progress_trend"
        rec = "rebalance_next_supervision"
    elif converged_rate >= 0.50 and reliability >= 0.70:
        trend = "stable_converging_trend"
        rec = "lighten_next_supervision"
    else:
        trend = "bounded_working_trend"
        rec = "continue_current_supervision"
    return {
        "records_used": total,
        "trajectory_length": trajectory_len,
        "stop_reason_counts": dict(stop_counts),
        "scheduled_status_counts": dict(scheduled_counts),
        "rates": {
            "converged_rate": converged_rate,
            "blocked_rate": blocked_rate,
            "hold_rate": hold_rate,
            "no_progress_rate": no_progress_rate,
            "cycle_cap_rate": cap_rate,
            "continue_rate": continue_rate,
        },
        "reliability_score": reliability,
        "trend_class": trend,
        "recommendation": rec,
    }


def build_qi_process_tensor_cycle_trend_summary(*, runtime_context: Mapping[str, Any], trend_summary_license_packet: Mapping[str, Any]) -> QiProcessTensorCycleTrendSummaryResult:
    ctx = _m(runtime_context)
    lic = _m(trend_summary_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    supervisor_receipt_path = root / "qi_process_tensor_cycle_supervisor_receipt.json"
    supervisor_audit_path = root / "qi_process_tensor_cycle_supervisor_audit.jsonl"
    trajectory_path = root / "qi_circulation_trajectory_packet.json"
    summary_path = root / "qi_process_tensor_cycle_trend_summary.json"
    receipt_path = root / "qi_process_tensor_cycle_trend_summary_receipt.json"
    audit_path = root / "qi_process_tensor_cycle_trend_summary_audit.jsonl"

    if ctx.get("qi_process_tensor_cycle_trend_summary_enabled") is not True:
        blockers.append("qi_process_tensor_cycle_trend_summary_enabled_not_true")
    if ctx.get("apply_process_tensor_cycle_trend_summary") is not True:
        blockers.append("apply_process_tensor_cycle_trend_summary_not_true")
    if lic.get("license_status") != "QI_PROCESS_TENSOR_CYCLE_TREND_SUMMARY_LICENSE_READY":
        blockers.append("process_tensor_cycle_trend_summary_license_not_ready")
    for name in ["supervisor_receipt_read_allowed", "supervisor_audit_read_allowed", "trajectory_read_allowed", "summary_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    if not supervisor_receipt_path.is_file() and not supervisor_audit_path.is_file():
        blockers.append("supervisor_history_missing")
    if not trajectory_path.is_file():
        blockers.append("trajectory_packet_missing")

    receipt = _read_json(supervisor_receipt_path)
    audit_rows = _read_jsonl(supervisor_audit_path)
    trajectory = _read_json(trajectory_path)
    if supervisor_audit_path.is_file() and not audit_rows:
        warnings.append("supervisor_audit_empty_or_unreadable")
    max_records = _i(ctx.get("max_summary_records"), 50)
    if max_records < 1:
        blockers.append("max_summary_records_invalid")
        max_records = 1
    records = _collect_records(receipt, audit_rows, max_records)
    trend_payload = _summary(records, _trajectory_length(trajectory))
    summary = {
        "version": "kuuos_runtime_daemon_qi_process_tensor_cycle_trend_summary_v3_9",
        "summary_epoch": int(time.time()),
        "runtime_root": str(root),
        **trend_payload,
        "source_digests": {
            "supervisor_receipt": _sha(receipt),
            "supervisor_audit_rows": _sha(audit_rows),
            "trajectory_packet": _sha(trajectory),
        },
        "boundary": {
            "non_authoritative": True,
            "does_not_run_cycles": True,
            "does_not_modify_trajectory": True,
            "does_not_grant_execution_authority": True,
        },
    }
    write_performed = False
    if not blockers:
        _write_json(summary_path, summary)
        write_performed = True
    status = "QI_PROCESS_TENSOR_CYCLE_TREND_SUMMARY_READY" if not blockers else "QI_PROCESS_TENSOR_CYCLE_TREND_SUMMARY_BLOCKED"
    packet_id = "qi-pt-cycle-trend-summary-" + _sha({"summary": summary, "blockers": blockers})[:16]
    out_receipt = {
        "version": "kuuos_runtime_daemon_qi_process_tensor_cycle_trend_summary_v3_9",
        "status": status,
        "packet_id": packet_id,
        "trend_class": summary["trend_class"],
        "recommendation": summary["recommendation"],
        "reliability_score": summary["reliability_score"],
        "records_used": summary["records_used"],
        "trajectory_length": summary["trajectory_length"],
        "write_performed": write_performed,
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, out_receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**out_receipt, "record_digest": _sha(out_receipt)})
    return QiProcessTensorCycleTrendSummaryResult(
        "kuuos_runtime_daemon_qi_process_tensor_cycle_trend_summary_v3_9",
        status,
        packet_id,
        str(root),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        str(summary["trend_class"]),
        str(summary["recommendation"]),
        float(summary["reliability_score"]),
        int(summary["records_used"]),
        int(summary["trajectory_length"]),
        blockers,
        warnings,
    )
