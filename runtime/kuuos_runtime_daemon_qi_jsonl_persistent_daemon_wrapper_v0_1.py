#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import pathlib
from typing import Any, Mapping, Sequence

try:
    from runtime.kuuos_runtime_daemon_qi_persistent_process_tensor_daemon_v0_1 import run_qi_persistent_process_tensor_daemon_tick
    from runtime.kuuos_runtime_daemon_qi_jsonl_ledger_backend_adapter_v0_1 import apply_qi_jsonl_ledger_backend_adapter
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_persistent_process_tensor_daemon_v0_1 import run_qi_persistent_process_tensor_daemon_tick
    from kuuos_runtime_daemon_qi_jsonl_ledger_backend_adapter_v0_1 import apply_qi_jsonl_ledger_backend_adapter


@dataclass(frozen=True)
class QiJsonlPersistentDaemonWrapperResult:
    wrapper_version: str
    wrapper_status: str
    backend_kind: str
    requested_tick_count: int
    completed_tick_count: int
    event_log_path: str
    ledger_state_path: str
    repeated_bounded_ticks_performed: bool
    heartbeat_count: int
    jsonl_event_lines_appended: int
    replay_cursor_after: int
    token_ledger_checked: bool
    idempotency_enforced: bool
    duplicate_tick_blocked: bool
    token_double_consume_blocked: bool
    memory_read_performed: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    tick_packets: list[dict[str, Any]]
    backend_packets: list[dict[str, Any]]
    wrapper_blockers: list[str]
    wrapper_warnings: list[str]
    authority: str = "jsonl_persistent_wrapper_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _entries(value: Any) -> list[Mapping[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, Mapping)]
    if isinstance(value, Mapping) and isinstance(value.get("entries"), list):
        return [item for item in value["entries"] if isinstance(item, Mapping)]
    if isinstance(value, Mapping):
        return [value]
    return []


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
        "memory_write_performed",
        "memory_append_performed",
        "memory_overwrite_performed",
        "world_update_performed",
        "control_packet_mutation_performed",
        "probe_execution_performed",
        "grants_probe_execution_authority",
        "grants_world_update_authority",
        "grants_memory_overwrite_authority",
    ]:
        if packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def run_qi_jsonl_persistent_daemon_wrapper(
    *,
    memory_entries: Sequence[Mapping[str, Any]] | Mapping[str, Any],
    scheduler_state: Mapping[str, Any],
    scheduler_proposal: Mapping[str, Any],
    process_tensor_metrics: Mapping[str, Any],
    event_log_path: str | pathlib.Path,
    ledger_state_path: str | pathlib.Path,
    start_tick: int,
    tick_count: int,
    wrapper_context: Mapping[str, Any] | None = None,
) -> QiJsonlPersistentDaemonWrapperResult:
    ctx = _mapping(wrapper_context)
    blockers: list[str] = []
    warnings: list[str] = []
    if ctx.get("allow_repeated_bounded_ticks") is not True:
        blockers.append("allow_repeated_bounded_ticks_not_true")
    if ctx.get("jsonl_backend_required") is not True:
        blockers.append("jsonl_backend_required_not_true")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")
    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_control_packet_mutation") is True:
        blockers.append("request_control_packet_mutation")
    if tick_count <= 0:
        blockers.append("tick_count_not_positive")
    if tick_count > int(ctx.get("max_tick_count", tick_count)):
        blockers.append("tick_count_exceeds_max_tick_count")

    event_path = pathlib.Path(event_log_path)
    state_path = pathlib.Path(ledger_state_path)
    tick_packets: list[dict[str, Any]] = []
    backend_packets: list[dict[str, Any]] = []
    duplicate_tick_blocked = False
    token_double_consume_blocked = False

    entries = _entries(memory_entries)
    for i in range(max(tick_count, 0)):
        current_tick = start_tick + i
        tick_id = str(ctx.get("tick_id_prefix", "qi-jsonl-tick")) + f"-{current_tick}"
        tick = run_qi_persistent_process_tensor_daemon_tick(
            memory_entries=entries,
            scheduler_state=scheduler_state,
            scheduler_proposal=scheduler_proposal,
            process_tensor_metrics=process_tensor_metrics,
            current_tick=current_tick,
            runtime_context={
                "tick_id": tick_id,
                "allow_persistent_tick": True,
                "bounded_tick": True,
                "heartbeat_required": True,
                "request_probe_execution": False,
                "request_memory_write": False,
                "request_world_update": False,
                "request_control_packet_mutation": False,
            },
        ).to_dict()
        tick_packets.append(tick)
        if tick.get("daemon_status") != "QI_PERSISTENT_PROCESS_TENSOR_DAEMON_TICK_READY":
            blockers.append(f"tick_{i}_not_ready")
            break
        _require_false(f"tick_{i}", tick, blockers)

        token_id = f"tok-{tick_id}"
        backend = apply_qi_jsonl_ledger_backend_adapter(
            tick_packet=tick,
            event_log_path=event_path,
            ledger_state_path=state_path,
            ledger_context={
                "event_id": f"evt-{tick_id}",
                "idempotency_key": f"idem-{tick_id}",
                "append_only_required": True,
                "idempotency_required": True,
                "replay_cursor_required": True,
                "token_ledger_required": True,
                "replay_cursor_stream": str(ctx.get("replay_cursor_stream", "memoryos/qi_process_tensor/append_only")),
                "replay_cursor_advance_by": int(tick.get("memory_entry_count", 0)),
                "request_memory_overwrite": False,
                "request_world_update": False,
                "request_probe_execution": False,
            },
            token_event={
                "token_event_kind": "one_shot_token_consumed",
                "token_id": token_id,
            },
        ).to_dict()
        backend_packets.append(backend)
        if backend.get("backend_status") != "QI_JSONL_LEDGER_BACKEND_ADAPTER_UPDATED":
            blockers.append(f"backend_{i}_not_updated")
            if backend.get("token_double_consume_blocked") is True:
                token_double_consume_blocked = True
            update = _mapping(backend.get("ledger_update_packet"))
            if "idempotency_key_already_seen" in update.get("ledger_blockers", []):
                duplicate_tick_blocked = True
            break
        _require_false(f"backend_{i}", backend, blockers)

    completed = len([p for p in backend_packets if p.get("backend_status") == "QI_JSONL_LEDGER_BACKEND_ADAPTER_UPDATED"])
    ready = not blockers and completed == tick_count
    if backend_packets:
        last_backend = backend_packets[-1]
        replay_cursor_after = int(last_backend.get("replay_cursor_after", 0))
    else:
        replay_cursor_after = 0
    return QiJsonlPersistentDaemonWrapperResult(
        wrapper_version="kuuos_runtime_daemon_qi_jsonl_persistent_daemon_wrapper_v0_1",
        wrapper_status="QI_JSONL_PERSISTENT_DAEMON_WRAPPER_COMPLETED" if ready else "QI_JSONL_PERSISTENT_DAEMON_WRAPPER_BLOCKED",
        backend_kind="jsonl_event_log_plus_json_sidecar",
        requested_tick_count=tick_count,
        completed_tick_count=completed,
        event_log_path=str(event_path),
        ledger_state_path=str(state_path),
        repeated_bounded_ticks_performed=ready,
        heartbeat_count=len([p for p in tick_packets if p.get("heartbeat_emitted") is True]),
        jsonl_event_lines_appended=completed,
        replay_cursor_after=replay_cursor_after,
        token_ledger_checked=True,
        idempotency_enforced=True,
        duplicate_tick_blocked=duplicate_tick_blocked,
        token_double_consume_blocked=token_double_consume_blocked,
        memory_read_performed=bool(tick_packets),
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        tick_packets=tick_packets,
        backend_packets=backend_packets,
        wrapper_blockers=blockers,
        wrapper_warnings=warnings,
    )
