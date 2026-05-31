#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import pathlib
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_health_metrics_watchdog_surface_v0_1 import (
    QiHealthMetricsWatchdogSurface,
    build_qi_health_metrics_watchdog_surface,
)


@dataclass(frozen=True)
class QiWatchdogSupervisorTimerReport:
    surface_version: str
    supervisor_status: str
    timer_status: str
    timer_mode: str
    iteration_count: int
    max_iterations: int
    last_health_status: str | None
    last_watchdog_status: str | None
    watchdog_exit_code: int
    read_only_required: bool
    timer_only: bool
    daemon_control_performed: bool
    daemon_restart_performed: bool
    daemon_stop_performed: bool
    daemon_resume_performed: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_daemon_control_authority: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    health_packets: list[dict[str, Any]]
    prometheus_text: str
    supervisor_blockers: list[str]
    supervisor_warnings: list[str]
    authority: str = "watchdog_supervisor_timer_read_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _bool(value: Any) -> bool:
    return value is True


def _prom_line(name: str, value: int | float, labels: Mapping[str, str] | None = None) -> str:
    if labels:
        rendered = ",".join(f'{key}="{val}"' for key, val in sorted(labels.items()))
        return f"{name}{{{rendered}}} {value}"
    return f"{name} {value}"


def _classify_exit_code(blockers: list[str], warnings: list[str], last: QiHealthMetricsWatchdogSurface | None) -> int:
    if blockers:
        return 2
    if last is None:
        return 2
    if last.health_status != "QI_HEALTH_METRICS_WATCHDOG_HEALTHY":
        return 2
    if last.watchdog_status != "QI_WATCHDOG_OK":
        return 1
    if warnings or last.surface_warnings:
        return 1
    return 0


def build_qi_watchdog_supervisor_timer_report(
    *,
    daemon_status_path: str | pathlib.Path,
    event_log_path: str | pathlib.Path,
    ledger_state_path: str | pathlib.Path,
    supervisor_context: Mapping[str, Any] | None = None,
    max_iterations: int = 1,
) -> QiWatchdogSupervisorTimerReport:
    """Run a bounded read-only watchdog timer pass.

    This supervisor intentionally does not restart, stop, resume, mutate, or repair the daemon.
    It repeatedly samples the health/metrics surface and emits a report suitable for systemd
    timer or cron-style external scheduling.
    """

    ctx = _mapping(supervisor_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("read_only_required") is not True:
        blockers.append("read_only_required_not_true")
    if ctx.get("timer_only") is not True:
        blockers.append("timer_only_not_true")
    if _bool(ctx.get("request_daemon_restart")):
        blockers.append("request_daemon_restart")
    if _bool(ctx.get("request_daemon_stop")):
        blockers.append("request_daemon_stop")
    if _bool(ctx.get("request_daemon_resume")):
        blockers.append("request_daemon_resume")
    if _bool(ctx.get("request_probe_execution")):
        blockers.append("request_probe_execution")
    if _bool(ctx.get("request_world_update")):
        blockers.append("request_world_update")
    if _bool(ctx.get("request_memory_write")):
        blockers.append("request_memory_write")
    if _bool(ctx.get("request_control_packet_mutation")):
        blockers.append("request_control_packet_mutation")

    bounded_iterations = max(1, min(int(max_iterations or 1), int(ctx.get("max_allowed_iterations", 5) or 5)))
    health_context = {
        "read_only_required": True,
        "watchdog_enabled": True,
        "request_probe_execution": False,
        "request_world_update": False,
        "request_memory_write": False,
        "min_heartbeat_count": int(ctx.get("min_heartbeat_count", 0) or 0),
    }

    packets: list[dict[str, Any]] = []
    last: QiHealthMetricsWatchdogSurface | None = None
    for _ in range(bounded_iterations):
        last = build_qi_health_metrics_watchdog_surface(
            daemon_status_path=daemon_status_path,
            event_log_path=event_log_path,
            ledger_state_path=ledger_state_path,
            watchdog_context=health_context,
        )
        packets.append(last.to_dict())

    if bounded_iterations < int(max_iterations or 1):
        warnings.append("max_iterations_clamped")
    if last is not None and last.surface_blockers:
        blockers.extend(f"health_surface:{item}" for item in last.surface_blockers)
    if last is not None and last.surface_warnings:
        warnings.extend(f"health_surface:{item}" for item in last.surface_warnings)

    exit_code = _classify_exit_code(blockers, warnings, last)
    supervisor_status = (
        "QI_WATCHDOG_SUPERVISOR_OK"
        if exit_code == 0
        else "QI_WATCHDOG_SUPERVISOR_DEGRADED"
        if exit_code == 1
        else "QI_WATCHDOG_SUPERVISOR_BLOCKED"
    )
    timer_status = "QI_WATCHDOG_TIMER_COMPLETED" if exit_code in (0, 1) else "QI_WATCHDOG_TIMER_BLOCKED"

    labels = {"daemon": "qi_jsonl", "surface": "watchdog_supervisor_timer"}
    prom_lines = [
        _prom_line("kuos_qi_watchdog_supervisor_ok", 1 if exit_code == 0 else 0, labels),
        _prom_line("kuos_qi_watchdog_supervisor_degraded", 1 if exit_code == 1 else 0, labels),
        _prom_line("kuos_qi_watchdog_supervisor_blocked", 1 if exit_code == 2 else 0, labels),
        _prom_line("kuos_qi_watchdog_supervisor_iterations", bounded_iterations, labels),
        _prom_line("kuos_qi_watchdog_supervisor_exit_code", exit_code, labels),
    ]
    if last is not None:
        prom_lines.append(last.prometheus_text.rstrip())

    return QiWatchdogSupervisorTimerReport(
        surface_version="kuuos_runtime_daemon_qi_watchdog_supervisor_timer_v0_1",
        supervisor_status=supervisor_status,
        timer_status=timer_status,
        timer_mode="bounded_read_only_timer",
        iteration_count=bounded_iterations,
        max_iterations=int(max_iterations or 1),
        last_health_status=last.health_status if last is not None else None,
        last_watchdog_status=last.watchdog_status if last is not None else None,
        watchdog_exit_code=exit_code,
        read_only_required=ctx.get("read_only_required") is True,
        timer_only=ctx.get("timer_only") is True,
        daemon_control_performed=False,
        daemon_restart_performed=False,
        daemon_stop_performed=False,
        daemon_resume_performed=False,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_daemon_control_authority=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        health_packets=packets,
        prometheus_text="\n".join(prom_lines) + "\n",
        supervisor_blockers=blockers,
        supervisor_warnings=warnings,
    )
