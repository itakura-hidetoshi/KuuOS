#!/usr/bin/env python3
"""v0.26 append-only finite Wa extrema-score stability source pins.

Inherits all selected predecessor references through v0.25. The six
immediate predecessor blobs must also match; all six new v0.26 source
paths and test declarations must be present. Static markers are not
Lean proofs or native program semantics.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_wa_finite_extrema_sources_v0_25 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "9dc7e05a8deb2852698abdaa260ce143f45f8c35"
SOURCE_BLOBS = {
    "formal/KuuOSFormal/WaFiniteExtremaV0_25.lean":
        "6af9ac53afbb351b6073edf203ce3f2038aac5e8",
    "runtime/kuuos_lean_python_wa_finite_extrema_v0_25.py":
        "d0cd9a3d601a892f0e5856f2aa6eb2f0ff4be01b",
    "scripts/check_kuuos_lean_python_wa_finite_extrema_sources_v0_25.py":
        "0ce947531021eb14122cb75d2e18ef59fd845fa0",
    "tests/lean_python_extensions/test_wa_finite_extrema_v0_25.py":
        "2084c3021912264f244dde5b338ab76178bc1981",
    "tests/lean_python_extensions/test_wa_finite_extrema_sources_v0_25.py":
        "24980e0ed99b8df8715126321114bc2626685e78",
    "docs/KUUOS_LEAN_PYTHON_WA_FINITE_EXTREMA_v0_25.md":
        "87b9c15b71f7ffb89c387a5f6372f374395a16d3",
}
REQUIRED_PATHS = (
    "formal/KuuOSFormal/WaExtremaStabilityV0_26.lean",
    "runtime/kuuos_lean_python_wa_extrema_stability_v0_26.py",
    "scripts/check_kuuos_lean_python_wa_extrema_stability_sources_v0_26.py",
    "tests/lean_python_extensions/test_wa_extrema_stability_v0_26.py",
    "tests/lean_python_extensions/test_wa_extrema_stability_sources_v0_26.py",
    "docs/KUUOS_LEAN_PYTHON_WA_EXTREMA_STABILITY_v0_26.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_wa_extrema_stability_v0_26.py":
        "WaExtremaStabilityTests",
    "tests/lean_python_extensions/test_wa_extrema_stability_sources_v0_26.py":
        "WaExtremaStabilitySourceTests",
}
_BASE = prior._BASE
PROOF_MARKERS = {
    "formal/KuuOSFormal/WaExtremaStabilityV0_26.lean": (
        b"theorem rational_ideal_weakest_nonexpansive",
        b"theorem rational_ideal_alert_nonexpansive",
        b"theorem rational_ideal_two_extrema_stability",
        b"theorem observed_wa_with_extrema_error",
        b"theorem native_normalized_wa_with_extrema_error",
        b"theorem native_normalized_wa_with_extrema_real",
    ),
}


def declared_test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not isinstance(root, Path):
        return {}
    output: dict[str, tuple[str, ...]] = {}
    for path, classname in TEST_CLASSES.items():
        raw, issue = _BASE._read_file(root, path)
        if issue:
            continue
        try:
            top = ast.parse(raw.decode("utf-8")).body
        except (SyntaxError, UnicodeError, ValueError, RecursionError):
            continue
        classes = [node for node in top
                   if isinstance(node, ast.ClassDef) and node.name == classname]
        if len(classes) != 1:
            continue
        names = [node.name for node in classes[0].body
                 if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
        if names and len(names) == len(set(names)):
            output[path.removesuffix(".py").replace("/", ".") + "." + classname] = (
                tuple(sorted(names))
            )
    return output


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    problems = list(prior.check_sources(root))
    for path, expected in SOURCE_BLOBS.items():
        raw, issue = _BASE._read_file(root, path)
        if issue:
            problems.append("v025_source_" + issue + ":" + path)
        elif _BASE._git_blob(raw) != expected:
            problems.append("source_byte_drift:" + path)
    for path in REQUIRED_PATHS:
        raw, issue = _BASE._read_file(root, path)
        if issue:
            problems.append("required_v026_file_" + issue + ":" + path)
        elif path in PROOF_MARKERS and not all(
                needle in raw for needle in PROOF_MARKERS[path]):
            problems.append("required_v026_proof_declaration_missing:" + path)
    inventory = declared_test_inventory(root)
    for path, name in TEST_CLASSES.items():
        key = path.removesuffix(".py").replace("/", ".") + "." + name
        if key not in inventory:
            problems.append("required_test_declarations_missing_or_invalid:" + key)
    return tuple(sorted(set(problems)))


def main() -> int:
    problems = check_sources()
    for problem in problems:
        print("BLOCKED:", problem)
    if not problems:
        print("STATIC_MATCH: 161 selected predecessor blob pins + 6 new v0.26 files")
        for k, v in sorted(declared_test_inventory().items()):
            print("DECLARED_TEST_CLASS:", k, "methods=" + str(len(v)))
        print("NOT_PROOF: only pinned Strict Lean compiler and audit certify theorems")
        print("NOT_SEMANTICS: counterfactual reference != native execution")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
