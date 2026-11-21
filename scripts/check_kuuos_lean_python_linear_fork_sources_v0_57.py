#!/usr/bin/env python3
"""v0.57 source integrity guard; does not replace Lean or Python CI."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PINNED = {
    "formal/KUOS/Architecture/LeanPythonCommonAncestorForkBoundaryV0_56.lean":
        "2ea0af030efe683342f4936d57be7f31c30cdac0",
    "runtime/kuuos_lean_python_common_ancestor_fork_v0_56.py":
        "6210f8a4925c2bb0d3754934dd18ccdfc954cece",
    "formal/KUOS/Architecture/LeanPythonPriorCheckpointPrefixBoundaryV0_55.lean":
        "1d64fa5e213382f3fa6494a0d8709d6465c484c1",
    "runtime/kuuos_lean_python_prior_checkpoint_prefix_v0_55.py":
        "9f0bee86d822d32997e4323b40aa3a049d562685",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
}
NEW_LEAN = "formal/KUOS/Architecture/LeanPythonLinearForkGluingObstructionV0_57.lean"
NEW_RUNTIME = "runtime/kuuos_lean_python_linear_fork_gluing_v0_57.py"
NEW_TEST = "tests/lean_python_extensions/test_linear_fork_gluing_v0_57.py"
IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56",
    "import KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)
DECLARATIONS = (
    "def hasDeclaredCommonLinearSuccessor",
    "theorem common_linear_successor_implies_comparability",
    "theorem incomparable_histories_have_no_common_linear_successor",
    "theorem declared_fork_blocks_linear_gluing",
    "theorem declared_fork_excludes_two_extension_witnesses",
    "theorem common_successor_excludes_declared_fork",
    "theorem comparable_left_has_declared_common_successor",
    "theorem comparable_right_has_declared_common_successor",
    "theorem comparable_histories_have_declared_common_successor",
    "theorem common_successor_iff_comparable",
    "theorem preference_cannot_resolve_linear_fork",
    "theorem linear_gluing_check_grants_no_original_execution",
)


def _blob(raw: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(raw)).encode() + b"\x00" + raw,
    ).hexdigest()


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
        source = (ROOT / NEW_LEAN).read_text(encoding="utf-8")
        lines = tuple(line.strip() for line in source.splitlines())
        for name in IMPORTS:
            if name not in lines:
                problems.append("missing_import:" + name)
        for name in DECLARATIONS:
            if not any(line == name or line.startswith(name + " ")
                       for line in lines):
                problems.append("missing_declaration:" + name)
        if source.count("#print axioms ") != len(DECLARATIONS):
            problems.append("incomplete_axiom_inventory")
        for bad in ("\nsorry", "\nadmit", "\naxiom ", "\nunsafe"):
            if bad in source:
                problems.append("forbidden_lean_escape")
    except (OSError, UnicodeError):
        problems.append("new_lean_source_unavailable")
    for filename in (NEW_RUNTIME, NEW_TEST):
        try:
            ast.parse((ROOT / filename).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, SyntaxError, ValueError, RecursionError):
            problems.append("new_python_source_invalid:" + filename)
    return tuple(problems)


if __name__ == "__main__":
    result = check()
    if result:
        raise SystemExit("\n".join(result))
    print("V057_PINNED_SOURCE_AND_SYNTAX_OK; proof/runtime certification separate")
