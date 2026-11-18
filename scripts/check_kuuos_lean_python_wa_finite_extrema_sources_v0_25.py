#!/usr/bin/env python3
"""v0.25 additive Wa finite-extrema source and test registration.

Inherits all 155 selected predecessor blob identities transitively.
New source marker presence is NOT pinned Lean theorem elaboration and
cannot be used to grant execution authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_wa_upper_clip_sources_v0_24 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "6a9ec01adfd67ea17822612ad1cb9fa50c4f82bc"
SOURCE_BLOBS = {
    "formal/KuuOSFormal/WaUpperClipV0_24.lean":
        "7c3efeb006a058271e71147d241b7b7d1f0ae610",
    "runtime/kuuos_lean_python_wa_upper_clip_v0_24.py":
        "354904caaa0d981689c9a58e5ef003cb48e9e67d",
    "scripts/check_kuuos_lean_python_wa_upper_clip_sources_v0_24.py":
        "cfb353713ba1d6227244ac0cf7cd2e30cea545d4",
    "tests/lean_python_extensions/test_wa_upper_clip_v0_24.py":
        "340cc8a0c3ade1107d00b774d2e1a80fa3658c1c",
    "tests/lean_python_extensions/test_wa_upper_clip_sources_v0_24.py":
        "3f37a4e2d7e21f5350a67d3b9979ffbec5437fa4",
    "docs/KUUOS_LEAN_PYTHON_WA_UPPER_CLIP_v0_24.md":
        "ebe5a52f11d045967aaab70e9ccb5d2e3eb6f474",
}
REQUIRED_PATHS = (
    "formal/KuuOSFormal/WaFiniteExtremaV0_25.lean",
    "runtime/kuuos_lean_python_wa_finite_extrema_v0_25.py",
    "scripts/check_kuuos_lean_python_wa_finite_extrema_sources_v0_25.py",
    "tests/lean_python_extensions/test_wa_finite_extrema_v0_25.py",
    "tests/lean_python_extensions/test_wa_finite_extrema_sources_v0_25.py",
    "docs/KUUOS_LEAN_PYTHON_WA_FINITE_EXTREMA_v0_25.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_wa_finite_extrema_v0_25.py":
        "WaFiniteExtremaTests",
    "tests/lean_python_extensions/test_wa_finite_extrema_sources_v0_25.py":
        "WaFiniteExtremaSourceTests",
}
_BASE = prior._BASE
PROOF_MARKERS = {
    "formal/KuuOSFormal/WaFiniteExtremaV0_25.lean": (
        b"theorem rational_min_unit",
        b"theorem rational_max_unit",
        b"theorem rational_finite_extrema_wa_ideal_in_unit",
        b"theorem observed_finite_extrema_ideal_identity",
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
        classes = [n for n in nodes
                   if isinstance(n, ast.ClassDef) and n.name == classname]
        if len(classes) != 1:
            continue
        tests = [n.name for n in classes[0].body
                 if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
        if tests and len(tests) == len(set(tests)):
            result[path.removesuffix(".py").replace("/", ".") + "." + classname] = (
                tuple(sorted(tests))
            )
    return result


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    problems = list(prior.check_sources(root))
    for path, sha in SOURCE_BLOBS.items():
        raw, issue = _BASE._read_file(root, path)
        if issue:
            problems.append("v024_source_" + issue + ":" + path)
        elif _BASE._git_blob(raw) != sha:
            problems.append("source_byte_drift:" + path)
    for path in REQUIRED_PATHS:
        raw, issue = _BASE._read_file(root, path)
        if issue:
            problems.append("required_v025_file_" + issue + ":" + path)
        elif path in PROOF_MARKERS and not all(
                mark in raw for mark in PROOF_MARKERS[path]):
            problems.append("required_v025_proof_declaration_missing:" + path)
    inventory = declared_test_inventory(root)
    for path, classname in TEST_CLASSES.items():
        name = path.removesuffix(".py").replace("/", ".") + "." + classname
        if name not in inventory:
            problems.append("required_test_declarations_missing_or_invalid:" + name)
    return tuple(sorted(set(problems)))


def main() -> int:
    problems = check_sources()
    for issue in problems:
        print("BLOCKED:", issue)
    if not problems:
        print("STATIC_MATCH: 155 selected predecessor blob pins + 6 new v0.25 paths")
        for name, methods in sorted(declared_test_inventory().items()):
            print("DECLARED_TEST_CLASS:", name, "methods=" + str(len(methods)))
        print("NOT_PROOF: compiler CI and exact-head Governance must independently succeed")
        print("NOT_SEMANTICS: finite rational witnesses != universal native min/max semantics")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
