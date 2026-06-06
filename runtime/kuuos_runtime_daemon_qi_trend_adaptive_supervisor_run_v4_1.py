#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_process_tensor_cycle_supervisor_v3_8 import build_qi_process_tensor_cycle_supervisor


@dataclass(frozen=True)
class QiTrendAdaptiveSupervisorRunResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    next_supervisor_packet_path: str
    receipt_path: str
    audit_path: str
    adaptation_class: str
    supervisor_status: str
    stop_reason: str
    cycles_run: int
    max_supervised_cycles: int
    max_trajectory_records: int
    run_performed: bool
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


def _supervisor_license(packet: Mapping[str, Any]) -> dict[str, Any]:
    hint = dict(_m(packet.get("license_hint")))
    base = {
        "license_status": "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_LICENSE_READY",
        "cycle_runner_run_allowed": True,
        "state_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    base.update(hint)
    return base


def _supervisor_context(root: pathlib.Path, packet: Mapping[str, Any]) -> tuple[dict[str, Any], int, int, list[str]]:
    warnings: list[str] = []
    context = dict(_m(packet.get("supervisor_context")))
    patch = dict(_m(packet.get("runtime_context_patch")))
    context.update(patch)
    max_cycles = _i(context.get("max_supervised_cycles"), 3)
    max_records = _i(context.get("max_trajectory_records"), 50)
    if max_cycles < 1:
        warnings.append("max_supervised_cycles_below_one_passed_to_supervisor")
    if max_records < 1:
        warnings.append("max_trajectory_records_below_one_passed_to_supervisor")
    return {
        "qi_process_tensor_cycle_supervisor_enabled": True,
        "apply_process_tensor_cycle_supervisor": True,
        "runtime_root": str(root),
        "max_supervised_cycles": max_cycles,
        "max_trajectory_records": max_records,
    }, max_cycles, max_records, warnings


def build_qi_trend_adaptive_supervisor_run(*, runtime_context: Mapping[str, Any], adaptive_run_license: Mapping[str, Any]) -> QiTrendAdaptiveSupervisorRunResult:
    ctx = _m(runtime_context)
    lic = _m(adaptive_run_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    next_supervisor_packet_path = root / "next_qi_process_tensor_cycle_supervisor_packet.json"
    receipt_path = root / "qi_trend_adaptive_supervisor_run_receipt.json"
    audit_path = root / "qi_trend_adaptive_supervisor_run_audit.jsonl"

    if ctx.get("qi_trend_adaptive_supervisor_run_enabled") is not True:
        blockers.append("qi_trend_adaptive_supervisor_run_enabled_not_true")
    if ctx.get("apply_trend_adaptive_supervisor_run") is not True:
        blockers.append("apply_trend_adaptive_supervisor_run_not_true")
    if lic.get("license_status") != "QI_TREND_ADAPTIVE_SUPERVISOR_RUN_LICENSE_READY":
        blockers.append("trend_adaptive_supervisor_run_license_not_ready")
    for name in ["next_supervisor_packet_read_allowed", "supervisor_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    if not (root / "qi_circulation_trajectory_packet.json").is_file():
        blockers.append("trajectory_packet_missing")
    if not (root / "qi_process_tensor_packet.json").is_file():
        blockers.append("process_tensor_packet_missing")

    packet = _read_json(next_supervisor_packet_path)
    if not packet:
        blockers.append("next_supervisor_packet_missing_or_invalid")
    if packet and _m(packet.get("boundary")).get("suggested_packet_only") is not True:
        warnings.append("suggested_packet_only_boundary_not_visible")

    supervisor_context, max_cycles, max_records, context_warnings = _supervisor_context(root, packet)
    warnings.extend(context_warnings)
    adaptation_class = str(packet.get("adaptation_class", "unknown")) if packet else "unknown"
    supervisor_payload: dict[str, Any] = {}
    run_performed = False
    supervisor_status = "NOT_RUN"
    stop_reason = "not_run"
    cycles_run = 0

    if not blockers:
        supervisor = build_qi_process_tensor_cycle_supervisor(
            runtime_context=supervisor_context,
            supervisor_license_packet=_supervisor_license(packet),
        )
        supervisor_payload = supervisor.to_dict()
        run_performed = True
        supervisor_status = str(supervisor_payload.get("status", "unknown"))
        stop_reason = str(supervisor_payload.get("stop_reason", "unknown"))
        cycles_run = _i(supervisor_payload.get("cycles_run"), 0)
        if supervisor_status != "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_READY":
            blockers.append("cycle_supervisor_not_ready")

    status = "QI_TREND_ADAPTIVE_SUPERVISOR_RUN_READY" if not blockers else "QI_TREND_ADAPTIVE_SUPERVISOR_RUN_BLOCKED"
    packet_id = "qi-trend-adaptive-supervisor-run-" + _sha({"packet": packet, "supervisor": supervisor_payload, "blockers": blockers})[:16]
    out_receipt = {
        "version": "kuuos_runtime_daemon_qi_trend_adaptive_supervisor_run_v4_1",
        "status": status,
        "packet_id": packet_id,
        "adaptation_class": adaptation_class,
        "supervisor_status": supervisor_status,
        "stop_reason": stop_reason,
        "cycles_run": cycles_run,
        "max_supervised_cycles": max_cycles,
        "max_trajectory_records": max_records,
        "run_performed": run_performed,
        "next_supervisor_packet_digest": _sha(packet),
        "supervisor_result_digest": _sha(supervisor_payload),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, out_receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**out_receipt, "record_digest": _sha(out_receipt)})
    return QiTrendAdaptiveSupervisorRunResult(
        "kuuos_runtime_daemon_qi_trend_adaptive_supervisor_run_v4_1",
        status,
        packet_id,
        str(root),
        str(next_supervisor_packet_path),
        str(receipt_path),
        str(audit_path),
        adaptation_class,
        supervisor_status,
        stop_reason,
        cycles_run,
        max_cycles,
        max_records,
        run_performed,
        blockers,
        warnings,
    )
