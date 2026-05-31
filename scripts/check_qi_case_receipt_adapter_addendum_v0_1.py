#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_case_receipt_adapter_addendum_v0_1.json"

REQUIRED_TRUE = [
    "approved_case_opener_enabled",
    "idempotency_key_required",
    "approval_receipt_required",
    "case_receipt_rendering_enabled",
    "approved_local_case_open_enabled",
]

REQUIRED_FALSE = [
    "external_api_call_performed",
    "outbound_delivery_performed",
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
    "runtime/kuuos_runtime_daemon_qi_approved_case_opener_adapter_v0_1.py",
    "scripts/run_qi_case_receipt_adapter_v0_1.py",
    "scripts/check_qi_case_receipt_adapter_v0_1.py",
    "scripts/check_qi_case_receipt_adapter_addendum_v0_1.py",
    "scripts/run_qi_case_receipt_adapter_checks_v0_1.py",
    "examples/qi_case_receipt_adapter_context_v0_1.json",
    "docs/qi_case_receipt_adapter_note_v0_1.md",
]


def main() -> int:
    errors: list[str] = []
    if not MANIFEST.is_file():
        errors.append("manifest_missing")
    else:
        value = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if value.get("addendum_status") != "QI_CASE_RECEIPT_ADAPTER_ADDENDUM_READY":
            errors.append("addendum_status_mismatch")
        if value.get("authority") != "approved_case_opener_adapter":
            errors.append("authority_mismatch")
        for key in REQUIRED_TRUE:
            if value.get(key) is not True:
                errors.append(f"{key}_not_true")
        for key in REQUIRED_FALSE:
            if value.get(key) is not False:
                errors.append(f"{key}_not_false")
        listed: list[str] = []
        for group in ("runtime_files", "script_files", "example_files", "docs_files"):
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
    print("PASS: Qi case receipt adapter addendum check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
