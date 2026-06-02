#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import pathlib
from typing import Any, Mapping, Sequence

try:
    from runtime.kuuos_runtime_daemon_qi_autonomous_tick_policy_kernel_v0_1 import build_qi_autonomous_tick_policy_kernel
    from runtime.kuuos_runtime_daemon_qi_autonomous_tick_loop_binding_v0_1 import bind_qi_autonomous_tick_policy_to_daemon_loop
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_autonomous_tick_policy_kernel_v0_1 import build_qi_autonomous_tick_policy_kernel
    from kuuos_runtime_daemon_qi_autonomous_tick_loop_binding_v0_1 import bind_qi_autonomous_tick_policy_to_daemon_loop


@dataclass(frozen=True)
class QiAutonomousMultiTickWindowGovernorResult:
    window_governor_version: str
    window_governor_status: str
    requested_window_ticks: int
    attempted_tick_count: int
    completed_tick_count: int
    stopped_early: bool
    stop_reason: str | None
    next_candidate_tick: int | None
    event_log_path: str
    ledger_state_path: str
    window_bound_enforced: bool
    one_tick_receipt_delegation_enforced: bool
    process_tensor_window_optimized: bool
    process_tensor_window_mode: str
    process_tensor_stop_on_observe: bool
    process_tensor_stop_on_full_history: bool
    process_tensor_stop_on_freeze: bool
    receipt_ids: list[str]
    policy_packet_ids: list[str]
    daemon_loop_actions: list[str]
    rollout_modes: list[str]
    optimization_modes: list[str]
    jsonl_event_lines_appended: int
    heartbeat_count: int
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
    policy_packets: list[dict[str, Any]]
    loop_binding_packets: list[dict[str, Any]]
    window_blockers: list[str]
    window_warnings: list[str]
    authority: str = "autonomous_multi_tick_window_governor_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _list_of_mappings(value: Any) -> list[Mapping[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, Mapping)]
    return []


def _truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() in {"true", "yes", "1"}


def _int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


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
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def _choose_pt_packet(base: Mapping[str, Any], schedule: list[Mapping[str, Any]], index: int) -> dict[str, Any]:
    packet = _dict(base)
    if index < len(schedule):
        packet.update(dict(schedule[index]))
    return packet


