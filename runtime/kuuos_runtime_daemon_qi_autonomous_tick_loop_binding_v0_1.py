#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import pathlib
from typing import Any, Mapping, Sequence

try:
    from runtime.kuuos_runtime_daemon_qi_autonomous_tick_policy_receipt_v0_1 import build_qi_autonomous_tick_policy_receipt
    from runtime.kuuos_runtime_daemon_qi_jsonl_safe_resume_controller_v0_1 import run_qi_jsonl_safe_resume_controller
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_autonomous_tick_policy_receipt_v0_1 import build_qi_autonomous_tick_policy_receipt
    from kuuos_runtime_daemon_qi_jsonl_safe_resume_controller_v0_1 import run_qi_jsonl_safe_resume_controller


@dataclass(frozen=True)
class QiAutonomousTickLoopBindingResult:
    loop_binding_version: str
    loop_binding_status: str
    receipt_status: str
    receipt_id: str | None
    selected_action: str
    daemon_loop_action: str
    safe_resume_allowed: bool
    safe_resume_invoked: bool
    safe_resume_status: str | None
    safe_resume_start_tick: int | None
    safe_resume_tick_count: int
    jsonl_event_lines_appended: int
    heartbeat_count: int
    event_log_path: str
    ledger_state_path: str
    process_tensor_optimization_mode: str
    process_tensor_rollout_mode: str
    process_tensor_pressure: str
    process_tensor_observation_required: bool
    process_tensor_baseline_fallback_required: bool
    process_tensor_full_history_required: bool
    hold_required: bool
    observe_required: bool
    notify_required: bool
    ticket_required: bool
    handover_required: bool
    freeze_required: bool
    memory_read_performed: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    receipt_packet: dict[str, Any]
    safe_resume_packet: dict[str, Any]
    loop_blockers: list[str]
    loop_warnings: list[str]
    authority: str = "autonomous_tick_loop_binding_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
        "memory_write_performed",
        "memory_append_performed",
        "memory_overwrite_performed",
        "world_update_performed",
        "control_packet_mutation_performed",
        "probe_execution_performed",
        "grants_probe_execution_authority",
        "grants_world_update_authority",
        "grants_memory_overwrite_authority",
    ]:
        if packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def bind_qi_autonomous_tick_policy_to_daemon_loop(
    *,
    policy_packet: Mapping[str, Any],
    process_tensor_packet: Mapping[str, Any] | None,
    memory_entries: Sequence[Mapping[str, Any]] | Mapping[str, Any],
    scheduler_state: Mapping[str, Any],
    scheduler_proposal: Mapping[str, Any],
    process_tensor_metrics: Mapping[str, Any],
    event_log_path: str | pathlib.Path,
    ledger_state_path: str | pathlib.Path,
    loop_context: Mapping[str, Any] | None = None,
) -> QiAutonomousTickLoopBindingResult:
    ctx = _mapping(loop_context)
    blockers: list[str] = []
    warnings: list[str] = []
    if ctx.get("loop_binding_enabled") is not True:
        blockers.append("loop_binding_enabled_not_true")
    if ctx.get("jsonl_backend_required") is not True:
        blockers.append("jsonl_backend_required_not_true")
    if ctx.get("read_only_loop_binding") is not True:
        blockers.append("read_only_loop_binding_not_true")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")
    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_control_packet_mutation") is True:
        blockers.append("request_control_packet_mutation")

    receipt = build_qi_autonomous_tick_policy_receipt(
        policy_packet=policy_packet,
        process_tensor_packet=process_tensor_packet,
        receipt_context={
            **dict(ctx),
            "root_id": ctx.get("root_id") or _mapping(policy_packet).get("root_id"),
        },
    ).to_dict()
    if receipt.get("receipt_status") != "QI_AUTONOMOUS_TICK_POLICY_RECEIPT_READY":
        blockers.append("receipt_not_ready")
    _require_false("receipt", receipt, blockers)

    event_path = pathlib.Path(event_log_path)
    ledger_path = pathlib.Path(ledger_state_path)
    safe_resume_packet: dict[str, Any] = {}
    safe_resume_invoked = False

    if not blockers and receipt.get("safe_resume_allowed") is True:
        start_tick = int(receipt.get("safe_resume_start_tick"))
        tick_prefix = str(ctx.get("tick_id_prefix", "qi-loop"))
        safe_resume_invoked = True
        safe_resume_packet = run_qi_jsonl_safe_resume_controller(
            memory_entries=memory_entries,
            scheduler_state=scheduler_state,
            scheduler_proposal=scheduler_proposal,
            process_tensor_metrics=process_tensor_metrics,
            event_log_path=event_path,
            ledger_state_path=ledger_path,
            desired_start_tick=start_tick,
            desired_tick_count=1,
            resume_context={
                "allow_safe_resume": True,
                "jsonl_backend_required": True,
                "skip_processed_ticks": True,
                "max_tick_count": 1,
                "tick_id_prefix": tick_prefix,
                "request_probe_execution": False,
                "request_memory_write": False,
                "request_world_update": False,
                "request_control_packet_mutation": False,
            },
        ).to_dict()
        if safe_resume_packet.get("resume_status") != "QI_JSONL_SAFE_RESUME_CONTROLLER_COMPLETED":
            blockers.append("safe_resume_not_completed")
        _require_false("safe_resume", safe_resume_packet, blockers)
    elif receipt.get("daemon_loop_action") == "advance_tick":
        warnings.append("advance_not_invoked_without_safe_resume_receipt")

    ready = not blockers
    appended = int(safe_resume_packet.get("jsonl_event_lines_appended", 0)) if safe_resume_packet else 0
    heartbeats = int(safe_resume_packet.get("heartbeat_count", 0)) if safe_resume_packet else 0
    return QiAutonomousTickLoopBindingResult(
        loop_binding_version="kuuos_runtime_daemon_qi_autonomous_tick_loop_binding_v0_1",
        loop_binding_status="QI_AUTONOMOUS_TICK_LOOP_BINDING_COMPLETED" if ready else "QI_AUTONOMOUS_TICK_LOOP_BINDING_BLOCKED",
        receipt_status=str(receipt.get("receipt_status")),
        receipt_id=str(receipt.get("receipt_id")) if receipt.get("receipt_id") else None,
        selected_action=str(receipt.get("selected_action")),
        daemon_loop_action=str(receipt.get("daemon_loop_action")),
        safe_resume_allowed=receipt.get("safe_resume_allowed") is True,
        safe_resume_invoked=safe_resume_invoked,
        safe_resume_status=str(safe_resume_packet.get("resume_status")) if safe_resume_packet.get("resume_status") else None,
        safe_resume_start_tick=int(receipt.get("safe_resume_start_tick")) if receipt.get("safe_resume_start_tick") is not None else None,
        safe_resume_tick_count=int(receipt.get("safe_resume_tick_count", 0)),
        jsonl_event_lines_appended=appended,
        heartbeat_count=heartbeats,
        event_log_path=str(event_path),
        ledger_state_path=str(ledger_path),
        process_tensor_optimization_mode=str(receipt.get("process_tensor_optimization_mode")),
        process_tensor_rollout_mode=str(receipt.get("process_tensor_rollout_mode")),
        process_tensor_pressure=str(receipt.get("process_tensor_pressure")),
        process_tensor_observation_required=receipt.get("process_tensor_observation_required") is True,
        process_tensor_baseline_fallback_required=receipt.get("process_tensor_baseline_fallback_required") is True,
        process_tensor_full_history_required=receipt.get("process_tensor_full_history_required") is True,
        hold_required=receipt.get("hold_required") is True,
        observe_required=receipt.get("observe_required") is True,
        notify_required=receipt.get("notify_required") is True,
        ticket_required=receipt.get("ticket_required") is True,
        handover_required=receipt.get("handover_required") is True,
        freeze_required=receipt.get("freeze_required") is True,
        memory_read_performed=safe_resume_invoked and safe_resume_packet.get("memory_read_performed") is True,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        receipt_packet=receipt,
        safe_resume_packet=safe_resume_packet,
        loop_blockers=blockers,
        loop_warnings=warnings,
    )
