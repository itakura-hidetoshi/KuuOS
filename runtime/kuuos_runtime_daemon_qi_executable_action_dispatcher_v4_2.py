#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Callable, Mapping

from runtime.kuuos_runtime_daemon_qi_process_tensor_cycle_trend_summary_v3_9 import build_qi_process_tensor_cycle_trend_summary
from runtime.kuuos_runtime_daemon_qi_trend_adaptive_supervisor_packet_v4_0 import build_qi_trend_adaptive_supervisor_packet
from runtime.kuuos_runtime_daemon_qi_trend_adaptive_supervisor_run_v4_1 import build_qi_trend_adaptive_supervisor_run
from runtime.kuuos_runtime_daemon_qi_process_tensor_cycle_supervisor_v3_8 import build_qi_process_tensor_cycle_supervisor
from runtime.kuuos_runtime_daemon_qi_process_tensor_cycle_runner_v3_7 import build_qi_process_tensor_cycle_runner
from runtime.kuuos_runtime_daemon_qi_process_tensor_return_loop_orchestrator_v3_6 import build_qi_process_tensor_return_loop


ALLOWLISTED_ACTIONS = {
    "cycle_trend_summary",
    "trend_adaptive_supervisor_packet",
    "trend_adaptive_supervisor_run",
    "cycle_supervisor",
    "cycle_runner",
    "return_loop",
}


@dataclass(frozen=True)
class QiExecutableActionDispatcherResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    action: str
    delegated_status: str
    delegated_packet_id: str
    receipt_path: str
    audit_path: str
    action_performed: bool
    delegated_result_digest: str
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


def _ctx(root: pathlib.Path, enabled: str, apply_key: str, patch: Mapping[str, Any] | None = None) -> dict[str, Any]:
    out = {enabled: True, apply_key: True, "runtime_root": str(root)}
    for key, value in dict(_m(patch)).items():
        if key in {"max_summary_records", "base_max_supervised_cycles", "base_max_trajectory_records", "max_supervised_cycles", "max_trajectory_records"}:
            out[key] = value
    return out


