#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor


@dataclass(frozen=True)
class QiProcessTensorSchedulerOverlayResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    scheduled_packet_path: str
    process_tensor_packet_path: str
    receipt_path: str
    audit_path: str
    overlay_class: str
    process_tensor_visible: bool
    nonmarkov_memory_visible: bool
    memory_depth: int
    non_markov_unresolved: bool
    recovery_witness_present: bool
    write_performed: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


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


def _b(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "present", "ok", "pass", "ready"}
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


def _raw_for_process_tensor(scheduled: Mapping[str, Any], pt: Mapping[str, Any]) -> dict[str, Any]:
    initial = _m(scheduled.get("initial_qi_packet"))
    handoff = _m(scheduled.get("scheduler_handoff"))
    raw = dict(initial)
    raw.update(dict(pt))
    if "process_history" not in raw:
        raw["process_history"] = _list(pt.get("process_history")) or _list(initial.get("process_history")) or _list(scheduled.get("process_history")) or _list(handoff.get("process_history"))
    raw.setdefault("cycle_id", str(pt.get("cycle_id") or handoff.get("source_digest") or "qi-process-tensor-scheduler-overlay"))
    return raw


def _classify_overlay(*, process_tensor_visible: bool, nonmarkov_memory_visible: bool, memory_depth: int, non_markov_unresolved: bool, recovery_witness_present: bool, pressure: float, coherence: float) -> str:
    if non_markov_unresolved:
        return "process_tensor_hold_overlay"
    if not recovery_witness_present:
        return "process_tensor_recovery_overlay"
    if process_tensor_visible and nonmarkov_memory_visible and memory_depth >= 5 and coherence >= 0.70 and pressure <= 0.65:
        return "process_tensor_stabilize_overlay"
    if process_tensor_visible and (memory_depth >= 3 or pressure >= 0.70):
        return "process_tensor_rebalance_overlay"
    return "process_tensor_continue_overlay"


def _overlay_packet(scheduled: Mapping[str, Any], pt: Mapping[str, Any], receipt: Mapping[str, Any], overlay_class: str) -> dict[str, Any]:
    out = dict(scheduled)
    initial = dict(_m(out.get("initial_qi_packet")))
    route_base = dict(_m(out.get("route_base")))
    pressure = _clamp(_f(pt.get("execution_pressure", pt.get("pressure", initial.get("circulation_pressure", initial.get("execution_pressure", 0.5)))), 0.5))
    coherence = _clamp(_f(pt.get("coherence_score", pt.get("coherence", initial.get("coherence_score", initial.get("coherence", 0.5)))), 0.5))
    memory_depth = _i(pt.get("memory_depth", pt.get("history_depth", receipt.get("process_history_length", 0))), 0)
    non_markov_unresolved = _b(pt.get("non_markov_unresolved"), False)
    recovery_missing = _b(pt.get("recovery_witness_missing"), False)
    recovery_present = _b(pt.get("recovery_witness_present"), not recovery_missing)

    if overlay_class == "process_tensor_hold_overlay":
        initial["critical_blocker_present"] = True
        initial["process_tensor_hold_required"] = True
        initial["circulation_pressure"] = round(max(_f(initial.get("circulation_pressure", pressure), pressure), pressure), 6)
    elif overlay_class == "process_tensor_recovery_overlay":
        initial["friction"] = round(_clamp(_f(initial.get("friction", 0.0), 0.0) + 0.15), 6)
        initial["circulation_pressure"] = round(_clamp(pressure - 0.10), 6)
        initial["recovery_witness_missing"] = True
    elif overlay_class == "process_tensor_stabilize_overlay":
        initial["qi_flow"] = round(_clamp(_f(initial.get("qi_flow", initial.get("flow", 0.5)), 0.5) + 0.03), 6)
        initial["coherence_score"] = round(_clamp(_f(initial.get("coherence_score", initial.get("coherence", coherence)), coherence) + 0.03), 6)
        initial["friction"] = round(_clamp(_f(initial.get("friction", 0.0), 0.0) - 0.03), 6)
    elif overlay_class == "process_tensor_rebalance_overlay":
        initial["circulation_pressure"] = round(_clamp(max(pressure, _f(initial.get("circulation_pressure", 0.0), 0.0)) + 0.05), 6)
        initial["friction"] = round(_clamp(_f(initial.get("friction", 0.0), 0.0) + 0.02), 6)
    else:
        initial["circulation_pressure"] = round(_clamp(pressure), 6)
        initial["coherence_score"] = round(_clamp(coherence), 6)

    initial["process_tensor_visible"] = bool(receipt.get("process_tensor_visible"))
    initial["memory_continuity_visible"] = bool(receipt.get("memory_continuity_visible"))
    initial["nonmarkov_memory_visible"] = bool(receipt.get("nonmarkov_memory_visible"))
    initial["process_tensor_memory_depth"] = memory_depth
    initial["non_markov_unresolved"] = non_markov_unresolved
    initial["recovery_witness_present"] = recovery_present
    initial["process_tensor_overlay_class"] = overlay_class

    route_base.setdefault("process_tensor_route_seed", overlay_class)
    route_base["process_tensor_memory_depth"] = memory_depth
    route_base["process_tensor_digest"] = _sha(dict(pt))
    out["initial_qi_packet"] = initial
    out["route_base"] = route_base
    out["process_tensor_scheduler_overlay"] = {
        "version": "kuuos_runtime_daemon_qi_process_tensor_scheduler_overlay_v3_5",
        "overlay_class": overlay_class,
        "process_tensor_digest": _sha(dict(pt)),
        "receipt_digest": _sha(dict(receipt)),
        "memory_depth": memory_depth,
        "non_markov_unresolved": non_markov_unresolved,
        "recovery_witness_present": recovery_present,
        "source": "qi_process_tensor_packet.json",
    }
    return out


