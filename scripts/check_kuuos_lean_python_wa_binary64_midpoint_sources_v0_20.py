#!/usr/bin/env python3
"""v0.20 predecessor source pins and declared test inventory, not a proof.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_wa_rational_shadow_sources_v0_19 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "73bba9d114c8f4fcdfe636ba46360f9e18b9977e"
SOURCE_BLOBS = {
    "formal/KuuOSFormal/WaRationalBridgeV0_19.lean": "892916746b0108d16630d7278bc3ae8d50c65cbf",
    "runtime/kuuos_lean_python_wa_rational_shadow_v0_19.py": "eaf4d4f1feddd4af1e1da503f8f340294e6b11a6",
    "scripts/check_kuuos_lean_python_wa_rational_shadow_sources_v0_19.py": "755f63bf31e9792701cfc2ddd937e9111a16370d",
    "tests/lean_python_extensions/test_wa_rational_shadow_v0_19.py": "61ad24df51e500cf44c8b5fc6c51c1d7dea7f1ce",
    "tests/lean_python_extensions/test_wa_rational_shadow_sources_v0_19.py": "b4942d58f051c83c2d3198b5cce35e4081dd0b8b",
    "docs/KUUOS_LEAN_PYTHON_WA_RATIONAL_SHADOW_v0_19.md": "7c179433b07c893faf32038738cc43527781f871",
}
REQUIRED_PATHS = (
    "formal/KuuOSFormal/WaGridRoundingV0_20.lean",
    "formal/KuuOSFormal/WaNeighborMidpointV0_20.lean",
    "runtime/kuuos_lean_python_wa_binary64_midpoint_v0_20.py",
    "scripts/check_kuuos_lean_python_wa_binary64_midpoint_sources_v0_20.py",
    "tests/lean_python_extensions/test_wa_binary64_midpoint_v0_20.py",
    "tests/lean_python_extensions/test_wa_binary64_midpoint_sources_v0_20.py",
    "docs/KUUOS_LEAN_PYTHON_WA_BINARY64_MIDPOINT_v0_20.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_wa_binary64_midpoint_v0_20.py": "WaBinary64MidpointTests",
    "tests/lean_python_extensions/test_wa_binary64_midpoint_sources_v0_20.py": "WaBinary64MidpointSourceTests",
}
_BASE = prior._BASE
PROOF_MARKERS = {
    "formal/KuuOSFormal/WaGridRoundingV0_20.lean": b"theorem gridRound_half_quantum",
    "formal/KuuOSFormal/WaNeighborMidpointV0_20.lean":
        b"theorem observed_neighbor_midpoint_error",
}


def declared_test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not isinstance(root, Path):
        return {}
    inventory = {}
    for relative, klass in TEST_CLASSES.items():
        raw, issue = _BASE._read_file(root, relative)
        if issue:
            continue
        try:
            nodes = ast.parse(raw.decode("utf-8")).body
        except (SyntaxError, UnicodeError, ValueError, RecursionError):
            continue
        classes = [node for node in nodes if isinstance(node, ast.ClassDef) and node.name == klass]
        if len(classes) != 1:
            continue
        methods = [node.name for node in classes[0].body
                   if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
        if methods and len(methods) == len(set(methods)):
            inventory[relative.removesuffix(".py").replace("/", ".") + "." + klass] = tuple(sorted(methods))
    return inventory


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    problems = list(prior.check_sources(root))
    for relative, sha in SOURCE_BLOBS.items():
        raw, issue = _BASE._read_file(root, relative)
        if issue:
            problems.append("source_" + issue + ":" + relative)
        elif _BASE._git_blob(raw) != sha:
            problems.append("source_byte_drift:" + relative)
    for relative in REQUIRED_PATHS:
        raw, issue = _BASE._read_file(root, relative)
        if issue:
            problems.append("required_v020_file_" + issue + ":" + relative)
        elif relative in PROOF_MARKERS and PROOF_MARKERS[relative] not in raw:
            problems.append("required_v020_proof_declaration_missing:" + relative)
    inventory = declared_test_inventory(root)
    for relative, klass in TEST_CLASSES.items():
        name = relative.removesuffix(".py").replace("/", ".") + "." + klass
        if name not in inventory:
            problems.append("required_test_declarations_missing_or_invalid:" + name)
    return tuple(sorted(set(problems)))


def main() -> int:
    problems = check_sources()
    for issue in problems:
        print("BLOCKED:", issue)
    if not problems:
        print("STATIC_MATCH: 124 selected historical blob pins + seven v0.20 paths")
        for name, methods in sorted(declared_test_inventory().items()):
            print("DECLARED_TEST_CLASS:", name, "methods=" + str(len(methods)))
        print("NOT_PROOF: exact pinned Lean elaboration and independent CI required")
        print("NOT_SEMANTICS: local Python observations do not prove arbitrary binary64")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
