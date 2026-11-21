#!/usr/bin/env python3
"""v0.54 bounded exact source / declaration / original OS guard.

Static checks do not certify SHA-256 security, Python behavior or Lean proofs.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "formal/KUOS/Architecture/LeanPythonLocalReplayLedgerBoundaryV0_53.lean":
        "532454f66a7333dcdc9491303592881c91e5d4cb",
    "runtime/kuuos_lean_python_local_replay_reservation_v0_53.py":
        "c865586bece69e7432657f7d5425c499dc8b81f7",
    "formal/KUOS/Architecture/LeanPythonLocallyMacBoundPlanClaimsV0_52.lean":
        "925d550004f0fcc9fb73e51db7d6bf065d168dcc",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
    "runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py":
        "d4e720d949022eb08e287362a4e5dc973241f408",
}
LEAN = "formal/KUOS/Architecture/LeanPythonDetachedReplayWitnessBoundaryV0_54.lean"
RUNTIME = "runtime/kuuos_lean_python_detached_replay_witness_v0_54.py"
TEST = "tests/lean_python_extensions/test_detached_replay_witness_v0_54.py"
IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)
DECLARATIONS = (
    "def replayRoot",
    "def selfConsistent",
    "def callerCheckpointMatches",
    "theorem replayRoot_append",
    "theorem supplied_checkpoint_agrees_with_replay",
    "theorem checkpoint_mismatch_remains_obstruction",
    "theorem prefix_extension_replays",
    "theorem recorded_fresh_pair_contains_both_local_keys",
    "theorem detached_witness_grants_no_original_execution",
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
        lean = (ROOT / LEAN).read_text(encoding="utf-8")
        lines = tuple(line.strip() for line in lean.splitlines())
        for statement in IMPORTS:
            if statement not in lines:
                issues.append("missing_import:" + statement)
        for statement in DECLARATIONS:
            if not any(line == statement or line.startswith(statement + " ")
                       for line in lines):
                issues.append("missing_declaration:" + statement)
        if lean.count("#print axioms ") != len(DECLARATIONS):
            issues.append("incomplete_axiom_audit")
        for bad in ("\nsorry", "\nadmit", "\naxiom ", "\nunsafe"):
            if bad in lean:
                issues.append("forbidden_lean_escape")
    except (OSError, UnicodeError):
        issues.append("new_lean_source_unavailable")
    for path in (RUNTIME, TEST):
        try:
            ast.parse((ROOT / path).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, SyntaxError, ValueError, RecursionError):
            issues.append("new_python_source_invalid:" + path)
    return tuple(issues)


if __name__ == "__main__":
    problems = check()
    if problems:
        raise SystemExit("\n".join(problems))
    print("V054_BOUNDED_SOURCE_INTEGRITY_OK; Lean/Runtime/CI distinct")
