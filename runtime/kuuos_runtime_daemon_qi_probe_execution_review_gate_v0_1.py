#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiProbeExecutionReviewGate:
    gate_version: str
    gate_status: str
    source_candidate_status: str | None
    reviewed_probe_type: str | None
    reviewed_schedule_mode: str | None
    review_outcome: str
    review_reason: str
    review_blockers: list[str]
    review_warnings: list[str]
    candidate_review_only: bool
    execution_review_gate_only: bool
    requires_operator_review: bool
    requires_governor_approval: bool
    ready_for_authority_review: bool
    authority_review_required: bool
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
        "grants_scheduler_authority",
        "grants_control_packet_authority",
        "grants_memory_overwrite_authority",
        "grants_world_update_authority",
        "scheduler_state_mutation_performed",
        "control_packet_mutation_performed",
        "probe_execution_performed",
        "dry_run_execution_performed",
        "next_tick_execution_performed",
        "memory_write_performed",
        "world_update_performed",
    ]:
        if payload.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def review_qi_probe_execution_candidate(*, candidate_packet: Mapping[str, Any]) -> QiProbeExecutionReviewGate:
    candidate = _mapping(candidate_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    source_status = str(candidate.get("candidate_status")) if candidate.get("candidate_status") else None
    probe_type = str(candidate.get("candidate_probe_type")) if candidate.get("candidate_probe_type") else None
    schedule_mode = str(candidate.get("candidate_schedule_mode")) if candidate.get("candidate_schedule_mode") else None

    if source_status != "QI_PROBE_EXECUTION_CANDIDATE_READY":
        blockers.append("candidate_not_ready")
    if candidate.get("execution_candidate_only") is not True:
        blockers.append("execution_candidate_only_not_true")
    if candidate.get("scheduler_due_required") is not True:
        blockers.append("scheduler_due_required_not_true")
    if candidate.get("scheduler_due_satisfied") is not True:
        blockers.append("scheduler_due_not_satisfied")
    if candidate.get("requires_operator_review") is not True:
        blockers.append("candidate_operator_review_not_required")
    if candidate.get("requires_governor_approval") is not True:
        blockers.append("candidate_governor_approval_not_required")
    if candidate.get("authority") != "none":
        blockers.append("candidate_authority_not_none")
    if not probe_type:
        blockers.append("candidate_probe_type_missing")
    if not schedule_mode:
        warnings.append("candidate_schedule_mode_missing")
    _require_false("candidate", candidate, blockers)

    ready = not blockers
    return QiProbeExecutionReviewGate(
        gate_version="kuuos_runtime_daemon_qi_probe_execution_review_gate_v0_1",
        gate_status="QI_PROBE_EXECUTION_REVIEW_GATE_READY" if ready else "QI_PROBE_EXECUTION_REVIEW_GATE_BLOCKED",
        source_candidate_status=source_status,
        reviewed_probe_type=probe_type if ready else None,
        reviewed_schedule_mode=schedule_mode if ready else None,
        review_outcome="READY_FOR_AUTHORITY_REVIEW" if ready else "HOLD",
        review_reason=(
            "candidate passed non-executing review gate; separate authority gate is still required before any execution"
            if ready
            else "candidate failed non-executing review gate"
        ),
        review_blockers=blockers,
        review_warnings=warnings,
        candidate_review_only=True,
        execution_review_gate_only=True,
        requires_operator_review=True,
        requires_governor_approval=True,
        ready_for_authority_review=ready,
        authority_review_required=True,
        scheduler_state_mutation_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        dry_run_execution_performed=False,
        next_tick_execution_performed=False,
        memory_write_performed=False,
        world_update_performed=False,
    )
