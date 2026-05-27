#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiProbeSchedulerProposal:
    scheduler_version: str
    scheduler_status: str
    recommended_schedule_mode: str | None
    recommended_revisit_after_ticks: int | None
    recommended_revisit_reason: str | None
    source_lattice_status: str | None
    source_recommended_probe_type: str | None
    scheduler_blockers: list[str]
    scheduler_warnings: list[str]
    schedule_proposal_only: bool
    counterfactual_only: bool
    simulation_only: bool
    dry_run_only: bool
    scheduler_mutation_performed: bool
    control_packet_mutation_performed: bool
    memory_write_performed: bool
    authority: str = "none"
    grants_execution_authority: bool = False
    grants_probe_execution_authority: bool = False
    grants_dry_run_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_scheduler_authority: bool = False
    grants_control_packet_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_world_update_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _no_authority(prefix: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    if payload.get("authority") != "none":
        blockers.append(f"{prefix}_authority_not_none")
    for key in [
        "grants_execution_authority",
        "grants_probe_execution_authority",
        "grants_dry_run_execution_authority",
        "grants_next_tick_execution_authority",
        "grants_control_packet_authority",
        "grants_memory_overwrite_authority",
        "grants_world_update_authority",
    ]:
        if payload.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def _schedule_for_probe(probe_type: str | None) -> tuple[str, int, str]:
    if probe_type == "recoverability_branch_probe":
        return "near_term_revisit", 1, "recoverability branch information should be revisited quickly"
    if probe_type == "observation_debt_probe":
        return "near_term_revisit", 1, "observation debt is likely limiting process visibility"
    if probe_type == "safe_reentry_window_probe":
        return "short_horizon_revisit", 2, "safe reentry window may contract if not rechecked"
    if probe_type == "memory_kernel_probe":
        return "short_horizon_revisit", 2, "memory kernel continuity should be rechecked before escalation"
    if probe_type == "nonmarkov_memory_link_probe":
        return "medium_horizon_revisit", 3, "non-Markov link structure benefits from another observation interval"
    if probe_type == "multi_time_correlation_probe":
        return "medium_horizon_revisit", 3, "multi-time correlation visibility needs accumulated observations"
    if probe_type == "continue_process_tensor_supervision_probe":
        return "routine_revisit", 5, "stable supervision can be revisited at a routine cadence"
    return "manual_review_revisit", 1, "probe type is missing or unrecognized"


def build_qi_probe_scheduler_proposal(*, counterfactual_lattice: Mapping[str, Any]) -> QiProbeSchedulerProposal:
    lattice = _mapping(counterfactual_lattice)
    blockers: list[str] = []
    warnings: list[str] = []

    if lattice.get("lattice_status") != "QI_COUNTERFACTUAL_PROBE_LATTICE_READY":
        blockers.append("counterfactual_lattice_not_ready")
    for key in ["counterfactual_only", "simulation_only", "dry_run_only"]:
        if lattice.get(key) is not True:
            blockers.append(f"counterfactual_lattice_{key}_not_true")
    for key in ["state_mutation_performed", "control_packet_mutation_performed", "memory_write_performed"]:
        if lattice.get(key) is not False:
            blockers.append(f"counterfactual_lattice_{key}_not_false")
    _no_authority("counterfactual_lattice", lattice, blockers)

    probe_type = lattice.get("recommended_probe_type") or lattice.get("chosen_probe_type")
    if not probe_type:
        warnings.append("recommended_probe_type_missing")
    mode, ticks, reason = _schedule_for_probe(str(probe_type) if probe_type else None)
    ready = not blockers
    return QiProbeSchedulerProposal(
        scheduler_version="kuuos_runtime_daemon_qi_probe_scheduler_proposal_v0_1",
        scheduler_status="QI_PROBE_SCHEDULER_PROPOSAL_READY" if ready else "QI_PROBE_SCHEDULER_PROPOSAL_BLOCKED",
        recommended_schedule_mode=mode if ready else None,
        recommended_revisit_after_ticks=ticks if ready else None,
        recommended_revisit_reason=reason if ready else None,
        source_lattice_status=str(lattice.get("lattice_status")) if lattice.get("lattice_status") else None,
        source_recommended_probe_type=str(probe_type) if probe_type else None,
        scheduler_blockers=blockers,
        scheduler_warnings=warnings,
        schedule_proposal_only=True,
        counterfactual_only=True,
        simulation_only=True,
        dry_run_only=True,
        scheduler_mutation_performed=False,
        control_packet_mutation_performed=False,
        memory_write_performed=False,
    )
