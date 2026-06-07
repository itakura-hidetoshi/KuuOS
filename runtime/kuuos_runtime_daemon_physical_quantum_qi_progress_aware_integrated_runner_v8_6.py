#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_progress_aware_integrated_runner_v7_9 import build_qi_progress_aware_integrated_runner


ALLOWED_RUNNER_MODES = {"continue", "observe", "retry", "hold"}
ALLOWED_PROGRESS_CLASSES = {
    "safe_progress_continue",
    "observe_with_progress_obligation",
    "retry_with_rebalance_probe",
    "hold_with_review_exit",
    "progress_gap_detected",
}


@dataclass(frozen=True)
class PhysicalQuantumQiProgressAwareIntegratedRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    runner_mode: str
    progress_class: str
    execution_class: str
    delegated_runner_status: str
    receipt_path: str
    audit_path: str
    delegated_runner_invoked: bool
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


def _delegate_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_progress_aware_integrated_runner_enabled": True,
        "apply_qi_progress_aware_integrated_runner": True,
        "runtime_root": str(root),
    }


def _delegate_license() -> dict[str, Any]:
    return {
        "license_status": "QI_PROGRESS_AWARE_INTEGRATED_RUNNER_LICENSE_READY",
        "runner_packet_read_allowed": True,
        "integrated_runner_invoke_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_physical_quantum_qi_progress_aware_integrated_runner(*, runtime_context: Mapping[str, Any], physical_qi_runner_license: Mapping[str, Any]) -> PhysicalQuantumQiProgressAwareIntegratedRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(physical_qi_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    runner_packet_path = root / "qi_progress_aware_runner_packet.json"
    receipt_path = root / "physical_quantum_qi_progress_aware_integrated_runner_receipt.json"
    audit_path = root / "physical_quantum_qi_progress_aware_integrated_runner_audit.jsonl"

    if ctx.get("physical_quantum_qi_progress_aware_integrated_runner_enabled") is not True:
        blockers.append("physical_quantum_qi_progress_aware_integrated_runner_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_progress_aware_integrated_runner") is not True:
        blockers.append("apply_physical_quantum_qi_progress_aware_integrated_runner_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_PROGRESS_AWARE_INTEGRATED_RUNNER_LICENSE_READY":
        blockers.append("physical_quantum_qi_progress_aware_integrated_runner_license_not_ready")
    for name in ["runner_packet_read_allowed", "delegated_runner_invoke_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(runner_packet_path)
    if not packet:
        blockers.append("qi_progress_aware_runner_packet_missing_or_invalid")
    runner_mode = str(packet.get("runner_mode", "unknown")) if packet else "unknown"
    progress_class = str(packet.get("progress_class", "unknown")) if packet else "unknown"
    if runner_mode not in ALLOWED_RUNNER_MODES:
        blockers.append("runner_mode_not_allowlisted")
    if progress_class not in ALLOWED_PROGRESS_CLASSES:
        blockers.append("progress_class_not_allowlisted")
    if packet and packet.get("physical_quantum_qi_motion_bias_used") is not True:
        blockers.append("physical_quantum_qi_motion_bias_used_not_true")
    if packet and packet.get("progress_required") is not True:
        blockers.append("progress_required_not_true")
    if packet and packet.get("boundary", {}).get("path_integral_candidate_weighting_preserved") is not True:
        blockers.append("path_integral_candidate_weighting_boundary_invalid")
    if packet and (_i(packet.get("max_bridge_cycles"), 0) < 1 or _i(packet.get("max_loop_steps_per_cycle"), 0) < 1):
        blockers.append("runner_packet_limits_invalid")

    delegated_result: Mapping[str, Any] = {}
    invoked = False
    delegated_status = "NOT_RUN"
    execution_class = "not_run"
    if not blockers:
        delegated_result = build_qi_progress_aware_integrated_runner(
            runtime_context=_delegate_context(root),
            progress_integrated_runner_license=_delegate_license(),
        ).to_dict()
        invoked = bool(delegated_result.get("integrated_runner_invoked", False))
        delegated_status = str(delegated_result.get("status", "unknown"))
        if delegated_status == "QI_PROGRESS_AWARE_INTEGRATED_RUNNER_READY":
            execution_class = str(delegated_result.get("execution_class", "unknown"))
        else:
            execution_class = "physical_qi_delegated_runner_blocked"
            blockers.append("delegated_progress_aware_runner_not_ready")

    status = "PHYSICAL_QUANTUM_QI_PROGRESS_AWARE_INTEGRATED_RUNNER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_PROGRESS_AWARE_INTEGRATED_RUNNER_BLOCKED"
    packet_id = "physical-quantum-qi-progress-runner-" + _sha({"packet": packet, "delegated": dict(delegated_result), "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_progress_aware_integrated_runner_v8_6",
        "status": status,
        "packet_id": packet_id,
        "runner_mode": runner_mode,
        "progress_class": progress_class,
        "execution_class": execution_class,
        "delegated_runner_status": delegated_status,
        "delegated_runner_invoked": invoked,
        "physical_quantum_qi_motion_bias_used": packet.get("physical_quantum_qi_motion_bias_used") is True if packet else False,
        "path_integral_candidate_weighting_preserved": packet.get("boundary", {}).get("path_integral_candidate_weighting_preserved") is True if packet else False,
        "runner_packet_digest": _sha(packet),
        "delegated_result_digest": _sha(dict(delegated_result)),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return PhysicalQuantumQiProgressAwareIntegratedRunnerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_progress_aware_integrated_runner_v8_6",
        status,
        packet_id,
        str(root),
        runner_mode,
        progress_class,
        execution_class,
        delegated_status,
        str(receipt_path),
        str(audit_path),
        invoked,
        blockers,
        warnings,
    )
