#!/usr/bin/env python3
"""KuuOS v0.31 immutable proof/native source pins: MemoryOS + WORLD.

Inherits all v0.30 and earlier immutable source pins; verifies original
v0.35 MemoryOS snapshot/retrieval and v0.34 WORLD atomic commit sources
plus selected Lean theorem declarations. Marker existence is NOT proof
of compilation nor global Lean↔Python refinement.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path
from scripts import check_kuuos_lean_python_codeai_native_selection_sources_v0_30 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "6a7e44869d4f367cf3ffb41f75e495355d898424"

PINNED = {
    "runtime/kuuos_memoryos_qi_world_blocker_integration_v0_35.py":
        "b21c942e9a4f91cf6bacd707f691827e20949d11",
    "runtime/kuuos_authorized_atomic_world_commit_v0_34.py":
        "77a0bc864ee20c8138e4fc643c83e0faf236d874",
    "runtime/kuuos_authorized_atomic_world_commit_entry_v0_34.py":
        "6a3129e011546a5eb32a19de3f81f365f7a59801",
    "tests/test_memoryos_qi_world_blocker_integration_v0_35.py":
        "77d46dcea167ed3bcc82bbf3956b0f714156a54a",
    "tests/test_authorized_atomic_world_commit_v0_34.py":
        "2300ac20fee1ebe0515dfe397e2b7f5b1278ad72",
    "formal/KUOS/OpenHorizon/MemoryOSQiWorldBlockerIntegrationKernelV0_35.lean":
        "b566f668f7bfb8fa8d93f12c1996964d571a7012",
    "formal/KUOS/OpenHorizon/AuthorizedAtomicWorldCommitKernelV0_34.lean":
        "ed0a9932efb423eb22fbacca2b6536d5a014d67f",
    "runtime/kuuos_lean_python_memory_obligations_v0_27.py":
        "f4044ec31eda1dc96beea343841af706956addb2",
    "runtime/kuuos_lean_python_world_obligations_v0_27.py":
        "3f818827fe2f8c18ef8d7cd73ffc7496eefa2006",
    "runtime/kuuos_lean_python_codeai_native_selection_v0_30.py":
        "77de0caaafda172fbcc1cc163fb0d00bbd1b15f5",
    "scripts/check_kuuos_lean_python_codeai_native_selection_sources_v0_30.py":
        "af7af03f61cb1986b65306e5ff17e0a89a3598ed",
    "tests/lean_python_extensions/test_codeai_native_selection_v0_30.py":
        "56455eae6b85c66fddb16955855337caafd783ef",
}
NEW_FILES = (
    "runtime/kuuos_lean_python_memory_world_native_v0_31.py",
    "runtime/kuuos_lean_python_memory_native_binding_v0_31.py",
    "runtime/kuuos_lean_python_world_native_binding_v0_31.py",
    "scripts/check_kuuos_lean_python_memory_world_native_sources_v0_31.py",
    "tests/lean_python_extensions/test_memory_world_native_bindings_v0_31.py",
    "tests/lean_python_extensions/test_memory_world_native_sources_v0_31.py",
    "docs/KUUOS_LEAN_PYTHON_MEMORY_WORLD_NATIVE_v0_31.md",
)
ENTRYPOINTS = {
    "runtime/kuuos_lean_python_memory_native_binding_v0_31.py":
        "audit_native_memory_blocker",
    "runtime/kuuos_lean_python_world_native_binding_v0_31.py":
        "audit_original_world_commit",
}
TEST_CLASSES = {
    "tests/lean_python_extensions/test_memory_world_native_bindings_v0_31.py":
        "NativeMemoryWorldSourceBindingsTests",
    "tests/lean_python_extensions/test_memory_world_native_sources_v0_31.py":
        "NativeMemoryWorldNativeSourceTests",
}
THEOREMS = {
    "formal/KUOS/OpenHorizon/MemoryOSQiWorldBlockerIntegrationKernelV0_35.lean": (
        "memory_cannot_discharge_blocker",
        "memoryos_qi_world_blocker_integration_boundary",
    ),
    "formal/KUOS/OpenHorizon/AuthorizedAtomicWorldCommitKernelV0_34.lean": (
        "local_commit_authorization_does_not_shrink_open_horizon",
        "atomic_world_commit_preserves_history_and_root",
        "rollback_reference_is_not_automatic_history_deletion",
    ),
}


def inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    output = {}
    for path, cls in TEST_CLASSES.items():
        raw, error = prior._read(root, path)
        if error:
            continue
        try:
            ast_root = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, UnicodeError, ValueError, RecursionError):
            continue
        match = [c for c in ast_root.body
                 if isinstance(c, ast.ClassDef) and c.name == cls]
        if len(match) != 1:
            continue
        tests = tuple(sorted(c.name for c in match[0].body
                             if isinstance(c, ast.FunctionDef)
                             and c.name.startswith("test_")))
        if tests and len(set(tests)) == len(tests):
            output[path] = tests
    return output


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    failures = list(prior.check_sources(root))
    for path, expected in PINNED.items():
        raw, error = prior._read(root, path)
        if error:
            failures.append("original_pin_unavailable:" + path)
        elif prior._blob(raw) != expected:
            failures.append("original_pin_changed:" + path)
    for path in NEW_FILES:
        raw, error = prior._read(root, path)
        if error:
            failures.append("new_source_unavailable:" + path)
            continue
        if path.endswith(".py"):
            try:
                nodes = ast.parse(raw.decode("utf-8")).body
            except (SyntaxError, UnicodeError, ValueError, RecursionError):
                failures.append("new_python_syntax_invalid:" + path)
                continue
            if path in ENTRYPOINTS and ENTRYPOINTS[path] not in {
                    node.name for node in nodes if isinstance(node, ast.FunctionDef)}:
                failures.append("native_entrypoint_missing:" + path)
    for path, theorem_names in THEOREMS.items():
        raw, error = prior._read(root, path)
        if error:
            failures.append("original_lean_unavailable:" + path)
            continue
        text = raw.decode("utf-8")
        for name in theorem_names:
            if not re.search(r"^\s*theorem\s+" + re.escape(name) + r"\b",
                             text, flags=re.MULTILINE):
                failures.append("source_lean_theorem_missing:" + name)
    if set(inventory(root)) != set(TEST_CLASSES):
        failures.append("v031_test_class_missing")
    return tuple(sorted(set(failures)))


def main() -> int:
    errors = check_sources()
    for x in errors:
        print("BLOCKED:", x)
    if not errors:
        print("STATIC_MATCH: 12 original MemoryOS/WORLD/CodeAI source pins"
              " and all inherited v0.30 source pins, 2 native entrypoints")
        print("NOT_PROOF: native source-local predicates never entail Lean"
              " dependent proof construction or external issuer authenticity")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
