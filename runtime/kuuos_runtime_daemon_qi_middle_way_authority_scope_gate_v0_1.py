#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiMiddleWayAuthorityScopeGate:
    gate_version: str
    gate_status: str
    source_authority_gate_status: str | None
    source_authority_emergence_outcome: str | None
    middle_way_scope_outcome: str
    middle_way_scope_reason: str
    reviewed_probe_type: str | None
    conventional_authority_scope: str | None
    authority_scope: str | None
    authority_not_reified: bool
    authority_not_denied_when_conditions_hold: bool
    avoids_eternalism: bool
    avoids_nihilism: bool
    conditioned_local_authority_only: bool
    ultimate_non_reification_preserved: bool
    dependent_origination_trace_present: bool
    two_truths_boundary_preserved: bool
    local_limited_revocable: bool
    mass_gap_barrier_preserved: bool
    no_direct_execution_collapse: bool
    scope_blockers: list[str]
    scope_warnings: list[str]
    middle_way_scope_only: bool
    authority_scope_candidate_only: bool
    actual_probe_execution_authority: bool
    execution_requires_separate_gate: bool
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
        "actual_probe_execution_authority",
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


def evaluate_qi_middle_way_authority_scope(
    *,
    authority_emergence_packet: Mapping[str, Any],
    scope_context: Mapping[str, Any] | None = None,
) -> QiMiddleWayAuthorityScopeGate:
    authority_packet = _mapping(authority_emergence_packet)
    ctx = _mapping(scope_context)
    blockers: list[str] = []
    warnings: list[str] = []

    source_gate_status = str(authority_packet.get("gate_status")) if authority_packet.get("gate_status") else None
    source_outcome = str(authority_packet.get("authority_emergence_outcome")) if authority_packet.get("authority_emergence_outcome") else None
    probe_type = str(authority_packet.get("reviewed_probe_type")) if authority_packet.get("reviewed_probe_type") else None
    conventional_scope = str(authority_packet.get("conventional_authority_scope")) if authority_packet.get("conventional_authority_scope") else None
    authority_scope = str(ctx.get("authority_scope")) if ctx.get("authority_scope") else conventional_scope

    if source_gate_status != "QI_TWO_TRUTHS_AUTHORITY_EMERGENCE_GATE_READY":
        blockers.append("authority_emergence_gate_not_ready")
    if source_outcome != "AUTHORITY_GRANT_CANDIDATE":
        blockers.append("authority_emergence_not_grant_candidate")
    if authority_packet.get("authority_grant_candidate_only") is not True:
        blockers.append("authority_grant_candidate_only_not_true")
    if authority_packet.get("execution_requires_separate_gate") is not True:
        blockers.append("execution_requires_separate_gate_not_true")
    if authority_packet.get("local_limited_revocable") is not True:
        blockers.append("source_local_limited_revocable_not_true")
    if authority_packet.get("authority") != "none":
        blockers.append("source_authority_not_none")
    if not probe_type:
        blockers.append("reviewed_probe_type_missing")
    if not authority_scope:
        blockers.append("authority_scope_missing")
    _require_false("authority_emergence", authority_packet, blockers)

    required_true = [
        "authority_not_reified",
        "authority_not_denied_when_conditions_hold",
        "avoids_eternalism",
        "avoids_nihilism",
        "conditioned_local_authority_only",
        "ultimate_non_reification_preserved",
        "dependent_origination_trace_present",
        "two_truths_boundary_preserved",
        "local_limited_revocable",
        "mass_gap_barrier_preserved",
        "no_direct_execution_collapse",
    ]
    for key in required_true:
        if not _truthy(ctx, key):
            blockers.append(f"{key}_not_true")

    if ctx.get("eternalist_authority_claim") is True:
        blockers.append("eternalist_authority_claim")
    if ctx.get("nihilist_authority_denial") is True:
        blockers.append("nihilist_authority_denial")
    if ctx.get("authority_scope_unbounded") is True:
        blockers.append("authority_scope_unbounded")
    if ctx.get("authority_irrevocable") is True:
        blockers.append("authority_irrevocable")
    if ctx.get("direct_execution_requested") is True:
        blockers.append("direct_execution_requested")

    if conventional_scope != authority_scope:
        warnings.append("scope_context_differs_from_conventional_scope")

    ready = not blockers
    return QiMiddleWayAuthorityScopeGate(
        gate_version="kuuos_runtime_daemon_qi_middle_way_authority_scope_gate_v0_1",
        gate_status="QI_MIDDLE_WAY_AUTHORITY_SCOPE_GATE_READY" if ready else "QI_MIDDLE_WAY_AUTHORITY_SCOPE_GATE_BLOCKED",
        source_authority_gate_status=source_gate_status,
        source_authority_emergence_outcome=source_outcome,
        middle_way_scope_outcome="MIDDLE_WAY_AUTHORITY_SCOPE_READY" if ready else "MIDDLE_WAY_AUTHORITY_SCOPE_HOLD",
        middle_way_scope_reason=(
            "authority scope is conditioned, local, limited, revocable, and avoids both eternalism and nihilism"
            if ready
            else "authority scope failed middle-way constraints"
        ),
        reviewed_probe_type=probe_type if ready else None,
        conventional_authority_scope=conventional_scope if ready else None,
        authority_scope=authority_scope if ready else None,
        authority_not_reified=_truthy(ctx, "authority_not_reified"),
        authority_not_denied_when_conditions_hold=_truthy(ctx, "authority_not_denied_when_conditions_hold"),
        avoids_eternalism=_truthy(ctx, "avoids_eternalism"),
        avoids_nihilism=_truthy(ctx, "avoids_nihilism"),
        conditioned_local_authority_only=_truthy(ctx, "conditioned_local_authority_only"),
        ultimate_non_reification_preserved=_truthy(ctx, "ultimate_non_reification_preserved"),
        dependent_origination_trace_present=_truthy(ctx, "dependent_origination_trace_present"),
        two_truths_boundary_preserved=_truthy(ctx, "two_truths_boundary_preserved"),
        local_limited_revocable=_truthy(ctx, "local_limited_revocable"),
        mass_gap_barrier_preserved=_truthy(ctx, "mass_gap_barrier_preserved"),
        no_direct_execution_collapse=_truthy(ctx, "no_direct_execution_collapse"),
        scope_blockers=blockers,
        scope_warnings=warnings,
        middle_way_scope_only=True,
        authority_scope_candidate_only=True,
        actual_probe_execution_authority=False,
        execution_requires_separate_gate=True,
        scheduler_state_mutation_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        dry_run_execution_performed=False,
        next_tick_execution_performed=False,
        memory_write_performed=False,
        world_update_performed=False,
    )
