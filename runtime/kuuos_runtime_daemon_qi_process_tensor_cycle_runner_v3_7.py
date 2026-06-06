#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_process_tensor_return_loop_orchestrator_v3_6 import build_qi_process_tensor_return_loop
from runtime.kuuos_runtime_daemon_qi_scheduled_closed_loop_runner_v3_2 import build_qi_scheduled_closed_loop_runner


@dataclass(frozen=True)
class QiProcessTensorCycleRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    receipt_path: str
    audit_path: str
    return_loop_status: str
    scheduled_closed_loop_status: str
    trajectory_appended: bool
    trajectory_length: int
    cycle_completed: bool
    final_qi_packet: dict[str, Any]
    blockers: list[str]
    warnings: list[str]
    stage_records: list[dict[str, Any]]

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


def _return_loop_license() -> dict[str, Any]:
    return {
        "license_status": "QI_PROCESS_TENSOR_RETURN_LOOP_LICENSE_READY",
        "trajectory_adaptor_run_allowed": True,
        "scheduler_packet_run_allowed": True,
        "process_tensor_overlay_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _scheduled_closed_loop_license() -> dict[str, Any]:
    return {
        "license_status": "QI_SCHEDULED_CLOSED_LOOP_LICENSE_READY",
        "packet_read_allowed": True,
        "scheduler_run_allowed": True,
        "closed_loop_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _record(stage: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage": stage,
        "status": str(payload.get("status") or "unknown"),
        "packet_id": str(payload.get("packet_id") or "unknown"),
        "digest": _sha(dict(payload)),
        "epoch": int(time.time()),
    }


def _trajectory_records(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = packet.get("trajectory", [])
    if isinstance(raw, list):
        return [dict(item) for item in raw if isinstance(item, Mapping)]
    return []


def _scheduled_record(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "status": str(payload.get("status", "unknown")),
        "objective_class": str(payload.get("objective_class", "unknown")),
        "converged": payload.get("converged") is True,
        "cycle_count": _i(payload.get("cycle_count"), 0),
        "final_qi_packet": dict(payload.get("final_qi_packet", {})) if isinstance(payload.get("final_qi_packet"), Mapping) else {},
        "scheduler_status": str(payload.get("scheduler_status", "unknown")),
        "closed_loop_status": str(payload.get("closed_loop_status", "unknown")),
        "source_packet_id": str(payload.get("packet_id", "unknown")),
        "source_digest": _sha(dict(payload)),
        "recorded_epoch": int(time.time()),
    }


def _append_trajectory(root: pathlib.Path, scheduled_payload: Mapping[str, Any], max_records: int) -> tuple[bool, int, dict[str, Any]]:
    path = root / "qi_circulation_trajectory_packet.json"
    packet = _read_json(path)
    records = _trajectory_records(packet)
    record = _scheduled_record(scheduled_payload)
    records.append(record)
    if max_records > 0:
        records = records[-max_records:]
    packet = dict(packet)
    packet["trajectory"] = records
    packet["last_scheduled_closed_loop_receipt"] = record
    packet["cycle_runner_updated_epoch"] = int(time.time())
    packet["cycle_runner_version"] = "kuuos_runtime_daemon_qi_process_tensor_cycle_runner_v3_7"
    _write_json(path, packet)
    return True, len(records), packet


def build_qi_process_tensor_cycle_runner(*, runtime_context: Mapping[str, Any], cycle_runner_license_packet: Mapping[str, Any]) -> QiProcessTensorCycleRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(cycle_runner_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_process_tensor_cycle_runner_receipt.json"
    audit_path = root / "qi_process_tensor_cycle_runner_audit.jsonl"

    if ctx.get("qi_process_tensor_cycle_runner_enabled") is not True:
        blockers.append("qi_process_tensor_cycle_runner_enabled_not_true")
    if ctx.get("apply_process_tensor_cycle_runner") is not True:
        blockers.append("apply_process_tensor_cycle_runner_not_true")
    if lic.get("license_status") != "QI_PROCESS_TENSOR_CYCLE_RUNNER_LICENSE_READY":
        blockers.append("process_tensor_cycle_runner_license_not_ready")
    for name in ["return_loop_run_allowed", "scheduled_closed_loop_run_allowed", "trajectory_append_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    if not (root / "qi_circulation_trajectory_packet.json").is_file():
        blockers.append("trajectory_packet_missing")
    if not (root / "qi_process_tensor_packet.json").is_file():
        blockers.append("process_tensor_packet_missing")

    return_loop_status = "NOT_RUN"
    scheduled_status = "NOT_RUN"
    trajectory_appended = False
    trajectory_length = 0
    final_qi_packet: dict[str, Any] = {}

    if not blockers:
        return_loop = build_qi_process_tensor_return_loop(
            runtime_context={"qi_process_tensor_return_loop_enabled": True, "apply_process_tensor_return_loop": True, "runtime_root": str(root)},
            return_loop_license_packet=_return_loop_license(),
        )
        return_payload = return_loop.to_dict()
        return_loop_status = str(return_payload.get("status", "unknown"))
        records.append(_record("return_loop_orchestrator_v3_6", return_payload))
        if return_loop_status != "QI_PROCESS_TENSOR_RETURN_LOOP_READY":
            blockers.append("return_loop_not_ready")

    scheduled_payload: dict[str, Any] = {}
    if not blockers:
        scheduled = build_qi_scheduled_closed_loop_runner(
            runtime_context={"qi_scheduled_closed_loop_enabled": True, "apply_scheduled_closed_loop": True, "runtime_root": str(root)},
            runner_license_packet=_scheduled_closed_loop_license(),
        )
        scheduled_payload = scheduled.to_dict()
        scheduled_status = str(scheduled_payload.get("status", "unknown"))
        final_qi_packet = dict(scheduled_payload.get("final_qi_packet", {})) if isinstance(scheduled_payload.get("final_qi_packet"), Mapping) else {}
        records.append(_record("scheduled_closed_loop_runner_v3_2", scheduled_payload))
        if scheduled_status not in {"QI_SCHEDULED_CLOSED_LOOP_READY", "QI_SCHEDULED_CLOSED_LOOP_CONVERGED"}:
            warnings.append("scheduled_closed_loop_not_ready_or_converged")

    if scheduled_payload and lic.get("trajectory_append_allowed") is True:
        trajectory_appended, trajectory_length, trajectory_packet = _append_trajectory(root, scheduled_payload, _i(ctx.get("max_trajectory_records"), 50))
        records.append({"stage": "trajectory_history_append", "status": "appended", "packet_id": str(scheduled_payload.get("packet_id", "unknown")), "digest": _sha(trajectory_packet), "epoch": int(time.time())})
    elif scheduled_payload:
        blockers.append("trajectory_append_not_allowed")

    cycle_completed = not blockers and return_loop_status == "QI_PROCESS_TENSOR_RETURN_LOOP_READY" and trajectory_appended
    status = "QI_PROCESS_TENSOR_CYCLE_RUNNER_READY" if cycle_completed else "QI_PROCESS_TENSOR_CYCLE_RUNNER_BLOCKED"
    packet_id = "qi-pt-cycle-runner-" + _sha({"root": str(root), "records": records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_process_tensor_cycle_runner_v3_7",
        "status": status,
        "packet_id": packet_id,
        "return_loop_status": return_loop_status,
        "scheduled_closed_loop_status": scheduled_status,
        "trajectory_appended": trajectory_appended,
        "trajectory_length": trajectory_length,
        "cycle_completed": cycle_completed,
        "final_qi_packet": final_qi_packet,
        "stage_records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiProcessTensorCycleRunnerResult(
        "kuuos_runtime_daemon_qi_process_tensor_cycle_runner_v3_7",
        status,
        packet_id,
        str(root),
        str(receipt_path),
        str(audit_path),
        return_loop_status,
        scheduled_status,
        trajectory_appended,
        trajectory_length,
        cycle_completed,
        final_qi_packet,
        blockers,
        warnings,
        records,
    )
