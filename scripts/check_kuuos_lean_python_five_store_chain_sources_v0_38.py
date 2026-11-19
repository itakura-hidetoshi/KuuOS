#!/usr/bin/env python3
"""v0.38 exact source inventory: five original persisted stores and four edges.

All v0.37-and-earlier Lean/native provenance pins are inherited.
Original Lean files, kernels, stores, and earlier adapters remain identical
by Git blob content. Only the v0.38 five new files may be added.
These checks do not certify interpreter refinement, issuer authenticity,
global descent, or exercise any execution authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_verify_learn_store_sources_v0_37 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "d0340d150312696b508595d9c24a864c0f7bae11"
PINNED = {
    "scripts/check_kuuos_lean_python_verify_learn_store_sources_v0_37.py":
        "76efcdae3e698da53f0fe9634489c7a8185f3e65",
    "runtime/kuuos_lean_python_plan_act_store_provenance_v0_34.py":
        "d6e52a321c8d99523f09b3d312638cf6ace25b6a",
    "runtime/kuuos_lean_python_act_observe_store_compat_v0_35.py":
        "71d3eeeb9cfb0a38e68afb71de87c4113179d17c",
    "runtime/kuuos_lean_python_observe_verify_store_compat_v0_36.py":
        "5c17c5fcec5f7d066a53476923cbfc5aa4ee6d60",
    "runtime/kuuos_lean_python_verify_learn_store_compat_v0_37.py":
        "1a64cb59b8467e2637347e7a9eeec22616f9c9d1",
    "runtime/kuuos_lean_python_os_path_composition_v0_6.py":
        "068158c2e4f90f5040f83504218e60752a5472ed",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "runtime/kuuos_plan_os_store_v0_1.py":
        "106a4adae2750bc543786c1ff36cd746a4d838d4",
    "runtime/kuuos_act_os_store_v0_1.py":
        "24ebc89667c493498926e8d03bb21f952f448cce",
    "runtime/kuuos_observe_os_store_v0_1.py":
        "7c6433b04fe83da4ac669a93d85f447591117897",
    "runtime/kuuos_verify_os_store_v0_1.py":
        "6f08033b55fdde4d36cf2cb491da48cc4c40d00d",
    "runtime/kuuos_learn_os_store_v0_1.py":
        "1a462212f9488c2b3dc2ca2ec96efcd7a20e0713",
    "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean":
        "0ff6a060bbe52bee4d4bcbe1ebbbd319689f5676",
    "formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean":
        "c08c8412d435553d9c2a20e309c7cdd4d649f360",
    "formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean":
        "0dccacb16696fc05a8c0f8d70bc09c34a50828f5",
    "formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean":
        "cb022ee1b0d43d5a67f38f879cc7e06f60092f9c",
    "formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean":
        "6dc7ba9d3bf1b4d12ca11e21560ab94d664e8097",
}
NEW = (
    "runtime/kuuos_lean_python_five_store_chain_compat_v0_38.py",
    "scripts/check_kuuos_lean_python_five_store_chain_sources_v0_38.py",
    "tests/lean_python_extensions/test_five_store_chain_compat_v0_38.py",
    "tests/lean_python_extensions/test_five_store_chain_sources_v0_38.py",
    "docs/KUUOS_LEAN_PYTHON_FIVE_STORE_CHAIN_COMPAT_v0_38.md",
)
CLASSES = {
    NEW[2]: "FiveOriginalStoreChainCompatTests",
    NEW[3]: "FiveOriginalStoreChainSourceTests",
}


def _read(root: Path, path: str):
    return prior._read(root, path)


def _blob(raw: bytes) -> str:
    return prior._blob(raw)


def test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    inventory: dict[str, tuple[str, ...]] = {}
    for path, cls in CLASSES.items():
        raw, problem = _read(root, path)
        if problem:
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            continue
        found = [node for node in tree.body
                 if isinstance(node, ast.ClassDef) and node.name == cls]
        if len(found) != 1:
            continue
        methods = [node.name for node in found[0].body
                   if isinstance(node, ast.FunctionDef)
                   and node.name.startswith("test_")]
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
            issues.append("v038_original_source_missing:" + path)
        elif _blob(raw) != expected:
            issues.append("v038_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            issues.append("v038_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            issues.append("v038_python_unparsable:" + path)
            continue
        if path == NEW[0] and not any(
            isinstance(node, ast.FunctionDef)
            and node.name == "audit_native_five_store_chain_compatibility"
            for node in tree.body
        ):
            issues.append("v038_five_store_auditor_missing")
        if path in CLASSES and any(
            isinstance(node, ast.ImportFrom)
            and (node.module or "").startswith("tests.")
            and any(alias.name.endswith(("Test", "Tests")) for alias in node.names)
            for node in tree.body
        ):
            issues.append("v038_duplicate_testcase_import_forbidden:" + path)
    if set(test_inventory(root)) != set(CLASSES):
        issues.append("v038_test_inventory_incomplete")
    return tuple(sorted(set(issues)))


def main() -> int:
    problems = check_sources()
    for issue in problems:
        print("BLOCKED:", issue)
    if not problems:
        print("STATIC_MATCH: v0.38 five original store kernels and typed adapters")
        print("STATIC_MATCH: seventeen original Lean/native Git blobs, all inherited pins")
        print("NOT_PROOF: local five-store path != formal descent/authority")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
