#!/usr/bin/env python3
"""v0.36 pins original Lean and native ObserveOS→VerifyOS source blobs.

Prior v0.35-and-earlier pins are mandatory. This checks byte-identical
original source and NEW Python-only tests, not independent issuer identity,
Lean/Python semantic refinement, global descent, or action authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_act_observe_store_sources_v0_35 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "269648c480cffd8f35d7cccdd0feaacf6ffb1e07"
PINNED = {
    "scripts/check_kuuos_lean_python_act_observe_store_sources_v0_35.py":
        "721eaa8aa09a1c61ed2e7268709ad2516af171cc",
    "runtime/kuuos_lean_python_act_observe_store_compat_v0_35.py":
        "71d3eeeb9cfb0a38e68afb71de87c4113179d17c",
    "runtime/kuuos_lean_python_verify_native_binding_v0_28.py":
        "7f7ea5b11134a64ba82b54e535427834072bbd00",
    "runtime/kuuos_lean_python_lineage_handoff_v0_2.py":
        "7cfa1037b4316fa7c646da0b2e678ac3231a0d4c",
    "runtime/kuuos_verify_os_store_v0_1.py":
        "6f08033b55fdde4d36cf2cb491da48cc4c40d00d",
    "runtime/kuuos_observe_os_store_v0_1.py":
        "7c6433b04fe83da4ac669a93d85f447591117897",
    "runtime/kuuos_verify_os_kernel_v0_1.py":
        "81a415d4eac83d0e828dca2a9e23a0dcfaedf4f0",
    "runtime/kuuos_verify_os_types_v0_1.py":
        "2889e0963f2171842e49ec477eec23e3a705eb6c",
    "runtime/kuuos_verify_os_fixture_v0_1.py":
        "3b7c326f913e212cab6450921f7834213eb265f7",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean":
        "cb022ee1b0d43d5a67f38f879cc7e06f60092f9c",
}
NEW = (
    "runtime/kuuos_lean_python_observe_verify_store_compat_v0_36.py",
    "scripts/check_kuuos_lean_python_observe_verify_store_sources_v0_36.py",
    "tests/lean_python_extensions/test_observe_verify_store_compat_v0_36.py",
    "tests/lean_python_extensions/test_observe_verify_store_sources_v0_36.py",
    "docs/KUUOS_LEAN_PYTHON_OBSERVE_VERIFY_STORE_COMPAT_v0_36.md",
)
CLASSES = {
    NEW[2]: "NativeObserveVerifyStoreCompatTests",
    NEW[3]: "NativeObserveVerifyStoreSourceTests",
}


def _read(root: Path, path: str):
    return prior._read(root, path)


def _blob(raw: bytes) -> str:
    return prior._blob(raw)


def test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    inventory = {}
    for path, cls in CLASSES.items():
        raw, problem = _read(root, path)
        if problem:
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            continue
        classes = [
            x for x in tree.body if isinstance(x, ast.ClassDef) and x.name == cls
        ]
        if len(classes) != 1:
            continue
        methods = [
            m.name for m in classes[0].body
            if isinstance(m, ast.FunctionDef) and m.name.startswith("test_")
        ]
        if len(methods) >= 5 and len(set(methods)) == len(methods):
            inventory[path] = tuple(sorted(methods))
    return inventory


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    issues = list(prior.check_sources(root))
    for path, expected in PINNED.items():
        raw, problem = _read(root, path)
        if problem:
            issues.append("v036_original_source_missing:" + path)
        elif _blob(raw) != expected:
            issues.append("v036_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            issues.append("v036_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            issues.append("v036_python_unparsable:" + path)
            continue
        if path == NEW[0] and not any(
            isinstance(x, ast.FunctionDef)
            and x.name == "audit_native_observe_verify_store_compatibility"
            for x in tree.body
        ):
            issues.append("v036_ObserveVerify_auditor_missing")
        if path in CLASSES and any(
            isinstance(x, ast.ImportFrom)
            and (x.module or "").startswith("tests.")
            and any(a.name.endswith(("Test", "Tests")) for a in x.names)
            for x in tree.body
        ):
            issues.append("v036_duplicate_testcase_import_forbidden:" + path)
    if set(test_inventory(root)) != set(CLASSES):
        issues.append("v036_test_inventory_incomplete")
    return tuple(sorted(set(issues)))


def main() -> int:
    failures = check_sources()
    for item in failures:
        print("BLOCKED:", item)
    if not failures:
        print("STATIC_MATCH: v0.36 eleven exact Lean/native source pins, inherited v0.35 checks")
        print("NOT_PROOF: verification != truth/causality/refinement/global descent/authority")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