def build_qi_process_tensor_scheduler_overlay(*, runtime_context: Mapping[str, Any], overlay_license_packet: Mapping[str, Any]) -> QiProcessTensorSchedulerOverlayResult:
    ctx = _m(runtime_context)
    lic = _m(overlay_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    scheduled_packet_path = root / "qi_scheduled_closed_loop_packet.json"
    process_tensor_packet_path = root / "qi_process_tensor_packet.json"
    receipt_path = root / "qi_process_tensor_scheduler_overlay_receipt.json"
    audit_path = root / "qi_process_tensor_scheduler_overlay_audit.jsonl"
    if ctx.get("qi_process_tensor_scheduler_overlay_enabled") is not True:
        blockers.append("qi_process_tensor_scheduler_overlay_enabled_not_true")
    if ctx.get("apply_process_tensor_scheduler_overlay") is not True:
        blockers.append("apply_process_tensor_scheduler_overlay_not_true")
    if lic.get("license_status") != "QI_PROCESS_TENSOR_SCHEDULER_OVERLAY_LICENSE_READY":
        blockers.append("process_tensor_scheduler_overlay_license_not_ready")
    for name in ["scheduled_packet_read_allowed", "process_tensor_packet_read_allowed", "scheduled_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    scheduled = _read_json(scheduled_packet_path)
    pt = _read_json(process_tensor_packet_path)
    if not scheduled:
        blockers.append("scheduled_closed_loop_packet_missing_or_invalid")
    if not pt:
        blockers.append("process_tensor_packet_missing_or_invalid")

    evaluated = evaluate_qi_process_tensor(_raw_for_process_tensor(scheduled, pt))
    receipt = evaluated.to_dict()
    process_tensor_visible = bool(receipt.get("process_tensor_visible"))
    nonmarkov_memory_visible = bool(receipt.get("nonmarkov_memory_visible"))
    memory_depth = _i(pt.get("memory_depth", pt.get("history_depth", receipt.get("process_history_length", 0))), 0)
    non_markov_unresolved = _b(pt.get("non_markov_unresolved"), False)
    recovery_missing = _b(pt.get("recovery_witness_missing"), False)
    recovery_present = _b(pt.get("recovery_witness_present"), not recovery_missing)
    pressure = _clamp(_f(pt.get("execution_pressure", pt.get("pressure")), 0.5))
    coherence = _clamp(_f(pt.get("coherence_score", pt.get("coherence")), 0.5))
    if pt and not (_b(pt.get("process_tensor_ok"), False) or process_tensor_visible):
        blockers.append("process_tensor_not_ready")
    if not nonmarkov_memory_visible:
        warnings.append("nonmarkov_memory_not_visible")
    if non_markov_unresolved:
        warnings.append("non_markov_unresolved_sets_hold_overlay")
    if not recovery_present:
        warnings.append("recovery_witness_missing_sets_recovery_overlay")

    overlay_class = _classify_overlay(process_tensor_visible=process_tensor_visible, nonmarkov_memory_visible=nonmarkov_memory_visible, memory_depth=memory_depth, non_markov_unresolved=non_markov_unresolved, recovery_witness_present=recovery_present, pressure=pressure, coherence=coherence)
    overlay_packet = _overlay_packet(scheduled, pt, receipt, overlay_class)
    write_performed = False
    if not blockers:
        _write_json(scheduled_packet_path, overlay_packet)
        write_performed = True
    status = "QI_PROCESS_TENSOR_SCHEDULER_OVERLAY_BLOCKED" if blockers else "QI_PROCESS_TENSOR_SCHEDULER_OVERLAY_READY"
    packet_id = "qi-pt-scheduler-overlay-" + _sha({"scheduled": scheduled, "pt": pt, "overlay": overlay_class, "blockers": blockers})[:16]
    out_receipt = {"version": "kuuos_runtime_daemon_qi_process_tensor_scheduler_overlay_v3_5", "status": status, "packet_id": packet_id, "overlay_class": overlay_class, "process_tensor_visible": process_tensor_visible, "nonmarkov_memory_visible": nonmarkov_memory_visible, "memory_depth": memory_depth, "non_markov_unresolved": non_markov_unresolved, "recovery_witness_present": recovery_present, "write_performed": write_performed, "scheduled_packet_digest": _sha(overlay_packet), "process_tensor_packet_digest": _sha(pt), "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, out_receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**out_receipt, "record_digest": _sha(out_receipt)})
    return QiProcessTensorSchedulerOverlayResult("kuuos_runtime_daemon_qi_process_tensor_scheduler_overlay_v3_5", status, packet_id, str(root), str(scheduled_packet_path), str(process_tensor_packet_path), str(receipt_path), str(audit_path), overlay_class, process_tensor_visible, nonmarkov_memory_visible, memory_depth, non_markov_unresolved, recovery_present, write_performed, blockers, warnings)
