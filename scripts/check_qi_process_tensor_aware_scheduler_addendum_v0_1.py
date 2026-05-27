#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_process_tensor_aware_scheduler_addendum_v0_1.json"


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
    if m.get("manifest_version") != "qi_process_tensor_aware_scheduler_addendum_v0_1":
        errors.append("manifest_version_mismatch")
    if m.get("addendum_status") != "QI_PROCESS_TENSOR_AWARE_SCHEDULER_ADDENDUM_READY":
        errors.append("addendum_status_mismatch")
    if m.get("authority") != "scheduler_state":
        errors.append("authority_not_scheduler_state")
    if m.get("grants_scheduler_authority") is not True:
        errors.append("grants_scheduler_authority_not_true")
    if m.get("scheduler_authority_scope") != "scheduler_state_only":
        errors.append("scheduler_authority_scope_mismatch")
    if m.get("process_tensor_aware") is not True:
        errors.append("process_tensor_aware_not_true")
    required_metrics = {
        "history_depth",
        "observation_debt_resolution_priority",
        "safe_reentry_window_score",
        "nonmarkov_link_density",
        "memory_kernel_preservation_score",
    }
    if not required_metrics.issubset(set(m.get("uses_process_tensor_metrics", []))):
        errors.append("required_process_tensor_metrics_missing")
    for key in [
        "control_packet_mutation_performed",
        "probe_execution_performed",
        "memory_write_performed",
        "world_update_performed",
        "grants_execution_authority",
        "grants_probe_execution_authority",
        "grants_dry_run_execution_authority",
        "grants_next_tick_execution_authority",
        "grants_control_packet_authority",
        "grants_memory_overwrite_authority",
        "grants_world_update_authority",
    ]:
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
    print("PASS: Qi process tensor aware scheduler addendum check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
