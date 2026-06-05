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
class QiCirculationObjectiveSchedulerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    packet_path: str
    closed_loop_packet_path: str
    receipt_path: str
    audit_path: str
    objective_class: str
    max_cycles: int
    convergence_threshold: float
    scheduled: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


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


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _classify(qi: Mapping[str, Any]) -> tuple[str, int, float]:
    flow = _clamp(_f(qi.get("qi_flow", qi.get("flow", 0.5)), 0.5))
    coherence = _clamp(_f(qi.get("coherence_score", qi.get("coherence", 0.5)), 0.5))
    pressure = _clamp(_f(qi.get("circulation_pressure", qi.get("execution_pressure", 0.5)), 0.5))
    friction = _clamp(_f(qi.get("friction", qi.get("drag", 0.0)), 0.0))
    if qi.get("critical_blocker_present") is True or qi.get("scope_mismatch") is True or qi.get("head_sha_mismatch") is True:
        return "concrete_stop", 1, 0.0
    circulation_score = _clamp((0.35 * flow) + (0.25 * coherence) + (0.25 * pressure) - (0.20 * friction))
    if circulation_score >= 0.78 and friction <= 0.20:
        return "maintain", 2, 0.015
    if circulation_score >= 0.48:
        return "rebalance", 4, 0.025
    return "reopen", 6, 0.04


def _closed_loop_packet(packet: Mapping[str, Any], objective: str, max_cycles: int, threshold: float) -> dict[str, Any]:
    initial = dict(packet.get("initial_qi_packet", {})) if isinstance(packet.get("initial_qi_packet"), Mapping) else dict(packet.get("qi_process_tensor_packet", {})) if isinstance(packet.get("qi_process_tensor_packet"), Mapping) else {}
    route_base = dict(packet.get("route_base", {})) if isinstance(packet.get("route_base"), Mapping) else {}
    return {
        "max_cycles": int(max_cycles),
        "convergence_threshold": threshold,
        "objective_class": objective,
        "initial_qi_packet": initial,
        "route_base": route_base,
    }


def build_qi_circulation_objective_scheduler(*, runtime_context: Mapping[str, Any], scheduler_license_packet: Mapping[str, Any]) -> QiCirculationObjectiveSchedulerResult:
    ctx = _m(runtime_context)
    lic = _m(scheduler_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "qi_circulation_scheduler_packet.json"
    closed_loop_packet_path = root / "qi_circulation_closed_loop_packet.json"
    receipt_path = root / "qi_circulation_scheduler_receipt.json"
    audit_path = root / "qi_circulation_scheduler_audit.jsonl"
    if ctx.get("qi_circulation_scheduler_enabled") is not True:
        blockers.append("qi_circulation_scheduler_enabled_not_true")
    if ctx.get("apply_circulation_scheduler") is not True:
        blockers.append("apply_circulation_scheduler_not_true")
    if lic.get("license_status") != "QI_CIRCULATION_SCHEDULER_LICENSE_READY":
        blockers.append("circulation_scheduler_license_not_ready")
    for name in ["packet_read_allowed", "closed_loop_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(packet_path)
    qi = dict(packet.get("initial_qi_packet", {})) if isinstance(packet.get("initial_qi_packet"), Mapping) else dict(packet.get("qi_process_tensor_packet", {})) if isinstance(packet.get("qi_process_tensor_packet"), Mapping) else {}
    route_base = packet.get("route_base", {})
    if not qi:
        blockers.append("initial_qi_packet_missing")
    if not isinstance(route_base, Mapping) or not route_base:
        blockers.append("route_base_missing")
    objective, max_cycles, threshold = _classify(qi)
    scheduled = False
    if objective == "concrete_stop":
        blockers.append("concrete_stop_objective")
    if not blockers:
        out = _closed_loop_packet(packet, objective, max_cycles, threshold)
        _write_json(closed_loop_packet_path, out)
        scheduled = True
    if blockers:
        status = "QI_CIRCULATION_SCHEDULER_BLOCKED"
    else:
        status = "QI_CIRCULATION_SCHEDULER_READY"
    packet_id = "qi-circulation-scheduler-" + _sha({"packet": packet, "objective": objective, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_circulation_objective_scheduler_v3_1", "status": status, "packet_id": packet_id, "objective_class": objective, "max_cycles": max_cycles, "convergence_threshold": threshold, "scheduled": scheduled, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiCirculationObjectiveSchedulerResult("kuuos_runtime_daemon_qi_circulation_objective_scheduler_v3_1", status, packet_id, str(root), str(packet_path), str(closed_loop_packet_path), str(receipt_path), str(audit_path), objective, max_cycles, threshold, scheduled, blockers, warnings)
