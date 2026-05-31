#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import pathlib
from typing import Any, Mapping


@dataclass(frozen=True)
class QiLocalMetricsHttpExporterSnapshot:
    surface_version: str
    exporter_status: str
    metrics_endpoint: str
    health_endpoint: str
    ready_endpoint: str
    bind_host: str
    bind_port: int
    metrics_file_path: str
    health_report_path: str | None
    metrics_bytes: int
    metrics_line_count: int
    health_report_status: str | None
    watchdog_exit_code: int | None
    read_only_required: bool
    local_http_exporter_enabled: bool
    prometheus_scrape_enabled: bool
    alert_rules_example_enabled: bool
    metrics_file_read_performed: bool
    health_report_read_performed: bool
    http_server_started: bool
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
    exporter_blockers: list[str]
    exporter_warnings: list[str]
    prometheus_text: str
    authority: str = "local_metrics_http_exporter_read_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _read_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _read_metrics(path: pathlib.Path) -> tuple[str, list[str]]:
    if not path.is_file():
        return "", ["metrics_file_missing"]
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return "", ["metrics_file_unreadable"]
    if not text.endswith("\n"):
        text += "\n"
    return text, []


def build_qi_local_metrics_http_exporter_snapshot(
    *,
    metrics_file_path: str | pathlib.Path,
    health_report_path: str | pathlib.Path | None = None,
    exporter_context: Mapping[str, Any] | None = None,
) -> QiLocalMetricsHttpExporterSnapshot:
    ctx = _mapping(exporter_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("read_only_required") is not True:
        blockers.append("read_only_required_not_true")
    if ctx.get("local_http_exporter_enabled") is not True:
        blockers.append("local_http_exporter_enabled_not_true")
    if ctx.get("prometheus_scrape_enabled") is not True:
        blockers.append("prometheus_scrape_enabled_not_true")
    for key in (
        "request_daemon_restart",
        "request_daemon_stop",
        "request_daemon_resume",
        "request_probe_execution",
        "request_world_update",
        "request_memory_write",
        "request_control_packet_mutation",
    ):
        if ctx.get(key) is True:
            blockers.append(key)

    metrics_path = pathlib.Path(metrics_file_path)
    metrics_text, metric_blockers = _read_metrics(metrics_path)
    blockers.extend(metric_blockers)

    report_path = pathlib.Path(health_report_path) if health_report_path is not None else None
    report = _read_json(report_path)
    health_status = report.get("supervisor_status") or report.get("health_status")
    exit_code_value = report.get("watchdog_exit_code")
    try:
        exit_code = int(exit_code_value) if exit_code_value is not None else None
    except (TypeError, ValueError):
        exit_code = None
        warnings.append("watchdog_exit_code_non_integer")

    if exit_code == 2:
        warnings.append("watchdog_report_blocked")
    elif exit_code == 1:
        warnings.append("watchdog_report_degraded")

    bind_host = str(ctx.get("bind_host", "127.0.0.1"))
    bind_port = int(ctx.get("bind_port", 9187) or 9187)
    endpoint = str(ctx.get("metrics_endpoint", "/metrics"))
    health_endpoint = str(ctx.get("health_endpoint", "/healthz"))
    ready_endpoint = str(ctx.get("ready_endpoint", "/readyz"))
    line_count = len([line for line in metrics_text.splitlines() if line.strip()])

    exporter_ok = not blockers
    return QiLocalMetricsHttpExporterSnapshot(
        surface_version="kuuos_runtime_daemon_qi_local_metrics_http_exporter_v0_1",
        exporter_status="QI_LOCAL_METRICS_HTTP_EXPORTER_READY" if exporter_ok else "QI_LOCAL_METRICS_HTTP_EXPORTER_BLOCKED",
        metrics_endpoint=endpoint,
        health_endpoint=health_endpoint,
        ready_endpoint=ready_endpoint,
        bind_host=bind_host,
        bind_port=bind_port,
        metrics_file_path=str(metrics_path),
        health_report_path=str(report_path) if report_path is not None else None,
        metrics_bytes=len(metrics_text.encode("utf-8")),
        metrics_line_count=line_count,
        health_report_status=str(health_status) if health_status else None,
        watchdog_exit_code=exit_code,
        read_only_required=ctx.get("read_only_required") is True,
        local_http_exporter_enabled=ctx.get("local_http_exporter_enabled") is True,
        prometheus_scrape_enabled=ctx.get("prometheus_scrape_enabled") is True,
        alert_rules_example_enabled=ctx.get("alert_rules_example_enabled") is True,
        metrics_file_read_performed=True,
        health_report_read_performed=report_path is not None,
        http_server_started=False,
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
        exporter_blockers=blockers,
        exporter_warnings=warnings,
        prometheus_text=metrics_text,
    )


def render_metrics_http_response(snapshot: QiLocalMetricsHttpExporterSnapshot) -> dict[str, Any]:
    status_code = 200 if snapshot.exporter_status == "QI_LOCAL_METRICS_HTTP_EXPORTER_READY" else 503
    return {
        "status_code": status_code,
        "content_type": "text/plain; version=0.0.4; charset=utf-8",
        "body": snapshot.prometheus_text,
        "daemon_control_performed": False,
        "world_update_performed": False,
        "memory_write_performed": False,
    }
