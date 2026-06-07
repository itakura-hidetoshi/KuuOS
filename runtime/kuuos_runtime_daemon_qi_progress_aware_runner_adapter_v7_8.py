#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ALLOWED_PROGRESS_CLASSES = {
    "safe_progress_continue",
    "observe_with_progress_obligation",
    "retry_with_rebalance_probe",
    "hold_with_review_exit",
    "progress_gap_detected",
}

ACTION_TO_MODE = {
    "advance_light": "continue",
    "observe_then_replan": "observe",
    "rebalance_then_retry": "retry",
    "hold_but_require_exit_condition": "hold",
    "open_small_probe_or_review_exit": "observe",
}


@dataclass(frozen=True)
class QiProgressAwareRunnerAdapterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    progress_class: str
    runner_mode: str
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


def _packet(safety: Mapping[str, Any]) -> dict[str, Any]:
    action = str(safety.get("progress_action", "observe_then_replan"))
    mode = ACTION_TO_MODE.get(action, "observe")
    cycles = max(1, _i(safety.get("suggested_max_bridge_cycles"), 1))
    steps = max(1, _i(safety.get("suggested_max_loop_steps_per_cycle"), 1))
    if safety.get("small_probe_required") is True:
        cycles = min(cycles, 3)
        steps = min(steps, 3)
    if safety.get("review_exit_required") is True:
        cycles = 1
        steps = 1
    return {
        "version": "qi_progress_aware_runner_packet_v7_8",
        "runner_mode": mode,
        "progress_class": str(safety.get("progress_class", "unknown")),
        "progress_action": action,
        "max_bridge_cycles": cycles,
        "max_loop_steps_per_cycle": steps,
        "progress_required": True,
        "small_probe_required": safety.get("small_probe_required") is True,
        "review_exit_required": safety.get("review_exit_required") is True,
        "source_safety_digest": _sha(dict(safety)),
        "boundary": {
            "runner_adapter_only": True,
            "does_not_run_runner": True,
            "progress_obligation_preserved": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_progress_aware_runner_adapter(*, runtime_context: Mapping[str, Any], progress_runner_adapter_license: Mapping[str, Any]) -> QiProgressAwareRunnerAdapterResult:
    ctx = _m(runtime_context)
    lic = _m(progress_runner_adapter_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    safety_path = root / "qi_progress_bearing_safety_packet.json"
    runner_path = root / "qi_progress_aware_runner_packet.json"
    receipt_path = root / "qi_progress_aware_runner_adapter_receipt.json"
    audit_path = root / "qi_progress_aware_runner_adapter_audit.jsonl"

    if ctx.get("qi_progress_aware_runner_adapter_enabled") is not True:
        blockers.append("qi_progress_aware_runner_adapter_enabled_not_true")
    if ctx.get("apply_qi_progress_aware_runner_adapter") is not True:
        blockers.append("apply_qi_progress_aware_runner_adapter_not_true")
    if lic.get("license_status") != "QI_PROGRESS_AWARE_RUNNER_ADAPTER_LICENSE_READY":
        blockers.append("qi_progress_aware_runner_adapter_license_not_ready")
    for name in ["safety_packet_read_allowed", "runner_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    safety = _read_json(safety_path)
    if not safety:
        blockers.append("qi_progress_bearing_safety_packet_missing_or_invalid")
    progress_class = str(safety.get("progress_class", "unknown")) if safety else "unknown"
    action = str(safety.get("progress_action", "unknown")) if safety else "unknown"
    if progress_class not in ALLOWED_PROGRESS_CLASSES:
        blockers.append("progress_class_not_allowlisted")
    if action not in ACTION_TO_MODE:
        blockers.append("progress_action_not_mapped")
    if safety and safety.get("progress_required") is not True:
        blockers.append("progress_required_not_true")
    if safety and safety.get("boundary", {}).get("progress_bearing_safety") is not True:
        blockers.append("progress_safety_boundary_invalid")

    packet: dict[str, Any] = {}
    written = False
    mode = "unknown"
    if not blockers:
        packet = _packet(safety)
        mode = str(packet["runner_mode"])
        _write_json(runner_path, packet)
        written = True

    status = "QI_PROGRESS_AWARE_RUNNER_ADAPTER_READY" if not blockers else "QI_PROGRESS_AWARE_RUNNER_ADAPTER_BLOCKED"
    packet_id = "qi-progress-aware-runner-adapter-" + _sha({"safety": safety, "packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_progress_aware_runner_adapter_v7_8",
        "status": status,
        "packet_id": packet_id,
        "progress_class": progress_class,
        "runner_mode": mode,
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
    return QiProgressAwareRunnerAdapterResult(
        "kuuos_runtime_daemon_qi_progress_aware_runner_adapter_v7_8",
        status,
        packet_id,
        str(root),
        progress_class,
        mode,
        str(runner_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
