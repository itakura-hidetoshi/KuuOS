#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_cbf_result_archive_receipt_v0_1.py"

CERT = {
    "certificate_status": "QI_CONNECTOR_CBF_GATE_CERTIFICATE_READY",
    "certificate_id": "qi-connector-cbf-test-0001",
    "source_connector_receipt_id": "qi-connector-case-test-0001",
    "incident_id": "qi-incident-test-0001",
    "cbf_ok": True,
    "cbf_margin_min": 0.5,
    "connector_result_ingested": True,
    "external_case_number": 999,
    "external_case_url": "https://github.com/itakura-hidetoshi/KuuOS/issues/999",
    "cbf_barriers": [
        {"name": "h_connector_call", "value": 1.0, "threshold": 0.0, "margin": 1.0, "ok": True},
        {"name": "h_live_result_present", "value": 1.0, "threshold": 0.0, "margin": 1.0, "ok": True},
        {"name": "h_duplicate_risk", "value": 0.5, "threshold": 0.0, "margin": 0.5, "ok": True}
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
    "append_only_required": True,
    "archive_key": "qi/cbf-result/test",
    "archive_mode": "append_only_receipt",
    "cbf_result_archive_enabled": True
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, cert: dict, ctx: dict, name: str) -> tuple[int, dict]:
    cert_path = root / f"{name}_certificate.json"
    ctx_path = root / f"{name}_context.json"
    out = root / f"{name}_archive.json"
    dump(cert_path, cert)
    dump(ctx_path, ctx)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--certificate", str(cert_path),
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

        rc, good = run_case(root, CERT, CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("archive_status") != "QI_CBF_RESULT_ARCHIVE_RECEIPT_READY":
            errors.append("good_status_mismatch")
        if good.get("live_result_archived") is not True:
            errors.append("good_archived_not_true")
        if good.get("cbf_ok") is not True:
            errors.append("good_cbf_not_true")
        if good.get("cbf_barrier_count") != 3:
            errors.append("barrier_count_mismatch")
        if not good.get("cbf_barrier_digest"):
            errors.append("barrier_digest_missing")
        if not good.get("archive_record_hash"):
            errors.append("archive_record_hash_missing")
        if good.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if good.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if good.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        bad_cert = {**CERT, "cbf_ok": False}
        rc, bad = run_case(root, bad_cert, CTX, "bad")
        if rc != 1:
            errors.append("bad_returncode_mismatch")
        if "cbf_ok_not_true" not in bad.get("archive_blockers", []):
            errors.append("cbf_blocker_missing")
        if bad.get("live_result_archived") is not False:
            errors.append("bad_archived_not_false")

        no_append = {**CTX, "append_only_required": False}
        rc, blocked = run_case(root, CERT, no_append, "no_append")
        if rc != 1:
            errors.append("no_append_returncode_mismatch")
        if "append_only_required_not_true" not in blocked.get("archive_blockers", []):
            errors.append("append_only_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi CBF result archive receipt check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
