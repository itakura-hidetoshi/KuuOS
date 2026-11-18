#!/usr/bin/env python3
"""v0.23 append-only predecessor byte pins and declared test inventory.

Static source presence is never Lean elaboration, Python runtime validation,
issuer authenticity or a grant of execution authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_wa_normalization_sources_v0_22 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "d0d62b0bf15fda60900532b245f4e1b23b3222cc"
SOURCE_BLOBS = {
    "formal/KuuOSFormal/WaNormalizationV0_22.lean":
        "5b69a60c593b0ffc4df5fd4a1140c645d3e915e8",
    "runtime/kuuos_lean_python_wa_normalization_v0_22.py":
        "ae2544ca25936fdea2dc2e75931024e14990770d",
    "scripts/check_kuuos_lean_python_wa_normalization_sources_v0_22.py":
        "2b84e9617ada207c951e3d9e8141e2e8c6d5216f",
    "tests/lean_python_extensions/test_wa_normalization_v0_22.py":
        "760ba42fedff956365067284e61e8d618fc3d319",
    "tests/lean_python_extensions/test_wa_normalization_sources_v0_22.py":
        "9f06e01b864103996eb51ae3fbdfe2915be089b5",
    "docs/KUUOS_LEAN_PYTHON_WA_NORMALIZATION_v0_22.md":
        "8fbb25332728c1a2fe2c0c52879fd3ad353861ca",
}
REQUIRED_PATHS = (
    "formal/KuuOSFormal/WaNormalizedScoreV0_23.lean",
    "runtime/kuuos_lean_python_wa_normalized_score_v0_23.py",
    "scripts/check_kuuos_lean_python_wa_normalized_score_sources_v0_23.py",
    "tests/lean_python_extensions/test_wa_normalized_score_v0_23.py",
    "tests/lean_python_extensions/test_wa_normalized_score_sources_v0_23.py",
    "docs/KUUOS_LEAN_PYTHON_WA_NORMALIZED_SCORE_v0_23.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_wa_normalized_score_v0_23.py":
        "WaNormalizedScoreTests",
    "tests/lean_python_extensions/test_wa_normalized_score_sources_v0_23.py":
        "WaNormalizedScoreSourceTests",
}
_BASE = prior._BASE
PROOF_MARKERS = {
    "formal/KuuOSFormal/WaNormalizedScoreV0_23.lean": (
        b"theorem rational_ideal_weighted_contraction",
        b"theorem certified_products_normalized_final_wa_real",
    ),
}


def declared_test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not isinstance(root, Path):
        return {}
    result: dict[str, tuple[str, ...]] = {}
    for path, classname in TEST_CLASSES.items():
        raw, issue = _BASE._read_file(root, path)
        if issue:
            continue
        try:
            nodes = ast.parse(raw.decode("utf-8")).body
        except (SyntaxError, UnicodeError, ValueError, RecursionError):
            continue
        classes = [node for node in nodes
                   if isinstance(node, ast.ClassDef) and node.name == classname]
        if len(classes) != 1:
            continue
        tests = [node.name for node in classes[0].body
                 if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
        if tests and len(tests) == len(set(tests)):
            result[path.removesuffix(".py").replace("/", ".") + "." + classname] = (
                tuple(sorted(tests))
            )
    return result


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    problems = list(prior.check_sources(root))
    for path, expected in SOURCE_BLOBS.items():
        raw, issue = _BASE._read_file(root, path)
        if issue:
            problems.append("v022_source_" + issue + ":" + path)
        elif _BASE._git_blob(raw) != expected:
            problems.append("source_byte_drift:" + path)
    for path in REQUIRED_PATHS:
        raw, issue = _BASE._read_file(root, path)
        if issue:
            problems.append("required_v023_file_" + issue + ":" + path)
        elif path in PROOF_MARKERS and not all(
                marker in raw for marker in PROOF_MARKERS[path]):
            problems.append("required_v023_proof_declaration_missing:" + path)
    inventory = declared_test_inventory(root)
    for path, classname in TEST_CLASSES.items():
        identifier = path.removesuffix(".py").replace("/", ".") + "." + classname
        if identifier not in inventory:
            problems.append("required_test_declarations_missing_or_invalid:" + identifier)
    return tuple(sorted(set(problems)))


def main() -> int:
    problems = check_sources()
    for issue in problems:
        print("BLOCKED:", issue)
    if not problems:
        print("STATIC_MATCH: 143 selected predecessor blob pins + 6 new v0.23 paths")
        for name, tests in sorted(declared_test_inventory().items()):
            print("DECLARED_TEST_CLASS:", name, "methods=" + str(len(tests)))
        print("NOT_PROOF: pinned Lean compiler and independent Runtime/Governance required")
        print("NOT_SEMANTICS: observed local Wa score bound != universal IEEE754 semantics")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
