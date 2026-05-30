#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

try:
    from runtime.kuuos_runtime_daemon_qi_memoryos_process_tensor_retrieval_replay_v0_1 import build_qi_memoryos_process_tensor_retrieval_replay
    from runtime.kuuos_runtime_daemon_qi_replay_scheduler_state_apply_v0_1 import apply_qi_replay_scheduler_state
    from runtime.kuuos_runtime_daemon_qi_probe_scheduler_proposal_reuse_v0_1 import build_qi_probe_scheduler_proposal_reuse
    from runtime.kuuos_runtime_daemon_qi_process_tensor_aware_scheduler_state_v0_2 import step_qi_process_tensor_aware_scheduler_state_v0_2
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_memoryos_process_tensor_retrieval_replay_v0_1 import build_qi_memoryos_process_tensor_retrieval_replay
    from kuuos_runtime_daemon_qi_replay_scheduler_state_apply_v0_1 import apply_qi_replay_scheduler_state
    from kuuos_runtime_daemon_qi_probe_scheduler_proposal_reuse_v0_1 import build_qi_probe_scheduler_proposal_reuse
    from kuuos_runtime_daemon_qi_process_tensor_aware_scheduler_state_v0_2 import step_qi_process_tensor_aware_scheduler_state_v0_2


@dataclass(frozen=True)
class QiPersistentProcessTensorDaemonTick:
    daemon_version: str
    daemon_status: str
    daemon_mode: str
    tick_id: str
    current_tick: int
    heartbeat_emitted: bool
    closed_loop_tick_performed: bool
    memory_entry_count: int
    replay_status: str | None
    scheduler_apply_status: str | None
    proposal_reuse_status: str | None
    v02_scheduler_status: str | None
    dominant_probe_type: str | None
    scheduler_reuse_hint: str | None
    process_tensor_pressure: str
    history_depth: int
    observation_debt_resolution_priority: float
    safe_reentry_window_score: float
    nonmarkov_link_density: float
    memory_kernel_preservation_score: float
    scheduler_state_mutation_performed: bool
    scheduler_update_scope: str
    memory_read_performed: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_scheduler_authority: bool
    grants_memory_write_authority: bool
    grants_memory_overwrite_authority: bool
    grants_world_update_authority: bool
    grants_control_packet_authority: bool
    grants_probe_execution_authority: bool
    replay_packet: dict[str, Any]
    scheduler_apply_packet: dict[str, Any]
    proposal_reuse_packet: dict[str, Any]
    v02_scheduler_packet: dict[str, Any]
    daemon_blockers: list[str]
    daemon_warnings: list[str]
    authority: str = "persistent_runtime_tick_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _entries(value: Any) -> list[Mapping[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, Mapping)]
    if isinstance(value, Mapping) and isinstance(value.get("entries"), list):
        return [item for item in value["entries"] if isinstance(item, Mapping)]
    if isinstance(value, Mapping):
        return [value]
    return []


def _float(payload: Mapping[str, Any], key: str, default: float) -> float:
    try:
        return float(payload.get(key, default))
    except (TypeError, ValueError):
        return default


def _int(payload: Mapping[str, Any], key: str, default: int) -> int:
    try:
        return int(payload.get(key, default))
    except (TypeError, ValueError):
        return default


def _pressure(metrics: Mapping[str, Any]) -> str:
    observation = _float(metrics, "observation_debt_resolution_priority", 0.0)
    reentry = _float(metrics, "safe_reentry_window_score", 1.0)
    nonmarkov = _float(metrics, "nonmarkov_link_density", 1.0)
    kernel = _float(metrics, "memory_kernel_preservation_score", 1.0)
    if observation >= 0.8 or reentry <= 0.25 or nonmarkov <= 0.25 or kernel <= 0.35:
        return "high"
    if observation >= 0.55 or reentry <= 0.5 or nonmarkov <= 0.5 or kernel <= 0.6:
        return "moderate"
    return "low"


