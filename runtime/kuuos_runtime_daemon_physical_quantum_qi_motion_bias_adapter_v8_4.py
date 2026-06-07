#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


PATH_TO_MOTION = {
    "stay_safely": {
        "motion_mode": "hold",
        "progress_action": "hold_but_require_exit_condition",
        "max_bridge_cycles": 1,
        "max_loop_steps_per_cycle": 1,
        "review_exit_required": True,
        "small_probe_required": False,
    },
    "light_progress": {
        "motion_mode": "continue",
        "progress_action": "advance_light",
        "max_bridge_cycles": 3,
        "max_loop_steps_per_cycle": 3,
        "review_exit_required": False,
        "small_probe_required": False,
    },
    "observe_probe": {
        "motion_mode": "observe",
        "progress_action": "observe_then_replan",
        "max_bridge_cycles": 2,
        "max_loop_steps_per_cycle": 2,
        "review_exit_required": False,
        "small_probe_required": True,
    },
    "rebalance_retry": {
        "motion_mode": "retry",
        "progress_action": "rebalance_then_retry",
        "max_bridge_cycles": 2,
        "max_loop_steps_per_cycle": 3,
        "review_exit_required": False,
        "small_probe_required": True,
    },
    "review_exit": {
        "motion_mode": "hold",
        "progress_action": "hold_but_require_exit_condition",
        "max_bridge_cycles": 1,
        "max_loop_steps_per_cycle": 1,
        "review_exit_required": True,
        "small_probe_required": False,
    },
}

ALLOWED_NEXT_BIAS = {"stable_continue", "observe_more", "retry_heavy", "hold_for_review"}


@dataclass(frozen=True)
class PhysicalQuantumQiMotionBiasAdapterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    dominant_path: str
    motion_mode: str
    next_motion_bias: str
    motion_bias_packet_path: str
    receipt_path: str
    audit_path: str
    motion_bias_packet_written: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _num(value: Any, default: float = 0.0) -> float:
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


def _confidence(path_packet: Mapping[str, Any], dominant: str) -> float:
    weights = path_packet.get("path_amplitude_weights", {})
    if not isinstance(weights, Mapping):
        return 0.0
    return round(_num(weights.get(dominant), 0.0), 6)


def _packet(path_packet: Mapping[str, Any]) -> dict[str, Any]:
    dominant = str(path_packet.get("dominant_path", "observe_probe"))
    profile = dict(PATH_TO_MOTION[dominant])
    next_bias = str(path_packet.get("next_motion_bias", "observe_more"))
    return {
        "version": "physical_quantum_qi_motion_bias_packet_v8_4",
        "physical_quantum_qi_path_integral_used": True,
        "qi_is_relational_field_not_substance": path_packet.get("qi_is_relational_field_not_substance") is True,
        "observe_only_bounded_motion_candidate": True,
        "dominant_path": dominant,
        "stationary_path": str(path_packet.get("stationary_path", dominant)),
        "next_motion_bias": next_bias,
        "motion_mode": profile["motion_mode"],
        "progress_action": profile["progress_action"],
        "max_bridge_cycles": profile["max_bridge_cycles"],
        "max_loop_steps_per_cycle": profile["max_loop_steps_per_cycle"],
        "review_exit_required": profile["review_exit_required"],
        "small_probe_required": profile["small_probe_required"],
        "path_weight_confidence": _confidence(path_packet, dominant),
        "path_integral_action": _num(path_packet.get("path_integral_action"), 0.0),
        "source_path_integral_digest": _sha(dict(path_packet)),
        "boundary": {
            "motion_bias_only": True,
            "does_not_run_runner": True,
            "does_not_overwrite_policy": True,
            "does_not_authorize_execution": True,
            "does_not_authorize_medical_action": True,
            "path_integral_candidate_weighting_preserved": True,
        },
        "epoch": int(time.time()),
    }


def build_physical_quantum_qi_motion_bias_adapter(*, runtime_context: Mapping[str, Any], motion_bias_license: Mapping[str, Any]) -> PhysicalQuantumQiMotionBiasAdapterResult:
    ctx = _m(runtime_context)
    lic = _m(motion_bias_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    path_packet_path = root / "physical_quantum_qi_path_integral_packet.json"
    motion_packet_path = root / "physical_quantum_qi_motion_bias_packet.json"
    receipt_path = root / "physical_quantum_qi_motion_bias_adapter_receipt.json"
    audit_path = root / "physical_quantum_qi_motion_bias_adapter_audit.jsonl"

    if ctx.get("physical_quantum_qi_motion_bias_adapter_enabled") is not True:
        blockers.append("physical_quantum_qi_motion_bias_adapter_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_motion_bias_adapter") is not True:
        blockers.append("apply_physical_quantum_qi_motion_bias_adapter_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_MOTION_BIAS_ADAPTER_LICENSE_READY":
        blockers.append("physical_quantum_qi_motion_bias_adapter_license_not_ready")
    for name in ["path_integral_packet_read_allowed", "motion_bias_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    path_packet = _read_json(path_packet_path)
    if not path_packet:
        blockers.append("physical_quantum_qi_path_integral_packet_missing_or_invalid")
    dominant = str(path_packet.get("dominant_path", "unknown")) if path_packet else "unknown"
    next_bias = str(path_packet.get("next_motion_bias", "unknown")) if path_packet else "unknown"
    if dominant not in PATH_TO_MOTION:
        blockers.append("dominant_path_not_allowlisted")
    if next_bias not in ALLOWED_NEXT_BIAS:
        blockers.append("next_motion_bias_not_allowlisted")
    if path_packet and path_packet.get("observe_only_bounded_motion_candidate") is not True:
        blockers.append("observe_only_bounded_motion_candidate_not_true")
    if path_packet and path_packet.get("boundary", {}).get("path_integral_is_candidate_weighting_not_truth") is not True:
        blockers.append("path_integral_boundary_invalid")

    packet: dict[str, Any] = {}
    written = False
    mode = "unknown"
    if not blockers:
        packet = _packet(path_packet)
        mode = str(packet["motion_mode"])
        _write_json(motion_packet_path, packet)
        written = True

    status = "PHYSICAL_QUANTUM_QI_MOTION_BIAS_ADAPTER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_MOTION_BIAS_ADAPTER_BLOCKED"
    packet_id = "physical-quantum-qi-motion-bias-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_motion_bias_adapter_v8_4",
        "status": status,
        "packet_id": packet_id,
        "dominant_path": dominant,
        "motion_mode": mode,
        "next_motion_bias": next_bias,
        "motion_bias_packet_written": written,
        "motion_bias_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return PhysicalQuantumQiMotionBiasAdapterResult(
        "kuuos_runtime_daemon_physical_quantum_qi_motion_bias_adapter_v8_4",
        status,
        packet_id,
        str(root),
        dominant,
        mode,
        next_bias,
        str(motion_packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
