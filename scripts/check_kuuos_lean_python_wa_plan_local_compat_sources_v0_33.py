#!/usr/bin/env python3
"""v0.33: append-only source-exact original Wa -> PlanOS local boundary.

Inherited v0.32/earlier Lean/native source pins stay active. The checked
Python source maps original local Lean data obligations; it is not a new
Lean proof, external replan attestation, or globally composable descent.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_memory_world_local_compat_sources_v0_32 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "cc5093e37adf01f7eec583b0a7ac4c99517d9368"
PINNED = {
    "scripts/check_kuuos_lean_python_memory_world_local_compat_sources_v0_32.py":
        "7836a8b705b2b43c9f00c690e7b5b4638a4c4d4a",
    "runtime/kuuos_lean_python_wa_native_binding_v0_29.py":
        "46ae50df5561252db52477a6f750c14d6f25c691",
    "runtime/kuuos_lean_python_plan_native_binding_v0_28.py":
        "d5e422a7f7a8ed363d44705b8815156fb0dc9471",
    "runtime/kuuos_lean_python_decision_plan_handoff_v0_3.py":
        "139afc7671c6c2b15a1f8bb7fc76569a616af7e9",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "runtime/kuuos_decision_os_wa_kernel_v0_3.py":
        "0ebc222ac5c73da86fea8c4e09f03782f84314b3",
    "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean":
        "0ff6a060bbe52bee4d4bcbe1ebbbd319689f5676",
    "formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean":
        "c278f21eb3459bef28df8f99c42e5f6cccedc22e",
}
NEW = (
    "runtime/kuuos_lean_python_wa_plan_local_compat_v0_33.py",
    "scripts/check_kuuos_lean_python_wa_plan_local_compat_sources_v0_33.py",
    "tests/lean_python_extensions/test_wa_plan_local_compat_v0_33.py",
    "tests/lean_python_extensions/test_wa_plan_local_compat_sources_v0_33.py",
    "docs/KUUOS_LEAN_PYTHON_WA_PLAN_LOCAL_COMPAT_v0_33.md",
)
CLASSES = {
    NEW[2]: "NativeWaPlanLocalCompatibilityTests",
    NEW[3]: "NativeWaPlanLocalCompatibilitySourceTests",
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
        tests = [m.name for m in classes[0].body
                 if isinstance(m, ast.FunctionDef) and m.name.startswith("test_")]
        if len(tests) >= 4 and len(tests) == len(set(tests)):
            inventory[path] = tuple(sorted(tests))
    return inventory


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    errors = list(prior.check_sources(root))
    for path, expected in PINNED.items():
        raw, problem = _read(root, path)
        if problem:
            errors.append("v033_original_source_missing:" + path)
        elif _blob(raw) != expected:
            errors.append("v033_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            errors.append("v033_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            errors.append("v033_python_unparsable:" + path)
            continue
        if path == NEW[0] and not any(
            isinstance(node, ast.FunctionDef)
            and node.name == "audit_native_wa_plan_local_compatibility"
            for node in tree.body
        ):
            errors.append("v033_native_wa_plan_entrypoint_missing")
        # Imported TestCase classes are re-discovered and duplicate IDs;
        # never import a prior fixture TestCase into either extension module.
        if path in CLASSES and any(
            isinstance(node, ast.ImportFrom)
            and (node.module or "").startswith("tests.")
            and any(alias.name.endswith(("Test", "Tests"))
                    for alias in node.names)
            for node in tree.body
        ):
            errors.append("v033_testcase_fixture_import_forbidden:" + path)
    if set(test_inventory(root)) != set(CLASSES):
        errors.append("v033_original_test_class_inventory_missing")
    return tuple(sorted(set(errors)))


def main() -> int:
    problems = check_sources()
    for issue in problems:
        print("BLOCKED:", issue)
    if not problems:
        print("STATIC_MATCH: v0.33 eight native/Lean source blobs + inherited v0.32 pins")
        print("NOT_PROOF: local Wa->Plan compatibility != Lean descent or authority")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
