#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_limited_one_shot_execution_authority_grant_gate_addendum_v0_1.json"


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
    checks = {
        "manifest_version": "qi_limited_one_shot_execution_authority_grant_gate_addendum_v0_1",
        "addendum_status": "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_ADDENDUM_READY",
        "extends_manifest": "manifests/qi_middle_way_authority_scope_gate_addendum_v0_1.json",
        "authority": "probe_execution_authority_grant",
    }
    for key, expected in checks.items():
        if m.get(key) != expected:
            errors.append(f"{key}_mismatch")
    for key in ["grants_probe_execution_authority", "grants_execution_authority", "one_shot", "single_probe_only", "rollback_required", "authority_expires_after_use", "authority_revocable"]:
        if m.get(key) is not True:
            errors.append(f"{key}_not_true")
    for key in ["memory_write_allowed", "world_update_allowed", "control_packet_mutation_allowed", "probe_execution_performed", "memory_write_performed", "world_update_performed", "grants_memory_overwrite_authority", "grants_world_update_authority"]:
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
    print("PASS: Qi limited one-shot execution-authority grant addendum check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
