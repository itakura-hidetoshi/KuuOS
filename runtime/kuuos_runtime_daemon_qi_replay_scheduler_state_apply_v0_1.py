#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiReplaySchedulerStateApply:
    apply_version: str
    apply_status: str
    source_replay_status: str | None
    previous_scheduler_status: str | None
    applied_probe_family: str | None
    applied_replay_hint: str | None
    scheduler_state_update_kind: str
    scheduler_state_mutation_performed: bool
    scheduler_update_scope: str
    scheduler_lineage_preserved: bool
    memory_read_performed: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_scheduler_authority: bool
    grants_memory_write_authority: bool
    grants_world_update_authority: bool
    grants_control_packet_authority: bool
    grants_probe_execution_authority: bool
    next_scheduler_state: dict[str, Any]
    apply_blockers: list[str]
    apply_warnings: list[str]
    authority: str = "scheduler_state_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def apply_qi_replay_scheduler_state(
    *,
    replay_packet: Mapping[str, Any],
    scheduler_state: Mapping[str, Any] | None = None,
    apply_context: Mapping[str, Any] | None = None,
) -> QiReplaySchedulerStateApply:
    replay = _mapping(replay_packet)
    state = dict(_mapping(scheduler_state))
    ctx = _mapping(apply_context)
    blockers: list[str] = []
    warnings: list[str] = []

    replay_status = replay.get("replay_status")
    previous_status = state.get("scheduler_status")
    dominant_probe = replay.get("dominant_probe_type")
    scheduler_hint = replay.get("scheduler_reuse_hint")

    if replay_status != "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY":
        blockers.append("replay_not_ready")
    if replay.get("retrieval_only") is not True:
        blockers.append("replay_retrieval_only_not_true")
    if replay.get("replay_surface_only") is not True:
        blockers.append("replay_surface_only_not_true")
    if replay.get("memory_read_performed") is not True:
        blockers.append("replay_memory_read_not_true")
    if not dominant_probe:
        blockers.append("dominant_probe_type_missing")
    if not scheduler_hint:
        blockers.append("scheduler_reuse_hint_missing")

    for key in [
        "memory_write_performed",
        "memory_append_performed",
        "memory_overwrite_performed",
        "world_update_performed",
        "control_packet_mutation_performed",
        "scheduler_state_mutation_performed",
        "grants_memory_write_authority",
        "grants_world_update_authority",
        "grants_probe_execution_authority",
    ]:
        if replay.get(key) is not False:
            blockers.append(f"replay_{key}_not_false")

    if ctx.get("allow_scheduler_state_update") is not True:
        blockers.append("allow_scheduler_state_update_not_true")
    if ctx.get("scheduler_update_scope") not in ("replay_hint_only", None):
        blockers.append("scheduler_update_scope_not_replay_hint_only")
    if ctx.get("scheduler_lineage_preserved") is not True:
        blockers.append("scheduler_lineage_preserved_not_true")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")
    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_control_packet_mutation") is True:
        blockers.append("request_control_packet_mutation")

    ready = not blockers
    next_state = dict(state)
    if ready:
        next_state.update({
            "scheduler_status": "QI_SCHEDULER_STATE_UPDATED_BY_MEMORYOS_REPLAY",
            "scheduler_update_kind": "memoryos_process_tensor_replay_hint",
            "replay_dominant_probe_type": dominant_probe,
            "replay_scheduler_reuse_hint": scheduler_hint,
            "replay_probe_planner_reuse_hint": replay.get("probe_planner_reuse_hint"),
            "lineage_preserved": True,
        })
    return QiReplaySchedulerStateApply(
        apply_version="kuuos_runtime_daemon_qi_replay_scheduler_state_apply_v0_1",
        apply_status="QI_REPLAY_SCHEDULER_STATE_APPLY_PERFORMED" if ready else "QI_REPLAY_SCHEDULER_STATE_APPLY_BLOCKED",
        source_replay_status=str(replay_status) if replay_status else None,
        previous_scheduler_status=str(previous_status) if previous_status else None,
        applied_probe_family=str(dominant_probe) if ready else None,
        applied_replay_hint=str(scheduler_hint) if ready else None,
        scheduler_state_update_kind="memoryos_process_tensor_replay_hint" if ready else "none",
        scheduler_state_mutation_performed=ready,
        scheduler_update_scope="replay_hint_only",
        scheduler_lineage_preserved=ready,
        memory_read_performed=True,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_scheduler_authority=False,
        grants_memory_write_authority=False,
        grants_world_update_authority=False,
        grants_control_packet_authority=False,
        grants_probe_execution_authority=False,
        next_scheduler_state=next_state if ready else state,
        apply_blockers=blockers,
        apply_warnings=warnings,
    )
