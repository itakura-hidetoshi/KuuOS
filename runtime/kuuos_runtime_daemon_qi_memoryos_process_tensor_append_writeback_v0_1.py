#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiMemoryOSProcessTensorAppendWriteback:
    writeback_version: str
    writeback_status: str
    source_execution_status: str | None
    source_probe_type: str | None
    memory_entry_kind: str | None
    memory_entry_summary: str | None
    memoryos_target_stream: str
    process_tensor_trace_preserved: bool
    nonmarkov_trace_preserved: bool
    observation_debt_trace_preserved: bool
    recoverability_trace_preserved: bool
    safe_reentry_trace_preserved: bool
    lineage_preserved: bool
    append_only: bool
    memory_append_performed: bool
    memory_write_performed: bool
    memory_overwrite_performed: bool
    memory_delete_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    scheduler_state_mutation_performed: bool
    grants_memory_append_authority: bool
    grants_memory_overwrite_authority: bool
    grants_world_update_authority: bool
    grants_control_packet_authority: bool
    grants_scheduler_authority: bool
    grants_probe_execution_authority: bool
    writeback_blockers: list[str]
    writeback_warnings: list[str]
    authority: str = "memory_append_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _truthy(payload: Mapping[str, Any], key: str) -> bool:
    return payload.get(key) is True


def run_qi_memoryos_process_tensor_append_writeback(
    *,
    probe_result: Mapping[str, Any],
    writeback_context: Mapping[str, Any] | None = None,
) -> QiMemoryOSProcessTensorAppendWriteback:
    result = _mapping(probe_result)
    ctx = _mapping(writeback_context)
    blockers: list[str] = []
    warnings: list[str] = []

    source_status = str(result.get("execution_status")) if result.get("execution_status") else None
    probe_type = str(result.get("probe_type")) if result.get("probe_type") else None
    entry_kind = str(ctx.get("memory_entry_kind")) if ctx.get("memory_entry_kind") else "qi_process_tensor_probe_result_memory_entry"
    entry_summary = str(ctx.get("memory_entry_summary")) if ctx.get("memory_entry_summary") else str(result.get("probe_result_summary") or "process tensor probe result appended to MemoryOS")
    target_stream = str(ctx.get("memoryos_target_stream")) if ctx.get("memoryos_target_stream") else "memoryos/qi_process_tensor/append_only"

    if source_status != "QI_ONE_SHOT_PROBE_EXECUTION_PERFORMED":
        blockers.append("probe_result_not_performed")
    if result.get("probe_execution_performed") is not True:
        blockers.append("probe_execution_performed_not_true")
    if result.get("probe_result_artifact_only") is not True:
        blockers.append("probe_result_artifact_only_not_true")
    if result.get("one_shot_token_consumed") is not True:
        blockers.append("one_shot_token_consumed_not_true")
    if result.get("token_reuse_allowed") is not False:
        blockers.append("token_reuse_allowed_not_false")
    if not probe_type:
        blockers.append("source_probe_type_missing")

    for key in [
        "grants_probe_execution_authority",
        "grants_execution_authority",
        "grants_memory_overwrite_authority",
        "grants_world_update_authority",
        "grants_control_packet_authority",
        "grants_scheduler_authority",
        "memory_write_performed",
        "world_update_performed",
        "control_packet_mutation_performed",
        "scheduler_state_mutation_performed",
    ]:
        if result.get(key) is not False:
            blockers.append(f"source_{key}_not_false")

    required_context = [
        "append_only_required",
        "lineage_preserved",
        "process_tensor_trace_preserved",
        "nonmarkov_trace_preserved",
        "observation_debt_trace_preserved",
        "recoverability_trace_preserved",
        "safe_reentry_trace_preserved",
        "no_memory_overwrite",
        "no_world_update",
        "no_control_packet_mutation",
    ]
    for key in required_context:
        if not _truthy(ctx, key):
            blockers.append(f"{key}_not_true")

    if ctx.get("request_memory_overwrite") is True:
        blockers.append("request_memory_overwrite")
    if ctx.get("request_memory_delete") is True:
        blockers.append("request_memory_delete")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_control_packet_mutation") is True:
        blockers.append("request_control_packet_mutation")
    if ctx.get("request_scheduler_mutation") is True:
        blockers.append("request_scheduler_mutation")

    ready = not blockers
    return QiMemoryOSProcessTensorAppendWriteback(
        writeback_version="kuuos_runtime_daemon_qi_memoryos_process_tensor_append_writeback_v0_1",
        writeback_status="QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED" if ready else "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_BLOCKED",
        source_execution_status=source_status,
        source_probe_type=probe_type if ready else None,
        memory_entry_kind=entry_kind if ready else None,
        memory_entry_summary=entry_summary if ready else None,
        memoryos_target_stream=target_stream,
        process_tensor_trace_preserved=_truthy(ctx, "process_tensor_trace_preserved"),
        nonmarkov_trace_preserved=_truthy(ctx, "nonmarkov_trace_preserved"),
        observation_debt_trace_preserved=_truthy(ctx, "observation_debt_trace_preserved"),
        recoverability_trace_preserved=_truthy(ctx, "recoverability_trace_preserved"),
        safe_reentry_trace_preserved=_truthy(ctx, "safe_reentry_trace_preserved"),
        lineage_preserved=_truthy(ctx, "lineage_preserved"),
        append_only=True,
        memory_append_performed=ready,
        memory_write_performed=ready,
        memory_overwrite_performed=False,
        memory_delete_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        scheduler_state_mutation_performed=False,
        grants_memory_append_authority=False,
        grants_memory_overwrite_authority=False,
        grants_world_update_authority=False,
        grants_control_packet_authority=False,
        grants_scheduler_authority=False,
        grants_probe_execution_authority=False,
        writeback_blockers=blockers,
        writeback_warnings=warnings,
    )
