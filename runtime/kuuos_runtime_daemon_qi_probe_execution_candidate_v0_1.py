#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiProbeExecutionCandidate:
    candidate_version: str
    candidate_status: str
    source_adjustment_status: str | None
    source_scheduler_status: str | None
    source_due_status: str | None
    candidate_probe_type: str | None
    candidate_schedule_mode: str | None
    candidate_reason: str
    candidate_blockers: list[str]
    candidate_warnings: list[str]
    execution_candidate_only: bool
    scheduler_due_required: bool
    scheduler_due_satisfied: bool
    requires_operator_review: bool
    requires_governor_approval: bool
    scheduler_state_mutation_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    dry_run_execution_performed: bool
    next_tick_execution_performed: bool
    memory_write_performed: bool
    world_update_performed: bool
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


def _false_grants(prefix: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
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


def build_qi_probe_execution_candidate(*, scheduler_surface: Mapping[str, Any]) -> QiProbeExecutionCandidate:
    surface = _mapping(scheduler_surface)
    scheduler_result = _mapping(surface.get("scheduler_result")) or surface
    blockers: list[str] = []
    warnings: list[str] = []

    source_adjustment_status = str(surface.get("adjustment_status")) if surface.get("adjustment_status") else None
    source_scheduler_status = str(scheduler_result.get("scheduler_status")) if scheduler_result.get("scheduler_status") else None
    source_due_status = str(scheduler_result.get("due_status")) if scheduler_result.get("due_status") else None
    candidate_probe_type = str(scheduler_result.get("scheduled_probe_type")) if scheduler_result.get("scheduled_probe_type") else None
    candidate_schedule_mode = str(scheduler_result.get("scheduled_mode")) if scheduler_result.get("scheduled_mode") else None

    if source_adjustment_status is not None and source_adjustment_status != "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED":
        blockers.append("process_tensor_scheduler_adjustment_not_ready")
    if source_adjustment_status is None:
        warnings.append("source_adjustment_status_missing")
    if source_scheduler_status != "QI_SCHEDULER_STATE_UPDATED":
        blockers.append("scheduler_state_not_updated")
    if source_due_status != "DUE":
        blockers.append("scheduler_due_status_not_due")
    if not candidate_probe_type:
        blockers.append("scheduled_probe_type_missing")

    if surface.get("process_tensor_aware") is not True:
        warnings.append("process_tensor_aware_not_true")
    if surface.get("authority") not in (None, "scheduler_state"):
        blockers.append("source_authority_not_scheduler_state")
    if surface.get("grants_scheduler_authority") not in (None, True):
        blockers.append("source_scheduler_authority_not_true")
    _false_grants("source", surface, blockers)
    _false_grants("scheduler_result", scheduler_result, blockers)

    ready = not blockers
    reason = (
        "scheduler is DUE; candidate packet is ready for operator/governor review without execution authority"
        if ready
        else "scheduler is not in a candidate-ready state"
    )
    return QiProbeExecutionCandidate(
        candidate_version="kuuos_runtime_daemon_qi_probe_execution_candidate_v0_1",
        candidate_status="QI_PROBE_EXECUTION_CANDIDATE_READY" if ready else "QI_PROBE_EXECUTION_CANDIDATE_BLOCKED",
        source_adjustment_status=source_adjustment_status,
        source_scheduler_status=source_scheduler_status,
        source_due_status=source_due_status,
        candidate_probe_type=candidate_probe_type if ready else None,
        candidate_schedule_mode=candidate_schedule_mode if ready else None,
        candidate_reason=reason,
        candidate_blockers=blockers,
        candidate_warnings=warnings,
        execution_candidate_only=True,
        scheduler_due_required=True,
        scheduler_due_satisfied=source_due_status == "DUE" and ready,
        requires_operator_review=True,
        requires_governor_approval=True,
        scheduler_state_mutation_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        dry_run_execution_performed=False,
        next_tick_execution_performed=False,
        memory_write_performed=False,
        world_update_performed=False,
    )
