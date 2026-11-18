#!/usr/bin/env python3
"""Additive v0.18 source pins and declared-test inventory.

104 prior selected historical blobs remain checked, plus exact seven v0.17
blobs. AST declarations are not execution evidence or authority.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_decision_evidence_sources_v0_17 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "157841103706f31b884bb8d3d691c7cb3d4899c0"
SOURCE_BLOBS = {
    "docs/KUUOS_LEAN_PYTHON_DECISION_EVIDENCE_BOUNDARY_v0_17.md": "391448d044a3d615afec4b321da2dcebb96e1204",
    "runtime/kuuos_lean_python_decision_evidence_guard_v0_17.py": "8991d498cfc2075823ffc8c96c0843ca487a8b49",
    "runtime/kuuos_lean_python_decision_evidence_native_cycle_v0_17.py": "05786aa853050caaaefd99055257e81c7102959a",
    "scripts/check_kuuos_lean_python_decision_evidence_sources_v0_17.py": "c3476a8d4408f52a5300f814193e1416f2ce90cb",
    "tests/lean_python_extensions/test_decision_evidence_guard_v0_17.py": "7ff2c7147c060e5eec8a6e4ddc21f910b18b4918",
    "tests/lean_python_extensions/test_decision_evidence_native_cycle_v0_17.py": "5b24f1d2e94971aeebc4531c341221c5a5ca3d24",
    "tests/lean_python_extensions/test_decision_evidence_sources_v0_17.py": "5c586991239b04cc8de6fd9c9c15f81c951e3eb5",
}
REQUIRED_PATHS = (
    "runtime/kuuos_lean_python_belief_receipt_guard_v0_18.py",
    "runtime/kuuos_lean_python_belief_receipt_native_cycle_v0_18.py",
    "scripts/check_kuuos_lean_python_belief_receipt_sources_v0_18.py",
    "tests/lean_python_extensions/test_belief_receipt_guard_v0_18.py",
    "tests/lean_python_extensions/test_belief_receipt_native_cycle_v0_18.py",
    "tests/lean_python_extensions/test_belief_receipt_sources_v0_18.py",
    "docs/KUUOS_LEAN_PYTHON_BELIEF_RECEIPT_BOUNDARY_v0_18.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_belief_receipt_guard_v0_18.py": "BeliefReceiptGuardTests",
    "tests/lean_python_extensions/test_belief_receipt_native_cycle_v0_18.py": "BeliefReceiptNativeTests",
    "tests/lean_python_extensions/test_belief_receipt_sources_v0_18.py": "BeliefReceiptSourceTests",
}


def declared_test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not isinstance(root, Path):
        return {}
    inventory: dict[str, tuple[str, ...]] = {}
    for relative, klass in TEST_CLASSES.items():
        raw, issue = prior.prior.prior.prior._read_file(root, relative)
        if issue:
            continue
        try:
            nodes = ast.parse(raw.decode("utf-8")).body
        except (SyntaxError, UnicodeError, ValueError, RecursionError):
            continue
        matched = [node for node in nodes if isinstance(node, ast.ClassDef) and node.name == klass]
        if len(matched) != 1:
            continue
        methods = [node.name for node in matched[0].body
                   if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
        if methods and len(methods) == len(set(methods)):
            inventory[relative.removesuffix(".py").replace("/", ".") + "." + klass] = tuple(sorted(methods))
    return inventory


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    problems = list(prior.check_sources(root))
    for relative, blob_sha in SOURCE_BLOBS.items():
        raw, issue = prior.prior.prior.prior._read_file(root, relative)
        if issue:
            problems.append("source_" + issue + ":" + relative)
        elif prior.prior.prior.prior._git_blob(raw) != blob_sha:
            problems.append("source_byte_drift:" + relative)
    for relative in REQUIRED_PATHS:
        _, issue = prior.prior.prior.prior._read_file(root, relative)
        if issue:
            problems.append("required_v018_file_" + issue + ":" + relative)
    inventory = declared_test_inventory(root)
    for relative, klass in TEST_CLASSES.items():
        name = relative.removesuffix(".py").replace("/", ".") + "." + klass
        if name not in inventory:
            problems.append("required_test_declarations_missing_or_invalid:" + name)
    return tuple(sorted(set(problems)))


def main() -> int:
    issues = check_sources()
    for issue in issues:
        print("BLOCKED:", issue)
    if not issues:
        print("STATIC_MATCH: 111 selected previous Git blobs + 7 v0.18 regular files")
        for name, methods in sorted(declared_test_inventory().items()):
            print("DECLARED_TEST_CLASS:", name, "methods=" + str(len(methods)))
        print("DECLARATION_NOT_EXECUTION: independent CI actual test IDs required")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
