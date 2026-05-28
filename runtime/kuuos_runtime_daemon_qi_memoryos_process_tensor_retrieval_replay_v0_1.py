#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class QiMemoryOSProcessTensorRetrievalReplay:
    replay_version: str
    replay_status: str
    retrieved_entry_count: int
    replay_ready_entry_count: int
    dominant_probe_type: str | None
    replay_summary: str
    scheduler_reuse_hint: str
    probe_planner_reuse_hint: str
    process_tensor_trace_available: bool
    nonmarkov_trace_available: bool
    observation_debt_trace_available: bool
    recoverability_trace_available: bool
    safe_reentry_trace_available: bool
    lineage_available: bool
    retrieval_only: bool
    replay_surface_only: bool
    memory_read_performed: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    memory_delete_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    scheduler_state_mutation_performed: bool
    grants_memory_write_authority: bool
    grants_memory_overwrite_authority: bool
    grants_world_update_authority: bool
    grants_control_packet_authority: bool
    grants_scheduler_authority: bool
    grants_probe_execution_authority: bool
    replay_blockers: list[str]
    replay_warnings: list[str]
    authority: str = "memory_read_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _entries(value: Any) -> list[Mapping[str, Any]]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [item for item in value if isinstance(item, Mapping)]
    return []


def _truthy(payload: Mapping[str, Any], key: str) -> bool:
    return payload.get(key) is True


def _count_probe_types(entries: list[Mapping[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in entries:
        probe_type = str(entry.get("source_probe_type") or entry.get("probe_type") or "unknown_probe")
        counts[probe_type] = counts.get(probe_type, 0) + 1
    return counts


def build_qi_memoryos_process_tensor_retrieval_replay(
    *,
    memory_entries: Sequence[Mapping[str, Any]],
    replay_context: Mapping[str, Any] | None = None,
) -> QiMemoryOSProcessTensorRetrievalReplay:
    entries = _entries(memory_entries)
    ctx = _mapping(replay_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if not entries:
        blockers.append("memory_entries_missing")

    ready_entries: list[Mapping[str, Any]] = []
    for i, entry in enumerate(entries):
        if entry.get("writeback_status") != "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED":
            warnings.append(f"entry_{i}_writeback_status_not_performed")
            continue
        if entry.get("append_only") is not True:
            warnings.append(f"entry_{i}_append_only_not_true")
            continue
        if entry.get("memory_append_performed") is not True:
            warnings.append(f"entry_{i}_memory_append_not_true")
            continue
        ready_entries.append(entry)

    if not ready_entries:
        blockers.append("no_replay_ready_memory_entries")

    required_trace_keys = [
        "process_tensor_trace_preserved",
        "nonmarkov_trace_preserved",
        "observation_debt_trace_preserved",
        "recoverability_trace_preserved",
        "safe_reentry_trace_preserved",
        "lineage_preserved",
    ]
    trace_flags = {key: any(entry.get(key) is True for entry in ready_entries) for key in required_trace_keys}
    for key, value in trace_flags.items():
        if not value:
            blockers.append(f"{key}_not_available")

    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")
    if ctx.get("request_memory_overwrite") is True:
        blockers.append("request_memory_overwrite")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_scheduler_mutation") is True:
        blockers.append("request_scheduler_mutation")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")

    counts = _count_probe_types(ready_entries)
    dominant_probe_type = max(counts, key=counts.get) if counts else None
    retrieved_count = len(entries)
    ready_count = len(ready_entries)
    replay_summary = (
        f"retrieved {ready_count}/{retrieved_count} replay-ready Qi process-tensor MemoryOS entries"
        if ready_count
        else "no replay-ready Qi process-tensor MemoryOS entries"
    )
    scheduler_hint = (
        f"reuse_nonmarkov_history_for_{dominant_probe_type}" if dominant_probe_type else "hold_for_process_tensor_memory_gap"
    )
    planner_hint = (
        f"prioritize_probe_family_{dominant_probe_type}" if dominant_probe_type else "request_more_process_tensor_memory"
    )

    ready = not blockers
    return QiMemoryOSProcessTensorRetrievalReplay(
        replay_version="kuuos_runtime_daemon_qi_memoryos_process_tensor_retrieval_replay_v0_1",
        replay_status="QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY" if ready else "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_BLOCKED",
        retrieved_entry_count=retrieved_count,
        replay_ready_entry_count=ready_count,
        dominant_probe_type=dominant_probe_type if ready else None,
        replay_summary=replay_summary,
        scheduler_reuse_hint=scheduler_hint if ready else "hold_for_process_tensor_memory_gap",
        probe_planner_reuse_hint=planner_hint if ready else "request_more_process_tensor_memory",
        process_tensor_trace_available=trace_flags["process_tensor_trace_preserved"],
        nonmarkov_trace_available=trace_flags["nonmarkov_trace_preserved"],
        observation_debt_trace_available=trace_flags["observation_debt_trace_preserved"],
        recoverability_trace_available=trace_flags["recoverability_trace_preserved"],
        safe_reentry_trace_available=trace_flags["safe_reentry_trace_preserved"],
        lineage_available=trace_flags["lineage_preserved"],
        retrieval_only=True,
        replay_surface_only=True,
        memory_read_performed=True,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        memory_delete_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        scheduler_state_mutation_performed=False,
        grants_memory_write_authority=False,
        grants_memory_overwrite_authority=False,
        grants_world_update_authority=False,
        grants_control_packet_authority=False,
        grants_scheduler_authority=False,
        grants_probe_execution_authority=False,
        replay_blockers=blockers,
        replay_warnings=warnings,
    )
