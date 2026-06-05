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
class QiCirculationFeedbackControllerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    packet_path: str
    next_packet_path: str
    receipt_path: str
    audit_path: str
    feedback_action: str
    flow_gain: float
    friction_attenuation: float
    recovery_bias: float
    next_qi_packet: dict[str, Any]
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


def _feedback_from_action(action: str, circulation: float, stagnation: float) -> tuple[str, float, float, float]:
    if action == "continue_cycle":
        return "maintain_circulation", 1.05, 0.98, 0.02
    if action == "rebalance_and_continue":
        return "rebalance_circulation", 1.14, 0.88, 0.08
    if action == "reopen_flow":
        gain = 1.25 + (0.20 * _clamp(stagnation))
        return "reopen_circulation", round(gain, 6), 0.65, 0.18
    if action == "concrete_stop":
        return "hold_for_concrete_reason", 1.0, 1.0, 0.0
    if circulation >= 0.7:
        return "maintain_circulation", 1.05, 0.98, 0.02
    if circulation >= 0.45:
        return "rebalance_circulation", 1.14, 0.88, 0.08
    return "reopen_circulation", 1.28, 0.65, 0.18


def _next_packet(current: Mapping[str, Any], feedback_action: str, flow_gain: float, friction_attenuation: float, recovery_bias: float) -> dict[str, Any]:
    qi_flow = _clamp(_f(current.get("qi_flow", current.get("flow", 0.5)), 0.5) * flow_gain)
    coherence = _clamp(_f(current.get("coherence_score", current.get("coherence", 0.5)), 0.5) + (0.5 * recovery_bias))
    pressure = _clamp(_f(current.get("circulation_pressure", current.get("execution_pressure", 0.5)), 0.5) + (0.4 * recovery_bias))
    friction = _clamp(_f(current.get("friction", current.get("drag", 0.0)), 0.0) * friction_attenuation)
    next_packet = dict(current)
    next_packet.update({
        "qi_flow": round(qi_flow, 6),
        "coherence_score": round(coherence, 6),
        "circulation_pressure": round(pressure, 6),
        "friction": round(friction, 6),
        "recovery_witness_present": True,
        "feedback_action": feedback_action,
        "feedback_epoch": int(time.time()),
    })
    return next_packet


def build_qi_circulation_feedback_controller(*, runtime_context: Mapping[str, Any], feedback_license_packet: Mapping[str, Any]) -> QiCirculationFeedbackControllerResult:
    ctx = _m(runtime_context)
    lic = _m(feedback_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "qi_circulation_feedback_packet.json"
    next_packet_path = root / "next_qi_process_tensor_packet.json"
    receipt_path = root / "qi_circulation_feedback_receipt.json"
    audit_path = root / "qi_circulation_feedback_audit.jsonl"
    if ctx.get("qi_circulation_feedback_enabled") is not True:
        blockers.append("qi_circulation_feedback_enabled_not_true")
    if ctx.get("apply_circulation_feedback") is not True:
        blockers.append("apply_circulation_feedback_not_true")
    if lic.get("license_status") != "QI_CIRCULATION_FEEDBACK_LICENSE_READY":
        blockers.append("circulation_feedback_license_not_ready")
    for name in ["packet_read_allowed", "next_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(packet_path)
    current = dict(packet.get("current_qi_packet", {})) if isinstance(packet.get("current_qi_packet"), Mapping) else {}
    router = _m(packet.get("router_receipt", {}))
    action = str(packet.get("recommended_action", router.get("recommended_action", current.get("recommended_action", ""))))
    circulation = _clamp(_f(packet.get("circulation_index", router.get("circulation_index", current.get("circulation_index", current.get("qi_flow", 0.5)))), 0.5))
    stagnation = _clamp(_f(packet.get("stagnation_index", router.get("stagnation_index", current.get("stagnation_index", 1.0 - circulation))), 1.0 - circulation))
    feedback_action, flow_gain, friction_attenuation, recovery_bias = _feedback_from_action(action, circulation, stagnation)
    if feedback_action == "hold_for_concrete_reason":
        blockers.append("concrete_reason_feedback_hold")
    next_packet = _next_packet(current, feedback_action, flow_gain, friction_attenuation, recovery_bias)
    if blockers:
        status = "QI_CIRCULATION_FEEDBACK_BLOCKED"
    else:
        status = "QI_CIRCULATION_FEEDBACK_READY"
    packet_id = "qi-circulation-feedback-" + _sha({"packet": packet, "next": next_packet, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_circulation_feedback_controller_v2_9", "status": status, "packet_id": packet_id, "feedback_action": feedback_action, "flow_gain": flow_gain, "friction_attenuation": friction_attenuation, "recovery_bias": recovery_bias, "next_qi_packet_digest": _sha(next_packet), "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("next_packet_write_allowed") is True and not blockers:
        _write_json(next_packet_path, next_packet)
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiCirculationFeedbackControllerResult("kuuos_runtime_daemon_qi_circulation_feedback_controller_v2_9", status, packet_id, str(root), str(packet_path), str(next_packet_path), str(receipt_path), str(audit_path), feedback_action, flow_gain, friction_attenuation, recovery_bias, next_packet, blockers, warnings)
