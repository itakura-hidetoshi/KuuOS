#!/usr/bin/env python3
"""v0.17 selected original blob pins and AST declared test inventory.

AST declarations are NOT executions; terminal independent CI is mandatory.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_wa_profile_source_sources_v0_16 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "9e1ce34bdf5f52faac28d741aa34dddda91bcba5"
SOURCE_BLOBS = {
    "docs/KUUOS_LEAN_PYTHON_WA_PROFILE_SOURCE_BOUNDARY_v0_16.md": "facc65dd0b7717981da8cee7e4e633ce66d237cf",
    "runtime/kuuos_lean_python_wa_profile_source_guard_v0_16.py": "95e0cf34d88eafef09da399b8e7439188dfe0568",
    "runtime/kuuos_lean_python_wa_profile_source_native_cycle_v0_16.py": "8336b7a5aa7186dc3b16971aff5e27c042b90a06",
    "scripts/check_kuuos_lean_python_wa_profile_source_sources_v0_16.py": "2b5dc20e6837a217325026d2ef1ee5cf0a16eb20",
    "tests/lean_python_extensions/test_wa_profile_source_guard_v0_16.py": "008712d9f25f36d0a6f25548560f655e455f4bae",
    "tests/lean_python_extensions/test_wa_profile_source_native_cycle_v0_16.py": "0d5aec0516b4cd834162e20f477aa8f1010bfaff",
    "tests/lean_python_extensions/test_wa_profile_source_sources_v0_16.py": "d2accfb187a9c3dbc913721bc0e5b1c4b414736d",
}
REQUIRED_PATHS = (
    "runtime/kuuos_lean_python_decision_evidence_guard_v0_17.py",
    "runtime/kuuos_lean_python_decision_evidence_native_cycle_v0_17.py",
    "scripts/check_kuuos_lean_python_decision_evidence_sources_v0_17.py",
    "tests/lean_python_extensions/test_decision_evidence_guard_v0_17.py",
    "tests/lean_python_extensions/test_decision_evidence_native_cycle_v0_17.py",
    "tests/lean_python_extensions/test_decision_evidence_sources_v0_17.py",
    "docs/KUUOS_LEAN_PYTHON_DECISION_EVIDENCE_BOUNDARY_v0_17.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_decision_evidence_guard_v0_17.py": "DecisionEvidenceGuardTests",
    "tests/lean_python_extensions/test_decision_evidence_native_cycle_v0_17.py": "DecisionEvidenceNativeCycleTests",
    "tests/lean_python_extensions/test_decision_evidence_sources_v0_17.py": "DecisionEvidenceSourceTests",
}


def declared_test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not isinstance(root, Path):
        return {}
    result = {}
    for relative, klass in TEST_CLASSES.items():
        raw, problem = prior.prior.prior._read_file(root, relative)
        if problem:
            continue
        try:
            body = ast.parse(raw.decode("utf-8")).body
        except (ValueError, SyntaxError, UnicodeError, RecursionError):
            continue
        classes = [node for node in body if isinstance(node, ast.ClassDef) and node.name == klass]
        if len(classes) != 1:
            continue
        methods = [node.name for node in classes[0].body
                   if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
        if methods and len(methods) == len(set(methods)):
            result[relative.removesuffix(".py").replace("/", ".") + "." + klass] = tuple(sorted(methods))
    return result


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    problems = list(prior.check_sources(root))
    for relative, sha in SOURCE_BLOBS.items():
        raw, problem = prior.prior.prior._read_file(root, relative)
        if problem:
            problems.append("source_" + problem + ":" + relative)
        elif prior.prior.prior._git_blob(raw) != sha:
            problems.append("source_byte_drift:" + relative)
    for relative in REQUIRED_PATHS:
        _, problem = prior.prior.prior._read_file(root, relative)
        if problem:
            problems.append("required_v017_file_" + problem + ":" + relative)
    inventory = declared_test_inventory(root)
    for relative, klass in TEST_CLASSES.items():
        key = relative.removesuffix(".py").replace("/", ".") + "." + klass
        if key not in inventory:
            problems.append("required_test_declarations_missing_or_invalid:" + key)
    return tuple(sorted(set(problems)))


def main() -> int:
    issues = check_sources()
    for issue in issues:
        print("BLOCKED:", issue)
    if not issues:
        print("STATIC_MATCH: 104 selected original Git blobs + 7 v0.17 regular files")
        for key, tests in sorted(declared_test_inventory().items()):
            print("DECLARED_TEST_CLASS:", key, "methods=" + str(len(tests)))
        print("DECLARATION_NOT_EXECUTION: independent CI must attest test IDs")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
