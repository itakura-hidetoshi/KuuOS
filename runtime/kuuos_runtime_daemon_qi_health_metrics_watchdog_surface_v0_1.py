#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import pathlib
from typing import Any, Mapping


@dataclass(frozen=True)
class QiHealthMetricsWatchdogSurface:
    surface_version: str
    health_status: str
    watchdog_status: str
    metrics_format: str
    event_log_path: str
    ledger_state_path: str
    daemon_status_path: str
    daemon_resume_status: str | None
    heartbeat_count: int
    jsonl_event_line_count: int
    replay_cursor_position: int
    replay_cursor_monotone: bool
    token_ledger_count: int
    process_tensor_pressure: str | None
    dominant_probe_type: str | None
    safe_resume_performed: bool
    no_op_resume: bool
    idempotency_enforced: bool
    duplicate_tick_blocked: bool
    token_ledger_checked: bool
    observation_debt_resolution_priority: float | None
    safe_reentry_window_score: float | None
    nonmarkov_link_density: float | None
    memory_kernel_preservation_score: float | None
    prometheus_text: str
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    surface_blockers: list[str]
    surface_warnings: list[str]
    authority: str = "health_metrics_watchdog_read_only"

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


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _pressure_value(value: str | None) -> int:
    if value == "high":
        return 3
    if value == "moderate":
        return 2
    if value == "low":
        return 1
    return 0


def _prom_line(name: str, value: int | float, labels: Mapping[str, str] | None = None) -> str:
    if labels:
        rendered = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
        return f"{name}{{{rendered}}} {value}"
    return f"{name} {value}"


def build_qi_health_metrics_watchdog_surface(
    *,
    daemon_status_path: str | pathlib.Path,
    event_log_path: str | pathlib.Path,
    ledger_state_path: str | pathlib.Path,
    watchdog_context: Mapping[str, Any] | None = None,
) -> QiHealthMetricsWatchdogSurface:
    ctx = _mapping(watchdog_context)
    status_path = pathlib.Path(daemon_status_path)
    event_path = pathlib.Path(event_log_path)
    ledger_path = pathlib.Path(ledger_state_path)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("read_only_required") is not True:
        blockers.append("read_only_required_not_true")
    if ctx.get("watchdog_enabled") is not True:
        blockers.append("watchdog_enabled_not_true")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")

    status = _read_json(status_path)
    ledger = _read_json(ledger_path)
    events = _read_jsonl(event_path)
    if not status:
        blockers.append("daemon_status_missing_or_invalid")
    if any("_invalid_jsonl_line" in row for row in events):
        blockers.append("event_log_contains_invalid_jsonl")

    resume_status = status.get("resume_status")
    if resume_status not in ("QI_JSONL_SAFE_RESUME_CONTROLLER_COMPLETED", None):
        blockers.append("daemon_resume_status_not_completed")
    if status.get("probe_execution_performed") is not False:
        blockers.append("daemon_probe_execution_not_false")
    if status.get("world_update_performed") is not False:
        blockers.append("daemon_world_update_not_false")
    if status.get("memory_overwrite_performed") is not False:
        blockers.append("daemon_memory_overwrite_not_false")

    cursor = _mapping(ledger.get("replay_cursor"))
    cursor_position = int(cursor.get("position", 0) or 0)
    token_ids = _mapping(ledger.get("token_ledger")).get("consumed_token_ids", [])
    token_count = len(token_ids) if isinstance(token_ids, list) else 0
    event_count = len(events)
    cursor_monotone = cursor_position >= 0 and cursor_position >= event_count if event_count else cursor_position >= 0
    if not cursor_monotone:
        blockers.append("replay_cursor_not_monotone")

    wrapper = _mapping(status.get("wrapper_packet"))
    tick_packets = wrapper.get("tick_packets", []) if isinstance(wrapper.get("tick_packets"), list) else []
    last_tick = tick_packets[-1] if tick_packets and isinstance(tick_packets[-1], Mapping) else {}
    heartbeat_count = int(status.get("heartbeat_count", 0) or 0)
    pressure = last_tick.get("process_tensor_pressure") or status.get("process_tensor_pressure")
    dominant_probe_type = last_tick.get("dominant_probe_type") or status.get("dominant_probe_type")
    metrics_payload = _mapping(status.get("process_tensor_metrics")) or _mapping(last_tick)

    warning_threshold = int(ctx.get("min_heartbeat_count", 0) or 0)
    if heartbeat_count < warning_threshold:
        warnings.append("heartbeat_count_below_threshold")
    if pressure == "high":
        warnings.append("process_tensor_pressure_high")

    health_ok = not blockers
    watchdog_ok = health_ok and not any(w == "heartbeat_count_below_threshold" for w in warnings)
    labels = {"daemon": "qi_jsonl", "surface": "health_metrics_watchdog"}
    metrics_lines = [
        _prom_line("kuos_qi_daemon_health_ok", 1 if health_ok else 0, labels),
        _prom_line("kuos_qi_daemon_watchdog_ok", 1 if watchdog_ok else 0, labels),
        _prom_line("kuos_qi_daemon_heartbeat_count", heartbeat_count, labels),
        _prom_line("kuos_qi_daemon_event_log_lines", event_count, labels),
        _prom_line("kuos_qi_daemon_replay_cursor_position", cursor_position, labels),
        _prom_line("kuos_qi_daemon_token_ledger_count", token_count, labels),
        _prom_line("kuos_qi_process_tensor_pressure", _pressure_value(str(pressure) if pressure else None), labels),
    ]
    return QiHealthMetricsWatchdogSurface(
        surface_version="kuuos_runtime_daemon_qi_health_metrics_watchdog_surface_v0_1",
        health_status="QI_HEALTH_METRICS_WATCHDOG_HEALTHY" if health_ok else "QI_HEALTH_METRICS_WATCHDOG_BLOCKED",
        watchdog_status="QI_WATCHDOG_OK" if watchdog_ok else "QI_WATCHDOG_ATTENTION_REQUIRED",
        metrics_format="prometheus_text_v0_0_4",
        event_log_path=str(event_path),
        ledger_state_path=str(ledger_path),
        daemon_status_path=str(status_path),
        daemon_resume_status=str(resume_status) if resume_status else None,
        heartbeat_count=heartbeat_count,
        jsonl_event_line_count=event_count,
        replay_cursor_position=cursor_position,
        replay_cursor_monotone=cursor_monotone,
        token_ledger_count=token_count,
        process_tensor_pressure=str(pressure) if pressure else None,
        dominant_probe_type=str(dominant_probe_type) if dominant_probe_type else None,
        safe_resume_performed=status.get("safe_resume_performed") is True,
        no_op_resume=status.get("no_op_resume") is True,
        idempotency_enforced=status.get("idempotency_enforced") is True,
        duplicate_tick_blocked=status.get("duplicate_tick_blocked") is True,
        token_ledger_checked=status.get("token_ledger_checked") is True,
        observation_debt_resolution_priority=_float_or_none(metrics_payload.get("observation_debt_resolution_priority")),
        safe_reentry_window_score=_float_or_none(metrics_payload.get("safe_reentry_window_score")),
        nonmarkov_link_density=_float_or_none(metrics_payload.get("nonmarkov_link_density")),
        memory_kernel_preservation_score=_float_or_none(metrics_payload.get("memory_kernel_preservation_score")),
        prometheus_text="\n".join(metrics_lines) + "\n",
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        surface_blockers=blockers,
        surface_warnings=warnings,
    )
