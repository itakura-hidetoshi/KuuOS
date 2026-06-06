#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_process_tensor_cycle_runner_v3_7 import build_qi_process_tensor_cycle_runner


@dataclass(frozen=True)
class QiProcessTensorCycleSupervisorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    state_path: str
    receipt_path: str
    audit_path: str
    cycles_requested: int
    cycles_run: int
    stop_reason: str
    final_cycle_status: str
    final_scheduled_status: str
    final_trajectory_length: int
    completed: bool
    blockers: list[str]
    warnings: list[str]
    cycle_records: list[dict[str, Any]]

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


def _cycle_runner_license() -> dict[str, Any]:
    return {
        "license_status": "QI_PROCESS_TENSOR_CYCLE_RUNNER_LICENSE_READY",
        "return_loop_run_allowed": True,
        "scheduled_closed_loop_run_allowed": True,
        "trajectory_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _cycle_context(root: pathlib.Path, max_trajectory_records: int) -> dict[str, Any]:
    return {
        "qi_process_tensor_cycle_runner_enabled": True,
        "apply_process_tensor_cycle_runner": True,
        "runtime_root": str(root),
        "max_trajectory_records": max_trajectory_records,
    }


def _last_stage(records: list[Mapping[str, Any]], stage: str) -> Mapping[str, Any]:
    for record in reversed(records):
        if record.get("stage") == stage:
            return record
    return {}


def _classify_stop(cycle_payload: Mapping[str, Any], previous_trajectory_len: int | None) -> str:
    if cycle_payload.get("status") != "QI_PROCESS_TENSOR_CYCLE_RUNNER_READY":
        return "blocked"
    records = [item for item in cycle_payload.get("stage_records", []) if isinstance(item, Mapping)]
    return_record = _last_stage(records, "return_loop_orchestrator_v3_6")
    if return_record and "hold" in str(return_record.get("digest", "")):
        return "continue"
    final = _m(cycle_payload.get("final_qi_packet", {}))
    scheduled_status = str(cycle_payload.get("scheduled_closed_loop_status", ""))
    trajectory_len = _i(cycle_payload.get("trajectory_length"), 0)
    if final.get("critical_blocker_present") is True or final.get("process_tensor_hold_required") is True:
        return "hold_overlay"
    if scheduled_status == "QI_SCHEDULED_CLOSED_LOOP_CONVERGED":
        return "converged"
    if previous_trajectory_len is not None and trajectory_len <= previous_trajectory_len:
        return "no_progress"
    return "continue"


def _cycle_record(index: int, cycle_payload: Mapping[str, Any], stop_reason: str) -> dict[str, Any]:
    return {
        "cycle_index": index,
        "cycle_status": str(cycle_payload.get("status", "unknown")),
        "scheduled_closed_loop_status": str(cycle_payload.get("scheduled_closed_loop_status", "unknown")),
        "trajectory_length": _i(cycle_payload.get("trajectory_length"), 0),
        "stop_reason_after_cycle": stop_reason,
        "packet_id": str(cycle_payload.get("packet_id", "unknown")),
        "digest": _sha(dict(cycle_payload)),
        "epoch": int(time.time()),
    }


def build_qi_process_tensor_cycle_supervisor(*, runtime_context: Mapping[str, Any], supervisor_license_packet: Mapping[str, Any]) -> QiProcessTensorCycleSupervisorResult:
    ctx = _m(runtime_context)
    lic = _m(supervisor_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    state_path = root / "qi_process_tensor_cycle_supervisor_state.json"
    receipt_path = root / "qi_process_tensor_cycle_supervisor_receipt.json"
    audit_path = root / "qi_process_tensor_cycle_supervisor_audit.jsonl"

    if ctx.get("qi_process_tensor_cycle_supervisor_enabled") is not True:
        blockers.append("qi_process_tensor_cycle_supervisor_enabled_not_true")
    if ctx.get("apply_process_tensor_cycle_supervisor") is not True:
        blockers.append("apply_process_tensor_cycle_supervisor_not_true")
    if lic.get("license_status") != "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_LICENSE_READY":
        blockers.append("process_tensor_cycle_supervisor_license_not_ready")
    for name in ["cycle_runner_run_allowed", "state_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    if not (root / "qi_circulation_trajectory_packet.json").is_file():
        blockers.append("trajectory_packet_missing")
    if not (root / "qi_process_tensor_packet.json").is_file():
        blockers.append("process_tensor_packet_missing")

    cycles_requested = _i(ctx.get("max_supervised_cycles"), 3)
    if cycles_requested < 1:
        blockers.append("max_supervised_cycles_invalid")
        cycles_requested = 0
    if cycles_requested > 20:
        warnings.append("max_supervised_cycles_capped_to_20")
        cycles_requested = 20
    max_trajectory_records = _i(ctx.get("max_trajectory_records"), 50)
    if max_trajectory_records < 1:
        blockers.append("max_trajectory_records_invalid")
        max_trajectory_records = 1

    cycle_records: list[dict[str, Any]] = []
    stop_reason = "not_run"
    final_cycle_status = "NOT_RUN"
    final_scheduled_status = "NOT_RUN"
    final_trajectory_length = 0
    previous_len: int | None = None

    if not blockers:
        for idx in range(1, cycles_requested + 1):
            result = build_qi_process_tensor_cycle_runner(
                runtime_context=_cycle_context(root, max_trajectory_records),
                cycle_runner_license_packet=_cycle_runner_license(),
            )
            payload = result.to_dict()
            final_cycle_status = str(payload.get("status", "unknown"))
            final_scheduled_status = str(payload.get("scheduled_closed_loop_status", "unknown"))
            final_trajectory_length = _i(payload.get("trajectory_length"), 0)
            stop_reason = _classify_stop(payload, previous_len)
            cycle_records.append(_cycle_record(idx, payload, stop_reason))
            previous_len = final_trajectory_length
            if stop_reason != "continue":
                break
        else:
            stop_reason = "cycle_cap_reached"
            if cycle_records:
                cycle_records[-1]["stop_reason_after_cycle"] = stop_reason

    completed = not blockers and bool(cycle_records)
    status = "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_READY" if completed else "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_BLOCKED"
    state = {
        "version": "kuuos_runtime_daemon_qi_process_tensor_cycle_supervisor_v3_8",
        "last_status": status,
        "last_stop_reason": stop_reason,
        "cycles_requested": cycles_requested,
        "cycles_run": len(cycle_records),
        "final_cycle_status": final_cycle_status,
        "final_scheduled_status": final_scheduled_status,
        "final_trajectory_length": final_trajectory_length,
        "cycle_records": cycle_records[-20:],
        "updated_epoch": int(time.time()),
    }
    if lic.get("state_write_allowed") is True:
        _write_json(state_path, state)
    packet_id = "qi-pt-cycle-supervisor-" + _sha({"state": state, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_process_tensor_cycle_supervisor_v3_8",
        "status": status,
        "packet_id": packet_id,
        "cycles_requested": cycles_requested,
        "cycles_run": len(cycle_records),
        "stop_reason": stop_reason,
        "final_cycle_status": final_cycle_status,
        "final_scheduled_status": final_scheduled_status,
        "final_trajectory_length": final_trajectory_length,
        "completed": completed,
        "state_digest": _sha(state),
        "blockers": blockers,
        "warnings": warnings,
        "cycle_records": cycle_records,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiProcessTensorCycleSupervisorResult(
        "kuuos_runtime_daemon_qi_process_tensor_cycle_supervisor_v3_8",
        status,
        packet_id,
        str(root),
        str(state_path),
        str(receipt_path),
        str(audit_path),
        cycles_requested,
        len(cycle_records),
        stop_reason,
        final_cycle_status,
        final_scheduled_status,
        final_trajectory_length,
        completed,
        blockers,
        warnings,
        cycle_records,
    )
