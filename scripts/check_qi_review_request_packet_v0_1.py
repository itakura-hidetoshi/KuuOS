#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_review_request_packet_v0_1.py"

HANDOFF = {
    "handoff_status": "QI_INCIDENT_HANDOFF_PACKET_READY",
    "incident_id": "qi-incident-test-0001",
    "max_severity": "warning",
    "recommended_action": "manual_review_recommended",
    "manual_review_required": True,
    "alert_summaries": [
        {
            "alert_name": "KuuOSQiJsonlWatchdogNeedsReview",
            "status": "firing",
            "severity": "warning",
            "authority": "read_only_alert",
            "summary": "KuuOS Qi JSONL watchdog needs review",
            "description": "Manual review requested without daemon control authority.",
        }
    ],
}

CTX = {
    "case_system": "review-queue",
    "explicit_delivery_gate_required": True,
    "perform_auto_remediation": False,
    "perform_case_open": False,
    "perform_control_packet_mutation": False,
    "perform_daemon_restart": False,
    "perform_daemon_resume": False,
    "perform_daemon_stop": False,
    "perform_memory_write": False,
    "perform_outbound_delivery": False,
    "perform_probe_execution": False,
    "perform_world_update": False,
    "read_only_required": True,
    "request_packet_only_required": True,
    "review_request_packet_enabled": True,
    "review_route": "external-review-inbox",
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
        handoff = root / "handoff.json"
        context = root / "context.json"
        packet = root / "request_packet.json"
        dump(handoff, HANDOFF)
        dump(context, CTX)
        completed = subprocess.run([
            sys.executable,
            str(CLI),
            "--incident-handoff", str(handoff),
            "--context", str(context),
            "--write", str(packet),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append("review_request_cli_failed")
            errors.append(completed.stdout.strip() or completed.stderr.strip())
        if not packet.is_file():
            errors.append("packet_missing")
        else:
            value = load(packet)
            if value.get("packet_status") != "QI_REVIEW_REQUEST_PACKET_READY":
                errors.append("packet_status_mismatch")
            if value.get("incident_id") != "qi-incident-test-0001":
                errors.append("incident_id_mismatch")
            if value.get("outbound_review_message_rendered") is not True:
                errors.append("outbound_message_not_rendered")
            if value.get("case_open_request_rendered") is not True:
                errors.append("case_request_not_rendered")
            if value.get("outbound_delivery_performed") is not False:
                errors.append("outbound_delivery_not_false")
            if value.get("case_opened") is not False:
                errors.append("case_opened_not_false")
            if value.get("daemon_restart_performed") is not False:
                errors.append("daemon_restart_not_false")
            if value.get("world_update_performed") is not False:
                errors.append("world_update_not_false")
            if value.get("memory_write_performed") is not False:
                errors.append("memory_write_not_false")
            if value.get("auto_remediation_performed") is not False:
                errors.append("auto_remediation_not_false")
            if "Boundary: request packet only" not in value.get("outbound_review_message", {}).get("body", ""):
                errors.append("boundary_text_missing")

        blocked_context = root / "blocked_context.json"
        blocked_packet = root / "blocked_request_packet.json"
        dump(blocked_context, {**CTX, "perform_case_open": True})
        blocked = subprocess.run([
            sys.executable,
            str(CLI),
            "--incident-handoff", str(handoff),
            "--context", str(blocked_context),
            "--write", str(blocked_packet),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if blocked.returncode != 1:
            errors.append("blocked_returncode_mismatch")
        if blocked_packet.is_file():
            value = load(blocked_packet)
            if "perform_case_open" not in value.get("packet_blockers", []):
                errors.append("case_open_blocker_missing")
            if value.get("case_opened") is not False:
                errors.append("blocked_case_opened_not_false")
        else:
            errors.append("blocked_packet_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi review request packet check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
