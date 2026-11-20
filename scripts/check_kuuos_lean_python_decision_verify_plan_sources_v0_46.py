#!/usr/bin/env python3
"""Source-identity inventory for bounded native Decision→Verify→Plan v0.46.

Pins original DecisionOS / VerifyOS / PlanOS Lean and Python source files and
their original fixture builders; delegates v0.45-and-earlier source checks.
This is a static byte check, not execution, proof elaboration or permission.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path

from scripts import check_kuuos_lean_python_middle_way_verify_plan_sources_v0_45 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "959fad7db61f1f5a9f4a2ba219b04714e67c93f9"
PINNED = {
    "formal/KUOS/DecisionOS/BoundedPlanSynthesisRequestHandoffV0_8.lean":
        "43770afe9e74a4d2a578f6f31c1482756eb118f7",
    "formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean":
        "3ec65ab43ccd12fd62f62c3322838d52e4c92662",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
    "formal/KUOS/Architecture/LeanPythonVerifyPlanSixRoutesV0_45.lean":
        "633d471f8ea1624f143b7068f98c9eb126efc85c",
    "runtime/kuuos_decisionos_bounded_plan_synthesis_request_handoff_v0_8.py":
        "1f7ab785c37880a239a467251a49eb3512169365",
    "runtime/kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4.py":
        "f8896f6a514156e193d85900fac36d83a760cf2f",
    "runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py":
        "d4e720d949022eb08e287362a4e5dc973241f408",
    "scripts/check_decisionos_bounded_plan_synthesis_request_handoff_v0_8.py":
        "45be5e8a4af81ff66e6eb0c6dc1ea92c00586f08",
    "scripts/check_verifyos_middle_way_conditional_continuity_verification_v0_4.py":
        "cc9d545cc51a1473cef7563e1d9e00b3499c03f8",
    "runtime/kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45.py":
        "87b0cfd11ad970586b8e33853ee05d47a4761438",
    "scripts/check_kuuos_lean_python_middle_way_verify_plan_sources_v0_45.py":
        "f7344aec937d35aefc6c813ce37ab781e8cfecab",
    "tests/lean_python_extensions/test_middle_way_verify_plan_six_routes_v0_45.py":
        "166f4a65b4aa67342754992eb65de2bbbe8899be",
    "tests/lean_python_extensions/test_middle_way_verify_plan_sources_v0_45.py":
        "6990840126fbaa6a11429bb05c3fb0487c0fa9e8",
    "docs/KUUOS_LEAN_PYTHON_MIDDLE_WAY_VERIFY_PLAN_SIX_ROUTES_v0_45.md":
        "21f63016cf213c3eb88e8f77fba2197d3cce4d61",
}
NEW = (
    "formal/KUOS/Architecture/LeanPythonDecisionVerifyPlanNativeHandoffV0_46.lean",
    "runtime/kuuos_lean_python_decision_verify_plan_native_handoff_v0_46.py",
    "scripts/check_kuuos_lean_python_decision_verify_plan_sources_v0_46.py",
    "tests/lean_python_extensions/test_decision_verify_plan_native_handoff_v0_46.py",
    "tests/lean_python_extensions/test_decision_verify_plan_sources_v0_46.py",
    "docs/KUUOS_LEAN_PYTHON_DECISION_VERIFY_PLAN_NATIVE_HANDOFF_v0_46.md",
)
TEST_CLASSES = {
    NEW[3]: "NativeDecisionVerifyPlanSixRouteTests",
    NEW[4]: "NativeDecisionVerifyPlanSourceTests",
}
LEAN_IMPORTS = (
    "import Mathlib",
    "import KUOS.DecisionOS.BoundedPlanSynthesisRequestHandoffV0_8",
    "import KUOS.Architecture.LeanPythonVerifyPlanSixRoutesV0_45",
)
LEAN_DECLARATIONS = (
    "def originalDecisionAuthorityBoundary",
    "theorem originalDecisionAuthorityBoundary_of_valid",
    "structure WholeReceiptSeam",
    "theorem decisionVerifyPlanConditionalWitness",
    "theorem decisionHandoff_onlyRetainIsBoundedIntake",
    "theorem decisionAndRouteCannotLicenseExecution",
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
    found = {}
    for path, classname in TEST_CLASSES.items():
        raw, problem = _read(root, path)
        if problem:
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (UnicodeError, SyntaxError, ValueError, RecursionError):
            continue
        classes = [
            item for item in tree.body
            if isinstance(item, ast.ClassDef) and item.name == classname
        ]
        if len(classes) != 1:
            continue
        tests = [
            node.name for node in classes[0].body
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
        ]
        if len(tests) >= 10 and len(tests) == len(set(tests)):
            found[path] = tuple(sorted(tests))
    return found


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not _trusted_root(root):
        return ("root:trusted_path_required",)
    issues = list(prior.check_sources(root))
    for path, sha in PINNED.items():
        raw, problem = _read(root, path)
        if problem:
            issues.append("v046_original_source_missing:" + path)
        elif _blob(raw) != sha:
            issues.append("v046_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            issues.append("v046_new_file_missing:" + path)
            continue
        if path.endswith(".py"):
            try:
                tree = ast.parse(raw.decode("utf-8"))
            except (UnicodeError, SyntaxError, ValueError, RecursionError):
                issues.append("v046_unparsable_python:" + path)
                continue
            if path == NEW[1] and not any(
                isinstance(node, ast.FunctionDef)
                and node.name == "audit_original_decision_verify_plan_native_handoff"
                for node in tree.body
            ):
                issues.append("v046_three_stage_native_auditor_missing")
    raw, problem = _read(root, NEW[0])
    if not problem:
        try:
            source = raw.decode("utf-8")
            code = prior._lean_code_without_comments_or_strings(source)
        except (UnicodeError, ValueError):
            issues.append("v046_lean_lexical_scan_incomplete")
        else:
            lines = tuple(line.strip() for line in code.splitlines())
            imports = tuple(line.strip() for line in source.splitlines())
            for name in LEAN_IMPORTS:
                if name not in imports:
                    issues.append("v046_lean_import_missing:" + name)
            for name in LEAN_DECLARATIONS:
                if not any(line == name or line.startswith(name + " ")
                           or line.startswith(name + ":") for line in lines):
                    issues.append("v046_lean_declaration_missing:" + name)
            if prior._contains_unproved_lean(source):
                issues.append("v046_unproved_lean_source")
    if set(test_inventory(root)) != set(TEST_CLASSES):
        issues.append("v046_test_inventory_incomplete")
    return tuple(sorted(set(issues)))


def main() -> int:
    issues = check_sources()
    for issue in issues:
        print("BLOCKED:", issue)
    if not issues:
        print("STATIC_MATCH: v0.46 DecisionOS→VerifyOS→PlanOS source identity")
        print("STATIC_MATCH: 14 unchanged source blobs and v0.45 prior pins")
        print("NOT_PROOF: no external issuer identity, global descent or host authority")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
