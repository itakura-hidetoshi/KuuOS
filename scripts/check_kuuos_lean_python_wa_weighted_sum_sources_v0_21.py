#!/usr/bin/env python3
"""v0.21 additive source-preservation and declared-test inventory.

Static checks are NOT Lean elaboration, source/issuer authentication, or
runtime proof. Preserve all original sources and fail closed on drift.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_wa_binary64_midpoint_sources_v0_20 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "3cad1cb96210ce88e9b7f1921c8dc7b9df198350"
SOURCE_BLOBS = {
    "formal/KuuOSFormal/WaGridRoundingV0_20.lean":
        "70aeb130f082cda6411a066704681db8eaa7d95a",
    "formal/KuuOSFormal/WaNeighborMidpointV0_20.lean":
        "69dcc280804ff400c29ce9ee32cb0fd31db342d5",
    "runtime/kuuos_lean_python_wa_binary64_midpoint_v0_20.py":
        "c58d49c10affe8c79a3239489c247c354d1f71c4",
    "scripts/check_kuuos_lean_python_wa_binary64_midpoint_sources_v0_20.py":
        "3eb6329c52218e1e1d32c1aca98188bcb358e677",
    "tests/lean_python_extensions/test_wa_binary64_midpoint_v0_20.py":
        "04b5bce3539a4ccb527d61fc2f1dc99edc0b0c56",
    "tests/lean_python_extensions/test_wa_binary64_midpoint_sources_v0_20.py":
        "0d320bdb2189c8482fa1fd7ed8faea8ea6ffd39c",
    "docs/KUUOS_LEAN_PYTHON_WA_BINARY64_MIDPOINT_v0_20.md":
        "7e02660de915e66a565ea86d02c455161e5b562a",
}
REQUIRED_PATHS = (
    "formal/KuuOSFormal/WaWeightedSumV0_21.lean",
    "runtime/kuuos_lean_python_wa_weighted_sum_certificate_v0_21.py",
    "scripts/check_kuuos_lean_python_wa_weighted_sum_sources_v0_21.py",
    "tests/lean_python_extensions/test_wa_weighted_sum_v0_21.py",
    "tests/lean_python_extensions/test_wa_weighted_sum_sources_v0_21.py",
    "docs/KUUOS_LEAN_PYTHON_WA_WEIGHTED_SUM_v0_21.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_wa_weighted_sum_v0_21.py":
        "WaWeightedSumTests",
    "tests/lean_python_extensions/test_wa_weighted_sum_sources_v0_21.py":
        "WaWeightedSumSourceTests",
}
_BASE = prior._BASE
PROOF_MARKERS = {
    "formal/KuuOSFormal/WaWeightedSumV0_21.lean":
        (b"theorem list_abs_sum_le_sum_abs", b"theorem weighted_sum_observed_real_error"),
}


def declared_test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not isinstance(root, Path):
        return {}
    result = {}
    for path, classname in TEST_CLASSES.items():
        raw, issue = _BASE._read_file(root, path)
        if issue:
            continue
        try:
            nodes = ast.parse(raw.decode("utf-8")).body
        except (UnicodeError, SyntaxError, ValueError, RecursionError):
            continue
        matches = [node for node in nodes
                   if isinstance(node, ast.ClassDef) and node.name == classname]
        if len(matches) != 1:
            continue
        test_names = [node.name for node in matches[0].body
                      if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
        if test_names and len(test_names) == len(set(test_names)):
            result[path.removesuffix(".py").replace("/", ".") + "." +
                   classname] = tuple(sorted(test_names))
    return result


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    issues = list(prior.check_sources(root))
    for path, sha in SOURCE_BLOBS.items():
        raw, problem = _BASE._read_file(root, path)
        if problem:
            issues.append("v020_source_" + problem + ":" + path)
        elif _BASE._git_blob(raw) != sha:
            issues.append("source_byte_drift:" + path)
    for path in REQUIRED_PATHS:
        raw, problem = _BASE._read_file(root, path)
        if problem:
            issues.append("required_v021_file_" + problem + ":" + path)
        elif path in PROOF_MARKERS and not all(
                marker in raw for marker in PROOF_MARKERS[path]):
            issues.append("required_v021_proof_declaration_missing:" + path)
    inventory = declared_test_inventory(root)
    for path, classname in TEST_CLASSES.items():
        identifier = path.removesuffix(".py").replace("/", ".") + "." + classname
        if identifier not in inventory:
            issues.append("required_test_declarations_missing_or_invalid:" + identifier)
    return tuple(sorted(set(issues)))


def main() -> int:
    errors = check_sources()
    for error in errors:
        print("BLOCKED:", error)
    if not errors:
        print("STATIC_MATCH: 131 selected predecessor blobs + 6 v0.21 files")
        for klass, methods in sorted(declared_test_inventory().items()):
            print("DECLARED_TEST_CLASS:", klass, "methods=" + str(len(methods)))
        print("NOT_PROOF: strict Lean elaboration and real test outcomes required")
        print("NOT_IEEE: input-specific observed error != all-input rounding semantics")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
