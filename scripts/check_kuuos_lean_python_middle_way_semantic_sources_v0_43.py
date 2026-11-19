#!/usr/bin/env python3
"""Exact source and formal declaration inventory for middle-way bridge v0.43.

A matching source tree and Lean file AST do NOT mean the Lean proof compiled.
The independent pinned Lean/Strict CI is the only machine-check certificate.
All inherited v0.42-and-earlier Git blob checks remain in force.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_belief_gerbe_store_sources_v0_42 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "e9cd8a9c314fd78ee5038e79fe0d60fa3632a1f7"
PINNED = {
    "runtime/kuuos_lean_python_belief_gerbe_store_origin_v0_42.py":
        "2b159c3149c9b7c874c761426dab2cd750bb1fea",
    "runtime/kuuos_lean_python_five_store_chain_compat_v0_38.py":
        "325f04426ffd982d554f4bdaf878658046714b77",
    "runtime/kuuos_lean_python_os_path_composition_v0_6.py":
        "068158c2e4f90f5040f83504218e60752a5472ed",
    "runtime/kuuos_lean_python_decision_plan_handoff_v0_3.py":
        "139afc7671c6c2b15a1f8bb7fc76569a616af7e9",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "scripts/check_kuuos_lean_python_belief_gerbe_store_sources_v0_42.py":
        "e0594c6f1923d82b05b66e22e31ee7fdfa3a70b6",
    "formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean":
        "3ec65ab43ccd12fd62f62c3322838d52e4c92662",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
    "formal/KUOS/CodeAI/VersionBoundRepairMemoryV0_1.lean":
        "fa10792d73151a289b914c7a8d29d67b353e6ebf",
    "formal/KUOS/BeliefOS/ContextGerbeCoherenceV0_3.lean":
        "b4023e192f78ac10495c851ba68d63ee9fb22048",
    "formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean":
        "9891ab2aa20c8d2ea4df08abe3bf12d99aad6726",
    "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean":
        "4b6588305193fb8d41e1fef9c66433a8b5ea67e5",
    "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean":
        "0ff6a060bbe52bee4d4bcbe1ebbbd319689f5676",
    "formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean":
        "cb022ee1b0d43d5a67f38f879cc7e06f60092f9c",
}
NEW = (
    "formal/KUOS/Architecture/LeanPythonMiddleWaySemanticBridgeV0_43.lean",
    "runtime/kuuos_lean_python_middle_way_semantic_bridge_v0_43.py",
    "scripts/check_kuuos_lean_python_middle_way_semantic_sources_v0_43.py",
    "tests/lean_python_extensions/test_middle_way_semantic_bridge_v0_43.py",
    "tests/lean_python_extensions/test_middle_way_semantic_sources_v0_43.py",
    "docs/KUUOS_LEAN_PYTHON_MIDDLE_WAY_SEMANTIC_BRIDGE_v0_43.md",
)
TEST_CLASSES = {
    NEW[3]: "MiddleWaySemanticBridgeTests",
    NEW[4]: "MiddleWaySemanticSourceTests",
}
LEAN_DECLARATIONS = (
    "theorem combineEvidence_checked_iff",
    "theorem observed_blocked_not_erased_left",
    "theorem observed_blocked_not_erased_right",
    "theorem noData_cannot_be_promoted_by_local_success",
    "theorem seamCompatibility_transitive",
    "theorem twoStageConditionalTransport",
    "theorem localCheck_does_not_grant_execution",
    "theorem locallyUsable_with_no_global_or_execution_certificate",
    "theorem no_unconditional_semantic_relation",
    "theorem verified_middleWay_intake_is_not_execution",
    "theorem codeAI_source_commit_mismatch_blocks_transfer",
)
LEAN_IMPORTS = (
    "import Mathlib",
    "import KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
    "import KUOS.CodeAI.VersionBoundRepairMemoryV0_1",
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
    inventory: dict[str, tuple[str, ...]] = {}
    for path, cls in TEST_CLASSES.items():
        raw, problem = _read(root, path)
        if problem:
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            continue
        matching = [
            n for n in tree.body
            if isinstance(n, ast.ClassDef) and n.name == cls
        ]
        if len(matching) != 1:
            continue
        methods = [n.name for n in matching[0].body
                   if isinstance(n, ast.FunctionDef)
                   and n.name.startswith("test_")]
        if len(methods) >= 5 and len(methods) == len(set(methods)):
            inventory[path] = tuple(sorted(methods))
    return inventory


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not _trusted_root(root):
        return ("root:trusted_path_required",)
    problems = list(prior.check_sources(root))
    for path, expected in PINNED.items():
        raw, issue = _read(root, path)
        if issue:
            problems.append("v043_original_source_missing:" + path)
        elif _blob(raw) != expected:
            problems.append("v043_original_source_changed:" + path)
    for path in NEW:
        raw, issue = _read(root, path)
        if issue:
            problems.append("v043_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            parsed = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            problems.append("v043_python_unparsable:" + path)
            continue
        if path == NEW[1] and not all(
            any(isinstance(n, ast.FunctionDef) and n.name == name
                for n in parsed.body)
            for name in ("audit_native_middle_way_semantics", "combine_evidence")
        ):
            problems.append("v043_middle_way_operational_auditor_missing")
    raw, issue = _read(root, NEW[0])
    if not issue:
        try:
            text = raw.decode("utf-8")
        except UnicodeError:
            problems.append("v043_lean_source_encoding_invalid")
        else:
            lines = tuple(line.strip() for line in text.splitlines())
            for name in LEAN_DECLARATIONS:
                if not any(line.startswith(name + " ") or
                           line.startswith(name + ":")
                           for line in lines):
                    problems.append("v043_lean_declaration_missing:" + name)
            for name in LEAN_IMPORTS:
                if name not in lines:
                    problems.append("v043_lean_import_missing:" + name)
            if any(line.startswith(("sorry", "admit", "axiom "))
                   for line in lines):
                problems.append("v043_lean_unproved_proof_term_detected")
    if set(test_inventory(root)) != set(TEST_CLASSES):
        problems.append("v043_new_test_inventory_incomplete")
    return tuple(sorted(set(problems)))


def main() -> int:
    problems = check_sources()
    for issue in problems:
        print("BLOCKED:", issue)
    if not problems:
        print("STATIC_MATCH: v0.43 conditional local simulation theorem source")
        print("STATIC_MATCH: exact pinned original source blobs and inherited v0.42 pins")
        print("NOT_PROOF: Lean declaration text != actual Lean CI compilation")
        print("NOT_PROOF: local Python acceptance != universal Lean/Python semantics")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
