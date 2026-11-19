#!/usr/bin/env python3
"""v0.34: original Plan→Act persisted-native source and Lean pins.

Append-only inheritance of v0.33 and earlier source checker chain.
No new Lean proofs, execution licensing, or broad descent claim.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_wa_plan_local_compat_sources_v0_33 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "6f4e3b5f89ef7090839c76ffabdf409ee12adbf7"
PINNED = {
    "scripts/check_kuuos_lean_python_wa_plan_local_compat_sources_v0_33.py":
        "f5cb287bf3bb687633c49d1ecc25da5bf6d6dd40",
    "runtime/kuuos_lean_python_plan_act_admission_v0_4.py":
        "8461d905eb22a45958a3cfe459b4e995eacf1585",
    "runtime/kuuos_lean_python_act_native_binding_v0_28.py":
        "4b4835ff83290ebae442edd2bea229119f01405e",
    "runtime/kuuos_lean_python_plan_native_binding_v0_28.py":
        "d5e422a7f7a8ed363d44705b8815156fb0dc9471",
    "runtime/kuuos_act_os_store_v0_1.py":
        "24ebc89667c493498926e8d03bb21f952f448cce",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "runtime/kuuos_plan_os_kernel_v0_1.py":
        "6942b32353b476fe8848d39c548d3cd2fe93ccff",
    "runtime/kuuos_act_os_kernel_v0_1.py":
        "db91d45cefd8982309f4a8d58e792f0df0c2c5d4",
    "formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean":
        "c08c8412d435553d9c2a20e309c7cdd4d649f360",
    "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean":
        "0ff6a060bbe52bee4d4bcbe1ebbbd319689f5676",
}
NEW = (
    "runtime/kuuos_lean_python_plan_act_store_provenance_v0_34.py",
    "scripts/check_kuuos_lean_python_plan_act_store_sources_v0_34.py",
    "tests/lean_python_extensions/test_plan_act_store_provenance_v0_34.py",
    "tests/lean_python_extensions/test_plan_act_store_sources_v0_34.py",
    "docs/KUUOS_LEAN_PYTHON_PLAN_ACT_STORE_PROVENANCE_v0_34.md",
)
CLASSES = {
    NEW[2]: "NativePlanActStoreProvenanceTests",
    NEW[3]: "NativePlanActStoreSourceTests",
}


def _read(root: Path, path: str):
    return prior._read(root, path)


def _blob(raw: bytes):
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
        classes = [x for x in tree.body
                   if isinstance(x, ast.ClassDef) and x.name == cls]
        if len(classes) != 1:
            continue
        methods = [m.name for m in classes[0].body
                   if isinstance(m, ast.FunctionDef) and m.name.startswith("test_")]
        if len(methods) >= 8 and len(methods) == len(set(methods)):
            inventory[path] = tuple(sorted(methods))
    return inventory


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    errors = list(prior.check_sources(root))
    for path, expected in PINNED.items():
        raw, issue = _read(root, path)
        if issue:
            errors.append("v034_original_source_missing:" + path)
        elif _blob(raw) != expected:
            errors.append("v034_original_source_changed:" + path)
    for path in NEW:
        raw, issue = _read(root, path)
        if issue:
            errors.append("v034_new_file_missing:" + path)
            continue
        if path.endswith(".py"):
            try:
                tree = ast.parse(raw.decode("utf-8"))
            except (SyntaxError, ValueError, UnicodeError, RecursionError):
                errors.append("v034_python_unparsable:" + path)
                continue
            if path == NEW[0] and not any(
                isinstance(x, ast.FunctionDef)
                and x.name == "audit_native_plan_act_store_compatibility"
                for x in tree.body
            ):
                errors.append("v034_plan_act_store_entrypoint_missing")
            if path in CLASSES and any(
                isinstance(x, ast.ImportFrom) and (x.module or "").startswith("tests.")
                and any(item.name.endswith(("Test", "Tests")) for item in x.names)
                for x in tree.body
            ):
                errors.append("v034_fixture_testcase_import_forbidden:" + path)
    if set(test_inventory(root)) != set(CLASSES):
        errors.append("v034_test_class_inventory_missing")
    return tuple(sorted(set(errors)))


def main() -> int:
    issues = check_sources()
    for issue in issues:
        print("BLOCKED:", issue)
    if not issues:
        print("STATIC_MATCH: ten exact original Lean/native blobs; inherited v0.33 pins")
        print("NOT_PROOF: original ActStore replay != numeric Lean jobs/slices or external authenticity")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
