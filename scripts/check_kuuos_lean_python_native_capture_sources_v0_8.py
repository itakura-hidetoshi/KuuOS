#!/usr/bin/env python3
"""Original builder/receipt source byte and mandatory v0.8 test-discovery guard.

This verifies selected source byte identity and the cumulative unittest import.
It does not run Lean or assert external receipt provenance.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_BLOBS = {
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "runtime/kuuos_decision_os_wa_kernel_v0_3.py":
        "0ebc222ac5c73da86fea8c4e09f03782f84314b3",
    "runtime/kuuos_plan_os_kernel_v0_1.py":
        "6942b32353b476fe8848d39c548d3cd2fe93ccff",
    "runtime/kuuos_decision_os_wa_types_v0_3.py":
        "9c1a67003adf61b340c3ff5a8266706fd3ea19d7",
    "runtime/kuuos_plan_os_types_v0_1.py":
        "fa3945092610c38d748342e0c7aba1c7cebf08dc",
    "runtime/kuuos_lean_python_native_cycle_ledger_replay_v0_7.py":
        "e1d4cdc5dd698b7c1aad1f2fcc3a9499a0eced49",
    "runtime/kuuos_act_os_store_v0_1.py":
        "24ebc89667c493498926e8d03bb21f952f448cce",
    "runtime/kuuos_lean_python_os_path_composition_v0_6.py":
        "068158c2e4f90f5040f83504218e60752a5472ed",
}
NEW_PATHS = (
    "runtime/kuuos_lean_python_native_cycle_receipt_capture_v0_8.py",
    "tests/test_kuuos_lean_python_native_cycle_receipt_capture_v0_8.py",
    "docs/KUUOS_LEAN_PYTHON_NATIVE_RECEIPT_CAPTURE_v0_8.md",
    "scripts/check_kuuos_lean_python_native_capture_sources_v0_8.py",
)
RUNNER_TEST = "tests/test_kuuos_lean_python_os_registry_v0_5.py"
MODULE = "tests.test_kuuos_lean_python_native_cycle_receipt_capture_v0_8"
REQUIRED_CLASSES = ("NativeCaptureV08Tests", "CaptureSourceV08Tests")


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    errors: list[str] = []
    for relative, expected in SOURCE_BLOBS.items():
        file = root / relative
        if not file.is_file():
            errors.append("source_missing:" + relative)
            continue
        raw = file.read_bytes()
        actual = hashlib.sha1(
            b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
        ).hexdigest()
        if actual != expected:
            errors.append("source_drift:" + relative)
    for relative in NEW_PATHS:
        if not (root / relative).is_file():
            errors.append("required_v08_file_missing:" + relative)

    file = root / RUNNER_TEST
    if not file.is_file():
        errors.append("cumulative_test_discovery_missing")
    else:
        try:
            syntax = ast.parse(file.read_text(encoding="utf-8"))
            imports = [
                node for node in syntax.body
                if isinstance(node, ast.ImportFrom) and node.module == MODULE
            ]
            if len(imports) != 1 or {
                alias.name for alias in imports[0].names
            } != set(REQUIRED_CLASSES):
                errors.append("cumulative_v08_native_tests_not_registered_exactly_once")
        except (OSError, UnicodeError, SyntaxError, ValueError):
            errors.append("cumulative_test_registration_unparseable")
    return tuple(sorted(set(errors)))


def main() -> int:
    problems = check_sources(ROOT)
    for problem in problems:
        print("BLOCKED:", problem)
    if not problems:
        print("STATIC_MATCH: 8 original source Git blobs and mandatory v0.8 "
              "native test discovery; NOT external provenance or Lean refinement")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
