#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_live_receipt_query_surface_v0_1.py"

RECEIPT = {
    "ingestion_status": "QI_LIVE_RECEIPT_INGESTION_READY",
    "ingestion_receipt_id": "qi-live-ingest-test-0001",
    "incident_id": "qi-incident-test-0001",
    "external_case_number": 999,
    "external_case_url": "https://github.com/itakura-hidetoshi/KuuOS/issues/999",
    "archive_key": "qi/cbf-result/test",
    "archive_record_hash": "archive-record-hash-test",
    "idempotency_digest": "idempotency-digest-test",
    "live_receipt_ingested": True,
    "connector_executor_performed": True,
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
    "live_receipt_query_enabled": True,
    "query_mode": "operator_replay_query",
    "read_only_surface_required": True,
    "replay_query_key": "qi/live/test"
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, receipt: dict, ctx: dict, name: str) -> tuple[int, dict]:
    receipt_path = root / f"{name}_receipt.json"
    ctx_path = root / f"{name}_context.json"
    out = root / f"{name}_snapshot.json"
    dump(receipt_path, receipt)
    dump(ctx_path, ctx)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--ingestion-receipt", str(receipt_path),
        "--context", str(ctx_path),
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

        rc, good = run_case(root, RECEIPT, CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("query_status") != "QI_LIVE_RECEIPT_QUERY_SNAPSHOT_READY":
            errors.append("good_status_mismatch")
        if good.get("dashboard_ready") is not True:
            errors.append("dashboard_ready_not_true")
        if good.get("replay_packet_rendered") is not True:
            errors.append("replay_packet_not_rendered")
        if good.get("read_only_surface") is not True:
            errors.append("read_only_not_true")
        if "external case 999" not in good.get("operator_summary", ""):
            errors.append("operator_summary_missing_case")
        if good.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if good.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if good.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        missing = {**RECEIPT, "external_case_url": None}
        rc, bad = run_case(root, missing, CTX, "missing")
        if rc != 1:
            errors.append("missing_returncode_mismatch")
        if "external_case_url_missing" not in bad.get("query_blockers", []):
            errors.append("missing_url_blocker_missing")
        if bad.get("dashboard_ready") is not False:
            errors.append("missing_dashboard_not_false")

        not_read = {**CTX, "read_only_surface_required": False}
        rc, blocked = run_case(root, RECEIPT, not_read, "blocked")
        if rc != 1:
            errors.append("blocked_returncode_mismatch")
        if "read_only_surface_required_not_true" not in blocked.get("query_blockers", []):
            errors.append("read_only_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi live receipt query surface check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
