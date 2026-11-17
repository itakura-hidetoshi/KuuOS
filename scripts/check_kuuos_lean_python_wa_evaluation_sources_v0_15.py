#!/usr/bin/env python3
"""Pin 83 previous blobs plus seven v0.14 files; check v0.15 AST inventory.

Static source identity and method syntax cannot establish actual test
execution, historical provenance or theorem authority.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_wa_gate_sources_v0_14 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "69bd75f4ae14e912b45f520636ffd8a400067d36"
SOURCE_BLOBS = {
    "docs/KUUOS_LEAN_PYTHON_WA_GATE_BOUNDARY_v0_14.md": "c495a21693776c28bcb4fae81be6799a4ffa85eb",
    "runtime/kuuos_lean_python_wa_gate_guard_v0_14.py": "c0ff6ba0698df3e94b863dd8463336f537f2bf49",
    "runtime/kuuos_lean_python_wa_gate_native_cycle_v0_14.py": "a70ae594cb5ac9c32107b761aae839b837881957",
    "scripts/check_kuuos_lean_python_wa_gate_sources_v0_14.py": "161802df19c68bceb18e19f5b288878de83dbdf7",
    "tests/lean_python_extensions/test_wa_gate_guard_v0_14.py": "1f8b677444cf1e60db9303759af64225dd959688",
    "tests/lean_python_extensions/test_wa_gate_native_cycle_v0_14.py": "4e147ee380b0b06a84513d56d22b9f7f4e822b5d",
    "tests/lean_python_extensions/test_wa_gate_sources_v0_14.py": "1cac9359359ef343b855bfeee090d2becde3d865",
}
REQUIRED_PATHS = (
    "runtime/kuuos_lean_python_wa_evaluation_guard_v0_15.py",
    "runtime/kuuos_lean_python_wa_evaluation_native_cycle_v0_15.py",
    "scripts/check_kuuos_lean_python_wa_evaluation_sources_v0_15.py",
    "tests/lean_python_extensions/test_wa_evaluation_guard_v0_15.py",
    "tests/lean_python_extensions/test_wa_evaluation_native_cycle_v0_15.py",
    "tests/lean_python_extensions/test_wa_evaluation_sources_v0_15.py",
    "docs/KUUOS_LEAN_PYTHON_WA_EVALUATION_BOUNDARY_v0_15.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_wa_evaluation_guard_v0_15.py": "WaEvaluationGuardTests",
    "tests/lean_python_extensions/test_wa_evaluation_native_cycle_v0_15.py": "WaEvaluationNativeCycleTests",
    "tests/lean_python_extensions/test_wa_evaluation_sources_v0_15.py": "WaEvaluationSourceTests",
}


def declared_test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not isinstance(root, Path):
        return {}
    inventory = {}
    for relative, klass in TEST_CLASSES.items():
        raw, problem = prior._read_file(root, relative)
        if problem:
            continue
        try:
            body = ast.parse(raw.decode("utf-8")).body
        except (SyntaxError, UnicodeError, ValueError, RecursionError):
            continue
        matches = [node for node in body if isinstance(node, ast.ClassDef) and node.name == klass]
        if len(matches) != 1:
            continue
        methods = [node.name for node in matches[0].body
                   if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
        if methods and len(methods) == len(set(methods)):
            inventory[relative.removesuffix(".py").replace("/", ".") + "." + klass] = tuple(sorted(methods))
    return inventory


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    issues = list(prior.check_sources(root))
    for relative, expected in SOURCE_BLOBS.items():
        raw, problem = prior._read_file(root, relative)
        if problem:
            issues.append("source_" + problem + ":" + relative)
        elif prior._git_blob(raw) != expected:
            issues.append("source_byte_drift:" + relative)
    for relative in REQUIRED_PATHS:
        _, problem = prior._read_file(root, relative)
        if problem:
            issues.append("required_v015_file_" + problem + ":" + relative)
    inventory = declared_test_inventory(root)
    for relative, klass in TEST_CLASSES.items():
        name = relative.removesuffix(".py").replace("/", ".") + "." + klass
        if name not in inventory:
            issues.append("required_test_declarations_missing_or_invalid:" + name)
    return tuple(sorted(set(issues)))


def main() -> int:
    issues = check_sources()
    for issue in issues:
        print("BLOCKED:", issue)
    if not issues:
        print("STATIC_MATCH: 90 prerequisite Git blobs + seven new v0.15 files")
        for name, methods in sorted(declared_test_inventory().items()):
            print("DECLARED_TEST_CLASS:", name, "methods=" + str(len(methods)))
        print("DECLARATION_NE_EXECUTION: actual CI test IDs still required")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