def run_qi_autonomous_multi_tick_window_governor(
    *,
    decisionos_packet: Mapping[str, Any],
    cbf_packet: Mapping[str, Any],
    token_ledger_packet: Mapping[str, Any],
    process_tensor_packet: Mapping[str, Any],
    memory_entries: Sequence[Mapping[str, Any]] | Mapping[str, Any],
    scheduler_state: Mapping[str, Any],
    scheduler_proposal: Mapping[str, Any],
    process_tensor_metrics: Mapping[str, Any],
    event_log_path: str | pathlib.Path,
    ledger_state_path: str | pathlib.Path,
    window_context: Mapping[str, Any] | None = None,
) -> QiAutonomousMultiTickWindowGovernorResult:
    ctx = _mapping(window_context)
    blockers: list[str] = []
    warnings: list[str] = []
    if ctx.get("window_governor_enabled") is not True:
        blockers.append("window_governor_enabled_not_true")
    if ctx.get("read_only_window_governor") is not True:
        blockers.append("read_only_window_governor_not_true")
    if ctx.get("jsonl_backend_required") is not True:
        blockers.append("jsonl_backend_required_not_true")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")
    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_control_packet_mutation") is True:
        blockers.append("request_control_packet_mutation")

    requested = _int(ctx.get("requested_window_ticks"), 1)
    max_window = _int(ctx.get("max_window_ticks"), requested)
    if requested <= 0:
        blockers.append("requested_window_ticks_not_positive")
    if max_window <= 0:
        blockers.append("max_window_ticks_not_positive")
    if requested > max_window:
        blockers.append("requested_window_exceeds_max_window_ticks")
    hard_cap = _int(ctx.get("absolute_max_window_ticks"), 16)
    if requested > hard_cap or max_window > hard_cap:
        blockers.append("window_ticks_exceed_absolute_cap")

    stop_on_observe = ctx.get("stop_on_observe") is not False
    stop_on_full_history = ctx.get("stop_on_full_history") is not False
    stop_on_freeze = True
    start_current_tick = _int(ctx.get("current_tick"), _int(token_ledger_packet.get("current_tick"), 0))
    tick_prefix = str(ctx.get("tick_id_prefix", "qi-window"))
    pt_schedule = _list_of_mappings(ctx.get("process_tensor_schedule"))

    policy_packets: list[dict[str, Any]] = []
    loop_packets: list[dict[str, Any]] = []
    stop_reason: str | None = None
    completed = 0
    attempted = 0
    total_appended = 0
    total_heartbeats = 0

    if not blockers:
        for index in range(requested):
            current_tick = start_current_tick + completed
            pt_packet = _choose_pt_packet(process_tensor_packet, pt_schedule, index)
            token_packet = _dict(token_ledger_packet)
            token_packet["current_tick"] = current_tick
            if "remaining_tokens" in token_packet:
                token_packet["remaining_tokens"] = max(0, _int(token_packet.get("remaining_tokens"), 0) - completed)
            policy_ctx = {
                "current_tick": current_tick,
                "tick_policy_enabled": True,
                "read_only_policy_surface": True,
                "notify_uncertainty_threshold": ctx.get("notify_uncertainty_threshold", 0.45),
                "ticket_uncertainty_threshold": ctx.get("ticket_uncertainty_threshold", 0.65),
                "handover_uncertainty_threshold": ctx.get("handover_uncertainty_threshold", 0.85),
            }
            policy = build_qi_autonomous_tick_policy_kernel(
                decisionos_packet=decisionos_packet,
                cbf_packet=cbf_packet,
                token_ledger_packet=token_packet,
                process_tensor_packet=pt_packet,
                policy_context=policy_ctx,
            ).to_dict()
            policy_packets.append(policy)
            attempted += 1
            if policy.get("policy_status") != "QI_AUTONOMOUS_TICK_POLICY_READY":
                stop_reason = "policy_not_ready"
                break
            _require_false(f"policy_{index}", policy, blockers)
            if blockers:
                stop_reason = "policy_boundary_violation"
                break

            loop = bind_qi_autonomous_tick_policy_to_daemon_loop(
                policy_packet=policy,
                process_tensor_packet=pt_packet,
                memory_entries=memory_entries,
                scheduler_state=scheduler_state,
                scheduler_proposal=scheduler_proposal,
                process_tensor_metrics=process_tensor_metrics,
                event_log_path=event_log_path,
                ledger_state_path=ledger_state_path,
                loop_context={
                    "loop_binding_enabled": True,
                    "jsonl_backend_required": True,
                    "read_only_loop_binding": True,
                    "tick_id_prefix": tick_prefix,
                    "memory_complexity_threshold": ctx.get("memory_complexity_threshold", pt_packet.get("memory_complexity_threshold", 1.0)),
                    "recovery_epsilon": ctx.get("recovery_epsilon", pt_packet.get("recovery_epsilon", 0.1)),
                    "freeze_on_critical_process_tensor_pressure": ctx.get("freeze_on_critical_process_tensor_pressure", True),
                },
            ).to_dict()
            loop_packets.append(loop)
            _require_false(f"loop_{index}", loop, blockers)
            if loop.get("loop_binding_status") != "QI_AUTONOMOUS_TICK_LOOP_BINDING_COMPLETED":
                stop_reason = "loop_binding_not_completed"
                break
            total_appended += int(loop.get("jsonl_event_lines_appended", 0))
            total_heartbeats += int(loop.get("heartbeat_count", 0))
            if loop.get("safe_resume_invoked") is True:
                completed += 1
            else:
                action = str(loop.get("daemon_loop_action"))
                if action == "observe" and stop_on_observe:
                    stop_reason = "process_tensor_observe_required"
                    break
                if loop.get("process_tensor_full_history_required") is True and stop_on_full_history:
                    stop_reason = "process_tensor_full_history_required"
                    break
                if action == "freeze" and stop_on_freeze:
                    stop_reason = "freeze_required"
                    break
                stop_reason = f"non_advance_action:{action}"
                break
            if loop.get("process_tensor_full_history_required") is True and stop_on_full_history:
                stop_reason = "process_tensor_full_history_after_tick"
                break
    ready = not blockers
    stopped_early = (ready and attempted < requested) or (stop_reason is not None and completed < requested)
    next_tick = start_current_tick + completed if ready else None
    receipt_ids = [str(p.get("receipt_id")) for p in loop_packets if p.get("receipt_id")]
    policy_ids = [str(p.get("policy_packet_id")) for p in policy_packets if p.get("policy_packet_id")]
    actions = [str(p.get("daemon_loop_action")) for p in loop_packets if p.get("daemon_loop_action")]
    rollout_modes = [str(p.get("process_tensor_rollout_mode")) for p in loop_packets if p.get("process_tensor_rollout_mode")]
    optimization_modes = [str(p.get("process_tensor_optimization_mode")) for p in loop_packets if p.get("process_tensor_optimization_mode")]
    if not stop_reason and ready and completed == requested:
        stop_reason = "window_completed"
    if not stop_reason and blockers:
        stop_reason = "window_blocked"

    window_mode = "empty"
    if rollout_modes:
        if "full_history" in rollout_modes:
            window_mode = "full_history_guarded"
        elif "partial_history" in rollout_modes:
            window_mode = "partial_history_guarded"
        elif "compressed" in rollout_modes:
            window_mode = "compressed_window"
        else:
            window_mode = "markov_window"

    return QiAutonomousMultiTickWindowGovernorResult(
        window_governor_version="kuuos_runtime_daemon_qi_autonomous_multi_tick_window_governor_v0_1",
        window_governor_status="QI_AUTONOMOUS_MULTI_TICK_WINDOW_GOVERNOR_COMPLETED" if ready else "QI_AUTONOMOUS_MULTI_TICK_WINDOW_GOVERNOR_BLOCKED",
        requested_window_ticks=requested,
        attempted_tick_count=attempted,
        completed_tick_count=completed,
        stopped_early=stopped_early,
        stop_reason=stop_reason,
        next_candidate_tick=next_tick,
        event_log_path=str(event_log_path),
        ledger_state_path=str(ledger_state_path),
        window_bound_enforced=True,
        one_tick_receipt_delegation_enforced=True,
        process_tensor_window_optimized=bool(loop_packets),
        process_tensor_window_mode=window_mode,
        process_tensor_stop_on_observe=stop_on_observe,
        process_tensor_stop_on_full_history=stop_on_full_history,
        process_tensor_stop_on_freeze=stop_on_freeze,
        receipt_ids=receipt_ids,
        policy_packet_ids=policy_ids,
        daemon_loop_actions=actions,
        rollout_modes=rollout_modes,
        optimization_modes=optimization_modes,
        jsonl_event_lines_appended=total_appended,
        heartbeat_count=total_heartbeats,
        memory_read_performed=completed > 0,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        policy_packets=policy_packets,
        loop_binding_packets=loop_packets,
        window_blockers=blockers,
        window_warnings=warnings,
    )
