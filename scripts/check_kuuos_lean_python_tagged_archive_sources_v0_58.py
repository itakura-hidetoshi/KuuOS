#!/usr/bin/env python3
"""v0.58 exact historical source blobs and new declaration inventory.

A static checker cannot prove Lean↔Python refinement, cryptographic
authenticity, independently kept history or original OS execution authority.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "formal/KUOS/Architecture/LeanPythonLinearForkGluingObstructionV0_57.lean":
        "c36ffadd638694fad0841f1e1d479aeb6a1bbd91",
    "runtime/kuuos_lean_python_linear_fork_gluing_v0_57.py":
        "d4ade6115658b4d1678922620b6229f7bb19ef4a",
    "formal/KUOS/Architecture/LeanPythonCommonAncestorForkBoundaryV0_56.lean":
        "2ea0af030efe683342f4936d57be7f31c30cdac0",
    "runtime/kuuos_lean_python_common_ancestor_fork_v0_56.py":
        "6210f8a4925c2bb0d3754934dd18ccdfc954cece",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
}
NEW_LEAN = "formal/KUOS/Architecture/LeanPythonTaggedForkArchiveBoundaryV0_58.lean"
NEW_RUNTIME = "runtime/kuuos_lean_python_tagged_fork_archive_v0_58.py"
NEW_TEST = "tests/lean_python_extensions/test_tagged_fork_archive_v0_58.py"
IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57",
    "import KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)
DECLARATIONS = (
    "def branchProjection",
    "def archiveDeclaredFork",
    "theorem left_branch_projection_exact",
    "theorem right_branch_projection_exact",
    "theorem either_branch_extends_ancestor",
    "theorem prior_ticket_retained_in_both_branches",
    "theorem archive_of_fork_has_exact_projections",
    "theorem archive_of_fork_preserves_incomparability",
    "theorem archived_fork_still_has_no_common_linear_successor",
    "theorem fork_can_be_archived_without_linear_gluing",
    "theorem tagged_archive_does_not_grant_original_execution",
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
        source = (ROOT / NEW_LEAN).read_text(encoding="utf-8")
        lines = tuple(line.strip() for line in source.splitlines())
        for tok in IMPORTS:
            if tok not in lines:
                problems.append("missing_import:" + tok)
        for tok in DECLARATIONS:
            if not any(line == tok or line.startswith(tok + " ") for line in lines):
                problems.append("missing_declaration:" + tok)
        if source.count("#print axioms ") != len(DECLARATIONS):
            problems.append("incomplete_axiom_audit")
        for bad in ("\nsorry", "\nadmit", "\naxiom ", "\nunsafe"):
            if bad in source:
                problems.append("forbidden_lean_escape")
    except (OSError, UnicodeError):
        problems.append("new_lean_source_unavailable")
    for name in (NEW_RUNTIME, NEW_TEST):
        try:
            ast.parse((ROOT / name).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, SyntaxError, RecursionError):
            problems.append("new_python_source_invalid:" + name)
    return tuple(problems)


if __name__ == "__main__":
    issues = check()
    if issues:
        raise SystemExit("\n".join(issues))
    print("V058_SOURCE_GIT_BLOBS_MATCH; strict Lean, runtime and custody separate")
