#!/usr/bin/env python3
"""v0.22 predecessor source pins and additive validation inventory.

Static source declarations are evidence of source presence only, not
Lean proof, Python execution, CPython semantics, or external provenance.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_wa_weighted_sum_sources_v0_21 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "9304e28e8f8391f49a7989f3f04a84ed56231ef6"
SOURCE_BLOBS = {
    "formal/KuuOSFormal/WaWeightedSumV0_21.lean":
        "0e144c2ca4bc99322a88cb3705634b846694a762",
    "runtime/kuuos_lean_python_wa_weighted_sum_certificate_v0_21.py":
        "db49d4c5e1a3b68c386ad7b93c0e3a5b06d156c2",
    "scripts/check_kuuos_lean_python_wa_weighted_sum_sources_v0_21.py":
        "9f67d5f0c6ee09cc34681b11baf647f2078708e8",
    "tests/lean_python_extensions/test_wa_weighted_sum_v0_21.py":
        "6f60492789c64eefe4fc7e232239117ca4259dfd",
    "tests/lean_python_extensions/test_wa_weighted_sum_sources_v0_21.py":
        "e07291c1b0dcf87e15add2a08efa922566d7de4d",
    "docs/KUUOS_LEAN_PYTHON_WA_WEIGHTED_SUM_v0_21.md":
        "e152a3b65f70c090eb4064ee1efafff0eb9d5eb2",
}
REQUIRED_PATHS = (
    "formal/KuuOSFormal/WaNormalizationV0_22.lean",
    "runtime/kuuos_lean_python_wa_normalization_v0_22.py",
    "scripts/check_kuuos_lean_python_wa_normalization_sources_v0_22.py",
    "tests/lean_python_extensions/test_wa_normalization_v0_22.py",
    "tests/lean_python_extensions/test_wa_normalization_sources_v0_22.py",
    "docs/KUUOS_LEAN_PYTHON_WA_NORMALIZATION_v0_22.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_wa_normalization_v0_22.py":
        "WaNormalizationTests",
    "tests/lean_python_extensions/test_wa_normalization_sources_v0_22.py":
        "WaNormalizationSourceTests",
}
_BASE = prior._BASE
PROOF_MARKERS = {
    "formal/KuuOSFormal/WaNormalizationV0_22.lean": (
        b"theorem rational_normalization_shift_bound",
        b"theorem observed_native_tolerance_to_normalized_real",
    ),
}


def declared_test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not isinstance(root, Path):
        return {}
    result = {}
    for path, classname in TEST_CLASSES.items():
        raw, problem = _BASE._read_file(root, path)
        if problem:
            continue
        try:
            nodes = ast.parse(raw.decode("utf-8")).body
        except (SyntaxError, UnicodeError, ValueError, RecursionError):
            continue
        classes = [node for node in nodes
                   if isinstance(node, ast.ClassDef) and node.name == classname]
        if len(classes) != 1:
            continue
        methods = [node.name for node in classes[0].body
                   if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
        if methods and len(methods) == len(set(methods)):
            result[path.removesuffix(".py").replace("/", ".") + "." +
                   classname] = tuple(sorted(methods))
    return result


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    issues = list(prior.check_sources(root))
    for path, expected in SOURCE_BLOBS.items():
        raw, problem = _BASE._read_file(root, path)
        if problem:
            issues.append("v021_source_" + problem + ":" + path)
        elif _BASE._git_blob(raw) != expected:
            issues.append("source_byte_drift:" + path)
    for path in REQUIRED_PATHS:
        raw, problem = _BASE._read_file(root, path)
        if problem:
            issues.append("required_v022_file_" + problem + ":" + path)
        elif path in PROOF_MARKERS and not all(
                marker in raw for marker in PROOF_MARKERS[path]):
            issues.append("required_v022_proof_declaration_missing:" + path)
    inventory = declared_test_inventory(root)
    for path, classname in TEST_CLASSES.items():
        identifier = path.removesuffix(".py").replace("/", ".") + "." + classname
        if identifier not in inventory:
            issues.append("required_test_declarations_missing_or_invalid:" + identifier)
    return tuple(sorted(set(issues)))


def main() -> int:
    errors = check_sources()
    for issue in errors:
        print("BLOCKED:", issue)
    if not errors:
        print("STATIC_MATCH: 137 selected predecessor blob pins + 6 v0.22 paths")
        for name, tests in sorted(declared_test_inventory().items()):
            print("DECLARED_TEST_CLASS:", name, "methods=" + str(len(tests)))
        print("NOT_PROOF: exact pinned Lean compiler and actual Python test outcomes required")
        print("NOT_IEEE: 1e-9 Python comparison != exact convex sum theorem")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
