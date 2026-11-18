#!/usr/bin/env python3
"""Static source, original predecessor pins and declared tests for v0.16.

First check all 90 pinned historical blobs from v0.15; pin the seven
additional v0.15 files and check seven new v0.16 regular paths. Test AST
syntax is not evidence of execution and cannot replace independent CI.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_wa_evaluation_sources_v0_15 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "9bbd82a95a579a8091a1cb5d7e7f7b92eb254924"

SOURCE_BLOBS = {
    "docs/KUUOS_LEAN_PYTHON_WA_EVALUATION_BOUNDARY_v0_15.md": "0d44ef30c3dc834a1fa4ec1777edf733acf86096",
    "runtime/kuuos_lean_python_wa_evaluation_guard_v0_15.py": "114b86c0b76a5b38e90f2f88bb6913802cd91aa9",
    "runtime/kuuos_lean_python_wa_evaluation_native_cycle_v0_15.py": "f4821a4dfe0a58471e7ff7a7c73e9ce00e4ac077",
    "scripts/check_kuuos_lean_python_wa_evaluation_sources_v0_15.py": "a177ca66c14ee8c2a38165a6edc79c7782856675",
    "tests/lean_python_extensions/test_wa_evaluation_guard_v0_15.py": "8be6c942bf116ca1e31adffc22f76edd3dbb0d9d",
    "tests/lean_python_extensions/test_wa_evaluation_native_cycle_v0_15.py": "f96509bfadfd5e39f9c3f1827888cb8cf5874aaf",
    "tests/lean_python_extensions/test_wa_evaluation_sources_v0_15.py": "1da4e4fa861cec0fbe678e34c90dc742f16c1c92",
}

REQUIRED_PATHS = (
    "runtime/kuuos_lean_python_wa_profile_source_guard_v0_16.py",
    "runtime/kuuos_lean_python_wa_profile_source_native_cycle_v0_16.py",
    "scripts/check_kuuos_lean_python_wa_profile_source_sources_v0_16.py",
    "tests/lean_python_extensions/test_wa_profile_source_guard_v0_16.py",
    "tests/lean_python_extensions/test_wa_profile_source_native_cycle_v0_16.py",
    "tests/lean_python_extensions/test_wa_profile_source_sources_v0_16.py",
    "docs/KUUOS_LEAN_PYTHON_WA_PROFILE_SOURCE_BOUNDARY_v0_16.md",
)

TEST_CLASSES = {
    "tests/lean_python_extensions/test_wa_profile_source_guard_v0_16.py": "WaProfileSourceGuardTests",
    "tests/lean_python_extensions/test_wa_profile_source_native_cycle_v0_16.py": "WaProfileSourceNativeCycleTests",
    "tests/lean_python_extensions/test_wa_profile_source_sources_v0_16.py": "WaProfileSourceSourceTests",
}


def declared_test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not isinstance(root, Path):
        return {}
    inventory: dict[str, tuple[str, ...]] = {}
    for relative, klass in TEST_CLASSES.items():
        raw, issue = prior.prior._read_file(root, relative)
        if issue:
            continue
        try:
            body = ast.parse(raw.decode("utf-8")).body
        except (SyntaxError, UnicodeError, ValueError, RecursionError):
            continue
        classes = [node for node in body if isinstance(node, ast.ClassDef) and node.name == klass]
        if len(classes) != 1:
            continue
        tests = [node.name for node in classes[0].body
                 if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
        if tests and len(tests) == len(set(tests)):
            inventory[relative.removesuffix(".py").replace("/", ".") + "." + klass] = tuple(sorted(tests))
    return inventory


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    problems = list(prior.check_sources(root))
    for relative, expected in SOURCE_BLOBS.items():
        raw, issue = prior.prior._read_file(root, relative)
        if issue:
            problems.append("source_" + issue + ":" + relative)
        elif prior.prior._git_blob(raw) != expected:
            problems.append("source_byte_drift:" + relative)
    for relative in REQUIRED_PATHS:
        _, issue = prior.prior._read_file(root, relative)
        if issue:
            problems.append("required_v016_file_" + issue + ":" + relative)
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
        print("STATIC_MATCH: 97 pinned original Git blobs + 7 v0.16 regular files")
        for name, methods in sorted(declared_test_inventory().items()):
            print("DECLARED_TEST_CLASS:", name, "methods=" + str(len(methods)))
        print("DECLARATION_NOT_EXECUTION: actual GitHub test IDs/terminal results required")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
