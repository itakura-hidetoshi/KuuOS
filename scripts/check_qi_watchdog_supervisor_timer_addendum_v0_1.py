#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_watchdog_supervisor_timer_addendum_v0_1.json"

REQUIRED_TRUE = [
    "read_only_required",
    "timer_only",
    "health_surface_required",
    "prometheus_metrics_forwarded",
    "watchdog_exit_code_forwarded",
    "systemd_timer_examples_included",
]

REQUIRED_FALSE = [
    "daemon_control_performed",
    "daemon_restart_performed",
    "daemon_stop_performed",
    "daemon_resume_performed",
    "memory_write_performed",
    "memory_append_performed",
    "memory_overwrite_performed",
    "world_update_performed",
    "control_packet_mutation_performed",
    "probe_execution_performed",
    "grants_daemon_control_authority",
    "grants_probe_execution_authority",
    "grants_world_update_authority",
    "grants_memory_overwrite_authority",
]

REQUIRED_FILES = [
    "runtime/kuuos_runtime_daemon_qi_watchdog_supervisor_timer_v0_1.py",
    "scripts/run_qi_watchdog_supervisor_timer_v0_1.py",
    "scripts/check_qi_watchdog_supervisor_timer_v0_1.py",
    "scripts/check_qi_watchdog_supervisor_timer_addendum_v0_1.py",
    "scripts/run_qi_watchdog_supervisor_timer_checks_v0_1.py",
    "examples/qi_watchdog_supervisor_timer_context_v0_1.json",
    "docs/qi_watchdog_supervisor_timer_note_v0_1.md",
    "deploy/systemd/qi-jsonl-watchdog.service.example",
    "deploy/systemd/qi-jsonl-watchdog.timer.example",
]


def main() -> int:
    errors: list[str] = []
    if not MANIFEST.is_file():
        errors.append("manifest_missing")
    else:
        value = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if value.get("addendum_status") != "QI_WATCHDOG_SUPERVISOR_TIMER_ADDENDUM_READY":
            errors.append("addendum_status_mismatch")
        if value.get("authority") != "watchdog_supervisor_timer_read_only":
            errors.append("authority_mismatch")
        for key in REQUIRED_TRUE:
            if value.get(key) is not True:
                errors.append(f"{key}_not_true")
        for key in REQUIRED_FALSE:
            if value.get(key) is not False:
                errors.append(f"{key}_not_false")
        listed = []
        for group in ("runtime_files", "script_files", "example_files", "docs_files", "deploy_files"):
            items = value.get(group, [])
            if isinstance(items, list):
                listed.extend(str(item) for item in items)
        for path in REQUIRED_FILES:
            if path not in listed:
                errors.append(f"manifest_missing_file:{path}")
            if not (ROOT / path).is_file():
                errors.append(f"repo_missing_file:{path}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi watchdog supervisor timer addendum check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
