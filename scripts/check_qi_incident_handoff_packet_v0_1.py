#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_incident_handoff_packet_v0_1.py"

ALERT_PAYLOAD = {
    "receiver": "qi-jsonl-review",
    "status": "firing",
    "groupKey": "qi-jsonl-watchdog",
    "alerts": [
        {
            "status": "firing",
            "labels": {
                "alertname": "KuuOSQiJsonlWatchdogNeedsReview",
                "severity": "warning",
                "authority": "read_only_alert",
                "daemon": "qi_jsonl",
            },
            "annotations": {
                "summary": "KuuOS Qi JSONL watchdog needs review",
                "description": "Manual review requested without daemon control authority.",
            },
        }
    ],
}

EXPORTER = {
    "exporter_status": "QI_LOCAL_METRICS_HTTP_EXPORTER_READY",
    "watchdog_exit_code": 1,
    "daemon_restart_performed": False,
    "world_update_performed": False,
    "memory_write_performed": False,
}

CTX = {
    "incident_handoff_enabled": True,
    "read_only_required": True,
    "review_only_required": True,
    "route_key": "qi-jsonl-review",
    "source_system": "prometheus_alertmanager",
    "request_auto_remediation": False,
    "request_control_packet_mutation": False,
    "request_daemon_restart": False,
    "request_daemon_resume": False,
    "request_daemon_stop": False,
    "request_email_send": False,
    "request_external_notification_send": False,
    "request_memory_write": False,
    "request_pagerduty_trigger": False,
    "request_probe_execution": False,
    "request_slack_message": False,
    "request_ticket_create": False,
    "request_webhook_call": False,
    "request_world_update": False,
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
        alert = root / "alert.json"
        exporter = root / "exporter.json"
        context = root / "context.json"
        packet = root / "packet.json"
        dump(alert, ALERT_PAYLOAD)
        dump(exporter, EXPORTER)
        dump(context, CTX)
        completed = subprocess.run([
            sys.executable,
            str(CLI),
            "--alertmanager-payload", str(alert),
            "--exporter-snapshot", str(exporter),
            "--context", str(context),
            "--write", str(packet),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append("handoff_cli_failed")
            errors.append(completed.stdout.strip() or completed.stderr.strip())
        if not packet.is_file():
            errors.append("packet_missing")
        else:
            value = load(packet)
            if value.get("handoff_status") != "QI_INCIDENT_HANDOFF_PACKET_READY":
                errors.append("handoff_status_mismatch")
            if value.get("alert_count") != 1:
                errors.append("alert_count_mismatch")
            if value.get("firing_count") != 1:
                errors.append("firing_count_mismatch")
            if value.get("max_severity") != "warning":
                errors.append("severity_mismatch")
            if value.get("manual_review_required") is not True:
                errors.append("manual_review_not_true")
            if value.get("recommended_action") != "manual_review_recommended":
                errors.append("recommended_action_mismatch")
            for key in (
                "external_notification_send_performed",
                "ticket_created",
                "pagerduty_triggered",
                "slack_message_sent",
                "email_sent",
                "webhook_called",
                "daemon_restart_performed",
                "world_update_performed",
                "memory_write_performed",
                "auto_remediation_performed",
            ):
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked_context = root / "blocked_context.json"
        blocked_packet = root / "blocked_packet.json"
        dump(blocked_context, {**CTX, "request_ticket_create": True})
        blocked = subprocess.run([
            sys.executable,
            str(CLI),
            "--alertmanager-payload", str(alert),
            "--exporter-snapshot", str(exporter),
            "--context", str(blocked_context),
            "--write", str(blocked_packet),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if blocked.returncode != 1:
            errors.append("blocked_returncode_mismatch")
        if blocked_packet.is_file():
            value = load(blocked_packet)
            if "request_ticket_create" not in value.get("handoff_blockers", []):
                errors.append("ticket_create_blocker_missing")
            if value.get("ticket_created") is not False:
                errors.append("blocked_ticket_created_not_false")
        else:
            errors.append("blocked_packet_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi incident handoff packet check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