def _trend_summary_license() -> dict[str, Any]:
    return {
        "license_status": "QI_PROCESS_TENSOR_CYCLE_TREND_SUMMARY_LICENSE_READY",
        "supervisor_receipt_read_allowed": True,
        "supervisor_audit_read_allowed": True,
        "trajectory_read_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _adaptive_packet_license() -> dict[str, Any]:
    return {
        "license_status": "QI_TREND_ADAPTIVE_SUPERVISOR_PACKET_LICENSE_READY",
        "trend_summary_read_allowed": True,
        "trend_receipt_read_allowed": True,
        "next_supervisor_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _adaptive_run_license() -> dict[str, Any]:
    return {
        "license_status": "QI_TREND_ADAPTIVE_SUPERVISOR_RUN_LICENSE_READY",
        "next_supervisor_packet_read_allowed": True,
        "supervisor_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _supervisor_license() -> dict[str, Any]:
    return {
        "license_status": "QI_PROCESS_TENSOR_CYCLE_SUPERVISOR_LICENSE_READY",
        "cycle_runner_run_allowed": True,
        "state_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _cycle_runner_license() -> dict[str, Any]:
    return {
        "license_status": "QI_PROCESS_TENSOR_CYCLE_RUNNER_LICENSE_READY",
        "return_loop_run_allowed": True,
        "scheduled_closed_loop_run_allowed": True,
        "trajectory_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _return_loop_license() -> dict[str, Any]:
    return {
        "license_status": "QI_PROCESS_TENSOR_RETURN_LOOP_LICENSE_READY",
        "trajectory_adaptor_run_allowed": True,
        "scheduler_packet_run_allowed": True,
        "process_tensor_overlay_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _dispatch(action: str, root: pathlib.Path, patch: Mapping[str, Any]) -> Mapping[str, Any]:
    if action == "cycle_trend_summary":
        return build_qi_process_tensor_cycle_trend_summary(
            runtime_context=_ctx(root, "qi_process_tensor_cycle_trend_summary_enabled", "apply_process_tensor_cycle_trend_summary", patch),
            trend_summary_license_packet=_trend_summary_license(),
        ).to_dict()
    if action == "trend_adaptive_supervisor_packet":
        return build_qi_trend_adaptive_supervisor_packet(
            runtime_context=_ctx(root, "qi_trend_adaptive_supervisor_packet_enabled", "apply_trend_adaptive_supervisor_packet", patch),
            adaptive_packet_license=_adaptive_packet_license(),
        ).to_dict()
    if action == "trend_adaptive_supervisor_run":
        return build_qi_trend_adaptive_supervisor_run(
            runtime_context=_ctx(root, "qi_trend_adaptive_supervisor_run_enabled", "apply_trend_adaptive_supervisor_run", patch),
            adaptive_run_license=_adaptive_run_license(),
        ).to_dict()
    if action == "cycle_supervisor":
        return build_qi_process_tensor_cycle_supervisor(
            runtime_context=_ctx(root, "qi_process_tensor_cycle_supervisor_enabled", "apply_process_tensor_cycle_supervisor", patch),
            supervisor_license_packet=_supervisor_license(),
        ).to_dict()
    if action == "cycle_runner":
        return build_qi_process_tensor_cycle_runner(
            runtime_context=_ctx(root, "qi_process_tensor_cycle_runner_enabled", "apply_process_tensor_cycle_runner", patch),
            cycle_runner_license_packet=_cycle_runner_license(),
        ).to_dict()
    if action == "return_loop":
        return build_qi_process_tensor_return_loop(
            runtime_context=_ctx(root, "qi_process_tensor_return_loop_enabled", "apply_process_tensor_return_loop", patch),
            return_loop_license_packet=_return_loop_license(),
        ).to_dict()
    raise ValueError(f"unsupported action: {action}")


def _delegated_status(payload: Mapping[str, Any]) -> str:
    return str(payload.get("status") or payload.get("trend_status") or "unknown")


def build_qi_executable_action_dispatcher(*, runtime_context: Mapping[str, Any], dispatcher_license: Mapping[str, Any]) -> QiExecutableActionDispatcherResult:
    ctx = _m(runtime_context)
    lic = _m(dispatcher_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    action_packet_path = root / "qi_executable_action_packet.json"
    receipt_path = root / "qi_executable_action_dispatcher_receipt.json"
    audit_path = root / "qi_executable_action_dispatcher_audit.jsonl"
    if ctx.get("qi_executable_action_dispatcher_enabled") is not True:
        blockers.append("qi_executable_action_dispatcher_enabled_not_true")
    if ctx.get("apply_executable_action_dispatcher") is not True:
        blockers.append("apply_executable_action_dispatcher_not_true")
    if lic.get("license_status") != "QI_EXECUTABLE_ACTION_DISPATCHER_LICENSE_READY":
        blockers.append("executable_action_dispatcher_license_not_ready")
    for name in ["action_packet_read_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(action_packet_path)
    if not packet:
        blockers.append("action_packet_missing_or_invalid")
    action = str(packet.get("action", "unknown")) if packet else "unknown"
    if action not in ALLOWLISTED_ACTIONS:
        blockers.append("action_not_allowlisted")
    if packet and packet.get("action_allowed") is not True:
        blockers.append("action_packet_action_allowed_not_true")
    if lic.get(f"allow_{action}_action") is not True:
        blockers.append(f"{action}_not_allowed_by_dispatcher_license")
    patch = _m(packet.get("action_context_patch"))
    delegated: Mapping[str, Any] = {}
    action_performed = False
    if not blockers:
        try:
            delegated = _dispatch(action, root, patch)
            action_performed = True
        except Exception as exc:  # pragma: no cover
            blockers.append("delegated_action_exception")
            warnings.append(str(exc))
            delegated = {}
    delegated_status = _delegated_status(delegated)
    if action_performed and not delegated_status.endswith("READY"):
        blockers.append("delegated_action_not_ready")
    status = "QI_EXECUTABLE_ACTION_DISPATCHER_READY" if not blockers else "QI_EXECUTABLE_ACTION_DISPATCHER_BLOCKED"
    packet_id = "qi-executable-action-dispatcher-" + _sha({"packet": packet, "delegated": delegated, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_executable_action_dispatcher_v4_2",
        "status": status,
        "packet_id": packet_id,
        "action": action,
        "delegated_status": delegated_status,
        "delegated_packet_id": str(delegated.get("packet_id") or delegated.get("trend_packet_id") or "unknown"),
        "action_performed": action_performed,
        "delegated_result_digest": _sha(delegated),
        "allowlisted_actions": sorted(ALLOWLISTED_ACTIONS),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiExecutableActionDispatcherResult(
        "kuuos_runtime_daemon_qi_executable_action_dispatcher_v4_2",
        status,
        packet_id,
        str(root),
        action,
        delegated_status,
        str(delegated.get("packet_id") or delegated.get("trend_packet_id") or "unknown"),
        str(receipt_path),
        str(audit_path),
        action_performed,
        _sha(delegated),
        blockers,
        warnings,
    )
