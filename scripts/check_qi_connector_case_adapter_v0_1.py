#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_connector_case_adapter_v0_1.py"

CASE_RECEIPT = {
    "receipt_status": "QI_APPROVED_CASE_OPENER_RECEIPT_READY",
    "receipt_id": "qi-case-receipt-test-0001",
    "incident_id": "qi-incident-test-0001",
    "case_title": "KuuOS Qi incident review request: qi-incident-test-0001 (warning)",
    "case_labels": ["kuuos", "qi-jsonl", "incident-review", "warning"],
    "case_opened": True,
    "idempotency_key": "qi-case-example-0001",
    "external_api_call_performed": False,
    "daemon_restart_performed": False,
    "world_update_performed": False,
    "memory_write_performed": False,
}

PAYLOAD_CTX = {
    "approved": True,
    "approved_by": "itakura-hidetoshi",
    "connector_case_adapter_enabled": True,
    "connector_kind": "github_issue",
    "connector_mode": "github_issue_connector",
    "target_repo": "itakura-hidetoshi/KuuOS",
}

CALLED_CTX = {
    **PAYLOAD_CTX,
    "connector_call_performed": True,
    "external_case_number": 999,
    "external_case_url": "https://github.com/itakura-hidetoshi/KuuOS/issues/999",
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, context: dict, name: str) -> tuple[int, dict]:
    case_receipt = root / f"{name}_case_receipt.json"
    ctx = root / f"{name}_context.json"
    out = root / f"{name}_connector_receipt.json"
    dump(case_receipt, CASE_RECEIPT)
    dump(ctx, context)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--case-receipt", str(case_receipt),
        "--connector-context", str(ctx),
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

        rc, payload = run_case(root, PAYLOAD_CTX, "payload")
        if rc != 0:
            errors.append("payload_returncode_mismatch")
        if payload.get("receipt_status") != "QI_CONNECTOR_CASE_RECEIPT_READY":
            errors.append("payload_status_mismatch")
        if payload.get("external_case_payload_rendered") is not True:
            errors.append("payload_not_rendered")
        if payload.get("connector_call_performed") is not False:
            errors.append("payload_connector_call_not_false")
        if payload.get("external_case_created") is not False:
            errors.append("payload_external_case_created_not_false")
        if "payload_ready_connector_call_not_performed" not in payload.get("adapter_warnings", []):
            errors.append("payload_warning_missing")

        rc, called = run_case(root, CALLED_CTX, "called")
        if rc != 0:
            errors.append("called_returncode_mismatch")
        if called.get("connector_call_performed") is not True:
            errors.append("called_connector_call_not_true")
        if called.get("external_case_created") is not True:
            errors.append("external_case_created_not_true")
        if called.get("outbound_delivery_performed") is not True:
            errors.append("outbound_delivery_not_true")
        if called.get("external_case_number") != 999:
            errors.append("external_case_number_mismatch")
        if called.get("external_case_url") != "https://github.com/itakura-hidetoshi/KuuOS/issues/999":
            errors.append("external_case_url_mismatch")
        if called.get("daemon_restart_performed") is not False:
            errors.append("daemon_restart_not_false")
        if called.get("world_update_performed") is not False:
            errors.append("world_update_not_false")
        if called.get("memory_write_performed") is not False:
            errors.append("memory_write_not_false")

        blocked_ctx = {**CALLED_CTX, "external_case_url": None}
        rc, blocked = run_case(root, blocked_ctx, "blocked")
        if rc != 1:
            errors.append("blocked_returncode_mismatch")
        if "external_case_url_missing" not in blocked.get("adapter_blockers", []):
            errors.append("external_case_url_blocker_missing")
        if blocked.get("external_case_created") is not False:
            errors.append("blocked_external_case_created_not_false")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi connector case adapter check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
