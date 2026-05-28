#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiProbeSchedulerProposalReuse:
    reuse_version: str
    reuse_status: str
    source_apply_status: str | None
    source_scheduler_update_kind: str | None
    reused_probe_family: str | None
    reused_scheduler_hint: str | None
    reused_probe_planner_hint: str | None
    proposed_schedule_mode: str | None
    proposed_revisit_after_ticks: int | None
    proposed_revisit_reason: str | None
    proposal_reuse_only: bool
    schedule_proposal_only: bool
    scheduler_state_read_performed: bool
    scheduler_state_mutation_performed: bool
    memory_read_performed: bool
    memory_write_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_scheduler_authority: bool
    grants_memory_write_authority: bool
    grants_world_update_authority: bool
    grants_control_packet_authority: bool
    grants_probe_execution_authority: bool
    reuse_blockers: list[str]
    reuse_warnings: list[str]
    authority: str = "none"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _schedule_for_probe(probe_type: str | None) -> tuple[str, int, str]:
    if probe_type == "recoverability_branch_probe":
        return "near_term_revisit", 1, "MemoryOS replay suggests recoverability branch should be revisited quickly"
    if probe_type == "observation_debt_probe":
        return "near_term_revisit", 1, "MemoryOS replay suggests observation debt remains scheduler-relevant"
    if probe_type == "safe_reentry_window_probe":
        return "short_horizon_revisit", 2, "MemoryOS replay suggests safe reentry window should be rechecked"
    if probe_type == "memory_kernel_probe":
        return "short_horizon_revisit", 2, "MemoryOS replay suggests memory kernel continuity should be rechecked"
    if probe_type == "nonmarkov_memory_link_probe":
        return "medium_horizon_revisit", 3, "MemoryOS replay suggests non-Markov link structure should be reused"
    if probe_type == "multi_time_correlation_probe":
        return "medium_horizon_revisit", 3, "MemoryOS replay suggests multi-time correlation remains relevant"
    if probe_type == "continue_process_tensor_supervision_probe":
        return "routine_revisit", 5, "MemoryOS replay suggests stable process tensor supervision"
    return "manual_review_revisit", 1, "MemoryOS replay probe family is missing or unrecognized"


def build_qi_probe_scheduler_proposal_reuse(*, replay_applied_scheduler_state: Mapping[str, Any], reuse_context: Mapping[str, Any] | None = None) -> QiProbeSchedulerProposalReuse:
    state = _mapping(replay_applied_scheduler_state)
    ctx = _mapping(reuse_context)
    blockers: list[str] = []
    warnings: list[str] = []

    apply_status = state.get("apply_status")
    nested_state = _mapping(state.get("next_scheduler_state")) or state
    update_kind = nested_state.get("scheduler_update_kind")
    probe_family = nested_state.get("replay_dominant_probe_type")
    scheduler_hint = nested_state.get("replay_scheduler_reuse_hint")
    planner_hint = nested_state.get("replay_probe_planner_reuse_hint")

    if apply_status is not None and apply_status != "QI_REPLAY_SCHEDULER_STATE_APPLY_PERFORMED":
        blockers.append("replay_scheduler_apply_not_performed")
    if update_kind != "memoryos_process_tensor_replay_hint":
        blockers.append("scheduler_update_kind_not_replay_hint")
    if not probe_family:
        blockers.append("replay_dominant_probe_type_missing")
    if not scheduler_hint:
        blockers.append("replay_scheduler_reuse_hint_missing")
    if nested_state.get("lineage_preserved") is not True:
        blockers.append("scheduler_lineage_not_preserved")

    if ctx.get("reuse_scope") not in (None, "proposal_only"):
        blockers.append("reuse_scope_not_proposal_only")
    if ctx.get("request_scheduler_state_mutation") is True:
        blockers.append("request_scheduler_state_mutation")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")
    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_control_packet_mutation") is True:
        blockers.append("request_control_packet_mutation")

    mode, ticks, reason = _schedule_for_probe(str(probe_family) if probe_family else None)
    ready = not blockers
    return QiProbeSchedulerProposalReuse(
        reuse_version="kuuos_runtime_daemon_qi_probe_scheduler_proposal_reuse_v0_1",
        reuse_status="QI_PROBE_SCHEDULER_PROPOSAL_REUSE_READY" if ready else "QI_PROBE_SCHEDULER_PROPOSAL_REUSE_BLOCKED",
        source_apply_status=str(apply_status) if apply_status else None,
        source_scheduler_update_kind=str(update_kind) if update_kind else None,
        reused_probe_family=str(probe_family) if ready else None,
        reused_scheduler_hint=str(scheduler_hint) if ready else None,
        reused_probe_planner_hint=str(planner_hint) if planner_hint and ready else None,
        proposed_schedule_mode=mode if ready else None,
        proposed_revisit_after_ticks=ticks if ready else None,
        proposed_revisit_reason=reason if ready else None,
        proposal_reuse_only=True,
        schedule_proposal_only=True,
        scheduler_state_read_performed=True,
        scheduler_state_mutation_performed=False,
        memory_read_performed=False,
        memory_write_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_scheduler_authority=False,
        grants_memory_write_authority=False,
        grants_world_update_authority=False,
        grants_control_packet_authority=False,
        grants_probe_execution_authority=False,
        reuse_blockers=blockers,
        reuse_warnings=warnings,
    )
