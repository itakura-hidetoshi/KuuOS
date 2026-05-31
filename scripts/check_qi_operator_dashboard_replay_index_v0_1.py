#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_operator_dashboard_replay_index_v0_1.py"

SNAPSHOT = {
    "query_status": "QI_LIVE_RECEIPT_QUERY_SNAPSHOT_READY",
    "snapshot_id": "qi-live-query-test-0001",
    "incident_id": "qi-incident-test-0001",
    "external_case_number": 999,
    "external_case_url": "https://github.com/itakura-hidetoshi/KuuOS/issues/999",
    "archive_key": "qi/cbf-result/test",
    "archive_record_hash": "archive-record-hash-test",
    "idempotency_digest": "idempotency-digest-test",
    "replay_query_key": "qi/live/test",
    "operator_summary": "Live receipt qi-live-ingest-test-0001 for incident qi-incident-test-0001 maps to external case 999",
    "dashboard_ready": True,
    "read_only_surface": True,
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
    "dashboard_title": "Qi Live Receipt Operator Dashboard",
    "operator_dashboard_enabled": True,
    "read_only_surface_required": True,
    "replay_index_key": "qi/replay/test"
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, snapshot: dict, ctx: dict, name: str) -> tuple[int, dict]:
    snap = root / f"{name}_snapshot.json"
    context = root / f"{name}_context.json"
    out = root / f"{name}_dashboard.json"
    dump(snap, snapshot)
    dump(context, ctx)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--query-snapshot", str(snap),
        "--context", str(context),
        "--write", str(out),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    return completed.returncode, load(out) if out.is_file() else {}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("cli_missing")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, good = run_case(root, SNAPSHOT, CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("index_status") != "QI_OPERATOR_DASHBOARD_REPLAY_INDEX_READY":
            errors.append("good_status_mismatch")
        if good.get("operator_dashboard_ready") is not True:
            errors.append("dashboard_ready_not_true")
        if good.get("dashboard_packet_rendered") is not True:
            errors.append("dashboard_packet_not_rendered")
        if good.get("replay_index_rendered") is not True:
            errors.append("replay_index_not_rendered")
        if good.get("read_only_surface") is not True:
            errors.append("read_only_not_true")
        if len(good.get("dashboard_cards", [])) != 4:
            errors.append("dashboard_card_count_mismatch")
        if not good.get("replay_index_hash"):
            errors.append("replay_index_hash_missing")
        if good.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if good.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if good.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        missing = {**SNAPSHOT, "archive_record_hash": None}
        rc, bad = run_case(root, missing, CTX, "missing")
        if rc != 1:
            errors.append("missing_returncode_mismatch")
        if "archive_record_hash_missing" not in bad.get("dashboard_blockers", []):
            errors.append("archive_hash_blocker_missing")
        if bad.get("operator_dashboard_ready") is not False:
            errors.append("missing_dashboard_ready_not_false")

        not_read = {**CTX, "read_only_surface_required": False}
        rc, blocked = run_case(root, SNAPSHOT, not_read, "blocked")
        if rc != 1:
            errors.append("blocked_returncode_mismatch")
        if "read_only_surface_required_not_true" not in blocked.get("dashboard_blockers", []):
            errors.append("read_only_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi operator dashboard replay index check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
