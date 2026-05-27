#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_qi_scheduler_state_v0_1 import step_qi_scheduler_state
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_scheduler_state_v0_1 import step_qi_scheduler_state


@dataclass(frozen=True)
class QiProcessTensorSchedulerAdjustment:
    adjustment_version: str
    adjustment_status: str
    base_revisit_after_ticks: int | None
    adjusted_revisit_after_ticks: int | None
    adjustment_reason: str
    process_tensor_pressure_level: str
    observation_debt_priority: float | None
    safe_reentry_window_score: float | None
    nonmarkov_link_density: float | None
    memory_kernel_preservation_score: float | None
    scheduler_result: dict[str, Any]
    adjustment_blockers: list[str]
    adjustment_warnings: list[str]
    process_tensor_aware: bool
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


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _clamp_tick(value: int | None) -> int | None:
    if value is None:
        return None
    return max(1, min(8, int(value)))


def _adjust_revisit_ticks(base_ticks: int | None, metrics: Mapping[str, Any]) -> tuple[int | None, str, str, list[str]]:
    warnings: list[str] = []
    if base_ticks is None:
        return None, "base revisit ticks missing", "unknown", warnings

    debt = _float_or_none(metrics.get("observation_debt_resolution_priority"))
    safe = _float_or_none(metrics.get("safe_reentry_window_score"))
    nonmarkov = _float_or_none(metrics.get("nonmarkov_link_density"))
    memory = _float_or_none(metrics.get("memory_kernel_preservation_score"))
    history = _float_or_none(metrics.get("history_depth"))

    if debt is None:
        warnings.append("observation_debt_resolution_priority_missing")
    if safe is None:
        warnings.append("safe_reentry_window_score_missing")
    if nonmarkov is None:
        warnings.append("nonmarkov_link_density_missing")
    if memory is None:
        warnings.append("memory_kernel_preservation_score_missing")

    pressure = 0
    reasons: list[str] = []
    if debt is not None and debt >= 0.70:
        pressure += 2
        reasons.append("high observation debt")
    elif debt is not None and debt >= 0.45:
        pressure += 1
        reasons.append("moderate observation debt")

    if safe is not None and safe <= 0.35:
        pressure += 2
        reasons.append("narrow safe reentry window")
    elif safe is not None and safe <= 0.55:
        pressure += 1
        reasons.append("moderate safe reentry constraint")

    if nonmarkov is not None and nonmarkov <= 0.25:
        pressure += 1
        reasons.append("sparse non-Markov links")
    if memory is not None and memory <= 0.45:
        pressure += 1
        reasons.append("fragile memory kernel")
    if history is not None and history >= 4:
        reasons.append("sufficient history depth for process-tensor scheduling")

    if pressure >= 4:
        adjusted = 1
        level = "high_process_tensor_pressure"
    elif pressure >= 2:
        adjusted = max(1, base_ticks - 1)
        level = "moderate_process_tensor_pressure"
    else:
        adjusted = base_ticks
        level = "low_process_tensor_pressure"
    reason = "; ".join(reasons) if reasons else "no strong process-tensor pressure detected"
    return _clamp_tick(adjusted), reason, level, warnings


def step_qi_process_tensor_aware_scheduler_state(
    *,
    scheduler_state: Mapping[str, Any],
    scheduler_proposal: Mapping[str, Any],
    process_tensor_metrics: Mapping[str, Any],
    current_tick: int,
) -> QiProcessTensorSchedulerAdjustment:
    proposal = dict(_mapping(scheduler_proposal))
    metrics = _mapping(process_tensor_metrics)
    blockers: list[str] = []
    warnings: list[str] = []

    if metrics.get("process_tensor_advantage_level") in (None, ""):
        warnings.append("process_tensor_advantage_level_missing")
    base_ticks = _int_or_none(proposal.get("recommended_revisit_after_ticks"))
    adjusted_ticks, reason, pressure_level, adjust_warnings = _adjust_revisit_ticks(base_ticks, metrics)
    warnings.extend(adjust_warnings)
    if adjusted_ticks is None:
        blockers.append("adjusted_revisit_after_ticks_missing")
    else:
        proposal["recommended_revisit_after_ticks"] = adjusted_ticks
        proposal["recommended_revisit_reason"] = f"process-tensor aware: {reason}"

    scheduler_result = step_qi_scheduler_state(
        scheduler_state=scheduler_state,
        scheduler_proposal=proposal,
        current_tick=current_tick,
    ).to_dict()
    if scheduler_result.get("scheduler_status") != "QI_SCHEDULER_STATE_UPDATED":
        blockers.append("scheduler_state_update_not_ready")

    ready = not blockers
    return QiProcessTensorSchedulerAdjustment(
        adjustment_version="kuuos_runtime_daemon_qi_process_tensor_aware_scheduler_state_v0_1",
        adjustment_status="QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED" if ready else "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_BLOCKED",
        base_revisit_after_ticks=base_ticks,
        adjusted_revisit_after_ticks=adjusted_ticks if ready else None,
        adjustment_reason=reason,
        process_tensor_pressure_level=pressure_level,
        observation_debt_priority=_float_or_none(metrics.get("observation_debt_resolution_priority")),
        safe_reentry_window_score=_float_or_none(metrics.get("safe_reentry_window_score")),
        nonmarkov_link_density=_float_or_none(metrics.get("nonmarkov_link_density")),
        memory_kernel_preservation_score=_float_or_none(metrics.get("memory_kernel_preservation_score")),
        scheduler_result=scheduler_result,
        adjustment_blockers=blockers,
        adjustment_warnings=warnings,
        process_tensor_aware=True,
        scheduler_state_updated=bool(scheduler_result.get("scheduler_state_updated")) and ready,
        scheduler_authority_scope="scheduler_state_only",
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        memory_write_performed=False,
        world_update_performed=False,
    )
