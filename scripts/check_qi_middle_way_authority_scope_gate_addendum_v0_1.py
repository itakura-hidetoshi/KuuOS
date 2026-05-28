#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_middle_way_authority_scope_gate_addendum_v0_1.json"


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
        "manifest_version": "qi_middle_way_authority_scope_gate_addendum_v0_1",
        "addendum_status": "QI_MIDDLE_WAY_AUTHORITY_SCOPE_GATE_ADDENDUM_READY",
        "extends_manifest": "manifests/qi_two_truths_authority_emergence_gate_addendum_v0_1.json",
        "authority": "none",
    }
    for key, expected in checks.items():
        if m.get(key) != expected:
            errors.append(f"{key}_mismatch")
    for key in ["middle_way_scope_only", "authority_scope_candidate_only", "execution_requires_separate_gate"]:
        if m.get(key) is not True:
            errors.append(f"{key}_not_true")
    for key in ["actual_probe_execution_authority", "probe_execution_performed", "memory_write_performed", "world_update_performed", "grants_probe_execution_authority"]:
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
    print("PASS: Qi middle-way authority scope gate addendum check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
