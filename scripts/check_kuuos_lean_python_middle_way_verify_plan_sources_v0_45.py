#!/usr/bin/env python3
"""v0.45 source identity and Lean six-route theorem inventory.

Check exact original VerifyOS/PlanOS Lean and Python kernel Git blobs,
their original fixture constructors, and all previous v0.44-and-earlier pins.
This static check is NOT Lean elaboration, runtime semantic refinement,
external issuer proof or permission.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

from scripts import check_kuuos_lean_python_finite_evidence_sources_v0_44 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "0be0755998af0d07ad7c66514293f15731d9f5e3"
PINNED = {
    "formal/KUOS/Architecture/LeanPythonMiddleWaySemanticBridgeV0_43.lean":
        "538e59f2188f39bca2c24fe9739828a5ec1e8c51",
    "formal/KUOS/Architecture/LeanPythonFiniteEvidenceWitnessV0_44.lean":
        "422b8f9598e631a50bcabffa0f536f149c1c3954",
    "formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean":
        "3ec65ab43ccd12fd62f62c3322838d52e4c92662",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
    "runtime/kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4.py":
        "f8896f6a514156e193d85900fac36d83a760cf2f",
    "runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py":
        "d4e720d949022eb08e287362a4e5dc973241f408",
    "scripts/check_verifyos_middle_way_conditional_continuity_verification_v0_4.py":
        "cc9d545cc51a1473cef7563e1d9e00b3499c03f8",
    "scripts/check_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py":
        "58855d8086992d5062959bdeaf8c7882af42ec5c",
    "scripts/check_kuuos_lean_python_finite_evidence_sources_v0_44.py":
        "3b058ea508bd149d5aabb50b15f68072183d32e3",
    "runtime/kuuos_lean_python_finite_evidence_witness_v0_44.py":
        "508044bb55b113699ec09a3b8e3c27d7b6462ff1",
}
NEW = (
    "formal/KUOS/Architecture/LeanPythonVerifyPlanSixRoutesV0_45.lean",
    "runtime/kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45.py",
    "scripts/check_kuuos_lean_python_middle_way_verify_plan_sources_v0_45.py",
    "tests/lean_python_extensions/test_middle_way_verify_plan_six_routes_v0_45.py",
    "tests/lean_python_extensions/test_middle_way_verify_plan_sources_v0_45.py",
    "docs/KUUOS_LEAN_PYTHON_MIDDLE_WAY_VERIFY_PLAN_SIX_ROUTES_v0_45.md",
)
TEST_CLASSES = {
    NEW[3]: "OriginalVerifyPlanSixRoutesTests",
    NEW[4]: "VerifyPlanSixRoutesSourceTests",
}
LEAN_DEFINITIONS = (
    "def encodeTransition",
    "def encodeValidity",
    "def encodeIntake",
    "def pythonVerifyModel",
    "def pythonIntakeModel",
    "def verifyRouteSimulation",
    "def intakeRouteSimulation",
    "def originalVerifyPlanIdentitySeam",
)
LEAN_THEOREMS = (
    "theorem encodedVerify_commutes",
    "theorem encodedIntake_commutes",
    "theorem sixRouteConditionalTwoStageWitness",
    "theorem onlyRetainRouteAdmitted",
    "theorem supersededRequiresReverification",
    "theorem completedAndTerminatedDoNotAdmit",
    "theorem unknownVerifyRouteIsNone",
    "theorem unknownIntakeStatusIsNone",
    "theorem sixRouteCannotLicenseExecution",
)
LEAN_IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonMiddleWaySemanticBridgeV0_43",
    "import KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)


def _read(root: Path, path: str):
    return prior._read(root, path)


def _blob(raw: bytes) -> str:
    return prior._blob(raw)


def _trusted_root(root: Path) -> bool:
    return prior._trusted_root(root)



def _lean_code_without_comments_or_strings(source: str) -> str:
    """Mask Lean comments and string literals, preserving executable tokens.

    Handles nested Lean block comments, line comments and escaped strings.
    This is a conservative source lint, not a Lean parser or proof checker.
    """
    out: list[str] = []
    block_depth = 0
    in_string = False
    in_quoted_ident = False
    i = 0
    while i < len(source):
        char = source[i]
        if block_depth:
            if source.startswith("/-", i):
                block_depth += 1
                out.extend("  ")
                i += 2
            elif source.startswith("-/", i):
                block_depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if char == "\n" else " ")
                i += 1
        elif in_string:
            if char == "\\" and i + 1 < len(source):
                out.append(" ")
                out.append("\n" if source[i + 1] == "\n" else " ")
                i += 2
            else:
                if char == '"':
                    in_string = False
                out.append("\n" if char == "\n" else " ")
                i += 1
        elif in_quoted_ident:
            if char == "»":
                in_quoted_ident = False
            out.append("\n" if char == "\n" else " ")
            i += 1
        elif source.startswith("--", i):
            while i < len(source) and source[i] != "\n":
                out.append(" ")
                i += 1
        elif source.startswith("/-", i):
            block_depth = 1
            out.extend("  ")
            i += 2
        elif char == '"':
            in_string = True
            out.append(" ")
            i += 1
        elif char == "«":
            in_quoted_ident = True
            out.append(" ")
            i += 1
        else:
            out.append(char)
            i += 1
    if block_depth or in_string or in_quoted_ident:
        raise ValueError("unterminated_lean_comment_string_or_quoted_identifier")
    return "".join(out)


def _contains_unproved_lean(source: str) -> bool:
    """Match forbidden *whole* Lean tokens, never identifier prefixes."""
    code = _lean_code_without_comments_or_strings(source)
    return re.search(r"(?<![\w'])(?:axiom|sorry|admit)(?![\w'])", code) is not None


def test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    if not _trusted_root(root):
        return {}
    inventory: dict[str, tuple[str, ...]] = {}
    for path, name in TEST_CLASSES.items():
        raw, issue = _read(root, path)
        if issue:
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            continue
        classes = [item for item in tree.body
                   if isinstance(item, ast.ClassDef) and item.name == name]
        if len(classes) != 1:
            continue
        tests = [item.name for item in classes[0].body
                 if isinstance(item, ast.FunctionDef)
                 and item.name.startswith("test_")]
        if len(tests) >= 5 and len(tests) == len(set(tests)):
            inventory[path] = tuple(sorted(tests))
    return inventory


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not _trusted_root(root):
        return ("root:trusted_path_required",)
    issues = list(prior.check_sources(root))
    for path, expected in PINNED.items():
        raw, problem = _read(root, path)
        if problem:
            issues.append("v045_original_source_missing:" + path)
        elif _blob(raw) != expected:
            issues.append("v045_original_source_changed:" + path)
    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            issues.append("v045_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, ValueError, UnicodeError, RecursionError):
            issues.append("v045_new_python_unparsable:" + path)
            continue
        if path == NEW[1] and not any(
            isinstance(node, ast.FunctionDef)
            and node.name == "audit_original_verify_plan_six_routes"
            for node in tree.body
        ):
            issues.append("v045_native_six_route_auditor_missing")
    raw, problem = _read(root, NEW[0])
    if not problem:
        try:
            lines = tuple(x.strip() for x in raw.decode("utf-8").splitlines())
        except UnicodeError:
            issues.append("v045_lean_source_not_utf8")
        else:
            for name in LEAN_DEFINITIONS + LEAN_THEOREMS:
                if not any(line == name or line.startswith(name + " ")
                           or line.startswith(name + ":") for line in lines):
                    issues.append("v045_lean_declaration_missing:" + name)
            for name in LEAN_IMPORTS:
                if name not in lines:
                    issues.append("v045_lean_import_missing:" + name)
            try:
                has_unproved = _contains_unproved_lean(raw.decode("utf-8"))
            except ValueError:
                issues.append("v045_lean_lexical_scan_incomplete")
            else:
                if has_unproved:
                    issues.append("v045_unproved_lean_source")
    if set(test_inventory(root)) != set(TEST_CLASSES):
        issues.append("v045_test_inventory_incomplete")
    return tuple(sorted(set(issues)))


def main() -> int:
    issues = check_sources()
    for item in issues:
        print("BLOCKED:", item)
    if not issues:
        print("STATIC_MATCH: v0.45 VerifyOS→PlanOS six route source identity")
        print("STATIC_MATCH: ten original Git blobs and all v0.44 earlier pins")
        print("NOT_PROOF: Lean source existence != strict Lean elaboration success")
        print("NOT_PROOF: original Python certificates != external authority")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
