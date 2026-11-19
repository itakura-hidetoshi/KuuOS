#!/usr/bin/env python3
"""v0.39 original full-origin constructors, stores and inherited source pins.

Only six v0.39 files are added. All prior source pins remain binding.
Static matching is not a Lean proof, interpreter refinement or authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_five_store_chain_sources_v0_38 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "1930ef2bed45e8c577c21f62f4812546f5ab597e"
PINNED = {
    "scripts/check_kuuos_lean_python_five_store_chain_sources_v0_38.py":
        "f3c13bc7c58815960910ac7fb6ef477523458f7a",
    "runtime/kuuos_lean_python_wa_plan_local_compat_v0_33.py":
        "6226519045a29ad39670fc9efa5b6ef771869718",
    "runtime/kuuos_lean_python_act_observe_store_compat_v0_35.py":
        "71d3eeeb9cfb0a38e68afb71de87c4113179d17c",
    "runtime/kuuos_lean_python_decision_plan_handoff_v0_3.py":
        "139afc7671c6c2b15a1f8bb7fc76569a616af7e9",
    "runtime/kuuos_lean_python_os_path_composition_v0_6.py":
        "068158c2e4f90f5040f83504218e60752a5472ed",
    "runtime/kuuos_decision_os_wa_store_v0_3.py":
        "7cd55ee49358df4e1b4e048195b258fd7bdd612b",
    "runtime/kuuos_plan_os_store_v0_1.py":
        "106a4adae2750bc543786c1ff36cd746a4d838d4",
    "runtime/kuuos_decision_os_wa_state_v0_3.py":
        "b0e6ea237d14f3b41e7cd2caf9cc1813d0918734",
    "runtime/kuuos_plan_os_state_v0_1.py":
        "20ebe52c2d8696281968fb4870f1904c976dac37",
    "runtime/kuuos_decision_os_wa_kernel_v0_3.py":
        "0ebc222ac5c73da86fea8c4e09f03782f84314b3",
    "runtime/kuuos_plan_os_kernel_v0_1.py":
        "6942b32353b476fe8848d39c548d3cd2fe93ccff",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "runtime/kuuos_lean_python_wa_native_binding_v0_29.py":
        "46ae50df5561252db52477a6f750c14d6f25c691",
    "runtime/kuuos_lean_python_plan_native_binding_v0_28.py":
        "d5e422a7f7a8ed363d44705b8815156fb0dc9471",
    "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean":
        "4b6588305193fb8d41e1fef9c66433a8b5ea67e5",
    "formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean":
        "c278f21eb3459bef28df8f99c42e5f6cccedc22e",
    "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean":
        "0ff6a060bbe52bee4d4bcbe1ebbbd319689f5676",
}
NEW = (
    "runtime/kuuos_lean_python_wa_plan_store_compat_v0_39.py",
    "scripts/check_kuuos_lean_python_wa_plan_store_sources_v0_39.py",
    "tests/lean_python_extensions/test_wa_plan_store_compat_v0_39.py",
    "tests/lean_python_extensions/test_wa_plan_store_sources_v0_39.py",
    "docs/KUUOS_LEAN_PYTHON_WA_PLAN_STORE_COMPAT_v0_39.md",
    "docs/superpowers/plans/2026-11-20-wa-plan-store-compat-v0-39.md",
)
CLASSES = {
    NEW[2]: "NativeWaPlanStoreCompatibilityTests",
    NEW[3]: "NativeWaPlanStoreSourceTests",
}


def _read(root: Path, path: str):
    return prior._read(root, path)


def _blob(raw: bytes) -> str:
    return prior._blob(raw)


def _trusted_root(root: Path) -> bool:
    if type(root) is not type(Path()):
        return False
    try:
        absolute = root.absolute()
        if ".." in absolute.parts:
            return False
        if any(part.is_symlink() for part in (absolute, *absolute.parents)):
            return False
        absolute.resolve()
    except (OSError, ValueError, RuntimeError):
        return False
    return True


def test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not _trusted_root(root):
        return {}
    inventory: dict[str, tuple[str, ...]] = {}
    for path, class_name in CLASSES.items():
        raw, problem = _read(root, path)
        if problem:
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            continue
        found = [n for n in tree.body
                 if isinstance(n, ast.ClassDef) and n.name == class_name]
        if len(found) != 1:
            continue
        methods = [n.name for n in found[0].body
                   if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
        if len(methods) >= 5 and len(methods) == len(set(methods)):
            inventory[path] = tuple(sorted(methods))
    return inventory


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not _trusted_root(root):
        return ("root:trusted_path_required",)
    issues = list(prior.check_sources(root))
    for path, expected in PINNED.items():
        raw, problem = _read(root, path)
        if problem:
            issues.append("v039_original_source_missing:" + path)
        elif _blob(raw) != expected:
            issues.append("v039_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            issues.append("v039_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            issues.append("v039_python_unparsable:" + path)
            continue
        if path == NEW[0] and not any(
            isinstance(n, ast.FunctionDef)
            and n.name == "audit_native_wa_plan_store_compatibility"
            for n in tree.body
        ):
            issues.append("v039_native_store_auditor_missing")
        if path in CLASSES and any(
            isinstance(n, ast.ImportFrom)
            and (n.module or "").startswith("tests.")
            and any(alias.name.endswith(("Test", "Tests")) for alias in n.names)
            for n in tree.body
        ):
            issues.append("v039_duplicate_testcase_import_forbidden:" + path)
    if set(test_inventory(root)) != set(CLASSES):
        issues.append("v039_test_inventory_incomplete")
    return tuple(sorted(set(issues)))


def main() -> int:
    problems = check_sources()
    for problem in problems:
        print("BLOCKED:", problem)
    if not problems:
        print("STATIC_MATCH: v0.39 original Wa/Plan full-origin constructors and stores")
        print("STATIC_MATCH: seventeen original Git blobs and inherited v0.38 source pins")
        print("NOT_PROOF: local origin compatibility != global descent/refinement/authority")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
