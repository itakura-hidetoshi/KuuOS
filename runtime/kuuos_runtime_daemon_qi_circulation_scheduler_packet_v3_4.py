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
class QiCirculationSchedulerPacketResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    next_scheduler_packet_path: str
    scheduled_closed_loop_packet_path: str
    receipt_path: str
    audit_path: str
    handoff_class: str
    objective_hint: str
    max_cycles_delta: int
    threshold_delta: float
    write_performed: bool
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


def _handoff_class(packet: Mapping[str, Any]) -> tuple[str, str, int, float, list[str]]:
    warnings: list[str] = []
    objective_hint = str(packet.get("objective_hint", "rebalance"))
    if objective_hint not in {"maintain", "rebalance", "reopen"}:
        warnings.append("unknown_objective_hint_defaulted_to_rebalance")
        objective_hint = "rebalance"
    max_cycles_delta = _i(packet.get("max_cycles_delta"), 0)
    threshold_delta = round(_f(packet.get("convergence_threshold_delta", packet.get("threshold_delta", 0.0)), 0.0), 6)
    if packet.get("trajectory_adapted") is not True:
        warnings.append("trajectory_adapted_not_true")
    if objective_hint == "maintain" and max_cycles_delta < 0 and threshold_delta <= 0:
        return "stable_lighten_handoff", objective_hint, max_cycles_delta, threshold_delta, warnings
    if objective_hint == "reopen":
        return "reopen_handoff", objective_hint, max_cycles_delta, threshold_delta, warnings
    if objective_hint == "rebalance":
        return "rebalance_handoff", objective_hint, max_cycles_delta, threshold_delta, warnings
    return "continue_handoff", objective_hint, max_cycles_delta, threshold_delta, warnings


def _scheduled_closed_loop_packet(next_packet: Mapping[str, Any], handoff_class: str, objective_hint: str) -> dict[str, Any]:
    return {
        "initial_qi_packet": dict(next_packet.get("initial_qi_packet", {})) if isinstance(next_packet.get("initial_qi_packet"), Mapping) else {},
        "route_base": dict(next_packet.get("route_base", {})) if isinstance(next_packet.get("route_base"), Mapping) else {},
        "scheduler_handoff": {
            "source": "next_qi_circulation_scheduler_packet",
            "version": "kuuos_runtime_daemon_qi_circulation_scheduler_packet_v3_4",
            "handoff_class": handoff_class,
            "objective_hint": objective_hint,
            "max_cycles_delta": _i(next_packet.get("max_cycles_delta"), 0),
            "convergence_threshold_delta": round(_f(next_packet.get("convergence_threshold_delta", next_packet.get("threshold_delta", 0.0)), 0.0), 6),
            "trajectory_adapted": next_packet.get("trajectory_adapted") is True,
            "adapted_epoch": next_packet.get("adapted_epoch"),
            "source_digest": _sha(next_packet),
        },
    }


def build_qi_circulation_scheduler_packet(
    *, runtime_context: Mapping[str, Any], scheduler_packet_license: Mapping[str, Any]
) -> QiCirculationSchedulerPacketResult:
    ctx = _m(runtime_context)
    lic = _m(scheduler_packet_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    next_scheduler_packet_path = root / "next_qi_circulation_scheduler_packet.json"
    scheduled_closed_loop_packet_path = root / "qi_scheduled_closed_loop_packet.json"
    receipt_path = root / "qi_circulation_scheduler_packet_receipt.json"
    audit_path = root / "qi_circulation_scheduler_packet_audit.jsonl"
    if ctx.get("qi_circulation_scheduler_packet_enabled") is not True:
        blockers.append("qi_circulation_scheduler_packet_enabled_not_true")
    if ctx.get("apply_circulation_scheduler_packet") is not True:
        blockers.append("apply_circulation_scheduler_packet_not_true")
    if lic.get("license_status") != "QI_CIRCULATION_SCHEDULER_PACKET_LICENSE_READY":
        blockers.append("circulation_scheduler_packet_license_not_ready")
    for name in [
        "next_scheduler_packet_read_allowed",
        "scheduled_closed_loop_packet_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(next_scheduler_packet_path)
    if not packet:
        blockers.append("next_scheduler_packet_missing_or_invalid")
    if packet and not isinstance(packet.get("initial_qi_packet"), Mapping):
        warnings.append("initial_qi_packet_missing_or_not_mapping")
    if packet and not isinstance(packet.get("route_base"), Mapping):
        warnings.append("route_base_missing_or_not_mapping")
    handoff_class, objective_hint, max_delta, threshold_delta, class_warnings = _handoff_class(packet)
    warnings.extend(class_warnings)
    scheduled_packet = _scheduled_closed_loop_packet(packet, handoff_class, objective_hint)
    write_performed = False
    if not blockers:
        _write_json(scheduled_closed_loop_packet_path, scheduled_packet)
        write_performed = True
    status = (
        "QI_CIRCULATION_SCHEDULER_PACKET_BLOCKED"
        if blockers
        else "QI_CIRCULATION_SCHEDULER_PACKET_READY"
    )
    packet_id = "qi-circulation-scheduler-packet-" + _sha(
        {"packet": packet, "scheduled": scheduled_packet, "blockers": blockers}
    )[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_circulation_scheduler_packet_v3_4",
        "status": status,
        "packet_id": packet_id,
        "handoff_class": handoff_class,
        "objective_hint": objective_hint,
        "max_cycles_delta": max_delta,
        "threshold_delta": threshold_delta,
        "write_performed": write_performed,
        "next_scheduler_packet_digest": _sha(packet),
        "scheduled_closed_loop_packet_digest": _sha(scheduled_packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiCirculationSchedulerPacketResult(
        "kuuos_runtime_daemon_qi_circulation_scheduler_packet_v3_4",
        status,
        packet_id,
        str(root),
        str(next_scheduler_packet_path),
        str(scheduled_closed_loop_packet_path),
        str(receipt_path),
        str(audit_path),
        handoff_class,
        objective_hint,
        max_delta,
        threshold_delta,
        write_performed,
        blockers,
        warnings,
    )
