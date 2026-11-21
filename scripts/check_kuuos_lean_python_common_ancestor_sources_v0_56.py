#!/usr/bin/env python3
"""v0.56 exact original Git blobs / new source inventory guard.

This is a source integrity precheck, NOT a Lean compiler, Python regression
certificate, authenticated historical fork or host authorization.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "formal/KUOS/Architecture/LeanPythonPriorCheckpointPrefixBoundaryV0_55.lean":
        "1d64fa5e213382f3fa6494a0d8709d6465c484c1",
    "runtime/kuuos_lean_python_prior_checkpoint_prefix_v0_55.py":
        "9f0bee86d822d32997e4323b40aa3a049d562685",
    "formal/KUOS/Architecture/LeanPythonDetachedReplayWitnessBoundaryV0_54.lean":
        "63c2ba8d19ce2f688df6b083adb21d5ff2f96a03",
    "runtime/kuuos_lean_python_detached_replay_witness_v0_54.py":
        "dbd969a630cb6114c6c57fbc273802aa1cfce862",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
}

NEW_LEAN = "formal/KUOS/Architecture/LeanPythonCommonAncestorForkBoundaryV0_56.lean"
NEW_RUNTIME = "runtime/kuuos_lean_python_common_ancestor_fork_v0_56.py"
NEW_TEST = "tests/lean_python_extensions/test_common_ancestor_fork_v0_56.py"
IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55",
    "import KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)
DECLARATIONS = (
    "def declaredExtension",
    "def locallyComparable",
    "def declaredForkObstruction",
    "theorem declared_extension_reflexive",
    "theorem declared_extension_transitive",
    "theorem extension_implies_comparability",
    "theorem differing_first_successors_are_incomparable",
    "theorem differing_first_successors_give_fork",
    "theorem fork_histories_cannot_agree",
    "theorem fork_retains_each_prior_ticket",
    "theorem local_fork_does_not_grant_planos_execution",
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
            actual = _blob((ROOT / name).read_bytes())
            if actual != expected:
                problems.append("changed_pinned_source:" + name)
        except OSError:
            problems.append("missing_pinned_source:" + name)
    try:
        source = (ROOT / NEW_LEAN).read_text(encoding="utf-8")
        lines = tuple(line.strip() for line in source.splitlines())
        for need in IMPORTS:
            if need not in lines:
                problems.append("missing_import:" + need)
        for need in DECLARATIONS:
            if not any(line == need or line.startswith(need + " ")
                       for line in lines):
                problems.append("missing_declaration:" + need)
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
        except (OSError, UnicodeError, ValueError, SyntaxError, RecursionError):
            problems.append("new_python_source_invalid:" + filename)
    return tuple(problems)


if __name__ == "__main__":
    problems = check()
    if problems:
        raise SystemExit("\n".join(problems))
    print("V056_ORIGINAL_BLOBS_AND_SOURCE_INVENTORY_OK; independent CI needed")
