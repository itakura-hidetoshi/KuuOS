#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_incident_handoff_packet_addendum_v0_1.json"

REQUIRED_TRUE = [
    "read_only_required",
    "review_only_required",
    "incident_handoff_packet_enabled",
    "manual_review_required",
    "alertmanager_payload_intake_enabled",
]

REQUIRED_FALSE = [
    "external_notification_send_performed",
    "ticket_created",
    "pagerduty_triggered",
    "slack_message_sent",
    "email_sent",
    "webhook_called",
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
    "auto_remediation_performed",
    "grants_daemon_control_authority",
    "grants_probe_execution_authority",
    "grants_world_update_authority",
    "grants_memory_overwrite_authority",
]

REQUIRED_FILES = [
    "runtime/kuuos_runtime_daemon_qi_incident_handoff_packet_v0_1.py",
    "scripts/run_qi_incident_handoff_packet_v0_1.py",
    "scripts/check_qi_incident_handoff_packet_v0_1.py",
    "scripts/check_qi_incident_handoff_packet_addendum_v0_1.py",
    "scripts/run_qi_incident_handoff_packet_checks_v0_1.py",
    "examples/qi_incident_handoff_context_v0_1.json",
    "examples/qi_alertmanager_payload_v0_1.json",
    "docs/qi_incident_handoff_packet_note_v0_1.md",
    "deploy/alertmanager/qi-jsonl-incident-handoff-route.example.yml",
]


def main() -> int:
    errors: list[str] = []
    if not MANIFEST.is_file():
        errors.append("manifest_missing")
    else:
        value = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if value.get("addendum_status") != "QI_INCIDENT_HANDOFF_PACKET_ADDENDUM_READY":
            errors.append("addendum_status_mismatch")
        if value.get("authority") != "incident_handoff_review_only":
            errors.append("authority_mismatch")
        for key in REQUIRED_TRUE:
            if value.get(key) is not True:
                errors.append(f"{key}_not_true")
        for key in REQUIRED_FALSE:
            if value.get(key) is not False:
                errors.append(f"{key}_not_false")
        listed: list[str] = []
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
    print("PASS: Qi incident handoff packet addendum check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
