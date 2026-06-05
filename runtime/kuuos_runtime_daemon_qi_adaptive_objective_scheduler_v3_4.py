#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_circulation_objective_scheduler_v3_1 import build_qi_circulation_objective_scheduler


@dataclass(frozen=True)
class QiAdaptiveObjectiveSchedulerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    packet_path: str
    base_scheduler_packet_path: str
    closed_loop_packet_path: str
    receipt_path: str
    audit_path: str
    base_objective_class: str
    objective_hint: str
    applied_objective_class: str
    base_max_cycles: int
    adapted_max_cycles: int
    base_threshold: float
    adapted_threshold: float
    adapted: bool
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


def _scheduler_license() -> dict[str, Any]:
    return {
        "license_status": "QI_CIRCULATION_SCHEDULER_LICENSE_READY",
        "packet_read_allowed": True,
        "closed_loop_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _source_scheduler_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    raw = packet.get("next_qi_circulation_scheduler_packet", packet.get("scheduler_packet", {}))
    if isinstance(raw, Mapping) and raw:
        return dict(raw)
    return {
        "initial_qi_packet": dict(packet.get("initial_qi_packet", {})) if isinstance(packet.get("initial_qi_packet"), Mapping) else {},
        "route_base": dict(packet.get("route_base", {})) if isinstance(packet.get("route_base"), Mapping) else {},
    }


def _schedule_defaults(objective: str) -> tuple[int, float]:
    if objective == "maintain":
        return 2, 0.015
    if objective == "reopen":
        return 6, 0.04
    return 4, 0.025


def _apply_adaptation(base_packet: Mapping[str, Any], scheduled: Mapping[str, Any], base_objective: str) -> tuple[dict[str, Any], str, int, float]:
    hint = str(base_packet.get("objective_hint", ""))
    objective = hint if hint in {"maintain", "rebalance", "reopen"} else base_objective
    base_cycles = _i(scheduled.get("max_cycles"), _schedule_defaults(base_objective)[0])
    base_threshold = _f(scheduled.get("convergence_threshold"), _schedule_defaults(base_objective)[1])
    cycle_delta = _i(base_packet.get("max_cycles_delta"), 0)
    threshold_delta = _f(base_packet.get("convergence_threshold_delta", base_packet.get("threshold_delta")), 0.0)
    if objective != base_objective:
        base_cycles, base_threshold = _schedule_defaults(objective)
    adapted_cycles = max(1, min(12, base_cycles + cycle_delta))
    adapted_threshold = round(max(0.0, min(1.0, base_threshold + threshold_delta)), 6)
    out = dict(scheduled)
    out.update({
        "objective_class": objective,
        "max_cycles": adapted_cycles,
        "convergence_threshold": adapted_threshold,
        "adaptive_objective_hint": hint,
        "adaptive_cycle_delta": cycle_delta,
        "adaptive_threshold_delta": threshold_delta,
        "adaptive_scheduler_applied": True,
    })
    return out, objective, adapted_cycles, adapted_threshold


def build_qi_adaptive_objective_scheduler(*, runtime_context: Mapping[str, Any], adaptive_license_packet: Mapping[str, Any]) -> QiAdaptiveObjectiveSchedulerResult:
    ctx = _m(runtime_context)
    lic = _m(adaptive_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "qi_adaptive_scheduler_packet.json"
    base_scheduler_packet_path = root / "qi_circulation_scheduler_packet.json"
    closed_loop_packet_path = root / "qi_circulation_closed_loop_packet.json"
    receipt_path = root / "qi_adaptive_scheduler_receipt.json"
    audit_path = root / "qi_adaptive_scheduler_audit.jsonl"
    if ctx.get("qi_adaptive_scheduler_enabled") is not True:
        blockers.append("qi_adaptive_scheduler_enabled_not_true")
    if ctx.get("apply_adaptive_scheduler") is not True:
        blockers.append("apply_adaptive_scheduler_not_true")
    if lic.get("license_status") != "QI_ADAPTIVE_SCHEDULER_LICENSE_READY":
        blockers.append("adaptive_scheduler_license_not_ready")
    for name in ["packet_read_allowed", "base_scheduler_run_allowed", "closed_loop_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(packet_path)
    source_packet = _source_scheduler_packet(packet)
    base_objective = "unknown"
    objective_hint = str(source_packet.get("objective_hint", ""))
    applied_objective = "unknown"
    base_max_cycles = 0
    adapted_max_cycles = 0
    base_threshold = 0.0
    adapted_threshold = 0.0
    adapted = False
    if not blockers:
        _write_json(base_scheduler_packet_path, source_packet)
        base = build_qi_circulation_objective_scheduler(
            runtime_context={"qi_circulation_scheduler_enabled": True, "apply_circulation_scheduler": True, "runtime_root": str(root)},
            scheduler_license_packet=_scheduler_license(),
        )
        base_payload = base.to_dict()
        if base_payload.get("status") != "QI_CIRCULATION_SCHEDULER_READY":
            blockers.append("base_scheduler_not_ready")
        else:
            scheduled = _read_json(closed_loop_packet_path)
            base_objective = str(scheduled.get("objective_class", base_payload.get("objective_class", "unknown")))
            base_max_cycles = _i(scheduled.get("max_cycles"), 0)
            base_threshold = _f(scheduled.get("convergence_threshold"), 0.0)
            adapted_packet, applied_objective, adapted_max_cycles, adapted_threshold = _apply_adaptation(source_packet, scheduled, base_objective)
            _write_json(closed_loop_packet_path, adapted_packet)
            adapted = True
    status = "QI_ADAPTIVE_SCHEDULER_BLOCKED" if blockers else "QI_ADAPTIVE_SCHEDULER_READY"
    packet_id = "qi-adaptive-scheduler-" + _sha({"packet": packet, "adapted": adapted, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_adaptive_objective_scheduler_v3_4", "status": status, "packet_id": packet_id, "base_objective_class": base_objective, "objective_hint": objective_hint, "applied_objective_class": applied_objective, "base_max_cycles": base_max_cycles, "adapted_max_cycles": adapted_max_cycles, "base_threshold": base_threshold, "adapted_threshold": adapted_threshold, "adapted": adapted, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiAdaptiveObjectiveSchedulerResult("kuuos_runtime_daemon_qi_adaptive_objective_scheduler_v3_4", status, packet_id, str(root), str(packet_path), str(base_scheduler_packet_path), str(closed_loop_packet_path), str(receipt_path), str(audit_path), base_objective, objective_hint, applied_objective, base_max_cycles, adapted_max_cycles, base_threshold, adapted_threshold, adapted, blockers, warnings)
