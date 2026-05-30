#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import pathlib
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_qi_persistent_event_log_cursor_ledger_v0_1 import update_qi_persistent_event_log_cursor_ledger
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_persistent_event_log_cursor_ledger_v0_1 import update_qi_persistent_event_log_cursor_ledger


@dataclass(frozen=True)
class QiJsonlLedgerBackendAdapterResult:
    backend_version: str
    backend_status: str
    backend_kind: str
    event_log_path: str
    ledger_state_path: str
    event_line_appended: bool
    ledger_state_written: bool
    append_only_event_log: bool
    replay_cursor_monotone: bool
    idempotency_enforced: bool
    token_double_consume_blocked: bool
    event_log_size_after: int
    replay_cursor_after: int
    token_consumption_recorded: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    ledger_update_packet: dict[str, Any]
    backend_blockers: list[str]
    backend_warnings: list[str]
    authority: str = "jsonl_backend_append_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            entries.append({"_invalid_jsonl_line": line})
            continue
        entries.append(value if isinstance(value, dict) else {"_non_object_jsonl_line": value})
    return entries


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def apply_qi_jsonl_ledger_backend_adapter(
    *,
    tick_packet: Mapping[str, Any],
    event_log_path: str | pathlib.Path,
    ledger_state_path: str | pathlib.Path,
    ledger_context: Mapping[str, Any],
    token_event: Mapping[str, Any] | None = None,
) -> QiJsonlLedgerBackendAdapterResult:
    event_path = pathlib.Path(event_log_path)
    state_path = pathlib.Path(ledger_state_path)
    blockers: list[str] = []
    warnings: list[str] = []

    prior_state = _read_json(state_path)
    prior_events = _read_jsonl(event_path)
    if any("_invalid_jsonl_line" in item for item in prior_events):
        blockers.append("event_log_contains_invalid_jsonl")
    prior_state.setdefault("event_log", prior_events)
    prior_state.setdefault("replay_cursor", {"stream": "memoryos/qi_process_tensor/append_only", "position": len(prior_events)})
    prior_state.setdefault("token_ledger", {"consumed_token_ids": []})

    update = update_qi_persistent_event_log_cursor_ledger(
        tick_packet=tick_packet,
        prior_ledger=prior_state,
        ledger_context=ledger_context,
        token_event=token_event,
    ).to_dict()
    if update.get("ledger_status") != "QI_PERSISTENT_EVENT_LOG_CURSOR_LEDGER_UPDATED":
        blockers.append("ledger_update_not_ready")

    ready = not blockers
    if ready:
        next_ledger = update.get("next_ledger", {})
        event_log = next_ledger.get("event_log", []) if isinstance(next_ledger, dict) else []
        if event_log:
            _append_jsonl(event_path, event_log[-1])
        sidecar = dict(next_ledger)
        sidecar["event_log"] = []
        sidecar["event_log_path"] = str(event_path)
        _write_json(state_path, sidecar)

    return QiJsonlLedgerBackendAdapterResult(
        backend_version="kuuos_runtime_daemon_qi_jsonl_ledger_backend_adapter_v0_1",
        backend_status="QI_JSONL_LEDGER_BACKEND_ADAPTER_UPDATED" if ready else "QI_JSONL_LEDGER_BACKEND_ADAPTER_BLOCKED",
        backend_kind="jsonl_event_log_plus_json_sidecar",
        event_log_path=str(event_path),
        ledger_state_path=str(state_path),
        event_line_appended=ready,
        ledger_state_written=ready,
        append_only_event_log=True,
        replay_cursor_monotone=update.get("replay_cursor_monotone") is True,
        idempotency_enforced=True,
        token_double_consume_blocked=update.get("token_double_consume_blocked") is True,
        event_log_size_after=int(update.get("event_log_size_after", len(prior_events))) if ready else len(prior_events),
        replay_cursor_after=int(update.get("replay_cursor_after", 0)) if ready else int(prior_state.get("replay_cursor", {}).get("position", 0)),
        token_consumption_recorded=update.get("token_consumption_recorded") is True,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        ledger_update_packet=update,
        backend_blockers=blockers,
        backend_warnings=warnings,
    )
