#!/usr/bin/env python3
"""v0.35 original ActOS→ObserveOS persisted native source pins.

All v0.34-and-earlier Lean/runtime pins remain active. Python-only,
no proof of global descent, issuer authenticity or authority.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_plan_act_store_sources_v0_34 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "b782f5a34607ff645e7bccb9d8934b38301517a1"
PINNED = {
    "scripts/check_kuuos_lean_python_plan_act_store_sources_v0_34.py":
        "f33b89b5bfc416f2b24e53ac96e3fc592803661e",
    "runtime/kuuos_lean_python_observe_native_binding_v0_28.py":
        "49c3a9ab79d623901c28f08c0f0d90b22efdb7d5",
    "runtime/kuuos_lean_python_lineage_handoff_v0_2.py":
        "7cfa1037b4316fa7c646da0b2e678ac3231a0d4c",
    "runtime/kuuos_act_os_store_v0_1.py":
        "24ebc89667c493498926e8d03bb21f952f448cce",
    "runtime/kuuos_observe_os_store_v0_1.py":
        "7c6433b04fe83da4ac669a93d85f447591117897",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean":
        "0dccacb16696fc05a8c0f8d70bc09c34a50828f5",
    "runtime/kuuos_observe_os_kernel_v0_1.py":
        "670b205f975149cacc3d6a82c3f27edcded8c4ca",
    "runtime/kuuos_act_os_kernel_v0_1.py":
        "db91d45cefd8982309f4a8d58e792f0df0c2c5d4",
}
NEW = (
    "runtime/kuuos_lean_python_act_observe_store_compat_v0_35.py",
    "scripts/check_kuuos_lean_python_act_observe_store_sources_v0_35.py",
    "tests/lean_python_extensions/test_act_observe_store_compat_v0_35.py",
    "tests/lean_python_extensions/test_act_observe_store_sources_v0_35.py",
    "docs/KUUOS_LEAN_PYTHON_ACT_OBSERVE_STORE_COMPAT_v0_35.md",
)
CLASSES = {
    NEW[2]: "NativeActObserveStoreCompatTests",
    NEW[3]: "NativeActObserveStoreSourceTests",
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
        classes = [x for x in tree.body
                   if isinstance(x, ast.ClassDef) and x.name == cls]
        if len(classes) != 1:
            continue
        methods = [m.name for m in classes[0].body
                   if isinstance(m, ast.FunctionDef) and m.name.startswith("test_")]
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
            issues.append("v035_original_source_missing:" + path)
        elif _blob(raw) != expected:
            issues.append("v035_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            issues.append("v035_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            issues.append("v035_python_unparsable:" + path)
            continue
        if path == NEW[0] and not any(
            isinstance(x, ast.FunctionDef)
            and x.name == "audit_native_act_observe_store_compatibility"
            for x in tree.body
        ):
            issues.append("v035_ActObserve_auditor_missing")
        if path in CLASSES and any(
            isinstance(x, ast.ImportFrom)
            and (x.module or "").startswith("tests.")
            and any(a.name.endswith(("Test", "Tests")) for a in x.names)
            for x in tree.body
        ):
            issues.append("v035_duplicate_testcase_import_forbidden:" + path)
    if set(test_inventory(root)) != set(CLASSES):
        issues.append("v035_test_inventory_incomplete")
    return tuple(sorted(set(issues)))


def main() -> int:
    failures = check_sources()
    for item in failures:
        print("BLOCKED:", item)
    if not failures:
        print("STATIC_MATCH: v0.35 nine exact original Lean/native blobs, inherited v0.34 pins")
        print("NOT_PROOF: observation != verification / truth / host execution / global descent")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
