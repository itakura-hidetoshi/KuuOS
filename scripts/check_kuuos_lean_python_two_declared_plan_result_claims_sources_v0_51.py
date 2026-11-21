#!/usr/bin/env python3
"""Source-bound audit of v0.51 original PlanOS declaration comparisons.

Static source check is not Lean elaboration, CPython refinement,
issuer authentication, a proof of global descent or host authority.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "formal/KUOS/Architecture/LeanPythonExplicitPlanResultEvidenceV0_50.lean":
        "8758a1f0794553fd5db800f24a2b047cb70d9d3d",
    "runtime/kuuos_lean_python_explicit_plan_result_evidence_v0_50.py":
        "89615b15dac5a1a1575188c972dfaea885b8bc02",
    "formal/KUOS/Architecture/LeanPythonPlanResultObservationObstructionV0_49.lean":
        "5af2d7bfc67c86167cde4ff7e1045b0330c8a1be",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
    "runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py":
        "d4e720d949022eb08e287362a4e5dc973241f408",
}
NEW_LEAN = "formal/KUOS/Architecture/LeanPythonTwoDeclaredPlanResultClaimsV0_51.lean"
NEW_PY = "runtime/kuuos_lean_python_two_declared_plan_result_claims_v0_51.py"
NEW_TEST = "tests/lean_python_extensions/test_two_declared_plan_result_claims_v0_51.py"
IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50",
    "import KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)
DECLARATIONS = (
    "structure DeclaredPlanResultClaim",
    "def sourceLabelsAgree",
    "def threeResultSetsAgree",
    "def threeResultSetsConflict",
    "theorem two_matches_one_original_imply_result_agreement",
    "theorem conflicting_claims_cannot_both_match_original",
    "def declareOriginalCertificate",
    "theorem source_label_agreement_does_not_imply_result_agreement",
    "theorem declared_agreement_no_host_authority",
)


def _git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()


def check(root: Path = ROOT) -> tuple[str, ...]:
    if type(root) is not type(ROOT) or root != ROOT:
        return ("trusted_root_required",)
    issues: list[str] = []
    for path, sha in PINNED.items():
        try:
            if _git_blob((ROOT / path).read_bytes()) != sha:
                issues.append("changed_pinned_source:" + path)
        except OSError:
            issues.append("missing_pinned_source:" + path)
    try:
        source = (ROOT / NEW_LEAN).read_text(encoding="utf-8")
        lines = tuple(line.strip() for line in source.splitlines())
        for token in IMPORTS:
            if token not in lines:
                issues.append("missing_import:" + token)
        for token in DECLARATIONS:
            if not any(line == token or line.startswith(token + " ") for line in lines):
                issues.append("missing_declaration:" + token)
        if source.count("#print axioms ") != len(DECLARATIONS) - 1:
            issues.append("incomplete_axiom_audit")
        for invalid in ("\nsorry", "\nadmit", "\naxiom "):
            if invalid in source:
                issues.append("placeholder_or_axiom_added")
    except (OSError, UnicodeError):
        issues.append("new_lean_source_unavailable")
    for path in (NEW_PY, NEW_TEST):
        try:
            ast.parse((ROOT / path).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, SyntaxError, ValueError, RecursionError):
            issues.append("new_python_source_invalid:" + path)
    return tuple(issues)


if __name__ == "__main__":
    issues = check()
    if issues:
        raise SystemExit("\n".join(issues))
    print("V051_SOURCE_PINS_CHECKED; not Lean or independent issuer certification")
