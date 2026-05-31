#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_local_metrics_http_exporter_v0_1.py"

PROM_TEXT = """kuos_qi_watchdog_supervisor_ok{daemon=\"qi_jsonl\",surface=\"watchdog_supervisor_timer\"} 1
kuos_qi_watchdog_supervisor_exit_code{daemon=\"qi_jsonl\",surface=\"watchdog_supervisor_timer\"} 0
kuos_qi_daemon_health_ok{daemon=\"qi_jsonl\",surface=\"health_metrics_watchdog\"} 1
"""

CTX = {
    "read_only_required": True,
    "local_http_exporter_enabled": True,
    "prometheus_scrape_enabled": True,
    "alert_rules_example_enabled": True,
    "bind_host": "127.0.0.1",
    "bind_port": 9187,
    "metrics_endpoint": "/metrics",
    "health_endpoint": "/healthz",
    "ready_endpoint": "/readyz",
    "request_daemon_restart": False,
    "request_daemon_stop": False,
    "request_daemon_resume": False,
    "request_probe_execution": False,
    "request_world_update": False,
    "request_memory_write": False,
    "request_control_packet_mutation": False,
}

REPORT = {
    "supervisor_status": "QI_WATCHDOG_SUPERVISOR_OK",
    "watchdog_exit_code": 0,
    "daemon_restart_performed": False,
    "world_update_performed": False,
    "memory_write_performed": False,
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("cli_missing")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        metrics = root / "watchdog_metrics.prom"
        report = root / "watchdog_report.json"
        context = root / "exporter_context.json"
        snapshot = root / "exporter_snapshot.json"
        response = root / "metrics_response.json"
        metrics.write_text(PROM_TEXT, encoding="utf-8")
        dump(report, REPORT)
        dump(context, CTX)
        completed = subprocess.run([
            sys.executable,
            str(CLI),
            "--metrics-file", str(metrics),
            "--health-report", str(report),
            "--context", str(context),
            "--write", str(snapshot),
            "--write-response", str(response),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append("exporter_cli_failed")
            errors.append(completed.stdout.strip() or completed.stderr.strip())
        if not snapshot.is_file() or not response.is_file():
            errors.append("exporter_outputs_missing")
        else:
            value = load(snapshot)
            reply = load(response)
            if value.get("exporter_status") != "QI_LOCAL_METRICS_HTTP_EXPORTER_READY":
                errors.append("exporter_status_mismatch")
            if value.get("metrics_line_count") != 3:
                errors.append("metrics_line_count_mismatch")
            if value.get("health_report_status") != "QI_WATCHDOG_SUPERVISOR_OK":
                errors.append("health_report_status_mismatch")
            if value.get("watchdog_exit_code") != 0:
                errors.append("watchdog_exit_code_mismatch")
            if value.get("http_server_started") is not False:
                errors.append("http_server_started_not_false")
            if value.get("daemon_restart_performed") is not False:
                errors.append("daemon_restart_not_false")
            if value.get("world_update_performed") is not False:
                errors.append("world_update_not_false")
            if value.get("memory_write_performed") is not False:
                errors.append("memory_write_not_false")
            if reply.get("status_code") != 200:
                errors.append("response_status_mismatch")
            if "kuos_qi_daemon_health_ok" not in reply.get("body", ""):
                errors.append("response_body_missing_metric")

        blocked_context = root / "blocked_context.json"
        blocked_snapshot = root / "blocked_snapshot.json"
        dump(blocked_context, {**CTX, "request_daemon_restart": True})
        blocked = subprocess.run([
            sys.executable,
            str(CLI),
            "--metrics-file", str(metrics),
            "--health-report", str(report),
            "--context", str(blocked_context),
            "--write", str(blocked_snapshot),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if blocked.returncode != 1:
            errors.append("blocked_exit_code_mismatch")
        if blocked_snapshot.is_file():
            value = load(blocked_snapshot)
            if "request_daemon_restart" not in value.get("exporter_blockers", []):
                errors.append("restart_blocker_missing")
            if value.get("daemon_restart_performed") is not False:
                errors.append("blocked_restart_not_false")
        else:
            errors.append("blocked_snapshot_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi local metrics HTTP exporter snapshot check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
