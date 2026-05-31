#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_live_receipt_ingestion_v0_1.py"

ARCHIVE = {
    "archive_status": "QI_CBF_RESULT_ARCHIVE_RECEIPT_READY",
    "archive_receipt_id": "qi-cbf-archive-test-0001",
    "source_cbf_certificate_id": "qi-connector-cbf-test-0001",
    "source_connector_receipt_id": "qi-connector-case-test-0001",
    "incident_id": "qi-incident-test-0001",
    "external_case_number": 999,
    "external_case_url": "https://github.com/itakura-hidetoshi/KuuOS/issues/999",
    "live_result_archived": True,
    "archive_record_hash": "archive-record-hash-test",
    "archive_key": "qi/cbf-result/test",
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
    "connector_executor_performed": True,
    "external_result_confirmed": True,
    "idempotency_key": "qi-live-ingestion-example-0001",
    "ingestion_mode": "live_result_receipt_ingestion",
    "live_receipt_ingestion_enabled": True
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, archive: dict, ctx: dict, name: str) -> tuple[int, dict]:
    archive_path = root / f"{name}_archive.json"
    ctx_path = root / f"{name}_context.json"
    out = root / f"{name}_ingestion.json"
    dump(archive_path, archive)
    dump(ctx_path, ctx)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--archive-receipt", str(archive_path),
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

        rc, good = run_case(root, ARCHIVE, CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("ingestion_status") != "QI_LIVE_RECEIPT_INGESTION_READY":
            errors.append("good_status_mismatch")
        if good.get("live_receipt_ingested") is not True:
            errors.append("good_ingested_not_true")
        if good.get("connector_executor_result_ingested") is not True:
            errors.append("executor_result_not_ingested")
        if good.get("external_result_confirmed") is not True:
            errors.append("external_result_not_confirmed")
        if not good.get("idempotency_digest"):
            errors.append("idempotency_digest_missing")
        if good.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if good.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if good.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        missing_url = {**ARCHIVE, "external_case_url": None}
        rc, missing = run_case(root, missing_url, CTX, "missing")
        if rc != 1:
            errors.append("missing_returncode_mismatch")
        if "external_case_url_missing" not in missing.get("ingestion_blockers", []):
            errors.append("missing_url_blocker_missing")
        if missing.get("live_receipt_ingested") is not False:
            errors.append("missing_ingested_not_false")

        bad_archive = {**ARCHIVE, "live_result_archived": False}
        rc, bad = run_case(root, bad_archive, CTX, "bad")
        if rc != 1:
            errors.append("bad_returncode_mismatch")
        if "live_result_archived_not_true" not in bad.get("ingestion_blockers", []):
            errors.append("bad_archive_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi live receipt ingestion check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
