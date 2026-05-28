#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiOneShotProbeExecutionResult:
    executor_version: str
    execution_status: str
    source_grant_status: str | None
    source_grant_outcome: str | None
    probe_type: str | None
    authority_scope: str | None
    authority_token_kind: str | None
    probe_result_kind: str | None
    probe_result_summary: str | None
    probe_result_artifact_only: bool
    one_shot_token_consumed: bool
    token_reuse_allowed: bool
    single_probe_only: bool
    rollback_required: bool
    reentry_window_bound: bool
    execution_blockers: list[str]
    execution_warnings: list[str]
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
    memory_write_allowed: bool
    world_update_allowed: bool
    control_packet_mutation_allowed: bool
    authority: str = "none"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _truthy(payload: Mapping[str, Any], key: str) -> bool:
    return payload.get(key) is True


def run_qi_one_shot_probe_executor(
    *,
    grant_packet: Mapping[str, Any],
    probe_payload: Mapping[str, Any] | None = None,
) -> QiOneShotProbeExecutionResult:
    grant = _mapping(grant_packet)
    payload = _mapping(probe_payload)
    blockers: list[str] = []
    warnings: list[str] = []

    source_status = str(grant.get("gate_status")) if grant.get("gate_status") else None
    source_outcome = str(grant.get("grant_outcome")) if grant.get("grant_outcome") else None
    probe_type = str(grant.get("authorized_probe_type")) if grant.get("authorized_probe_type") else None
    authority_scope = str(grant.get("authority_scope")) if grant.get("authority_scope") else None
    token_kind = str(grant.get("authority_token_kind")) if grant.get("authority_token_kind") else None

    if source_status != "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_READY":
        blockers.append("grant_gate_not_ready")
    if source_outcome != "LIMITED_ONE_SHOT_PROBE_EXECUTION_AUTHORITY_GRANTED":
        blockers.append("grant_outcome_not_granted")
    if grant.get("grants_probe_execution_authority") is not True:
        blockers.append("grant_probe_execution_authority_not_true")
    if grant.get("grants_execution_authority") is not True:
        blockers.append("grant_execution_authority_not_true")
    if grant.get("one_shot") is not True:
        blockers.append("grant_one_shot_not_true")
    if grant.get("single_probe_only") is not True:
        blockers.append("grant_single_probe_only_not_true")
    if grant.get("rollback_required") is not True:
        blockers.append("grant_rollback_required_not_true")
    if grant.get("reentry_window_bound") is not True:
        blockers.append("grant_reentry_window_bound_not_true")
    if grant.get("authority_expires_after_use") is not True:
        blockers.append("grant_authority_expires_after_use_not_true")
    if grant.get("authority_revocable") is not True:
        blockers.append("grant_authority_revocable_not_true")
    if not probe_type:
        blockers.append("authorized_probe_type_missing")
    if token_kind != "single_use_probe_execution_authority":
        blockers.append("authority_token_kind_not_single_use")

    for key in [
        "grants_memory_overwrite_authority",
        "grants_world_update_authority",
        "grants_control_packet_authority",
        "grants_scheduler_authority",
        "memory_write_allowed",
        "world_update_allowed",
        "control_packet_mutation_allowed",
        "probe_execution_performed",
        "memory_write_performed",
        "world_update_performed",
        "control_packet_mutation_performed",
    ]:
        if grant.get(key) is not False:
            blockers.append(f"grant_{key}_not_false")

    if _truthy(payload, "token_already_consumed"):
        blockers.append("token_already_consumed")
    if _truthy(payload, "request_multi_probe"):
        blockers.append("request_multi_probe")
    if _truthy(payload, "request_memory_write"):
        blockers.append("request_memory_write")
    if _truthy(payload, "request_world_update"):
        blockers.append("request_world_update")
    if _truthy(payload, "request_control_packet_mutation"):
        blockers.append("request_control_packet_mutation")
    if _truthy(payload, "request_scheduler_mutation"):
        blockers.append("request_scheduler_mutation")

    result_kind = str(payload.get("probe_result_kind")) if payload.get("probe_result_kind") else "qi_one_shot_probe_observation"
    result_summary = str(payload.get("probe_result_summary")) if payload.get("probe_result_summary") else "one-shot probe executed and returned artifact-only observation"

    ready = not blockers
    return QiOneShotProbeExecutionResult(
        executor_version="kuuos_runtime_daemon_qi_one_shot_probe_executor_v0_1",
        execution_status="QI_ONE_SHOT_PROBE_EXECUTION_PERFORMED" if ready else "QI_ONE_SHOT_PROBE_EXECUTION_BLOCKED",
        source_grant_status=source_status,
        source_grant_outcome=source_outcome,
        probe_type=probe_type if ready else None,
        authority_scope=authority_scope if ready else None,
        authority_token_kind=token_kind if ready else None,
        probe_result_kind=result_kind if ready else None,
        probe_result_summary=result_summary if ready else None,
        probe_result_artifact_only=True,
        one_shot_token_consumed=ready,
        token_reuse_allowed=False,
        single_probe_only=True,
        rollback_required=True,
        reentry_window_bound=True,
        execution_blockers=blockers,
        execution_warnings=warnings,
        grants_probe_execution_authority=False,
        grants_execution_authority=False,
        grants_dry_run_execution_authority=False,
        grants_next_tick_execution_authority=False,
        grants_scheduler_authority=False,
        grants_control_packet_authority=False,
        grants_memory_overwrite_authority=False,
        grants_world_update_authority=False,
        probe_execution_performed=ready,
        dry_run_execution_performed=False,
        next_tick_execution_performed=False,
        scheduler_state_mutation_performed=False,
        control_packet_mutation_performed=False,
        memory_write_performed=False,
        world_update_performed=False,
        memory_write_allowed=False,
        world_update_allowed=False,
        control_packet_mutation_allowed=False,
    )
