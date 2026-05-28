#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_qi_probe_execution_candidate_v0_1 import build_qi_probe_execution_candidate
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_probe_execution_candidate_v0_1 import build_qi_probe_execution_candidate


@dataclass(frozen=True)
class QiV02ExecutionCandidateBridge:
    bridge_version: str
    bridge_status: str
    source_v02_status: str | None
    source_base_status: str | None
    candidate_status: str | None
    candidate_packet: dict[str, Any]
    v02_replay_reuse_integrated: bool
    v02_scheduler_state_updated: bool
    v02_scheduler_authority_scope: str | None
    bridge_candidate_only: bool
    execution_candidate_only: bool
    scheduler_due_required: bool
    scheduler_due_satisfied: bool
    requires_operator_review: bool
    requires_governor_approval: bool
    bridge_blockers: list[str]
    bridge_warnings: list[str]
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


def _require_false(prefix: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
        "grants_execution_authority",
        "grants_probe_execution_authority",
        "grants_dry_run_execution_authority",
        "grants_next_tick_execution_authority",
        "grants_control_packet_authority",
        "grants_memory_overwrite_authority",
        "grants_world_update_authority",
        "control_packet_mutation_performed",
        "probe_execution_performed",
        "memory_write_performed",
        "world_update_performed",
    ]:
        if payload.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def build_qi_v02_execution_candidate_bridge(*, v02_scheduler_surface: Mapping[str, Any]) -> QiV02ExecutionCandidateBridge:
    surface = _mapping(v02_scheduler_surface)
    base = _mapping(surface.get("base_result"))
    blockers: list[str] = []
    warnings: list[str] = []

    source_v02_status = str(surface.get("adjustment_status")) if surface.get("adjustment_status") else None
    source_base_status = str(base.get("adjustment_status")) if base.get("adjustment_status") else None

    if source_v02_status != "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_UPDATED":
        blockers.append("v02_scheduler_status_not_updated")
    if source_base_status != "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED":
        blockers.append("v02_base_scheduler_status_not_v0_1_updated")
    if surface.get("scheduler_state_updated") is not True:
        blockers.append("v02_scheduler_state_updated_not_true")
    if surface.get("scheduler_authority_scope") != "scheduler_state_only":
        blockers.append("v02_scheduler_authority_scope_not_scheduler_state_only")
    if surface.get("replay_reuse_integrated") is not True:
        warnings.append("v02_replay_reuse_not_integrated")
    if surface.get("authority") != "scheduler_state":
        blockers.append("v02_authority_not_scheduler_state")
    if surface.get("grants_scheduler_authority") is not True:
        blockers.append("v02_scheduler_authority_not_true")
    _require_false("v02", surface, blockers)

    adapted = dict(base)
    adapted["adjustment_status"] = "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED"
    adapted["process_tensor_aware"] = True
    adapted["authority"] = "scheduler_state"
    adapted["grants_scheduler_authority"] = True
    adapted["grants_execution_authority"] = False
    adapted["grants_probe_execution_authority"] = False
    adapted["grants_dry_run_execution_authority"] = False
    adapted["grants_next_tick_execution_authority"] = False
    adapted["grants_control_packet_authority"] = False
    adapted["grants_memory_overwrite_authority"] = False
    adapted["grants_world_update_authority"] = False

    candidate = build_qi_probe_execution_candidate(scheduler_surface=adapted).to_dict() if base else {}
    if candidate.get("candidate_status") != "QI_PROBE_EXECUTION_CANDIDATE_READY":
        blockers.append("candidate_not_ready_from_v02_surface")
    ready = not blockers
    return QiV02ExecutionCandidateBridge(
        bridge_version="kuuos_runtime_daemon_qi_v02_execution_candidate_bridge_v0_1",
        bridge_status="QI_V02_EXECUTION_CANDIDATE_BRIDGE_READY" if ready else "QI_V02_EXECUTION_CANDIDATE_BRIDGE_BLOCKED",
        source_v02_status=source_v02_status,
        source_base_status=source_base_status,
        candidate_status=str(candidate.get("candidate_status")) if candidate.get("candidate_status") else None,
        candidate_packet=candidate if ready else candidate,
        v02_replay_reuse_integrated=surface.get("replay_reuse_integrated") is True,
        v02_scheduler_state_updated=surface.get("scheduler_state_updated") is True,
        v02_scheduler_authority_scope=str(surface.get("scheduler_authority_scope")) if surface.get("scheduler_authority_scope") else None,
        bridge_candidate_only=True,
        execution_candidate_only=candidate.get("execution_candidate_only") is True,
        scheduler_due_required=candidate.get("scheduler_due_required") is True,
        scheduler_due_satisfied=candidate.get("scheduler_due_satisfied") is True and ready,
        requires_operator_review=True,
        requires_governor_approval=True,
        bridge_blockers=blockers,
        bridge_warnings=warnings,
        scheduler_state_mutation_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        dry_run_execution_performed=False,
        next_tick_execution_performed=False,
        memory_write_performed=False,
        world_update_performed=False,
    )
