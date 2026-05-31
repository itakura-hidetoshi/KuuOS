#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_static_dashboard_surface_v0_1.py"

PACKET = {
    "index_status": "QI_OPERATOR_DASHBOARD_REPLAY_INDEX_READY",
    "dashboard_packet_id": "qi-dashboard-test-0001",
    "dashboard_title": "Qi Live Receipt Operator Dashboard",
    "operator_dashboard_ready": True,
    "read_only_surface": True,
    "replay_index_key": "qi/replay/test",
    "replay_index_hash": "replay-index-hash-test",
    "dashboard_cards": [
        {"card": "incident", "incident_id": "qi-incident-test-0001", "summary": "test summary"},
        {"card": "external_case", "external_case_number": 999, "external_case_url": "https://github.com/itakura-hidetoshi/KuuOS/issues/999"},
        {"card": "replay", "replay_query_key": "qi/live/test", "archive_key": "qi/cbf-result/test", "archive_record_hash": "archive-record-hash-test"},
        {"card": "idempotency", "idempotency_digest": "idempotency-digest-test"}
    ],
    "daemon_control_performed": False,
    "daemon_restart_performed": False,
    "daemon_stop_performed": False,
    "daemon_resume_performed": False,
    "memory_write_performed": False,
    "memory_append_performed": False,
    "memory_overwrite_performed": False,
    "world_update_performed": False,
    "control_packet_mutation_performed": False,
    "probe_execution_performed": False,
    "auto_remediation_performed": False,
    "grants_daemon_control_authority": False,
    "grants_probe_execution_authority": False,
    "grants_world_update_authority": False,
    "grants_memory_overwrite_authority": False
}

CTX = {
    "generated_by": "kuuos_static_dashboard_surface_v0_1",
    "html_artifact_name": "qi-dashboard-test.html",
    "read_only_surface_required": True,
    "static_dashboard_surface_enabled": True
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, packet: dict, ctx: dict, name: str) -> tuple[int, dict, str]:
    packet_path = root / f"{name}_packet.json"
    ctx_path = root / f"{name}_context.json"
    out = root / f"{name}_surface.json"
    html = root / f"{name}.html"
    dump(packet_path, packet)
    dump(ctx_path, ctx)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--dashboard-packet", str(packet_path),
        "--context", str(ctx_path),
        "--write", str(out),
        "--write-html", str(html),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    return completed.returncode, load(out) if out.is_file() else {}, html.read_text(encoding="utf-8") if html.is_file() else ""


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("cli_missing")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        rc, good, html = run_case(root, PACKET, CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("surface_status") != "QI_STATIC_DASHBOARD_SURFACE_READY":
            errors.append("good_status_mismatch")
        if good.get("dashboard_artifact_ready") is not True:
            errors.append("artifact_ready_not_true")
        if good.get("static_html_rendered") is not True:
            errors.append("html_not_rendered")
        if good.get("js_enabled") is not False:
            errors.append("js_enabled_not_false")
        if good.get("external_network_required") is not False:
            errors.append("external_network_not_false")
        if not good.get("html_sha256"):
            errors.append("html_sha_missing")
        if "<script" in html.lower():
            errors.append("script_tag_present")
        if "Qi Live Receipt Operator Dashboard" not in html:
            errors.append("title_missing_in_html")
        if good.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if good.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if good.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        missing = {**PACKET, "dashboard_cards": []}
        rc, bad, _ = run_case(root, missing, CTX, "missing")
        if rc != 1:
            errors.append("missing_returncode_mismatch")
        if "dashboard_cards_missing" not in bad.get("surface_blockers", []):
            errors.append("cards_blocker_missing")
        if bad.get("dashboard_artifact_ready") is not False:
            errors.append("bad_artifact_ready_not_false")

        not_read = {**CTX, "read_only_surface_required": False}
        rc, blocked, _ = run_case(root, PACKET, not_read, "blocked")
        if rc != 1:
            errors.append("blocked_returncode_mismatch")
        if "read_only_surface_required_not_true" not in blocked.get("surface_blockers", []):
            errors.append("read_only_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi static dashboard surface check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
