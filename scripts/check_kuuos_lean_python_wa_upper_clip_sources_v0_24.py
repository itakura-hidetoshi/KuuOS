#!/usr/bin/env python3
"""v0.24 additive source pins and test registration; not formal certification.

All 149 selected predecessor references are inherited transitively. This
checker preserves the exact six v0.23 predecessor blobs and requires six
new additive files. Static source markers NEVER replace Lean elaboration.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_wa_normalized_score_sources_v0_23 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "3f754ac305366a2c69627512a44d8fb86a788fff"
SOURCE_BLOBS = {
    "formal/KuuOSFormal/WaNormalizedScoreV0_23.lean":
        "7d852af602d3e50d4634b4648aba097a54483483",
    "runtime/kuuos_lean_python_wa_normalized_score_v0_23.py":
        "36e768afd82ac2e7a779716c53dec97eb78a7db4",
    "scripts/check_kuuos_lean_python_wa_normalized_score_sources_v0_23.py":
        "768bcca3b9d7d97dd5e37c7ecf55f21c79f36d96",
    "tests/lean_python_extensions/test_wa_normalized_score_v0_23.py":
        "d134f54a621a6ed037716d420f55be604cd14884",
    "tests/lean_python_extensions/test_wa_normalized_score_sources_v0_23.py":
        "20ee769793d050efb21116bf369d8702fae9400f",
    "docs/KUUOS_LEAN_PYTHON_WA_NORMALIZED_SCORE_v0_23.md":
        "688c91878c15d330d3523172da595049b5f1f34e",
}
REQUIRED_PATHS = (
    "formal/KuuOSFormal/WaUpperClipV0_24.lean",
    "runtime/kuuos_lean_python_wa_upper_clip_v0_24.py",
    "scripts/check_kuuos_lean_python_wa_upper_clip_sources_v0_24.py",
    "tests/lean_python_extensions/test_wa_upper_clip_v0_24.py",
    "tests/lean_python_extensions/test_wa_upper_clip_sources_v0_24.py",
    "docs/KUUOS_LEAN_PYTHON_WA_UPPER_CLIP_v0_24.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_wa_upper_clip_v0_24.py":
        "WaUpperClipTests",
    "tests/lean_python_extensions/test_wa_upper_clip_sources_v0_24.py":
        "WaUpperClipSourceTests",
}
_BASE = prior._BASE
PROOF_MARKERS = {
    "formal/KuuOSFormal/WaUpperClipV0_24.lean": (
        b"theorem rational_normalized_wa_ideal_in_unit",
        b"theorem native_clipped_upper_final_wa_real",
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
            problems.append("v023_source_" + issue + ":" + path)
        elif _BASE._git_blob(raw) != expected:
            problems.append("source_byte_drift:" + path)
    for path in REQUIRED_PATHS:
        raw, issue = _BASE._read_file(root, path)
        if issue:
            problems.append("required_v024_file_" + issue + ":" + path)
        elif path in PROOF_MARKERS and not all(
                marker in raw for marker in PROOF_MARKERS[path]):
            problems.append("required_v024_proof_declaration_missing:" + path)
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
        print("STATIC_MATCH: 149 selected predecessor blob pins + 6 new v0.24 paths")
        for name, tests in sorted(declared_test_inventory().items()):
            print("DECLARED_TEST_CLASS:", name, "methods=" + str(len(tests)))
        print("NOT_PROOF: pinned Lean compiler and independent Runtime/Governance required")
        print("NOT_SEMANTICS: observed native min identity != universal CPython min semantics")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
