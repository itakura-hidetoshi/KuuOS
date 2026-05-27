#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiSchedulerStateResult:
    scheduler_version: str
    scheduler_status: str
    current_tick: int
    last_scheduled_tick: int | None
    next_due_tick: int | None
    due_status: str
    source_scheduler_proposal_status: str | None
    scheduled_probe_type: str | None
    scheduled_mode: str | None
    scheduler_state: dict[str, Any]
    scheduler_blockers: list[str]
    scheduler_warnings: list[str]
    scheduler_state_updated: bool
    scheduler_authority_scope: str
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    memory_write_performed: bool
    world_update_performed: bool
    authority: str = "scheduler_state"
    grants_scheduler_authority: bool = True
    grants_execution_authority: bool = False
    grants_probe_execution_authority: bool = False
    grants_dry_run_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_control_packet_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_world_update_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _safe_int(value: Any, default: int | None = None) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _proposal_ok(proposal: Mapping[str, Any], blockers: list[str]) -> None:
    if proposal.get("scheduler_status") != "QI_PROBE_SCHEDULER_PROPOSAL_READY":
        blockers.append("scheduler_proposal_not_ready")
    if proposal.get("schedule_proposal_only") is not True:
        blockers.append("scheduler_proposal_flag_missing")
    if proposal.get("authority") != "none":
        blockers.append("scheduler_proposal_authority_not_none")
    for key in [
        "grants_execution_authority",
        "grants_probe_execution_authority",
        "grants_dry_run_execution_authority",
        "grants_next_tick_execution_authority",
        "grants_control_packet_authority",
        "grants_memory_overwrite_authority",
        "grants_world_update_authority",
    ]:
        if proposal.get(key) is not False:
            blockers.append(f"scheduler_proposal_{key}_not_false")


def step_qi_scheduler_state(
    *,
    scheduler_state: Mapping[str, Any],
    scheduler_proposal: Mapping[str, Any],
    current_tick: int,
) -> QiSchedulerStateResult:
    state = dict(_mapping(scheduler_state))
    proposal = _mapping(scheduler_proposal)
    blockers: list[str] = []
    warnings: list[str] = []

    _proposal_ok(proposal, blockers)
    if current_tick < 0:
        blockers.append("current_tick_negative")

    revisit_after = _safe_int(proposal.get("recommended_revisit_after_ticks"), None)
    if revisit_after is None or revisit_after < 1:
        blockers.append("recommended_revisit_after_ticks_invalid")
        revisit_after = None

    last_tick = _safe_int(state.get("last_scheduled_tick"), None)
    if last_tick is None:
        last_tick = current_tick
        warnings.append("last_scheduled_tick_missing_initialized_to_current_tick")

    next_due_tick = last_tick + revisit_after if revisit_after is not None else None
    due_status = "BLOCKED"
    state_updated = False
    if not blockers and next_due_tick is not None:
        due_status = "DUE" if current_tick >= next_due_tick else "WAIT"
        state.update({
            "scheduler_state_version": "qi_scheduler_state_v0_1",
            "last_observed_tick": current_tick,
            "last_scheduled_tick": last_tick,
            "next_due_tick": next_due_tick,
            "due_status": due_status,
            "scheduled_probe_type": proposal.get("source_recommended_probe_type"),
            "scheduled_mode": proposal.get("recommended_schedule_mode"),
        })
        state_updated = True

    return QiSchedulerStateResult(
        scheduler_version="kuuos_runtime_daemon_qi_scheduler_state_v0_1",
        scheduler_status="QI_SCHEDULER_STATE_UPDATED" if state_updated else "QI_SCHEDULER_STATE_BLOCKED",
        current_tick=current_tick,
        last_scheduled_tick=last_tick,
        next_due_tick=next_due_tick,
        due_status=due_status,
        source_scheduler_proposal_status=str(proposal.get("scheduler_status")) if proposal.get("scheduler_status") else None,
        scheduled_probe_type=str(proposal.get("source_recommended_probe_type")) if proposal.get("source_recommended_probe_type") else None,
        scheduled_mode=str(proposal.get("recommended_schedule_mode")) if proposal.get("recommended_schedule_mode") else None,
        scheduler_state=state,
        scheduler_blockers=blockers,
        scheduler_warnings=warnings,
        scheduler_state_updated=state_updated,
        scheduler_authority_scope="scheduler_state_only",
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        memory_write_performed=False,
        world_update_performed=False,
    )
