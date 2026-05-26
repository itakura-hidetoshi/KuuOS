#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_dry_run_probe_simulator_addendum_v0_1.json"


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
    if m.get("manifest_version") != "qi_dry_run_probe_simulator_addendum_v0_1":
        errors.append("manifest_version_mismatch")
    if m.get("addendum_status") != "QI_DRY_RUN_PROBE_SIMULATOR_ADDENDUM_READY":
        errors.append("addendum_status_mismatch")
    if m.get("authority") != "none":
        errors.append("authority_not_none")
    for key in [
        "simulation_only",
        "dry_run_only",
    ]:
        if m.get(key) is not True:
            errors.append(f"{key}_not_true")
    for key in [
        "state_mutation_performed",
        "control_packet_mutation_performed",
        "memory_write_performed",
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
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: Qi dry-run probe simulator addendum check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
