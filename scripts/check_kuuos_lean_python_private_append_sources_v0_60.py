#!/usr/bin/env python3
"""v0.60 exact original source SHA and new declaration/source preflight.

Static digest and AST syntax checks cannot certify actual Lean compilation,
the Python runtime's semantics, external issuer custody, or host authority.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "formal/KUOS/Architecture/LeanPythonTaggedSpanObservationGluingV0_59.lean":
        "a1c931c4382e7d150706fb19cacda9d697ed95b4",
    "runtime/kuuos_lean_python_tagged_span_gluing_v0_59.py":
        "4c37ee18d79a67fe7f2d481de4737ac3b381573f",
    "formal/KUOS/Architecture/LeanPythonTaggedForkArchiveBoundaryV0_58.lean":
        "06e01b49e7d2119e37340351906ad587f0f440bb",
    "runtime/kuuos_lean_python_tagged_fork_archive_v0_58.py":
        "c05f2ac95d87af2fc6e74399116aed13272ea8b5",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
}
LEAN = "formal/KUOS/Architecture/LeanPythonTaggedPrivateAppendInvarianceV0_60.lean"
RUNTIME = "runtime/kuuos_lean_python_tagged_private_append_v0_60.py"
TEST = "tests/lean_python_extensions/test_tagged_private_append_v0_60.py"
IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59",
    "import KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)
DECLARATIONS = (
    "def appendPrivate",
    "def oldLeftIndex",
    "def oldRightIndex",
    "theorem shared_positions_unchanged",
    "theorem left_history_has_exact_append",
    "theorem right_history_has_exact_append",
    "theorem old_left_private_observations_retained",
    "theorem old_right_private_observations_retained",
    "theorem overlap_compatible_after_private_append_iff",
    "theorem compatible_old_observations_remain_compatible",
    "theorem incompatibility_does_not_disappear_under_private_append",
    "theorem tagged_gluing_existence_after_private_append_iff",
    "theorem old_tagged_gluing_constructs_new_tagged_gluing",
    "theorem old_gluing_obstruction_persists_after_private_append",
    "theorem old_shared_disagreement_remains_obstruction",
    "theorem extended_private_branches_remain_disjoint",
    "theorem prior_linear_fork_obstruction_still_holds",
    "theorem append_only_tagged_gluing_does_not_grant_planos_execution",
)


def _blob(raw: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(raw)).encode() + b"\x00" + raw,
    ).hexdigest()


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
        lean = (ROOT / LEAN).read_text(encoding="utf-8")
        lines = tuple(line.strip() for line in lean.splitlines())
        for imp in IMPORTS:
            if imp not in lines:
                problems.append("missing_import:" + imp)
        for declaration in DECLARATIONS:
            if not any(x == declaration or x.startswith(declaration + " ")
                       for x in lines):
                problems.append("missing_declaration:" + declaration)
        if lean.count("#print axioms ") != len(DECLARATIONS):
            problems.append("incomplete_axiom_inventory")
        for bad in ("\nsorry", "\nadmit", "\naxiom ", "\nunsafe"):
            if bad in lean:
                problems.append("forbidden_lean_escape")
    except (OSError, UnicodeError):
        problems.append("new_lean_source_unavailable")
    for path in (RUNTIME, TEST):
        try:
            ast.parse((ROOT / path).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, SyntaxError, RecursionError):
            problems.append("new_python_source_invalid:" + path)
    return tuple(problems)


if __name__ == "__main__":
    problems = check()
    if problems:
        raise SystemExit("\n".join(problems))
    print("V060_ORIGINAL_GIT_BLOBS_AND_DECLARATIONS_MATCH; CI required")
