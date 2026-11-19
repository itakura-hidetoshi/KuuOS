#!/usr/bin/env python3
"""Source-exact MemoryOS↔WORLD local compatibility v0.32 static inventory.

Inherits all v0.31/earlier original Lean and native source pins. No
new Lean compiler proof and no proof of global descent/gluing.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_memory_world_native_sources_v0_31 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_STAGE_PARENT = "5c072a1a914b2e1c7a0083866af87398b56e879a"
PINNED = {
    "runtime/kuuos_lean_python_memory_world_native_v0_31.py":
        "21a4511f7a00272eb43726360b33b24f270cf772",
    "runtime/kuuos_lean_python_memory_native_binding_v0_31.py":
        "39872e7092af48154ed6d21b265813c821f1858d",
    "runtime/kuuos_lean_python_world_native_binding_v0_31.py":
        "9b2b33999d69206947751f9e3a57430bae0fc05b",
    "scripts/check_kuuos_lean_python_memory_world_native_sources_v0_31.py":
        "441eb94f2544a6a29f71f6cbf5c2339cef264745",
    "tests/lean_python_extensions/test_memory_world_native_bindings_v0_31.py":
        "aa44d28ea2528a3ac95ff3ae794ef4b1af4054e8",
    "runtime/kuuos_memoryos_qi_world_blocker_integration_v0_35.py":
        "b21c942e9a4f91cf6bacd707f691827e20949d11",
    "runtime/kuuos_authorized_atomic_world_commit_entry_v0_34.py":
        "6a3129e011546a5eb32a19de3f81f365f7a59801",
    "formal/KUOS/OpenHorizon/MemoryOSQiWorldBlockerIntegrationKernelV0_35.lean":
        "b566f668f7bfb8fa8d93f12c1996964d571a7012",
    "formal/KUOS/OpenHorizon/AuthorizedAtomicWorldCommitKernelV0_34.lean":
        "ed0a9932efb423eb22fbacca2b6536d5a014d67f",
}
NEW = (
    "runtime/kuuos_lean_python_memory_world_local_compat_v0_32.py",
    "scripts/check_kuuos_lean_python_memory_world_local_compat_sources_v0_32.py",
    "tests/lean_python_extensions/test_memory_world_local_compat_v0_32.py",
    "tests/lean_python_extensions/test_memory_world_local_compat_sources_v0_32.py",
    "docs/KUUOS_LEAN_PYTHON_MEMORY_WORLD_LOCAL_COMPAT_v0_32.md",
)
CLASSES = {
    "tests/lean_python_extensions/test_memory_world_local_compat_v0_32.py":
        "NativeMemoryWorldLocalCompatibilityTests",
    "tests/lean_python_extensions/test_memory_world_local_compat_sources_v0_32.py":
        "NativeMemoryWorldCompatibilitySourceTests",
}


def _read(root: Path, path: str):
    return prior.prior._read(root, path)


def _blob(raw: bytes) -> str:
    return prior.prior._blob(raw)


def inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    output = {}
    for path, cls in CLASSES.items():
        raw, issue = _read(root, path)
        if issue:
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (ValueError, UnicodeError, SyntaxError, RecursionError):
            continue
        matches = [x for x in tree.body
                   if isinstance(x, ast.ClassDef) and x.name == cls]
        if len(matches) != 1:
            continue
        methods = tuple(sorted(x.name for x in matches[0].body
                               if isinstance(x, ast.FunctionDef)
                               and x.name.startswith("test_")))
        if methods and len(methods) == len(set(methods)):
            output[path] = methods
    return output


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    errors = list(prior.check_sources(root))
    for path, expected in PINNED.items():
        raw, problem = _read(root, path)
        if problem:
            errors.append("v032_original_source_missing:" + path)
        elif _blob(raw) != expected:
            errors.append("v032_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            errors.append("v032_new_file_missing:" + path)
        elif path.endswith(".py"):
            try:
                body = ast.parse(raw.decode("utf-8")).body
            except (ValueError, UnicodeError, SyntaxError, RecursionError):
                errors.append("v032_python_unparsable:" + path)
                continue
            if path == NEW[0] and not any(
                    isinstance(x, ast.FunctionDef)
                    and x.name == "audit_memory_world_compatibility"
                    for x in body):
                errors.append("v032_local_compatibility_entrypoint_missing")
    if set(inventory(root)) != set(CLASSES):
        errors.append("v032_test_classes_missing")
    return tuple(sorted(set(errors)))


def main() -> int:
    failures = check_sources()
    for item in failures:
        print("BLOCKED:", item)
    if not failures:
        print("STATIC_MATCH: nine exact originals + inherited v0.31"
              " proof/native blob pins; two new test classes")
        print("NOT_PROOF: local MemoryOS/WORLD source match does NOT certify"
              " global Lean gluing/descent or external authority")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
