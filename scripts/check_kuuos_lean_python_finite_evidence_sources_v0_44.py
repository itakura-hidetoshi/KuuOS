#!/usr/bin/env python3
"""v0.44 exact source pins, added finite-model Lean declarations and tests.

Static source identity does not prove Lean elaboration, Python/Lean runtime
refinement, issuer authenticity or execution authority. Independent Lean
Strict and cumulative Python CI remain required.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_middle_way_semantic_sources_v0_43 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "e14b193e8b4f735008c3d97fb6bca61671213130"
PINNED = {
    "formal/KUOS/Architecture/LeanPythonMiddleWaySemanticBridgeV0_43.lean":
        "538e59f2188f39bca2c24fe9739828a5ec1e8c51",
    "runtime/kuuos_lean_python_middle_way_semantic_bridge_v0_43.py":
        "c5367bf403e3e81d911ca5f794d45bb60bf05164",
    "scripts/check_kuuos_lean_python_middle_way_semantic_sources_v0_43.py":
        "37169cb26389ac4216602ca5bb1811690c062968",
    "formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean":
        "3ec65ab43ccd12fd62f62c3322838d52e4c92662",
}
NEW = (
    "formal/KUOS/Architecture/LeanPythonFiniteEvidenceWitnessV0_44.lean",
    "runtime/kuuos_lean_python_finite_evidence_witness_v0_44.py",
    "scripts/check_kuuos_lean_python_finite_evidence_sources_v0_44.py",
    "tests/lean_python_extensions/test_finite_evidence_witness_v0_44.py",
    "tests/lean_python_extensions/test_finite_evidence_sources_v0_44.py",
    "docs/KUUOS_LEAN_PYTHON_FINITE_EVIDENCE_WITNESS_v0_44.md",
)
TEST_CLASSES = {
    NEW[3]: "FiniteEvidenceWitnessTests",
    NEW[4]: "FiniteEvidenceSourceTests",
}
LEAN_DECLARATIONS = (
    "theorem encodeStatus_injective",
    "theorem encodedJoin_commutes",
    "theorem finiteTwoStageSimulation",
    "theorem encodedTwoStage_commutes",
    "theorem combineEvidence_assoc",
    "theorem pythonJoinModel_assoc_on_encoded",
    "theorem invalidPythonStatus_blocks",
    "theorem unknownPythonStatus_is_not_success",
    "theorem finiteCheckedWitness_grants_no_execution",
)
LEAN_DEFINITIONS = (
    "def encodeStatus",
    "def pythonJoinModel",
    "def finiteEvidenceSimulation",
    "def finiteIdentitySeam",
)
LEAN_IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonMiddleWaySemanticBridgeV0_43",
)
PYTHON_DEFINITIONS = (
    "audit_finite_status_table",
    "audit_native_finite_evidence_instance",
)


def _read(root: Path, path: str):
    return prior._read(root, path)


def _blob(raw: bytes) -> str:
    return prior._blob(raw)


def _trusted_root(root: Path) -> bool:
    return prior._trusted_root(root)


def test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not _trusted_root(root):
        return {}
    result: dict[str, tuple[str, ...]] = {}
    for path, name in TEST_CLASSES.items():
        raw, problem = _read(root, path)
        if problem:
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            continue
        classes = [
            n for n in tree.body
            if isinstance(n, ast.ClassDef) and n.name == name
        ]
        if len(classes) != 1:
            continue
        methods = [
            n.name for n in classes[0].body
            if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
        ]
        if len(methods) >= 5 and len(methods) == len(set(methods)):
            result[path] = tuple(sorted(methods))
    return result


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not _trusted_root(root):
        return ("root:trusted_path_required",)
    problems = list(prior.check_sources(root))
    for path, expected in PINNED.items():
        raw, problem = _read(root, path)
        if problem:
            problems.append("v044_original_source_missing:" + path)
        elif _blob(raw) != expected:
            problems.append("v044_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            problems.append("v044_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            problems.append("v044_python_unparsable:" + path)
            continue
        if path == NEW[1]:
            funcs = {n.name for n in tree.body
                     if isinstance(n, ast.FunctionDef)}
            if not set(PYTHON_DEFINITIONS).issubset(funcs):
                problems.append("v044_finite_runtime_audit_missing")
    raw, problem = _read(root, NEW[0])
    if not problem:
        try:
            lines = tuple(line.strip()
                          for line in raw.decode("utf-8").splitlines())
        except UnicodeError:
            problems.append("v044_lean_encoding_invalid")
        else:
            for name in LEAN_DECLARATIONS + LEAN_DEFINITIONS:
                if not any(line == name or line.startswith(name + " ")
                           or line.startswith(name + ":") for line in lines):
                    problems.append("v044_lean_declaration_missing:" + name)
            for name in LEAN_IMPORTS:
                if name not in lines:
                    problems.append("v044_lean_import_missing:" + name)
            if any(line.startswith(("sorry", "admit", "axiom "))
                   for line in lines):
                problems.append("v044_unproved_lean_source")
    if set(test_inventory(root)) != set(TEST_CLASSES):
        problems.append("v044_test_inventory_incomplete")
    return tuple(sorted(set(problems)))


def main() -> int:
    failures = check_sources()
    for item in failures:
        print("BLOCKED:", item)
    if not failures:
        print("STATIC_MATCH: v0.44 three-valued finite-model Lean/Python source pins")
        print("STATIC_MATCH: inherited v0.43/v0.42/v0.41 earlier sources")
        print("NOT_PROOF: static Lean text is not Lean kernel certification")
        print("NOT_PROOF: exhaustive finite model != universal Python/Lean refinement")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
