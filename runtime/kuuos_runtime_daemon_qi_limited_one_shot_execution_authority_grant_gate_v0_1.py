#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiLimitedOneShotExecutionAuthorityGrantGate:
    gate_version: str
    gate_status: str
    source_scope_gate_status: str | None
    source_scope_outcome: str | None
    grant_outcome: str
    grant_reason: str
    authorized_probe_type: str | None
    authority_scope: str | None
    authority_token_kind: str | None
    one_shot: bool
    single_probe_only: bool
    rollback_required: bool
    reentry_window_bound: bool
    memory_write_allowed: bool
    world_update_allowed: bool
    control_packet_mutation_allowed: bool
    authority_expires_after_use: bool
    authority_revocable: bool
    grant_blockers: list[str]
    grant_warnings: list[str]
    grants_probe_execution_authority: bool
    grants_execution_authority: bool
    grants_dry_run_execution_authority: bool
    grants_next_tick_execution_authority: bool
    grants_scheduler_authority: bool
    grants_control_packet_authority: bool
    grants_memory_overwrite_authority: bool
    grants_world_update_authority: bool
    probe_execution_performed: bool
    dry_run_execution_performed: bool
    next_tick_execution_performed: bool
    scheduler_state_mutation_performed: bool
    control_packet_mutation_performed: bool
    memory_write_performed: bool
    world_update_performed: bool
    authority: str = "probe_execution_authority_grant"

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
        "probe_execution_performed",
        "dry_run_execution_performed",
        "next_tick_execution_performed",
        "scheduler_state_mutation_performed",
        "control_packet_mutation_performed",
        "memory_write_performed",
        "world_update_performed",
    ]:
        if payload.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def evaluate_qi_limited_one_shot_execution_authority_grant(
    *,
    middle_way_scope_packet: Mapping[str, Any],
    grant_context: Mapping[str, Any] | None = None,
) -> QiLimitedOneShotExecutionAuthorityGrantGate:
    scope = _mapping(middle_way_scope_packet)
    ctx = _mapping(grant_context)
    blockers: list[str] = []
    warnings: list[str] = []

    source_status = str(scope.get("gate_status")) if scope.get("gate_status") else None
    source_outcome = str(scope.get("middle_way_scope_outcome")) if scope.get("middle_way_scope_outcome") else None
    probe_type = str(scope.get("reviewed_probe_type")) if scope.get("reviewed_probe_type") else None
    authority_scope = str(scope.get("authority_scope")) if scope.get("authority_scope") else None

    if source_status != "QI_MIDDLE_WAY_AUTHORITY_SCOPE_GATE_READY":
        blockers.append("middle_way_scope_gate_not_ready")
    if source_outcome != "MIDDLE_WAY_AUTHORITY_SCOPE_READY":
        blockers.append("middle_way_scope_not_ready")
    if scope.get("middle_way_scope_only") is not True:
        blockers.append("middle_way_scope_only_not_true")
    if scope.get("authority_scope_candidate_only") is not True:
        blockers.append("authority_scope_candidate_only_not_true")
    if scope.get("execution_requires_separate_gate") is not True:
        blockers.append("execution_requires_separate_gate_not_true")
    if scope.get("authority") != "none":
        blockers.append("source_authority_not_none")
    if not probe_type:
        blockers.append("reviewed_probe_type_missing")
    if not authority_scope:
        blockers.append("authority_scope_missing")
    _require_false("middle_way_scope", scope, blockers)

    required_true = [
        "operator_approved_one_shot",
        "governor_approved_one_shot",
        "single_probe_only",
        "rollback_path_verified",
        "safe_reentry_window_bound",
        "memory_write_forbidden",
        "world_update_forbidden",
        "control_packet_mutation_forbidden",
        "authority_expires_after_use",
        "authority_revocable",
    ]
    for key in required_true:
        if not _truthy(ctx, key):
            blockers.append(f"{key}_not_true")

    if ctx.get("request_multi_probe") is True:
        blockers.append("request_multi_probe")
    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_control_packet_mutation") is True:
        blockers.append("request_control_packet_mutation")
    if ctx.get("request_persistent_authority") is True:
        blockers.append("request_persistent_authority")
    if ctx.get("rollback_unavailable") is True:
        blockers.append("rollback_unavailable")

    token_kind = "single_use_probe_execution_authority" if not blockers else None
    ready = not blockers
    return QiLimitedOneShotExecutionAuthorityGrantGate(
        gate_version="kuuos_runtime_daemon_qi_limited_one_shot_execution_authority_grant_gate_v0_1",
        gate_status="QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_READY" if ready else "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_BLOCKED",
        source_scope_gate_status=source_status,
        source_scope_outcome=source_outcome,
        grant_outcome="LIMITED_ONE_SHOT_PROBE_EXECUTION_AUTHORITY_GRANTED" if ready else "LIMITED_ONE_SHOT_PROBE_EXECUTION_AUTHORITY_HOLD",
        grant_reason=(
            "single-use probe execution authority is granted as local limited revocable authority; no execution is performed by this gate"
            if ready
            else "limited one-shot execution authority constraints are not satisfied"
        ),
        authorized_probe_type=probe_type if ready else None,
        authority_scope=authority_scope if ready else None,
        authority_token_kind=token_kind,
        one_shot=True,
        single_probe_only=True,
        rollback_required=True,
        reentry_window_bound=True,
        memory_write_allowed=False,
        world_update_allowed=False,
        control_packet_mutation_allowed=False,
        authority_expires_after_use=True,
        authority_revocable=True,
        grant_blockers=blockers,
        grant_warnings=warnings,
        grants_probe_execution_authority=ready,
        grants_execution_authority=ready,
        grants_dry_run_execution_authority=False,
        grants_next_tick_execution_authority=False,
        grants_scheduler_authority=False,
        grants_control_packet_authority=False,
        grants_memory_overwrite_authority=False,
        grants_world_update_authority=False,
        probe_execution_performed=False,
        dry_run_execution_performed=False,
        next_tick_execution_performed=False,
        scheduler_state_mutation_performed=False,
        control_packet_mutation_performed=False,
        memory_write_performed=False,
        world_update_performed=False,
    )