def run_qi_persistent_process_tensor_daemon_tick(
    *,
    memory_entries: Sequence[Mapping[str, Any]] | Mapping[str, Any],
    scheduler_state: Mapping[str, Any],
    scheduler_proposal: Mapping[str, Any],
    process_tensor_metrics: Mapping[str, Any],
    current_tick: int,
    runtime_context: Mapping[str, Any] | None = None,
) -> QiPersistentProcessTensorDaemonTick:
    ctx = _mapping(runtime_context)
    metrics = _mapping(process_tensor_metrics)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("allow_persistent_tick") is not True:
        blockers.append("allow_persistent_tick_not_true")
    if ctx.get("bounded_tick") is not True:
        blockers.append("bounded_tick_not_true")
    if ctx.get("heartbeat_required") is not True:
        blockers.append("heartbeat_required_not_true")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")
    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_control_packet_mutation") is True:
        blockers.append("request_control_packet_mutation")

    tick_id = str(ctx.get("tick_id") or f"qi-persistent-tick-{current_tick}")
    entries = _entries(memory_entries)

    replay = build_qi_memoryos_process_tensor_retrieval_replay(
        memory_entries=entries,
        replay_context={
            "request_memory_write": False,
            "request_memory_overwrite": False,
            "request_world_update": False,
            "request_scheduler_mutation": False,
            "request_probe_execution": False,
        },
    ).to_dict()
    if replay.get("replay_status") != "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY":
        blockers.append("replay_not_ready")

    apply_packet = apply_qi_replay_scheduler_state(
        replay_packet=replay,
        scheduler_state=scheduler_state,
        apply_context={
            "allow_scheduler_state_update": True,
            "scheduler_update_scope": "replay_hint_only",
            "scheduler_lineage_preserved": True,
            "request_probe_execution": False,
            "request_memory_write": False,
            "request_world_update": False,
            "request_control_packet_mutation": False,
        },
    ).to_dict()
    if apply_packet.get("apply_status") != "QI_REPLAY_SCHEDULER_STATE_APPLY_PERFORMED":
        blockers.append("scheduler_apply_not_performed")

    reuse = build_qi_probe_scheduler_proposal_reuse(
        replay_applied_scheduler_state=apply_packet,
        reuse_context={
            "reuse_scope": "proposal_only",
            "request_scheduler_state_mutation": False,
            "request_probe_execution": False,
            "request_memory_write": False,
            "request_world_update": False,
            "request_control_packet_mutation": False,
        },
    ).to_dict()
    if reuse.get("reuse_status") != "QI_PROBE_SCHEDULER_PROPOSAL_REUSE_READY":
        blockers.append("proposal_reuse_not_ready")

    v02 = step_qi_process_tensor_aware_scheduler_state_v0_2(
        scheduler_state=scheduler_state,
        scheduler_proposal=scheduler_proposal,
        process_tensor_metrics=metrics,
        current_tick=current_tick,
        proposal_reuse=reuse,
    ).to_dict()
    if v02.get("adjustment_status") != "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_UPDATED":
        blockers.append("v02_scheduler_not_updated")

    for label, packet in [("replay", replay), ("apply", apply_packet), ("reuse", reuse), ("v02", v02)]:
        for key in ["probe_execution_performed", "memory_write_performed", "world_update_performed", "control_packet_mutation_performed", "grants_probe_execution_authority", "grants_world_update_authority"]:
            if packet.get(key) is not False:
                blockers.append(f"{label}_{key}_not_false")

    ready = not blockers
    return QiPersistentProcessTensorDaemonTick(
        daemon_version="kuuos_runtime_daemon_qi_persistent_process_tensor_daemon_v0_1",
        daemon_status="QI_PERSISTENT_PROCESS_TENSOR_DAEMON_TICK_READY" if ready else "QI_PERSISTENT_PROCESS_TENSOR_DAEMON_TICK_BLOCKED",
        daemon_mode="bounded_persistent_tick",
        tick_id=tick_id,
        current_tick=current_tick,
        heartbeat_emitted=ready,
        closed_loop_tick_performed=ready,
        memory_entry_count=len(entries),
        replay_status=str(replay.get("replay_status")) if replay.get("replay_status") else None,
        scheduler_apply_status=str(apply_packet.get("apply_status")) if apply_packet.get("apply_status") else None,
        proposal_reuse_status=str(reuse.get("reuse_status")) if reuse.get("reuse_status") else None,
        v02_scheduler_status=str(v02.get("adjustment_status")) if v02.get("adjustment_status") else None,
        dominant_probe_type=str(replay.get("dominant_probe_type")) if replay.get("dominant_probe_type") else None,
        scheduler_reuse_hint=str(replay.get("scheduler_reuse_hint")) if replay.get("scheduler_reuse_hint") else None,
        process_tensor_pressure=_pressure(metrics),
        history_depth=_int(metrics, "history_depth", 0),
        observation_debt_resolution_priority=_float(metrics, "observation_debt_resolution_priority", 0.0),
        safe_reentry_window_score=_float(metrics, "safe_reentry_window_score", 1.0),
        nonmarkov_link_density=_float(metrics, "nonmarkov_link_density", 1.0),
        memory_kernel_preservation_score=_float(metrics, "memory_kernel_preservation_score", 1.0),
        scheduler_state_mutation_performed=ready,
        scheduler_update_scope="replay_hint_only",
        memory_read_performed=True,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_scheduler_authority=False,
        grants_memory_write_authority=False,
        grants_memory_overwrite_authority=False,
        grants_world_update_authority=False,
        grants_control_packet_authority=False,
        grants_probe_execution_authority=False,
        replay_packet=replay,
        scheduler_apply_packet=apply_packet,
        proposal_reuse_packet=reuse,
        v02_scheduler_packet=v02,
        daemon_blockers=blockers,
        daemon_warnings=warnings,
    )
