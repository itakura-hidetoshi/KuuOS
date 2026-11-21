#!/usr/bin/env python3
"""v0.59 immutable source pins, declaration inventory and new Python syntax.

This static audit is necessary but never sufficient for Lean certification,
complete CPython refinement, actual external history or execution authority.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "formal/KUOS/Architecture/LeanPythonTaggedForkArchiveBoundaryV0_58.lean":
        "06e01b49e7d2119e37340351906ad587f0f440bb",
    "runtime/kuuos_lean_python_tagged_fork_archive_v0_58.py":
        "c05f2ac95d87af2fc6e74399116aed13272ea8b5",
    "formal/KUOS/Architecture/LeanPythonLinearForkGluingObstructionV0_57.lean":
        "c36ffadd638694fad0841f1e1d479aeb6a1bbd91",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
}
LEAN = "formal/KUOS/Architecture/LeanPythonTaggedSpanObservationGluingV0_59.lean"
RUNTIME = "runtime/kuuos_lean_python_tagged_span_gluing_v0_59.py"
TEST = "tests/lean_python_extensions/test_tagged_span_gluing_v0_59.py"
IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58",
    "import KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)
DECLARATIONS = (
    "def leftInclusion",
    "def rightInclusion",
    "theorem common_position_identified",
    "theorem branch_private_positions_disjoint",
    "def ticketAt",
    "noncomputable def spanFromArchive",
    "theorem archived_left_history_exact",
    "theorem archived_right_history_exact",
    "def overlapCompatible",
    "def glueTagged",
    "theorem glue_left",
    "theorem glue_right",
    "theorem tagged_gluing_unique",
    "theorem tagged_observation_gluing_iff",
    "theorem incompatible_observations_block_gluing",
    "theorem shared_value_disagreement_obstructs",
    "theorem archived_fork_remains_non_linear",
    "theorem tagged_span_gluing_grants_no_original_execution",
)


def _blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode() + b"\x00" + data,
    ).hexdigest()


def check(root: Path = ROOT) -> tuple[str, ...]:
    if type(root) is not type(ROOT) or root != ROOT:
        return ("trusted_root_required",)
    problems: list[str] = []
    for name, sha in PINNED.items():
        try:
            if _blob((ROOT / name).read_bytes()) != sha:
                problems.append("changed_pinned_source:" + name)
        except OSError:
            problems.append("missing_pinned_source:" + name)
    try:
        lean = (ROOT / LEAN).read_text(encoding="utf-8")
        lines = tuple(line.strip() for line in lean.splitlines())
        for imp in IMPORTS:
            if imp not in lines:
                problems.append("missing_import:" + imp)
        for name in DECLARATIONS:
            if not any(line == name or line.startswith(name + " ")
                       for line in lines):
                problems.append("missing_declaration:" + name)
        if lean.count("#print axioms ") != len(DECLARATIONS):
            problems.append("incomplete_axiom_inventory")
        for bad in ("\nsorry", "\nadmit", "\naxiom ", "\nunsafe"):
            if bad in lean:
                problems.append("forbidden_lean_escape")
    except (OSError, UnicodeError):
        problems.append("new_lean_source_unavailable")
    for name in (RUNTIME, TEST):
        try:
            ast.parse((ROOT / name).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, SyntaxError, RecursionError):
            problems.append("new_python_source_invalid:" + name)
    return tuple(problems)


if __name__ == "__main__":
    problems = check()
    if problems:
        raise SystemExit("\n".join(problems))
    print("V059_PINNED_BLOBS_AND_DECLARATIONS_MATCH; independent CI still required")
