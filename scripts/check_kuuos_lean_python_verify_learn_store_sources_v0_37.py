#!/usr/bin/env python3
"""v0.37: exact original Lean/native VerifyOS→LearnOS source pins.

Append-only source checks: inherit ALL v0.36-and-earlier pins, preserve
existing kernels/stores unchanged, require new Python tests and docs.
No assertion of Lean/Python semantic refinement, global descent,
external issuer authentication, truth, or execution authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_observe_verify_store_sources_v0_36 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "6672365b1bba5739d7fd1b30a250395647d46c89"
PINNED = {
    "scripts/check_kuuos_lean_python_observe_verify_store_sources_v0_36.py":
        "2046a3516ffd130e0dfbbd9c561972f6dc01b45a",
    "runtime/kuuos_lean_python_observe_verify_store_compat_v0_36.py":
        "5c17c5fcec5f7d066a53476923cbfc5aa4ee6d60",
    "runtime/kuuos_lean_python_learn_native_binding_v0_28.py":
        "e82fd3cc39c83838b9246b717f7a3086c365b2cf",
    "runtime/kuuos_lean_python_lineage_handoff_v0_2.py":
        "7cfa1037b4316fa7c646da0b2e678ac3231a0d4c",
    "runtime/kuuos_verify_os_store_v0_1.py":
        "6f08033b55fdde4d36cf2cb491da48cc4c40d00d",
    "runtime/kuuos_learn_os_store_v0_1.py":
        "1a462212f9488c2b3dc2ca2ec96efcd7a20e0713",
    "runtime/kuuos_learn_os_kernel_v0_1.py":
        "8eeaf80af8522df2dc99a1df546b3145aafa2612",
    "runtime/kuuos_learn_os_types_v0_1.py":
        "3e74b2e672064c435ff785e03ea85b8c6ab5f5eb",
    "runtime/kuuos_learn_os_fixture_v0_1.py":
        "b1e97bda4c4d27a01cbe882c2aafc1bae9bbe0b0",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean":
        "6dc7ba9d3bf1b4d12ca11e21560ab94d664e8097",
    "runtime/kuuos_verify_os_kernel_v0_1.py":
        "81a415d4eac83d0e828dca2a9e23a0dcfaedf4f0",
    "runtime/kuuos_verify_os_types_v0_1.py":
        "2889e0963f2171842e49ec477eec23e3a705eb6c",
    "runtime/v01_learn_os_future_only_evidence_learning.py":
        "7598baf82572c5d59b6ee915f07265904db9a895",
}
NEW = (
    "runtime/kuuos_lean_python_verify_learn_store_compat_v0_37.py",
    "scripts/check_kuuos_lean_python_verify_learn_store_sources_v0_37.py",
    "tests/lean_python_extensions/test_verify_learn_store_compat_v0_37.py",
    "tests/lean_python_extensions/test_verify_learn_store_sources_v0_37.py",
    "docs/KUUOS_LEAN_PYTHON_VERIFY_LEARN_STORE_COMPAT_v0_37.md",
)
CLASSES = {
    NEW[2]: "NativeVerifyLearnStoreCompatTests",
    NEW[3]: "NativeVerifyLearnStoreSourceTests",
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
        classes = [node for node in tree.body
                   if isinstance(node, ast.ClassDef) and node.name == cls]
        if len(classes) != 1:
            continue
        methods = [
            item.name for item in classes[0].body
            if isinstance(item, ast.FunctionDef) and item.name.startswith("test_")
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
            issues.append("v037_original_source_missing:" + path)
        elif _blob(raw) != expected:
            issues.append("v037_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            issues.append("v037_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            issues.append("v037_python_unparsable:" + path)
            continue
        if path == NEW[0] and not any(
            isinstance(node, ast.FunctionDef)
            and node.name == "audit_native_verify_learn_store_compatibility"
            for node in tree.body
        ):
            issues.append("v037_VerifyLearn_auditor_missing")
        if path in CLASSES and any(
            isinstance(node, ast.ImportFrom)
            and (node.module or "").startswith("tests.")
            and any(alias.name.endswith(("Test", "Tests")) for alias in node.names)
            for node in tree.body
        ):
            issues.append("v037_duplicate_testcase_import_forbidden:" + path)
    if set(test_inventory(root)) != set(CLASSES):
        issues.append("v037_test_inventory_incomplete")
    return tuple(sorted(set(issues)))


def main() -> int:
    failures = check_sources()
    for item in failures:
        print("BLOCKED:", item)
    if not failures:
        print("STATIC_MATCH: v0.37 fourteen original Lean/native pins and inherited v0.36")
        print("NOT_PROOF: learning != truth/authority/refinement/global descent")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
