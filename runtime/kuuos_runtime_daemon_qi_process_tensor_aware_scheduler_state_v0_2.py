#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_qi_process_tensor_aware_scheduler_state_v0_1 import step_qi_process_tensor_aware_scheduler_state
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_process_tensor_aware_scheduler_state_v0_1 import step_qi_process_tensor_aware_scheduler_state


@dataclass(frozen=True)
class QiProcessTensorAwareSchedulerStateV02:
    adjustment_version: str
    adjustment_status: str
    reused_proposal_status: str | None
    replay_reuse_integrated: bool
    reused_probe_family: str | None
    reused_scheduler_hint: str | None
    reused_probe_planner_hint: str | None
    base_result: dict[str, Any]
    v02_blockers: list[str]
    v02_warnings: list[str]
    process_tensor_aware: bool
    scheduler_state_updated: bool
    scheduler_authority_scope: str
    scheduler_state_mutation_performed: bool
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


def step_qi_process_tensor_aware_scheduler_state_v0_2(
    *,
    scheduler_state: Mapping[str, Any],
    scheduler_proposal: Mapping[str, Any],
    process_tensor_metrics: Mapping[str, Any],
    current_tick: int,
    proposal_reuse: Mapping[str, Any] | None = None,
) -> QiProcessTensorAwareSchedulerStateV02:
    reuse = _mapping(proposal_reuse)
    blockers: list[str] = []
    warnings: list[str] = []
    proposal = dict(_mapping(scheduler_proposal))

    reuse_status = reuse.get("reuse_status")
    reuse_ready = reuse_status == "QI_PROBE_SCHEDULER_PROPOSAL_REUSE_READY"
    if reuse:
        if not reuse_ready:
            blockers.append("proposal_reuse_not_ready")
        if reuse.get("proposal_reuse_only") is not True:
            blockers.append("proposal_reuse_only_not_true")
        if reuse.get("schedule_proposal_only") is not True:
            blockers.append("reuse_schedule_proposal_only_not_true")
        if reuse.get("scheduler_state_mutation_performed") is not False:
            blockers.append("reuse_scheduler_state_mutation_not_false")
        for key in [
            "memory_write_performed",
            "world_update_performed",
            "control_packet_mutation_performed",
            "probe_execution_performed",
            "grants_probe_execution_authority",
            "grants_world_update_authority",
            "grants_memory_write_authority",
        ]:
            if reuse.get(key) is not False:
                blockers.append(f"reuse_{key}_not_false")
        if reuse_ready:
            if reuse.get("proposed_schedule_mode"):
                proposal["recommended_schedule_mode"] = reuse.get("proposed_schedule_mode")
            if reuse.get("proposed_revisit_after_ticks") is not None:
                proposal["recommended_revisit_after_ticks"] = reuse.get("proposed_revisit_after_ticks")
            if reuse.get("proposed_revisit_reason"):
                proposal["recommended_revisit_reason"] = "replay-reuse: " + str(reuse.get("proposed_revisit_reason"))
            if reuse.get("reused_probe_family"):
                proposal["recommended_probe_type"] = reuse.get("reused_probe_family")
                proposal["source_recommended_probe_type"] = reuse.get("reused_probe_family")
    else:
        warnings.append("proposal_reuse_missing_v0_2_runs_v0_1_path")

    base = step_qi_process_tensor_aware_scheduler_state(
        scheduler_state=scheduler_state,
        scheduler_proposal=proposal,
        process_tensor_metrics=process_tensor_metrics,
        current_tick=current_tick,
    ).to_dict()
    if base.get("adjustment_status") != "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED":
        blockers.append("base_process_tensor_scheduler_not_updated")

    ready = not blockers
    return QiProcessTensorAwareSchedulerStateV02(
        adjustment_version="kuuos_runtime_daemon_qi_process_tensor_aware_scheduler_state_v0_2",
        adjustment_status="QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_UPDATED" if ready else "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_BLOCKED",
        reused_proposal_status=str(reuse_status) if reuse_status else None,
        replay_reuse_integrated=bool(reuse_ready and ready),
        reused_probe_family=str(reuse.get("reused_probe_family")) if reuse_ready and reuse.get("reused_probe_family") else None,
        reused_scheduler_hint=str(reuse.get("reused_scheduler_hint")) if reuse_ready and reuse.get("reused_scheduler_hint") else None,
        reused_probe_planner_hint=str(reuse.get("reused_probe_planner_hint")) if reuse_ready and reuse.get("reused_probe_planner_hint") else None,
        base_result=base,
        v02_blockers=blockers,
        v02_warnings=warnings,
        process_tensor_aware=True,
        scheduler_state_updated=bool(base.get("scheduler_state_updated")) and ready,
        scheduler_authority_scope="scheduler_state_only",
        scheduler_state_mutation_performed=bool(base.get("scheduler_state_updated")) and ready,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        memory_write_performed=False,
        world_update_performed=False,
    )
