#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REMOVED_FILES = [
    "specs/kuuos_qi_meridian_os_bridge_v0_1.json",
    "scripts/validate_kuuos_qi_meridian_os_bridge_v0_1_min.py",
    ".github/workflows/kuuos_qi_naming_cleanup_validation.yml",
    "specs/kuuos_qi_sanjiao_os_bridge_v0_1.json",
    "scripts/validate_kuuos_qi_sanjiao_os_bridge_v0_1_min.py",
    ".github/workflows/kuuos_qi_naming_cleanup_validation.yml",
]
# Only scan active Qi runtime / total-field files. Historical PR titles or
# external docs are not part of the runtime path.
SCAN_FILES = [
    "specs/kuuos_qi_runtime_binding_os_bridge_v0_1.json",
    "specs/kuuos_qi_total_field_os_bridge_v0_1.json",
    "runtime/qi_runtime_binding_v0_1.py",
    "runtime/qi_cycle_runner_v0_1.py",
    "runtime/qi_total_field_v0_1.py",
    "tests/test_qi_runtime_binding_v0_1.py",
    "tests/test_qi_cycle_runner_v0_1.py",
    "tests/test_qi_total_field_v0_1.py",
]
FORBIDDEN = ["qi_meridian", "Qi Meridian", "meridian", "qi_sanjiao", "Qi Sanjiao", "sanjiao", "Sanjiao"]


def main() -> int:
    errors: list[str] = []
    for rel in REMOVED_FILES:
        if (ROOT / rel).exists():
            errors.append(f"removed naming-only Qi file still exists: {rel}")

    for rel in SCAN_FILES:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing active Qi runtime file: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN:
            if forbidden in text:
                errors.append(f"forbidden naming-only reference in {rel}: {forbidden}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: no Qi naming-only layers remain in active runtime path")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
