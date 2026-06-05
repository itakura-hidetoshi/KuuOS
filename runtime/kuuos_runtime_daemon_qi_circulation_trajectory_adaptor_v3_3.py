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
class QiCirculationTrajectoryAdaptorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    packet_path: str
    next_scheduler_packet_path: str
    receipt_path: str
    audit_path: str
    adaptation_class: str
    next_objective_hint: str
    max_cycles_delta: int
    threshold_delta: float
    adapted: bool
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


def _i(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
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


def _trajectory(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = packet.get("trajectory", [])
    if isinstance(raw, list):
        return [dict(item) for item in raw if isinstance(item, Mapping)]
    receipt = packet.get("scheduled_closed_loop_receipt", {})
    if isinstance(receipt, Mapping):
        return [dict(receipt)]
    return []


def _classify(records: list[dict[str, Any]]) -> tuple[str, str, int, float]:
    if not records:
        return "no_trajectory", "reopen", 2, 0.01
    last = records[-1]
    status = str(last.get("status", ""))
    objective = str(last.get("objective_class", "unknown"))
    converged = last.get("converged") is True
    cycle_count = _i(last.get("cycle_count"), 0)
    final_qi = _m(last.get("final_qi_packet", {}))
    qi_flow = _clamp(_f(final_qi.get("qi_flow", final_qi.get("flow", 0.5)), 0.5))
    friction = _clamp(_f(final_qi.get("friction", final_qi.get("drag", 0.0)), 0.0))
    if "BLOCKED" in status:
        return "blocked_recovery", "reopen", 2, 0.02
    if converged and qi_flow >= 0.78 and friction <= 0.20:
        return "stable_lighten", "maintain", -1, -0.005
    if objective == "reopen" and qi_flow < 0.55:
        return "needs_more_reopen", "reopen", 2, 0.015
    if cycle_count >= 5 and not converged:
        return "long_cycle_rebalance", "rebalance", 1, 0.01
    return "continue_adapt", objective if objective in {"maintain", "rebalance", "reopen"} else "rebalance", 0, 0.0


def _next_scheduler_packet(packet: Mapping[str, Any], objective_hint: str, max_cycles_delta: int, threshold_delta: float) -> dict[str, Any]:
    base = dict(packet.get("next_scheduler_packet", {})) if isinstance(packet.get("next_scheduler_packet"), Mapping) else {}
    if not base:
        base = {
            "initial_qi_packet": dict(packet.get("next_qi_packet", {})) if isinstance(packet.get("next_qi_packet"), Mapping) else dict(packet.get("initial_qi_packet", {})) if isinstance(packet.get("initial_qi_packet"), Mapping) else {},
            "route_base": dict(packet.get("route_base", {})) if isinstance(packet.get("route_base"), Mapping) else {},
        }
    base["objective_hint"] = objective_hint
    base["max_cycles_delta"] = int(max_cycles_delta)
    base["convergence_threshold_delta"] = round(threshold_delta, 6)
    base["trajectory_adapted"] = True
    base["adapted_epoch"] = int(time.time())
    return base


def build_qi_circulation_trajectory_adaptor(*, runtime_context: Mapping[str, Any], adaptor_license_packet: Mapping[str, Any]) -> QiCirculationTrajectoryAdaptorResult:
    ctx = _m(runtime_context)
    lic = _m(adaptor_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "qi_circulation_trajectory_packet.json"
    next_scheduler_packet_path = root / "next_qi_circulation_scheduler_packet.json"
    receipt_path = root / "qi_circulation_trajectory_receipt.json"
    audit_path = root / "qi_circulation_trajectory_audit.jsonl"
    if ctx.get("qi_circulation_trajectory_adaptor_enabled") is not True:
        blockers.append("qi_circulation_trajectory_adaptor_enabled_not_true")
    if ctx.get("apply_circulation_trajectory_adaptor") is not True:
        blockers.append("apply_circulation_trajectory_adaptor_not_true")
    if lic.get("license_status") != "QI_CIRCULATION_TRAJECTORY_ADAPTOR_LICENSE_READY":
        blockers.append("circulation_trajectory_adaptor_license_not_ready")
    for name in ["packet_read_allowed", "next_scheduler_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(packet_path)
    records = _trajectory(packet)
    adaptation_class, objective_hint, max_delta, threshold_delta = _classify(records)
    if adaptation_class == "no_trajectory":
        warnings.append("no_trajectory_using_reopen_seed")
    adapted = False
    next_packet = _next_scheduler_packet(packet, objective_hint, max_delta, threshold_delta)
    if not blockers:
        _write_json(next_scheduler_packet_path, next_packet)
        adapted = True
    if blockers:
        status = "QI_CIRCULATION_TRAJECTORY_ADAPTOR_BLOCKED"
    else:
        status = "QI_CIRCULATION_TRAJECTORY_ADAPTOR_READY"
    packet_id = "qi-circulation-trajectory-adaptor-" + _sha({"packet": packet, "adaptation": adaptation_class, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_circulation_trajectory_adaptor_v3_3", "status": status, "packet_id": packet_id, "adaptation_class": adaptation_class, "next_objective_hint": objective_hint, "max_cycles_delta": max_delta, "threshold_delta": threshold_delta, "adapted": adapted, "next_scheduler_packet_digest": _sha(next_packet), "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiCirculationTrajectoryAdaptorResult("kuuos_runtime_daemon_qi_circulation_trajectory_adaptor_v3_3", status, packet_id, str(root), str(packet_path), str(next_scheduler_packet_path), str(receipt_path), str(audit_path), adaptation_class, objective_hint, max_delta, threshold_delta, adapted, blockers, warnings)
