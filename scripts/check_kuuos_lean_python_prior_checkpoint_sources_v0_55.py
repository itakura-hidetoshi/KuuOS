#!/usr/bin/env python3
"""v0.55 exact original blob guard and bounded declaration inventory.

No static check substitutes for strict Lean, real Python tests or external
checkpoint custody authentication.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "formal/KUOS/Architecture/LeanPythonDetachedReplayWitnessBoundaryV0_54.lean":
        "63c2ba8d19ce2f688df6b083adb21d5ff2f96a03",
    "runtime/kuuos_lean_python_detached_replay_witness_v0_54.py":
        "dbd969a630cb6114c6c57fbc273802aa1cfce862",
    "formal/KUOS/Architecture/LeanPythonLocalReplayLedgerBoundaryV0_53.lean":
        "532454f66a7333dcdc9491303592881c91e5d4cb",
    "runtime/kuuos_lean_python_local_replay_reservation_v0_53.py":
        "c865586bece69e7432657f7d5425c499dc8b81f7",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
}
LEAN = "formal/KUOS/Architecture/LeanPythonPriorCheckpointPrefixBoundaryV0_55.lean"
RUNTIME = "runtime/kuuos_lean_python_prior_checkpoint_prefix_v0_55.py"
TEST = "tests/lean_python_extensions/test_prior_checkpoint_prefix_v0_55.py"
IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54",
    "import KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)
DECLARATIONS = (
    "def declaredPrefixExtension",
    "def strictPrefixExtension",
    "def callerPriorSnapshotMatches",
    "theorem strict_extension_has_longer_history",
    "theorem prior_ticket_remains_in_extended_history",
    "theorem prefix_extension_replays_from_prior_head",
    "theorem divergent_history_blocks_declared_prefix",
    "theorem checkpoint_value_mismatch_remains_obstruction",
    "theorem compatible_strict_extension_with_checkpoint_value",
    "theorem strict_extension_histories_distinct",
    "theorem local_prefix_check_does_not_grant_original_execution",
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
        source = (ROOT / LEAN).read_text(encoding="utf-8")
        lines = tuple(line.strip() for line in source.splitlines())
        for name in IMPORTS:
            if name not in lines:
                issues.append("missing_import:" + name)
        for name in DECLARATIONS:
            if not any(line == name or line.startswith(name + " ") for line in lines):
                issues.append("missing_declaration:" + name)
        if source.count("#print axioms ") != len(DECLARATIONS):
            issues.append("incomplete_axiom_inventory")
        for bad in ("\nsorry", "\nadmit", "\naxiom ", "\nunsafe"):
            if bad in source:
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
    result = check()
    if result:
        raise SystemExit("\n".join(result))
    print("V055_SOURCE_BLOBS_AND_SYNTAX_OK; strict Lean/runtime separate")
