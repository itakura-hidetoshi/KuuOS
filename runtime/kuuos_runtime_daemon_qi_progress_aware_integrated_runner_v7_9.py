#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_integrated_bridge_runner_v6_8 import build_qi_github_actions_integrated_bridge_runner


ALLOWED_MODES = {"continue", "observe", "retry", "hold"}
ALLOWED_PROGRESS_CLASSES = {
    "safe_progress_continue",
    "observe_with_progress_obligation",
    "retry_with_rebalance_probe",
    "hold_with_review_exit",
    "progress_gap_detected",
}


@dataclass(frozen=True)
class QiProgressAwareIntegratedRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    runner_mode: str
    progress_class: str
    execution_class: str
    integrated_runner_status: str
    receipt_path: str
    audit_path: str
    integrated_runner_invoked: bool
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


def _integrated_context(root: pathlib.Path, runner_packet: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "qi_github_actions_integrated_bridge_runner_enabled": True,
        "apply_github_actions_integrated_bridge_runner": True,
        "runtime_root": str(root),
        "max_bridge_cycles": _i(runner_packet.get("max_bridge_cycles"), 1),
        "max_loop_steps_per_cycle": _i(runner_packet.get("max_loop_steps_per_cycle"), 1),
    }


def _integrated_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_LICENSE_READY",
        "internal_loop_run_allowed": True,
        "external_bridge_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_qi_progress_aware_integrated_runner(*, runtime_context: Mapping[str, Any], progress_integrated_runner_license: Mapping[str, Any]) -> QiProgressAwareIntegratedRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(progress_integrated_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    runner_packet_path = root / "qi_progress_aware_runner_packet.json"
    receipt_path = root / "qi_progress_aware_integrated_runner_receipt.json"
    audit_path = root / "qi_progress_aware_integrated_runner_audit.jsonl"

    if ctx.get("qi_progress_aware_integrated_runner_enabled") is not True:
        blockers.append("qi_progress_aware_integrated_runner_enabled_not_true")
    if ctx.get("apply_qi_progress_aware_integrated_runner") is not True:
        blockers.append("apply_qi_progress_aware_integrated_runner_not_true")
    if lic.get("license_status") != "QI_PROGRESS_AWARE_INTEGRATED_RUNNER_LICENSE_READY":
        blockers.append("qi_progress_aware_integrated_runner_license_not_ready")
    for name in ["runner_packet_read_allowed", "integrated_runner_invoke_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    runner_packet = _read_json(runner_packet_path)
    if not runner_packet:
        blockers.append("qi_progress_aware_runner_packet_missing_or_invalid")
    runner_mode = str(runner_packet.get("runner_mode", "unknown")) if runner_packet else "unknown"
    progress_class = str(runner_packet.get("progress_class", "unknown")) if runner_packet else "unknown"
    if runner_mode not in ALLOWED_MODES:
        blockers.append("runner_mode_not_allowlisted")
    if progress_class not in ALLOWED_PROGRESS_CLASSES:
        blockers.append("progress_class_not_allowlisted")
    if runner_packet and runner_packet.get("progress_required") is not True:
        blockers.append("progress_required_not_true")
    if runner_packet and runner_packet.get("boundary", {}).get("progress_obligation_preserved") is not True:
        blockers.append("runner_packet_boundary_invalid")
    cycles = _i(runner_packet.get("max_bridge_cycles"), 0) if runner_packet else 0
    steps = _i(runner_packet.get("max_loop_steps_per_cycle"), 0) if runner_packet else 0
    if runner_packet and (cycles < 1 or steps < 1):
        blockers.append("runner_packet_limits_invalid")

    integrated_result: Mapping[str, Any] = {}
    invoked = False
    execution_class = "not_run"
    integrated_status = "NOT_RUN"
    if not blockers:
        if runner_mode == "hold":
            execution_class = "progress_hold_with_exit"
            integrated_status = "HELD_WITH_EXIT"
        else:
            integrated_result = build_qi_github_actions_integrated_bridge_runner(
                runtime_context=_integrated_context(root, runner_packet),
                integrated_bridge_runner_license=_integrated_license(),
            ).to_dict()
            invoked = True
            integrated_status = str(integrated_result.get("status", "unknown"))
            if integrated_status == "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_READY":
                execution_class = "progress_runner_completed"
            else:
                blockers.append("integrated_runner_not_ready")
                execution_class = "progress_runner_blocked"

    status = "QI_PROGRESS_AWARE_INTEGRATED_RUNNER_READY" if not blockers else "QI_PROGRESS_AWARE_INTEGRATED_RUNNER_BLOCKED"
    packet_id = "qi-progress-aware-integrated-runner-" + _sha({"runner_packet": runner_packet, "integrated": dict(integrated_result), "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_progress_aware_integrated_runner_v7_9",
        "status": status,
        "packet_id": packet_id,
        "runner_mode": runner_mode,
        "progress_class": progress_class,
        "execution_class": execution_class,
        "integrated_runner_status": integrated_status,
        "integrated_runner_invoked": invoked,
        "runner_packet_digest": _sha(runner_packet),
        "integrated_result_digest": _sha(dict(integrated_result)),
        "progress_exit_preserved": runner_mode == "hold" or runner_packet.get("review_exit_required") is True,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiProgressAwareIntegratedRunnerResult(
        "kuuos_runtime_daemon_qi_progress_aware_integrated_runner_v7_9",
        status,
        packet_id,
        str(root),
        runner_mode,
        progress_class,
        execution_class,
        integrated_status,
        str(receipt_path),
        str(audit_path),
        invoked,
        blockers,
        warnings,
    )
