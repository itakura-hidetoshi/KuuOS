#!/usr/bin/env python3
"""v0.41 source pins for original Decision store and supplied Belief receipt.

Inherits all v0.40 and earlier source pins unchanged. Source consistency is
not a Lean theorem, formal Python refinement or external issuer authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_plural_store_origin_sources_v0_40 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "7d9396aa06ccb59f0b2359406ed58ba12d169aad"
PINNED = {
    "runtime/kuuos_lean_python_plural_store_origin_v0_40.py":
        "2eab5ce9301edc58ac66123cd01f958365b4985c",
    "scripts/check_kuuos_lean_python_plural_store_origin_sources_v0_40.py":
        "69ebf66916bf4f6a6484dccf35bffc42683a1a80",
    "runtime/kuuos_decision_os_store_v0_1.py":
        "7ddcc08cc7f3d4a6e274ff0406805ef632457931",
    "runtime/kuuos_decision_os_state_v0_1.py":
        "80ea719c2a77fb30cef488fe5f9f1f9ae597991a",
    "runtime/kuuos_decision_os_kernel_v0_1.py":
        "7fbe347c0ae22f7efea0cb0147f1e1934ee743d4",
    "runtime/kuuos_decision_os_types_v0_1.py":
        "7a8432fad3eca3d04ac14e17cc4178833fd3c9aa",
    "runtime/kuuos_belief_os_gerbe_types_v0_3.py":
        "2b751413296450a38cd975e7680adc99d1f7a462",
    "formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean":
        "9891ab2aa20c8d2ea4df08abe3bf12d99aad6726",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "runtime/kuuos_lean_python_os_path_composition_v0_6.py":
        "068158c2e4f90f5040f83504218e60752a5472ed",
}
NEW = (
    "runtime/kuuos_lean_python_decision_store_origin_v0_41.py",
    "scripts/check_kuuos_lean_python_decision_store_origin_sources_v0_41.py",
    "tests/lean_python_extensions/test_decision_store_origin_v0_41.py",
    "tests/lean_python_extensions/test_decision_store_sources_v0_41.py",
    "docs/KUUOS_LEAN_PYTHON_DECISION_STORE_ORIGIN_v0_41.md",
)
TEST_CLASSES = {
    NEW[2]: "NativeDecisionStoreOriginTests",
    NEW[3]: "NativeDecisionStoreOriginSourceTests",
}


def _read(root: Path, path: str):
    return prior._read(root, path)


def _blob(raw: bytes) -> str:
    return prior._blob(raw)


def test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not prior.prior._trusted_root(root):
        return {}
    result: dict[str, tuple[str, ...]] = {}
    for path, name in TEST_CLASSES.items():
        raw, problem = _read(root, path)
        if problem:
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            continue
        classes = [
            n for n in tree.body
            if isinstance(n, ast.ClassDef) and n.name == name
        ]
        if len(classes) != 1:
            continue
        methods = [
            n.name for n in classes[0].body
            if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
        ]
        if len(methods) >= 5 and len(methods) == len(set(methods)):
            result[path] = tuple(sorted(methods))
    return result


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not prior.prior._trusted_root(root):
        return ("root:trusted_path_required",)
    issues = list(prior.check_sources(root))
    for path, expected in PINNED.items():
        raw, problem = _read(root, path)
        if problem:
            issues.append("v041_original_source_missing:" + path)
        elif _blob(raw) != expected:
            issues.append("v041_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            issues.append("v041_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            issues.append("v041_python_unparsable:" + path)
            continue
        if path == NEW[0] and not any(
            isinstance(n, ast.FunctionDef)
            and n.name == "audit_native_decision_store_origin"
            for n in tree.body
        ):
            issues.append("v041_original_decision_auditor_missing")
        if path in TEST_CLASSES and any(
            isinstance(n, ast.ImportFrom)
            and (n.module or "").startswith("tests.")
            and any(alias.name.endswith(("Test", "Tests")) for alias in n.names)
            for n in tree.body
        ):
            issues.append("v041_duplicate_testcase_import_forbidden:" + path)
    if set(test_inventory(root)) != set(TEST_CLASSES):
        issues.append("v041_test_inventory_incomplete")
    return tuple(sorted(set(issues)))


def main() -> int:
    issues = check_sources()
    for issue in issues:
        print("BLOCKED:", issue)
    if not issues:
        print("STATIC_MATCH: v0.41 original DecisionOS full-origin source pins")
        print("STATIC_MATCH: Belief receipt and prior v0.40/v0.39 Lean source continuity")
        print("NOT_PROOF: self-consistent receipt != external issuer authenticity")
        print("NOT_PROOF: numeric timestamp order != common source clock")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
