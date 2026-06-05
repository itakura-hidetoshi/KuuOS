#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_circulation_objective_scheduler_v3_1 import build_qi_circulation_objective_scheduler
from runtime.kuuos_runtime_daemon_qi_circulation_closed_loop_runner_v3_0 import build_qi_circulation_closed_loop_runner


@dataclass(frozen=True)
class QiScheduledClosedLoopRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    packet_path: str
    scheduler_packet_path: str
    closed_loop_packet_path: str
    receipt_path: str
    audit_path: str
    scheduler_status: str
    closed_loop_status: str
    objective_class: str
    cycle_count: int
    converged: bool
    final_qi_packet: dict[str, Any]
    blockers: list[str]
    warnings: list[str]
    records: list[dict[str, Any]]

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


def _scheduler_license() -> dict[str, Any]:
    return {
        "license_status": "QI_CIRCULATION_SCHEDULER_LICENSE_READY",
        "packet_read_allowed": True,
        "closed_loop_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _closed_loop_license() -> dict[str, Any]:
    return {
        "license_status": "QI_CIRCULATION_CLOSED_LOOP_LICENSE_READY",
        "packet_read_allowed": True,
        "router_run_allowed": True,
        "feedback_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _scheduler_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "initial_qi_packet": dict(packet.get("initial_qi_packet", {})) if isinstance(packet.get("initial_qi_packet"), Mapping) else dict(packet.get("qi_process_tensor_packet", {})) if isinstance(packet.get("qi_process_tensor_packet"), Mapping) else {},
        "route_base": dict(packet.get("route_base", {})) if isinstance(packet.get("route_base"), Mapping) else {},
    }


def build_qi_scheduled_closed_loop_runner(*, runtime_context: Mapping[str, Any], runner_license_packet: Mapping[str, Any]) -> QiScheduledClosedLoopRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(runner_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "qi_scheduled_closed_loop_packet.json"
    scheduler_packet_path = root / "qi_circulation_scheduler_packet.json"
    closed_loop_packet_path = root / "qi_circulation_closed_loop_packet.json"
    receipt_path = root / "qi_scheduled_closed_loop_receipt.json"
    audit_path = root / "qi_scheduled_closed_loop_audit.jsonl"
    if ctx.get("qi_scheduled_closed_loop_enabled") is not True:
        blockers.append("qi_scheduled_closed_loop_enabled_not_true")
    if ctx.get("apply_scheduled_closed_loop") is not True:
        blockers.append("apply_scheduled_closed_loop_not_true")
    if lic.get("license_status") != "QI_SCHEDULED_CLOSED_LOOP_LICENSE_READY":
        blockers.append("scheduled_closed_loop_license_not_ready")
    for name in ["packet_read_allowed", "scheduler_run_allowed", "closed_loop_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(packet_path)
    scheduler_status = "NOT_RUN"
    closed_loop_status = "NOT_RUN"
    objective_class = "unknown"
    cycle_count = 0
    converged = False
    final_qi_packet: dict[str, Any] = {}
    if not blockers:
        _write_json(scheduler_packet_path, _scheduler_packet(packet))
        scheduler = build_qi_circulation_objective_scheduler(
            runtime_context={"qi_circulation_scheduler_enabled": True, "apply_circulation_scheduler": True, "runtime_root": str(root)},
            scheduler_license_packet=_scheduler_license(),
        )
        scheduler_payload = scheduler.to_dict()
        scheduler_status = str(scheduler_payload.get("status"))
        objective_class = str(scheduler_payload.get("objective_class", "unknown"))
        records.append({"stage": "scheduler", "status": scheduler_status, "objective_class": objective_class, "digest": _sha(scheduler_payload), "epoch": int(time.time())})
        if scheduler_status != "QI_CIRCULATION_SCHEDULER_READY":
            blockers.append("scheduler_not_ready")
    if not blockers:
        closed = build_qi_circulation_closed_loop_runner(
            runtime_context={"qi_circulation_closed_loop_enabled": True, "apply_circulation_closed_loop": True, "runtime_root": str(root)},
            loop_license_packet=_closed_loop_license(),
        )
        closed_payload = closed.to_dict()
        closed_loop_status = str(closed_payload.get("status"))
        cycle_count = int(closed_payload.get("cycle_count", 0) or 0)
        converged = bool(closed_payload.get("converged"))
        final_qi_packet = dict(closed_payload.get("final_qi_packet", {})) if isinstance(closed_payload.get("final_qi_packet"), Mapping) else {}
        records.append({"stage": "closed_loop", "status": closed_loop_status, "cycle_count": cycle_count, "converged": converged, "digest": _sha(closed_payload), "epoch": int(time.time())})
        if closed_loop_status == "QI_CIRCULATION_CLOSED_LOOP_BLOCKED":
            blockers.append("closed_loop_blocked")
    if blockers:
        status = "QI_SCHEDULED_CLOSED_LOOP_BLOCKED"
    elif converged:
        status = "QI_SCHEDULED_CLOSED_LOOP_CONVERGED"
    else:
        status = "QI_SCHEDULED_CLOSED_LOOP_READY"
    packet_id = "qi-scheduled-closed-loop-" + _sha({"packet": packet, "records": records, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_scheduled_closed_loop_runner_v3_2", "status": status, "packet_id": packet_id, "scheduler_status": scheduler_status, "closed_loop_status": closed_loop_status, "objective_class": objective_class, "cycle_count": cycle_count, "converged": converged, "final_qi_packet": final_qi_packet, "records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiScheduledClosedLoopRunnerResult("kuuos_runtime_daemon_qi_scheduled_closed_loop_runner_v3_2", status, packet_id, str(root), str(packet_path), str(scheduler_packet_path), str(closed_loop_packet_path), str(receipt_path), str(audit_path), scheduler_status, closed_loop_status, objective_class, cycle_count, converged, final_qi_packet, blockers, warnings, records)
