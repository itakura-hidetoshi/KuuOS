#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


@dataclass(frozen=True)
class QiTrendAdaptiveSupervisorPacketResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    next_supervisor_packet_path: str
    receipt_path: str
    audit_path: str
    adaptation_class: str
    recommendation: str
    reliability_score: float
    max_supervised_cycles: int
    max_trajectory_records: int
    write_performed: bool
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


def _clamp_int(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def _clamp_float(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
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


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _trend(summary: Mapping[str, Any], receipt: Mapping[str, Any]) -> tuple[str, str, float, int, int]:
    trend_class = str(summary.get("trend_class") or receipt.get("trend_class") or "insufficient_history_trend")
    recommendation = str(summary.get("recommendation") or receipt.get("recommendation") or "observe_more_history")
    reliability = round(_clamp_float(_f(summary.get("reliability_score", receipt.get("reliability_score", 0.0)), 0.0)), 6)
    records_used = _i(summary.get("records_used", receipt.get("records_used", 0)), 0)
    trajectory_length = _i(summary.get("trajectory_length", receipt.get("trajectory_length", 0)), 0)
    return trend_class, recommendation, reliability, records_used, trajectory_length


def _adaptation(*, recommendation: str, trend_class: str, reliability: float, base_cycles: int, base_records: int) -> tuple[str, int, int, list[str]]:
    warnings: list[str] = []
    if recommendation == "lighten_next_supervision" and reliability >= 0.70:
        return "lighten_supervision_packet", _clamp_int(base_cycles - 1, 1, 20), _clamp_int(base_records, 5, 200), warnings
    if recommendation == "rebalance_next_supervision":
        return "rebalance_supervision_packet", _clamp_int(base_cycles + 1, 1, 20), _clamp_int(base_records + 5, 5, 200), warnings
    if recommendation == "review_hold_condition":
        return "hold_review_supervision_packet", _clamp_int(base_cycles + 1, 1, 20), _clamp_int(base_records + 10, 5, 200), warnings
    if recommendation == "repair_blocked_path":
        return "blocked_repair_supervision_packet", _clamp_int(base_cycles + 2, 1, 20), _clamp_int(base_records + 10, 5, 200), warnings
    if recommendation == "observe_more_history":
        return "observe_more_supervision_packet", _clamp_int(max(base_cycles, 2), 1, 20), _clamp_int(base_records + 10, 5, 200), warnings
    if recommendation != "continue_current_supervision":
        warnings.append("unknown_recommendation_defaulted_to_continue")
    if trend_class == "stable_converging_trend" and reliability >= 0.80:
        return "lighten_supervision_packet", _clamp_int(base_cycles - 1, 1, 20), _clamp_int(base_records, 5, 200), warnings
    return "continue_supervision_packet", _clamp_int(base_cycles, 1, 20), _clamp_int(base_records, 5, 200), warnings


def _next_packet(*, summary: Mapping[str, Any], receipt: Mapping[str, Any], adaptation_class: str, recommendation: str, trend_class: str, reliability: float, max_cycles: int, max_records: int) -> dict[str, Any]:
    return {
        "version": "next_qi_process_tensor_cycle_supervisor_packet_v4_0",
        "source": "qi_trend_adaptive_supervisor_packet_v4_0",
        "adaptation_class": adaptation_class,
        "recommendation": recommendation,
        "trend_class": trend_class,
        "reliability_score": reliability,
        "runtime_context_patch": {
            "max_supervised_cycles": max_cycles,
            "max_trajectory_records": max_records,
        },
        "supervisor_context": {
            "qi_process_tensor_cycle_supervisor_enabled": True,
            "apply_process_tensor_cycle_supervisor": True,
            "max_supervised_cycles": max_cycles,
            "max_trajectory_records": max_records,
        },
        "license_hint": {
            "license_status": "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_LICENSE_READY",
            "cycle_runner_run_allowed": True,
            "state_write_allowed": True,
            "receipt_write_allowed": True,
            "audit_append_allowed": True,
        },
        "source_digests": {
            "trend_summary": _sha(dict(summary)),
            "trend_receipt": _sha(dict(receipt)),
        },
        "boundary": {
            "non_authoritative": True,
            "does_not_run_cycles": True,
            "does_not_modify_trajectory": True,
            "suggested_packet_only": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_trend_adaptive_supervisor_packet(*, runtime_context: Mapping[str, Any], adaptive_packet_license: Mapping[str, Any]) -> QiTrendAdaptiveSupervisorPacketResult:
    ctx = _m(runtime_context)
    lic = _m(adaptive_packet_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    summary_path = root / "qi_process_tensor_cycle_trend_summary.json"
    trend_receipt_path = root / "qi_process_tensor_cycle_trend_summary_receipt.json"
    next_supervisor_packet_path = root / "next_qi_process_tensor_cycle_supervisor_packet.json"
    receipt_path = root / "qi_trend_adaptive_supervisor_packet_receipt.json"
    audit_path = root / "qi_trend_adaptive_supervisor_packet_audit.jsonl"

    if ctx.get("qi_trend_adaptive_supervisor_packet_enabled") is not True:
        blockers.append("qi_trend_adaptive_supervisor_packet_enabled_not_true")
    if ctx.get("apply_trend_adaptive_supervisor_packet") is not True:
        blockers.append("apply_trend_adaptive_supervisor_packet_not_true")
    if lic.get("license_status") != "QI_TREND_ADAPTIVE_SUPERVISOR_PACKET_LICENSE_READY":
        blockers.append("trend_adaptive_supervisor_packet_license_not_ready")
    for name in ["trend_summary_read_allowed", "trend_receipt_read_allowed", "next_supervisor_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    summary = _read_json(summary_path)
    receipt = _read_json(trend_receipt_path)
    if not summary and not receipt:
        blockers.append("trend_summary_missing")
    trend_class, recommendation, reliability, records_used, trajectory_length = _trend(summary, receipt)
    base_cycles = _clamp_int(_i(ctx.get("base_max_supervised_cycles"), 3), 1, 20)
    base_records = _clamp_int(_i(ctx.get("base_max_trajectory_records"), 50), 5, 200)
    if records_used <= 0:
        warnings.append("records_used_zero_or_missing")
    if trajectory_length <= 0:
        warnings.append("trajectory_length_zero_or_missing")
    adaptation_class, max_cycles, max_records, adaptation_warnings = _adaptation(
        recommendation=recommendation,
        trend_class=trend_class,
        reliability=reliability,
        base_cycles=base_cycles,
        base_records=base_records,
    )
    warnings.extend(adaptation_warnings)
    packet = _next_packet(
        summary=summary,
        receipt=receipt,
        adaptation_class=adaptation_class,
        recommendation=recommendation,
        trend_class=trend_class,
        reliability=reliability,
        max_cycles=max_cycles,
        max_records=max_records,
    )
    write_performed = False
    if not blockers:
        _write_json(next_supervisor_packet_path, packet)
        write_performed = True
    status = "QI_TREND_ADAPTIVE_SUPERVISOR_PACKET_READY" if not blockers else "QI_TREND_ADAPTIVE_SUPERVISOR_PACKET_BLOCKED"
    packet_id = "qi-trend-adaptive-supervisor-" + _sha({"packet": packet, "blockers": blockers})[:16]
    out_receipt = {
        "version": "kuuos_runtime_daemon_qi_trend_adaptive_supervisor_packet_v4_0",
        "status": status,
        "packet_id": packet_id,
        "adaptation_class": adaptation_class,
        "recommendation": recommendation,
        "trend_class": trend_class,
        "reliability_score": reliability,
        "records_used": records_used,
        "trajectory_length": trajectory_length,
        "max_supervised_cycles": max_cycles,
        "max_trajectory_records": max_records,
        "write_performed": write_performed,
        "next_supervisor_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, out_receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**out_receipt, "record_digest": _sha(out_receipt)})
    return QiTrendAdaptiveSupervisorPacketResult(
        "kuuos_runtime_daemon_qi_trend_adaptive_supervisor_packet_v4_0",
        status,
        packet_id,
        str(root),
        str(next_supervisor_packet_path),
        str(receipt_path),
        str(audit_path),
        adaptation_class,
        recommendation,
        reliability,
        max_cycles,
        max_records,
        write_performed,
        blockers,
        warnings,
    )
