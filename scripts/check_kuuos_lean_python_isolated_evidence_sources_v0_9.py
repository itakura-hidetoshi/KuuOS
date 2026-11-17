#!/usr/bin/env python3
"""Exact original-source pins and cumulative v0.9 test registration guard.

This does NOT certify external receipt signatures, provenance, Lean
elaboration or Lean/Python semantic refinement.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_BLOBS = {
    "runtime/kuuos_lean_python_native_cycle_receipt_capture_v0_8.py":
        "219ace2ec190cd8bf91284d413914afa4c696aef",
    "runtime/kuuos_lean_python_native_cycle_ledger_replay_v0_7.py":
        "e1d4cdc5dd698b7c1aad1f2fcc3a9499a0eced49",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "runtime/kuuos_act_os_store_v0_1.py":
        "24ebc89667c493498926e8d03bb21f952f448cce",
    "runtime/kuuos_lean_python_os_path_composition_v0_6.py":
        "068158c2e4f90f5040f83504218e60752a5472ed",
    "runtime/kuuos_lean_python_os_registry_v0_5.py":
        "7bb5e7cf2e0fea1a14029a00301708604510b371",
    "scripts/check_kuuos_lean_python_native_capture_sources_v0_8.py":
        "94ff7a78ab5163aec22c7c88714dadcc3bd3970b",
}
REQUIRED_PATHS = (
    "runtime/kuuos_lean_python_isolated_native_receipt_evidence_v0_9.py",
    "tests/test_kuuos_lean_python_isolated_native_evidence_v0_9.py",
    "scripts/check_kuuos_lean_python_isolated_evidence_sources_v0_9.py",
    "docs/KUUOS_LEAN_PYTHON_ISOLATED_NATIVE_EVIDENCE_v0_9.md",
)
REGISTERED_TEST_PATH = "tests/test_kuuos_lean_python_os_registry_v0_5.py"
REGISTERED_MODULE = "tests.test_kuuos_lean_python_isolated_native_evidence_v0_9"
TEST_CLASSES = frozenset(("IsolatedNativeEvidenceTests", "EvidenceSourcePinTests"))


def check_sources(root: Path = ROOT, *, check_registration: bool = True) -> tuple[str, ...]:
    issues: list[str] = []
    for relative, expected in SOURCE_BLOBS.items():
        source = root / relative
        if not source.is_file():
            issues.append("source_missing:" + relative)
            continue
        try:
            raw = source.read_bytes()
            actual = hashlib.sha1(
                b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
            ).hexdigest()
        except OSError:
            issues.append("source_unreadable:" + relative)
            continue
        if actual != expected:
            issues.append("source_byte_drift:" + relative)
    for relative in REQUIRED_PATHS:
        if not (root / relative).is_file():
            issues.append("required_v09_file_missing:" + relative)
    if check_registration:
        testfile = root / REGISTERED_TEST_PATH
        if not testfile.is_file():
            issues.append("cumulative_test_module_missing")
        else:
            try:
                body = ast.parse(testfile.read_text(encoding="utf-8")).body
                found = [
                    node for node in body
                    if isinstance(node, ast.ImportFrom)
                    and node.module == REGISTERED_MODULE
                ]
                if len(found) != 1 or frozenset(
                    alias.name for alias in found[0].names
                ) != TEST_CLASSES:
                    issues.append("native_tests_not_registered")
            except (OSError, SyntaxError, UnicodeError):
                issues.append("cumulative_test_registration_invalid")
    return tuple(sorted(set(issues)))


def main() -> int:
    errors = check_sources()
    for error in errors:
        print("BLOCKED:", error)
    if not errors:
        print(
            "STATIC_MATCH: 7 prior exact Git blobs, all v0.9 files and "
            "mandatory cumulative native test discovery; "
            "no external provenance or formal refinement"
        )
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
