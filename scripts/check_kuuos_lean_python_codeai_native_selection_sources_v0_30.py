#!/usr/bin/env python3
"""Exact source CodeAI Lean-to-Python native selection evidence pins v0.30.

This adds no Lean declaration or original CodeAI mutation. It requires all
prior v0.29 exact-source pins and ten original CodeAI/Lean source blobs,
separately from the actual original runtime and independent CI execution.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
import ast
import re
from pathlib import Path

from scripts import check_kuuos_lean_python_native_decision_mediator_sources_v0_29 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "52691b7a98a289dc154950dfef097bef7ecb4fb4"
ORIGINAL_BLOBS = {
    "runtime/kuuos_codeai_evidence_weighted_selection_abstention_v0_1.py":
        "b85a3af39dfe3b5d514c8fd69d1570958fb465b7",
    "runtime/kuuos_codeai_evidence_weighted_selection_abstention_checks_v0_1.py":
        "2237e1f000fba8fe05729d53bf58337124491680",
    "runtime/kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1.py":
        "b8032df09338674aefa20730f5d3c9d795529364",
    "runtime/kuuos_codeai_candidate_static_admissibility_preflight_schema_v0_1.py":
        "ad745d535a39bc7dbd7c0b69eca16d8beb036c06",
    "runtime/kuuos_lean_python_codeai_obligations_v0_27.py":
        "d81584cbee43f50f4484ecbbf6fc0266266b4bf5",
    "runtime/kuuos_lean_python_contract_bridge_v0_1.py":
        "f6c3f570a996f9fc6c65f026b2fb001ae03c0097",
    "formal/KUOS/CodeAI/EvidenceWeightedSelectionAbstentionV0_1.lean":
        "eecfc1fe1efcac83c669d46edb693d3b833ba967",
    "scripts/check_kuuos_lean_python_native_decision_mediator_sources_v0_29.py":
        "d259d1bc045e5e27809f901afb44050083aa9ea4",
    "tests/test_kuuos_codeai_evidence_weighted_selection_abstention_v0_1.py":
        "bcefda9008953863de1c2de4c4316cee3dd35101",
    "scripts/build_codeai_evidence_weighted_selection_abstention_fixture_v0_1.py":
        "85699aa97585b590dd61cb6f1531e56aac0cf80e",
}
NEW_FILES = (
    "runtime/kuuos_lean_python_codeai_native_selection_v0_30.py",
    "scripts/check_kuuos_lean_python_codeai_native_selection_sources_v0_30.py",
    "tests/lean_python_extensions/test_codeai_native_selection_v0_30.py",
    "tests/lean_python_extensions/test_codeai_native_selection_sources_v0_30.py",
    "docs/KUUOS_LEAN_PYTHON_CODEAI_NATIVE_SELECTION_v0_30.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_codeai_native_selection_v0_30.py":
        "NativeCodeAISelectionBindingsTests",
    "tests/lean_python_extensions/test_codeai_native_selection_sources_v0_30.py":
        "CodeAINativeSourceBindingTests",
}
THEOREMS = (
    "highScoreCannotOverrideInadmissible",
    "incompleteEvidenceCannotBecomeEligible",
    "Receipt.WellFormed.selectedCandidateEligible",
    "Receipt.WellFormed.scoreBoundary",
    "Receipt.WellFormed.abstentionIsNotRejection",
    "Receipt.WellFormed.downstreamAuthorityRemainsSeparate",
    "Receipt.WellFormed.effectBoundary",
)


def _read(root: Path, path: str) -> tuple[bytes | None, str | None]:
    return prior.previous.prior._read(root, path)


def _blob(data: bytes) -> str:
    return prior.previous.prior._blob(data)


def inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    result = {}
    for path, classname in TEST_CLASSES.items():
        raw, issue = _read(root, path)
        if issue:
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, UnicodeError, ValueError, RecursionError):
            continue
        matching = [c for c in tree.body
                    if isinstance(c, ast.ClassDef) and c.name == classname]
        if len(matching) != 1:
            continue
        methods = tuple(sorted(c.name for c in matching[0].body
                               if isinstance(c, ast.FunctionDef)
                               and c.name.startswith("test_")))
        if methods and len(set(methods)) == len(methods):
            result[path] = methods
    return result


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    issues = list(prior.check_sources(root))
    for path, exact in ORIGINAL_BLOBS.items():
        source, issue = _read(root, path)
        if issue:
            issues.append("v030_original_source_missing:" + path)
        elif _blob(source) != exact:
            issues.append("v030_original_source_drift:" + path)
    for path in NEW_FILES:
        source, problem = _read(root, path)
        if problem:
            issues.append("v030_new_source_missing:" + path)
            continue
        if path.endswith(".py"):
            try:
                defs = ast.parse(source.decode("utf-8")).body
            except (SyntaxError, UnicodeError, ValueError, RecursionError):
                issues.append("v030_new_python_not_parseable:" + path)
                continue
            if path == NEW_FILES[0] and not any(
                    isinstance(x, ast.FunctionDef)
                    and x.name == "audit_native_codeai_selection"
                    for x in defs):
                issues.append("v030_native_entrypoint_missing")
    proof_path = "formal/KUOS/CodeAI/EvidenceWeightedSelectionAbstentionV0_1.lean"
    proof, err = _read(root, proof_path)
    if err:
        issues.append("v030_theorem_source_missing")
    else:
        source = proof.decode("utf-8")
        for name in THEOREMS:
            if not re.search(r"^\s*theorem\s+" + re.escape(name) + r"\b",
                             source, flags=re.MULTILINE):
                issues.append("v030_lean_declaration_missing:" + name)
    contents = inventory(root)
    if set(contents) != set(TEST_CLASSES):
        issues.append("v030_new_test_class_missing")
    return tuple(sorted(set(issues)))


def main() -> int:
    problems = check_sources()
    for issue in problems:
        print("BLOCKED:", issue)
    if not problems:
        print("STATIC_MATCH: 10 pinned original CodeAI/Lean sources and"
              " all v0.29 pins, native CodeAI selection entrypoint and two"
              " new test classes")
        print("NOT_PROOF: interpreter refinement, independent attestation"
              " and host authority are not provided")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
