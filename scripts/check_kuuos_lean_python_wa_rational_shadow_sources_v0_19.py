#!/usr/bin/env python3
"""v0.19 predecessor source pins and declared test inventory. No proof claims.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_belief_receipt_sources_v0_18 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "af8b47cc20d35e1a44b25df4917505a90a4a9709"
SOURCE_BLOBS = {
    "runtime/kuuos_lean_python_belief_receipt_guard_v0_18.py": "73921ba36ed3b608aac45c526fceae105568722e",
    "runtime/kuuos_lean_python_belief_receipt_native_cycle_v0_18.py": "1c62e02dd51391d93ad71e95d067588b6e595e44",
    "scripts/check_kuuos_lean_python_belief_receipt_sources_v0_18.py": "9843dd1bae73a7d168b3091ac6f47596d6be9b46",
    "tests/lean_python_extensions/test_belief_receipt_guard_v0_18.py": "5f9ae35bcc9a9af6084674996eb93ef937d1b495",
    "tests/lean_python_extensions/test_belief_receipt_native_cycle_v0_18.py": "88ac9ab5f2371967641ea2dc0090b176123b4c9e",
    "tests/lean_python_extensions/test_belief_receipt_sources_v0_18.py": "d07fb575cb2dfc6fde473b6d92195d337094b910",
    "docs/KUUOS_LEAN_PYTHON_BELIEF_RECEIPT_BOUNDARY_v0_18.md": "40f80ece3c44c525a85fdbf59df9da352f00b98e",
}
REQUIRED_PATHS = (
    "formal/KuuOSFormal/WaRationalBridgeV0_19.lean",
    "runtime/kuuos_lean_python_wa_rational_shadow_v0_19.py",
    "scripts/check_kuuos_lean_python_wa_rational_shadow_sources_v0_19.py",
    "tests/lean_python_extensions/test_wa_rational_shadow_v0_19.py",
    "tests/lean_python_extensions/test_wa_rational_shadow_sources_v0_19.py",
    "docs/KUUOS_LEAN_PYTHON_WA_RATIONAL_SHADOW_v0_19.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_wa_rational_shadow_v0_19.py": "WaRationalShadowTests",
    "tests/lean_python_extensions/test_wa_rational_shadow_sources_v0_19.py": "WaRationalShadowSourceTests",
}
_BASE = prior.prior.prior.prior.prior


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
        found = [item for item in nodes if isinstance(item, ast.ClassDef) and item.name == klass]
        if len(found) != 1:
            continue
        methods = [item.name for item in found[0].body
                   if isinstance(item, ast.FunctionDef) and item.name.startswith("test_")]
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
            problems.append("required_v019_file_" + issue + ":" + relative)
        elif relative.endswith(".lean") and (b"theorem rationalIdeal_cast" not in raw
                or b"theorem two_stage_score_error_bound" not in raw):
            problems.append("required_v019_proof_declarations_missing:" + relative)
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
        print("STATIC_MATCH: 118 selected historical blob pins + six v0.19 paths")
        for name, methods in sorted(declared_test_inventory().items()):
            print("DECLARED_TEST_CLASS:", name, "methods=" + str(len(methods)))
        print("NOT_PROOF: direct Lean elaboration and Strict Lean CI required")
        print("NOT_EXECUTION: actual test IDs and outcomes required")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
