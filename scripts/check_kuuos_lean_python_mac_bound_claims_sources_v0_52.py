#!/usr/bin/env python3
"""v0.52 pinned-original and new Lean source static audit.

Static pin verification does NOT replace independent Lean compilation,
cryptographic source trust, or verification of HMAC's security in Lean.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "formal/KUOS/Architecture/LeanPythonTwoDeclaredPlanResultClaimsV0_51.lean":
        "1236dc54b37181b660fddbe6f388d7db385d64f1",
    "runtime/kuuos_lean_python_two_declared_plan_result_claims_v0_51.py":
        "f79b84fd7943c2db24f8f899e3280a5a6060427e",
    "formal/KUOS/Architecture/LeanPythonExplicitPlanResultEvidenceV0_50.lean":
        "8758a1f0794553fd5db800f24a2b047cb70d9d3d",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
    "runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py":
        "d4e720d949022eb08e287362a4e5dc973241f408",
}
LEAN = "formal/KUOS/Architecture/LeanPythonLocallyMacBoundPlanClaimsV0_52.lean"
RUNTIME = "runtime/kuuos_lean_python_local_mac_bound_plan_claims_v0_52.py"
TEST = "tests/lean_python_extensions/test_local_mac_bound_plan_claims_v0_52.py"
IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51",
    "import KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)
DECLARATIONS = (
    "structure ReportedMacBoundClaim",
    "def localMacPassed",
    "theorem exact_original_matches_agree_despite_mac_report",
    "theorem mac_reports_cannot_erase_original_obstruction",
    "theorem mac_flags_and_matching_labels_do_not_force_result_agreement",
    "theorem local_mac_does_not_grant_execution",
)


def _blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()


def check(root: Path = ROOT) -> tuple[str, ...]:
    if type(root) is not type(ROOT) or root != ROOT:
        return ("trusted_root_required",)
    problems: list[str] = []
    for path, expected in PINNED.items():
        try:
            if _blob((ROOT / path).read_bytes()) != expected:
                problems.append("changed_pinned_source:" + path)
        except OSError:
            problems.append("missing_pinned_source:" + path)
    try:
        source = (ROOT / LEAN).read_text(encoding="utf-8")
        lines = tuple(x.strip() for x in source.splitlines())
        for name in IMPORTS:
            if name not in lines:
                problems.append("missing_import:" + name)
        for name in DECLARATIONS:
            if not any(line == name or line.startswith(name + " ") for line in lines):
                problems.append("missing_declaration:" + name)
        if source.count("#print axioms ") != len(DECLARATIONS) - 1:
            problems.append("axiom_audit_incomplete")
        for marker in ("\nsorry", "\nadmit", "\naxiom ", "\nunsafe"):
            if marker in source:
                problems.append("forbidden_lean_placeholder")
    except (OSError, UnicodeError):
        problems.append("new_lean_source_unavailable")
    for path in (RUNTIME, TEST):
        try:
            ast.parse((ROOT / path).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, RecursionError, SyntaxError):
            problems.append("new_python_source_invalid:" + path)
    return tuple(problems)


if __name__ == "__main__":
    bad = check()
    if bad:
        raise SystemExit("\n".join(bad))
    print("V052_EXACT_SOURCE_PINS_VALID; still requires Lean and Runtime CI")
