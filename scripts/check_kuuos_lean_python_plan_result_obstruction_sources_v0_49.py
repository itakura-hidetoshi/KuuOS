#!/usr/bin/env python3
"""v0.49 exact original Git blob/source pin and declaration checker.

Static source matching does not establish Lean elaboration; check pinned
Strict Lean, #print axioms, Runtime and Governance in independent CI.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "formal/KUOS/Architecture/LeanPythonOriginalVerifyPlanCertificateSeamV0_48.lean":
        "de35fe67129b96111eff85827f51aad47016dd3c",
    "runtime/kuuos_lean_python_original_verify_plan_certificate_seam_v0_48.py":
        "c0d19f0637c967a5d2162a7f523837fc7cb76525",
    "formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean":
        "3ec65ab43ccd12fd62f62c3322838d52e4c92662",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
    "runtime/kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4.py":
        "f8896f6a514156e193d85900fac36d83a760cf2f",
    "runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py":
        "d4e720d949022eb08e287362a4e5dc973241f408",
}
NEW_LEAN = "formal/KUOS/Architecture/LeanPythonPlanResultObservationObstructionV0_49.lean"
NEW_PY = "runtime/kuuos_lean_python_plan_result_observation_obstruction_v0_49.py"
NEW_TEST = "tests/lean_python_extensions/test_plan_result_observation_obstruction_v0_49.py"
DECLARATIONS = (
    "structure VisiblePlanSourceProjection",
    "def visiblePlanSourceProjection",
    "def widenedPlanOfVerify",
    "theorem widened_plan_valid",
    "theorem widened_plan_preserves_original_seam",
    "theorem same_visible_projection",
    "theorem different_resulting_lineage_if_fresh",
    "theorem different_resulting_dissent_if_fresh",
    "theorem different_resulting_minority_if_fresh",
    "theorem compatible_certificates_with_same_projection_can_differ",
    "theorem no_total_exact_decoder_on_both_originals",
)
EXPECTED_IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48",
    "import KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)


def _blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()


def check(root: Path = ROOT) -> tuple[str, ...]:
    if type(root) is not type(ROOT) or root != ROOT:
        return ("trusted_root_required",)
    problems: list[str] = []
    for name, expected in PINNED.items():
        try:
            if _blob((ROOT / name).read_bytes()) != expected:
                problems.append("changed_pinned_source:" + name)
        except OSError:
            problems.append("missing_pinned_source:" + name)
    try:
        content = (ROOT / NEW_LEAN).read_text(encoding="utf-8")
        lines = [x.strip() for x in content.splitlines()]
        for expected in EXPECTED_IMPORTS:
            if expected not in lines:
                problems.append("missing_import:" + expected)
        for decl in DECLARATIONS:
            if not any(x == decl or x.startswith(decl + " ") for x in lines):
                problems.append("missing_declaration:" + decl)
        if content.count("#print axioms ") != len(DECLARATIONS) - 1:
            problems.append("incomplete_axiom_audit")
        for blocked in ("\nsorry", "\nadmit", "\naxiom "):
            if blocked in content:
                problems.append("unproved_lean_token")
    except (OSError, UnicodeError):
        problems.append("new_lean_source_unavailable")
    for name in (NEW_PY, NEW_TEST):
        try:
            ast.parse((ROOT / name).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, SyntaxError, ValueError, RecursionError):
            problems.append("invalid_python_source:" + name)
    return tuple(problems)


if __name__ == "__main__":
    issues = check()
    if issues:
        raise SystemExit("\n".join(issues))
    print("V049_STATIC_SOURCE_OK; not independent Lean or Python authority")
