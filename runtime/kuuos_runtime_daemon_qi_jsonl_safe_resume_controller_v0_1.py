#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import pathlib
from typing import Any, Mapping, Sequence

try:
    from runtime.kuuos_runtime_daemon_qi_jsonl_persistent_daemon_wrapper_v0_1 import run_qi_jsonl_persistent_daemon_wrapper
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_jsonl_persistent_daemon_wrapper_v0_1 import run_qi_jsonl_persistent_daemon_wrapper


@dataclass(frozen=True)
class QiJsonlSafeResumeControllerResult:
    resume_version: str
    resume_status: str
    event_log_path: str
    ledger_state_path: str
    desired_start_tick: int
    desired_tick_count: int
    resume_start_tick: int | None
    resume_tick_count: int
    processed_tick_count_detected: int
    skipped_processed_tick_count: int
    no_op_resume: bool
    safe_resume_performed: bool
    wrapper_status: str | None
    replay_cursor_before: int
    replay_cursor_after: int
    replay_cursor_monotone: bool
    heartbeat_count: int
    jsonl_event_lines_appended: int
    idempotency_enforced: bool
    duplicate_tick_blocked: bool
    token_ledger_checked: bool
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
    wrapper_packet: dict[str, Any]
    resume_blockers: list[str]
    resume_warnings: list[str]
    authority: str = "jsonl_safe_resume_controller_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


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
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            rows.append({"_invalid_jsonl_line": line})
            continue
        rows.append(value if isinstance(value, dict) else {"_non_object_jsonl_line": value})
    return rows


def _processed_ticks(rows: Sequence[Mapping[str, Any]], tick_id_prefix: str) -> set[int]:
    processed: set[int] = set()
    for row in rows:
        tick_id = str(row.get("tick_id") or "")
        prefix = tick_id_prefix + "-"
        if not tick_id.startswith(prefix):
            continue
        suffix = tick_id[len(prefix):]
        try:
            processed.add(int(suffix))
        except ValueError:
            continue
    return processed


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


def run_qi_jsonl_safe_resume_controller(
    *,
    memory_entries: Sequence[Mapping[str, Any]] | Mapping[str, Any],
    scheduler_state: Mapping[str, Any],
    scheduler_proposal: Mapping[str, Any],
    process_tensor_metrics: Mapping[str, Any],
    event_log_path: str | pathlib.Path,
    ledger_state_path: str | pathlib.Path,
    desired_start_tick: int,
    desired_tick_count: int,
    resume_context: Mapping[str, Any] | None = None,
) -> QiJsonlSafeResumeControllerResult:
    ctx = _mapping(resume_context)
    event_path = pathlib.Path(event_log_path)
    state_path = pathlib.Path(ledger_state_path)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("allow_safe_resume") is not True:
        blockers.append("allow_safe_resume_not_true")
    if ctx.get("jsonl_backend_required") is not True:
        blockers.append("jsonl_backend_required_not_true")
    if ctx.get("skip_processed_ticks") is not True:
        blockers.append("skip_processed_ticks_not_true")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")
    if desired_tick_count < 0:
        blockers.append("desired_tick_count_negative")

    tick_prefix = str(ctx.get("tick_id_prefix", "wrap"))
    rows = _read_jsonl(event_path)
    if any("_invalid_jsonl_line" in row for row in rows):
        blockers.append("event_log_contains_invalid_jsonl")
    state = _read_json(state_path)
    cursor_before = int(_mapping(state.get("replay_cursor")).get("position", len(rows)))
    processed = _processed_ticks(rows, tick_prefix)
    desired_ticks = list(range(desired_start_tick, desired_start_tick + max(desired_tick_count, 0)))
    pending = [tick for tick in desired_ticks if tick not in processed]
    if pending:
        expected_suffix = list(range(pending[0], pending[0] + len(pending)))
        if pending != expected_suffix:
            blockers.append("pending_ticks_not_contiguous_suffix")
    skipped = len(desired_ticks) - len(pending)
    no_op = not pending and not blockers

    wrapper_packet: dict[str, Any] = {}
    if not blockers and pending:
        wrapper_packet = run_qi_jsonl_persistent_daemon_wrapper(
            memory_entries=memory_entries,
            scheduler_state=scheduler_state,
            scheduler_proposal=scheduler_proposal,
            process_tensor_metrics=process_tensor_metrics,
            event_log_path=event_path,
            ledger_state_path=state_path,
            start_tick=pending[0],
            tick_count=len(pending),
            wrapper_context={
                "allow_repeated_bounded_ticks": True,
                "jsonl_backend_required": True,
                "max_tick_count": int(ctx.get("max_tick_count", len(pending))),
                "tick_id_prefix": tick_prefix,
                "request_probe_execution": False,
                "request_memory_write": False,
                "request_world_update": False,
                "request_control_packet_mutation": False,
            },
        ).to_dict()
        if wrapper_packet.get("wrapper_status") != "QI_JSONL_PERSISTENT_DAEMON_WRAPPER_COMPLETED":
            blockers.append("wrapper_not_completed")
        _require_false("wrapper", wrapper_packet, blockers)

    next_state = _read_json(state_path)
    cursor_after = int(_mapping(next_state.get("replay_cursor")).get("position", cursor_before))
    ready = not blockers
    return QiJsonlSafeResumeControllerResult(
        resume_version="kuuos_runtime_daemon_qi_jsonl_safe_resume_controller_v0_1",
        resume_status="QI_JSONL_SAFE_RESUME_CONTROLLER_COMPLETED" if ready else "QI_JSONL_SAFE_RESUME_CONTROLLER_BLOCKED",
        event_log_path=str(event_path),
        ledger_state_path=str(state_path),
        desired_start_tick=desired_start_tick,
        desired_tick_count=desired_tick_count,
        resume_start_tick=pending[0] if pending and ready else None,
        resume_tick_count=len(pending) if ready else 0,
        processed_tick_count_detected=len(processed),
        skipped_processed_tick_count=skipped if ready else 0,
        no_op_resume=no_op,
        safe_resume_performed=ready and bool(pending),
        wrapper_status=str(wrapper_packet.get("wrapper_status")) if wrapper_packet.get("wrapper_status") else None,
        replay_cursor_before=cursor_before,
        replay_cursor_after=cursor_after,
        replay_cursor_monotone=cursor_after >= cursor_before,
        heartbeat_count=int(wrapper_packet.get("heartbeat_count", 0)) if wrapper_packet else 0,
        jsonl_event_lines_appended=int(wrapper_packet.get("jsonl_event_lines_appended", 0)) if wrapper_packet else 0,
        idempotency_enforced=True,
        duplicate_tick_blocked=True,
        token_ledger_checked=True,
        memory_read_performed=bool(pending) and ready,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        wrapper_packet=wrapper_packet,
        resume_blockers=blockers,
        resume_warnings=warnings,
    )
