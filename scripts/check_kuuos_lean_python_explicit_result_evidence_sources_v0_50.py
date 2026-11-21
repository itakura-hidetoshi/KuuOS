#!/usr/bin/env python3
"""Exact-source v0.50 bounded evidence checker; not a Lean proof itself."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "formal/KUOS/Architecture/LeanPythonPlanResultObservationObstructionV0_49.lean":
        "5af2d7bfc67c86167cde4ff7e1045b0330c8a1be",
    "formal/KUOS/Architecture/LeanPythonOriginalVerifyPlanCertificateSeamV0_48.lean":
        "de35fe67129b96111eff85827f51aad47016dd3c",
    "runtime/kuuos_lean_python_plan_result_observation_obstruction_v0_49.py":
        "e8d357ded78d2634cda45b6289ba37099e07ddc0",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
    "runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py":
        "d4e720d949022eb08e287362a4e5dc973241f408",
}
NEW_LEAN = "formal/KUOS/Architecture/LeanPythonExplicitPlanResultEvidenceV0_50.lean"
NEW_RUNTIME = "runtime/kuuos_lean_python_explicit_plan_result_evidence_v0_50.py"
NEW_TEST = "tests/lean_python_extensions/test_explicit_plan_result_evidence_v0_50.py"
EXPECTED_IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49",
    "import KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)
DECLARATIONS = (
    "structure ExplicitPlanResultEvidence",
    "def explicitResultEvidence",
    "structure EvidenceMatchesOriginal",
    "theorem explicit_result_evidence_matches_original",
    "theorem matching_explicit_evidence_determines_result_sets",
    "theorem explicit_evidence_distinguishes_fresh_lineage",
    "theorem no_common_exact_evidence_for_distinct_original_results",
    "theorem original_bounded_projection_still_ambiguous",
    "theorem matched_evidence_does_not_transfer_execution_authority",
)

def _blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()

def check(root: Path = ROOT) -> tuple[str, ...]:
    if type(root) is not type(ROOT) or root != ROOT:
        return ("trusted_root_required",)
    issues: list[str] = []
    for path, sha in PINNED.items():
        try:
            if _blob((ROOT / path).read_bytes()) != sha:
                issues.append("changed_pinned_source:" + path)
        except OSError:
            issues.append("missing_pinned_source:" + path)
    try:
        source = (ROOT / NEW_LEAN).read_text(encoding="utf-8")
        lines = tuple(x.strip() for x in source.splitlines())
        for name in EXPECTED_IMPORTS:
            if name not in lines:
                issues.append("missing_import:" + name)
        for name in DECLARATIONS:
            if not any(line == name or line.startswith(name + " ") for line in lines):
                issues.append("missing_declaration:" + name)
        if source.count("#print axioms ") != 7:
            issues.append("axiom_audit_incomplete")
        for invalid in ("\nsorry", "\nadmit", "\naxiom "):
            if invalid in source:
                issues.append("disallowed_lean_placeholder")
    except (OSError, UnicodeError):
        issues.append("lean_source_missing_or_invalid")
    for path in (NEW_RUNTIME, NEW_TEST):
        try:
            ast.parse((ROOT / path).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, RecursionError, SyntaxError):
            issues.append("python_source_missing_or_invalid:" + path)
    return tuple(issues)

if __name__ == "__main__":
    issues = check()
    if issues:
        raise SystemExit("\n".join(issues))
    print("V050_SOURCE_PINS_OK; independent Lean and Runtime still required")
