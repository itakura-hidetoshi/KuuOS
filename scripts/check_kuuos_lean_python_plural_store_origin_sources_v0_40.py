#!/usr/bin/env python3
"""v0.40 original Plural store, constructor and Lean source inventory.

Retains all v0.39 and earlier exact Git source pins. This is a static source
binding test, NOT a Lean proof or global runtime semantic equivalence.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_wa_plan_store_sources_v0_39 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "aabd1f2d9be0405624c464eb437e5d8acac68a8e"
PINNED = {
    "scripts/check_kuuos_lean_python_wa_plan_store_sources_v0_39.py":
        "b8e2c414471b23ef23f0f6e0c850751051e75659",
    "runtime/kuuos_lean_python_wa_plan_store_compat_v0_39.py":
        "28f9039b3ac6f267e9ffb435a80294c9ad6ec945",
    "runtime/kuuos_decision_os_plural_store_v0_2.py":
        "45fb12e558c5ee6c442e4806022f2677c8ce777e",
    "runtime/kuuos_decision_os_plural_kernel_v0_2.py":
        "fd7a336640c5f25e6596be5ec29ec36ff7fce03d",
    "runtime/kuuos_decision_os_plural_types_v0_2.py":
        "2fa6dced94e4cf296ff8243c6101e343807385da",
    "runtime/kuuos_lean_python_plural_native_binding_v0_29.py":
        "71463793050f26ab7bb5be1f80589053dd6e8d5d",
    "runtime/kuuos_lean_python_os_path_composition_v0_6.py":
        "068158c2e4f90f5040f83504218e60752a5472ed",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean":
        "4b6588305193fb8d41e1fef9c66433a8b5ea67e5",
}
NEW = (
    "runtime/kuuos_lean_python_plural_store_origin_v0_40.py",
    "scripts/check_kuuos_lean_python_plural_store_origin_sources_v0_40.py",
    "tests/lean_python_extensions/test_plural_store_origin_v0_40.py",
    "tests/lean_python_extensions/test_plural_store_sources_v0_40.py",
    "docs/KUUOS_LEAN_PYTHON_PLURAL_STORE_ORIGIN_v0_40.md",
)
TEST_CLASSES = {
    NEW[2]: "NativePluralStoreOriginTests",
    NEW[3]: "NativePluralStoreOriginSourceTests",
}


def _read(root: Path, path: str):
    return prior._read(root, path)


def _blob(raw: bytes) -> str:
    return prior._blob(raw)


def test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not prior._trusted_root(root):
        return {}
    inventory: dict[str, tuple[str, ...]] = {}
    for path, class_name in TEST_CLASSES.items():
        raw, problem = _read(root, path)
        if problem:
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            continue
        classes = [n for n in tree.body
                   if isinstance(n, ast.ClassDef) and n.name == class_name]
        if len(classes) != 1:
            continue
        methods = [n.name for n in classes[0].body
                   if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
        if len(methods) >= 5 and len(methods) == len(set(methods)):
            inventory[path] = tuple(sorted(methods))
    return inventory


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not prior._trusted_root(root):
        return ("root:trusted_path_required",)
    issues = list(prior.check_sources(root))
    for path, expected in PINNED.items():
        raw, problem = _read(root, path)
        if problem:
            issues.append("v040_original_source_missing:" + path)
        elif _blob(raw) != expected:
            issues.append("v040_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            issues.append("v040_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            issues.append("v040_python_unparsable:" + path)
            continue
        if path == NEW[0] and not any(
            isinstance(n, ast.FunctionDef)
            and n.name == "audit_native_plural_store_origin"
            for n in tree.body
        ):
            issues.append("v040_native_plural_auditor_missing")
        if path in TEST_CLASSES and any(
            isinstance(n, ast.ImportFrom)
            and (n.module or "").startswith("tests.")
            and any(alias.name.endswith(("Test", "Tests")) for alias in n.names)
            for n in tree.body
        ):
            issues.append("v040_duplicate_testcase_import_forbidden:" + path)
    if set(test_inventory(root)) != set(TEST_CLASSES):
        issues.append("v040_test_inventory_incomplete")
    return tuple(sorted(set(issues)))


def main() -> int:
    issues = check_sources()
    for issue in issues:
        print("BLOCKED:", issue)
    if not issues:
        print("STATIC_MATCH: v0.40 Plural full-origin constructor and real store")
        print("STATIC_MATCH: 9 exact original Git blobs and all inherited source pins")
        print("NOT_PROOF: local source identity != Lean/Python refinement or authority")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
