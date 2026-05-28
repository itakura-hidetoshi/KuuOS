#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_one_shot_probe_executor_addendum_v0_1.json"


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
        "manifest_version": "qi_one_shot_probe_executor_addendum_v0_1",
        "addendum_status": "QI_ONE_SHOT_PROBE_EXECUTOR_ADDENDUM_READY",
        "extends_manifest": "manifests/qi_limited_one_shot_execution_authority_grant_gate_addendum_v0_1.json",
        "authority": "none",
        "consumes_authority_token_kind": "single_use_probe_execution_authority",
    }
    for key, value in expected.items():
        if m.get(key) != value:
            errors.append(f"{key}_mismatch")
    for key in ["probe_execution_performed", "probe_result_artifact_only", "one_shot_token_consumed", "single_probe_only", "rollback_required", "reentry_window_bound"]:
        if m.get(key) is not True:
            errors.append(f"{key}_not_true")
    for key in ["token_reuse_allowed", "grants_probe_execution_authority", "grants_execution_authority", "memory_write_allowed", "world_update_allowed", "control_packet_mutation_allowed", "memory_write_performed", "world_update_performed", "control_packet_mutation_performed"]:
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
    print("PASS: Qi one-shot probe executor addendum check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
