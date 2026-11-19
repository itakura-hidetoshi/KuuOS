#!/usr/bin/env python3
"""v0.42 original Belief gerbe store and final receipt source provenance.

Retains all previous v0.41/v0.40/v0.39 source pins. This static check
does not itself execute the original kernel or prove Lean/Python refinement.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_decision_store_origin_sources_v0_41 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "0272779f97c0513f8922e8e1e4c3c645cfab3810"
PINNED = {
    "scripts/check_kuuos_lean_python_decision_store_origin_sources_v0_41.py":
        "43dfe70b00a6d8929251f445dc95527d5c9ef168",
    "runtime/kuuos_lean_python_decision_store_origin_v0_41.py":
        "4c262b0f8a0ac23de3367f162c8b50b95afa7cf8",
    "runtime/kuuos_belief_os_gerbe_store_v0_3.py":
        "9982c835c1f828ac608a038b24d66ed350c3af67",
    "runtime/kuuos_belief_os_gerbe_types_v0_3.py":
        "2b751413296450a38cd975e7680adc99d1f7a462",
    "runtime/kuuos_belief_os_gerbe_coherence_v0_3.py":
        "566d2f1b923093c4c1ca12f98506841062a8e6a2",
    "runtime/kuuos_lean_python_belief_receipt_guard_v0_18.py":
        "73921ba36ed3b608aac45c526fceae105568722e",
    "runtime/kuuos_lean_python_wa_plan_store_compat_v0_39.py":
        "28f9039b3ac6f267e9ffb435a80294c9ad6ec945",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "formal/KUOS/BeliefOS/ContextGerbeCoherenceV0_3.lean":
        "b4023e192f78ac10495c851ba68d63ee9fb22048",
}
NEW = (
    "runtime/kuuos_lean_python_belief_gerbe_store_origin_v0_42.py",
    "scripts/check_kuuos_lean_python_belief_gerbe_store_sources_v0_42.py",
    "tests/lean_python_extensions/test_belief_gerbe_store_origin_v0_42.py",
    "tests/lean_python_extensions/test_belief_gerbe_store_sources_v0_42.py",
    "docs/KUUOS_LEAN_PYTHON_BELIEF_GERBE_STORE_ORIGIN_v0_42.md",
)
TEST_CLASSES = {
    NEW[2]: "NativeBeliefGerbeStoreOriginTests",
    NEW[3]: "NativeBeliefGerbeStoreOriginSourceTests",
}


def _read(root: Path, path: str):
    return prior._read(root, path)


def _blob(raw: bytes) -> str:
    return prior._blob(raw)


def _trusted_root(root: Path) -> bool:
    return prior.prior.prior._trusted_root(root)


def test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not _trusted_root(root):
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
        classes = [n for n in tree.body
                   if isinstance(n, ast.ClassDef) and n.name == name]
        if len(classes) != 1:
            continue
        tests = [
            n.name for n in classes[0].body
            if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
        ]
        if len(tests) >= 5 and len(tests) == len(set(tests)):
            result[path] = tuple(sorted(tests))
    return result


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not _trusted_root(root):
        return ("root:trusted_path_required",)
    issues = list(prior.check_sources(root))
    for path, expected in PINNED.items():
        raw, problem = _read(root, path)
        if problem:
            issues.append("v042_original_source_missing:" + path)
        elif _blob(raw) != expected:
            issues.append("v042_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            issues.append("v042_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            issues.append("v042_python_unparsable:" + path)
            continue
        if path == NEW[0] and not any(
            isinstance(n, ast.FunctionDef)
            and n.name == "audit_native_belief_gerbe_store_origin"
            for n in tree.body
        ):
            issues.append("v042_belief_gerbe_auditor_missing")
        if path in TEST_CLASSES and any(
            isinstance(n, ast.ImportFrom)
            and (n.module or "").startswith("tests.")
            and any(alias.name.endswith(("Test", "Tests")) for alias in n.names)
            for n in tree.body
        ):
            issues.append("v042_duplicate_testcase_import_forbidden:" + path)
    if set(test_inventory(root)) != set(TEST_CLASSES):
        issues.append("v042_test_inventory_incomplete")
    return tuple(sorted(set(issues)))


def main() -> int:
    issues = check_sources()
    for issue in issues:
        print("BLOCKED:", issue)
    if not issues:
        print("STATIC_MATCH: v0.42 original Belief gerbe state/receipt sources")
        print("STATIC_MATCH: nine original Git blobs and all v0.41 earlier source pins")
        print("NOT_PROOF: local last receipt replay is not external issuer authenticity")
        print("NOT_PROOF: Belief numeric time and Decision genesis are not a common clock")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
