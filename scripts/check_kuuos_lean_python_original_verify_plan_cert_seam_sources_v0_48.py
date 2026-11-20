#!/usr/bin/env python3
"""v0.48 exact original source, imports and file-scope audit; not a Lean proof."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean":
        "3ec65ab43ccd12fd62f62c3322838d52e4c92662",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
    "formal/KUOS/Architecture/LeanPythonVerifyPlanSixRoutesV0_45.lean":
        "633d471f8ea1624f143b7068f98c9eb126efc85c",
    "formal/KUOS/Architecture/LeanPythonOriginalDecisionTypeBridgeV0_47.lean":
        "fd812d6dd93c5074207747825177375fdc6be5e5",
    "runtime/kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4.py":
        "f8896f6a514156e193d85900fac36d83a760cf2f",
    "runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py":
        "d4e720d949022eb08e287362a4e5dc973241f408",
    "runtime/kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45.py":
        "87b0cfd11ad970586b8e33853ee05d47a4761438",
    "lakefile.toml": "947bac41f9535a7ba2ef03a93081cdfbc1b946f7",
}
NEW_LEAN = "formal/KUOS/Architecture/LeanPythonOriginalVerifyPlanCertificateSeamV0_48.lean"
NEW_PYTHON = "runtime/kuuos_lean_python_original_verify_plan_certificate_seam_v0_48.py"
NEW_TEST = "tests/lean_python_extensions/test_original_verify_plan_certificate_seam_v0_48.py"
EXPECTED_IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonOriginalDecisionTypeBridgeV0_47",
    "import KUOS.Architecture.LeanPythonVerifyPlanSixRoutesV0_45",
    "import KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)
DECLARATIONS = (
    "structure OriginalCertificateSeam",
    "theorem original_status_transport",
    "theorem original_disposition_transport",
    "theorem original_only_retain_admitted",
    "theorem original_lineage_transport",
    "theorem original_predecessor_transport",
    "theorem original_responsibility_dissent_minority_transport",
    "theorem original_seam_no_execution_authority",
    "def inertPlanOfVerify",
    "theorem inert_plan_valid",
    "theorem inert_plan_exact_seam",
    "theorem inert_plan_retain_iff",
)


def blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()


def check(root: Path = ROOT) -> tuple[str, ...]:
    if type(root) is not type(ROOT) or root != ROOT:
        return ("trusted_root_required",)
    problems: list[str] = []
    for path, expected in PINNED.items():
        try:
            raw = (root / path).read_bytes()
            if blob(raw) != expected:
                problems.append("pinned_source_modified:" + path)
        except OSError:
            problems.append("pinned_source_missing:" + path)
    try:
        lean = (root / NEW_LEAN).read_text(encoding="utf-8")
        lines = tuple(x.strip() for x in lean.splitlines())
        for name in EXPECTED_IMPORTS:
            if name not in lines:
                problems.append("missing_original_import:" + name)
        for name in DECLARATIONS:
            if not any(x == name or x.startswith(name + " ") for x in lines):
                problems.append("missing_declaration:" + name)
        code = re.sub(r"/-![\s\S]*?-/", "", lean)
        if re.search(r"(?<![A-Za-z0-9_])(?:sorry|admit|axiom)(?![A-Za-z0-9_])", code):
            problems.append("unproved_lean_token")
        if lean.count("#print axioms ") != len(DECLARATIONS) - 1:
            problems.append("axiom_audit_count_mismatch")
    except (OSError, UnicodeError):
        problems.append("v048_lean_missing_or_invalid")
    for path in (NEW_PYTHON, NEW_TEST):
        try:
            ast.parse((root / path).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, SyntaxError, ValueError, RecursionError):
            problems.append("python_source_missing_or_invalid:" + path)
    return tuple(problems)


if __name__ == "__main__":
    issues = check()
    if issues:
        raise SystemExit("\n".join(issues))
    print("STATIC_OK: original typed source pins and additive v0.48 files")
    print("NOT_PROOF: run exact-head pinned Strict Lean and runtime tests independently")
