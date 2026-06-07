#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


MOTION_TO_PROGRESS_CLASS = {
    "continue": "safe_progress_continue",
    "observe": "observe_with_progress_obligation",
    "retry": "retry_with_rebalance_probe",
    "hold": "hold_with_review_exit",
}

ALLOWED_MOTION_MODES = set(MOTION_TO_PROGRESS_CLASS)
ALLOWED_PROGRESS_ACTIONS = {
    "advance_light",
    "observe_then_replan",
    "rebalance_then_retry",
    "hold_but_require_exit_condition",
}


@dataclass(frozen=True)
class PhysicalQuantumQiMotionToRunnerAdapterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    motion_mode: str
    progress_class: str
    runner_packet_path: str
    receipt_path: str
    audit_path: str
    runner_packet_written: bool
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


def _bounded(value: int, low: int = 1, high: int = 20) -> int:
    return max(low, min(high, value))


def _runner_packet(motion: Mapping[str, Any]) -> dict[str, Any]:
    mode = str(motion.get("motion_mode", "observe"))
    progress_class = MOTION_TO_PROGRESS_CLASS[mode]
    cycles = _bounded(_i(motion.get("max_bridge_cycles"), 1))
    steps = _bounded(_i(motion.get("max_loop_steps_per_cycle"), 1))
    if motion.get("small_probe_required") is True:
        cycles = min(cycles, 3)
        steps = min(steps, 3)
    if motion.get("review_exit_required") is True:
        cycles = 1
        steps = 1
    return {
        "version": "qi_progress_aware_runner_packet_v8_5_from_physical_quantum_qi",
        "physical_quantum_qi_motion_bias_used": True,
        "runner_mode": mode,
        "progress_class": progress_class,
        "progress_action": str(motion.get("progress_action", "observe_then_replan")),
        "max_bridge_cycles": cycles,
        "max_loop_steps_per_cycle": steps,
        "progress_required": True,
        "small_probe_required": motion.get("small_probe_required") is True,
        "review_exit_required": motion.get("review_exit_required") is True,
        "dominant_path": str(motion.get("dominant_path", "unknown")),
        "next_motion_bias": str(motion.get("next_motion_bias", "unknown")),
        "path_weight_confidence": round(_num(motion.get("path_weight_confidence"), 0.0), 6),
        "source_motion_bias_digest": _sha(dict(motion)),
        "boundary": {
            "progress_obligation_preserved": True,
            "runner_packet_only": True,
            "does_not_run_runner": True,
            "does_not_authorize_medical_action": True,
            "path_integral_candidate_weighting_preserved": True,
        },
        "epoch": int(time.time()),
    }


def build_physical_quantum_qi_motion_to_runner_adapter(*, runtime_context: Mapping[str, Any], motion_to_runner_license: Mapping[str, Any]) -> PhysicalQuantumQiMotionToRunnerAdapterResult:
    ctx = _m(runtime_context)
    lic = _m(motion_to_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    motion_path = root / "physical_quantum_qi_motion_bias_packet.json"
    runner_path = root / "qi_progress_aware_runner_packet.json"
    receipt_path = root / "physical_quantum_qi_motion_to_runner_adapter_receipt.json"
    audit_path = root / "physical_quantum_qi_motion_to_runner_adapter_audit.jsonl"

    if ctx.get("physical_quantum_qi_motion_to_runner_adapter_enabled") is not True:
        blockers.append("physical_quantum_qi_motion_to_runner_adapter_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_motion_to_runner_adapter") is not True:
        blockers.append("apply_physical_quantum_qi_motion_to_runner_adapter_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_MOTION_TO_RUNNER_ADAPTER_LICENSE_READY":
        blockers.append("physical_quantum_qi_motion_to_runner_adapter_license_not_ready")
    for name in ["motion_bias_packet_read_allowed", "runner_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    motion = _read_json(motion_path)
    if not motion:
        blockers.append("physical_quantum_qi_motion_bias_packet_missing_or_invalid")
    mode = str(motion.get("motion_mode", "unknown")) if motion else "unknown"
    action = str(motion.get("progress_action", "unknown")) if motion else "unknown"
    if mode not in ALLOWED_MOTION_MODES:
        blockers.append("motion_mode_not_allowlisted")
    if action not in ALLOWED_PROGRESS_ACTIONS:
        blockers.append("progress_action_not_allowlisted")
    if motion and motion.get("observe_only_bounded_motion_candidate") is not True:
        blockers.append("observe_only_bounded_motion_candidate_not_true")
    if motion and motion.get("boundary", {}).get("motion_bias_only") is not True:
        blockers.append("motion_bias_boundary_invalid")
    if motion and motion.get("boundary", {}).get("does_not_authorize_execution") is not True:
        blockers.append("execution_authority_boundary_invalid")

    packet: dict[str, Any] = {}
    written = False
    progress_class = "unknown"
    if not blockers:
        packet = _runner_packet(motion)
        progress_class = str(packet["progress_class"])
        _write_json(runner_path, packet)
        written = True

    status = "PHYSICAL_QUANTUM_QI_MOTION_TO_RUNNER_ADAPTER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_MOTION_TO_RUNNER_ADAPTER_BLOCKED"
    packet_id = "physical-quantum-qi-motion-to-runner-" + _sha({"motion": motion, "packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_motion_to_runner_adapter_v8_5",
        "status": status,
        "packet_id": packet_id,
        "motion_mode": mode,
        "progress_class": progress_class,
        "runner_packet_written": written,
        "runner_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return PhysicalQuantumQiMotionToRunnerAdapterResult(
        "kuuos_runtime_daemon_physical_quantum_qi_motion_to_runner_adapter_v8_5",
        status,
        packet_id,
        str(root),
        mode,
        progress_class,
        str(runner_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
