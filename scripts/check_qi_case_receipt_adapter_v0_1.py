#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_case_receipt_adapter_v0_1.py"

REQUEST = {
    "packet_status": "QI_REVIEW_REQUEST_PACKET_READY",
    "packet_id": "qi-review-request-test-0001",
    "incident_id": "qi-incident-test-0001",
    "case_open_request": {
        "system": "review-queue",
        "title": "KuuOS Qi incident review request: qi-incident-test-0001 (warning)",
        "labels": ["kuuos", "qi-jsonl", "incident-review", "warning"],
        "case_opened": False,
        "case_open_authority_granted": False,
    },
}

APPROVED_CTX = {
    "adapter_mode": "approved_local_case_receipt",
    "approval_receipt_sha": "sha256:approved-review-request-example",
    "approved": True,
    "approved_by": "itakura-hidetoshi",
    "approved_case_opener_enabled": True,
    "dry_run": False,
    "idempotency_key": "qi-case-example-0001",
    "idempotency_key_required": True,
    "perform_auto_remediation": False,
    "perform_control_packet_mutation": False,
    "perform_daemon_restart": False,
    "perform_daemon_resume": False,
    "perform_daemon_stop": False,
    "perform_memory_write": False,
    "perform_probe_execution": False,
    "perform_world_update": False,
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, context: dict, name: str) -> tuple[int, dict]:
    request = root / f"{name}_request.json"
    ctx = root / f"{name}_context.json"
    out = root / f"{name}_receipt.json"
    dump(request, REQUEST)
    dump(ctx, context)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--review-request", str(request),
        "--approval-context", str(ctx),
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

        rc, approved = run_case(root, APPROVED_CTX, "approved")
        if rc != 0:
            errors.append("approved_case_returncode_mismatch")
        if approved.get("receipt_status") != "QI_APPROVED_CASE_OPENER_RECEIPT_READY":
            errors.append("approved_status_mismatch")
        if approved.get("case_opened") is not True:
            errors.append("approved_case_opened_not_true")
        if approved.get("case_open_adapter_executed") is not True:
            errors.append("approved_adapter_executed_not_true")
        if approved.get("external_api_call_performed") is not False:
            errors.append("external_api_call_not_false")
        if approved.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if approved.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if approved.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        dry_ctx = {**APPROVED_CTX, "dry_run": True, "approved": False, "approved_by": None, "approval_receipt_sha": None, "idempotency_key": "qi-case-dry-0001"}
        rc, dry = run_case(root, dry_ctx, "dry")
        if rc != 0:
            errors.append("dry_run_returncode_mismatch")
        if dry.get("case_opened") is not False:
            errors.append("dry_case_opened_not_false")
        if "dry_run_no_case_opened" not in dry.get("adapter_warnings", []):
            errors.append("dry_warning_missing")

        blocked_ctx = {**APPROVED_CTX, "idempotency_key": None}
        rc, blocked = run_case(root, blocked_ctx, "blocked")
        if rc != 1:
            errors.append("blocked_returncode_mismatch")
        if "idempotency_key_missing" not in blocked.get("adapter_blockers", []):
            errors.append("idempotency_blocker_missing")
        if blocked.get("case_opened") is not False:
            errors.append("blocked_case_opened_not_false")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi case receipt adapter check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
