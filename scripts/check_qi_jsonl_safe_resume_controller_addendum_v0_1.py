#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_jsonl_safe_resume_controller_addendum_v0_1.json"


def load(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main() -> int:
    errors: list[str] = []
    m = load(MANIFEST)
    if not m:
        errors.append("manifest_missing")
    expected = {
        "manifest_version": "qi_jsonl_safe_resume_controller_addendum_v0_1",
        "addendum_status": "QI_JSONL_SAFE_RESUME_CONTROLLER_ADDENDUM_READY",
        "extends_manifest": "manifests/qi_jsonl_persistent_daemon_wrapper_addendum_v0_1.json",
        "authority": "jsonl_safe_resume_controller_only",
    }
    for key, value in expected.items():
        if m.get(key) != value:
            errors.append(f"{key}_mismatch")
    for key in ["safe_resume_performed", "skip_processed_ticks", "no_op_resume_allowed", "jsonl_backend_required", "replay_cursor_monotone", "idempotency_enforced", "duplicate_tick_blocked", "token_ledger_checked", "memory_read_performed"]:
        if m.get(key) is not True:
            errors.append(f"{key}_not_true")
    for key in ["memory_write_performed", "memory_append_performed", "memory_overwrite_performed", "world_update_performed", "control_packet_mutation_performed", "probe_execution_performed", "grants_probe_execution_authority", "grants_world_update_authority", "grants_memory_overwrite_authority"]:
        if m.get(key) is not False:
            errors.append(f"{key}_not_false")
    for group in ["runtime_files", "script_files", "test_files"]:
        files = m.get(group, [])
        if not isinstance(files, list) or not files:
            errors.append(f"{group}_missing")
            continue
        for item in files:
            if not (ROOT / item).is_file():
                errors.append(f"missing_file:{item}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi JSONL safe resume controller addendum check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
