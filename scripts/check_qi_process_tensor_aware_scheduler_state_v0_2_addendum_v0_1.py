#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_process_tensor_aware_scheduler_state_v0_2_addendum_v0_1.json"


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
        "manifest_version": "qi_process_tensor_aware_scheduler_state_v0_2_addendum_v0_1",
        "addendum_status": "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_ADDENDUM_READY",
        "extends_manifest": "manifests/qi_probe_scheduler_proposal_reuse_addendum_v0_1.json",
        "authority": "scheduler_state",
        "scheduler_authority_scope": "scheduler_state_only",
    }
    for key, value in expected.items():
        if m.get(key) != value:
            errors.append(f"{key}_mismatch")
    for key in ["replay_reuse_integrated", "process_tensor_aware", "scheduler_state_updated", "scheduler_state_mutation_performed", "grants_scheduler_authority"]:
        if m.get(key) is not True:
            errors.append(f"{key}_not_true")
    for key in ["control_packet_mutation_performed", "probe_execution_performed", "memory_write_performed", "world_update_performed", "grants_probe_execution_authority", "grants_world_update_authority"]:
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
    print("PASS: Qi process tensor aware scheduler state v0.2 addendum check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
