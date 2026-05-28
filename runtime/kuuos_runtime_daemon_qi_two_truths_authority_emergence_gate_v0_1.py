#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiTwoTruthsAuthorityEmergenceGate:
    gate_version: str
    gate_status: str
    source_review_gate_status: str | None
    source_review_outcome: str | None
    authority_emergence_outcome: str
    authority_emergence_reason: str
    reviewed_probe_type: str | None
    reviewed_schedule_mode: str | None
    conventional_authority_scope: str | None
    ultimate_non_reification_preserved: bool
    dependent_origination_trace_present: bool
    two_truths_boundary_preserved: bool
    mass_gap_barrier_preserved: bool
    superstring_membrane_boundary_preserved: bool
    super_relativity_record_surface_present: bool
    causal_trace_present: bool
    rollback_path_present: bool
    safe_reentry_window_acceptable: bool
    observation_debt_targeted_or_bounded: bool
    memory_kernel_preservation_acceptable: bool
    authority_blockers: list[str]
    authority_warnings: list[str]
    authority_grant_candidate_only: bool
    actual_probe_execution_authority: bool
    authority_review_gate_only: bool
    execution_requires_separate_gate: bool
    local_limited_revocable: bool
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


def _truthy(payload: Mapping[str, Any], key: str) -> bool:
    return payload.get(key) is True


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


def evaluate_qi_two_truths_authority_emergence(
    *,
    review_gate_packet: Mapping[str, Any],
    authority_context: Mapping[str, Any] | None = None,
) -> QiTwoTruthsAuthorityEmergenceGate:
    review = _mapping(review_gate_packet)
    ctx = _mapping(authority_context)
    blockers: list[str] = []
    warnings: list[str] = []

    source_gate_status = str(review.get("gate_status")) if review.get("gate_status") else None
    source_review_outcome = str(review.get("review_outcome")) if review.get("review_outcome") else None
    probe_type = str(review.get("reviewed_probe_type")) if review.get("reviewed_probe_type") else None
    schedule_mode = str(review.get("reviewed_schedule_mode")) if review.get("reviewed_schedule_mode") else None
    conventional_scope = str(ctx.get("conventional_authority_scope")) if ctx.get("conventional_authority_scope") else None

    if source_gate_status != "QI_PROBE_EXECUTION_REVIEW_GATE_READY":
        blockers.append("review_gate_not_ready")
    if source_review_outcome != "READY_FOR_AUTHORITY_REVIEW":
        blockers.append("review_outcome_not_ready_for_authority_review")
    if review.get("ready_for_authority_review") is not True:
        blockers.append("ready_for_authority_review_not_true")
    if review.get("authority_review_required") is not True:
        blockers.append("authority_review_required_not_true")
    if review.get("authority") != "none":
        blockers.append("review_gate_authority_not_none")
    if not probe_type:
        blockers.append("reviewed_probe_type_missing")
    _require_false("review_gate", review, blockers)

    required_true = [
        "ultimate_non_reification_preserved",
        "dependent_origination_trace_present",
        "two_truths_boundary_preserved",
        "mass_gap_barrier_preserved",
        "superstring_membrane_boundary_preserved",
        "super_relativity_record_surface_present",
        "causal_trace_present",
        "rollback_path_present",
        "safe_reentry_window_acceptable",
        "observation_debt_targeted_or_bounded",
        "memory_kernel_preservation_acceptable",
    ]
    for key in required_true:
        if not _truthy(ctx, key):
            blockers.append(f"{key}_not_true")
    if not conventional_scope:
        blockers.append("conventional_authority_scope_missing")

    if ctx.get("authority_claims_ultimate_truth") is True:
        blockers.append("authority_claims_ultimate_truth")
    if ctx.get("authority_scope_unbounded") is True:
        blockers.append("authority_scope_unbounded")
    if ctx.get("authority_irrevocable") is True:
        blockers.append("authority_irrevocable")
    if ctx.get("mass_gap_collapsed") is True:
        blockers.append("mass_gap_collapsed")
    if ctx.get("direct_execution_requested") is True:
        blockers.append("direct_execution_requested")

    if ctx.get("operator_review_record_present") is not True:
        warnings.append("operator_review_record_not_present_yet")
    if ctx.get("governor_review_record_present") is not True:
        warnings.append("governor_review_record_not_present_yet")

    ready = not blockers
    return QiTwoTruthsAuthorityEmergenceGate(
        gate_version="kuuos_runtime_daemon_qi_two_truths_authority_emergence_gate_v0_1",
        gate_status="QI_TWO_TRUTHS_AUTHORITY_EMERGENCE_GATE_READY" if ready else "QI_TWO_TRUTHS_AUTHORITY_EMERGENCE_GATE_BLOCKED",
        source_review_gate_status=source_gate_status,
        source_review_outcome=source_review_outcome,
        authority_emergence_outcome="AUTHORITY_GRANT_CANDIDATE" if ready else "AUTHORITY_HOLD",
        authority_emergence_reason=(
            "two-truths authority emergence conditions hold; this is still only a local limited revocable grant candidate"
            if ready
            else "two-truths authority emergence conditions are not satisfied"
        ),
        reviewed_probe_type=probe_type if ready else None,
        reviewed_schedule_mode=schedule_mode if ready else None,
        conventional_authority_scope=conventional_scope if ready else None,
        ultimate_non_reification_preserved=_truthy(ctx, "ultimate_non_reification_preserved"),
        dependent_origination_trace_present=_truthy(ctx, "dependent_origination_trace_present"),
        two_truths_boundary_preserved=_truthy(ctx, "two_truths_boundary_preserved"),
        mass_gap_barrier_preserved=_truthy(ctx, "mass_gap_barrier_preserved"),
        superstring_membrane_boundary_preserved=_truthy(ctx, "superstring_membrane_boundary_preserved"),
        super_relativity_record_surface_present=_truthy(ctx, "super_relativity_record_surface_present"),
        causal_trace_present=_truthy(ctx, "causal_trace_present"),
        rollback_path_present=_truthy(ctx, "rollback_path_present"),
        safe_reentry_window_acceptable=_truthy(ctx, "safe_reentry_window_acceptable"),
        observation_debt_targeted_or_bounded=_truthy(ctx, "observation_debt_targeted_or_bounded"),
        memory_kernel_preservation_acceptable=_truthy(ctx, "memory_kernel_preservation_acceptable"),
        authority_blockers=blockers,
        authority_warnings=warnings,
        authority_grant_candidate_only=True,
        actual_probe_execution_authority=False,
        authority_review_gate_only=True,
        execution_requires_separate_gate=True,
        local_limited_revocable=True,
        scheduler_state_mutation_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        dry_run_execution_performed=False,
        next_tick_execution_performed=False,
        memory_write_performed=False,
        world_update_performed=False,
    )
