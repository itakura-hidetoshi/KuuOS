#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class QiPersistentEventLogCursorLedgerUpdate:
    ledger_version: str
    ledger_status: str
    event_id: str | None
    idempotency_key: str | None
    tick_id: str | None
    event_append_performed: bool
    append_only: bool
    event_log_size_before: int
    event_log_size_after: int
    replay_cursor_stream: str
    replay_cursor_before: int
    replay_cursor_after: int
    replay_cursor_advanced: bool
    replay_cursor_monotone: bool
    token_ledger_checked: bool
    token_consumption_recorded: bool
    token_id: str | None
    token_double_consume_blocked: bool
    process_tensor_pressure: str | None
    dominant_probe_type: str | None
    scheduler_update_scope: str | None
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
    next_ledger: dict[str, Any]
    ledger_blockers: list[str]
    ledger_warnings: list[str]
    authority: str = "persistent_ledger_append_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)) else []


def _int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


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


def update_qi_persistent_event_log_cursor_ledger(
    *,
    tick_packet: Mapping[str, Any],
    prior_ledger: Mapping[str, Any] | None = None,
    ledger_context: Mapping[str, Any] | None = None,
    token_event: Mapping[str, Any] | None = None,
) -> QiPersistentEventLogCursorLedgerUpdate:
    tick = _mapping(tick_packet)
    prior = dict(_mapping(prior_ledger))
    ctx = _mapping(ledger_context)
    token = _mapping(token_event)
    blockers: list[str] = []
    warnings: list[str] = []

    if tick.get("daemon_status") != "QI_PERSISTENT_PROCESS_TENSOR_DAEMON_TICK_READY":
        blockers.append("tick_not_ready")
    if tick.get("heartbeat_emitted") is not True:
        blockers.append("heartbeat_not_emitted")
    if tick.get("closed_loop_tick_performed") is not True:
        blockers.append("closed_loop_tick_not_performed")
    if tick.get("scheduler_update_scope") != "replay_hint_only":
        blockers.append("scheduler_update_scope_not_replay_hint_only")
    _require_false("tick", tick, blockers)

    if ctx.get("append_only_required") is not True:
        blockers.append("append_only_required_not_true")
    if ctx.get("idempotency_required") is not True:
        blockers.append("idempotency_required_not_true")
    if ctx.get("replay_cursor_required") is not True:
        blockers.append("replay_cursor_required_not_true")
    if ctx.get("token_ledger_required") is not True:
        blockers.append("token_ledger_required_not_true")
    if ctx.get("request_memory_overwrite") is True:
        blockers.append("request_memory_overwrite")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")

    tick_id = str(tick.get("tick_id") or "")
    event_id = str(ctx.get("event_id") or f"evt-{tick_id}") if tick_id else None
    idempotency_key = str(ctx.get("idempotency_key") or f"idem-{tick_id}") if tick_id else None
    if not tick_id:
        blockers.append("tick_id_missing")
    if not event_id:
        blockers.append("event_id_missing")
    if not idempotency_key:
        blockers.append("idempotency_key_missing")

    event_log = _list(prior.get("event_log"))
    seen_keys = {str(item.get("idempotency_key")) for item in event_log if isinstance(item, Mapping) and item.get("idempotency_key")}
    seen_events = {str(item.get("event_id")) for item in event_log if isinstance(item, Mapping) and item.get("event_id")}
    if idempotency_key in seen_keys:
        blockers.append("idempotency_key_already_seen")
    if event_id in seen_events:
        blockers.append("event_id_already_seen")

    cursor = dict(_mapping(prior.get("replay_cursor")))
    stream = str(ctx.get("replay_cursor_stream") or cursor.get("stream") or "memoryos/qi_process_tensor/append_only")
    before = _int(cursor.get("position"), 0)
    advance_by = _int(ctx.get("replay_cursor_advance_by"), _int(tick.get("memory_entry_count"), 0))
    if advance_by < 0:
        blockers.append("replay_cursor_advance_negative")
    after = before + max(advance_by, 0)
    if after < before:
        blockers.append("replay_cursor_regressed")

    token_ledger = dict(_mapping(prior.get("token_ledger")))
    consumed_tokens = {str(x) for x in _list(token_ledger.get("consumed_token_ids"))}
    token_id = str(token.get("token_id")) if token.get("token_id") else None
    token_consumption_recorded = False
    token_double_consume_blocked = False
    if token:
        if token.get("token_event_kind") != "one_shot_token_consumed":
            blockers.append("token_event_kind_not_consumed")
        if not token_id:
            blockers.append("token_id_missing")
        elif token_id in consumed_tokens:
            blockers.append("token_already_consumed")
            token_double_consume_blocked = True
        else:
            token_consumption_recorded = True

    ready = not blockers
    next_event_log = list(event_log)
    if ready:
        next_event_log.append({
            "event_id": event_id,
            "idempotency_key": idempotency_key,
            "tick_id": tick_id,
            "event_kind": "qi_persistent_process_tensor_tick",
            "process_tensor_pressure": tick.get("process_tensor_pressure"),
            "dominant_probe_type": tick.get("dominant_probe_type"),
            "scheduler_update_scope": tick.get("scheduler_update_scope"),
            "memory_entry_count": tick.get("memory_entry_count"),
        })
    next_consumed = sorted(consumed_tokens | ({token_id} if ready and token_consumption_recorded and token_id else set()))
    next_ledger = {
        "ledger_version": "qi_persistent_event_log_cursor_ledger_v0_1",
        "event_log": next_event_log,
        "replay_cursor": {
            "stream": stream,
            "position": after if ready else before,
            "last_tick_id": tick_id if ready else cursor.get("last_tick_id"),
            "last_event_id": event_id if ready else cursor.get("last_event_id"),
        },
        "token_ledger": {
            **token_ledger,
            "consumed_token_ids": next_consumed,
        },
    }
    return QiPersistentEventLogCursorLedgerUpdate(
        ledger_version="kuuos_runtime_daemon_qi_persistent_event_log_cursor_ledger_v0_1",
        ledger_status="QI_PERSISTENT_EVENT_LOG_CURSOR_LEDGER_UPDATED" if ready else "QI_PERSISTENT_EVENT_LOG_CURSOR_LEDGER_BLOCKED",
        event_id=event_id if ready else None,
        idempotency_key=idempotency_key if ready else None,
        tick_id=tick_id if ready else None,
        event_append_performed=ready,
        append_only=True,
        event_log_size_before=len(event_log),
        event_log_size_after=len(next_event_log),
        replay_cursor_stream=stream,
        replay_cursor_before=before,
        replay_cursor_after=after if ready else before,
        replay_cursor_advanced=ready and after > before,
        replay_cursor_monotone=after >= before,
        token_ledger_checked=True,
        token_consumption_recorded=ready and token_consumption_recorded,
        token_id=token_id if ready and token_id else None,
        token_double_consume_blocked=token_double_consume_blocked,
        process_tensor_pressure=str(tick.get("process_tensor_pressure")) if tick.get("process_tensor_pressure") else None,
        dominant_probe_type=str(tick.get("dominant_probe_type")) if tick.get("dominant_probe_type") else None,
        scheduler_update_scope=str(tick.get("scheduler_update_scope")) if tick.get("scheduler_update_scope") else None,
        memory_read_performed=tick.get("memory_read_performed") is True,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        next_ledger=next_ledger if ready else prior,
        ledger_blockers=blockers,
        ledger_warnings=warnings,
    )
