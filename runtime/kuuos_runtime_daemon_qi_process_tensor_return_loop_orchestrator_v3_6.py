#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_circulation_trajectory_adaptor_v3_3 import build_qi_circulation_trajectory_adaptor
from runtime.kuuos_runtime_daemon_qi_circulation_scheduler_packet_v3_4 import build_qi_circulation_scheduler_packet
from runtime.kuuos_runtime_daemon_qi_process_tensor_scheduler_overlay_v3_5 import build_qi_process_tensor_scheduler_overlay


@dataclass(frozen=True)
class QiProcessTensorReturnLoopResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    receipt_path: str
    audit_path: str
    trajectory_status: str
    scheduler_packet_status: str
    process_tensor_overlay_status: str
    adaptation_class: str
    handoff_class: str
    overlay_class: str
    final_packet_path: str
    completed: bool
    blockers: list[str]
    warnings: list[str]
    stage_records: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


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


def _trajectory_adaptor_license() -> dict[str, Any]:
    return {
        "license_status": "QI_CIRCULATION_TRAJECTORY_ADAPTOR_LICENSE_READY",
        "packet_read_allowed": True,
        "next_scheduler_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _scheduler_packet_license() -> dict[str, Any]:
    return {
        "license_status": "QI_CIRCULATION_SCHEDULER_PACKET_LICENSE_READY",
        "next_scheduler_packet_read_allowed": True,
        "scheduled_closed_loop_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _process_tensor_overlay_license() -> dict[str, Any]:
    return {
        "license_status": "QI_PROCESS_TENSOR_SCHEDULER_OVERLAY_LICENSE_READY",
        "scheduled_packet_read_allowed": True,
        "process_tensor_packet_read_allowed": True,
        "scheduled_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _record(stage: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage": stage,
        "status": str(payload.get("status") or payload.get("policy_status") or "unknown"),
        "packet_id": str(payload.get("packet_id") or payload.get("policy_packet_id") or "unknown"),
        "class": str(payload.get("adaptation_class") or payload.get("handoff_class") or payload.get("overlay_class") or "unknown"),
        "digest": _sha(dict(payload)),
        "epoch": int(time.time()),
    }


def build_qi_process_tensor_return_loop(*, runtime_context: Mapping[str, Any], return_loop_license_packet: Mapping[str, Any]) -> QiProcessTensorReturnLoopResult:
    ctx = _m(runtime_context)
    lic = _m(return_loop_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_process_tensor_return_loop_receipt.json"
    audit_path = root / "qi_process_tensor_return_loop_audit.jsonl"
    final_packet_path = root / "qi_scheduled_closed_loop_packet.json"

    if ctx.get("qi_process_tensor_return_loop_enabled") is not True:
        blockers.append("qi_process_tensor_return_loop_enabled_not_true")
    if ctx.get("apply_process_tensor_return_loop") is not True:
        blockers.append("apply_process_tensor_return_loop_not_true")
    if lic.get("license_status") != "QI_PROCESS_TENSOR_RETURN_LOOP_LICENSE_READY":
        blockers.append("process_tensor_return_loop_license_not_ready")
    for name in ["trajectory_adaptor_run_allowed", "scheduler_packet_run_allowed", "process_tensor_overlay_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    if not (root / "qi_circulation_trajectory_packet.json").is_file():
        blockers.append("trajectory_packet_missing")
    if not (root / "qi_process_tensor_packet.json").is_file():
        blockers.append("process_tensor_packet_missing")

    trajectory_status = "NOT_RUN"
    scheduler_packet_status = "NOT_RUN"
    overlay_status = "NOT_RUN"
    adaptation_class = "unknown"
    handoff_class = "unknown"
    overlay_class = "unknown"

    if not blockers:
        trajectory = build_qi_circulation_trajectory_adaptor(
            runtime_context={"qi_circulation_trajectory_adaptor_enabled": True, "apply_circulation_trajectory_adaptor": True, "runtime_root": str(root)},
            adaptor_license_packet=_trajectory_adaptor_license(),
        )
        trajectory_payload = trajectory.to_dict()
        trajectory_status = str(trajectory_payload.get("status", "unknown"))
        adaptation_class = str(trajectory_payload.get("adaptation_class", "unknown"))
        records.append(_record("trajectory_adaptor_v3_3", trajectory_payload))
        if trajectory_status != "QI_CIRCULATION_TRAJECTORY_ADAPTOR_READY":
            blockers.append("trajectory_adaptor_not_ready")

    if not blockers:
        scheduler = build_qi_circulation_scheduler_packet(
            runtime_context={"qi_circulation_scheduler_packet_enabled": True, "apply_circulation_scheduler_packet": True, "runtime_root": str(root)},
            scheduler_packet_license=_scheduler_packet_license(),
        )
        scheduler_payload = scheduler.to_dict()
        scheduler_packet_status = str(scheduler_payload.get("status", "unknown"))
        handoff_class = str(scheduler_payload.get("handoff_class", "unknown"))
        records.append(_record("scheduler_packet_v3_4", scheduler_payload))
        if scheduler_packet_status != "QI_CIRCULATION_SCHEDULER_PACKET_READY":
            blockers.append("scheduler_packet_not_ready")

    if not blockers:
        overlay = build_qi_process_tensor_scheduler_overlay(
            runtime_context={"qi_process_tensor_scheduler_overlay_enabled": True, "apply_process_tensor_scheduler_overlay": True, "runtime_root": str(root)},
            overlay_license_packet=_process_tensor_overlay_license(),
        )
        overlay_payload = overlay.to_dict()
        overlay_status = str(overlay_payload.get("status", "unknown"))
        overlay_class = str(overlay_payload.get("overlay_class", "unknown"))
        records.append(_record("process_tensor_scheduler_overlay_v3_5", overlay_payload))
        if overlay_status != "QI_PROCESS_TENSOR_SCHEDULER_OVERLAY_READY":
            blockers.append("process_tensor_overlay_not_ready")

    final_packet = _read_json(final_packet_path)
    if not blockers and not final_packet:
        blockers.append("final_scheduled_closed_loop_packet_missing")
    completed = not blockers
    status = "QI_PROCESS_TENSOR_RETURN_LOOP_READY" if completed else "QI_PROCESS_TENSOR_RETURN_LOOP_BLOCKED"
    packet_id = "qi-pt-return-loop-" + _sha({"root": str(root), "records": records, "blockers": blockers, "final": final_packet})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_process_tensor_return_loop_orchestrator_v3_6",
        "status": status,
        "packet_id": packet_id,
        "trajectory_status": trajectory_status,
        "scheduler_packet_status": scheduler_packet_status,
        "process_tensor_overlay_status": overlay_status,
        "adaptation_class": adaptation_class,
        "handoff_class": handoff_class,
        "overlay_class": overlay_class,
        "completed": completed,
        "final_packet_digest": _sha(final_packet),
        "stage_records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiProcessTensorReturnLoopResult(
        "kuuos_runtime_daemon_qi_process_tensor_return_loop_orchestrator_v3_6",
        status,
        packet_id,
        str(root),
        str(receipt_path),
        str(audit_path),
        trajectory_status,
        scheduler_packet_status,
        overlay_status,
        adaptation_class,
        handoff_class,
        overlay_class,
        str(final_packet_path),
        completed,
        blockers,
        warnings,
        records,
    )
